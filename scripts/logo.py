#!/usr/bin/env python3
"""Build every file of the personal logo of Bruno Lemos, "the ember core": the heart of the profile
banner made a mark. A magenta hexagonal ring open at the upper right, a dark hexagon, an
ember hexagon with the flame cut into it and a lit core, three sparks escaping through the
opening. Same finish as the Tenebris Forge mark (dark outlines, two-tone ring).

    python3 scripts/logo.py

Writes, in brand/: mark.svg, mark-small.svg (16-48 px), mark-black.svg, mark-white.svg,
mark-mono.svg, avatar.svg, app-icon.svg, lockup-horizontal.svg, lockup-stacked.svg.
The name is outlined Geist 800 (scripts/wordmark.py writes brand/wordmark.json).
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand"
INK, VOID = "#1b1e24", "#120a1a"
RING, BEVEL = "#b8328f", "#f07ad2"
RIM, EMBER_HI, EMBER, EMBER_LO = "#e95904", "#ffc66e", "#fb8e31", "#e95904"
CORE = "#e84fc0"
SPARKS = [((160, 24, 5), "#ffd28a", 5), ((178, 42, 9), "#fb8e31", 6), ((199, 62, 6), "#e84fc0", 5)]
WORDMARK = json.loads((OUT / "wordmark.json").read_text())


def hexagon(r, cx=128, cy=128):
    return [(cx + r * math.cos(math.radians(a - 90)), cy + r * math.sin(math.radians(a - 90))) for a in range(0, 360, 60)]


def sub(points):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points) + " Z"


def open_ring(r_out, r_in):
    """The ring without its upper right side, in one piece (no seams at the corners)."""
    o, i, order = hexagon(r_out), hexagon(r_in), [1, 2, 3, 4, 5, 0]
    return sub([o[k] for k in order] + [i[k] for k in reversed(order)])


def flame(cx, top, bottom, w):
    h = bottom - top
    return (f"M{cx} {top} C{cx + w * .55} {top + h * .25} {cx + w} {top + h * .45} {cx + w * .95} {top + h * .7} "
            f"C{cx + w * .9} {top + h * .9} {cx + w * .45} {bottom} {cx} {bottom} "
            f"C{cx - w * .45} {bottom} {cx - w * .9} {top + h * .9} {cx - w * .95} {top + h * .7} "
            f"C{cx - w} {top + h * .5} {cx - w * .55} {top + h * .38} {cx - w * .2} {top + h * .25} "
            f"C{cx - w * .05} {top + h * .42} {cx + w * .1} {top + h * .45} {cx + w * .2} {top + h * .42} "
            f"C{cx + w * .25} {top + h * .28} {cx + w * .1} {top + h * .12} {cx} {top} Z")


def diamond(x, y, r):
    return f"M{x} {y - r} L{x + r} {y} L{x} {y + r} L{x - r} {y} Z"


def ink(w):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" paint-order="stroke"'


GRADIENT = ('<linearGradient id="bl-ember" gradientUnits="userSpaceOnUse" x1="0" y1="62" x2="0" y2="194">'
            f'<stop offset="0" stop-color="{EMBER_HI}"/><stop offset=".55" stop-color="{EMBER}"/>'
            f'<stop offset="1" stop-color="{EMBER_LO}"/></linearGradient>')
FLAME = flame(128, 82, 178, 30)


def colour(small=False):
    parts = [f'<path fill="{RING}" {ink(14 if small else 10)} d="{open_ring(116, 94)}"/>']
    if not small:
        parts.append(f'<path fill="{BEVEL}" d="{open_ring(103, 94)}"/>')
    parts += [f'<path fill="{INK}" d="{sub(hexagon(90))}"/>',
              f'<path fill="{RIM}" d="{sub(hexagon(76))}"/>',
              f'<path fill="url(#bl-ember)" d="{sub(hexagon(64))}"/>',
              f'<path fill="{INK}" d="{FLAME if not small else flame(128, 78, 182, 34)}"/>']
    if not small:
        parts.append(f'<path fill="{CORE}" d="{flame(128, 128, 170, 13)}"/>')
        parts += [f'<path fill="{c}" {ink(s)} d="{diamond(*xyr)}"/>' for xyr, c, s in SPARKS]
    return "".join(parts)


def mono(color):
    """One colour: the open ring, the hexagon with the flame cut out, the sparks."""
    return (f'<g fill="{color}"><path d="{open_ring(116, 94)}"/>'
            f'<path fill-rule="evenodd" d="{sub(hexagon(84))} {FLAME}"/>'
            + "".join(f'<path d="{diamond(*xyr)}"/>' for xyr, _, _ in SPARKS) + "</g>")


def svg(w, h, body, title="Bruno Lemos"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')


def name(x, baseline, size, anchor="start", color="#ffffff"):
    """The outlined name; returns the paths and the total width."""
    w, s, space = WORDMARK["words"], size / WORDMARK["em"], WORDMARK["space"]
    order = ["Bruno", "Lemos"]
    total = (sum(w[k]["width"] for k in order) + space * (len(order) - 1)) * s
    x0 = x - total / 2 if anchor == "middle" else x
    out, cur = [], x0
    for k in order:
        out.append(f'<path fill="{color}" transform="translate({cur:.1f} {baseline}) scale({s:.4f})" d="{w[k]["d"]}"/>')
        cur += (w[k]["width"] + space) * s
    return "".join(out), total


if __name__ == "__main__":
    defs = f"<defs>{GRADIENT}</defs>"
    h_name, h_w = name(282, 162, 96)
    s_name, s_w = name(0, 0, 66)
    stacked_w = max(560, int(s_w) + 40)
    s_name, _ = name(stacked_w / 2, 356, 66, "middle")
    files = {
        "mark.svg": svg(256, 256, defs + colour()),
        "mark-small.svg": svg(256, 256, defs + colour(small=True), "Bruno Lemos, small sizes"),
        "mark-black.svg": svg(256, 256, mono("#111111")),
        "mark-white.svg": svg(256, 256, mono("#ffffff")),
        "mark-mono.svg": svg(256, 256, mono(CORE)),
        "avatar.svg": svg(512, 512, f'<defs>{GRADIENT}<radialGradient id="g" cx="50%" cy="42%" r="60%">'
                                    f'<stop offset="0" stop-color="#4a1440"/><stop offset="1" stop-color="{VOID}"/></radialGradient></defs>'
                                    f'<rect width="512" height="512" fill="url(#g)"/><g transform="translate(36 36) scale(1.72)">{colour()}</g>'),
        "app-icon.svg": svg(512, 512, f'{defs}<rect width="512" height="512" fill="{VOID}"/>'
                                      f'<g transform="translate(96 96) scale(1.25)">{colour(small=True)}</g>'),
        "lockup-horizontal.svg": svg(int(282 + h_w + 24), 256, defs + colour() + h_name),
        "lockup-stacked.svg": svg(stacked_w, 400, defs + f'<g transform="translate({stacked_w / 2 - 128:.0f} 0)">{colour()}</g>' + s_name),
    }
    for f, s in files.items():
        (OUT / f).write_text(s)
    print("brand/:", " ".join(files))
