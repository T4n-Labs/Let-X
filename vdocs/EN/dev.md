# Let-X — Developer Guide

> Technical documentation for contributors and maintainers of **Let-X v0.2.0**.

## Table of Contents

- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Module Reference](#module-reference)
- [Data Flow](#data-flow)
- [Development Environment Setup](#development-environment-setup)
- [Code Conventions](#code-conventions)
- [Adding New Commands](#adding-new-commands)
- [Running Tests](#running-tests)
- [Building xbps-src Package](#building-xbps-src-package)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)

## Project Architecture

Let-X follows the **separation of concerns** principle — each layer has one clear responsibility:


```

┌──────────────────────────────────────────────┐
│               CLI (cli.py)                   │  argparse: parse args, routing to handler
├────────────────────┬─────────────────────────┤
│       ops/         │         repo/           │  business logic vs data access
│  search.py         │     index.py            │
│  info.py           │     fetch.py            │
├────────────────────┴─────────────────────────┤
│              utils/print.py                  │  Rich: all terminal output
├──────────────────────────────────────────────┤
│               config.py                      │  constants, paths, URLs
└──────────────────────────────────────────────┘

```

**Important principles:**
- `cli.py` must not contain logic — only orchestrate to `ops/` and `repo/`
- `ops/` knows nothing about HTTP — that is handled by `repo/`
- `repo/` knows nothing about layout/display — that is handled by `utils/`
- `config.py` does not import any module from this project

---

## Directory Structure

```text
.
├── letx/                                   ← Main Python package
│   ├── __init__.py                         → Version and app name
│   ├── backend/
│   │   ├── common/
│   │   │   ├── build-helper/
│   │   │   │   ├── cmake-wxWidgets-gtk3.sh
│   │   │   │   ├── gir.sh
│   │   │   │   ├── haskell.sh
│   │   │   │   ├── meson.sh
│   │   │   │   ├── numpy.sh
│   │   │   │   ├── python3.sh
│   │   │   │   ├── qemu.sh
│   │   │   │   ├── qmake.sh
│   │   │   │   ├── qmake6.sh
│   │   │   │   └── rust.sh
│   │   │   ├── build-profiles/
│   │   │   │   ├── aarch64-musl.sh
│   │   │   │   ├── aarch64.sh
│   │   │   │   ├── armv6l-musl.sh
│   │   │   │   ├── armv6l.sh
│   │   │   │   ├── armv7l-musl.sh
│   │   │   │   ├── armv7l.sh
│   │   │   │   ├── bootstrap.sh
│   │   │   │   ├── i686-musl.sh
│   │   │   │   ├── i686.sh
│   │   │   │   ├── ppc-musl.sh
│   │   │   │   ├── ppc.sh
│   │   │   │   ├── ppc64-musl.sh
│   │   │   │   ├── ppc64.sh
│   │   │   │   ├── ppc64le-musl.sh
│   │   │   │   ├── ppc64le.sh
│   │   │   │   ├── ppcle-musl.sh
│   │   │   │   ├── ppcle.sh
│   │   │   │   ├── README
│   │   │   │   ├── riscv64-musl.sh
│   │   │   │   ├── riscv64.sh
│   │   │   │   ├── x86_64-musl.sh
│   │   │   │   └── x86_64.sh
│   │   │   ├── build-style/
│   │   │   │   ├── cabal.sh
│   │   │   │   ├── cargo.sh
│   │   │   │   ├── cmake.sh
│   │   │   │   ├── configure.sh
│   │   │   │   ├── fetch.sh
│   │   │   │   ├── gem.sh
│   │   │   │   ├── gemspec.sh
│   │   │   │   ├── gnu-configure.sh
│   │   │   │   ├── gnu-makefile.sh
│   │   │   │   ├── go.sh
│   │   │   │   ├── haskell-stack.sh
│   │   │   │   ├── meson.sh
│   │   │   │   ├── perl-module.sh
│   │   │   │   ├── perl-ModuleBuild.sh
│   │   │   │   ├── python2-module.sh
│   │   │   │   ├── python3-module.sh
│   │   │   │   ├── python3-pep517.sh
│   │   │   │   ├── qmake.sh
│   │   │   │   ├── R-cran.sh
│   │   │   │   ├── raku-dist.sh
│   │   │   │   ├── README
│   │   │   │   ├── ruby-module.sh
│   │   │   │   ├── scons.sh
│   │   │   │   ├── sip-build.sh
│   │   │   │   ├── slashpackage.sh
│   │   │   │   ├── texmf.sh
│   │   │   │   ├── tree-sitter.sh
│   │   │   │   ├── void-cross.sh
│   │   │   │   ├── waf3.sh
│   │   │   │   └── zig-build.sh
│   │   │   ├── chroot-style/
│   │   │   │   ├── bwrap.sh
│   │   │   │   ├── ethereal.sh
│   │   │   │   ├── README
│   │   │   │   ├── uchroot.sh
│   │   │   │   └── uunshare.sh
│   │   │   ├── container/
│   │   │   │   ├── Containerfile
│   │   │   │   ├── docker-bake.hcl
│   │   │   │   ├── noextract.conf
│   │   │   │   ├── README.md
│   │   │   │   └── setup.sh
│   │   │   ├── cross-profiles/
│   │   │   │   ├── aarch64-musl.sh
│   │   │   │   ├── aarch64.sh
│   │   │   │   ├── armv5te-musl.sh -> armv5tel-musl.sh
│   │   │   │   ├── armv5te.sh -> armv5tel.sh
│   │   │   │   ├── armv5tel-musl.sh
│   │   │   │   ├── armv5tel.sh
│   │   │   │   ├── armv6hf-musl.sh -> armv6l-musl.sh
│   │   │   │   ├── armv6hf.sh -> armv6l.sh
│   │   │   │   ├── armv6l-musl.sh
│   │   │   │   ├── armv6l.sh
│   │   │   │   ├── armv7hf-musl.sh -> armv7l-musl.sh
│   │   │   │   ├── armv7hf.sh -> armv7l.sh
│   │   │   │   ├── armv7l-musl.sh
│   │   │   │   ├── armv7l.sh
│   │   │   │   ├── i686-musl.sh
│   │   │   │   ├── i686.sh
│   │   │   │   ├── mips-musl.sh
│   │   │   │   ├── mipsel-musl.sh
│   │   │   │   ├── mipselhf-musl.sh
│   │   │   │   ├── mipshf-musl.sh
│   │   │   │   ├── ppc-musl.sh
│   │   │   │   ├── ppc.sh
│   │   │   │   ├── ppc64-musl.sh
│   │   │   │   ├── ppc64.sh
│   │   │   │   ├── ppc64le-musl.sh
│   │   │   │   ├── ppc64le.sh
│   │   │   │   ├── ppcle-musl.sh
│   │   │   │   ├── ppcle.sh
│   │   │   │   ├── README
│   │   │   │   ├── riscv64-musl.sh
│   │   │   │   ├── riscv64.sh
│   │   │   │   ├── x86_64-musl.sh
│   │   │   │   └── x86_64.sh
│   │   │   ├── environment/
│   │   │   │   ├── build/
│   │   │   │   │   ├── bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├── ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├── cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├── debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├── hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └── pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├── build-style/
│   │   │   │   │   ├── cabal.sh
│   │   │   │   │   ├── cargo.sh
│   │   │   │   │   ├── cmake.sh
│   │   │   │   │   ├── gem.sh
│   │   │   │   │   ├── gemspec.sh
│   │   │   │   │   ├── go.sh
│   │   │   │   │   ├── haskell-stack.sh
│   │   │   │   │   ├── meson.sh
│   │   │   │   │   ├── perl-module.sh
│   │   │   │   │   ├── perl-ModuleBuild.sh
│   │   │   │   │   ├── python2-module.sh
│   │   │   │   │   ├── python3-module.sh
│   │   │   │   │   ├── python3-pep517.sh
│   │   │   │   │   ├── R-cran.sh
│   │   │   │   │   ├── raku-dist.sh
│   │   │   │   │   ├── ruby-module.sh
│   │   │   │   │   ├── scons.sh
│   │   │   │   │   ├── texmf/
│   │   │   │   │   │   └── ownership.txt
│   │   │   │   │   ├── texmf.sh
│   │   │   │   │   ├── tree-sitter.sh
│   │   │   │   │   ├── void-cross.sh
│   │   │   │   │   ├── waf.sh
│   │   │   │   │   ├── waf3.sh
│   │   │   │   │   └── zig-build.sh
│   │   │   │   ├── check/
│   │   │   │   │   ├── bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├── ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├── cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├── debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├── hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   ├── no_display.sh
│   │   │   │   │   └── pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├── configure/
│   │   │   │   │   ├── autoconf_cache/
│   │   │   │   │   │   ├── aarch64-linux
│   │   │   │   │   │   ├── arm-common
│   │   │   │   │   │   ├── arm-linux
│   │   │   │   │   │   ├── common-glibc
│   │   │   │   │   │   ├── common-linux
│   │   │   │   │   │   ├── endian-big
│   │   │   │   │   │   ├── endian-little
│   │   │   │   │   │   ├── ix86-common
│   │   │   │   │   │   ├── mips-common
│   │   │   │   │   │   ├── mips-linux
│   │   │   │   │   │   ├── mipsel-linux
│   │   │   │   │   │   ├── musl-linux
│   │   │   │   │   │   ├── powerpc-common
│   │   │   │   │   │   ├── powerpc-linux
│   │   │   │   │   │   ├── powerpc32-linux
│   │   │   │   │   │   ├── powerpc64-linux
│   │   │   │   │   │   ├── riscv64-linux
│   │   │   │   │   │   └── x86_64-linux
│   │   │   │   │   ├── automake/
│   │   │   │   │   │   ├── config.guess
│   │   │   │   │   │   └── config.sub
│   │   │   │   │   ├── bootstrap.sh
│   │   │   │   │   ├── ccache.sh
│   │   │   │   │   ├── cross.sh
│   │   │   │   │   ├── debug-debug-prefix-map.sh
│   │   │   │   │   ├── gccspecs/
│   │   │   │   │   │   ├── hardened-cc1
│   │   │   │   │   │   ├── hardened-ld
│   │   │   │   │   │   └── hardened-mips-cc1
│   │   │   │   │   ├── gnu-configure-args.sh
│   │   │   │   │   ├── hardening.sh
│   │   │   │   │   └── pkg-config.sh
│   │   │   │   ├── extract/
│   │   │   │   │   └── .empty
│   │   │   │   ├── fetch/
│   │   │   │   │   ├── fetch_cmd.sh
│   │   │   │   │   └── misc.sh -> ../setup/misc.sh
│   │   │   │   ├── install/
│   │   │   │   │   ├── ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├── cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├── debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├── extglob.sh
│   │   │   │   │   ├── hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └── pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├── patch/
│   │   │   │   │   ├── bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├── ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├── cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├── debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├── gnu-configure-args.sh -> ../configure/gnu-configure-args.sh
│   │   │   │   │   ├── hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └── pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├── pkg/
│   │   │   │   │   └── extglob.sh -> ../install/extglob.sh
│   │   │   │   ├── README
│   │   │   │   ├── setup/
│   │   │   │   │   ├── archive.sh
│   │   │   │   │   ├── git.sh
│   │   │   │   │   ├── install.sh
│   │   │   │   │   ├── misc.sh
│   │   │   │   │   ├── options.sh
│   │   │   │   │   ├── python.sh
│   │   │   │   │   ├── replace-interpreter.sh
│   │   │   │   │   ├── sourcepkg.sh
│   │   │   │   │   └── vsed.sh
│   │   │   │   └── setup-subpkg/
│   │   │   │       └── subpkg.sh
│   │   │   ├── hooks/
│   │   │   │   ├── do-build/
│   │   │   │   │   └── .empty
│   │   │   │   ├── do-check/
│   │   │   │   │   └── .empty
│   │   │   │   ├── do-configure/
│   │   │   │   │   └── .empty
│   │   │   │   ├── do-extract/
│   │   │   │   │   └── 00-distfiles.sh
│   │   │   │   ├── do-fetch/
│   │   │   │   │   └── 00-distfiles.sh
│   │   │   │   ├── do-install/
│   │   │   │   ├── do-patch/
│   │   │   │   │   └── 00-patches.sh
│   │   │   │   ├── do-pkg/
│   │   │   │   │   └── 00-gen-pkg.sh
│   │   │   │   ├── post-build/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-check/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-configure/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-extract/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-fetch/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-install/
│   │   │   │   │   ├── 00-compress-info-files.sh
│   │   │   │   │   ├── 00-fixup-gir-path.sh
│   │   │   │   │   ├── 00-libdir.sh
│   │   │   │   │   ├── 00-uncompress-manpages.sh
│   │   │   │   │   ├── 01-remove-misc.sh
│   │   │   │   │   ├── 02-remove-libtool-archives.sh
│   │   │   │   │   ├── 02-remove-perl-files.sh
│   │   │   │   │   ├── 02-remove-python-bytecode-files.sh
│   │   │   │   │   ├── 03-remove-empty-dirs.sh
│   │   │   │   │   ├── 04-create-xbps-metadata-scripts.sh
│   │   │   │   │   ├── 05-generate-gitrevs.sh
│   │   │   │   │   ├── 06-strip-and-debug-pkgs.sh
│   │   │   │   │   ├── 10-pkglint-devel-paths.sh
│   │   │   │   │   ├── 11-pkglint-elf-in-usrshare.sh
│   │   │   │   │   ├── 12-rename-python3-c-bindings.sh
│   │   │   │   │   ├── 13-pkg-config-clean-xbps-cross-base-ref.sh
│   │   │   │   │   ├── 14-fix-permissions.sh
│   │   │   │   │   ├── 15-qt-private-api.sh
│   │   │   │   │   ├── 80-prepare-32bit.sh
│   │   │   │   │   ├── 98-shlib-provides.sh
│   │   │   │   │   └── 99-pkglint-warn-cross-cruft.sh
│   │   │   │   ├── post-patch/
│   │   │   │   │   └── .empty
│   │   │   │   ├── post-pkg/
│   │   │   │   │   └── 00-register-pkg.sh
│   │   │   │   ├── pre-build/
│   │   │   │   │   └── 02-script-wrapper.sh -> ../pre-configure/02-script-wrapper.sh
│   │   │   │   ├── pre-check/
│   │   │   │   │   └── .empty
│   │   │   │   ├── pre-configure/
│   │   │   │   │   ├── 00-gnu-configure-asneeded.sh
│   │   │   │   │   ├── 01-override-config.sh
│   │   │   │   │   └── 02-script-wrapper.sh
│   │   │   │   ├── pre-extract/
│   │   │   │   ├── pre-fetch/
│   │   │   │   ├── pre-install/
│   │   │   │   │   ├── 00-libdir.sh
│   │   │   │   │   ├── 02-script-wrapper.sh -> ../pre-configure/02-script-wrapper.sh
│   │   │   │   │   └── 98-fixup-gir-path.sh
│   │   │   │   ├── pre-patch/
│   │   │   │   │   └── .empty
│   │   │   │   ├── pre-pkg/
│   │   │   │   │   ├── 03-restrict-py3-version.sh
│   │   │   │   │   ├── 03-rewrite-python-shebang.sh
│   │   │   │   │   ├── 04-generate-provides.sh
│   │   │   │   │   ├── 04-generate-runtime-deps.sh
│   │   │   │   │   ├── 05-generate-32bit-runtime-deps.sh
│   │   │   │   │   ├── 06-verify-python-deps.sh
│   │   │   │   │   ├── 90-set-timestamps.sh
│   │   │   │   │   ├── 99-pkglint-subpkgs.sh
│   │   │   │   │   ├── 99-pkglint.sh
│   │   │   │   │   └── 999-collected-rdeps.sh
│   │   │   │   └── README
│   │   │   ├── options.description
│   │   │   ├── repo-keys/
│   │   │   │   ├── 3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
│   │   │   │   └── 60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
│   │   │   ├── scripts/
│   │   │   │   ├── check-custom-licenses
│   │   │   │   ├── gen-wrap-distfiles.py
│   │   │   │   ├── lint-commits
│   │   │   │   ├── lint-conflicts
│   │   │   │   ├── lint-version-change
│   │   │   │   ├── lint2annotations.awk
│   │   │   │   ├── parse-py-metadata.py
│   │   │   │   ├── README.xbps-cycles.md
│   │   │   │   └── xbps-cycles.py
│   │   │   ├── shlibs
│   │   │   ├── travis/
│   │   │   │   ├── build.sh
│   │   │   │   ├── changed_templates.sh
│   │   │   │   ├── check-install.sh
│   │   │   │   ├── fetch-xbps.sh
│   │   │   │   ├── fetch-xtools.sh
│   │   │   │   ├── license.lst
│   │   │   │   ├── prepare.sh
│   │   │   │   ├── set_mirror.sh
│   │   │   │   ├── show_files.sh
│   │   │   │   ├── verify-update-check.sh
│   │   │   │   ├── xlint.sh
│   │   │   │   └── xpkgdiff.sh
│   │   │   ├── wrappers/
│   │   │   │   ├── cross-cc
│   │   │   │   ├── date.sh
│   │   │   │   ├── install.sh
│   │   │   │   ├── ldconfig.sh
│   │   │   │   ├── strip.sh
│   │   │   │   └── uname.sh
│   │   │   └── xbps-src/
│   │   │       ├── libexec/
│   │   │       │   ├── build.sh
│   │   │       │   ├── xbps-src-dobuild.sh
│   │   │       │   ├── xbps-src-docheck.sh
│   │   │       │   ├── xbps-src-doconfigure.sh
│   │   │       │   ├── xbps-src-doextract.sh
│   │   │       │   ├── xbps-src-dofetch.sh
│   │   │       │   ├── xbps-src-doinstall.sh
│   │   │       │   ├── xbps-src-dopatch.sh
│   │   │       │   ├── xbps-src-dopkg.sh
│   │   │       │   └── xbps-src-prepkg.sh
│   │   │       └── shutils/
│   │   │           ├── build_dependencies.sh
│   │   │           ├── bulk.sh
│   │   │           ├── chroot.sh
│   │   │           ├── common.sh
│   │   │           ├── consistency_check.sh
│   │   │           ├── cross.sh
│   │   │           ├── pkgtarget.sh
│   │   │           ├── purge_distfiles.sh
│   │   │           ├── show.sh
│   │   │           ├── update_check.sh
│   │   │           └── update_hash_cache.sh
│   │   ├── COPYING
│   │   ├── etc/
│   │   │   ├── defaults.conf
│   │   │   ├── defaults.virtual
│   │   │   └── xbps.d/
│   │   │       ├── repos-local-x86_64-multilib.conf
│   │   │       ├── repos-local.conf
│   │   │       ├── repos-remote-aarch64-musl.conf
│   │   │       ├── repos-remote-aarch64.conf
│   │   │       ├── repos-remote-musl.conf
│   │   │       ├── repos-remote-x86_64-multilib.conf
│   │   │       └── repos-remote.conf
│   ├── root-git/
│   │   ├── config
│   │   ├── description
│   │   ├── HEAD
│   │   ├── hooks/
│   │   │   ├── applypatch-msg.sample
│   │   │   ├── commit-msg.sample
│   │   │   ├── fsmonitor-watchman.sample
│   │   │   ├── post-update.sample
│   │   │   ├── pre-applypatch.sample
│   │   │   ├── pre-commit.sample
│   │   │   ├── pre-merge-commit.sample
│   │   │   ├── pre-push.sample
│   │   │   ├── pre-rebase.sample
│   │   │   ├── pre-receive.sample
│   │   │   ├── prepare-commit-msg.sample
│   │   │   ├── push-to-checkout.sample
│   │   │   ├── sendemail-validate.sample
│   │   │   └── update.sample
│   │   ├── index
│   │   ├── info/
│   │   │   └── exclude
│   │   ├── logs/
│   │   │   ├── HEAD
│   │   │   └── refs/
│   │   │       ├── heads/
│   │   │       │   └── master
│   │   │       └── remotes/
│   │   │           └── origin/
│   │   │               └── HEAD
│   │   ├── README.md
│   │   └── xbps-src
│   ├── cli.py                      → CLI Entry point (argparse)
│   ├── config.py                   → All constants and paths
│   ├── ops/                        → Data access layer (GitHub)
│   │   ├── __init__.py
│   │   ├── info.py                 → Fetch and cache packages.json
│   │   └── search.py               → Download template folder via GitHub API
│   ├── repo/                       → Business logic layer
│   │   ├── __init__.py
│   │   ├── fetch.py                → Search, list, count, local template lookup
│   │   └── index.py                → Package details + local template info
│   └── utils/
│   │   ├── __init__.py
│		├── xbps.py
│       └── print.py                → All Rich output (tables, panels, colors)
├── tests/
│   ├── __init__.py
│   └── test_search.py              → Unit tests
├── vdocs/
│   ├── docs.md
│   ├── EN/
│   │   ├── dev.md
│   │   └── user.md
│   └── ID/
│       ├── dev.md
│       └── user.md
├── xbps-template/                  → xbps-src template
│   └── template
├── pyproject.toml                  → Project metadata and dependencies
├── install.sh                      → Bash installation script
├── LICENSE
└── README.md

```

## Module Reference

### `config.py`

The single source of truth for all constants. Other modules must not hardcode paths or URLs.

```python
# Remote
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Local paths
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # seconds (1 hour)

```

### `repo/index.py`

Manages fetching and caching `packages.json`.

| Function      | Signature                               | Description                               |
|---------------|-----------------------------------------|-------------------------------------------|
| `fetch_index` | `(force: bool = False) → list[Package]` | Fetch all packages (from cache or GitHub) |
| `get_package` | `(name: str) → Package \| None`         | Search for a single package by exact name |
| `cache_info`  | `() → dict`                             | Current cache status                      |

**Cache logic:**

```
fetch_index()
    │
    ├─ Cache exists AND age < TTL AND force=False?
    │   └─ return local cache
    │
    └─ Otherwise:
        ├─ GET packages.json from GitHub
        ├─ Write to ~/.cache/letx/packages.json
        └─ Return new data
            │
            └─ If fetch FAILS but old cache exists:
                └─ Return old cache (graceful degradation)

```

### `repo/fetch.py`

Downloads template folders from GitHub using the **GitHub Contents API** — no `git` or `svn` required.

| Function                 | Signature                                            | Description                              |
|--------------------------|------------------------------------------------------|------------------------------------------|
| `download_package`       | `(pkg_path, category, pkg_name, progress_cb) → Path` | Download package folder from VUR         |
| `package_exists_locally` | `(category, pkg_name) → bool`                        | Check if template already exists locally |
| `local_package_path`     | `(category, pkg_name) → Path \| None`                | Local package path if it exists          |

**Fetch strategy:**

```
GitHub Contents API
GET /repos/T4n-Labs/vur/contents/extra/discord
    │
    └─ Response: list of {type, name, path, ...}
        │
        ├─ type == "file"  → download via raw.githubusercontent.com
        └─ type == "dir"   → recurse into subdirectory

```

### `ops/search.py`

All search and listing operations. Fully offline once the index is cached.

| Function                | Signature                                   | Description                        |
|-------------------------|---------------------------------------------|------------------------------------|
| `search_packages`       | `(keyword, category=None) → list[Package]`  | Search by name or description      |
| `list_packages`         | `(category=None) → list[Package]`           | List all packages                  |
| `latest_packages`       | `(category=None, limit=20) → list[Package]` | Last added packages                |
| `count_packages`        | `(category=None) → dict[str, int]`          | Number of packages per category    |
| `search_local_template` | `(pkg_name) → LocalTemplateResult`          | Search template in local directory |
| `available_categories`  | `() → list[str]`                            | Unique categories in index         |

**Search fields (fix v0.1.2):**

```python
# Only name and description — no false positives from maintainer/homepage
_SEARCH_FIELDS = ("name", "description")

```

**Search result ranking:**

```python
def _rank(pkg) -> int:
    name = pkg["name"].lower()
    if name == keyword:       return 0   # exact match → highest priority
    if name.startswith(kw):   return 1   # prefix match
    if kw in name:            return 2   # contains match
    return 3                             # match in description

```

**Local template lookup order — core → extra → multilib:**

```python
search_order = ["core", "extra", "multilib"]
for cat in search_order:
    pkg_dir = TEMPLATE_DIRS[cat] / pkg_name
    if pkg_dir.exists():
        return LocalTemplateResult(found=True, category=cat, path=pkg_dir, ...)
return LocalTemplateResult(found=False, ...)

```

### `ops/info.py`

| Function                  | Signature                    | Description                    |
|---------------------------|------------------------------|--------------------------------|
| `get_info`                | `(name: str) → dict \| None` | Package details + local status |
| `get_local_template_info` | `(pkg_name: str) → dict`     | Local template info + VUR data |

### `utils/print.py`

All terminal output must go through this module. **Never `print()` directly from other modules.**

| Function                                          | Description                           |
|---------------------------------------------------|---------------------------------------|
| `print_package_table(packages, title, show_desc)` | Rich table for package listing        |
| `print_package_info(info)`                        | Rich panel for single package details |
| `print_local_template_info(info)`                 | Rich panel for local templates        |
| `print_package_counts(counts, category)`          | Statistics table                      |
| `print_success(msg)`                              | `✔ message` (green)                   |
| `print_error(msg)`                                | `✘ message` (red)                     |
| `print_info(msg)`                                 | `→ message` (cyan)                    |
| `print_warn(msg)`                                 | `! message` (yellow)                  |

**Color themes:**

```python
C_NAME    = "bold cyan"     # package name
C_VER     = "green"         # version
C_CAT     = "yellow"        # category
C_DESC    = "dim white"     # description
C_MAINT   = "dim white"     # maintainer
C_LOCAL   = "bold green"    # locally available
C_MISSING = "dim red"       # not downloaded yet
C_PATH    = "cyan"          # file path
C_FILE    = "dim cyan"      # file listing

```

## Data Flow

### `letx search <keyword>`

```
letx search discord
    │
    ▼
cli.py:cmd_search()
    │
    ├─ args.template? → _search_local_template()
    │                       → ops/search.py:search_local_template()
    │                       → utils/print.py:print_local_template_info()
    │
    ├─ keyword exists → ops/search.py:search_packages()
    │                    │
    │                    ├─ repo/index.py:fetch_index()
    │                    │       │
    │                    │       ├─ cache valid → read file
    │                    │       └─ expired     → GET GitHub → write cache
    │                    │
    │                    └─ filter (name + description) → sort by rank
    │
    └─ utils/print.py:print_package_table()

```

### `letx list -p`

```
letx list -p
    │
    ▼
cli.py:cmd_list()
    │
    ├─ ops/search.py:count_packages()
    │       │
    │       └─ fetch_index() → count per category
    │
    └─ utils/print.py:print_package_counts()

```

### `letx get <pkg>`

```
letx get discord
    │
    ▼
cli.py:cmd_get()
    │
    ├─ ops/info.py:get_info()            → check index + local status
    │
    ├─ Already local & no --force?       → print_warn(), exit 0
    │
    └─ repo/fetch.py:download_package()
    │       ││
    │       └─ GitHub Contents API (recursive)
    │               ├─ each file → GET raw.githubusercontent.com
    │               └─ write to ~/.config/letx/<category>/<pkg>/
    │
    └─ utils/print.py:print_success()

```

## Development Environment Setup

```bash
# 1. Fork and clone repo
git clone https://github.com/<username>/Let-X
cd Let-X

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Verify
letx --help
pytest tests/ -v

```

## Code Conventions

**Naming:**

* Modules and functions: `snake_case`
* Constants in `config.py`: `SCREAMING_SNAKE_CASE`
* Type hints are required for all public functions

**Import order:**

```python
# 1. stdlib
import sys
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (always absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index

```

**Docstring — required for all public functions:**

```python
def search_packages(keyword: str, category: str | None = None) -> list[Package]:
    """
    Search packages by keyword (case-insensitive).
    Matches against: name, description.

    Args:
        keyword:  search keyword
        category: optional filter ("core"|"extra"|"multilib")

    Returns:
        Matching packages sorted by relevance.
    """

```

## Adding New Commands

1. Add subparser in `cli.py:build_parser()`
2. Add handler `cmd_<name>()` in `cli.py`
3. Register it in the dispatch block of `main()`
4. Business logic goes into `ops/` (not in `cli.py`)
5. Data access goes into `repo/` (not in `ops/`)
6. Output must always use `utils/print.py`
7. Write tests in `tests/`

**Skeleton for new command:**

```python
# In build_parser():
p_remove = sub.add_parser("remove", help="Remove a local template")
p_remove.add_argument("name", help="Package name")

# Handler:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template   # new module
    removed = remove_template(args.name)
    if removed:
        print_success(f"Template '{args.name}' removed.")
        return 0
    print_error(f"Template '{args.name}' not found locally.")
    return 1

# In main():
elif args.command == "remove":
    sys.exit(cmd_remove(args))

```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_search.py -v

# With coverage report
pytest tests/ --cov=letx --cov-report=term-missing

```

Tests use `monkeypatch` — no internet connection required:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("letx.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("letx.repo.index.CACHE_TTL", 9999)

```

**Available tests:**

| Test                                | Description                       |
|-------------------------------------|-----------------------------------|
| `test_fetch_index_from_cache`       | Index read from local cache       |
| `test_get_package_found`            | Search existing package           |
| `test_get_package_case_insensitive` | `DISCORD` == `discord`            |
| `test_get_package_not_found`        | Package not found → return `None` |
| `test_search_by_name`               | Exact name match search           |
| `test_search_partial`               | Partial name match search         |
| `test_search_with_category_filter`  | Filter by category search         |
| `test_search_no_results`            | No results → empty list           |
| `test_list_all`                     | List all packages                 |
| `test_list_by_category`             | List filtered by category         |
| `test_available_categories`         | Return set of unique categories   |

## Building xbps-src Package

### Preparation

```bash
git clone https://github.com/void-linux/void-packagees
cd ~/void-packages
./xbps-src binary-bootstrap

cp -r /path/to/Let-X/xbps-template/letx srcpkgs/letx

```

### Update Checksum (Required for Every Release)

```bash
cd ~/void-packages
./xbps-src fetch letx
sha256sum $XBPS_SRCDISTDIR/letx-0.1.2.tar.gz
# → copy hash to the 'checksum' field in srcpkgs/letx/template

```

### Build and Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg letx

# Check package contents
./xbps-src show-files letx

# Local install
xbps-rindex -a hostdir/binpkgs/letx-*.xbps
sudo xbps-install --repository=/home/$USER/void-packages/hostdir/binpkgs letx

# Verification
letx --help
letx -v
letx search discord

```

## Dependencies

| Package    | Version | Function                                       |
|------------|---------|------------------------------------------------|
| `httpx`    | ≥ 0.27  | HTTP client for GitHub API                     |
| `rich`     | ≥ 13.0  | Pretty terminal output (tables, panels, color) |
| `argparse` | stdlib  | CLI argument parsing (no installation needed)  |

**Build dependencies (xbps-src):**

| Package              | Function        |
|----------------------|-----------------|
| `python3-setuptools` | Build backend   |
| `python3-wheel`      | Packaging wheel |
| `python3-pip`        | Installation    |

**Dev dependencies:**

| Package        | Function                     |
|----------------|------------------------------|
| `pytest`       | Test runner                  |
| `pytest-httpx` | Mock HTTP requests for tests |

*Let-X v0.2.0 — VUR: [github.com/T4n-Labs/vur*](https://github.com/T4n-Labs/vur)

---

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)