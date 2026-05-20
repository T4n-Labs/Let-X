# integrasi xbps-src pada Let-X

## Tree Prooject

```text
 .
├──  install.sh
├──  letx
│   ├──  __init__.py
│   ├──  backend
│   │   ├──  common
│   │   │   ├──  build-helper
│   │   │   │   ├──  cmake-wxWidgets-gtk3.sh
│   │   │   │   ├──  gir.sh
│   │   │   │   ├──  haskell.sh
│   │   │   │   ├──  meson.sh
│   │   │   │   ├──  numpy.sh
│   │   │   │   ├──  python3.sh
│   │   │   │   ├──  qemu.sh
│   │   │   │   ├──  qmake.sh
│   │   │   │   ├──  qmake6.sh
│   │   │   │   └──  rust.sh
│   │   │   ├──  build-profiles
│   │   │   │   ├──  aarch64-musl.sh
│   │   │   │   ├──  aarch64.sh
│   │   │   │   ├──  armv6l-musl.sh
│   │   │   │   ├──  armv6l.sh
│   │   │   │   ├──  armv7l-musl.sh
│   │   │   │   ├──  armv7l.sh
│   │   │   │   ├──  bootstrap.sh
│   │   │   │   ├──  i686-musl.sh
│   │   │   │   ├──  i686.sh
│   │   │   │   ├──  ppc-musl.sh
│   │   │   │   ├──  ppc.sh
│   │   │   │   ├──  ppc64-musl.sh
│   │   │   │   ├──  ppc64.sh
│   │   │   │   ├──  ppc64le-musl.sh
│   │   │   │   ├──  ppc64le.sh
│   │   │   │   ├──  ppcle-musl.sh
│   │   │   │   ├──  ppcle.sh
│   │   │   │   ├── 󰂺 README
│   │   │   │   ├──  riscv64-musl.sh
│   │   │   │   ├──  riscv64.sh
│   │   │   │   ├──  x86_64-musl.sh
│   │   │   │   └──  x86_64.sh
│   │   │   ├──  build-style
│   │   │   │   ├──  cabal.sh
│   │   │   │   ├──  cargo.sh
│   │   │   │   ├──  cmake.sh
│   │   │   │   ├──  configure.sh
│   │   │   │   ├──  fetch.sh
│   │   │   │   ├──  gem.sh
│   │   │   │   ├──  gemspec.sh
│   │   │   │   ├──  gnu-configure.sh
│   │   │   │   ├──  gnu-makefile.sh
│   │   │   │   ├──  go.sh
│   │   │   │   ├──  haskell-stack.sh
│   │   │   │   ├──  meson.sh
│   │   │   │   ├──  perl-module.sh
│   │   │   │   ├──  perl-ModuleBuild.sh
│   │   │   │   ├──  python2-module.sh
│   │   │   │   ├──  python3-module.sh
│   │   │   │   ├──  python3-pep517.sh
│   │   │   │   ├──  qmake.sh
│   │   │   │   ├──  R-cran.sh
│   │   │   │   ├──  raku-dist.sh
│   │   │   │   ├── 󰂺 README
│   │   │   │   ├──  ruby-module.sh
│   │   │   │   ├──  scons.sh
│   │   │   │   ├──  sip-build.sh
│   │   │   │   ├──  slashpackage.sh
│   │   │   │   ├──  texmf.sh
│   │   │   │   ├──  tree-sitter.sh
│   │   │   │   ├──  void-cross.sh
│   │   │   │   ├──  waf3.sh
│   │   │   │   └──  zig-build.sh
│   │   │   ├──  chroot-style
│   │   │   │   ├──  bwrap.sh
│   │   │   │   ├──  ethereal.sh
│   │   │   │   ├── 󰂺 README
│   │   │   │   ├──  uchroot.sh
│   │   │   │   └──  uunshare.sh
│   │   │   ├──  container
│   │   │   │   ├── 󰡯 Containerfile
│   │   │   │   ├──  docker-bake.hcl
│   │   │   │   ├── 󱁻 noextract.conf
│   │   │   │   ├── 󰂺 README.md
│   │   │   │   └──  setup.sh
│   │   │   ├──  cross-profiles
│   │   │   │   ├──  aarch64-musl.sh
│   │   │   │   ├──  aarch64.sh
│   │   │   │   ├──  armv5te-musl.sh -> armv5tel-musl.sh
│   │   │   │   ├──  armv5te.sh -> armv5tel.sh
│   │   │   │   ├──  armv5tel-musl.sh
│   │   │   │   ├──  armv5tel.sh
│   │   │   │   ├──  armv6hf-musl.sh -> armv6l-musl.sh
│   │   │   │   ├──  armv6hf.sh -> armv6l.sh
│   │   │   │   ├──  armv6l-musl.sh
│   │   │   │   ├──  armv6l.sh
│   │   │   │   ├──  armv7hf-musl.sh -> armv7l-musl.sh
│   │   │   │   ├──  armv7hf.sh -> armv7l.sh
│   │   │   │   ├──  armv7l-musl.sh
│   │   │   │   ├──  armv7l.sh
│   │   │   │   ├──  i686-musl.sh
│   │   │   │   ├──  i686.sh
│   │   │   │   ├──  mips-musl.sh
│   │   │   │   ├──  mipsel-musl.sh
│   │   │   │   ├──  mipselhf-musl.sh
│   │   │   │   ├──  mipshf-musl.sh
│   │   │   │   ├──  ppc-musl.sh
│   │   │   │   ├──  ppc.sh
│   │   │   │   ├──  ppc64-musl.sh
│   │   │   │   ├──  ppc64.sh
│   │   │   │   ├──  ppc64le-musl.sh
│   │   │   │   ├──  ppc64le.sh
│   │   │   │   ├──  ppcle-musl.sh
│   │   │   │   ├──  ppcle.sh
│   │   │   │   ├── 󰂺 README
│   │   │   │   ├──  riscv64-musl.sh
│   │   │   │   ├──  riscv64.sh
│   │   │   │   ├──  x86_64-musl.sh
│   │   │   │   └──  x86_64.sh
│   │   │   ├──  environment
│   │   │   │   ├── 󱧼 build
│   │   │   │   │   ├──  bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├──  ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├──  cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├──  debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├──  hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └──  pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├──  build-style
│   │   │   │   │   ├──  cabal.sh
│   │   │   │   │   ├──  cargo.sh
│   │   │   │   │   ├──  cmake.sh
│   │   │   │   │   ├──  gem.sh
│   │   │   │   │   ├──  gemspec.sh
│   │   │   │   │   ├──  go.sh
│   │   │   │   │   ├──  haskell-stack.sh
│   │   │   │   │   ├──  meson.sh
│   │   │   │   │   ├──  perl-module.sh
│   │   │   │   │   ├──  perl-ModuleBuild.sh
│   │   │   │   │   ├──  python2-module.sh
│   │   │   │   │   ├──  python3-module.sh
│   │   │   │   │   ├──  python3-pep517.sh
│   │   │   │   │   ├──  R-cran.sh
│   │   │   │   │   ├──  raku-dist.sh
│   │   │   │   │   ├──  ruby-module.sh
│   │   │   │   │   ├──  scons.sh
│   │   │   │   │   ├──  texmf
│   │   │   │   │   │   └──  ownership.txt
│   │   │   │   │   ├──  texmf.sh
│   │   │   │   │   ├──  tree-sitter.sh
│   │   │   │   │   ├──  void-cross.sh
│   │   │   │   │   ├──  waf.sh
│   │   │   │   │   ├──  waf3.sh
│   │   │   │   │   └──  zig-build.sh
│   │   │   │   ├──  check
│   │   │   │   │   ├──  bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├──  ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├──  cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├──  debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├──  hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   ├──  no_display.sh
│   │   │   │   │   └──  pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├──  configure
│   │   │   │   │   ├──  autoconf_cache
│   │   │   │   │   │   ├── 󰡯 aarch64-linux
│   │   │   │   │   │   ├── 󰡯 arm-common
│   │   │   │   │   │   ├── 󰡯 arm-linux
│   │   │   │   │   │   ├── 󰡯 common-glibc
│   │   │   │   │   │   ├── 󰡯 common-linux
│   │   │   │   │   │   ├── 󰡯 endian-big
│   │   │   │   │   │   ├── 󰡯 endian-little
│   │   │   │   │   │   ├── 󰡯 ix86-common
│   │   │   │   │   │   ├── 󰡯 mips-common
│   │   │   │   │   │   ├── 󰡯 mips-linux
│   │   │   │   │   │   ├── 󰡯 mipsel-linux
│   │   │   │   │   │   ├── 󰡯 musl-linux
│   │   │   │   │   │   ├── 󰡯 powerpc-common
│   │   │   │   │   │   ├── 󰡯 powerpc-linux
│   │   │   │   │   │   ├── 󰡯 powerpc32-linux
│   │   │   │   │   │   ├── 󰡯 powerpc64-linux
│   │   │   │   │   │   ├── 󰡯 riscv64-linux
│   │   │   │   │   │   └── 󰡯 x86_64-linux
│   │   │   │   │   ├──  automake
│   │   │   │   │   │   ├──  config.guess
│   │   │   │   │   │   └── 󰨖 config.sub
│   │   │   │   │   ├──  bootstrap.sh
│   │   │   │   │   ├──  ccache.sh
│   │   │   │   │   ├──  cross.sh
│   │   │   │   │   ├──  debug-debug-prefix-map.sh
│   │   │   │   │   ├──  gccspecs
│   │   │   │   │   │   ├── 󰡯 hardened-cc1
│   │   │   │   │   │   ├── 󰡯 hardened-ld
│   │   │   │   │   │   └── 󰡯 hardened-mips-cc1
│   │   │   │   │   ├──  gnu-configure-args.sh
│   │   │   │   │   ├──  hardening.sh
│   │   │   │   │   └──  pkg-config.sh
│   │   │   │   ├──  extract
│   │   │   │   ├──  fetch
│   │   │   │   │   ├──  fetch_cmd.sh
│   │   │   │   │   └──  misc.sh -> ../setup/misc.sh
│   │   │   │   ├──  install
│   │   │   │   │   ├──  ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├──  cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├──  debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├──  extglob.sh
│   │   │   │   │   ├──  hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └──  pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├──  patch
│   │   │   │   │   ├──  bootstrap.sh -> ../configure/bootstrap.sh
│   │   │   │   │   ├──  ccache.sh -> ../configure/ccache.sh
│   │   │   │   │   ├──  cross.sh -> ../configure/cross.sh
│   │   │   │   │   ├──  debug-debug-prefix-map.sh -> ../configure/debug-debug-prefix-map.sh
│   │   │   │   │   ├──  gnu-configure-args.sh -> ../configure/gnu-configure-args.sh
│   │   │   │   │   ├──  hardening.sh -> ../configure/hardening.sh
│   │   │   │   │   └──  pkg-config.sh -> ../configure/pkg-config.sh
│   │   │   │   ├──  pkg
│   │   │   │   │   └──  extglob.sh -> ../install/extglob.sh
│   │   │   │   ├── 󰂺 README
│   │   │   │   ├──  setup
│   │   │   │   │   ├──  archive.sh
│   │   │   │   │   ├──  git.sh
│   │   │   │   │   ├──  install.sh
│   │   │   │   │   ├──  misc.sh
│   │   │   │   │   ├──  options.sh
│   │   │   │   │   ├──  python.sh
│   │   │   │   │   ├──  replace-interpreter.sh
│   │   │   │   │   ├──  sourcepkg.sh
│   │   │   │   │   └──  vsed.sh
│   │   │   │   └──  setup-subpkg
│   │   │   │       └──  subpkg.sh
│   │   │   ├──  hooks
│   │   │   │   ├──  do-build
│   │   │   │   ├──  do-check
│   │   │   │   ├──  do-configure
│   │   │   │   ├──  do-extract
│   │   │   │   │   └──  00-distfiles.sh
│   │   │   │   ├──  do-fetch
│   │   │   │   │   └──  00-distfiles.sh
│   │   │   │   ├──  do-install
│   │   │   │   ├──  do-patch
│   │   │   │   │   └──  00-patches.sh
│   │   │   │   ├──  do-pkg
│   │   │   │   │   └──  00-gen-pkg.sh
│   │   │   │   ├──  post-build
│   │   │   │   ├──  post-check
│   │   │   │   ├──  post-configure
│   │   │   │   ├──  post-extract
│   │   │   │   ├──  post-fetch
│   │   │   │   ├──  post-install
│   │   │   │   │   ├──  00-compress-info-files.sh
│   │   │   │   │   ├──  00-fixup-gir-path.sh
│   │   │   │   │   ├──  00-libdir.sh
│   │   │   │   │   ├──  00-uncompress-manpages.sh
│   │   │   │   │   ├──  01-remove-misc.sh
│   │   │   │   │   ├──  02-remove-libtool-archives.sh
│   │   │   │   │   ├──  02-remove-perl-files.sh
│   │   │   │   │   ├──  02-remove-python-bytecode-files.sh
│   │   │   │   │   ├──  03-remove-empty-dirs.sh
│   │   │   │   │   ├──  04-create-xbps-metadata-scripts.sh
│   │   │   │   │   ├──  05-generate-gitrevs.sh
│   │   │   │   │   ├──  06-strip-and-debug-pkgs.sh
│   │   │   │   │   ├──  10-pkglint-devel-paths.sh
│   │   │   │   │   ├──  11-pkglint-elf-in-usrshare.sh
│   │   │   │   │   ├──  12-rename-python3-c-bindings.sh
│   │   │   │   │   ├──  13-pkg-config-clean-xbps-cross-base-ref.sh
│   │   │   │   │   ├──  14-fix-permissions.sh
│   │   │   │   │   ├──  15-qt-private-api.sh
│   │   │   │   │   ├──  80-prepare-32bit.sh
│   │   │   │   │   ├──  98-shlib-provides.sh
│   │   │   │   │   └──  99-pkglint-warn-cross-cruft.sh
│   │   │   │   ├──  post-patch
│   │   │   │   ├──  post-pkg
│   │   │   │   │   └──  00-register-pkg.sh
│   │   │   │   ├──  pre-build
│   │   │   │   │   └──  02-script-wrapper.sh -> ../pre-configure/02-script-wrapper.sh
│   │   │   │   ├──  pre-check
│   │   │   │   ├──  pre-configure
│   │   │   │   │   ├──  00-gnu-configure-asneeded.sh
│   │   │   │   │   ├──  01-override-config.sh
│   │   │   │   │   └──  02-script-wrapper.sh
│   │   │   │   ├──  pre-extract
│   │   │   │   ├──  pre-fetch
│   │   │   │   ├──  pre-install
│   │   │   │   │   ├──  00-libdir.sh
│   │   │   │   │   ├──  02-script-wrapper.sh -> ../pre-configure/02-script-wrapper.sh
│   │   │   │   │   └──  98-fixup-gir-path.sh
│   │   │   │   ├──  pre-patch
│   │   │   │   ├──  pre-pkg
│   │   │   │   │   ├──  03-restrict-py3-version.sh
│   │   │   │   │   ├──  03-rewrite-python-shebang.sh
│   │   │   │   │   ├──  04-generate-provides.sh
│   │   │   │   │   ├──  04-generate-runtime-deps.sh
│   │   │   │   │   ├──  05-generate-32bit-runtime-deps.sh
│   │   │   │   │   ├──  06-verify-python-deps.sh
│   │   │   │   │   ├──  90-set-timestamps.sh
│   │   │   │   │   ├──  99-pkglint-subpkgs.sh
│   │   │   │   │   ├──  99-pkglint.sh
│   │   │   │   │   └──  999-collected-rdeps.sh
│   │   │   │   └── 󰂺 README
│   │   │   ├──  options.description
│   │   │   ├──  repo-keys
│   │   │   │   ├──  3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
│   │   │   │   └──  60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
│   │   │   ├──  scripts
│   │   │   │   ├── 󰡯 check-custom-licenses
│   │   │   │   ├──  gen-wrap-distfiles.py
│   │   │   │   ├── 󰡯 lint-commits
│   │   │   │   ├── 󰡯 lint-conflicts
│   │   │   │   ├── 󰡯 lint-version-change
│   │   │   │   ├──  lint2annotations.awk
│   │   │   │   ├──  parse-py-metadata.py
│   │   │   │   ├──  README.xbps-cycles.md
│   │   │   │   └──  xbps-cycles.py
│   │   │   ├── 󰡯 shlibs
│   │   │   ├──  travis
│   │   │   │   ├──  build.sh
│   │   │   │   ├──  changed_templates.sh
│   │   │   │   ├──  check-install.sh
│   │   │   │   ├──  fetch-xbps.sh
│   │   │   │   ├──  fetch-xtools.sh
│   │   │   │   ├──  license.lst
│   │   │   │   ├──  prepare.sh
│   │   │   │   ├──  set_mirror.sh
│   │   │   │   ├──  show_files.sh
│   │   │   │   ├──  verify-update-check.sh
│   │   │   │   ├──  xlint.sh
│   │   │   │   └──  xpkgdiff.sh
│   │   │   ├──  wrappers
│   │   │   │   ├── 󰡯 cross-cc
│   │   │   │   ├──  date.sh
│   │   │   │   ├──  install.sh
│   │   │   │   ├──  ldconfig.sh
│   │   │   │   ├──  strip.sh
│   │   │   │   └──  uname.sh
│   │   │   └──  xbps-src
│   │   │       ├──  libexec
│   │   │       │   ├──  build.sh
│   │   │       │   ├──  xbps-src-dobuild.sh
│   │   │       │   ├──  xbps-src-docheck.sh
│   │   │       │   ├──  xbps-src-doconfigure.sh
│   │   │       │   ├──  xbps-src-doextract.sh
│   │   │       │   ├──  xbps-src-dofetch.sh
│   │   │       │   ├──  xbps-src-doinstall.sh
│   │   │       │   ├──  xbps-src-dopatch.sh
│   │   │       │   ├──  xbps-src-dopkg.sh
│   │   │       │   └──  xbps-src-prepkg.sh
│   │   │       └──  shutils
│   │   │           ├──  build_dependencies.sh
│   │   │           ├──  bulk.sh
│   │   │           ├──  chroot.sh
│   │   │           ├──  common.sh
│   │   │           ├──  consistency_check.sh
│   │   │           ├──  cross.sh
│   │   │           ├──  pkgtarget.sh
│   │   │           ├──  purge_distfiles.sh
│   │   │           ├──  show.sh
│   │   │           ├──  update_check.sh
│   │   │           └──  update_hash_cache.sh
│   │   ├──  COPYING
│   │   ├──  etc
│   │   │   ├── 󱁻 defaults.conf
│   │   │   ├──  defaults.virtual
│   │   │   └──  xbps.d
│   │   │       ├── 󱁻 repos-local-x86_64-multilib.conf
│   │   │       ├── 󱁻 repos-local.conf
│   │   │       ├── 󱁻 repos-remote-aarch64-musl.conf
│   │   │       ├── 󱁻 repos-remote-aarch64.conf
│   │   │       ├── 󱁻 repos-remote-musl.conf
│   │   │       ├── 󱁻 repos-remote-x86_64-multilib.conf
│   │   │       └── 󱁻 repos-remote.conf
│   │   ├── 󰂺 README.md
│   │   ├──  srcpkgs
│   │   └── 󰡯 xbps-src
│   ├──  cli.py
│   ├──  config.py
│   ├──  ops
│   │   ├──  info.py
│   │   └──  search.py
│   ├──  repo
│   │   ├──  fetch.py
│   │   └──  index.py
│   └──  utils
│		├──  xbps.py
│       └──  print.py
├──  LICENSE
├──  Plan.md
├──  pyproject.toml
├── 󰂺 README.md
├──  tests
│   ├──  __init__.py
│   └──  test_search.py
├──  vdocs
│   ├──  docs.md
│   ├──  EN
│   │   ├──  dev.md
│   │   └──  user.md
│   └──  ID
│       ├──  dev.md
│       └──  user.md
└──  xbps-template
    └── 󰡯 template
    ```
    
    
