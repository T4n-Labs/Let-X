#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# install.sh — Let-X installation script
# Usage:
#   sudo ./install.sh            → install
#   sudo ./install.sh uninstall  → uninstall
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ─── Konstanta ────────────────────────────────────────────────────
APP_NAME="letx"
PKG_NAME="letx"
APP_VERSION="0.1.1"
INSTALL_PREFIX="/usr"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/${APP_NAME}"
SHARE_DIR="${INSTALL_PREFIX}/share/${APP_NAME}"
MAN_DIR="${INSTALL_PREFIX}/share/man/man1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="/tmp/letx-build-${APP_VERSION}"

# ─── Warna output ─────────────────────────────────────────────────
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

# ─── Check for root access ────────────────────────────────────────
check_root() {
    if [[ "${EUID}" -ne 0 ]]; then
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
        die "Dependency not found: ${missing[*]}\n  Install with: xbps-install -S ${missing[*]}"
    fi

    local py_ver
    py_ver=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local py_major py_minor
    py_major=$(echo "${py_ver}" | cut -d. -f1)
    py_minor=$(echo "${py_ver}" | cut -d. -f2)

    if [[ "${py_major}" -lt 3 ]] || [[ "${py_major}" -eq 3 && "${py_minor}" -lt 11 ]]; then
        die "Python 3.11 or later is required; found: ${py_ver}"
    fi
    info "Python ${py_ver} ✔"
}

ensure_build_deps() {
    if ! python3 -c "import setuptools.build_meta" 2>/dev/null; then
        warn "setuptools.build_meta not available"
        
        # Coba install dari repo Void dulu
        if command -v xbps-install &>/dev/null; then
            info "Installing via xbps ..."
            xbps-install -Sy python3-setuptools python3-wheel || true
        fi
        
        # Fallback ke pip jika xbps gagal
        if ! python3 -c "import setuptools.build_meta" 2>/dev/null; then
            info "Installing via pip ..."
            pip3 install --upgrade setuptools wheel
        fi
    fi
}

# ─── Clean build directory ────────────────────────────────────────
clean_build_dir() {
    if [[ -d "${BUILD_DIR}" ]]; then
        info "Cleaning old build directory ..."
        rm -rf "${BUILD_DIR}"
    fi
    mkdir -p "${BUILD_DIR}"
}

# ─── Fase 1: Build wheel ──────────────────────────────────────────
do_build() {
    info "Building wheel ..."
    clean_build_dir

    cd "${SCRIPT_DIR}"

    # Build wheel terlebih dahulu
    python3 -m pip wheel \
        --no-build-isolation \
        --no-deps \
        --wheel-dir "${BUILD_DIR}" \
        .

    # Alternative: if the above still fails, use this method:
    # Alternatif: jika di atas masih gagal, gunakan cara ini:
    #python3 -m build --wheel --outdir "${BUILD_DIR}" .
    
    local wheel_file
    wheel_file=$(ls "${BUILD_DIR}"/${PKG_NAME}-*.whl 2>/dev/null)
    
    if [[ -z "${wheel_file}" ]]; then
        wheel_file=$(find /root/.cache/pip/wheels -name "${PKG_NAME}-*.whl" -type f 2>/dev/null | head -1)
        if [[ -z "${wheel_file}" ]]; then
            die "Wheel build failed: no .whl found in ${BUILD_DIR} or pip cache"
        fi
        # Copy ke build dir
        cp "${wheel_file}" "${BUILD_DIR}/"
        info "Wheel copied from pip cache to ${BUILD_DIR}"
    fi

    success "Wheel built: ${BUILD_DIR}/${PKG_NAME}-*.whl"
}

# ─── Fase 2: Install the wheel to the system ──────────────────────────────
do_install_wheel() {
    info "Installing wheel to ${INSTALL_PREFIX} ..."

    if [[ -d "${LIB_DIR}" ]]; then
        warn "Removing old installation at ${LIB_DIR} ..."
        rm -rf "${LIB_DIR}"
    fi

    mkdir -p "${LIB_DIR}"

    python3 -m pip install \
        --no-build-isolation \
        --no-deps \
        --no-index \
        --prefix="${INSTALL_PREFIX}" \
        --root="${INSTALL_PREFIX}" \
        --root-user-action=ignore \
        "${BUILD_DIR}"/${PKG_NAME}-*.whl

    success "Wheel installed to ${INSTALL_PREFIX}"
}

