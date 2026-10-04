"""Umbreon: gold line-art on black, moon-phase buttons, red-eye highlights."""

from base import Art, circle, frame, line, path, rect, sparkle, svg, vgrad
from themes._common import plump_ear

BLACK = "#050505"
PANEL = "#0c0b0d"
RAISED = "#17141a"
GOLD = "#c69246"
GOLD_HI = "#f0c274"
GOLD_DIM = "#5a4326"
RED = "#e0122c"
RED_HI = "#ff3b55"


def moon(cx, cy, r, phase, fill):
    """Moon-phase glyph: crescent | full | half (lit on the right)."""
    if phase == "full":
        return circle(cx, cy, r, fill)
    if phase == "half":
        return path(f"M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} Z", fill=fill)
    # crescent: outer right arc, back along a flatter inner arc
    return path(f"M{cx},{cy - r} A{r},{r} 0 1 1 {cx},{cy + r} "
                f"A{r * 0.55},{r} 0 1 0 {cx},{cy - r} Z", fill=fill)


class Umbreon(Art):
    NAME = "Umbreon"
    WALLPAPER = "6/wp10646924-1609250659.jpg"
    BG_SOLID = BLACK

    P = dict(base=PANEL, panel=PANEL, raised=RAISED, line=GOLD, line_dim=GOLD_DIM,
             accent=GOLD, accent_hi=GOLD_HI, text=GOLD_HI, text_dim=GOLD_DIM,
             sel=RAISED, sel_text="#fff0d0", danger=RED, shadow=BLACK)

    M = dict(Art.M, title_h=26, side=5, bottom=6, corner=24, btn=16, btn_gap=5, btn_right=8,
             title_edge=(24, 24), menu_title_h=24)

    FONTS = dict(border="pango:DejaVu Serif Bold 9", menu="pango:DejaVu Serif 9",
                 dialog="pango:DejaVu Serif 9", small="pango:DejaVu Serif Bold 8")

    TEXT = dict(title_active="#e8b86a", title_inactive="#7a6038", menu_title=GOLD_HI,
                menu="#d8a85e", menu_hilite="#fff0d0", dialog="#dcb37a", tooltip="#e8b86a")
    CURSOR = (GOLD_HI, BLACK)
    ROFI = dict(border_color=GOLD, radius=0, title_pad=22, sel=(
        "background-image: linear-gradient(to right, rgba(198,146,70,40%), rgba(198,146,70,3%)); "
        "border: 0 0 1px 2px; border-color: #f0c274;"))
    MATTE = dict(title=BLACK, menu=BLACK, dialog=PANEL, popup=BLACK)

    # Everything shares one outer gold hairline, 1.5px in from the window edge.
    O = 1.5

    def _c(self, active):
        return GOLD if active else GOLD_DIM

    # ---- window borders -----------------------------------------------------

    def title(self, w, h, active):
        c, o = self._c(active), self.O
        b = rect(0, 0, w, h, BLACK)
        b += line(0, o, w, o, c)                                  # outer frame, top
        b += line(w - o, o, w - o, h, c)                          # outer frame, right end
        b += line(0, h - 4.5, w - 4, h - 4.5, c)                  # double rule under title
        b += line(0, h - 2.5, w - 4, h - 2.5, c, extra='opacity="0.55"')
        if active:
            b += sparkle(12, h / 2 - 1.5, 4.5, GOLD_HI)
            b += circle(4, h / 2 - 1.5, 1, GOLD)
        return svg(w, h, b)

    def menu_title(self, w, h):
        o = self.O
        b = rect(0, 0, w, h, BLACK)
        b += line(0, o, w, o, GOLD) + line(o, o, o, h, GOLD) + line(w - o, o, w - o, h, GOLD)
        b += line(0, h - 3.5, w, h - 3.5, GOLD) + line(0, h - 1.5, w, h - 1.5, GOLD, extra='opacity="0.55"')
        b += sparkle(12, h / 2 - 1, 4.5, GOLD_HI) + sparkle(w - 12, h / 2 - 1, 4.5, GOLD_HI)
        return svg(w, h, b)

    # ---- shape: Umbreon's tall ears, gold-ringed, rising above the title bar ----

    SHAPE = dict(top=42)

    def decorations(self):
        T = self.SHAPE["top"]

        def ears(active):
            c, band = (GOLD, GOLD_HI) if active else (GOLD_DIM, GOLD_DIM)
            kw = dict(fill=BLACK, tipc=BLACK, edge=c, band=band, band_at=0.5, band_w=3.4, sw=1.3,
                      bulge=0.17)
            b = plump_ear((10, T + 3), (25, T + 3), (2, 1), "l", **kw)
            b += plump_ear((35, T + 3), (50, T + 3), (60, 2), "r", **kw)
            return svg(64, T + 3, b)

        return [("ears", 64, T + 3, "tl", 0, 0, ears)]

    def emblem(self, s, state):
        """Line-art Poke Ball, as dotted along the wallpaper's chevrons."""
        c = {"inactive": GOLD_DIM, "active": GOLD, "hover": RED_HI}[state]
        fc = self._c(state != "inactive")
        o = self.O
        b = rect(0, 0, s, s, BLACK)
        b += line(o, o, s, o, fc) + line(o, o, o, s, fc)
        b += line(o, s - 4.5, s, s - 4.5, fc) + line(o, s - 2.5, s, s - 2.5, fc, extra='opacity="0.55"')
        cx, cy, r = s / 2 + 1, s / 2 - 1.5, 6.5
        if state == "hover":
            b += circle(cx, cy, r + 1, RED, extra='opacity="0.4" filter="url(#g)"')
        b += circle(cx, cy, r, BLACK, c, 1.3)
        b += line(cx - r, cy, cx - 2.2, cy, c, 1.3) + line(cx + 2.2, cy, cx + r, cy, c, 1.3)
        b += circle(cx, cy, 1.9, BLACK, c, 1.3)
        return svg(s, s, b, '<filter id="g"><feGaussianBlur stdDeviation="1.4"/></filter>')

    def button(self, kind, s, state):
        phase = {"iconify": "crescent", "max": "full", "close": "half"}[kind]
        ring = {"inactive": GOLD_DIM, "active": GOLD, "hover": GOLD_HI, "clicked": RED}[state]
        fill = {"inactive": GOLD_DIM, "active": GOLD, "hover": RED_HI, "clicked": RED}[state]
        cx = cy = s / 2
        b = ""
        if state == "hover":
            b += circle(cx, cy, s / 2 - 1.5, RED, extra='opacity="0.35" filter="url(#g)"')
        b += circle(cx, cy, s / 2 - 1, BLACK, ring, 1.2)
        b += moon(cx, cy, s / 2 - 3.6, phase, fill)
        return svg(s, s, b, '<filter id="g"><feGaussianBlur stdDeviation="1.2"/></filter>')

    def side(self, w, h, active, which):
        x = self.O if which == "left" else w - self.O
        return svg(w, h, rect(0, 0, w, h, BLACK) + line(x, 0, x, h, self._c(active)))

    def bottom(self, w, h, active):
        return svg(w, h, rect(0, 0, w, h, BLACK) + line(0, h - self.O, w, h - self.O, self._c(active)))

    def corner(self, w, h, active, which):
        c, o = self._c(active), self.O
        x = o if which == "left" else w - o
        d = f"M{x},0 L{x},{h - o} L{w - x},{h - o}" if which == "left" else f"M{x},0 L{x},{h - o} L0,{h - o}"
        b = rect(0, 0, w, h, BLACK) + path(d, stroke=c, sw=1)
        # small gold stud where the frame turns the corner
        b += circle(o + 1.5 if which == "left" else w - o - 1.5, h - o - 1.5, 1.6, c)
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK))

    def menu_sel(self, w, h):
        defs = ('<linearGradient id="s" x1="0" y1="0" x2="1" y2="0">'
                f'<stop offset="0" stop-color="{GOLD}" stop-opacity="0.38"/>'
                f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0.04"/></linearGradient>')
        b = rect(2, 1, w - 4, h - 2, "url(#s)") + rect(2, 1, 2, h - 2, GOLD_HI)
        b += line(4, h - 1.5, w - 2, h - 1.5, GOLD, extra='opacity="0.5"')
        return svg(w, h, b, defs)

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        c = GOLD_HI if hilite else GOLD
        x, m = w - 16, h / 2
        # double chevron, as in the wallpaper's V bands
        chev = (path(f"M{x},{m - 4} L{x + 4},{m} L{x},{m + 4}", stroke=c, sw=1.2)
                + path(f"M{x + 4},{m - 4} L{x + 8},{m} L{x + 4},{m + 4}", stroke=RED_HI if hilite else c, sw=1.2))
        return base.replace("</svg>", chev + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PANEL))

    def area(self, w, h):
        b = frame(w, h, GOLD_DIM, 1, fill=BLACK)
        for x, y in ((3.5, 3.5), (w - 3.5, 3.5), (3.5, h - 3.5), (w - 3.5, h - 3.5)):
            b += circle(x, y, 1, GOLD)
        return svg(w, h, b)

    def push_button(self, w, h, state):
        st = {"normal": GOLD, "hover": GOLD_HI, "clicked": RED}[state]
        fill = {"normal": BLACK, "hover": RAISED, "clicked": "#2a0a10"}[state]
        b = frame(w, h, st, 1, fill=fill)
        b += rect(2.5, 2.5, w - 5, h - 5, "none", st, 0.6, extra='opacity="0.5"')
        return svg(w, h, b)

    def check(self, s, on, hover):
        b = frame(s, s, GOLD_HI if hover else GOLD, 1, fill=BLACK)
        if on:
            b += sparkle(s / 2, s / 2, s / 2 - 2.5, RED_HI if hover else GOLD_HI)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        b = circle(s / 2, s / 2, s / 2 - 1, BLACK, GOLD_HI if hover else GOLD, 1)
        if on:
            b += moon(s / 2, s / 2, s / 2 - 3.5, "full", RED_HI if hover else GOLD_HI)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, line(0, h / 2, w, h / 2, GOLD_DIM))

    def trough(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, BLACK) + line(w / 2, 0, w / 2, h, GOLD_DIM, 1.5))
        return svg(w, h, rect(0, 0, w, h, BLACK) + line(0, h / 2, w, h / 2, GOLD_DIM, 1.5))

    def knob(self, w, h, vertical, clicked):
        c = RED_HI if clicked else GOLD
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, BLACK, c, 1, rx=min(w, h) / 2)
                   + rect(3, 3, w - 6, h - 6, c, rx=(min(w, h) - 6) / 2))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, GOLD) + sparkle(s / 2, s / 2, s / 2, GOLD_HI))

    # ---- popups ------------------------------------------------------------

    def tooltip(self, w, h):
        b = frame(w, h, GOLD, 1, fill=BLACK) + rect(3.5, 3.5, w - 7, h - 7, "none", GOLD_DIM, 0.8)
        return svg(w, h, b)

    def bubble(self, s, i):
        return svg(s, s, sparkle(s / 2, s / 2, s / 2 - 0.5, GOLD_HI if i < 3 else GOLD))

    def popup_sel(self, w, h):
        return svg(w, h, frame(w, h, RED_HI, 1, fill="#1f0a0f") + rect(3.5, 3.5, w - 7, h - 7, "none", GOLD, 0.8))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, GOLD) + line(0, 1.5, w, 1.5, GOLD_HI))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK))

    def pager_win(self, w, h):
        return svg(w, h, frame(w, h, GOLD_DIM, 1, fill=RAISED))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, GOLD_HI, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, GOLD_DIM, 1, fill=BLACK))

    def arrow(self, s, direction):
        d = {"up": f"M4,{s-5} L{s/2},5 L{s-4},{s-5}", "down": f"M4,5 L{s/2},{s-5} L{s-4},5",
             "left": f"M{s-5},4 L5,{s/2} L{s-5},{s-4}", "right": f"M5,4 L{s-5},{s/2} L5,{s-4}"}[direction]
        return svg(s, s, rect(0, 0, s, s, BLACK) + path(d, stroke=GOLD, sw=1.2))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, BLACK) + line(w - 1.5, 0, w - 1.5, h, GOLD))
        return svg(w, h, rect(0, 0, w, h, BLACK) + line(0, h - 1.5, w, h - 1.5, GOLD))

    def startup_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK) + line(0, h - 1.5, w, h - 1.5, GOLD))
