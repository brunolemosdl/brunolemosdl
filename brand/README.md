# Bruno Lemos logo

**The ember core**: the heart of the profile banner made into a mark. A magenta hexagonal
ring left open at the upper right, a dark hexagon, an ember with a flame cut into it and a
lit core, and three sparks escaping through the opening. It shares its finish with the
Tenebris Forge mark (dark outlines, two-tone ring, ember gradient), so the person and the
studio read as one family; magenta is his colour, violet is the studio's. Approved on
2026-11-25.

## Files

| File | Use |
|---|---|
| `mark.svg`, `mark.png` | Full colour on transparent: anything from 64 px up |
| `mark-small.svg`, `favicon-16/32/48.png` | 16 to 48 px: no sparks, bevel or core, heavier lines |
| `mark-black.svg`, `mark-white.svg`, `mark-mono.svg` | One colour: print, light or dark single-colour backgrounds |
| `avatar.svg`, `avatar.png` | Square on the dark background |
| `app-icon.svg`, `app-icon-180/192/512.png` | Site and app icons; the mark sits inside the maskable safe zone |
| `lockup-horizontal.svg/.png`, `lockup-stacked.svg/.png` | Mark with the name "Bruno Lemos" |

Everything is drawn by [`scripts/logo.py`](../scripts/logo.py) on a 256 grid; change the
geometry there. PNGs come from the SVGs with resvg.

## Name

"Bruno Lemos" in **Geist ExtraBold (800)**, white on dark (ink on light), outlined by
[`scripts/wordmark.py`](../scripts/wordmark.py) from the font in `fonts/` (SIL Open Font
Licence, `fonts/LICENSE`). The full name is not used in the logo.

## Colours

| Role | HEX |
|---|---|
| Ring | `#b8328f`, bevel `#f07ad2` |
| Ember | rim `#e95904`; `#ffc66e` to `#fb8e31` to `#e95904` |
| Flame core | `#e84fc0` |
| Ink (outlines, hexagon, flame) | `#1b1e24` |
| Background | `#120a1a` |
| Sparks | `#ffd28a`, `#fb8e31`, `#e84fc0` |

One-colour version: `#e84fc0`, or black or white.

## Rules

- **Clear space**: the ring's thickness (22 units of 256, about 9 % of the width) on every side.
- **Minimum size**: full mark 64 px; below that `mark-small`. Horizontal lockup at least 160 px wide.
- **Backgrounds**: the colour mark on `#120a1a` or a dark, quiet background; on light ones use
  `mark-black` or the `avatar` tile.
- **Do not**: recolour parts, close the ring's opening, move the sparks, stretch, rotate, or add
  shadows and glows.
