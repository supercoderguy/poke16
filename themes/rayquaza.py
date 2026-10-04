"""Rayquaza: an emerald serpent's body with yellow ring markings, glowing green energy."""

from base import Art, circle, frame, hgrad, path, rect, sparkle, svg, vgrad
from themes._common import frame_bottom, frame_corner, frame_side, glyph, starfield, title_grad, tri_arrow

SPACE = "#04140a"
DEEP = "#08180e"
RAY_LT = "#4ab07a"
RAY = "#2a8a5a"
RAY_DK = "#145a36"
YELLOW = "#e8c840"
YELLOW_DK = "#a88a20"
NEON = "#40ff70"
NEON_DK = "#1ac04a"
RED = "#cf4512"
BLACK = "#0a0e0c"
DIM = "#1a2a20"
DIM_DK = "#0e1a12"
DIM_Y = "#5a5a3a"


def ring_mark(cx, cy, rx, ry, yellow=YELLOW, outline=BLACK, sw=1.8):
    """Rayquaza's ring markings: yellow rings with a black outline."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{outline}" stroke-width="{sw + 1.4}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{yellow}" stroke-width="{sw}"/>')


GLOW = '<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.3"/></filter>'


class Rayquaza(Art):
    NAME = "Rayquaza"
    WALLPAPER = "12/wp2075324-rayquaza-hd-wallpapers.png"
    WALLPAPER_MODE = "crop"      # the image is 2:1
    BG_SOLID = SPACE

    P = dict(base=DEEP, panel=DEEP, raised=RAY_DK, line=NEON_DK, line_dim="#1e3a28",
             accent=NEON_DK, accent_hi=NEON, text="#d0f0d8", text_dim="#7a9a84",
             sel=NEON_DK, sel_text="#ffffff", danger=RED, shadow=SPACE)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=44, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans ExtraBold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold 8")

    TEXT = dict(title_active="#f0fff0", title_inactive="#7a9a84", menu_title="#f0fff0",
                menu="#d0f0d8", menu_hilite="#ffffff", dialog="#d0f0d8", tooltip="#d8ffe0")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    MENU_BG_TILE = 40
    CURSOR = (NEON, BLACK)
    MATTE = dict(title=RAY, menu=SPACE, dialog=DEEP, popup=DEEP)
    ROFI = dict(border_color=NEON_DK, radius=4, sel=(
        "background-image: linear-gradient(to right, #2ad860, #0a8a3a); "
        "border: 0 0 0 3px; border-color: #e8c840; border-radius: 3px;"))

    # ---- window borders: the serpent's body ----------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, RAY_LT), (0.5, RAY), (1, RAY_DK)] if active else [(0, DIM), (1, DIM_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, BLACK)
        b += rect(0, TH - 6 - dy, w, 1.5, YELLOW if active else DIM_Y)              # yellow side stripe
        b += rect(0, TH - 4.5 - dy, w, 1, BLACK)
        if active:   # energy glow under the body
            b += rect(0, TH - 3 - dy, w, 2, NEON, extra='opacity="0.8" filter="url(#g)"') + rect(0, TH - 2.5 - dy, w, 1, NEON)
        b += rect(0, TH - 1 - dy, w, 1, BLACK)
        return title_grad(TH, dy, stops) + GLOW, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        y, k = (YELLOW, BLACK) if active else (DIM_Y, "#060a08")
        b += ring_mark(11, 10, 6.5, 4.5, y, k) + ring_mark(26, 10, 4.5, 3.2, y, k) + ring_mark(36, 10, 2.8, 2, y, k, 1.4)
        b += rect(w - 1, 0, 1, h, BLACK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#v)") + rect(0, 0, w, 1, BLACK)
        b += rect(0, h - 6, w, 1.5, YELLOW) + rect(0, h - 4.5, w, 1, BLACK)
        b += rect(0, h - 3, w, 2, NEON, extra='opacity="0.8" filter="url(#g)"') + rect(0, h - 2.5, w, 1, NEON)
        b += rect(0, h - 1, w, 1, BLACK)
        b += ring_mark(11, 9, 5.5, 3.8) + ring_mark(w - 11, 9, 5.5, 3.8)
        return svg(w, h, b, vgrad("v", [(0, RAY_LT), (0.5, RAY), (1, RAY_DK)]) + GLOW)

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, BLACK)
        cx, cy = s / 2 + 1, s / 2 - 2.5
        if state == "inactive":
            b += ring_mark(cx, cy, 6.5, 6.5, DIM_Y, "#060a08", 2.2)
        else:
            if state == "hover":
                b += circle(cx, cy, 9, NEON, extra='opacity="0.8" filter="url(#g)"')
            b += ring_mark(cx, cy, 6.5, 6.5, YELLOW, BLACK, 2.2) + circle(cx, cy, 2, NEON if state == "hover" else YELLOW)
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, g = {"inactive": (DIM_DK, DIM_Y, "#7a9a84"),
                        "active": (RAY_DK, YELLOW, YELLOW),
                        "hover": (RED if kind == "close" else NEON, "#ffffff", "#ffffff" if kind == "close" else BLACK),
                        "clicked": (YELLOW_DK, YELLOW, BLACK)}[state]
        c = s / 2
        if state == "hover":
            b += circle(c, c, c - 1, NEON if kind != "close" else RED, extra='opacity="0.8" filter="url(#g)"')
        b += circle(c, c, c - 1.5, BLACK) + circle(c, c, c - 2.2, fill, rim, 1.4)
        b += glyph(kind, s, g, 1.8, 6.3)
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (DEEP, BLACK, NEON_DK) if active else (DIM_DK, BLACK, "#1e3a28")

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            b += ring_mark(10 if which == "left" else w - 10, h / 2 + 0.5, 3, 2, YELLOW, BLACK, 1.1)
        return svg(w, h, b)

    # ---- menus: green-tinted space ----------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE) + starfield(w, h, 12, 9, [NEON, "#a0ffb0", "#ffffff"], 0.8))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, "url(#s)", rx=3) + rect(2, 1, 3, h - 2, YELLOW)
                   + rect(6, 1.5, w - 10, 1, "#ffffff", extra='opacity="0.3"'),
                   hgrad("s", [(0, "#2ad860"), (1, "#0a8a3a")]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        # a fin: a swept-back triangle
        fin = path(f"M{x},{m - 5} L{x + 7},{m} L{x},{m + 5} L{x + 2.5},{m} Z", fill=YELLOW, stroke=BLACK, sw=0.6)
        return base.replace("</svg>", fin + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, DEEP))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#1e5a34", 1, rx=4, fill="#04100a"))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (RAY_DK, YELLOW), "hover": (RAY, NEON), "clicked": (NEON_DK, "#ffffff")}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=4)
                   + rect(3, 2, w - 6, 1, "#ffffff", extra='opacity="0.2"'))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, "#04100a", NEON if hover else YELLOW, 1, rx=2)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=NEON, sw=2)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, "#04100a", NEON if hover else YELLOW_DK, 1)
        if on:
            b += ring_mark(c, c, c - 3, c - 3, YELLOW, BLACK, 1.6)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, "#1e5a34"))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#1e5a34", 1, rx=min(w, h) / 2, fill="#04100a"))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, NEON if clicked else RAY, YELLOW, 1, rx=min(w, h) / 2))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, RAY) + circle(s / 2, s / 2, 2, YELLOW))

    # ---- popups: dark with a neon edge ------------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NEON_DK, rx=4) + rect(1.5, 1.5, w - 3, h - 3, DEEP, rx=3)
                   + rect(1.5, h - 3.5, w - 3, 2, YELLOW))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NEON_DK, rx=4) + rect(1.5, 1.5, w - 3, h - 3, DEEP, rx=3))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, YELLOW, rx=4) + rect(1.5, 1.5, w - 3, h - 3, NEON_DK, rx=3))

    def bubble(self, s, i):
        return svg(s, s, sparkle(s / 2, s / 2, s / 2 - 0.3, [NEON, "#a0ffb0", YELLOW, NEON][i - 1]))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, NEON_DK), (1, NEON)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK) + rect(1, 1, w - 2, h - 2, RAY) + rect(1, 1, w - 2, 2, YELLOW))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, NEON, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, DEEP))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#1e5a34", 1, rx=4, fill="#04100a"))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, DEEP, YELLOW))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, RAY_DK) + rect(w - 3, 0, 1.5, h, YELLOW) + rect(w - 1, 0, 1, h, BLACK))
        return svg(w, h, rect(0, 0, w, h, RAY_DK) + rect(0, h - 3, w, 1.5, YELLOW) + rect(0, h - 1, w, 1, BLACK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: its head fin sweeping up off the title bar and body fins out of the right side ----

    SHAPE = dict(top=24, right=26)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def headfin(active):
            body, ring, edge = (RAY, YELLOW, BLACK) if active else (DIM, DIM_Y, BLACK)
            d = f"M6,{T + 3} C10,{T - 8} 18,6 46,1 C34,8 28,{T - 6} 30,{T + 3} Z"
            b = path(d, fill=body, stroke=edge, sw=1.3)
            b += path(f"M14,{T - 2} C20,14 30,8 40,4", stroke=ring, sw=1.8)
            return svg(48, T + 3, b)

        def fins(active):
            body, ring, edge = (RAY, YELLOW, BLACK) if active else (DIM, DIM_Y, BLACK)
            b = ""
            for y, reach in ((2, 30), (30, 24)):
                d = f"M0,{y} L0,{y + 16} L{reach - 8},{y + 10} L{reach},{y} L{reach - 10},{y + 4} Z"
                b += path(d, fill=body, stroke=edge, sw=1.2)
                b += path(f"M3,{y + 8} L{reach - 10},{y + 6}", stroke=ring, sw=1.5)
            return svg(31, 48, b)

        return [("headfin", 48, T + 3, "tl", 2, 0, headfin),
                ("fins", 31, 48, "tr", 0, T + 12, fins)]