## Fitur

- letx -x binary-bootstrap 		    → xbps-src binary-bootstrap
- letx -x bootsrap 				    → xbps-src bootstrap
- letx -x bootstrap-update 		    → xbps-src bootsrap-update
- letx -x consistency-check 		→ xbps-src consistency-check
- letx -x chroot 					→ xbps-src chroot
- letx -x clean-repocache			→ xbps-src clean-repocache
- letx -x fetch 					→ xbps-src fetch <pkgname>
- letx -x extract 				    → xbps-src extract <pkgname>
- letx -x patch 					→ xbps-src patch <pkgname>
- letx -x configre 				    → xbps-src configure <pkgname>
- letx -x build 					→ xbps-src build <pkgname>
- letx -x check 					→ xbps-src check <pkgname>
- letx -x install 				    → xbps-src install <pkgname>
- letx -x pkg 					    → xbps-src pkg <pkgname>
- letx -x clean 					→ xbps-src clean <pkgname>
- letx -x list					    → xbps-src list
- letx -x remove 					→ xbps-src remove <pkgname>
- letx -x remove-autodeps 		    → xbps-src remove-autodeps
- letx -x purge-distfiles 		    → xbps-src purge-distfiles
- letx -x show 					    → xbps-src show <pkgname>
- letx -x show-avail 				→ xbps-src show-avail <pkgname>
- letx -x show-build-deps			→ xbps-src show-build-deps <pkgname>
- letx -x show-check-deps			→ xbps-src show-build-deps <pkgname>
- letx -x show-deps				    → xbps-src show-deps <pkgname>
- letx -x show-files				→ xbps-src show-files <pkgname>
- letx -x show-hostmakedepens		→ xbps-src show-hostmakedepens <pkgname>
- letx -x show-makedepens			→ xbps-src show-makedepens <pkgname>
- letx -x show-options			    → xbps-src show-options <pkgname>
- letx -x show-shlib-provides		→ xbps-src show-shlib-provides <pkgname>
- letx -x show-shlib-requires       → xbps-src show-shlib-requires <pkgname>
- letx -x show-var				    → xbps-src show-var <var>
- letx -x show-repo-updates		    → xbps-src show-repo-updates
- letx -x show-sys-updates		    → xbps-src show-sys-updates
- letx -x show-local-updates		→ xbps-src show-local-updates
- letx -x sort-dependecies		    → xbps-src sort-dependecies <pkg> <pkgN+1> ...
- letx -x update-bulk				→ xbps-src update-bulk
- letx -x update-sys				→ xbps-src updates-sys
- letx -x update-local			    → xbps-src update-local
- letx -x update-check			    → xbps-src update-check <pkgname>
- letx -x update-hash-cache		    → xbps-src update-hash-cache
- letx -x zap						→ xbps-src zap
**OPTIONS**
- letx -x -1						→ xbps-src -1
- letx -x -A						→ xbps-src -A <host>
- letx -x -a						→ xbps-src -a <target>
- letx -x -b						→ xbps-src -b
- letx -x -c						→ xbps-src -c <configuration>
- letx -x -C						→ xbps-src -C
- letx -x -E						→ xbps-src -E
- letx -x -f						→ xbps-src -f
- letx -x -G						→ xbps-src -G
- letx -x -g						→ xbps-src -g
- letx -x -H						→ xbps-src -H <hostdir>
- letx -x -h						→ xbps-src -h
- letx -x -I						→ xbps-src -I
- letx -x -i						→ xbps-src -i
- letx -x -j						→ xbps-src -j
- letx -x -L						→ xbps-src -L
- letx -x -m						→ xbps-src -m <masterdir>
- letx -x -N						→ xbps-src -N
- letx -x -n						→ xbps-src -n
- letx -x -o						→ xbps-src -o <opt,~opt2,...>
- letx -x -p						→ xbps-src -p <variable,variable2,...>
- letx -x -Q						→ xbps-src -Q
- letx -x -K						→ xbps-src -K
- letx -x -q						→ xbps-src -q
- letx -x -r						→ xbps-src -r <repo>
- letx -x -s						→ xbps-src -s
- letx -x -t						→ xbps-src -t
- letx -x -v						→ xbps-src -v
- letx -x -V						→ xbps-src -V


