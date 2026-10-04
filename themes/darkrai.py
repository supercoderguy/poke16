"""Darkrai: smoke-black and storm-grey, the red collar spikes, a cyan eye, the white plume."""

from base import circle, path, rect
from themes._kit import Kit

SMOKE = "#1c1c1c"
SMOKE_LT = "#3a3a3c"
INK = "#0b0b0c"
RED = "#b4202a"
RED_DK = "#661d23"
PLUME = "#d8d8dc"
CYAN = "#22b8cc"
GREY = "#6a6a70"


def collar(x, y, k, fill=RED):
    """Darkrai's jagged red collar: a row of downward spikes."""
    d = f"M{x},{y}"
    for i in range(5):
        d += f" L{x + (i + 0.5) * 6 * k},{y + 7 * k} L{x + (i + 1) * 6 * k},{y}"
    return path(d + " Z", fill=fill)


def eye(cx, cy, r, colour=CYAN):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.4}" ry="{r}" fill="{PLUME}"/>'
            + circle(cx + r * 0.2, cy, r * 0.7, colour) + circle(cx + r * 0.2, cy, r * 0.3, INK))


class Darkrai(Kit):
    NAME = "Darkrai"
    WALLPAPER = "15/JZLJt7d-pokemon-darkrai-wallpaper.jpg"
    BG_SOLID = SMOKE

    TITLE = ("#3a3a3e", "#18181a")
    TITLE_DIM = ("#2a2a2c", "#1c1c1e")
    TITLE_HI = "#5a5a60"
    BAND, BAND_DIM, OUTER = RED, "#3a2a2c", INK
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = "#161618", RED_DK, "#1c1c1e", "#2e2e30"
    BG, BG_DK, MENU_BG, LINE = "#1a1a1c", "#101012", "#141416", "#2e2e32"
    CHECK_EDGE = GREY
    ACCENT, ACCENT_HI, ACCENT_FG = RED, "#e0404a", "#ffffff"
    SEL, SEL_EDGE = ("#7a1c24", "#b4202a"), CYAN
    POPUP_BG, POPUP_EDGE = "#202024", PLUME
    BTN = dict(inactive=("#222224", "#4a4a50", GREY), active=(INK, PLUME, PLUME),
               hover=(CYAN, "#ffffff", INK), close_hover=(RED, "#ffffff", "#ffffff"),
               clicked=(PLUME, "#ffffff", INK))
    MENU_BG_TILE = 24
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans Black 9")
    TEXT = dict(title_active="#ececf0", title_inactive="#7a7a80", menu_title="#ececf0",
                menu="#d8d8dc", menu_hilite="#ffffff", dialog="#d8d8dc", tooltip="#ececf0")
    CURSOR = (PLUME, INK)

    def ornament(self, active):
        return collar(6, 7, 1.1, RED if active else "#4a3a3c")

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return circle(cx, cy, 6, "#2a2a2c", GREY, 1)
        b = ""
        if state == "hover":
            b += circle(cx, cy, 8, CYAN, extra='opacity="0.6" filter="url(#g)"')
        return b + eye(cx, cy, 4.5)

    def corner_mark(self, x, y, active, which):
        return circle(x, y, 1.6, RED) if active else ""

    def check_mark(self, s, hover):
        return path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=CYAN if hover else "#e0404a", sw=2.2)

    def radio_mark(self, s, hover):
        return eye(s / 2, s / 2, 2.6)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, PLUME if i < 3 else GREY)

    def menu_tile(self, w, h):
        # Darkrai's smoke: soft dark patches
        return (rect(0, 0, w, h, self.MENU_BG) + circle(6, 6, 7, "#1e1e22", extra='opacity="0.7"')
                + circle(18, 18, 6, "#1c1c20", extra='opacity="0.7"'))


    # ---- shape: its white smoke plume streaming off the top, red collar spikes out of the left side ----

    SHAPE = dict(top=28, left=18)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def plume(active):
            fill, edge = (PLUME, GREY) if active else (SMOKE_LT, "#2a2a2c")
            d = (f"M6,{T + 3} C4,{T - 10} 12,10 24,6 C34,3 42,8 52,2 C48,10 40,14 32,15 "
                 f"C40,16 46,20 50,24 C40,22 32,{T - 2} 30,{T + 3} Z")
            return svg(54, T + 3, path(d, fill=fill, stroke=edge, sw=1.2))

        def spikes(active):
            fill, edge = (RED, INK) if active else ("#3a2a2c", INK)
            b = ""
            for y in (2, 16, 30):
                b += path(f"M23,{y} L23,{y + 11} L0,{y + 5} Z", fill=fill, stroke=edge, sw=1)
            return svg(23, 44, b)

        return [("plume", 54, T + 3, "tl", 18, 0, plume),
                ("spikes", 23, 44, "tl", 0, T + 6, spikes)]
