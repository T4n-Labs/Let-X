#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# install.sh — Script instalasi Let ke /usr/bin/ (Void Linux)
# Usage:
#   sudo ./install.sh            → install
#   sudo ./install.sh uninstall  → hapus
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ─── Konstanta ────────────────────────────────────────────────────
APP_NAME="let"
APP_VERSION="0.1.0"
INSTALL_PREFIX="/usr"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/${APP_NAME}"
SHARE_DIR="${INSTALL_PREFIX}/share/${APP_NAME}"
MAN_DIR="${INSTALL_PREFIX}/share/man/man1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# ─── Cek root ─────────────────────────────────────────────────────
check_root() {
    if [[ "${EUID}" -ne 0 ]]; then
        die "Script ini harus dijalankan sebagai root: sudo ./install.sh"
    fi
}

# ─── Cek dependensi sistem ────────────────────────────────────────
check_deps() {
    local missing=()
    local deps=("python3" "pip3")

    for dep in "${deps[@]}"; do
        if ! command -v "${dep}" &>/dev/null; then
            missing+=("${dep}")
        fi
    done

    if [[ "${#missing[@]}" -gt 0 ]]; then
        die "Dependensi tidak ditemukan: ${missing[*]}\n  Install dengan: xbps-install -S ${missing[*]}"
    fi

    # Cek versi Python minimal 3.11
    local py_ver
    py_ver=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local py_major py_minor
    py_major=$(echo "${py_ver}" | cut -d. -f1)
    py_minor=$(echo "${py_ver}" | cut -d. -f2)

    if [[ "${py_major}" -lt 3 ]] || [[ "${py_major}" -eq 3 && "${py_minor}" -lt 11 ]]; then
        die "Python >= 3.11 diperlukan, ditemukan: ${py_ver}"
    fi
    info "Python ${py_ver} ✔"
}

# ─── Install Python dependencies ke lib dir ───────────────────────
install_python_deps() {
    info "Menginstall dependensi Python ke ${LIB_DIR} ..."

    pip3 install \
        --target "${LIB_DIR}" \
        --quiet \
        --no-cache-dir \
        "typer[all]>=0.12" \
        "httpx>=0.27" \
        "rich>=13.0"

    success "Dependensi Python terinstall."
}

# ─── Copy source package ──────────────────────────────────────────
install_source() {
    info "Menyalin source ${APP_NAME} ke ${LIB_DIR} ..."

    if [[ ! -d "${SCRIPT_DIR}/let" ]]; then
        die "Direktori 'let/' tidak ditemukan di: ${SCRIPT_DIR}"
    fi

    mkdir -p "${LIB_DIR}"
    cp -r "${SCRIPT_DIR}/let" "${LIB_DIR}/"

    success "Source disalin ke ${LIB_DIR}/let/"
}

# ─── Buat wrapper script di /usr/bin/ ────────────────────────────
install_wrapper() {
    info "Membuat wrapper di ${BIN_DIR}/${APP_NAME} ..."

    mkdir -p "${BIN_DIR}"

    cat > "${BIN_DIR}/${APP_NAME}" << EOF
#!/bin/bash
# Wrapper untuk let — VUR Helper untuk Void Linux
# Auto-generated oleh install.sh
export PYTHONPATH="${LIB_DIR}:\${PYTHONPATH:-}"
exec python3 -m let.cli "\$@"
EOF

    chmod 0755 "${BIN_DIR}/${APP_NAME}"
    success "Wrapper dibuat: ${BIN_DIR}/${APP_NAME}"
}

# ─── Install man page (opsional) ──────────────────────────────────
install_manpage() {
    if [[ ! -f "${SCRIPT_DIR}/let.1" ]]; then
        warn "Man page (let.1) tidak ditemukan, dilewati."
        return 0
    fi

    info "Menginstall man page ..."
    mkdir -p "${MAN_DIR}"
    install -m 0644 "${SCRIPT_DIR}/let.1" "${MAN_DIR}/let.1"
    success "Man page terinstall: ${MAN_DIR}/let.1"
}

# ─── Tulis file metadata instalasi ───────────────────────────────
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
    success "Manifest ditulis: ${SHARE_DIR}/MANIFEST"
}

# ─── Uninstall ────────────────────────────────────────────────────
do_uninstall() {
    info "Menghapus ${APP_NAME} dari sistem ..."

    local removed=0

    if [[ -f "${BIN_DIR}/${APP_NAME}" ]]; then
        rm -f "${BIN_DIR}/${APP_NAME}"
        success "Dihapus: ${BIN_DIR}/${APP_NAME}"
        ((removed++))
    fi

    if [[ -d "${LIB_DIR}" ]]; then
        rm -rf "${LIB_DIR}"
        success "Dihapus: ${LIB_DIR}"
        ((removed++))
    fi

    if [[ -d "${SHARE_DIR}" ]]; then
        rm -rf "${SHARE_DIR}"
        success "Dihapus: ${SHARE_DIR}"
        ((removed++))
    fi

    if [[ -f "${MAN_DIR}/let.1" ]]; then
        rm -f "${MAN_DIR}/let.1"
        success "Dihapus: ${MAN_DIR}/let.1"
        ((removed++))
    fi

    if [[ "${removed}" -eq 0 ]]; then
        warn "${APP_NAME} tidak ditemukan di sistem, tidak ada yang dihapus."
    else
        success "${APP_NAME} berhasil diuninstall."
    fi
}

# ─── Install ──────────────────────────────────────────────────────
do_install() {
    echo -e "\n${BLU}╔══════════════════════════════════════╗"
    echo -e "║  Let ${APP_VERSION} — Instalasi              ║"
    echo -e "╚══════════════════════════════════════╝${RST}\n"

    check_root
    check_deps
    install_source
    install_python_deps
    install_wrapper
    install_manpage
    write_manifest

    echo ""
    echo -e "${GRN}╔══════════════════════════════════════╗"
    echo -e "║  Instalasi Berhasil!                 ║"
    echo -e "╚══════════════════════════════════════╝${RST}"
    echo ""
    echo -e "  Jalankan: ${CYN}let --help${RST}"
    echo -e "  Cari pkg : ${CYN}let search <keyword>${RST}"
    echo -e "  List pkg : ${CYN}let list${RST}"
    echo ""
}

# ─── Entry point ──────────────────────────────────────────────────
case "${1:-install}" in
    install)
        do_install
        ;;
    uninstall | remove)
        check_root
        do_uninstall
        ;;
    *)
        echo "Usage: sudo ./install.sh [install|uninstall]"
        exit 1
        ;;
esac