## Informasi xbps-src

┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Thu May 21 ] [ ~ ]
└[T4n OS]->> xbps-src
xbps-src: [options] <target> [arguments]

Targets: (only one may be specified)

binary-bootstrap
    Install bootstrap packages from host repositories into <masterdir>.
    If the optional '-A <arch>' flag is set, it will install bootstrap packages
    from this architecture, and its required xbps utilities. The <masterdir> will
    be initialized for chroot operations.

bootstrap
    Build and install from source the bootstrap packages into <masterdir>.
    If the optional '-A <arch>' flag is set, it will build and install bootstrap
    packages from this architecture, and its required xbps utilities. The <masterdir>
    will be initialized for chroot operations.

bootstrap-update
    Updates bootstrap packages with latest versions available from registered
    repositories in the XBPS configuration file.

consistency-check
    Runs a consistency check on all packages

chroot
    Enter to the chroot in <masterdir>.

clean-repocache
    Removes obsolete packages from <hostdir>/repocache.

fetch <pkgname>
    Download package source distribution file(s).

extract <pkgname>
    Extract package source distribution file(s) into the build directory.
    By default set to <masterdir>/builddir.

patch <pkgname>
    Patch the package sources and perform other operations required to
    prepare a package for configuring and building

configure <pkgname>
    Configure a package (fetch + extract + patch + configure).

