"""Zoroark: dark violet fur, the crimson mane tipped teal, a halftone purple sky and a sly grin."""

from base import circle, path, rect
from themes._kit import Kit

VIOLET = "#8a2ae8"
SKY = "#5a2ab0"
FUR = "#2e2448"
FUR_DK = "#1c1630"
MANE = "#c8285a"
MANE_DK = "#8a1840"
TEAL = "#2ab8c8"
CLOUD = "#7ac8f8"
GRIN = "#f4f0f8"


def mane(x, y, k, fill=MANE, tip=TEAL):
    """Zoroark's swept-back mane with a teal tip."""
    d = (f"M{x},{y + 10 * k} C{x + 10 * k},{y + 2 * k} {x + 24 * k},{y} {x + 38 * k},{y + 4 * k} "
         f"C{x + 26 * k},{y + 6 * k} {x + 16 * k},{y + 9 * k} {x + 8 * k},{y + 14 * k} Z")
    return path(d, fill=fill) + circle(x + 36 * k, y + 4.5 * k, 2.6 * k, tip)


def halftone(w, h, colour):
    b = ""
    for j, y in enumerate(range(2, h, 6)):
        for x in range(2 + (3 if j % 2 else 0), w, 6):
            b += circle(x, y, 0.4 + 1.2 * (y / h), colour)
    return b


class Zoroark(Kit):
    NAME = "Zoroark"
    WALLPAPER = "22/wp3631684-zoroark-hd-wallpapers.jpg"
    WALLPAPER_MODE = "crop"
    BG_SOLID = SKY

    TITLE = ("#3e2e64", FUR_DK)
    TITLE_DIM = ("#2a2638", "#201c2c")
    TITLE_HI = "#5a4488"
    BAND, BAND2, BAND_DIM, OUTER = MANE, TEAL, "#34303e", "#0e0a18"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = FUR_DK, MANE, "#201c2c", "#34303e"
    BG, BG_DK, MENU_BG, LINE = "#221a38", "#160f28", FUR_DK, "#3e3060"
    ACCENT, ACCENT_HI, ACCENT_FG = MANE, "#f04a7a", "#ffffff"
    SEL, SEL_EDGE = (MANE_DK, VIOLET), TEAL
    POPUP_BG, POPUP_EDGE = FUR, TEAL
    POPUP_RADIUS = 8
    BTN = dict(inactive=("#2a2638", "#4a4458", "#8a84a0"), active=(FUR_DK, MANE, GRIN),
               hover=(TEAL, "#ffffff", FUR_DK), close_hover=(MANE, "#ffffff", "#ffffff"),
               clicked=(VIOLET, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 24
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans Black 9")
    TEXT = dict(title_active=GRIN, title_inactive="#8a84a0", menu_title=GRIN,
                menu="#e4dcf4", menu_hilite="#ffffff", dialog="#e4dcf4", tooltip=GRIN)
    CURSOR = (GRIN, MANE_DK)

    def ornament(self, active):
        return mane(4, 3, 1.05, MANE if active else "#4a3a48", TEAL if active else "#4a5a64")

    def emblem_art(self, cx, cy, state):
        """Zoroark's grin and eye."""
        if state == "inactive":
            return circle(cx, cy, 7, "#2a2638", "#5a5470", 1)
        b = circle(cx, cy, 9, TEAL, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        b += circle(cx, cy, 7.5, FUR, MANE, 1.2)
        b += path(f"M{cx - 5},{cy + 1} Q{cx},{cy + 6} {cx + 5},{cy + 1} Z", fill=GRIN)
        b += path(f"M{cx - 4},{cy - 3} L{cx - 0.5},{cy - 2} L{cx - 4},{cy - 1.2} Z", fill=TEAL)
        return b

    def corner_mark(self, x, y, active, which):
        return circle(x, y, 2, TEAL) if active else ""

    def check_mark(self, s, hover):
        return mane(1.5, 3, 0.32, MANE, TEAL)

    def radio_mark(self, s, hover):
        return circle(s / 2, s / 2, s / 2 - 3, TEAL)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, [TEAL, CLOUD, MANE, TEAL][i - 1])

    def menu_tile(self, w, h):
        return rect(0, 0, w, h, FUR_DK) + halftone(w, h, "#2e2650")


    # ---- shape: its crimson mane sweeping back over the top of the window ----

    SHAPE = dict(top=32)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def hair(active):
            m, md, t = (MANE, MANE_DK, TEAL) if active else ("#4a3a48", "#3a2e3a", "#4a5a64")
            # Zoroark's mane: three thick locks rising from the title bar and
            # sweeping back to the right, each ending in a teal bead
            b = ""
            for x0, w, tip, col in ((4, 16, (60, 4), md), (12, 18, (78, 10), m), (2, 14, (44, 14), m)):
                tx, ty = tip
                d = (f"M{x0},{T + 3} C{x0 - 2},{T - 18} {tx - 34},{ty - 6} {tx},{ty} "
                     f"C{tx - 8},{ty + 16} {x0 + w + 14},{T - 2} {x0 + w},{T + 3} Z")
                b += path(d, fill=col, stroke=FUR_DK, sw=1.2)
                b += circle(tx - 1, ty + 1, 3.4, t, FUR_DK, 0.8)
            return svg(84, T + 3, b)

        return [("mane", 84, T + 3, "tl", 0, 0, hair)]
