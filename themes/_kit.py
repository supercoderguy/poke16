"""A parametrised theme base for the later themes.

A theme sets the colour attributes below and overrides whichever motif hooks it
wants (ornament, emblem_art, corner_mark, check_mark, radio_mark, arrow_mark,
bubble_art, menu_tile).  Everything else - title bar layering, frames, title
buttons, menus, dialogs, popups, pager - is drawn here from those colours.
"""

from base import Art, circle, frame, hgrad, path, rect, sparkle, svg, vgrad
from themes._common import diamond, frame_bottom, frame_corner, frame_side, glyph, title_grad, tri_arrow


class Kit(Art):
    # --- title bar ---------------------------------------------------------
    TITLE = ("#444444", "#222222")         # active gradient top, bottom
    TITLE_DIM = ("#333333", "#262626")     # inactive gradient
    TITLE_HI = "#666666"                   # 1px top highlight
    BAND = "#888888"                       # accent stripe under the title
    BAND2 = None                           # optional second stripe below it
    BAND_DIM = "#3a3a3a"
    OUTER = "#000000"                      # outline round the window
    # --- frame -------------------------------------------------------------
    FRAME = "#222222"
    FRAME_IN = "#888888"                   # inner accent line on the frame
    FRAME_DIM = "#262626"
    FRAME_IN_DIM = "#3a3a3a"
    # --- surfaces ----------------------------------------------------------
    BG = "#1c1c1c"                         # dialogs / windows
    BG_DK = "#141414"                      # fields, areas, troughs
    MENU_BG = "#1c1c1c"
    LINE = "#3a3a3a"                       # field / area outlines
    # --- accents -----------------------------------------------------------
    ACCENT = "#4a90d9"
    ACCENT_HI = "#7ab4f0"
    ACCENT_FG = "#ffffff"
    SEL = ("#4a90d9", "#7ab4f0")           # selection gradient (left -> right)
    SEL_EDGE = "#ffffff"                   # 3px marker on the selection's left
    SEL_RADIUS = 4
    CHECK_EDGE = None                      # check/radio outline; default FRAME_IN
    # --- popups ------------------------------------------------------------
    POPUP_BG = "#2a2a2a"
    POPUP_EDGE = "#888888"
    POPUP_RADIUS = 5
    # --- title buttons -------------------------------------------------------
    BTN_SHAPE = "circle"                   # circle | square | diamond
    BTN = dict(inactive=("#2a2a2a", "#555555", "#888888"),   # fill, rim, glyph
               active=("#111111", "#888888", "#ffffff"),
               hover=("#4a90d9", "#ffffff", "#ffffff"),
               close_hover=("#d94a4a", "#ffffff", "#ffffff"),
               clicked=("#ffffff", "#ffffff", "#111111"))
    FRAME_RADIUS = 0                       # rounding of push buttons / areas

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=50, menu_title_h=24)
    FONTS = dict(border="pango:Adwaita Sans Bold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans SemiBold 8")

    TEXT_EFFECT = "__EFFECT_SHADOW"
    TITLE_JUSTIFY = 0
    GLOW = '<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>'

    def __init__(self):
        # derive the framework palette / rofi highlight from the kit colours
        T = self.TEXT
        self.P = dict(base=self.BG, panel=self.BG, raised=self.TITLE[1], line=self.FRAME_IN,
                      line_dim=self.FRAME_IN_DIM, accent=self.ACCENT, accent_hi=self.ACCENT_HI,
                      text=T["dialog"], text_dim=T["title_inactive"], sel=self.SEL[0],
                      sel_text=T["menu_hilite"], danger=self.BTN["close_hover"][0], shadow=self.OUTER)
        grad = (f"background-image: linear-gradient(to right, {self.SEL[0]}, {self.SEL[1]}); "
                f"border: 0 0 0 3px; border-color: {self.SEL_EDGE}; border-radius: {self.SEL_RADIUS}px;")
        self.ROFI = dict(border_color=self.FRAME_IN, radius=getattr(self, "ROFI_RADIUS", 6), sel=grad,
                         **getattr(self, "ROFI_EXTRA_CFG", {}))

    @property
    def MATTE(self):
        return dict(title=self.TITLE[1], menu=self.MENU_BG, dialog=self.BG, popup=self.POPUP_BG)

    # ---- motif hooks (override per theme) -----------------------------------

    def ornament(self, active):
        """Drawn at the left of the title bar, x 4..44, y 0..title_h."""
        return ""

    def emblem_art(self, cx, cy, state):
        c = {"inactive": self.FRAME_IN_DIM, "active": self.ACCENT, "hover": self.ACCENT_HI}[state]
        return circle(cx, cy, 7, c)

    def corner_mark(self, x, y, active, which):
        return ""

    def check_mark(self, s, hover):
        return path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=self.ACCENT_HI if hover else self.ACCENT, sw=2)

    def radio_mark(self, s, hover):
        return circle(s / 2, s / 2, s / 2 - 3.2, self.ACCENT_HI if hover else self.ACCENT)

    def arrow_mark(self, x, m, hilite):
        return path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=self.TEXT["menu_hilite"] if hilite else self.ACCENT)

    def bubble_art(self, s, i):
        return sparkle(s / 2, s / 2, s / 2 - 0.3, [self.ACCENT, self.ACCENT_HI, self.POPUP_EDGE, self.ACCENT][i - 1])

    def menu_tile(self, w, h):
        return rect(0, 0, w, h, self.MENU_BG)

    # ---- title bar --------------------------------------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        top, bot = self.TITLE if active else self.TITLE_DIM
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, self.TITLE_HI if active else self.TITLE_DIM[0])
        if self.BAND2:
            b += rect(0, TH - 5 - dy, w, 2, self.BAND if active else self.BAND_DIM)
            b += rect(0, TH - 3 - dy, w, 2, self.BAND2 if active else self.BAND_DIM)
        else:
            b += rect(0, TH - 4 - dy, w, 3, self.BAND if active else self.BAND_DIM)
        b += rect(0, TH - 1 - dy, w, 1, self.OUTER)
        return title_grad(TH, dy, [(0, top), (1, bot)]) + self.GLOW, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        b += self.ornament(active)
        b += rect(w - 1, 0, 1, h, self.OUTER)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        defs, b = self._title_bg(w, True)
        b += rect(0, 0, 1, h, self.OUTER) + rect(w - 1, 0, 1, h, self.OUTER)
        b += self.emblem_art(12, h / 2 - 2, "active").replace('filter="url(#g)"', "")
        b += f'<g transform="translate({w},0) scale(-1,1)">' + self.emblem_art(12, h / 2 - 2, "active") + "</g>"
        return svg(w, h, b, defs)

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, self.OUTER)
        b += self.emblem_art(s / 2 + 1, s / 2 - 1.5, state)
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        key = "close_hover" if (kind == "close" and state == "hover") else state
        fill, rim, g = self.BTN[key]
        c = s / 2
        if state == "hover":
            b += circle(c, c, c - 1, fill, extra='opacity="0.7" filter="url(#g)"')
        if self.BTN_SHAPE == "square":
            b += rect(1.2, 1.2, s - 2.4, s - 2.4, fill, rim, 1.3, rx=3)
        elif self.BTN_SHAPE == "diamond":
            b += diamond(c, c, c - 0.8, c - 0.8, fill, rim, 1.3)
        else:
            b += circle(c, c, c - 1.3, fill, rim, 1.3)
        b += glyph(kind, s, g, 1.8, 6.2 if self.BTN_SHAPE == "diamond" else 6)
        return svg(s, s, b, defs)

    # ---- frame --------------------------------------------------------------------

    def _edge(self, active):
        return ((self.FRAME, self.OUTER, self.FRAME_IN) if active
                else (self.FRAME_DIM, self.OUTER, self.FRAME_IN_DIM))

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        b += self.corner_mark(10 if which == "left" else w - 10, h / 2 + 0.5, active, which)
        return svg(w, h, b)

    # ---- menus ----------------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, self.menu_tile(w, h))

    def menu_sel(self, w, h):
        r = self.SEL_RADIUS
        b = rect(2, 1, w - 4, h - 2, "url(#s)", rx=r) + rect(2, 1, 3, h - 2, self.SEL_EDGE, rx=1)
        b += rect(6, 1.5, w - 10, 1, "#ffffff", extra='opacity="0.25"')
        return svg(w, h, b, hgrad("s", [(0, self.SEL[0]), (1, self.SEL[1])]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        return base.replace("</svg>", self.arrow_mark(w - 15, h / 2, hilite) + "</svg>")

    # ---- dialogs ----------------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, self.BG))

    def area(self, w, h):
        return svg(w, h, frame(w, h, self.LINE, 1, rx=self.FRAME_RADIUS + 3, fill=self.BG_DK))

    def push_button(self, w, h, state):
        top, bot = self.TITLE
        fill, edge = {"normal": ("url(#b)", self.FRAME_IN), "hover": ("url(#b)", self.ACCENT_HI),
                      "clicked": (self.ACCENT, self.ACCENT_HI)}[state]
        b = rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=self.FRAME_RADIUS + 4)
        b += rect(4, 2, w - 8, 1, "#ffffff", extra='opacity="0.18"')
        return svg(w, h, b, vgrad("b", [(0, top), (1, bot)]))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, self.BG_DK, self.ACCENT_HI if hover else (self.CHECK_EDGE or self.FRAME_IN), 1, rx=2)
        if on:
            b += self.check_mark(s, hover)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, self.BG_DK, self.ACCENT_HI if hover else (self.CHECK_EDGE or self.FRAME_IN), 1)
        if on:
            b += self.radio_mark(s, hover)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, self.LINE))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, self.LINE, 1, rx=min(w, h) / 2, fill=self.BG_DK))

    def knob(self, w, h, vertical, clicked):
        g = hgrad("k", [(0, self.SEL[0]), (1, self.SEL[1])]) if not clicked else hgrad("k", [(0, self.ACCENT_HI), (1, self.ACCENT_HI)])
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", self.OUTER, 0.8, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, self.ACCENT) + circle(s / 2, s / 2, 1.8, self.ACCENT_FG))

    # ---- popups ------------------------------------------------------------------

    def tooltip(self, w, h):
        r = self.POPUP_RADIUS
        return svg(w, h, rect(0, 0, w, h, self.POPUP_EDGE, rx=r) + rect(1.5, 1.5, w - 3, h - 3, self.POPUP_BG, rx=r - 1)
                   + rect(1.5, h - 3.5, w - 3, 2, self.ACCENT))

    def popup(self, w, h):
        r = self.POPUP_RADIUS
        return svg(w, h, rect(0, 0, w, h, self.POPUP_EDGE, rx=r) + rect(1.5, 1.5, w - 3, h - 3, self.POPUP_BG, rx=r - 1))

    def popup_sel(self, w, h):
        r = self.POPUP_RADIUS
        return svg(w, h, rect(0, 0, w, h, self.POPUP_EDGE, rx=r) + rect(1.5, 1.5, w - 3, h - 3, "url(#s)", rx=r - 1),
                   hgrad("s", [(0, self.SEL[0]), (1, self.SEL[1])]))

    def bubble(self, s, i):
        return svg(s, s, self.bubble_art(s, i))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, self.SEL[0]), (1, self.SEL[1])]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, self.BG_DK))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, self.FRAME_IN) + rect(1, 1, w - 2, h - 2, self.TITLE[1])
                   + rect(1, 1, w - 2, 3, self.BAND))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, self.ACCENT_HI, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, self.BG))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, self.LINE, 1, rx=4, fill=self.BG_DK))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, self.BG, self.ACCENT))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, self.FRAME) + rect(w - 3, 0, 2, h, self.BAND) + rect(w - 1, 0, 1, h, self.OUTER))
        return svg(w, h, rect(0, 0, w, h, self.FRAME) + rect(0, h - 3, w, 2, self.BAND) + rect(0, h - 1, w, 1, self.OUTER))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
