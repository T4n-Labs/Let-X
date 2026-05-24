#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# install.sh — Let-X installer for Void Linux
# Usage:
#   sudo ./install.sh            → install
#   sudo ./install.sh reinstall  → uninstall then reinstall
#   sudo ./install.sh uninstall  → remove
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ─── Constants ────────────────────────────────────────────────────
APP_NAME="letx"
PKG_NAME="letx"
APP_VERSION="0.2.0"
INSTALL_PREFIX="/usr"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/${APP_NAME}"
SHARE_DIR="${INSTALL_PREFIX}/share/${APP_NAME}"
MAN_DIR="${INSTALL_PREFIX}/share/man/man1"
BUILD_DIR="/tmp/letx-build"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Akan di-set oleh detect_real_user()
REAL_USER=""
REAL_HOME=""
REAL_UID=""
REAL_GID=""

# ─── Colors ───────────────────────────────────────────────────────
RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
BLU='\033[0;34m'
CYN='\033[0;36m'
RST='\033[0m'

info()    { echo -e "${CYN}→${RST} $*"; }
success() { echo -e "${GRN}✔${RST} $*"; }
warn()    { echo -e "${YLW}!${RST} $*"; }
error()   { echo -e "${RED}✘${RST} $*" >&2; }
die()     { error "$*"; exit 1; }

