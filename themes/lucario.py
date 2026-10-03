"""Lucario: blue with a black mask band, chest-spike ornament, an aura-sphere emblem."""

from base import Art, circle, frame, hgrad, path, rect, svg, vgrad
from themes._common import frame_bottom, frame_corner, frame_side, glyph, title_grad, tri_arrow

BLUE_LT = "#4aa8f0"
BLUE = "#1e7ad8"
BLUE_DK = "#0a3a8a"
DEEP = "#06184a"
NIGHT = "#0a1220"
PANEL = "#0e1626"
BLACK = "#16171c"
BLACK_LT = "#2a2c34"
YELLOW = "#f0d050"
RED = "#d81818"
AURA = "#a8e8ff"
AURA_W = "#e8f8ff"
SPIKE = "#d8e8f4"
DIM = "#2a2c34"
DIM_DK = "#1e2026"

GLOW = '<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>'
SPHERE = ('<radialGradient id="as" cx="0.4" cy="0.38" r="0.62">'
          f'<stop offset="0" stop-color="#ffffff"/><stop offset="0.35" stop-color="{AURA}"/>'
          f'<stop offset="0.8" stop-color="{BLUE_LT}"/><stop offset="1" stop-color="{BLUE}"/></radialGradient>')


def aura_sphere(cx, cy, r, glow=True):
    b = circle(cx, cy, r + 1.5, AURA, extra='opacity="0.6" filter="url(#g)"') if glow else ""
    return b + circle(cx, cy, r, "url(#as)")


def spike(x, cy, length, half, fill=SPIKE):
    """The spike on Lucario's chest and paws, pointing right."""
    return path(f"M{x},{cy - half} L{x + length},{cy} L{x},{cy + half} Z", fill=fill)


