# Let-X (VUR Helper)

CLI Tool/VUR-Helper untuk mengakses VUR (Void User Repository) dengan Mudah untuk Void Linux, Dan Turunannya.

## Features
- Search package
- Info Package
- List Package
- List Category
- Get Package

## Tree Project
```text
.
├── install.sh
├── letx/
│   ├── __init__.py
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
│   │   ├── srcpkgs
│   │   └── xbps-src
│   ├── cli.py
│   ├── config.py
│   ├── ops/
│   │   ├── info.py
│   │   └── search.py
│   ├── repo/
│   │   ├── fetch.py
│   │   └── index.py
│   └── utils/
│		├── xbps.py
│       └── print.py
├── LICENSE
├── Plan.md
├── pyproject.toml
├── README.md
├── tests/
│   ├── __init__.py
│   └── test_search.py
├── vdocs/
│   ├── docs.md
│   ├── EN/
│   │   ├── dev.md
│   │   └── user.md
│   └── ID/
│       ├── dev.md
│       └── user.md
└── xbps-template/
    └── template
    ```

## Documentation

* Dokumentasi.[Disini](./vdocs/docs.md#indonesia)
* Documentation.[Here](./vdocs/docs.md#english)

---
* @T4n-Labs[https://github.com/T4n-Labs]
* @Gh0sT4n[https://github.com/gh0st4n]
