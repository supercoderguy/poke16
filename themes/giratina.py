"""Giratina: the Distortion World - rust-red cavern, Giratina's black/red striped wings,
gold crown and spikes, the Origin trio of Palkia pink and Dialga steel blue."""

from base import circle, path, rect
from themes._kit import Kit

CAVE = "#4c1616"
CAVE_DK = "#2a0c10"
SHADOW = "#1c1418"
GOLD = "#e0b840"
GOLD_DK = "#9a7a20"
STRIPE = "#c02838"
PALKIA = "#e8a8c0"
DIALGA = "#5a7ab8"
GREY = "#4a4048"


def crown(cx, cy, k, fill=GOLD, edge=SHADOW):
    """Giratina's gold head crest: three upswept horns."""
    d = (f"M{cx - 7 * k},{cy + 4 * k} L{cx - 8 * k},{cy - 5 * k} L{cx - 3 * k},{cy} L{cx},{cy - 8 * k} "
         f"L{cx + 3 * k},{cy} L{cx + 8 * k},{cy - 5 * k} L{cx + 7 * k},{cy + 4 * k} Z")
    return path(d, fill=fill, stroke=edge, sw=0.8)


def ribs(x, y, active):
    """The striped wing: black bands edged in red."""
    b = ""
    for i in range(4):
        c = STRIPE if active else "#4a3036"
        b += path(f"M{x + i * 9},{y + 14} L{x + i * 9 + 6},{y + 2} L{x + i * 9 + 9},{y + 4} L{x + i * 9 + 4},{y + 15} Z",
                  fill=SHADOW, stroke=c, sw=1)
    return b


class Giratina(Kit):
    NAME = "Giratina"
    WALLPAPER = "21/wp2817465-giratina-hd-wallpaper.jpg"
    WALLPAPER_MODE = "crop"
    BG_SOLID = CAVE_DK

    TITLE = ("#5a2024", CAVE_DK)
    TITLE_DIM = ("#2e2428", "#221c20")
    TITLE_HI = "#7a3036"
    BAND, BAND2, BAND_DIM, OUTER = GOLD, STRIPE, "#3a2e30", "#120808"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = SHADOW, GOLD_DK, "#221c20", "#3a2e30"
    BG, BG_DK, MENU_BG, LINE = "#241418", "#170c10", "#1c1014", "#4a2a2e"
    ACCENT, ACCENT_HI, ACCENT_FG = GOLD, "#f8d870", SHADOW
    SEL, SEL_EDGE = (STRIPE, "#7a1c28"), GOLD
    POPUP_BG, POPUP_EDGE = "#2a1c22", GOLD
    BTN = dict(inactive=("#2a2226", "#4a3a40", "#8a7a80"), active=(SHADOW, GOLD, GOLD),
               hover=(PALKIA, "#ffffff", SHADOW), close_hover=(STRIPE, "#ffffff", "#ffffff"),
               clicked=(DIALGA, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 24
    FONTS = dict(Kit.FONTS, border="pango:DejaVu Serif Bold 9")
    TEXT = dict(title_active="#f4e4c8", title_inactive="#8a7a80", menu_title="#f4e4c8",
                menu="#e8d8d0", menu_hilite="#ffffff", dialog="#e8d8d0", tooltip="#f4e4c8")
    CURSOR = (GOLD, SHADOW)

    def ornament(self, active):
        return ribs(4, 3, active)

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return crown(cx, cy + 1, 1, "#5a4a40", "#2a2024")
        b = circle(cx, cy, 9, GOLD, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        return b + crown(cx, cy + 1, 1)

    def corner_mark(self, x, y, active, which):
        # pink and blue: Palkia on one side, Dialga on the other
        return circle(x, y, 2, PALKIA if which == "left" else DIALGA) if active else ""

    def check_mark(self, s, hover):
        return crown(s / 2, s / 2 + 1, 0.5, GOLD)

    def radio_mark(self, s, hover):
        c = s / 2
        return (circle(c, c, c - 3, STRIPE) + circle(c, c, c - 5, GOLD))

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, [GOLD, PALKIA, DIALGA, STRIPE][i - 1])

    def menu_tile(self, w, h):
        # the Distortion World's floating stone
        return (rect(0, 0, w, h, self.MENU_BG)
                + path(f"M2,{h - 4} L8,{h - 9} L14,{h - 6} L10,{h - 2} Z", fill="#2a1820")
                + path(f"M{w - 10},6 L{w - 4},3 L{w - 2},8 L{w - 8},10 Z", fill="#2a1820"))