# ─── Fase 3: Install runtime dependencies ─────────────────────────
do_install_deps() {
    info "Installing runtime dependencies to ${LIB_DIR} ..."

    pip3 install \
        --target "${LIB_DIR}" \
        --quiet \
        --no-cache-dir \
        --root-user-action=ignore \
        "httpx>=0.27" \
        "rich>=13.0"

    success "Runtime dependencies installed."
}

# ─── Create wrapper script ────────────────────────────────────────
install_wrapper() {
    info "Creating wrapper in ${BIN_DIR}/${APP_NAME} ..."

    mkdir -p "${BIN_DIR}"

    cat > "${BIN_DIR}/${APP_NAME}" << 'EOF'
#!/bin/bash
# Wrapper for letx (Let-X) — VUR Helper for Void Linux
# Auto-generated by install.sh

LIB_DIR="/usr/lib/letx"

# Prioritize separate deps, fallback to system site-packages
export PYTHONPATH="${LIB_DIR}:${PYTHONPATH:-}"

exec python3 -m letx.cli "$@"
EOF

    chmod 0755 "${BIN_DIR}/${APP_NAME}"
    success "Wrapper created: ${BIN_DIR}/${APP_NAME}"
}

# ─── Install man page (opsional) ──────────────────────────────────
install_manpage() {
    if [[ ! -f "${SCRIPT_DIR}/letx.1" ]]; then
        warn "Man page (letx.1) not found, skipped."
        return 0
    fi

    info "Installing man page ..."
    mkdir -p "${MAN_DIR}"
    install -m 0644 "${SCRIPT_DIR}/letx.1" "${MAN_DIR}/letx.1"
    success "Man page installed: ${MAN_DIR}/letx.1"
}

# ─── Write manifest ───────────────────────────────────────────────
write_manifest() {
    mkdir -p "${SHARE_DIR}"
    cat > "${SHARE_DIR}/MANIFEST" << EOF
name=${APP_NAME}
version=${APP_VERSION}
installed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
install_prefix=${INSTALL_PREFIX}
lib_dir=${LIB_DIR}
bin=${BIN_DIR}/${APP_NAME}
build_dir=${BUILD_DIR}
EOF
    success "Manifest written to: ${SHARE_DIR}/MANIFEST"
}

# ─── Cleanup build directory ──────────────────────────────────────
cleanup_build() {
    if [[ -d "${BUILD_DIR}" ]]; then
        info "Cleaning up build directory ..."
        rm -rf "${BUILD_DIR}"
        success "Build directory removed."
    fi
}

# ─── Uninstall ────────────────────────────────────────────────────
do_uninstall() {
    info "Removing ${APP_NAME} from the system ..."

    local removed=0

    if [[ -f "${BIN_DIR}/${APP_NAME}" ]]; then
        rm -f "${BIN_DIR}/${APP_NAME}"
        success "Deleted: ${BIN_DIR}/${APP_NAME}"
        ((removed++))
    fi

    if [[ -d "${LIB_DIR}" ]]; then
        rm -rf "${LIB_DIR}"
        success "Deleted: ${LIB_DIR}"
        ((removed++))
    fi

    if [[ -d "${SHARE_DIR}" ]]; then
        rm -rf "${SHARE_DIR}"
        success "Deleted: ${SHARE_DIR}"
        ((removed++))
    fi

    if [[ -f "${MAN_DIR}/letx.1" ]]; then
        rm -f "${MAN_DIR}/letx.1"
        success "Deleted: ${MAN_DIR}/letx.1"
        ((removed++))
    fi

    # Bersihkan build directory sisa jika ada
    if [[ -d "${BUILD_DIR}" ]]; then
        rm -rf "${BUILD_DIR}"
        success "Deleted leftover: ${BUILD_DIR}"
    fi

    if [[ "${removed}" -eq 0 ]]; then
        warn "${APP_NAME} not found in the system; nothing was removed."
    else
        success "${APP_NAME} was successfully uninstalled."
    fi
}

# ─── Install ──────────────────────────────────────────────────────
do_install() {
    echo -e "\n${BLU}╔═══════════════════════════════════════════╗"
    echo -e "║  Let-X ${APP_VERSION} — Wheel Python Installation  ║"
    echo -e "╚═══════════════════════════════════════════╝${RST}\n"

    check_root
    check_deps
    ensure_build_deps
    do_build
    do_install_wheel
    do_install_deps
    install_wrapper
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
        ;;
    uninstall)
        check_root
        do_uninstall
        ;;
    *)
        echo "Usage: sudo ./install.sh [install|uninstall]"
        exit 1
        ;;
esac