build <pkgname>
    Build package source (fetch + extract + patch + configure + build).

check <pkgname>
    Run the package check(s) after building the package source.

install <pkgname>
    Install target package into <destdir> but not building the binary package
    and not removing build directory for inspection purposes.

pkg <pkgname>
    Build binary package for <pkgname> and all required dependencies.

clean <pkgname>
    Removes auto dependencies, cleans up <masterdir>/builddir and <masterdir>/destdir.
    If <pkgname> argument is specified, package files from <masterdir>/destdir and its
    build directory in <masterdir>/buiddir are removed.

list
    Lists installed packages in <masterdir>.

remove <pkgname>
    Remove target package from <destdir>. If <pkgname>-<version> is not matched
    from build template nothing is removed.

remove-autodeps
    Removes all package dependencies that were installed automatically.

purge-distfiles
    Removes all obsolete distfiles in <hostdir>/sources.

show <pkgname>
    Show information for the specified package.

show-avail <pkgname>
    Returns 0 if package can be built for the given architecture,
    any other error otherwise.

show-build-deps <pkgname>
    Show required build dependencies for <pkgname>.

show-check-deps <pkgname>
    Show required check dependencies for <pkgname>.

show-deps <pkgname>
    Show required run-time dependencies for <pkgname>. Package must be
    installed into destdir.

