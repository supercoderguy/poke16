"""Eon: Latias and Latios over Alto Mare at night - deep blue water streaks,
Latios blue and Latias red, white wing trim, the red/blue triangle marks."""

from base import circle, path, rect
from themes._common import starfield
from themes._kit import Kit

NIGHT = "#0e1c3a"
NIGHT_LT = "#1e3a6a"
SEA = "#1a6aa8"
LATIOS = "#3a5ad8"
LATIOS_DK = "#24365a"
LATIAS = "#d83a3a"
LATIAS_DK = "#8a2030"
TRIM = "#f0f2f8"
GLOW = "#9ae8ff"
LAMP = "#f8c868"


def tri(cx, cy, r, fill, rot=0):
    """The triangle on Latios'/Latias' chest."""
    return f'<g transform="rotate({rot} {cx} {cy})">' + path(
        f"M{cx - r},{cy - r * 0.6} L{cx + r},{cy - r * 0.6} L{cx},{cy + r * 0.9} Z", fill=fill) + "</g>"


class Eon(Kit):
    NAME = "Eon"
    WALLPAPER = "19/wp2054972-latios-and-latias-wallpaper.png"
    WALLPAPER_MODE = "crop"
    BG_SOLID = NIGHT

    TITLE = (NIGHT_LT, NIGHT)
    TITLE_DIM = ("#1e2634", "#161c28")
    TITLE_HI = "#3a5a8a"
    BAND, BAND2, BAND_DIM, OUTER = LATIOS, LATIAS, "#2a3040", "#060c1a"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = NIGHT, TRIM, "#161c28", "#2a3040"
    BG, BG_DK, MENU_BG, LINE = "#122244", "#0a1630", "#0c1a36", "#2a4470"
    ACCENT, ACCENT_HI, ACCENT_FG = LATIOS, GLOW, "#ffffff"
    SEL, SEL_EDGE = (LATIOS, LATIAS), TRIM
    POPUP_BG, POPUP_EDGE = TRIM, LATIOS_DK
    BTN = dict(inactive=("#1e2634", "#3a4458", "#7a8498"), active=(TRIM, LATIOS_DK, LATIOS_DK),
               hover=(GLOW, "#ffffff", LATIOS_DK), close_hover=(LATIAS, "#ffffff", "#ffffff"),
               clicked=(LATIOS, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 40
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans Bold 9")
    TEXT = dict(title_active=TRIM, title_inactive="#7a8498", menu_title=TRIM,
                menu="#d8e4f8", menu_hilite="#ffffff", dialog="#d8e4f8", tooltip=LATIOS_DK)
    CURSOR = (TRIM, LATIOS_DK)

    def ornament(self, active):
        # the pair streaking past: a blue and a red swept wing
        a, b = (LATIOS, LATIAS) if active else ("#2e3850", "#3e2e38")
        return (path("M4,8 C14,4 26,4 40,7 L30,10 Z", fill=a, stroke=TRIM if active else "#4a5468", sw=0.7)
                + path("M4,16 C14,12 26,12 40,15 L30,18 Z", fill=b, stroke=TRIM if active else "#4a5468", sw=0.7))

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return tri(cx, cy, 6.5, "#3a4458")
        b = circle(cx, cy, 9, GLOW, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        return b + tri(cx - 2, cy, 5.5, LATIOS) + tri(cx + 2.5, cy + 1, 5.5, LATIAS, 180)

    def corner_mark(self, x, y, active, which):
        return tri(x, y, 2.5, LATIOS if which == "left" else LATIAS) if active else ""

    def check_mark(self, s, hover):
        return tri(s / 2, s / 2, s / 2 - 2.5, LATIAS)

    def radio_mark(self, s, hover):
        return tri(s / 2, s / 2 + 0.5, s / 2 - 3, LATIOS)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, [GLOW, LAMP, TRIM, GLOW][i - 1])

    def menu_tile(self, w, h):
        # Alto Mare's lamplight on the water
        return rect(0, 0, w, h, self.MENU_BG) + starfield(w, h, 19, 6, [GLOW, LAMP, "#ffffff"], 0.8)
