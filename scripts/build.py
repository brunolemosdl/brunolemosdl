#!/usr/bin/env python3
"""Draw the SVG images of this profile: the banner and the project cards.

    python3 scripts/build.py

Palette of the Forja design (deep purple surfaces, violet, magenta, ember orange). The
images use system fonts only: GitHub serves SVGs as images, so web fonts do not load.
"""

import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
BG, CARD, BORDER = "#120a1a", "#1d1228", "#3a2a4d"
VIOLET, GLOW, EMBER, EMBER2, SPARK = "#9b3df0", "#e84fc0", "#fb8e31", "#e95904", "#ffd28a"
FG, MUTED = "#ffffff", "#b3a8c2"


def hexagon(cx, cy, r, rot=30):
    return " ".join(f"{cx + r * math.cos(math.radians(a + rot)):.1f},{cy + r * math.sin(math.radians(a + rot)):.1f}"
                    for a in range(0, 360, 60))


def sparks(n, w, h, seed, x0=0):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = x0 + rnd.uniform(0, w), rnd.uniform(h * 0.55, h)
        s, dur, delay = rnd.uniform(2, 5), rnd.uniform(4, 9), rnd.uniform(0, 8)
        color = rnd.choice([EMBER, SPARK, GLOW, EMBER])
        out.append(
            f'<polygon points="{x:.0f},{y - s:.0f} {x + s:.0f},{y:.0f} {x:.0f},{y + s:.0f} {x - s:.0f},{y:.0f}" fill="{color}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{rnd.uniform(-30, 30):.0f} -{h * 0.7:.0f}" '
            f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/></polygon>')
    return "\n".join(out)


def banner():
    w, h = 1200, 320
    grid = []
    for row in range(-1, 8):
        for col in range(-1, 26):
            cx = col * 52 + (26 if row % 2 else 0)
            cy = row * 45
            grid.append(f'<polygon points="{hexagon(cx, cy, 28)}" fill="none" stroke="{VIOLET}" stroke-opacity="0.07"/>')
    core = (
        f'<g transform="translate(985 160)">'
        f'<polygon points="{hexagon(0, 0, 92)}" fill="none" stroke="{GLOW}" stroke-opacity="0.45" stroke-width="3">'
        f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="60s" repeatCount="indefinite"/></polygon>'
        f'<polygon points="{hexagon(0, 0, 66)}" fill="#1b1e24"/>'
        f'<polygon points="{hexagon(0, 0, 54)}" fill="{EMBER2}"/>'
        f'<polygon points="{hexagon(0, 0, 42)}" fill="{EMBER}">'
        f'<animate attributeName="opacity" values="1;0.75;1" dur="3s" repeatCount="indefinite"/></polygon>'
        f'<path d="M0 -28 C20 -6 23 12 15 24 C10 32 -12 32 -16 24 C-22 12 -13 0 -6 -6 C-4 3 1 8 4 6 C6 -4 3 -16 0 -28Z" fill="#1b1e24"/>'
        f'</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Bruno Lemos de Lima">
<defs>
<radialGradient id="g1" cx="20%" cy="0%" r="70%"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="82%" cy="50%" r="35%"><stop offset="0" stop-color="{EMBER}" stop-opacity=".25"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{FG}"/><stop offset="1" stop-color="#e9d5ff"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="url(#g1)"/>
<rect width="{w}" height="{h}" fill="url(#g2)"/>
{"".join(grid)}
{sparks(28, w, h, 7)}
{core}
<text x="64" y="128" font-family="{FONT}" font-size="58" font-weight="700" fill="url(#t)" letter-spacing="-1">Bruno Lemos de Lima</text>
<text x="66" y="176" font-family="{FONT}" font-size="24" fill="{MUTED}">Software Engineer · Game AI &amp; reinforcement learning researcher</text>
<g font-family="{FONT}" font-size="17" font-weight="600">
<rect x="64" y="212" width="196" height="36" rx="18" fill="{VIOLET}" fill-opacity=".18" stroke="{VIOLET}" stroke-opacity=".5"/>
<text x="162" y="236" text-anchor="middle" fill="#d8b4fe">MSc · UFMG</text>
<rect x="274" y="212" width="236" height="36" rx="18" fill="{EMBER}" fill-opacity=".14" stroke="{EMBER}" stroke-opacity=".5"/>
<text x="392" y="236" text-anchor="middle" fill="{EMBER}">Engineer · Nextpower</text>
<rect x="524" y="212" width="246" height="36" rx="18" fill="{GLOW}" fill-opacity=".14" stroke="{GLOW}" stroke-opacity=".5"/>
<text x="647" y="236" text-anchor="middle" fill="{GLOW}">Founder · Tenebris Forge</text>
</g>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="{BORDER}"/>
</svg>'''


def wrap(text, width):
    words, lines, line = text.split(), [], ""
    for w in words:
        if len(line) + len(w) + 1 > width:
            lines.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    return lines + [line]


def inline_mark(path, cx, cy, size):
    """Another SVG's drawing scaled into a card, its defs kept (ids are unique per mark)."""
    import re
    src = (OUT / path).read_text()
    defs = re.search(r"<defs>(.*?)</defs>", src, re.S)
    body = src.split("</defs>", 1)[1] if defs else re.sub(r"^<svg[^>]*>|<title.*?</title>", "", src)
    body = body.rsplit("</svg>", 1)[0]
    s = size / 256
    return (f'<defs>{defs.group(1)}</defs>' if defs else "") + \
        f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({s:.4f})">{body}</g>'


def card(title, badge, color, text, tags, mark=None):
    w, h = 560, 200
    body = "".join(f'<text x="28" y="{96 + i * 22}" font-family="{FONT}" font-size="15" fill="{MUTED}">{escape(l)}</text>'
                   for i, l in enumerate(wrap(text, 64)[:3]))
    x, chips = 28, []
    for t in tags:
        tw = 14 + len(t) * 8
        chips.append(f'<rect x="{x}" y="{h - 46}" width="{tw}" height="24" rx="12" fill="{color}" fill-opacity=".14"/>'
                     f'<text x="{x + tw / 2}" y="{h - 29}" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="{color}">{escape(t)}</text>')
        x += tw + 8
    bw = 18 + len(badge) * 8.5
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)}">
<defs><radialGradient id="g" cx="100%" cy="0%" r="80%"><stop offset="0" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#g)"/>
{inline_mark(mark, 44, 46, 44) if mark else f'<polygon points="{hexagon(42, 46, 16)}" fill="{color}" fill-opacity=".2" stroke="{color}" stroke-width="2"/>'}
<text x="70" y="53" font-family="{FONT}" font-size="22" font-weight="700" fill="{FG}">{escape(title)}</text>
<rect x="{w - 28 - bw}" y="30" width="{bw}" height="26" rx="13" fill="{color}" fill-opacity=".18" stroke="{color}" stroke-opacity=".6"/>
<text x="{w - 28 - bw / 2}" y="48" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="{color}">{escape(badge)}</text>
{body}
{"".join(chips)}
</svg>'''


CARDS = {
    "card-intent-pcgrl-demo": ("Text to level with RL", "AIIDE 2026", EMBER,
                               "Ask for a platformer level in plain English, watch a reinforcement learning policy build it, then play it in the browser.",
                               ["LLM", "PCGRL", "Python", "Web"]),
    "card-quadruped-rl-genesis": ("Quadruped RL in Genesis", "CROS 2026", GLOW,
                                  "PPO, SAC and TD3 compared on a Unitree Go2 over flat, irregular and rough procedural terrain in the Genesis simulator.",
                                  ["Deep RL", "Robotics", "Genesis", "SB3"]),
    "card-research-gaps": ("Research gap detection", "WESAAC 2026", VIOLET,
                           "A multi-agent system that detects research gaps in scientific literature and ranks them by priority.",
                           ["Multi-agent", "LLM", "Python", "Web"]),
    "card-tenebris-forge": ("Tenebris Forge", "Studio", GLOW,
                            "An independent studio crafting horror experiences: online games, web apps and tools forged in darkness.",
                            ["Games", "Web", "Next.js"], "tenebris-forge-mark.svg"),
}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    for name, args in CARDS.items():
        (OUT / f"{name}.svg").write_text(card(*args))
    print("assets written:", sorted(p.name for p in OUT.glob("*.svg")))
