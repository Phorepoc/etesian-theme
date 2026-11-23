# Etesian theme

The Etesian design language (the N9's look, re-envisioned) as a standard S60 theme for Symbian^3 and Phorepoc OS: dark colours, its own
application icons and the Fira Sans typeface.

- `skin/` two skins: `etesian.txt` = "Etesian", the Hybrid colour mode (the default: light content, dark chrome; UID E7016B33, made by `tools/gen_hybrid.py`) and `etesian-dark.txt` = "Etesian Dark" (UID E7016B31), the backgrounds, `icons/` the 37 application icons (22 bitmap icons from the n9ish pack by speactra, N9-like icons by hpluslabels, GPL-3.0, `icons/n9ish/` and `icons/bmp/`; the other 15 our own drawings in the same style, `icons/own/`; see NOTICE)
  (SVG, `mapping.txt` = application UID to icon).
- `fonts/` Fira Sans Light, Regular and Bold, unmodified, with the SIL OFL.
- `tools/build_skin.py` compiles the skin with the pdk toolchain (`akn_skin_desc_compiler`, `mifconv`) into `.skn`, `.mif` and `.mbm`.
  `gen_descriptor.py`, `gen_frames.py` and `gen_n9_style_icons.py` are the maintainer tools that write the descriptor, the frames and the own icons.

## Where it is used

- **Built into the Phorepoc OS images** (PC, phone): the pdk compiles the skin into the ROM, with the fonts in `Z:\resource\fonts`; the theme
  is then selectable in Themes next to the stock ones. Nothing to install.
- **A SIS for other phones** (`etesian-theme-arm.sis`, from the release page and Catalogue): the compiled skin only, no fonts and no shell.
  Pick Etesian in Themes. Early; tested on Phorepoc images only so far.
- **The Etesian shell** ([etesian-ui](https://github.com/Phorepoc/etesian-ui)) activates this theme when you choose the shell and puts the
  previous theme back when you switch away.

## Licences

AGPL-3.0-only (`LICENSE`), with the additional terms of `ADDITIONAL-TERMS.md`: the theme is derived from the
[Etesian Design Language](https://github.com/Etesian-design/design) (its tokens, colours and icon glyphs), and carries the
same terms as the upstream: the section 7(b) attribution "Etesian, founded by Kyriakos Bompotis", which must stay in the
`NOTICE` and wherever a derived work shows its legal notices; section 7(e), the Etesian names and logos (`TRADEMARKS.md`);
and the Phorepoc exception, under which the Phorepoc images and packages use it. Anyone else uses it under the AGPL.

Fira Sans (`fonts/`) is SIL OFL 1.1, unmodified (`LICENSES/OFL-1.1.txt`). The skin descriptor follows the layout of the
Symbian skin format (EPL-1.0); no artwork from the 2010 release is used. The SIS and the images install `LICENSES/` and
`NOTICE` in `\resource\etesian\licences\`.

## History

First commit of this repository: the skin, icons, fonts and tools of etesian-ui at its commit 25a4c01 (etesian-ui keeps the shell).