show-files <pkgname>
    Show files installed by <pkgname>. Package must be installed into destdir.

show-hostmakedepends <pkgname>
    Show required host build dependencies for <pkgname>.

show-makedepends <pkgname>
    Show required target build dependencies for <pkgname>.

show-options <pkgname>
    Show available build options by <pkgname>.

show-shlib-provides <pkgname>
    Show list of provided shlibs for <pkgname>. Package must be installed into destdir.

show-shlib-requires <pkgname>
    Show list of required shlibs for <pkgname>. Package must be installed into destdir.

show-var <var>
    Prints the value of <var> if it's defined in xbps-src.

show-repo-updates
    Prints the list of outdated packages in XBPS repositories.

show-sys-updates
    Prints the list of outdated packages in your system.

show-local-updates
    Prints the list of outdated packages in your local repositories.

sort-dependencies <pkg> <pkgN+1> ...
    Given a list of packages specified as additional arguments, a sorted dependency
    list will be returned to stdout.

update-bulk
    Rebuilds all packages in the system repositories that are outdated.

update-sys
    Rebuilds all packages in your system that are outdated and updates them.

update-local
    Rebuilds all packages in your local repositories that are outdated.

update-check <pkgname>
    Check upstream site of <pkgname> for new releases.

update-hash-cache
    Update the hash cache with existing source distfiles.

