# Let-X — AI Coder Context Prompt

> Paste this prompt into the system prompt or the beginning of a conversation before asking for code help.

---

```
You are working on Let-X — a Python CLI tool (VUR Helper for Void Linux).
Binary: `letx` | Version: 0.2.0 | Python 3.11+

## Architecture (strict separation of concerns)
cli.py → ops/ → repo/ → utils/
- cli.py       : argparse only, no logic
- ops/         : business logic (search.py, info.py)
- repo/        : data access (index.py, fetch.py)
- utils/print  : all Rich terminal output
- utils/xbps   : ONLY module allowed to call xbps-src subprocess
- config.py    : all constants/paths, imports stdlib only

## Key Paths (config.py)
BACKEND_DIR          = letx/backend/              # xbps-src bundle
XBPS_SRC_PATH        = letx/backend/xbps-src
BACKEND_GIT_DIR      = letx/backend/root-git/     # renamed .git/
BACKEND_SRCPKGS_DIR  = letx/backend/srcpkgs/      # base-files, base-chroot ONLY
CONFIG_DIR           = ~/.config/letx/
CACHE_DIR            = ~/.cache/letx/
TEMPLATE_DIRS        = {core|extra|multilib: CONFIG_DIR/<cat>/}
LETX_MASTERDIR       = ~/.config/letx/masterdir/
LETX_CHROOT_SRCPKGS  = ~/.config/letx/masterdir/letx-srcpkgs/
LETX_HOSTDIR         = ~/.config/letx/hostdir/

## VUR Template System
Templates live in: ~/.config/letx/{core,extra,multilib}/<pkgname>/template
find_template() loops: core → extra → multilib
Templates are NEVER modified. stage_vur_template() creates a patched copy
at LETX_CHROOT_SRCPKGS/<pkgname>/ before every build.

Patch applied during staging:
  If ${pkgname}_package() missing → inject `${pkgname}_package() { :; }`
  (xbps-src-doinstall.sh requires this for all packages)

## xbps-src Integration (utils/xbps.py)
Two command groups:
  CMDS_NEED_PKG → _run_with_template()
    1. find_template()           # loop core/extra/multilib
    2. stage_vur_template()      # copy+patch to masterdir/letx-srcpkgs/
    3. build_xbps_env()          # set XBPS_CHROOT_CMD=letx
                                 # set XBPS_CHROOT_CMD_ARGS (bind mount)
    4. subprocess: BACKEND_DIR/xbps-src <target> <pkg>

  CMDS_NO_PKG → _run_xbps_raw()
    XBPS_SRCPKGDIR = BACKEND_SRCPKGS_DIR
    subprocess: BACKEND_DIR/xbps-src <target>

## Critical: letx.sh (custom chroot style)
File: letx/backend/common/chroot-style/letx.sh
WHY: uunshare.sh default puts EXTRA_ARGS BEFORE DISTDIR mount.
     Linux namespaces: DISTDIR mount overwrites EXTRA_ARGS submounts.
     letx.sh puts DISTDIR mount FIRST, EXTRA_ARGS AFTER → overlay works.
XBPS_CHROOT_CMD=letx activates it.
XBPS_CHROOT_CMD_ARGS="-b {LETX_CHROOT_SRCPKGS}:void-packages/srcpkgs"

## Two xbps-src instances per build
Outer (host): reads XBPS_SRCPKGDIR from env → LETX_CHROOT_SRCPKGS
Inner (chroot IN_CHROOT=1): env cleared by env -i, reads from XBPS_DISTDIR
  → XBPS_SRCPKGDIR=/void-packages/srcpkgs/ (default)
  → accessible because letx.sh bind-mounted LETX_CHROOT_SRCPKGS there

## GIT_DIR fix
root-git/ = renamed .git/ (avoids conflict with Let-X .git/).
build_xbps_env() sets GIT_DIR=root-git/ if exists, else pops it.

## VUR Remote
REPO: T4n-Labs/vur | BRANCH: main
PACKAGES_URL: raw.githubusercontent.com/T4n-Labs/vur/main/packages.json

## Conventions
- Type hints required on all public functions
- Imports: stdlib → third-party → internal (absolute)
- Output: always via utils/print.py (never print() in ops/ or repo/)
- Errors: return int exit code (0=ok, 1=error), never sys.exit() in ops/
- New commands: subparser in build_parser() + cmd_<name>() + dispatch in main()

## Known TODOs (v0.3.0)
- Staging cleanup after build (masterdir/letx-srcpkgs/ grows unbounded)
- letx-bwrap.sh for bwrap chroot style compatibility
- Subpackage ($subpackages) support in stage_vur_template()
- Remove LETX_SRCPKGS_DIR legacy path

## Rules for this session
- DO NOT fetch or read files unless explicitly asked
- DO NOT reproduce entire files — show only changed sections
- If you need a file's content to answer, ask: "Please share <file>"
- Assume the architecture above is correct; ask before changing patterns
- Prefer surgical edits (str_replace style) over full rewrites
```