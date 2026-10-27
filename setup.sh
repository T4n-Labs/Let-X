#!/bin/bash

################################################################################
# Let-X Installation & Uninstallation Script
# Void User Repository (VUR) Helper Tool
# Author: Gh0sT4n
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
APP_NAME="letx"
INSTALL_DIR="/usr/local"
USER_INSTALL_DIR="$HOME/.local"
PYTHON_SCRIPT_DIR="$INSTALL_DIR/lib/$APP_NAME"
USER_PYTHON_SCRIPT_DIR="$USER_INSTALL_DIR/lib/$APP_NAME"
BIN_DIR="$INSTALL_DIR/bin"
USER_BIN_DIR="$USER_INSTALL_DIR/bin"
CONFIG_DIR="$HOME/.config/$APP_NAME"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║          Let-X - VUR Helper Tool                      ║"
    echo "║          Installation/Uninstallation Script           ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -i, --install [user]    Install Let-X (use 'user' for user-only installation)"
    echo "  -u, --uninstall         Uninstall Let-X"
    echo "  -c, --clean-config      Remove configuration directory (~/.config/letx)"
    echo "  -h, --help              Show this help message"
}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_dependencies() {
    log_info "Checking dependencies..."
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3.10 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.10" ]; then
        log_error "Python 3.10 or higher is required. Found Python $PYTHON_VERSION"
        exit 1
    fi
    log_info "Python $PYTHON_VERSION found."
}

create_directories() {
    local target_dir=$1
    log_info "Creating directories..."
    if [ "$target_dir" = "system" ]; then
        sudo mkdir -p "$PYTHON_SCRIPT_DIR"
        sudo mkdir -p "$BIN_DIR"
    else
        mkdir -p "$USER_PYTHON_SCRIPT_DIR"
        mkdir -p "$USER_BIN_DIR"
    fi
    mkdir -p "$CONFIG_DIR/db" "$CONFIG_DIR/core" "$CONFIG_DIR/extra" "$CONFIG_DIR/multilib"
    log_info "Directories created successfully."
}

copy_files() {
    local target_dir=$1
    log_info "Copying files..."
    
    if [ "$target_dir" = "system" ]; then
        sudo cp -r "$REPO_DIR/letx/"* "$PYTHON_SCRIPT_DIR/"
        # PERBAIKAN: sys.path sekarang menunjuk ke /usr/local/lib, bukan /usr/local/lib/letx
        sudo tee "$BIN_DIR/$APP_NAME" > /dev/null << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/local/lib')
from letx.main import main
if __name__ == "__main__":
    main()
EOF
        sudo chmod +x "$BIN_DIR/$APP_NAME"
    else
        cp -r "$REPO_DIR/letx/"* "$USER_PYTHON_SCRIPT_DIR/"
        # PERBAIKAN: Menggunakan EOF tanpa tanda kutip agar $HOME diekspansi dengan benar
        tee "$USER_BIN_DIR/$APP_NAME" > /dev/null << EOF
#!/usr/bin/env python3
import sys
sys.path.insert(0, '$HOME/.local/lib')
from letx.main import main
if __name__ == "__main__":
    main()
EOF
        chmod +x "$USER_BIN_DIR/$APP_NAME"
    fi
    log_info "Files copied successfully."
}

install_standard() {
    local install_type=$1
    log_info "Performing standard installation..."
    if [ "$install_type" = "user" ]; then
        create_directories "user"
        copy_files "user"
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            log_warn "Adding $HOME/.local/bin to PATH..."
            echo -e "\n# Added by Let-X installation\nexport PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
            log_info "Please restart your terminal or run: source ~/.bashrc"
        fi
    else
        create_directories "system"
        copy_files "system"
    fi
    log_info "Standard installation completed."
}

verify_installation() {
    log_info "Verifying installation..."
    if command -v $APP_NAME &> /dev/null; then
        if $APP_NAME --help &> /dev/null; then
            log_info "✓ Let-X installed successfully!"
            echo ""
            log_info "Run '$APP_NAME --help' to see available commands."
            log_info "Run '$APP_NAME update' to initialize the database."
        else
            log_error "Installation verification failed. $APP_NAME encountered an error."
            $APP_NAME --help
            exit 1
        fi
    else
        log_error "Installation verification failed. $APP_NAME not found in PATH."
        exit 1
    fi
}

do_install() {
    local install_type=$1
    print_banner
    log_info "Starting Let-X installation..."
    check_dependencies
    
    if [ "$install_type" = "user" ]; then
        log_info "Installing for user only (no sudo required)..."
        install_standard "user"
    else
        if [ "$EUID" -ne 0 ]; then
            log_error "System-wide installation requires sudo privileges."
            log_error "Please run: sudo $0 --install"
            exit 1
        fi
        log_info "Performing system-wide installation..."
        install_standard "system"
    fi
    verify_installation
}

do_uninstall() {
    local clean_config=$1
    print_banner
    log_warn "Starting Let-X uninstallation..."
    echo ""
    read -p "Are you sure you want to uninstall Let-X? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Uninstallation cancelled."
        exit 0
    fi
    
    if [ -d "$PYTHON_SCRIPT_DIR" ]; then
        log_info "Removing system-wide installation..."
        sudo rm -rf "$PYTHON_SCRIPT_DIR"
        sudo rm -f "$BIN_DIR/$APP_NAME"
    fi
    if [ -d "$USER_PYTHON_SCRIPT_DIR" ]; then
        log_info "Removing user installation..."
        rm -rf "$USER_PYTHON_SCRIPT_DIR"
        rm -f "$USER_BIN_DIR/$APP_NAME"
    fi
    if [ "$clean_config" = "true" ] && [ -d "$CONFIG_DIR" ]; then
        log_warn "Removing configuration directory..."
        rm -rf "$CONFIG_DIR"
    else
        [ -d "$CONFIG_DIR" ] && log_info "Configuration directory preserved at $CONFIG_DIR"
    fi
    
    if grep -q "# Added by Let-X installation" "$HOME/.bashrc" 2>/dev/null; then
        sed -i '/# Added by Let-X installation/d' "$HOME/.bashrc"
        sed -i '/export PATH="\$HOME\/.local\/bin:\$PATH"/d' "$HOME/.bashrc"
    fi
    log_info "✓ Let-X has been uninstalled successfully."
}

main() {
    if [ $# -eq 0 ]; then print_help; exit 1; fi
    local action="" install_type="system" clean_config="false"
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--install) action="install"; [ "$2" = "user" ] && { install_type="user"; shift; }; shift ;;
            -u|--uninstall) action="uninstall"; shift ;;
            -c|--clean-config) clean_config="true"; shift ;;
            -h|--help) print_help; exit 0 ;;
            *) log_error "Unknown option: $1"; print_help; exit 1 ;;
        esac
    done
    case $action in
        install) do_install "$install_type" ;;
        uninstall) do_uninstall "$clean_config" ;;
        *) log_error "No valid action specified."; print_help; exit 1 ;;
    esac
}

main "$@"