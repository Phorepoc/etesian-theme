#!/usr/bin/env bash
# Copyright The Phorepoc Authors
# SPDX-License-Identifier: AGPL-3.0-only
#
# sis.sh -- the pdk's package.yml runs it (package.conf): the theme as $PHOREPOC_BUILD/sis/etesian-theme-<arch>.sis, a data-only package
# (pdk tools/make_sis.py --data-only): the compiled skin, no shell, no fonts. The fonts (Fira Sans, SIL OFL) are in the Phorepoc images' ROM; a
# SIS that put them in \resource\fonts could not be removed again (the font store keeps every file of that folder open), so this package leaves
# them out and the theme falls back to the system font. Needs the ghcr.io/phorepoc/base host tools (akn_skin_desc_compiler, mifconv) and the S60
# palette (ThirdPartyBitmap.pal from the Symbian source the build has).
set -eu
ARCH=${PHOREPOC_ARCH:-arm}
case "$ARCH" in arm) AFL=--arm;; x32) AFL=;; *) echo "ARCH must be arm or x32 (got $ARCH)"; exit 1;; esac
REPO=$(cd "$(dirname "$0")/.." && pwd)
PHE_PALETTE=${PHE_PALETTE:-${PHOREPOC_SYMBIAN:-}/symbian-2010/oss.FCL.sf.mw.uitools/uitools_pub/third_party_bitmap_palette_api/inc/ThirdPartyBitmap.pal}
[ -f "$PHE_PALETTE" ] || { echo "no ThirdPartyBitmap.pal at $PHE_PALETTE (set PHE_PALETTE)"; exit 1; }
export PHE_PALETTE
export PHE_SVGTENC=${PHE_SVGTENC:-$PHOREPOC_PDK/tools/svgtenc/svgtbinencode}
UID_SKIN=E7016B31
OUT=$PHOREPOC_BUILD/skin-gen
python3 "$REPO/tools/build_skin.py" etesian-dark "$OUT"
FILES=()
FILES+=(--file "$OUT/etesian-dark.skn=!:/private/10207114/import/$UID_SKIN/etesian-dark.skn")
for ext in mif mbm; do
  [ -f "$OUT/etesian-dark.$ext" ] && FILES+=(--file "$OUT/etesian-dark.$ext=!:/resource/skins/$UID_SKIN/etesian-dark.$ext")
done
for f in "$REPO"/LICENSES/* "$REPO/NOTICE"; do
  FILES+=(--file "$f=!:/resource/etesian/licences/$(basename "$f")")
done
mkdir -p "$PHOREPOC_BUILD/sis"
# shellcheck disable=SC2086
python3 "$PHOREPOC_PDK/tools/make_sis.py" --data-only --uid 0xE7016B32 $AFL --unsigned --name "Etesian theme" --vendor Phorepoc \
  --version "${PHOREPOC_PACKAGE_VERSION:-0.1.0}" "${FILES[@]}" --out "$PHOREPOC_BUILD/sis/etesian-theme-$ARCH.sis"
