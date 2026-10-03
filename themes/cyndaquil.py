"""Cyndaquil: a red-orange sunset, the back flames, navy fur and a cream belly."""

from base import circle, path, rect
from themes._kit import Kit

RED = "#e83a18"
RED_DK = "#9f181b"
ORANGE = "#f99a14"
SUN = "#ffd84a"
FLAME = "#ffe85a"
NAVY = "#1e2a44"
NAVY_DK = "#121a2c"
CREAM = "#f4d8a0"
EMBER = "#2a1410"


def flames(x, y, k, outer=RED, inner=FLAME):
    """Cyndaquil's back flames: three licking tongues."""
    def tongue(dx, h):
        return (f"M{x + dx * k},{y + 12 * k} C{x + (dx - 3) * k},{y + (12 - h * .5) * k} {x + (dx - 1) * k},{y + (12 - h) * k} "
                f"{x + (dx + 1) * k},{y + (12 - h - 2) * k} C{x + (dx + 2) * k},{y + (12 - h) * k} {x + (dx + 5) * k},{y + (12 - h * .4) * k} {x + (dx + 4) * k},{y + 12 * k} Z")
    b = "".join(path(tongue(dx, h), fill=outer) for dx, h in ((0, 7), (6, 10), (12, 8)))
    return b + "".join(path(tongue(dx + 1, h * 0.55), fill=inner) for dx, h in ((0, 7), (6, 10), (12, 8)))


class Cyndaquil(Kit):
    NAME = "Cyndaquil"
    WALLPAPER = "17/wallhaven-x897qz.jpg"
    BG_SOLID = RED

    TITLE = (NAVY, NAVY_DK)
    TITLE_DIM = ("#2a2a34", "#1e1e26")
    TITLE_HI = "#3a4a6a"
    BAND, BAND2, BAND_DIM, OUTER = ORANGE, RED, "#3a3030", "#0a0a12"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = NAVY_DK, ORANGE, "#1e1e26", "#3a3030"
    BG, BG_DK, MENU_BG, LINE = "#241612", "#180e0a", EMBER, "#5a2a1a"
    ACCENT, ACCENT_HI, ACCENT_FG = ORANGE, SUN, "#2a1208"
    SEL, SEL_EDGE = (RED, ORANGE), FLAME
    POPUP_BG, POPUP_EDGE = CREAM, RED_DK
    BTN = dict(inactive=("#26262e", "#4a4a54", "#8a8a94"), active=(CREAM, ORANGE, NAVY),
               hover=(SUN, "#ffffff", NAVY), close_hover=(RED, "#ffffff", "#ffffff"),
               clicked=(ORANGE, "#ffffff", NAVY))
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans ExtraBold 9")
    TEXT = dict(title_active=CREAM, title_inactive="#8a8a94", menu_title=CREAM,
                menu="#f4dcc0", menu_hilite="#ffffff", dialog="#f4dcc0", tooltip=EMBER)
    CURSOR = (CREAM, NAVY)

    def ornament(self, active):
        return flames(6, 3, 1.4, RED if active else "#4a3a3a", FLAME if active else "#6a5a4a")

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return circle(cx, cy, 7, "#3a3434", "#5a5050", 1)
        b = circle(cx, cy, 10, SUN, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        # the setting sun with wavy heat lines
        b += circle(cx, cy, 7.5, ORANGE) + circle(cx, cy, 5, SUN)
        return b + path(f"M{cx - 9},{cy + 4} Q{cx - 6},{cy + 2} {cx - 3},{cy + 4} T{cx + 3},{cy + 4} T{cx + 9},{cy + 4}",
                         stroke=FLAME, sw=1.2)

    def corner_mark(self, x, y, active, which):
        return flames(x - 4, y - 5, 0.45, RED, FLAME) if active else ""

    def check_mark(self, s, hover):
        return flames(1.5, 1, 0.6, RED, FLAME)

    def radio_mark(self, s, hover):
        return circle(s / 2, s / 2, s / 2 - 3, ORANGE) + circle(s / 2, s / 2, s / 2 - 5, SUN)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, [FLAME, ORANGE, RED, SUN][i - 1])
