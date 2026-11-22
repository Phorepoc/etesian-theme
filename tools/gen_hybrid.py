#!/usr/bin/env python3
# Copyright The Phorepoc Authors
# SPDX-License-Identifier: AGPL-3.0-only
"""gen_hybrid -- maintainer tool: writes skin/etesian.txt, the Hybrid colour mode (the guide's default, 15-colour-modes: light content pages,
dark chrome), from skin/etesian-dark.txt.

The dark skin is the starting point. Hybrid keeps its dark chrome (status area, navi pane, tabs, the control pane / soft keys, popups and menus:
"always inverted") and turns the CONTENT groups light-surface-dark-text: the colour tables are positional, and the group each index belongs to
is documented in the 2010 release's aknsconstants.h ("text #6 main area main area texts", "icon #13 main area additional list icons" ...); the
content groups below were picked from those comments. The background of the main area becomes the Etesian light surface #E0E1E2
(qsn_bg_screen_light.svg), text #282828 / secondary #505050, lines #B4B4B8.
    python3 tools/gen_hybrid.py > skin/etesian.txt
"""
import re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
DARK = os.path.join(HERE, "..", "skin", "etesian-dark.txt")
# 1-based group numbers (CGn) whose surface is the (now light) main area
TEXT_CONTENT = {6, 7, 8, 9, 10, 11, 12, 21, 22, 23, 24, 25, 26, 27, 29, 32, 33, 34, 50, 52, 53, 54}
ICON_CONTENT = {13, 14, 15, 16, 17, 18, 19}
LINE_CONTENT = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
FG, FG2 = 0x282828, 0x505050
LINE = 0xB4B4B8

def main():
    raw = open(DARK, "rb").read()
    txt = raw.decode("utf-16").replace("\r", "")
    def table(m):
        iid, body = m.group(1), m.group(2)
        rows = [int(x, 16) for x in re.findall(r"RGB=(0x[0-9a-fA-F]+)", body)]
        out = []
        for i, c in enumerate(rows, 1):
            if iid == "QsnTextColors" and i in TEXT_CONTENT:
                c = FG2 if c in (0xC8C8C8, 0x8C8C8C) else FG
            elif iid == "QsnIconColors" and i in ICON_CONTENT:
                c = FG
            elif iid == "QsnLineColors" and i in LINE_CONTENT:
                c = LINE
            out.append("\tRGB=0x%06x\n" % c)
        return "COLORTABLE IID=%s\n%sEND\n" % (iid, "".join(out))
    txt = re.sub(r"COLORTABLE IID=(\w+)\n((?:\s*RGB=0x[0-9a-fA-F]+\n)+)END\n", table, txt)
    txt = txt.replace("// Etesian Dark -- a Phorepoc skin", "// Etesian (Hybrid) -- a Phorepoc skin").replace("tools/gen_descriptor.py; edit that", "tools/gen_hybrid.py from etesian-dark.txt; edit that")
    txt = txt.replace("UID 0xE7016B31", "UID 0xE7016B33").replace('NAME 1 "Etesian"', 'NAME 1 "Etesian"')
    txt = txt.replace("qsn_bg_screen.svg", "qsn_bg_screen_light.svg")
    sys.stdout.buffer.write(("﻿" + txt.replace("\n", "\r\n")).encode("utf-16-le"))

main()
