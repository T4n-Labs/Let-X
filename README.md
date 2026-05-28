# Let-X — VUR Helper

>- CLI Tool untuk mengakses **VUR (Void User Repository)** dengan mudah di Void Linux dan turunannya.
>- CLI Tool to easily access **VUR (Void User Repository)** on Void Linux and its derivatives.

**Versi:** 0.2.0 | **Python:** 3.11+ | **Binary:** `letx`

## Features

| Feature                      | Command       |
|------------------------------|---------------|
| Cari package                 | `letx search` |
| Info package                 | `letx info`   |
| List package                 | `letx list`   |
| Download template            | `letx get`    |
| Refresh index                | `letx update` |
| Build & install via xbps-src | `letx -x`     |

## Quick Start

### Install via script
```bash
git clone https://github.com/T4n-Labs/Let-X && cd Let-X
sudo ./install.sh
```

### Install via xbps-src
```bash
cp -r xbps-template/letx /path/to/void-packages/srcpkgs/
cd /path/to/void-packages
xbps-src pkg letx
sudo xbps-install --repository=hostdir/binpkgs letx
```

### Use
```bash
# Setup build environment (sekali saja)
letx -x binary-bootstrap

# Cari, download, dan build package
letx search <package>
letx get <package>
letx -x pkg <package>

# Install hasil build
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs <package>
```

## Documentation

| Audience            | Indonesia                              | English                              |
|---------------------|----------------------------------------|--------------------------------------|
| **User Guide**      | [Panduan Pengguna](./vdocs/user-id.md) | [User Guide](./vdocs/user-en.md)     |
| **Developer Guide** | [Panduan Developer](./vdocs/dev-id.md) | [Developer Guide](./vdocs/dev-en.md) |

## AI Coder Prompt

* A context prompt for Claude, OpenCode, or any other AI coder to understand the Let-X architecture without reading all the source.naan files
* Prompt konteks untuk Claude, OpenCode, atau AI coder lainnya agar memahami arsitektur Let-X tanpa membaca semua file source.

| Audience     | Link                                               |
|--------------|----------------------------------------------------|
| 🇮🇩 Indonesia | [Prompt-AI/prompt-id.md](./Prompt-AI/prompt-id.md) |
| 🇬🇧 English   | [Prompt-AI/prompt-en.md](./Prompt-AI/prompt-en.md) |

## Links

- **VUR Repository:** [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)
- **VUR Web Index:** [t4n-labs.github.io/vur-web](https://t4n-labs.github.io/vur-web)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>