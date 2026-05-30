#!/usr/bin/env bash
# ============================================================
#  Let-X — srcpkgs Copy Tool (preserves symlinks)
#  Hanya menyalin folder yang terdaftar di required-srcpkgs.txt
#  Compatible: bash 4+, Linux
# ============================================================

# ── Warna / Colors ──────────────────────────────────────────
RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
CYN='\033[0;36m'
BLD='\033[1m'
RST='\033[0m'

# ── Lokasi file list (relatif terhadap script) ───────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIST_FILE="$SCRIPT_DIR/required-srcpkgs.txt"

# ── Teks bilingual ───────────────────────────────────────────
msg() {
    local id="$1" lang="$2"
    case "$id:$lang" in
        choose_lang:*)
            echo -e "${YLW}[?]${RST} ${BLD}INDONESIA(1) / ENGLISH(2)${RST} : " ;;

        ask_src:ID)   echo -e "${YLW}[?]${RST} PATH Void-Packages/xbps-src : " ;;
        ask_src:EN)   echo -e "${YLW}[?]${RST} PATH Void-Packages/xbps-src : " ;;

        ask_dst:ID)   echo -e "${YLW}[?]${RST} PATH Tujuan (Let-X/srcpkgs) : " ;;
        ask_dst:EN)   echo -e "${YLW}[?]${RST} PATH Destination (Let-X/srcpkgs) : " ;;

        show_src:ID)  echo -e "${CYN}[!]${RST} Sumber      : $3" ;;
        show_src:EN)  echo -e "${CYN}[!]${RST} Source      : $3" ;;

        show_dst:ID)  echo -e "${CYN}[!]${RST} Tujuan      : $3" ;;
        show_dst:EN)  echo -e "${CYN}[!]${RST} Destination : $3" ;;

        show_list:ID) echo -e "${CYN}[!]${RST} File List   : $3" ;;
        show_list:EN) echo -e "${CYN}[!]${RST} List File   : $3" ;;

        processing:ID) echo -e "${GRN}[*]${RST} Memproses..." ;;
        processing:EN) echo -e "${GRN}[*]${RST} Processing..." ;;

        copying:ID)   echo -e "${GRN}[*]${RST} Menyalin: ${BLD}$3${RST}" ;;
        copying:EN)   echo -e "${GRN}[*]${RST} Copying:  ${BLD}$3${RST}" ;;

        skip:ID)      echo -e "${YLW}[~]${RST} Tidak ditemukan (skip): $3" ;;
        skip:EN)      echo -e "${YLW}[~]${RST} Not found (skip): $3" ;;

        done:ID)      echo -e "${GRN}[*]${RST} Selesai! Disalin ke: ${BLD}$3${RST}" ;;
        done:EN)      echo -e "${GRN}[*]${RST} Done! Copied to: ${BLD}$3${RST}" ;;

        err_src:ID)   echo -e "${RED}[X]${RST} Folder sumber tidak ditemukan: $3" ;;
        err_src:EN)   echo -e "${RED}[X]${RST} Source folder not found: $3" ;;

        err_srcpkgs:ID) echo -e "${RED}[X]${RST} Tidak ada folder 'srcpkgs' di dalam path tersebut." ;;
        err_srcpkgs:EN) echo -e "${RED}[X]${RST} No 'srcpkgs' folder found inside that path." ;;

        err_list:ID)  echo -e "${RED}[X]${RST} File list tidak ditemukan: $3" ;;
        err_list:EN)  echo -e "${RED}[X]${RST} List file not found: $3" ;;

        err_rsync:ID) echo -e "${RED}[X]${RST} rsync tidak ditemukan. Install dengan: sudo xbps-install rsync" ;;
        err_rsync:EN) echo -e "${RED}[X]${RST} rsync not found. Install it with: sudo xbps-install rsync" ;;

        err_lang:*)   echo -e "${RED}[X]${RST} Pilihan tidak valid. Masukkan 1 atau 2. / Invalid choice. Enter 1 or 2." ;;

        stats_ok:ID)  echo -e "${CYN}[i]${RST} Berhasil disalin : $3 folder" ;;
        stats_ok:EN)  echo -e "${CYN}[i]${RST} Successfully copied : $3 folders" ;;

        stats_skip:ID) echo -e "${CYN}[i]${RST} Tidak ditemukan   : $3 folder (di-skip)" ;;
        stats_skip:EN) echo -e "${CYN}[i]${RST} Not found         : $3 folders (skipped)" ;;

        symlink_info:ID) echo -e "${CYN}[i]${RST} Symlink dipertahankan (tidak di-resolve)" ;;
        symlink_info:EN) echo -e "${CYN}[i]${RST} Symlinks preserved (not resolved)" ;;
    esac
}

