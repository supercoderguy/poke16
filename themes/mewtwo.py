"""Mewtwo: pale lavender-white on a black starfield, the purple tail and belly, psychic glow."""

from base import circle, path, rect
from themes._common import starfield
from themes._kit import Kit

SPACE = "#050508"
SPACE_LT = "#14141c"
PALE = "#e8e6f4"
PALE_DK = "#c8c4dc"
PURPLE = "#8a62b8"
PURPLE_DK = "#5a3e82"
PSY = "#c890ff"
INK = "#2a2438"


def psy_orb(cx, cy, r, core=PALE, ring=PURPLE):
    """A Shadow Ball / psychic orb."""
    return circle(cx, cy, r, ring) + circle(cx - r * 0.2, cy - r * 0.2, r * 0.6, core) + circle(cx, cy, r, "none", PSY, 0.8)


class Mewtwo(Kit):
    NAME = "Mewtwo"
    WALLPAPER = "20/wp2152739-mewtwo-hd-wallpapers.jpg"
    WALLPAPER_MODE = "crop"
    BG_SOLID = SPACE

    TITLE = (PALE, PALE_DK)
    TITLE_DIM = ("#4a4858", "#3a3846")
    TITLE_HI = "#ffffff"
    BAND, BAND2, BAND_DIM, OUTER = PURPLE, PURPLE_DK, "#2e2c38", SPACE
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = SPACE_LT, PURPLE, "#1c1c24", "#2e2c38"
    BG, BG_DK, MENU_BG, LINE = "#121218", "#08080c", SPACE, "#2e2c3c"
    ACCENT, ACCENT_HI, ACCENT_FG = PURPLE, PSY, "#ffffff"
    SEL, SEL_EDGE = (PURPLE_DK, PURPLE), PALE
    POPUP_BG, POPUP_EDGE = PALE, PURPLE_DK
    POPUP_RADIUS = 8
    BTN = dict(inactive=("#3a3846", "#5a5868", "#9a98a8"), active=(PURPLE, INK, PALE),
               hover=(PSY, "#ffffff", INK), close_hover=("#d0406a", "#ffffff", "#ffffff"),
               clicked=(PURPLE_DK, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 40
    TEXT_EFFECT = "__EFFECT_NONE"
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans Black 9")
    TEXT = dict(title_active=INK, title_inactive="#b0aec0", menu_title=INK,
                menu="#dedcec", menu_hilite="#ffffff", dialog="#dedcec", tooltip=INK)
    CURSOR = (PALE, PURPLE_DK)

    def ornament(self, active):
        # the curling tail
        c = PURPLE if active else "#5a5868"
        return path("M6,18 C6,6 20,4 26,10 C30,14 26,20 20,17 C16,15 18,11 22,12", stroke=c, sw=3)

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return circle(cx, cy, 7, "#3a3846", "#6a6878", 1)
        b = circle(cx, cy, 10, PSY, extra='opacity="0.7" filter="url(#g)"') if state == "hover" else ""
        return b + psy_orb(cx, cy, 7.5)

    def corner_mark(self, x, y, active, which):
        return circle(x, y, 2, PSY, extra='opacity="0.9"') if active else ""

    def check_mark(self, s, hover):
        return path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=PSY, sw=2)

    def radio_mark(self, s, hover):
        return psy_orb(s / 2, s / 2, s / 2 - 2.6)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, PSY, extra=f'opacity="{1 - i * 0.15}"')

    def menu_tile(self, w, h):
        return rect(0, 0, w, h, SPACE) + starfield(w, h, 20, 9, ["#ffffff", PALE_DK, PSY], 0.8)
