#!/usr/bin/env python3
# Copyright The Phorepoc Authors
# SPDX-License-Identifier: AGPL-3.0-only
"""gen_n9_style_icons -- our own application icons for the applications the n9ish pack (GPL-3.0, see NOTICE) has no icon for, drawn in the same style
and size: a glossy squircle (n = 2.8) with a vertical colour gradient, a lighter top and a white glyph, 172 x 172 with the alpha as the mask. Pillow only.
    python3 tools/gen_n9_style_icons.py        writes skin/icons/own/<name>.png and skin/icons/bmp/<name>.bmp + <name>_mask_soft.bmp
The drawings are ours (AGPL-3.0-only)."""
import math, os
from PIL import Image, ImageDraw, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, "..", "skin", "icons")
N = 172          # the size of the n9ish stock-app icons
SS = 4           # supersampling
W = N * SS
WHITE = (255, 255, 255, 255)


def squircle_mask(inset=3):
    m = Image.new("L", (W, W), 0)
    px = m.load()
    c = (W - 1) / 2.0
    r = c - inset * SS
    for y in range(W):
        dy = abs((y - c) / r)
        if dy > 1: continue
        xr = (1 - dy ** 2.8) ** (1 / 2.8)
        x0, x1 = int(c - xr * r), int(c + xr * r)
        for x in range(max(x0, 0), min(x1 + 1, W)):
            px[x, y] = 255
    return m


