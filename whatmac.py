#!/usr/bin/env python3
"""whatmac - visa en MAC-adress i alla vanliga format och slå upp tillverkaren.

Användning:
    whatmac aa:bb:cc:dd:ee:ff
    whatmac aabb.ccdd.eeff
    whatmac --update        # ladda ner IEEE:s OUI-lista på nytt
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "whatmac"
OUI_FILE = CACHE_DIR / "oui.txt"
OUI_URL = "https://standards-oui.ieee.org/oui/oui.txt"
API_URL = "https://api.macvendors.com/{}"
MAX_CACHE_AGE = 30 * 24 * 3600  # 30 dagar

BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

if not sys.stdout.isatty():
    BOLD = DIM = CYAN = GREEN = YELLOW = RED = RESET = ""


def normalize(raw: str) -> str:
    """Returnera 12 hex-tecken (versaler) eller kasta ValueError."""
    hexstr = re.sub(r"[^0-9a-fA-F]", "", raw)
    if len(hexstr) != 12 or re.search(r"[^0-9a-fA-F:\-.\s]", raw):
        raise ValueError(f"Ogiltig MAC-adress: {raw!r}")
    return hexstr.upper()


def formats(mac: str) -> list[tuple[str, str]]:
    lo = mac.lower()
    pairs = [mac[i:i + 2] for i in range(0, 12, 2)]
    quads = [lo[i:i + 4] for i in range(0, 12, 4)]
    return [
        ("Kolon (Linux/macOS)", ":".join(pairs).lower()),
        ("Kolon versaler", ":".join(pairs)),
        ("Bindestreck (Windows)", "-".join(pairs)),
        ("Cisco", ".".join(quads)),
        ("HP / Aruba", "-".join(quads)),
        ("Bara hex", lo),
        ("Bara hex versaler", mac),
    ]


def download_oui() -> bool:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{DIM}Laddar ner OUI-databas från IEEE...{RESET}", file=sys.stderr)
    req = urllib.request.Request(OUI_URL, headers={"User-Agent": "Mozilla/5.0 whatmac"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"{YELLOW}Kunde inte ladda ner OUI-listan: {e}{RESET}", file=sys.stderr)
        return False
    tmp = OUI_FILE.with_suffix(".tmp")
    tmp.write_bytes(data)
    tmp.replace(OUI_FILE)
    return True


def lookup_local(mac: str) -> tuple[str, str] | None:
    """Slå upp i IEEE:s lista. Returnerar (tillverkare, adress) eller None."""
    if not OUI_FILE.exists() or time.time() - OUI_FILE.stat().st_mtime > MAX_CACHE_AGE:
        if not download_oui() and not OUI_FILE.exists():
            return None
    prefix = mac[:6]
    lines = OUI_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        if line.startswith(prefix) and "(base 16)" in line:
            vendor = line.split("(base 16)", 1)[1].strip()
            addr = []
            for nxt in lines[i + 1:i + 4]:
                nxt = nxt.strip()
                if not nxt:
                    break
                addr.append(nxt)
            return vendor, ", ".join(addr)
    return None


def lookup_api(mac: str) -> str | None:
    req = urllib.request.Request(API_URL.format(mac[:6]), headers={"User-Agent": "whatmac"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode().strip() or None
    except (urllib.error.URLError, TimeoutError):
        return None


def describe_bits(mac: str) -> list[str]:
    first = int(mac[:2], 16)
    notes = []
    if mac == "FFFFFFFFFFFF":
        notes.append("Broadcast-adress")
    elif first & 0x01:
        notes.append("Multicast-adress")
    else:
        notes.append("Unicast")
    if first & 0x02:
        notes.append("Lokalt administrerad (troligen slumpad/privat MAC, t.ex. iPhone/Android/Windows)")
    else:
        notes.append("Globalt unik (tillverkartilldelad)")
    return notes


def show(raw: str) -> int:
    try:
        mac = normalize(raw)
    except ValueError as e:
        print(f"{RED}{e}{RESET}")
        return 1

    print(f"\n{BOLD}MAC-adress:{RESET} {CYAN}{raw}{RESET}\n")
    for name, value in formats(mac):
        print(f"  {DIM}{name:<22}{RESET} {GREEN}{value}{RESET}")

    print(f"\n{BOLD}Typ:{RESET}")
    for note in describe_bits(mac):
        print(f"  • {note}")

    print(f"\n{BOLD}Tillverkare:{RESET}")
    if int(mac[:2], 16) & 0x02:
        print(f"  {YELLOW}Okänd – lokalt administrerade adresser har ingen registrerad tillverkare.{RESET}")
    else:
        found = lookup_local(mac)
        if found:
            vendor, addr = found
            print(f"  {GREEN}{vendor}{RESET}")
            if addr:
                print(f"  {DIM}{addr}{RESET}")
        else:
            vendor = lookup_api(mac)
            if vendor:
                print(f"  {GREEN}{vendor}{RESET} {DIM}(via macvendors.com){RESET}")
            else:
                print(f"  {YELLOW}Hittades inte (OUI {mac[:2]}:{mac[2:4]}:{mac[4:6]}){RESET}")
    print()
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if args[0] in ("-u", "--update"):
        return 0 if download_oui() else 1
    # Tillåt både "whatmac aa bb cc dd ee ff" och flera adresser
    joined = " ".join(args)
    try:
        normalize(joined)
        return show(joined)
    except ValueError:
        return max(show(a) for a in args)


if __name__ == "__main__":
    sys.exit(main())
