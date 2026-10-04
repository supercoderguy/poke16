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


def plump_ear(b1, b2, tip, uid, fill="#ffe200", tipc="#221e07", edge="#221e07", tip_len=0.4, bulge=0.28,
              sw=1.4, band=None, band_at=0.55, band_w=3):
    """A rounded, leaf-shaped ear from base b1..b2 to tip, coloured `tipc` near the
    tip; `band` adds a ring of that colour across the ear (Umbreon's gold rings)."""
    import math
    (x1, y1), (x2, y2), (tx, ty) = b1, b2, tip

    def ctrl(ax, ay, t, side):
        # a point t of the way from (ax, ay) to the tip, pushed outward by `bulge`
        dx, dy = tx - ax, ty - ay
        n = math.hypot(dx, dy)
        return ax + dx * t + side * -dy / n * n * bulge, ay + dy * t + side * dx / n * n * bulge

    side1 = 1 if (x2 - x1) * (ty - y1) - (y2 - y1) * (tx - x1) > 0 else -1
    a1, a2 = ctrl(x1, y1, 0.35, side1), ctrl(x1, y1, 0.8, side1 * 0.4)
    c1, c2 = ctrl(x2, y2, 0.8, -side1 * 0.4), ctrl(x2, y2, 0.35, -side1)
    d = (f"M{x1},{y1} C{a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f} {tx},{ty} "
         f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2},{y2} Z")
    r = math.hypot(tx - (x1 + x2) / 2, ty - (y1 + y2) / 2) * tip_len
    out = (f'<clipPath id="tip{uid}"><path d="{d}"/></clipPath>' + path(d, fill=fill)
           + f'<circle cx="{tx}" cy="{ty}" r="{r:.1f}" fill="{tipc}" clip-path="url(#tip{uid})"/>')
    if band:
        rb = math.hypot(tx - (x1 + x2) / 2, ty - (y1 + y2) / 2) * band_at
        out += (f'<circle cx="{tx}" cy="{ty}" r="{rb:.1f}" fill="none" stroke="{band}" '
                f'stroke-width="{band_w}" clip-path="url(#tip{uid})"/>')
    return out + path(d, stroke=edge, sw=sw)


def mute(colour, toward="#6a6a6a", t=0.6):
    """A colour faded towards a grey: decorations on unfocused windows."""
    a = [int(colour.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(toward.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def mirror(w, body):
    """Flip a w-wide drawing left-to-right (a left-side decoration for the right side)."""
    return f'<g transform="translate({w},0) scale(-1,1)">{body}</g>'