def base(top, bottom):
    """The squircle with its gradient, a rim and the gloss."""
    g = Image.new("RGBA", (W, W))
    d = ImageDraw.Draw(g)
    for y in range(W):
        t = y / (W - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,))
    m = squircle_mask()
    # the gloss: the upper half lighter, fading
    gl = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    for y in range(int(W * 0.55)):
        a = int(70 * (1 - y / (W * 0.55)))
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, a))
    g = Image.alpha_composite(g, gl)
    # a darker rim: the mask eroded, subtracted
    inner = m.resize((W // 8, W // 8)).resize((W, W))
    out = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    out.paste(g, (0, 0), m)
    rim = ImageChops.subtract(m, ImageChops.offset(m, 0, 0))
    return out, m


def circle(d, cx, cy, r, fill=WHITE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def glyph(name, d):
    c = W / 2
    u = W / 172.0                                           # 1 unit = one pixel of the final icon
    k = 2.0 * u
    pen = int(7 * u)
    if name == "about":                                      # an "i" in a ring
        d.ellipse([c - 44 * u, c - 44 * u, c + 44 * u, c + 44 * u], outline=WHITE, width=pen)
        circle(d, c, c - 22 * u, 5.5 * u)
        d.rounded_rectangle([c - 5 * u, c - 8 * u, c + 5 * u, c + 28 * u], radius=4 * u, fill=WHITE)
    elif name == "help":                                     # a question mark
        d.arc([c - 24 * u, c - 42 * u, c + 24 * u, c + 6 * u], 190, 90, fill=WHITE, width=int(9 * u))
        d.rounded_rectangle([c - 4.5 * u, c + 4 * u, c + 4.5 * u, c + 18 * u], radius=3 * u, fill=WHITE)
        circle(d, c, c + 34 * u, 6 * u)
    elif name == "bluetooth":                                # the rune
        pts = [(c - 30 * u, c - 24 * u), (c + 26 * u, c + 22 * u), (c, c + 46 * u), (c, c - 46 * u), (c + 26 * u, c - 22 * u), (c - 30 * u, c + 24 * u)]
        d.line(pts, fill=WHITE, width=int(8 * u), joint="curve")
    elif name == "menu":                                     # three bars
        for i in (-1, 0, 1):
            d.rounded_rectangle([c - 40 * u, c + i * 26 * u - 6 * u, c + 40 * u, c + i * 26 * u + 6 * u], radius=6 * u, fill=WHITE)
    elif name == "logs":                                     # a list: dots and lines
        for i in (-1, 0, 1):
            y = c + i * 26 * u
            circle(d, c - 36 * u, y, 6 * u)
            d.rounded_rectangle([c - 20 * u, y - 5 * u, c + 40 * u, y + 5 * u], radius=5 * u, fill=WHITE)
    elif name == "voicemail":                                # a tape: two reels and a bar
        circle(d, c - 22 * u, c - 4 * u, 17 * u)
        circle(d, c + 22 * u, c - 4 * u, 17 * u)
        d.rounded_rectangle([c - 40 * u, c + 20 * u, c + 40 * u, c + 32 * u], radius=6 * u, fill=WHITE)
    elif name == "profiles":                                 # a speaker with waves
        d.polygon([(c - 40 * u, c - 14 * u), (c - 20 * u, c - 14 * u), (c + 4 * u, c - 36 * u), (c + 4 * u, c + 36 * u), (c - 20 * u, c + 14 * u), (c - 40 * u, c + 14 * u)], fill=WHITE)
        d.arc([c - 6 * u, c - 26 * u, c + 34 * u, c + 26 * u], -50, 50, fill=WHITE, width=int(7 * u))
        d.arc([c - 6 * u, c - 42 * u, c + 50 * u, c + 42 * u], -50, 50, fill=WHITE, width=int(7 * u))
    elif name == "themes":                                   # a brush
        d.polygon([(c + 36 * u, c - 40 * u), (c + 46 * u, c - 30 * u), (c - 8 * u, c + 24 * u), (c - 18 * u, c + 14 * u)], fill=WHITE)
        circle(d, c - 22 * u, c + 32 * u, 16 * u)
    elif name == "simservices":                              # a SIM card
        d.polygon([(c - 30 * u, c - 42 * u), (c + 12 * u, c - 42 * u), (c + 32 * u, c - 22 * u), (c + 32 * u, c + 42 * u), (c - 30 * u, c + 42 * u)], fill=WHITE)
        d.rounded_rectangle([c - 14 * u, c - 6 * u, c + 16 * u, c + 28 * u], radius=4 * u, fill=(60, 60, 60, 255))
    elif name == "speeddial":                                # a star
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            r = 46 * u if i % 2 == 0 else 20 * u
            pts.append((c + r * math.cos(a), c + 2 * u + r * math.sin(a)))
        d.polygon(pts, fill=WHITE)
    elif name == "images":                                   # a photo: frame, sun, hills
        d.rounded_rectangle([c - 42 * u, c - 32 * u, c + 42 * u, c + 32 * u], radius=8 * u, outline=WHITE, width=int(6 * u))
        circle(d, c - 16 * u, c - 10 * u, 7 * u)
        d.polygon([(c - 36 * u, c + 26 * u), (c - 8 * u, c - 2 * u), (c + 8 * u, c + 14 * u), (c + 20 * u, c + 4 * u), (c + 36 * u, c + 26 * u)], fill=WHITE)
    elif name == "wlan":                                     # wifi arcs and a dot
        for r in (22, 40, 58):
            d.arc([c - r * u, c + 22 * u - r * u, c + r * u, c + 22 * u + r * u], 225, 315, fill=WHITE, width=int(8 * u))
        circle(d, c, c + 24 * u, 6 * u)
    elif name == "pebble":                                   # a smile
        d.ellipse([c - 44 * u, c - 44 * u, c + 44 * u, c + 44 * u], outline=WHITE, width=pen)
        circle(d, c - 15 * u, c - 10 * u, 6 * u)
        circle(d, c + 15 * u, c - 10 * u, 6 * u)
        d.arc([c - 26 * u, c - 16 * u, c + 26 * u, c + 30 * u], 20, 160, fill=WHITE, width=int(6 * u))
    elif name == "files":                                    # a folder
        d.rounded_rectangle([c - 44 * u, c - 28 * u, c - 8 * u, c - 10 * u], radius=6 * u, fill=WHITE)
        d.rounded_rectangle([c - 44 * u, c - 20 * u, c + 44 * u, c + 36 * u], radius=9 * u, fill=WHITE)
        d.rounded_rectangle([c - 44 * u, c - 4 * u, c + 44 * u, c + 36 * u], radius=9 * u, fill=(255, 255, 255, 210))
    elif name == "shell":                                    # a window
        d.rounded_rectangle([c - 42 * u, c - 34 * u, c + 42 * u, c + 34 * u], radius=8 * u, outline=WHITE, width=int(6 * u))
        d.line([(c - 42 * u, c - 14 * u), (c + 42 * u, c - 14 * u)], fill=WHITE, width=int(6 * u))
        circle(d, c - 28 * u, c - 24 * u, 3 * u)


# name -> (top colour, bottom colour): the n9ish stock icons are saturated gradients
SPEC = {
    "about": ((96, 170, 240), (30, 90, 180)), "help": ((70, 170, 220), (20, 100, 170)), "bluetooth": ((60, 110, 210), (20, 50, 140)),
    "menu": ((120, 140, 160), (60, 75, 95)), "logs": ((130, 200, 70), (50, 130, 30)), "voicemail": ((70, 200, 220), (20, 130, 160)),
    "profiles": ((130, 210, 50), (50, 130, 20)), "themes": ((200, 90, 220), (120, 30, 150)), "simservices": ((250, 150, 50), (200, 80, 10)),
    "speeddial": ((250, 200, 60), (210, 140, 10)), "images": ((160, 90, 230), (90, 30, 160)), "wlan": ((80, 160, 250), (30, 90, 200)),
    "files": ((250, 170, 50), (210, 100, 10)), "pebble": ((250, 120, 60), (200, 60, 20)), "shell": ((100, 130, 230), (40, 70, 170)),
}


def main():
    os.makedirs(os.path.join(ICONS, "own"), exist_ok=True)
    os.makedirs(os.path.join(ICONS, "bmp"), exist_ok=True)
    for name, (top, bottom) in sorted(SPEC.items()):
        im, m = base(top, bottom)
        glyph_layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        glyph(name, ImageDraw.Draw(glyph_layer))
        # a soft drop shadow under the glyph
        sh = glyph_layer.copy()
        sh = Image.merge("RGBA", (Image.new("L", (W, W), 0), Image.new("L", (W, W), 0), Image.new("L", (W, W), 0), sh.split()[3].point(lambda v: v * 70 // 255)))
        sh = ImageChops.offset(sh, 0, 3 * SS)
        im = Image.alpha_composite(im, sh)
        im = Image.alpha_composite(im, glyph_layer)
        # keep the squircle's alpha
        a = ImageChops.multiply(im.split()[3], m)
        im.putalpha(a)
        im = im.resize((N, N), Image.LANCZOS)
        im.save(os.path.join(ICONS, "own", name + ".png"))
        bg = Image.new("RGB", im.size, (0, 0, 0))
        bg.paste(im, mask=im.split()[3])
        bg.save(os.path.join(ICONS, "bmp", name + ".bmp"))
        im.split()[3].save(os.path.join(ICONS, "bmp", name + "_mask_soft.bmp"))
        print(name)


if __name__ == "__main__":
    main()
