# whatmac

A small command-line tool that shows a MAC address in every common format and looks up which vendor it belongs to.

```
$ whatmac 3c:22:fb:12:34:56

MAC address: 3c:22:fb:12:34:56

  Colon (Linux/macOS)    3c:22:fb:12:34:56
  Colon uppercase        3C:22:FB:12:34:56
  Hyphen (Windows)       3C-22-FB-12-34-56
  Cisco                  3c22.fb12.3456
  HP / Aruba             3c22-fb12-3456
  Plain hex              3c22fb123456
  Plain hex uppercase    3C22FB123456

Type:
  • Unicast
  • Globally unique (assigned by manufacturer)

Vendor:
  Apple, Inc.
  1 Infinite Loop, Cupertino  CA  95014, US
```

## Features

- Accepts MAC addresses in any format: `aa:bb:cc:dd:ee:ff`, `AA-BB-CC-DD-EE-FF`, `aabb.ccdd.eeff`, `aabbccddeeff`, or separated by spaces.
- Prints the address in colon, hyphen, Cisco and HP/Aruba format, plus plain hex.
- Looks up the vendor in the official IEEE OUI registry. The list is downloaded on first run and cached in `~/.cache/whatmac/`. It refreshes automatically every 30 days, so lookups work offline.
- Falls back to [macvendors.com](https://macvendors.com) if the address isn't in the local list.
- Shows whether the address is unicast, multicast or broadcast.
- Detects locally administered (randomized/private) addresses. iPhone, Android and Windows often use these on Wi-Fi, and they have no registered vendor.

## Requirements

Python 3.10 or later. No external packages needed.

## Installation

```sh
git clone https://github.com/Troih/whatmac.git
cd whatmac
chmod +x whatmac.py
mkdir -p ~/.local/bin
ln -s "$PWD/whatmac.py" ~/.local/bin/whatmac
```

Make sure `~/.local/bin` is on your `PATH`:

- **fish:** `fish_add_path ~/.local/bin`
- **bash/zsh:** add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc` or `~/.zshrc`, then open a new terminal.

To run it without installing, use `python3 whatmac.py <mac>`. On Windows, use `python whatmac.py <mac>`.

To update, run `git pull` in the `whatmac` folder. The symlink points at the file in the repo, so nothing needs reinstalling.

## Usage

```sh
whatmac 3c:22:fb:12:34:56                 # one address
whatmac 001b.d4aa.bbcc                    # Cisco format works too
whatmac aa:bb:cc:00:00:01 3c22fb123456    # several addresses at once
whatmac --update                          # re-download the OUI list
whatmac --help
```

## License

MIT – see [LICENSE](LICENSE).