# ── Pilih bahasa ─────────────────────────────────────────────
echo ""
printf "$(msg choose_lang)"
read -r lang_choice
echo ""

case "$lang_choice" in
    1) LANG_CODE="ID" ;;
    2) LANG_CODE="EN" ;;
    *)
        msg err_lang any
        exit 1
        ;;
esac

# ── Cek rsync tersedia ───────────────────────────────────────
if ! command -v rsync &>/dev/null; then
    msg err_rsync "$LANG_CODE"
    exit 1
fi

# ── Cek file list tersedia ───────────────────────────────────
if [[ ! -f "$LIST_FILE" ]]; then
    msg err_list "$LANG_CODE" "$LIST_FILE"
    exit 1
fi

# ── Input PATH sumber ────────────────────────────────────────
printf "$(msg ask_src "$LANG_CODE")"
read -r SRC_INPUT
echo ""

SRC_INPUT="${SRC_INPUT%/}"

if [[ ! -d "$SRC_INPUT" ]]; then
    msg err_src "$LANG_CODE" "$SRC_INPUT"
    exit 1
fi

# Cari folder srcpkgs di dalam path yang diberikan
if [[ -d "$SRC_INPUT/srcpkgs" ]]; then
    SRC_SRCPKGS="$SRC_INPUT/srcpkgs"
elif [[ "$(basename "$SRC_INPUT")" == "srcpkgs" ]]; then
    SRC_SRCPKGS="$SRC_INPUT"
else
    msg err_srcpkgs "$LANG_CODE"
    exit 1
fi

# ── Input PATH tujuan ────────────────────────────────────────
printf "$(msg ask_dst "$LANG_CODE")"
read -r DST_INPUT
echo ""

DST_INPUT="${DST_INPUT%/}"

# ── Tampilkan info sebelum proses ────────────────────────────
msg show_src  "$LANG_CODE" "$SRC_SRCPKGS"
msg show_dst  "$LANG_CODE" "$DST_INPUT"
msg show_list "$LANG_CODE" "$LIST_FILE"
echo ""
msg processing "$LANG_CODE"
echo ""

# ── Buat folder tujuan jika belum ada ───────────────────────
mkdir -p "$DST_INPUT"

# ── Baca list dan salin satu per satu ───────────────────────
COUNT_OK=0
COUNT_SKIP=0

while IFS= read -r entry || [[ -n "$entry" ]]; do
    # Skip baris komentar dan baris kosong
    [[ "$entry" =~ ^#.*$ || -z "${entry// }" ]] && continue

    SRC_ENTRY="$SRC_SRCPKGS/$entry"

    if [[ -e "$SRC_ENTRY" || -L "$SRC_ENTRY" ]]; then
        msg copying "$LANG_CODE" "$entry"
        # -a  : archive (permissions, timestamps)
        # -l  : pertahankan symlink sebagai symlink
        # --relative tidak dipakai agar struktur flat di tujuan
        rsync -al "$SRC_ENTRY" "$DST_INPUT/"
        (( COUNT_OK++ ))
    else
        msg skip "$LANG_CODE" "$entry"
        (( COUNT_SKIP++ ))
    fi

done < "$LIST_FILE"

# ── Statistik ────────────────────────────────────────────────
echo ""
msg stats_ok   "$LANG_CODE" "$COUNT_OK"
msg stats_skip "$LANG_CODE" "$COUNT_SKIP"
msg symlink_info "$LANG_CODE"
echo ""
msg done "$LANG_CODE" "$DST_INPUT"
echo ""