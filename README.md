# whatmac

Ett litet terminalverktyg som visar en MAC-adress i alla vanliga format och slår upp vilken tillverkare den tillhör.

```
$ whatmac 3c:22:fb:12:34:56

MAC-adress: 3c:22:fb:12:34:56

  Kolon (Linux/macOS)    3c:22:fb:12:34:56
  Kolon versaler         3C:22:FB:12:34:56
  Bindestreck (Windows)  3C-22-FB-12-34-56
  Cisco                  3c22.fb12.3456
  HP / Aruba             3c22-fb12-3456
  Bara hex               3c22fb123456
  Bara hex versaler      3C22FB123456

Typ:
  • Unicast
  • Globalt unik (tillverkartilldelad)

Tillverkare:
  Apple, Inc.
  1 Infinite Loop, Cupertino  CA  95014, US
```

## Funktioner

- Tar emot MAC-adresser i valfritt format: `aa:bb:cc:dd:ee:ff`, `AA-BB-CC-DD-EE-FF`, `aabb.ccdd.eeff`, `aabbccddeeff` eller med mellanslag.
- Skriver ut adressen i kolon-, bindestreck-, Cisco- och HP/Aruba-format samt som ren hex.
- Slår upp tillverkaren i IEEE:s officiella OUI-register. Listan laddas ner första gången och sparas i `~/.cache/whatmac/`. Den uppdateras automatiskt var 30:e dag, så uppslagningar fungerar utan internet.
- Frågar [macvendors.com](https://macvendors.com) om adressen inte finns i den lokala listan.
- Visar om adressen är unicast, multicast eller broadcast.
- Känner igen lokalt administrerade (slumpade/privata) adresser. Sådana används ofta av iPhone, Android och Windows på wifi och saknar registrerad tillverkare.

## Krav

Python 3.10 eller senare. Inga externa paket behövs.

## Installation

```sh
git clone https://github.com/Troih/whatmac.git
cd whatmac
chmod +x whatmac.py
ln -s "$PWD/whatmac.py" ~/.local/bin/whatmac
```

Se till att `~/.local/bin` finns i din `PATH`:

- **fish:** `fish_add_path ~/.local/bin`
- **bash/zsh:** lägg till `export PATH="$HOME/.local/bin:$PATH"` i `~/.bashrc` eller `~/.zshrc`

## Användning

```sh
whatmac 3c:22:fb:12:34:56         # en adress
whatmac 001b.d4aa.bbcc            # Cisco-format fungerar också
whatmac aa:bb:cc:00:00:01 3c22fb123456   # flera adresser samtidigt
whatmac --update                  # ladda ner OUI-listan på nytt
whatmac --help
```

## Licens

MIT – se [LICENSE](LICENSE).
