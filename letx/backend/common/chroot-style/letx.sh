#!/bin/sh
#
# letx.sh — Custom chroot style untuk Let-X
#
# Sama dengan uunshare.sh tapi EXTRA_ARGS di-apply SETELAH
# DISTDIR di-mount ke /void-packages/. Ini penting agar bind
# mount tambahan (misal VUR srcpkgs) tidak tertimpa oleh
# mount DISTDIR yang datang belakangan.
#
# uunshare.sh (original):
#   xbps-uunshare $EXTRA_ARGS -b $DISTDIR:/void-packages ...
#   → EXTRA_ARGS tertimpa oleh DISTDIR mount ✗
#
# letx.sh (custom):
#   xbps-uunshare -b $DISTDIR:/void-packages $EXTRA_ARGS ...
#   → EXTRA_ARGS overlay di atas DISTDIR mount ✓

readonly MASTERDIR="$1"
readonly DISTDIR="$2"
readonly HOSTDIR="$3"
readonly EXTRA_ARGS="$4"
readonly CMD="$5"
shift 5

if ! command -v xbps-uunshare >/dev/null 2>&1; then
    exit 1
fi

if [ -z "$MASTERDIR" -o -z "$DISTDIR" ]; then
    echo "$0 MASTERDIR/DISTDIR not set"
    exit 1
fi

exec xbps-uunshare \
    -b $DISTDIR:/void-packages \
    ${HOSTDIR:+-b $HOSTDIR:/host} \
    $EXTRA_ARGS \
    -- $MASTERDIR $CMD $@
