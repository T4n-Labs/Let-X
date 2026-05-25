# ISSUES
## ISSUES #1: Let-X Inconsistent output

### <span style="background-color: blue">STATUS</span> : <span style="color: orange">ON GOING</span>

```bash
┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Sun May 24 ] [ ~ ]
└[T4n OS]->> letx
[ERROR] No Options

usage: letx [-h] [-v] [-x ...] <command> ...

Let-X — VUR Helper for Void Linux

positional arguments:
  <command>
    search        Search for a package in VUR
    info          Show package details
    list          List available packages
    get           Download package template locally
    update        Refresh the VUR package index cache

options:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -x, --xbps ...  letx integration xbps-src (letx -x <target> [pkgname]
                  [options])

Examples:
  letx -h
  letx -v
  letx update

┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Sun May 24 ] [ ~ ]
└[T4n OS]->> letx search
[ERROR] No Options

usage: letx search [-h] [-c CATEGORY] [-t PKG_NAME] [keyword]

positional arguments:
  keyword               Package name or description to search

options:
  -h, --help            show this help message and exit
  -c, --category CATEGORY
                        Filter by category: core | extra | multilib
  -t, --template PKG_NAME
                        Search for a template locally in ~/.config/letx/

Examples:
  letx search discord
  letx search "Programming Language"
  letx search browser -c extra
  letx search -t discord

┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Mon May 25 ] [ ~ ]
└[T4n OS]->> letx info
[ERROR] No Options

usage: letx [-h] [-v] [-x ...] <command> ...

Let-X — VUR Helper for Void Linux

positional arguments:
  <command>
    search        Search for a package in VUR
    info          Show package details
    list          List available packages
    get           Download package template locally
    update        Refresh the VUR package index cache

options:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -x, --xbps ...  letx integration xbps-src (letx -x <target> [pkgname]
                  [options])

Examples:
  letx -h
  letx -v
  letx update

┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Mon May 25 ] [ ~ ]
└[T4n OS]->> letx list
[ERROR] No Options

usage: letx [-h] [-v] [-x ...] <command> ...

Let-X — VUR Helper for Void Linux

positional arguments:
  <command>
    search        Search for a package in VUR
    info          Show package details
    list          List available packages
    get           Download package template locally
    update        Refresh the VUR package index cache

options:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -x, --xbps ...  letx integration xbps-src (letx -x <target> [pkgname]
                  [options])

Examples:
  letx -h
  letx -v
  letx update

┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Mon May 25 ] [ ~ ]
└[T4n OS]->> letx get
usage: letx get [-h] [-f] name
letx get: error: the following arguments are required: name
```

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
