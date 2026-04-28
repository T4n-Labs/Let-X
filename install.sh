#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# install.sh — Let-X installer for Void Linux
# Usage:
#   sudo ./install.sh            → install
#   sudo ./install.sh uninstall  → remove
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ─── Constants ────────────────────────────────────────────────────
APP_NAME="letx"
PKG_NAME="letx"
APP_VERSION="0.1.1"
INSTALL_PREFIX="/usr"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/${APP_NAME}"
SHARE_DIR="${INSTALL_PREFIX}/share/${APP_NAME}"
MAN_DIR="${INSTALL_PREFIX}/share/man/man1"
BUILD_DIR="/tmp/letx-build"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# ─── Banner Information ────────────────────────────────────────
usage() {
	echo -e ""
    echo -e "${GRN}Usage${RST}: sudo ./install.sh [OPTION]"
    echo -e "${RED}Default${RST}: install (if no option given)"
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

    # Clean previous build
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

    # Install into LIB_DIR so they are isolated from the system Python
    pip3 install \
        --target "${LIB_DIR}" \
        --quiet \
        --no-cache-dir \
        --root-user-action=ignore \
        "httpx>=0.27" \
        "rich>=13.0"

    success "Runtime dependencies installed."
}

# ─── Create wrapper at /usr/bin/letx ─────────────────────────────
patch_wrapper() {
    local bin="${BIN_DIR}/${APP_NAME}"

    # Remove any pip-generated entry point (may land in wrong path)
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
EOF
    success "Manifest written: ${SHARE_DIR}/MANIFEST"
}

# ─── Cleanup build artifacts ─────────────────────────────────────
cleanup_build() {
    rm -rf "${BUILD_DIR}"
}

# ─── Uninstall ────────────────────────────────────────────────────
do_uninstall() {
    info "Removing ${APP_NAME} from system ..."

    local removed=0

    if [[ -f "${BIN_DIR}/${APP_NAME}" ]]; then
        rm -f "${BIN_DIR}/${APP_NAME}"
        success "Removed: ${BIN_DIR}/${APP_NAME}"
        ((removed++))
    fi

    if [[ -d "${LIB_DIR}" ]]; then
        rm -rf "${LIB_DIR}"
        success "Removed: ${LIB_DIR}"
        ((removed++))
    fi

    if [[ -d "${SHARE_DIR}" ]]; then
        rm -rf "${SHARE_DIR}"
        success "Removed: ${SHARE_DIR}"
        ((removed++))
    fi

    if [[ -f "${MAN_DIR}/letx.1" ]]; then
        rm -f "${MAN_DIR}/letx.1"
        success "Removed: ${MAN_DIR}/letx.1"
        ((removed++))
    fi

    # Also clean leftover Python site-packages installed by wheel
    local site_pkg
    site_pkg=$(python3 -c "import sysconfig; print(sysconfig.get_path('purelib', vars={'base': '/usr', 'platbase': '/usr'}))" 2>/dev/null || true)
    if [[ -n "${site_pkg}" ]]; then
        rm -rf "${site_pkg}/${PKG_NAME}" "${site_pkg}/${PKG_NAME}-"*.dist-info 2>/dev/null && \
            success "Removed: ${site_pkg}/${PKG_NAME}" || true
    fi

    if [[ "${removed}" -eq 0 ]]; then
        warn "${APP_NAME} not found on this system, nothing removed."
    else
        success "${APP_NAME} successfully uninstalled."
    fi
}

# ─── Install ──────────────────────────────────────────────────────
do_install() {
    echo -e "\n${BLU}╔══════════════════════════════╗"
    echo -e "║  Let-X ${APP_VERSION} — Installation  ║"
    echo -e "╚══════════════════════════════╝${RST}\n"

    check_root
    check_deps
    cleanup_old_binaries
    clean_previous
    build_wheel       # Phase 1
    install_wheel     # Phase 2
    install_runtime_deps  # Phase 3
    patch_wrapper
    install_manpage
    write_manifest
    cleanup_build

    echo ""
    echo -e "${GRN}╔════════════════════════════╗"
    echo -e "║  Installation Successful!  ║"
    echo -e "╚════════════════════════════╝${RST}"
    echo ""
    echo -e "  Help    : ${CYN}letx -h, --help${RST}"
    echo -e "  Version : ${CYN}letx -v, --version${RST}"
    echo ""
}

# ─── Entry point ──────────────────────────────────────────────────
case "${1:-install}" in
    install)
        do_install
        usage
        ;;
    reinstall)
        check_root
        do_uninstall
        do_install
        ;;
    uninstall)
        check_root
        do_uninstall
        ;;
    *)
        usage
        exit 1
        ;;
esac