class Lucario(Art):
    NAME = "Lucario"
    WALLPAPER = "13/wp2217966-pokemon-ex-wallpapers.png"
    BG_SOLID = DEEP

    P = dict(base=PANEL, panel=PANEL, raised=BLACK_LT, line=BLUE, line_dim="#1e2a40",
             accent=BLUE, accent_hi=AURA, text="#d8e6f8", text_dim="#8a92a8",
             sel=BLUE, sel_text="#ffffff", danger=RED, shadow=DEEP)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=40, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans Bold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans SemiBold 8")

    TEXT = dict(title_active="#ffffff", title_inactive="#8a92a8", menu_title="#ffffff",
                menu="#d8e6f8", menu_hilite="#ffffff", dialog="#d8e6f8", tooltip="#e8f4ff")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    CURSOR = (AURA_W, BLACK)
    MATTE = dict(title=BLUE, menu=NIGHT, dialog=PANEL, popup=BLACK)
    ROFI = dict(border_color=BLUE, radius=6, sel=(
        "background-image: linear-gradient(to right, #1e7ad8, #4aa8f0); "
        "border: 0 0 0 3px; border-color: #a8e8ff; border-radius: 4px;"))

    # ---- window borders: blue with the black mask band -------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, BLUE_LT), (0.55, BLUE), (1, BLUE_DK)] if active else [(0, DIM), (1, DIM_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, "#8ac8ff" if active else "#3a3c44")
        b += rect(0, TH - 6 - dy, w, 1, YELLOW if active else "#4a4a44")          # chest fur
        b += rect(0, TH - 5 - dy, w, 5, BLACK)                                      # mask band
        return title_grad(TH, dy, stops), b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += '<g filter="url(#g)" opacity="0.9">' + spike(6, 10, 16, 3.5, AURA) + "</g>"
            b += spike(6, 10, 16, 3, SPIKE) + spike(24, 10, 8, 2, AURA_W)
        else:
            b += spike(6, 10, 16, 3, "#4a4e58") + spike(24, 10, 8, 2, "#3e424c")
        b += rect(w - 1, 0, 1, h, BLACK)
        return svg(w, h, b, defs + GLOW)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#v)") + rect(0, 0, w, 1, "#8ac8ff")
        b += rect(0, h - 6, w, 1, YELLOW) + rect(0, h - 5, w, 5, BLACK)
        b += aura_sphere(11, h / 2 - 3, 4.5) + aura_sphere(w - 11, h / 2 - 3, 4.5)
        return svg(w, h, b, vgrad("v", [(0, BLUE_LT), (0.55, BLUE), (1, BLUE_DK)]) + GLOW + SPHERE)

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, BLACK)
        cx, cy = s / 2 + 1, s / 2 - 3
        if state == "inactive":
            b += circle(cx, cy, 6.5, "#3a3e48") + circle(cx - 1.5, cy - 1.5, 2.5, "#5a5e68")
        else:
            b += aura_sphere(cx, cy, 6.5 if state == "active" else 7.5)
        return svg(s, s, b, defs + GLOW + SPHERE)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, g = {"inactive": (DIM_DK, "#3a3c44", "#8a92a8"),
                        "active": (BLACK, BLACK_LT, AURA),
                        "hover": (RED if kind == "close" else AURA, "#ffffff", "#ffffff" if kind == "close" else BLACK),
                        "clicked": (BLUE_DK, AURA, "#ffffff")}[state]
        if state == "hover":
            b += rect(1, 1, s - 2, s - 2, RED if kind == "close" else AURA, rx=6, extra='opacity="0.8" filter="url(#g)"')
        b += rect(1.5, 1.5, s - 3, s - 3, fill, rim, 1.2, rx=5)   # a black paw pad
        b += glyph(kind, s, g, 1.9, 6)
        return svg(s, s, b, defs + GLOW)

    def _edge(self, active):
        return (BLACK, "#08090c", BLUE) if active else (DIM_DK, "#08090c", "#2a3040")

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            b += (spike(6, h / 2 + 0.5, 8, 2, SPIKE) if which == "left"
                  else f'<g transform="translate({w},0) scale(-1,1)">' + spike(6, h / 2 + 0.5, 8, 2, SPIKE) + "</g>")
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NIGHT))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, "url(#s)", rx=4) + rect(2, 1, 3, h - 2, AURA, rx=1)
                   + rect(6, 1.5, w - 10, 1, "#ffffff", extra='opacity="0.3"'),
                   hgrad("s", [(0, BLUE), (1, BLUE_LT)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        return base.replace("</svg>", spike(w - 16, h / 2, 9, 3.5, "#ffffff" if hilite else SPIKE) + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PANEL))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#1e3a6a", 1, rx=4, fill=NIGHT))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (BLACK, BLUE), "hover": (BLACK_LT, AURA), "clicked": (BLUE, AURA_W)}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=5)
                   + rect(4, 2, w - 8, 1, "#ffffff", extra='opacity="0.12"'))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, NIGHT, AURA if hover else BLUE, 1, rx=2)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=YELLOW, sw=2)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, NIGHT, AURA if hover else BLUE, 1)
        if on:
            b += aura_sphere(c, c, c - 2.6, glow=False)
        return svg(s, s, b, SPHERE)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, "#1e3a6a"))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#1e3a6a", 1, rx=min(w, h) / 2, fill=NIGHT))

    def knob(self, w, h, vertical, clicked):
        g = hgrad("k", [(0, BLUE), (1, BLUE_LT)]) if not clicked else hgrad("k", [(0, AURA), (1, "#ffffff")])
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", AURA_W, 0.8, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, BLUE) + circle(s / 2, s / 2, 2, AURA_W))

    # ---- popups: black with an aura edge -----------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLUE, rx=5) + rect(1.5, 1.5, w - 3, h - 3, BLACK, rx=4)
                   + rect(1.5, h - 3.5, w - 3, 1, YELLOW))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLUE, rx=5) + rect(1.5, 1.5, w - 3, h - 3, BLACK, rx=4))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, AURA, rx=5) + rect(1.5, 1.5, w - 3, h - 3, BLUE, rx=4))

    def bubble(self, s, i):
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 0.4, "url(#as)"), SPHERE)

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, BLUE), (1, AURA)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, DEEP))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK) + rect(1, 1, w - 2, h - 2, BLUE) + rect(1, h - 5, w - 2, 4, BLACK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, AURA, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PANEL))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#1e3a6a", 1, rx=4, fill=NIGHT))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, PANEL, AURA))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, BLACK) + rect(w - 2, 0, 1.5, h, BLUE))
        return svg(w, h, rect(0, 0, w, h, BLACK) + rect(0, h - 2, w, 1.5, BLUE))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
