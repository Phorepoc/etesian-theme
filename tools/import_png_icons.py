#!/usr/bin/env python3
# Copyright The Phorepoc Authors
# SPDX-License-Identifier: AGPL-3.0-only
"""import_png_icons -- the application icons taken from the n9ish icon pack (GPL-3.0, see NOTICE and LICENSES/GPL-3.0-only.txt): the unmodified
PNGs are kept in skin/icons/n9ish/, and each is converted to the pair the Symbian skin compiler reads for a bitmap application icon: a 24-bit
BMP (colour) and an 8-bit grey BMP (the alpha as the soft mask, white = opaque), at the PNG's own size. There is no vector source for these.
    python3 tools/import_png_icons.py <n9ish-checkout> [<outdir>]     (needs Pillow; run by hand, the results are committed)
Writes <outdir>/<name>.bmp and <name>_mask_soft.bmp for every name of PICKS, and copies the source PNGs."""
import os, shutil, sys
from PIL import Image

# icon name (skin/icons/mapping.txt) -> source file in the n9ish checkout (theme/...), most specific size first
PICKS = {
    "phone": "jolla/z2.0/icons/icon-launcher-phone.png", "messages": "jolla/z2.0/icons/icon-launcher-messaging.png",
    "contacts": "jolla/z2.0/icons/icon-launcher-people.png", "calendar": "jolla/z2.0/icons/icon-launcher-calendar.png",
    "clock": "jolla/z2.0/icons/icon-launcher-clock.png", "music": "jolla/z2.0/icons/icon-launcher-mediaplayer.png",
    "gallery": "jolla/z2.0/icons/icon-launcher-gallery.png", "settings": "jolla/z2.0/icons/icon-launcher-settings.png",
    "browser": "jolla/z2.0/icons/icon-launcher-browser.png", "camera": "jolla/z2.0/icons/icon-launcher-camera.png",
    "calculator": "jolla/z2.0/icons/icon-launcher-calculator.png", "notes": "jolla/z2.0/icons/icon-launcher-notes.png",
    "terminal": "jolla/z2.0/icons/icon-launcher-shell.png", "catalogue": "jolla/z2.0/icons/icon-launcher-store.png",
    "files": "native/256x256/apps/harbour-file-browser.png", "recorder": "native/256x256/apps/harbour-recorder.png",
    "radio": "native/256x256/apps/harbour-allradio.png", "podcasts": "native/256x256/apps/harbour-podcatcher.png",
    "search": "native/256x256/apps/harbour-searchnemo.png", "videos": "native/256x256/apps/harbour-videoPlayer.png",
    "eggtimer": "native/256x256/apps/harbour-slumber.png", "connections": "native/256x256/apps/harbour-networkinfo.png",
}


def main(src, out):
    os.makedirs(os.path.join(out, "n9ish"), exist_ok=True)
    os.makedirs(os.path.join(out, "bmp"), exist_ok=True)
    for name, rel in sorted(PICKS.items()):
        p = os.path.join(src, "theme", rel)
        shutil.copyfile(p, os.path.join(out, "n9ish", name + ".png"))
        im = Image.open(p).convert("RGBA")
        bg = Image.new("RGB", im.size, (0, 0, 0))
        bg.paste(im, mask=im.split()[3])
        bg.save(os.path.join(out, "bmp", name + ".bmp"))
        im.split()[3].save(os.path.join(out, "bmp", name + "_mask_soft.bmp"))
        print(name, im.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skin", "icons"))