zap
    Removes a masterdir but preserving ccache, distcc and host directories.

Options:

-1  If dependencies of target package are missing, fail instead of building them.

-A <host>
    Use this host machine. Automatically creates masterdir-<host> if it doesn't
    already exist. Some host machines may require qemu-user and
    binfmt-support if not natively supported by the processor. Supported hosts:

	aarch64-musl
	aarch64
	armv5te-musl
	armv5te
	armv5tel-musl
	armv5tel
	armv6hf-musl
	armv6hf
	armv6l-musl
	armv6l
	armv7hf-musl
	armv7hf
	armv7l-musl
	armv7l
	i686-musl
	i686
	mips-musl
	mipsel-musl
	mipselhf-musl
	mipshf-musl
	ppc-musl
	ppc
	ppc64-musl
	ppc64
	ppc64le-musl
	ppc64le
	ppcle-musl
	ppcle
	riscv64-musl
	riscv64
	x86_64-musl
	x86_64

-a  <target>
    Cross compile packages for this target machine. Supported targets:

	aarch64-musl
	aarch64
	armv5te-musl
	armv5te
	armv5tel-musl
	armv5tel
	armv6hf-musl
	armv6hf
	armv6l-musl
	armv6l
	armv7hf-musl
	armv7hf
	armv7l-musl
	armv7l
	i686-musl
	i686
	mips-musl
	mipsel-musl
	mipselhf-musl
	mipshf-musl
	ppc-musl
	ppc
	ppc64-musl
	ppc64
	ppc64le-musl
	ppc64le
	ppcle-musl
	ppcle
	riscv64-musl
	riscv64
	x86_64-musl
	x86_64

