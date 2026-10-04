"""Paldea: the starters' coral backdrop, a Scarlet/Violet Poke Ball logo, starter-coloured buttons."""

from base import circle, path, rect
from themes._kit import Kit

CORAL = "#ed7660"
CORAL_LT = "#f59882"
CORAL_DK = "#c85a46"
CREAM = "#fff6ec"
YELLOW = "#fff200"
INK = "#3a2620"
SPRIG = "#6aa84a"       # Sprigatito green
FUECO = "#e2502e"       # Fuecoco red
QUAX = "#4ab0e0"        # Quaxly blue
TILE_A, TILE_B = "#f8e8a8", "#a8d8e8"


def ball(cx, cy, r, top=YELLOW, edge=INK):
    """The Scarlet/Violet logo ball: a yellow ring with a band."""
    return (circle(cx, cy, r, top, edge, 1) + circle(cx, cy, r * 0.55, CORAL, edge, 0.8)
            + rect(cx - r, cy - 0.6, r * 0.45, 1.2, edge) + rect(cx + r * 0.55, cy - 0.6, r * 0.45, 1.2, edge))


class Paldea(Kit):
    NAME = "Paldea"
    WALLPAPER = "16/Pokémon.Scarlet...Violet.full.3975849-763114152.jpg"
    BG_SOLID = CORAL

    TITLE = (CORAL_LT, CORAL)
    TITLE_DIM = ("#e8c8be", "#dcb2a6")
    TITLE_HI = "#ffd0c2"
    BAND, BAND2, BAND_DIM, OUTER = CREAM, YELLOW, "#ecdcd2", CORAL_DK
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = CORAL, CREAM, "#dcb2a6", "#f0e2da"
    BG, BG_DK, MENU_BG, LINE = CREAM, "#ffffff", CREAM, "#f0c8b8"
    ACCENT, ACCENT_HI, ACCENT_FG = FUECO, CORAL_DK, "#ffffff"
    SEL, SEL_EDGE = (CORAL, CORAL_LT), YELLOW
    SEL_RADIUS = 10
    CHECK_EDGE = CORAL_DK
    POPUP_BG, POPUP_EDGE = CREAM, CORAL_DK
    POPUP_RADIUS = 8
    BTN = dict(inactive=("#f0dcd4", "#c8a89c", "#a88a80"), active=(CREAM, INK, INK),
               hover=(QUAX, INK, "#ffffff"), close_hover=(FUECO, INK, "#ffffff"),
               clicked=(SPRIG, INK, "#ffffff"))
    FRAME_RADIUS = 6
    MENU_BG_TILE = 24
    TEXT_EFFECT = "__EFFECT_NONE"
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans ExtraBold 9")
    TEXT = dict(title_active="#ffffff", title_inactive="#8a6a60", menu_title="#ffffff",
                menu=INK, menu_hilite="#ffffff", dialog=INK, tooltip=INK)
    CURSOR = (CREAM, CORAL_DK)
    YTM = dict(veil=0.8)

    def ornament(self, active):
        # three dots for the three starters
        cs = (SPRIG, FUECO, QUAX) if active else ("#d8c0b8",) * 3
        return "".join(circle(10 + i * 9, 11, 3.6, c, CREAM if active else "#e8d8d0", 1) for i, c in enumerate(cs))

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return ball(cx, cy, 7.5, "#f0e4c8", "#b8988c")
        b = circle(cx, cy, 9, YELLOW, extra='opacity="0.7" filter="url(#g)"') if state == "hover" else ""
        return b + ball(cx, cy, 7.5)

    def corner_mark(self, x, y, active, which):
        return circle(x, y, 2, YELLOW, INK, 0.6) if active else ""

    def check_mark(self, s, hover):
        return path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=SPRIG, sw=2.2)

    def radio_mark(self, s, hover):
        return ball(s / 2, s / 2, s / 2 - 2.2)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, [SPRIG, FUECO, QUAX, YELLOW][i - 1], INK, 0.8)

    def menu_tile(self, w, h):
        # the Mesagoza tiled floor, faintly
        return (rect(0, 0, w, h, CREAM) + rect(0, 0, w / 2, h / 2, TILE_A, extra='opacity="0.25"')
                + rect(w / 2, h / 2, w / 2, h / 2, TILE_B, extra='opacity="0.25"'))


    # ---- shape: the three starters peeking over the title bar: Sprigatito's ears, Fuecoco's flame, Quaxly's crest ----

    SHAPE = dict(top=22)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def starters(active):
            k = (lambda c: c) if active else (lambda c: mute(c, "#dcb2a6", 0.6))
            kw = dict(edge=k(INK), sw=1.2, bulge=0.2)
            # Sprigatito: two little green ears
            b = plump_ear((2, T + 3), (12, T + 3), (3, 6), "s1", fill=k(SPRIG), tipc=k("#3a7a2a"), **kw)
            b += plump_ear((14, T + 3), (24, T + 3), (22, 6), "s2", fill=k(SPRIG), tipc=k("#3a7a2a"), **kw)
            # Fuecoco: the flame on its head
            b += path(f"M34,{T + 3} C30,{T - 6} 36,12 38,4 C40,10 46,{T - 8} 44,{T + 3} Z", fill=k(FUECO), stroke=k(INK), sw=1.2)
            b += path(f"M37,{T + 3} C35,{T - 4} 38,{T - 10} 39,{T - 14} C40,{T - 8} 42,{T - 4} 41,{T + 3} Z", fill=k(YELLOW))
            # Quaxly: its blue wave crest
            b += path(f"M52,{T + 3} C50,{T - 8} 58,6 68,8 C62,10 60,14 64,16 C58,16 58,{T - 4} 62,{T + 3} Z",
                      fill=k(QUAX), stroke=k(INK), sw=1.2)
            return svg(70, T + 3, b)

        return [("starters", 70, T + 3, "tl", 4, 0, starters)]