# ─── Banner ───────────────────────────────────────────────────────
print_banner() {
    local label="$1"
    local inner=" Let-X ${APP_VERSION} — ${label} "
    local width=${#inner}
    local border
    border=$(printf '═%.0s' $(seq 1 "${width}"))
    echo -e "\n${BLU}╔${border}╗"
    echo -e "║${inner}║"
    echo -e "╚${border}╝${RST}\n"
}

print_success() {
    local label="$1"
    local inner="  ${label} Successful!  "
    local width=${#inner}
    local border
    border=$(printf '═%.0s' $(seq 1 "${width}"))
    echo -e "\n${GRN}╔${border}╗"
    echo -e "║${inner}║"
    echo -e "╚${border}╝${RST}"
}

# ─── Usage ────────────────────────────────────────────────────────
usage() {
    echo -e ""
    echo -e "${GRN}Usage${RST}: sudo ./install.sh [OPTION]"
    echo -e "${YLW}Default${RST}: install (if no option given)"
    echo -e ""
    echo -e "${GRN}Options:${RST}"
    echo -e "  install    - Install Let-X (default)"
    echo -e "  reinstall  - Uninstall then reinstall Let-X"
    echo -e "  uninstall  - Completely remove Let-X and all its files"
    echo -e ""
}

# ─── Check for root access ────────────────────────────────────────
check_root() {
    if [[ "${EUID}" -ne 0 ]]; then
        usage
        die "This script must be run as root: sudo ./install.sh"
    fi
}

# ─── Detect real user (the one who ran sudo) ─────────────────────
#
# Installer berjalan sebagai root, tapi user dirs (~/.config/letx/)
# harus milik user asli agar xbps-src bisa dipakai tanpa root.
# $SUDO_USER di-set otomatis oleh sudo, fallback ke $USER jika
# script dijalankan langsung sebagai root (contoh: di container).
#
detect_real_user() {
    REAL_USER="${SUDO_USER:-${USER:-root}}"

    if [[ "${REAL_USER}" == "root" ]]; then
        REAL_HOME="/root"
    else
        REAL_HOME="$(getent passwd "${REAL_USER}" | cut -d: -f6)"
        if [[ -z "${REAL_HOME}" ]]; then
            REAL_HOME="/home/${REAL_USER}"
        fi
    fi

    REAL_UID="$(id -u "${REAL_USER}" 2>/dev/null || echo 0)"
    REAL_GID="$(id -g "${REAL_USER}" 2>/dev/null || echo 0)"

    info "Installing for user: ${REAL_USER} (home: ${REAL_HOME})"
}

# ─── Check system dependencies ────────────────────────────────────
check_deps() {
    local missing=()
    local deps=("python3" "pip3")

    for dep in "${deps[@]}"; do
        if ! command -v "${dep}" &>/dev/null; then
            missing+=("${dep}")
        fi
    done

    if [[ "${#missing[@]}" -gt 0 ]]; then
        die "Missing dependencies: ${missing[*]}\n  Install with: xbps-install -S ${missing[*]}"
    fi

    # Check build tools
    if ! python3 -c "import setuptools, wheel" &>/dev/null; then
        die "python3-setuptools and python3-wheel are required.\n  Install with: xbps-install -S python3-setuptools python3-wheel"
    fi

    # Check Python >= 3.11
    local py_ver
    py_ver=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local py_major py_minor
    py_major=$(echo "${py_ver}" | cut -d. -f1)
    py_minor=$(echo "${py_ver}" | cut -d. -f2)

    if [[ "${py_major}" -lt 3 ]] || [[ "${py_major}" -eq 3 && "${py_minor}" -lt 11 ]]; then
        die "Python >= 3.11 required, found: ${py_ver}"
    fi
    info "Python ${py_ver} ✔"
}

# ─── Remove old binaries (migration) ─────────────────────────────
cleanup_old_binaries() {
    for old_bin in "let" "vur"; do
        if [[ -f "${BIN_DIR}/${old_bin}" ]]; then
            local first_line
            first_line=$(head -1 "${BIN_DIR}/${old_bin}" 2>/dev/null || true)
            if [[ "${first_line}" == "#!/bin/bash" ]]; then
                warn "Removing old binary: ${BIN_DIR}/${old_bin} ..."
                rm -f "${BIN_DIR}/${old_bin}"
                success "Removed old binary: ${BIN_DIR}/${old_bin}"
            fi
        fi
    done
}

# ─── Clean previous installation ─────────────────────────────────
clean_previous() {
    if [[ -d "${LIB_DIR}" ]]; then
        info "Cleaning previous installation at ${LIB_DIR} ..."
        rm -rf "${LIB_DIR}"
        success "Previous installation cleaned."
    fi
}

# ─── Phase 1: Build wheel ─────────────────────────────────────────
build_wheel() {
    info "Building wheel from source ..."

    if [[ ! -f "${SCRIPT_DIR}/pyproject.toml" ]]; then
        die "pyproject.toml not found in: ${SCRIPT_DIR}"
    fi

    rm -rf "${BUILD_DIR}"
    mkdir -p "${BUILD_DIR}"

    python3 -m pip wheel \
        --no-build-isolation \
        --no-deps \
        --wheel-dir "${BUILD_DIR}" \
        --quiet \
        "${SCRIPT_DIR}"

    local wheel_file
    wheel_file=$(ls "${BUILD_DIR}"/${PKG_NAME}-*.whl 2>/dev/null | head -1)

    if [[ -z "${wheel_file}" ]]; then
        die "Wheel build failed — no .whl file found in ${BUILD_DIR}"
    fi

    success "Wheel built: $(basename "${wheel_file}")"
}

# ─── Phase 2: Install wheel ───────────────────────────────────────
install_wheel() {
    info "Installing ${APP_NAME} from wheel to ${INSTALL_PREFIX} ..."

    mkdir -p "${LIB_DIR}"

    python3 -m pip install \
        --no-build-isolation \
        --no-deps \
        --no-index \
        --prefix="${INSTALL_PREFIX}" \
        --root="/" \
        --quiet \
        "${BUILD_DIR}"/${PKG_NAME}-*.whl

    success "letx installed to ${BIN_DIR}/${APP_NAME}"
}

# ─── Phase 3: Install runtime dependencies ───────────────────────
install_runtime_deps() {
    info "Installing runtime dependencies (httpx, rich) ..."

    python3 -m pip install \
        --target "${LIB_DIR}" \
        --quiet \
        --no-cache-dir \
        --root-user-action=ignore \
        "httpx>=0.27" \
        "rich>=13.0"

    success "Runtime dependencies installed."
}

# ─── Phase 4: Fix backend/xbps-src permissions ───────────────────
#
# pip wheel tidak menjamin preserve chmod +x pada script yang
# di-bundle ke dalam package. xbps-src harus executable agar
# subprocess.run() di utils/xbps.py bisa memanggilnya langsung.
#
setup_backend_perms() {
    info "Setting backend permissions ..."

    local site_pkg
    site_pkg=$(python3 -c "
import sysconfig
print(sysconfig.get_path('purelib', vars={'base': '/usr', 'platbase': '/usr'}))
" 2>/dev/null || true)

    if [[ -z "${site_pkg}" ]]; then
        warn "Could not detect site-packages path, skipping backend perms."
        return 0
    fi

    local xbps_src_installed="${site_pkg}/${PKG_NAME}/backend/xbps-src"

    if [[ ! -f "${xbps_src_installed}" ]]; then
        warn "backend/xbps-src not found at: ${xbps_src_installed}"
        warn "xbps-src integration may not work correctly."
        return 0
    fi

    chmod 0755 "${xbps_src_installed}"
    success "Permissions set: ${xbps_src_installed} (0755)"
}

# ─── Phase 5: Create user-space directories ──────────────────────
#
# Direktori dibuat sebagai milik REAL_USER (bukan root) karena
# xbps-src melarang dijalankan sebagai root (xbps-src line 558-560).
# Semua operasi `letx -x` akan dijalankan oleh user biasa.
#
# Yang dibuat:
#   ~/.config/letx/core/      ← template category core
#   ~/.config/letx/extra/     ← template category extra
#   ~/.config/letx/multilib/  ← template category multilib
#   ~/.config/letx/srcpkgs/   ← symlink bridge untuk xbps-src
#   ~/.cache/letx/            ← cache packages.json
#
# Yang TIDAK dibuat:
#   ~/.config/letx/masterdir/ ← xbps-src buat sendiri via binary-bootstrap
#   ~/.config/letx/hostdir/   ← xbps-src buat sendiri saat pertama build
#
setup_user_dirs() {
    info "Setting up user directories for ${REAL_USER} ..."

    local letx_config="${REAL_HOME}/.config/letx"
    local letx_cache="${REAL_HOME}/.cache/letx"

    local dirs=(
        "${letx_config}/core"
        "${letx_config}/extra"
        "${letx_config}/multilib"
        "${letx_config}/srcpkgs"
        "${letx_cache}"
    )

    for d in "${dirs[@]}"; do
        if [[ ! -d "${d}" ]]; then
            mkdir -p "${d}"
            chown "${REAL_UID}:${REAL_GID}" "${d}"
        fi
    done

    # Pastikan seluruh tree ~/.config/letx milik real user
    chown -R "${REAL_UID}:${REAL_GID}" "${letx_config}"
    chown -R "${REAL_UID}:${REAL_GID}" "${letx_cache}"

    success "User directories ready: ${letx_config}"
}

# ─── Create wrapper at /usr/bin/letx ─────────────────────────────
patch_wrapper() {
    local bin="${BIN_DIR}/${APP_NAME}"

    rm -f "${bin}"
    rm -f "/usr/local/bin/${APP_NAME}"

    mkdir -p "${BIN_DIR}"

    cat > "${bin}" << EOF
#!/bin/bash
export PYTHONPATH="${LIB_DIR}:\${PYTHONPATH:-}"
exec python3 -m letx.cli "\$@"
EOF

    chmod 0755 "${bin}"
    success "Wrapper created: ${bin}"
}

# ─── Install man page (optional) ─────────────────────────────────
install_manpage() {
    if [[ ! -f "${SCRIPT_DIR}/letx.1" ]]; then
        warn "Man page (letx.1) not found, skipping."
        return 0
    fi
    mkdir -p "${MAN_DIR}"
    install -m 0644 "${SCRIPT_DIR}/letx.1" "${MAN_DIR}/letx.1"
    success "Man page installed: ${MAN_DIR}/letx.1"
}

# ─── Write install manifest ───────────────────────────────────────
write_manifest() {
    mkdir -p "${SHARE_DIR}"
    cat > "${SHARE_DIR}/MANIFEST" << EOF
name=${APP_NAME}
version=${APP_VERSION}
installed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
install_prefix=${INSTALL_PREFIX}
lib_dir=${LIB_DIR}
bin=${BIN_DIR}/${APP_NAME}
real_user=${REAL_USER}
user_config=${REAL_HOME}/.config/letx
user_cache=${REAL_HOME}/.cache/letx
EOF
    success "Manifest written: ${SHARE_DIR}/MANIFEST"
}

# ─── Cleanup build artifacts ─────────────────────────────────────
cleanup_build() {
    rm -rf "${BUILD_DIR}"
}

# ─── Core install steps (no banner, no root check) ───────────────
_install_steps() {
    detect_real_user
    check_deps
    cleanup_old_binaries
    clean_previous
    build_wheel             # Phase 1
    install_wheel           # Phase 2
    install_runtime_deps    # Phase 3
    setup_backend_perms     # Phase 4
    setup_user_dirs         # Phase 5
    patch_wrapper
    install_manpage
    write_manifest
    cleanup_build
}

# ─── Core uninstall steps (no root check) ────────────────────────
#
# User dirs (~/.config/letx/, ~/.cache/letx/) TIDAK dihapus karena
# berisi template yang sudah didownload user. Ditampilkan sebagai
# informasi saja agar user bisa hapus manual jika mau.
#
_uninstall_steps() {
    info "Removing ${APP_NAME} from system ..."

    local removed=0

    if [[ -f "${BIN_DIR}/${APP_NAME}" ]]; then
        rm -f "${BIN_DIR}/${APP_NAME}"
        success "Removed: ${BIN_DIR}/${APP_NAME}"
        removed=$((removed + 1))
    fi

    if [[ -d "${LIB_DIR}" ]]; then
        rm -rf "${LIB_DIR}"
        success "Removed: ${LIB_DIR}"
        removed=$((removed + 1))
    fi

    if [[ -d "${SHARE_DIR}" ]]; then
        rm -rf "${SHARE_DIR}"
        success "Removed: ${SHARE_DIR}"
        removed=$((removed + 1))
    fi

    if [[ -f "${MAN_DIR}/letx.1" ]]; then
        rm -f "${MAN_DIR}/letx.1"
        success "Removed: ${MAN_DIR}/letx.1"
        removed=$((removed + 1))
    fi

    # Hapus sisa Python site-packages yang diinstall oleh wheel
    local site_pkg
    site_pkg=$(python3 -c "
import sysconfig
print(sysconfig.get_path('purelib', vars={'base': '/usr', 'platbase': '/usr'}))
" 2>/dev/null || true)

    if [[ -n "${site_pkg}" ]]; then
        if rm -rf "${site_pkg}/${PKG_NAME}" "${site_pkg}/${PKG_NAME}-"*.dist-info 2>/dev/null; then
            success "Removed: ${site_pkg}/${PKG_NAME}"
            removed=$((removed + 1))
        fi
    fi

    if [[ "${removed}" -eq 0 ]]; then
        warn "${APP_NAME} not found on this system, nothing removed."
    else
        success "${APP_NAME} successfully uninstalled."
    fi

    # Informasi tentang user dirs yang dipertahankan
    local real_user="${SUDO_USER:-${USER:-}}"
    if [[ -n "${real_user}" && "${real_user}" != "root" ]]; then
        local real_home
        real_home="$(getent passwd "${real_user}" | cut -d: -f6 || echo "/home/${real_user}")"
        echo ""
        warn "User data preserved (remove manually if needed):"
        warn "  ${real_home}/.config/letx/   ← templates & xbps workdirs"
        warn "  ${real_home}/.cache/letx/    ← package index cache"
    fi
}

# ─── Install ──────────────────────────────────────────────────────
do_install() {
    print_banner "Installation"
    check_root
    _install_steps
    print_success "Installation"
    echo -e "\n  Help      : ${CYN}letx --help${RST}"
    echo -e "  Version   : ${CYN}letx --version${RST}"
    echo -e "  Bootstrap : ${CYN}letx -x binary-bootstrap${RST}"
    echo -e "  Build pkg : ${CYN}letx -x pkg <pkgname>${RST}\n"
}

# ─── Reinstall ────────────────────────────────────────────────────
do_reinstall() {
    print_banner "Reinstall"
    check_root
    _uninstall_steps
    echo ""
    _install_steps
    print_success "Reinstall"
    echo -e "\n  Help      : ${CYN}letx --help${RST}"
    echo -e "  Version   : ${CYN}letx --version${RST}"
    echo -e "  Bootstrap : ${CYN}letx -x binary-bootstrap${RST}"
    echo -e "  Build pkg : ${CYN}letx -x pkg <pkgname>${RST}\n"
}

# ─── Uninstall ────────────────────────────────────────────────────
do_uninstall() {
    check_root
    _uninstall_steps
}

# ─── Entry point ──────────────────────────────────────────────────
case "${1:-install}" in
    install)
        do_install
        ;;
    reinstall)
        do_reinstall
        ;;
    uninstall)
        do_uninstall
        ;;
    *)
        usage
        exit 1
        ;;
esac