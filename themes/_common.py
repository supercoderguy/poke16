"""Small drawing helpers shared by the later themes (the first six predate this)."""

import math

from base import circle, path, rect


def title_grad(TH, dy, stops, gid="tb"):
    """Vertical title gradient in title-bar coordinates, so a slice drawn dy px
    down the bar (buttons, emblem) lines up with the bar itself."""
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" '
            f'x2="0" y2="{TH - dy}">{s}</linearGradient>')


def frame_side(w, h, which, fill, outer, inner, inner_w=1):
    """Left/right border strip: outer edge line, fill, inner accent line."""
    b = rect(0, 0, w, h, fill)
    if which == "left":
        b += rect(0, 0, 1, h, outer) + rect(w - inner_w, 0, inner_w, h, inner)
    else:
        b += rect(w - 1, 0, 1, h, outer) + rect(0, 0, inner_w, h, inner)
    return b


def frame_bottom(w, h, fill, outer, inner, inner_w=1):
    return rect(0, 0, w, h, fill) + rect(0, 0, w, inner_w, inner) + rect(0, h - 1, w, 1, outer)


def frame_corner(w, h, which, fill, outer, inner, side_w, inner_w=1):
    """Bottom corner: the inner accent turns from the side border into the bottom."""
    b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, outer)
    if which == "left":
        b += rect(0, 0, 1, h, outer) + rect(side_w - inner_w, 0, w - side_w + inner_w, inner_w, inner)
    else:
        b += rect(w - 1, 0, 1, h, outer) + rect(0, 0, w - side_w + inner_w, inner_w, inner)
    return b


def tri_arrow(s, direction, bg, fill, stroke=None):
    c = s / 2
    d = {"up": f"M3,{s-4} L{c},4 L{s-3},{s-4}Z", "down": f"M3,4 L{c},{s-4} L{s-3},4Z",
         "left": f"M{s-4},3 L4,{c} L{s-4},{s-3}Z", "right": f"M4,3 L{s-4},{c} L4,{s-3}Z"}[direction]
    return rect(0, 0, s, s, bg) + path(d, fill=fill, stroke=stroke, sw=0.8)


def glyph(kind, s, colour, sw=2, m=5.5):
    """Standard close / maximise / iconify marks."""
    c = s / 2
    return {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=colour, sw=sw),
            "max": rect(m, m, s - 2 * m, s - 2 * m, "none", colour, sw * 0.85, rx=1.2),
            "iconify": path(f"M{m},{c + 2.5} L{s-m},{c + 2.5}", stroke=colour, sw=sw)}[kind]


def burst(cx, cy, r, n, inner, fill, rot=-90):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180 / n)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return path("M" + " L".join(pts) + "Z", fill=fill)


def crescent(cx, cy, r, fill, thick=0.55, rot=0):
    """Crescent opening to the right (rot rotates it around the centre)."""
    d = (f"M{cx},{cy - r} A{r},{r} 0 1 0 {cx},{cy + r} "
         f"A{r * thick},{r} 0 1 1 {cx},{cy - r} Z")
    return f'<g transform="rotate({rot} {cx} {cy})">' + path(d, fill=fill) + "</g>"


def starfield(w, h, seed, n, colours, rmax=0.9):
    """Deterministic scatter of tiny stars (for tiled menu backgrounds)."""
    import random
    rnd = random.Random(seed)
    b = ""
    for _ in range(n):
        b += circle(round(rnd.uniform(0, w), 1), round(rnd.uniform(0, h), 1),
                    round(rnd.uniform(0.3, rmax), 2), rnd.choice(colours))
    return b


def diamond(cx, cy, rx, ry, fill, stroke=None, sw=1):
    return path(f"M{cx},{cy - ry} L{cx + rx},{cy} L{cx},{cy + ry} L{cx - rx},{cy} Z", fill=fill, stroke=stroke, sw=sw)