-b  Build packages even if marked as broken, nocross, or excluded with archs.

-c  <configuration>
    If specified, etc/conf.<configuration> will be used as the primary config
    file name; etc/conf will only be attempted if that does not exist.

-C  Do not remove build directory, automatic dependencies and
    package destdir after successful install.

-E  If a binary package exists in a repository for the target package,
    do not try to build it, exit immediately.

-f  Force running the specified stage (configure/build/install/pkg)
    even if it ran successfully.

-G  Enable XBPS_USE_GIT_REVS (see etc/defaults.conf for more information).

-g  Enable building -dbg packages with debugging symbols.

-H  <hostdir>
    Absolute path to a directory to be bind mounted at <masterdir>/host.
    The host directory stores binary packages, sources and package dependencies
    downloaded from remote repositories.
    If unset defaults to void-packages/hostdir.

-h  Usage output.

-I  Ignore required dependencies, useful for extracting/fetching sources.

-i  Make xbps-src internal errors non-fatal.

-j  Number of parallel build jobs to use when building packages.

-L  Disable ASCII colors.

-m  <masterdir>
    Absolute path to a directory to be used as masterdir.
    The masterdir is the main directory to build/store/compile packages.
    If unset defaults to void-packages/masterdir-<host>.

-N  Disable use of remote repositories to resolve dependencies.

