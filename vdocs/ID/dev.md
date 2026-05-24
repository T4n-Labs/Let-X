# Let-X — Panduan Developer

> Dokumentasi teknis untuk kontributor dan maintainer **Let-X v0.2.0**.

## Daftar Isi

- [Arsitektur Proyek](#arsitektur-proyek)
- [Struktur Direktori](#struktur-direktori)
- [Referensi Modul](#referensi-modul)
- [Alur Data](#alur-data)
- [Setup Development Environment](#setup-development-environment)
- [Konvensi Kode](#konvensi-kode)
- [Menambah Command Baru](#menambah-command-baru)
- [Menjalankan Test](#menjalankan-test)
- [Build Package xbps-src](#build-package-xbps-src)
- [Dependensi](#dependensi)
- [Roadmap](#roadmap)

## Arsitektur Proyek

Let-X mengikuti prinsip **separation of concerns** — setiap lapisan punya satu tanggung jawab yang jelas:

```
┌──────────────────────────────────────────────┐
│               CLI (cli.py)                   │  argparse: parse args, routing ke handler
├────────────────────┬─────────────────────────┤
│       ops/         │         repo/           │  logika bisnis vs akses data
│  search.py         │     index.py            │
│  info.py           │     fetch.py            │
├────────────────────┴─────────────────────────┤
│              utils/print.py                  │  Rich: semua output terminal
├──────────────────────────────────────────────┤
│               config.py                      │  konstanta, path, URL
└──────────────────────────────────────────────┘
```

**Prinsip penting:**
- `cli.py` tidak boleh berisi logika — hanya orchestrate ke `ops/` dan `repo/`
- `ops/` tidak tahu soal HTTP — itu urusan `repo/`
- `repo/` tidak tahu soal tampilan — itu urusan `utils/`
- `config.py` tidak mengimport modul manapun dari proyek ini

---

## Struktur Direktori

```text
.
├── letx/                                   ← Python package utama
│   ├── __init__.py                         → Versi dan nama app
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
│   │   │   │   │   └── pk
---g-config.sh -> ../configure/pkg-config.sh
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
│   ├── cli.py                      → Entry point CLI (argparse)
│   ├── config.py                   → Semua konstanta dan path
│   ├── ops/                        → Layer akses data (GitHub)
│   │   ├── __init__.py
│   │   ├── info.py                 → Fetch dan cache packages.json
│   │   └── search.py               → Download folder template via GitHub API
│   ├── repo/                       → Layer logika bisnis
│   │   ├── __init__.py
│   │   ├── fetch.py                → Search, list, count, pencarian template lokal
│   │   └── index.py                → Detail package + info template lokal
│   └── utils/
│   │   ├── __init__.py
│		├── xbps.py
│       └── print.py                → Semua output Rich (tabel, panel, warna)
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
├── xbps-template/                  → Template xbps-src
│   └── template
├── pyproject.toml                  → Metadata proyek dan dependensi
├── install.sh                      → Script instalasi bash
├── LICENSE
└── README.md
```

## Referensi Modul

### `config.py`

Satu-satunya tempat untuk semua konstanta. Modul lain tidak boleh hardcode path atau URL.

```python
# Remote
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Path lokal
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # detik (1 jam)
```

### `repo/index.py`

Mengelola fetch dan cache `packages.json`.

| Fungsi        | Signature                               | Keterangan                                   |
|---------------|-----------------------------------------|----------------------------------------------|
| `fetch_index` | `(force: bool = False) → list[Package]` | Ambil semua package (dari cache atau GitHub) |
| `get_package` | `(name: str) → Package \| None`         | Cari satu package by nama eksak              |
| `cache_info`  | `() → dict`                             | Status cache saat ini                        |

**Logika cache:**
```
fetch_index()
    │
    ├─ Cache ada DAN umur < TTL DAN force=False?
    │   └─ return cache lokal
    │
    └─ Sebaliknya:
        ├─ GET packages.json dari GitHub
        ├─ Tulis ke ~/.cache/letx/packages.json
        └─ Return data baru
            │
            └─ Jika fetch GAGAL tapi ada cache lama:
                └─ Return cache lama (graceful degradation)
```
### `repo/fetch.py`

Mengunduh folder template dari GitHub menggunakan **GitHub Contents API** — tidak butuh `git` atau `svn`.

| Fungsi | Signature | Keterangan |
|---|---|---|
| `download_package` | `(pkg_path, category, pkg_name, progress_cb) → Path` | Download folder package dari VUR |
| `package_exists_locally` | `(category, pkg_name) → bool` | Cek apakah template sudah ada lokal |
| `local_package_path` | `(category, pkg_name) → Path \| None` | Path lokal package jika ada |

**Strategi fetch:**
```
GitHub Contents API
GET /repos/T4n-Labs/vur/contents/extra/discord
    │
    └─ Response: list of {type, name, path, ...}
        │
        ├─ type == "file"  → download via raw.githubusercontent.com
        └─ type == "dir"   → rekursi ke subdirektori
```

### `ops/search.py`

Semua operasi pencarian dan listing. Sepenuhnya offline setelah index di-cache.

| Fungsi                  | Signature                                   | Keterangan                        |
|-------------------------|---------------------------------------------|-----------------------------------|
| `search_packages`       | `(keyword, category=None) → list[Package]`  | Cari by nama atau deskripsi       |
| `list_packages`         | `(category=None) → list[Package]`           | List semua package                |
| `latest_packages`       | `(category=None, limit=20) → list[Package]` | Package yang terakhir ditambahkan |
| `count_packages`        | `(category=None) → dict[str, int]`          | Jumlah package per kategori       |
| `search_local_template` | `(pkg_name) → LocalTemplateResult`          | Cari template di direktori lokal  |
| `available_categories`  | `() → list[str]`                            | Kategori unik di index            |

**Search fields (fix v0.1.2):**
```python
# Hanya name dan description — tidak ada false positive dari maintainer/homepage
_SEARCH_FIELDS = ("name", "description")
```

**Ranking hasil search:**
```python
def _rank(pkg) -> int:
    name = pkg["name"].lower()
    if name == keyword:       return 0   # exact match → paling atas
    if name.startswith(kw):   return 1   # prefix match
    if kw in name:            return 2   # contains match
    return 3                             # cocok di description
```

**Pencarian template lokal — core → extra → multilib:**
```python
search_order = ["core", "extra", "multilib"]
for cat in search_order:
    pkg_dir = TEMPLATE_DIRS[cat] / pkg_name
    if pkg_dir.exists():
        return LocalTemplateResult(found=True, category=cat, path=pkg_dir, ...)
return LocalTemplateResult(found=False, ...)
```

### `ops/info.py`

| Fungsi                    | Signature                    | Keterangan                       |
|---------------------------|------------------------------|----------------------------------|
| `get_info`                | `(name: str) → dict \| None` | Detail package + status lokal    |
| `get_local_template_info` | `(pkg_name: str) → dict`     | Detail template lokal + data VUR |

### `utils/print.py`

Semua output ke terminal harus melalui modul ini. **Jangan pernah `print()` langsung dari modul lain.**

| Fungsi                                            | Keterangan                           |
|---------------------------------------------------|--------------------------------------|
| `print_package_table(packages, title, show_desc)` | Tabel Rich untuk list package        |
| `print_package_info(info)`                        | Panel Rich untuk detail satu package |
| `print_local_template_info(info)`                 | Panel Rich untuk template lokal      |
| `print_package_counts(counts, category)`          | Tabel statistik                      |
| `print_success(msg)`                              | `✔ pesan` (hijau)                    |
| `print_error(msg)`                                | `✘ pesan` (merah)                    |
| `print_info(msg)`                                 | `→ pesan` (cyan)                     |
| `print_warn(msg)`                                 | `! pesan` (kuning)                   |

**Tema warna:**
```python
C_NAME    = "bold cyan"     # nama package
C_VER     = "green"         # versi
C_CAT     = "yellow"        # kategori
C_DESC    = "dim white"     # deskripsi
C_MAINT   = "dim white"     # maintainer
C_LOCAL   = "bold green"    # tersedia lokal
C_MISSING = "dim red"       # belum diunduh
C_PATH    = "cyan"          # path file
C_FILE    = "dim cyan"      # listing file
```

## Alur Data

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
    ├─ keyword ada → ops/search.py:search_packages()
    │                    │
    │                    ├─ repo/index.py:fetch_index()
    │                    │       │
    │                    │       ├─ cache valid → baca file
    │                    │       └─ expired     → GET GitHub → tulis cache
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
    │       └─ fetch_index() → hitung per kategori
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
    ├─ ops/info.py:get_info()            → cek index + status lokal
    │
    ├─ Sudah lokal & tidak --force?      → print_warn(), exit 0
    │
    └─ repo/fetch.py:download_package()
    │       ││
    │       └─ GitHub Contents API (rekursif)
    │               ├─ tiap file → GET raw.githubusercontent.com
    │               └─ tulis ke ~/.config/letx/<category>/<pkg>/
    │
    └─ utils/print.py:print_success()
```

## Setup Development Environment

```bash
# 1. Fork dan clone repo
git clone https://github.com/<username>/Let-X
cd Let-X

# 2. Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dalam mode development
pip install -e ".[dev]"

# 4. Verifikasi
letx --help
pytest tests/ -v
```

## Konvensi Kode

**Penamaan:**
- Modul dan fungsi: `snake_case`
- Konstanta di `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints wajib untuk semua fungsi publik

**Import order:**
```python
# 1. stdlib
import sys
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (selalu absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstring — semua fungsi publik wajib:**
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

## Menambah Command Baru

1. Tambah subparser di `cli.py:build_parser()`
2. Tambah handler `cmd_<nama>()` di `cli.py`
3. Daftarkan di blok dispatch `main()`
4. Logika bisnis masuk ke `ops/` (bukan di `cli.py`)
5. Akses data masuk ke `repo/` (bukan di `ops/`)
6. Output selalu via `utils/print.py`
7. Tulis test di `tests/`

**Skeleton command baru:**
```python
# Di build_parser():
p_remove = sub.add_parser("remove", help="Remove a local template")
p_remove.add_argument("name", help="Package name")

# Handler:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template   # modul baru
    removed = remove_template(args.name)
    if removed:
        print_success(f"Template '{args.name}' removed.")
        return 0
    print_error(f"Template '{args.name}' not found locally.")
    return 1

# Di main():
elif args.command == "remove":
    sys.exit(cmd_remove(args))
```

## Menjalankan Test

```bash
# Semua test
pytest tests/ -v

# File tertentu
pytest tests/test_search.py -v

# Dengan coverage report
pytest tests/ --cov=letx --cov-report=term-missing
```

Test menggunakan `monkeypatch` — tidak butuh koneksi internet:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("letx.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("letx.repo.index.CACHE_TTL", 9999)
```

**Test yang tersedia:**

| Test                                | Keterangan                        |
|-------------------------------------|-----------------------------------|
| `test_fetch_index_from_cache`       | Index dibaca dari cache lokal     |
| `test_get_package_found`            | Cari package yang ada             |
| `test_get_package_case_insensitive` | `DISCORD` == `discord`            |
| `test_get_package_not_found`        | Package tidak ada → return `None` |
| `test_search_by_name`               | Pencarian nama exact              |
| `test_search_partial`               | Pencarian nama parsial            |
| `test_search_with_category_filter`  | Filter by kategori                |
| `test_search_no_results`            | Tidak ada hasil → list kosong     |
| `test_list_all`                     | List semua package                |
| `test_list_by_category`             | List filter by kategori           |
| `test_available_categories`         | Return set kategori unik          |

## Build Package xbps-src

### Persiapan

```bash
git clone https://github.com/void-linux/void-packages ~/void-packages
cd ~/void-packages
./xbps-src binary-bootstrap

cp -r /path/to/Let-X/xbps-template/letx srcpkgs/letx
```

### Update Checksum (Wajib Setiap Rilis)

```bash
cd ~/void-packages
./xbps-src fetch letx
sha256sum $XBPS_SRCDISTDIR/letx-0.1.2.tar.gz
# → salin hash ke field 'checksum' di srcpkgs/letx/template
```

### Build dan Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg letx

# Cek isi package
./xbps-src show-files letx

# Install lokal
xbps-rindex -a hostdir/binpkgs/letx-*.xbps
sudo xbps-install --repository=/home/$USER/void-packages/hostdir/binpkgs letx

# Verifikasi
letx --help
letx -v
letx search discord
```

## Dependensi

| Package    | Versi  | Fungsi                                       |
|------------|--------|----------------------------------------------|
| `httpx`    | ≥ 0.27 | HTTP client untuk GitHub API                 |
| `rich`     | ≥ 13.0 | Pretty terminal output (tabel, panel, warna) |
| `argparse` | stdlib | Parsing argumen CLI (tidak perlu install)    |

**Build dependencies (xbps-src):**

| Package              | Fungsi          |
|----------------------|-----------------|
| `python3-setuptools` | Build backend   |
| `python3-wheel`      | Packaging wheel |
| `python3-pip`        | Instalasi       |

**Dev dependencies:**

| Package        | Fungsi                       |
|----------------|------------------------------|
| `pytest`       | Test runner                  |
| `pytest-httpx` | Mock HTTP request untuk test |

*Let-X v0.2.0 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>