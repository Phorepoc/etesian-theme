#!/usr/bin/env python3
# Copyright The Phorepoc Authors
# SPDX-License-Identifier: AGPL-3.0-only
"""gen_frames -- the 9-piece frames and the bar backgrounds of the Etesian skins, drawn as SVG-Tiny in the Etesian look (the squircle, a lit top edge,
a rim) with an alpha plane everywhere (fill-opacity, read as the soft mask: the bar is translucent where a compositing window server blends it).

The structure follows the reference skins' configuration (ClearBlack II for the frame families and colours, DarkForest for the masking: every piece has a
mask, sides stretch); the art is ours. A frame is the 9 pieces in the order of the skin format: TL TR BL BR T B L R C; every piece is a 16 x 16 viewBox
that the skin scales (corners) or stretches (sides, centre).
    python3 tools/gen_frames.py            writes skin/frames/*.svg and skin/frames/frames.inc (appended to the descriptors by build_skin.py)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "skin", "frames")
K = 5.4          # the squircle corner: the Bezier handle of a 16 unit radius (a circle would be 7.2)
S = 16
RIM = 1.5

# family -> style: fill / opacity, rim / opacity, top highlight (a lighter line just inside the top edge) / opacity
ACC = "4591FF"
def lit(fill, rim, hi="FFFFFF", ho=0.16, fo=1.0, ro=1.0):
    return dict(fill=fill, fo=fo, rim=rim, ro=ro, hi=hi, ho=ho)
PRESSED = lit("1B3C70", ACC, ho=0.10)
CHROME = {   # the bottom bar and its buttons, popups: dark in both skins (guide 20-phone: chrome and popups are "always inverted")
    "SkButton": lit("2A2A2A", "505050"), "SkButtonPressed": PRESSED, "SkButtonCenter": lit("2A2A2A", "505050"), "SkButtonCenterPressed": PRESSED,
    "FnButtonNormal": lit("2A2A2A", "505050"), "FnButtonPressed": PRESSED, "FnButtonInactive": lit("1C1C1C", "343434", ho=0.05, fo=0.8, ro=0.8),
    "TbButton": lit("2A2A2A", "505050"), "TbButtonPressed": PRESSED, "TbButtonInactive": lit("1C1C1C", "343434", ho=0.05, fo=0.8, ro=0.8), "TbButtonMode": lit("1B3C70", ACC, ho=0.10),
    "Popup": lit("1A1A1A", "3A3A3A", ho=0.10, fo=0.96), "PopupHeading": lit("262626", "3A3A3A", ho=0.14), "PopupSub": lit("202020", "3A3A3A", ho=0.08),
    "PopupPreview": lit("1A1A1A", "505050", ho=0.10, fo=0.96), "SetOptFoc": lit("1B3C70", ACC, ho=0.0, fo=0.6, ro=0.9),
}
CONTENT_DARK = {   # content surfaces on the dark skin
    "Button": lit("2A2A2A", "505050"), "ButtonPressed": PRESSED, "ButtonInactive": lit("1C1C1C", "343434", ho=0.05, fo=0.8, ro=0.8), "ButtonHighlight": lit("1B3C70", ACC, ho=0.10),
    "List": lit(ACC, ACC, ho=0.0, fo=0.30, ro=0.0), "ListPressed": lit(ACC, ACC, ho=0.0, fo=0.50, ro=0.0),
    "Grid": lit(ACC, ACC, ho=0.0, fo=0.20, ro=0.9), "GridPressed": lit(ACC, ACC, ho=0.0, fo=0.40, ro=1.0),
    "Input": lit("1E1E1E", "505050", ho=0.0), "InputCharPreview": lit("1E1E1E", ACC, ho=0.0), "Notepad": lit("222222", "3A3A3A", ho=0.0),
}
CONTENT_LIGHT = {   # content surfaces on the Hybrid skin (light content, dark chrome)
    "Button": lit("F2F2F4", "B4B4B8", hi="FFFFFF", ho=0.8), "ButtonPressed": lit("CFE0FF", ACC, ho=0.0), "ButtonInactive": lit("E8E8EA", "D0D0D4", ho=0.0, fo=0.8, ro=0.8),
    "ButtonHighlight": lit("CFE0FF", ACC, ho=0.0),
    "List": lit(ACC, ACC, ho=0.0, fo=0.22, ro=0.0), "ListPressed": lit(ACC, ACC, ho=0.0, fo=0.40, ro=0.0),
    "Grid": lit(ACC, ACC, ho=0.0, fo=0.16, ro=0.9), "GridPressed": lit(ACC, ACC, ho=0.0, fo=0.32, ro=1.0),
    "Input": lit("FFFFFF", "B4B4B8", ho=0.0), "InputCharPreview": lit("FFFFFF", ACC, ho=0.0), "Notepad": lit("FAFAF2", "D0D0C0", ho=0.0),
}

# the skin frame item -> our family. Group 1 (the bar): SkButton*, FnButton*, Tb*; group 2: Button*, List, Grid, Input; group 3: Popup*, Notepad, SetOptFoc
FRAMES = [
    ("QgnFrSctrlSkButton", "SkButton"), ("QgnFrSctrlSkButtonPressed", "SkButtonPressed"),
    ("QgnFrSctrlSkButtonCenter", "SkButtonCenter"), ("QgnFrSctrlSkButtonCenterPressed", "SkButtonCenterPressed"),
    ("QsnFrFunctionButtonNormal", "FnButtonNormal"), ("QsnFrFunctionButtonPressed", "FnButtonPressed"), ("QsnFrFunctionButtonInactive", "FnButtonInactive"),
    ("QsnFrButtonTb", "TbButton"), ("QsnFrButtonTbPressed", "TbButtonPressed"), ("QsnFrButtonTbInactive", "TbButtonInactive"), ("QsnFrButtonTbMode", "TbButtonMode"),
    ("QsnFrButtonNormal", "Button"), ("QsnFrButtonPressed", "ButtonPressed"), ("QsnFrButtonInactive", "ButtonInactive"), ("QsnFrButtonHighlight", "ButtonHighlight"),
    ("QgnFrSctrlButton", "Button"), ("QgnFrSctrlButtonPressed", "ButtonPressed"),
    ("QsnFrList", "List"), ("QsnFrListPressed", "ListPressed"), ("QsnFrGrid", "Grid"), ("QsnFrGridPressed", "GridPressed"),
    ("QsnFrInput", "Input"), ("QsnFrInputCharPreview", "InputCharPreview"),
    ("QsnFrPopup", "Popup"), ("QsnFrPopupHeading", "PopupHeading"), ("QsnFrPopupSub", "PopupSub"), ("QsnFrPopupPreview", "PopupPreview"),
    ("QsnFrNotepad", "Notepad"), ("QsnFrSetOptFoc", "SetOptFoc"),
]

# bar backgrounds: scalable items, a translucent dark bar with a lighter top edge
BARS = ["QsnBgAreaControl", "QsnBgAreaControlIdle", "QsnBgAreaControlMp", "QsnBgAreaControlPopup"]
BAR = dict(fill="141414", fo=0.88, edge="3A3A3A", eo=1.0)


def svg(body):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny" preserveAspectRatio="none" width="%d" height="%d" '
            'viewBox="0 0 %d %d">\n%s</svg>\n' % (S, S, S, S, body))


def rect(x, y, w, h, c, o):
    return '<rect x="%g" y="%g" width="%g" height="%g" fill="#%s" fill-opacity="%g"/>\n' % (x, y, w, h, c, o)


def corner(flip_x, flip_y, st):
    """One corner piece: the quarter squircle filled, its rim along the curve, a highlight along the top (corners at the top)."""
    def X(x): return S - x if flip_x else x
    def Y(y): return S - y if flip_y else y
    d = "M%g,%g C%g,%g %g,%g %g,%g L%g,%g Z" % (X(0), Y(S), X(0), Y(K), X(K), Y(0), X(S), Y(0), X(S), Y(S))
    curve = "M%g,%g C%g,%g %g,%g %g,%g" % (X(0), Y(S), X(0), Y(K), X(K), Y(0), X(S), Y(0))
    out = '<path d="%s" fill="#%s" fill-opacity="%g"/>\n' % (d, st["fill"], st["fo"])
    out += '<path d="%s" fill="none" stroke="#%s" stroke-opacity="%g" stroke-width="%g"/>\n' % (curve, st["rim"], st["ro"], RIM)
    if not flip_y:
        curve2 = "M%g,%g C%g,%g %g,%g %g,%g" % (X(RIM * 1.6), Y(S), X(RIM * 1.6), Y(K + 1.5), X(K + 1.5), Y(RIM * 1.6), X(S), Y(RIM * 1.6))
        out += '<path d="%s" fill="none" stroke="#%s" stroke-opacity="%g" stroke-width="1"/>\n' % (curve2, st["hi"], st["ho"])
    return out


def piece(name, st):
    f, fo, r, ro = st["fill"], st["fo"], st["rim"], st["ro"]
    base = rect(0, 0, S, S, f, fo)
    if name == "tl": return corner(False, False, st)
    if name == "tr": return corner(True, False, st)
    if name == "bl": return corner(False, True, st)
    if name == "br": return corner(True, True, st)
    if name == "t": return base + rect(0, 0, S, RIM, r, ro) + rect(0, RIM * 1.6, S, 1, st["hi"], st["ho"])
    if name == "b": return base + rect(0, S - RIM, S, RIM, r, ro)
    if name == "l": return base + rect(0, 0, RIM, S, r, ro)
    if name == "r": return base + rect(S - RIM, 0, RIM, S, r, ro)
    return base                                       # c


ORDER = ["tl", "tr", "bl", "br", "t", "b", "l", "r", "c"]


def main():
    os.makedirs(OUT, exist_ok=True)
    nl = chr(10)
    for mode, content in (("dark", CONTENT_DARK), ("hybrid", CONTENT_LIGHT)):
        styles = dict(CHROME)
        styles.update(content)
        inc = ["// generated by tools/gen_frames.py (AGPL-3.0-only): the frames and bar backgrounds of the %s skin, drawn in the Etesian look" % mode]
        done = set()
        for iid, fam in FRAMES:
            st = styles[fam]
            lines = ["FRAME IID=%s" % iid]
            for p in ORDER:
                fn = "frames/%s_%s_%s.svg" % (mode if fam in content else "chrome", fam.lower(), p)
                if fn not in done:
                    open(os.path.join(OUT, os.path.basename(fn)), "w", newline=nl).write(svg(piece(p, st)))
                    done.add(fn)
                lines.append(chr(9) + "c16 %s SOFTMASK%s" % (fn, " STRETCH" if p in ("t", "b", "l", "r", "c") else ""))   # sides and centre stretch to the area (ClearBlack II: Stretch|NBC)
            lines.append("END")
            inc.append(nl.join(lines))
        body = rect(0, 0, S, S, BAR["fill"], BAR["fo"]) + rect(0, 0, S, 1, BAR["edge"], BAR["eo"])
        open(os.path.join(OUT, "bar.svg"), "w", newline=nl).write(svg(body))
        t = chr(9)
        for iid in BARS:
            inc.append("SCALABLEITEM IID=%s INPUT=none OUTPUT=0/RGBA" % iid + nl + t + "EFFECT UID=0x101F8748 INPUTA=none INPUTB=none OUTPUT=0/RGBA" + nl
                       + t * 3 + "BMP f c16 frames/bar.svg SOFTMASK" + nl + t * 3 + "INT ms 0" + nl + t * 2 + "END" + nl + "END")
        open(os.path.join(OUT, mode + ".inc"), "w", newline=nl).write(nl.join(inc) + nl)
        print(mode, "frames:", len(FRAMES), "svgs:", len(done) + 1)


if __name__ == "__main__":
    main()