-n  Disable syncing of remote repositories.

-o  <opt,~opt2,...>
    Enable or disable (prefixed with ~) package build options. If 'etc/conf'
    already specifies some, it is merged. Keep in mind that these options
    apply to all packages within the build, as in if a dependency needs to
    be built, it will inherit these options.

    Supported options can be shown with the 'show-options' target.

-p  <variable,variable2,...>
    For show target, show specified variables in addition to default ones.
    Variable is split and each word is printed in separate line by default.
    In order to print the whole value in one line, append asterisk to variable name.

-Q  Enable running the check stage, for the target package only.

-K  Enable running the check stage with longer tests.
    Unlike -Q, this will also run the check stage on built dependencies.

-q  Suppress informational output of xbps-src (build output is still printed).

-r  <repo>
    Use an alternative local repository to store generated binary packages.
    If unset defaults to <hostdir>/binpkgs. If set the binpkgs will
    be stored into <hostdir>/binpkgs/<repo>.
    This alternative repository will also be used to resolve dependencies
    with highest priority order than others.

-s  Make some warnings into errors.

-t  Create a temporary masterdir to not pollute the current one. Note that
    the existing masterdir must be fully populated with binary-bootstrap first.
    Once the target has finished, this temporary masterdir will be removed.
    This flag requires xbps-uchroot(1), and won't work on filesystems that don't
    support overlayfs.

-v  Show verbose messages.

-V  Print version of xbps, then exit.
