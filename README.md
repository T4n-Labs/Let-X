# Let-X — VUR Helper

> CLI Tool untuk mengakses **VUR (Void User Repository)** dengan mudah di Void Linux dan turunannya.

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

```bash
# Install
git clone https://github.com/T4n-Labs/Let-X && cd Let-X
sudo ./install.sh
## OR
mkdir /path/to/void-packages/srcpkgs/letx
git clone https://github.com/T4n-Labs/Let-X && cd Let-X
cp xbps-template/template /path/to/void-packages/srcpkgs/letx
xbps-src pkg letx
sudo xbps-install --repository=/path/to/void-packages/hostdir/binpkgs letx

# Setup build environment (sekali saja)
letx -x binary-bootstrap

# Cari, download, dan build package
letx search <nama_package>
letx get <nama_package>
letx -x pkg <nama_package>

# Install hasil build
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs z<nama_package>
```

## Documentation

| Audience            | Indonesia                              | English                              |
|---------------------|----------------------------------------|--------------------------------------|
| **User Guide**      | [Panduan Pengguna](./vdocs/user-id.md) | [User Guide](./vdocs/user-en.md)     |
| **Developer Guide** | [Panduan Developer](./vdocs/dev-id.md) | [Developer Guide](./vdocs/dev-en.md) |

## AI Coder Prompt

Prompt konteks untuk Claude, OpenCode, atau AI coder lainnya agar memahami arsitektur Let-X tanpa perlu membaca semua file source.

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