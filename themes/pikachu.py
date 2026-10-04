"""Pikachu: electric yellow, black-tipped ears, red cheek buttons, a lightning tail, back stripes."""

from base import Art, circle, frame, path, rect, svg, vgrad
from themes._common import plump_ear, frame_bottom, frame_corner, frame_side, glyph, title_grad, tri_arrow

YELLOW_LT = "#fff176"
YELLOW = "#ffe200"
YELLOW_DK = "#f0b800"
AMBER = "#e89a00"
CHEEK = "#fe4224"
CHEEK_LT = "#ff6a4a"
CHEEK_DK = "#c02a14"
BLACK = "#221e07"
BROWN = "#9c4204"
CREAM = "#fff8d0"
WHITE = "#ffffff"
PALE = "#f4ecc0"          # inactive
PALE_DK = "#e0d4a0"
TAN = "#b8a870"


def ear(base1, base2, tip, fill=YELLOW, tipc=BLACK, edge=BLACK, frac=0.38):
    """A long ear with a black tip covering the top `frac` of it."""
    (x1, y1), (x2, y2), (tx, ty) = base1, base2, tip
    a = (tx + (x1 - tx) * frac, ty + (y1 - ty) * frac)
    b = (tx + (x2 - tx) * frac, ty + (y2 - ty) * frac)
    out = path(f"M{x1},{y1} Q{(x1 + tx) / 2 - 1},{(y1 + ty) / 2} {tx},{ty} Q{(x2 + tx) / 2 + 1},{(y2 + ty) / 2} {x2},{y2} Z",
               fill=fill, stroke=edge, sw=0.9)
    return out + path(f"M{a[0]:.2f},{a[1]:.2f} L{tx},{ty} L{b[0]:.2f},{b[1]:.2f} Z", fill=tipc)


def bolt_tail(x, y, fill=YELLOW, edge=BLACK, base=BROWN):
    """Pikachu's lightning-bolt tail, lying along the title bar."""
    d = (f"M{x},{y + 12} L{x + 9},{y + 7} L{x + 7},{y + 4} L{x + 20},{y} L{x + 18},{y - 4} "
         f"L{x + 34},{y - 6} L{x + 26},{y + 1} L{x + 28},{y + 3} L{x + 14},{y + 10} L{x + 16},{y + 13} L{x + 3},{y + 15} Z")
    return path(d, fill=fill, stroke=edge, sw=0.9) + path(f"M{x},{y + 12} L{x + 3},{y + 15} L{x + 6},{y + 13} L{x + 4},{y + 10} Z", fill=base)


def bolt_small(cx, cy, k, fill=YELLOW, edge=BLACK):
    d = (f"M{cx - 1 * k},{cy - 5 * k} L{cx + 3 * k},{cy - 5 * k} L{cx + 1 * k},{cy - 1 * k} L{cx + 3.5 * k},{cy - 1 * k} "
         f"L{cx - 1.5 * k},{cy + 5.5 * k} L{cx},{cy + 0.5 * k} L{cx - 2.5 * k},{cy + 0.5 * k} Z")
    return path(d, fill=fill, stroke=edge, sw=0.7)


class Pikachu(Art):
    NAME = "Pikachu"
    WALLPAPER = "14/wp2403365-pikachu-hd-wallpapers.png"
    BG_SOLID = YELLOW

    P = dict(base=CREAM, panel=CREAM, raised=YELLOW, line=BLACK, line_dim=TAN,
             accent=CHEEK, accent_hi=AMBER, text=BLACK, text_dim=TAN,
             sel=CHEEK, sel_text=WHITE, danger=CHEEK, shadow=CREAM)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=44, menu_title_h=24, menu_item_pad=(12, 22, 3, 3))

    FONTS = dict(border="pango:Adwaita Sans Black 9", menu="pango:Adwaita Sans SemiBold 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold 8")

    TEXT = dict(title_active=BLACK, title_inactive="#8a7a50", menu_title=BLACK,
                menu="#3a2a08", menu_hilite=WHITE, dialog="#3a2a08", tooltip=BLACK)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_NONE"
    MENU_BG_TILE = 24
    CURSOR = (YELLOW, BLACK)
    MATTE = dict(title=YELLOW, menu=CREAM, dialog=CREAM, popup=WHITE)
    ROFI = dict(border_color=BLACK, radius=10, sel=(
        "background-color: #fe4224; border: 2px; border-color: #c02a14; border-radius: 12px;"))

    # ---- shape: ears above the title bar, the bolt tail out of the right side ----

    SHAPE = dict(top=30, right=26)      # right margin + 5px frame = the tail's width

    def decorations(self):
        T = self.SHAPE["top"]

        def ears(active):
            kw = {} if active else dict(fill=PALE_DK, tipc=TAN, edge=TAN)
            # long, leaf-shaped ears leaning outward; bases sink into the title bar's top edge
            b = plump_ear((12, T + 3), (28, T + 3), (3, 2), "l", **kw)
            b += plump_ear((40, T + 3), (56, T + 3), (66, 3), "r", **kw)
            return svg(70, T + 3, b)

        def tail(active):
            fill, edge, base = (YELLOW, BLACK, BROWN) if active else (PALE_DK, TAN, TAN)
            # the lightning-bolt tail: brown root inside the frame, zigzagging up and out
            d = ("M0,38 L12,31 L7,23 L21,16 L16,9 L30,1 L30,13 L24,16 L29,23 L14,32 L19,37 L0,48 Z")
            b = path(d, fill=fill, stroke=edge, sw=1.2)
            b += path("M0,38 L6,35 L7,45 L0,48 Z", fill=base, stroke=edge, sw=0.8)
            return svg(31, 49, b)

        return [("ears", 70, T + 3, "tl", 8, 0, ears),
                ("tail", 31, 49, "tr", 0, T + 30, tail)]

    # ---- window borders: Pikachu's back ----------------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, YELLOW_LT), (0.5, YELLOW), (1, YELLOW_DK)] if active else [(0, PALE), (1, PALE_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, BLACK if active else TAN)
        b += rect(0, TH - 3 - dy, w, 2, BROWN if active else TAN)
        b += rect(0, TH - 1 - dy, w, 1, BLACK if active else TAN)
        return title_grad(TH, dy, stops), b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += bolt_tail(4, 7)
        else:
            b += bolt_tail(4, 7, PALE_DK, TAN, TAN)
        b += rect(w - 1, 0, 1, h, BLACK if active else TAN)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, BLACK)
        b += rect(0, h - 3, w, 2, BROWN) + rect(0, h - 1, w, 1, BLACK)
        b += rect(0, 0, 1, h, BLACK) + rect(w - 1, 0, 1, h, BLACK)
        b += bolt_small(11, h / 2 - 1.5, 1.4) + bolt_small(w - 11, h / 2 - 1.5, 1.4)
        return svg(w, h, b, vgrad("g", [(0, YELLOW_LT), (0.5, YELLOW), (1, YELLOW_DK)]))

    def emblem(self, s, state):
        """A red cheek (the ears now stand up above the title bar)."""
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, BLACK if state != "inactive" else TAN)
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "inactive":
            return svg(s, s, b + circle(cx, cy, 7, PALE_DK, TAN, 1), defs)
        if state == "hover":   # sparks off the cheek
            for x1, y1, x2, y2 in ((2, 4, 5, 7), (s - 2, 4, s - 5, 7), (2, s - 8, 5, s - 10)):
                b += path(f"M{x1},{y1} L{x2},{y2}", stroke=AMBER, sw=1.3)
        b += circle(cx, cy, 7.5, CHEEK, CHEEK_DK, 1.2) + circle(cx - 2.5, cy - 2.5, 2, WHITE, extra='opacity="0.5"')
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        """The red cheeks."""
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, g = {"inactive": (PALE_DK, TAN, "#8a7a50"),
                        "active": (CHEEK, CHEEK_DK, WHITE),
                        "hover": (CHEEK_LT, BLACK, WHITE),
                        "clicked": (CHEEK_DK, BLACK, YELLOW_LT)}[state]
        c = s / 2
        b += circle(c, c, c - 1.2, fill, rim, 1.2)
        if state in ("active", "hover"):
            b += circle(c - 3, c - 3.5, 1.6, WHITE, extra='opacity="0.45"')
        if state == "hover":
            for x1, y1, x2, y2 in ((1, 3, 3, 5), (s - 1, 3, s - 3, 5), (1, s - 3, 3, s - 5)):
                b += path(f"M{x1},{y1} L{x2},{y2}", stroke=AMBER, sw=1.2)
        b += glyph(kind, s, g, 2, 6)
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (YELLOW, BLACK, BROWN) if active else (PALE, TAN, PALE_DK)

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:   # the two brown stripes on Pikachu's back
            x = 8 if which == "left" else w - 16
            b += rect(x, 2, 3, h - 3, BROWN, rx=1) + rect(x + 5, 2, 3, h - 3, BROWN, rx=1)
        return svg(w, h, b)

    # ---- menus: cream with a faint cell pattern -----------------------------------

    def menu_bg(self, w, h):
        b = rect(0, 0, w, h, CREAM)
        for x, y in ((4, 5), (16, 14), (8, 19), (20, 3)):
            b += path(f"M{x},{y - 2.5} L{x + 2.5},{y - 1} L{x + 2},{y + 2} L{x - 1},{y + 2.5} L{x - 2.5},{y} Z",
                      fill="none", stroke="#fbe58a", sw=0.8)
        return svg(w, h, b)

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, CHEEK, CHEEK_DK, 1, rx=(h - 2) / 2)
                   + rect(9, 2.5, w - 18, 1.5, WHITE, extra='opacity="0.35"'))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=WHITE if hilite else BLACK)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CREAM))

    def area(self, w, h):
        return svg(w, h, frame(w, h, YELLOW_DK, 1.2, rx=6, fill=WHITE))

    def push_button(self, w, h, state):
        top, bot, edge = {"normal": (YELLOW_LT, YELLOW, BLACK), "hover": (YELLOW_LT, YELLOW_DK, CHEEK),
                          "clicked": (YELLOW_DK, AMBER, BLACK)}[state]
        return svg(w, h, rect(0.6, 0.6, w - 1.2, h - 1.2, "url(#g)", edge, 1.2, rx=h / 2 - 1)
                   + rect(7, 2.5, w - 14, 1.5, WHITE, extra='opacity="0.6"'),
                   vgrad("g", [(0, top), (1, bot)]))

    def check(self, s, on, hover):
        b = rect(0.6, 0.6, s - 1.2, s - 1.2, WHITE, CHEEK if hover else BLACK, 1.2, rx=3)
        if on:
            b += bolt_small(s / 2, s / 2, 1.05)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, WHITE, CHEEK if hover else BLACK, 1.2)
        if on:
            b += circle(c, c, c - 3, CHEEK) + circle(c - 1.3, c - 1.3, 1, WHITE, extra='opacity="0.5"')
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 2, YELLOW_DK))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, BLACK, 1, rx=min(w, h) / 2, fill=WHITE))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0.6, 0.6, w - 1.2, h - 1.2, CHEEK if clicked else YELLOW, BLACK, 1.2, rx=min(w, h) / 2 - 0.6))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, YELLOW) + circle(s / 2, s / 2, 2, CHEEK))

    # ---- popups ------------------------------------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK, rx=7) + rect(2, 2, w - 4, h - 4, WHITE, rx=6)
                   + rect(2, h - 5, w - 4, 3, YELLOW))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK, rx=7) + rect(2, 2, w - 4, h - 4, WHITE, rx=6))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK, rx=7) + rect(2, 2, w - 4, h - 4, CHEEK, rx=6))

    def bubble(self, s, i):
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 0.5, BLACK) + circle(s / 2, s / 2, s / 2 - 1.8, YELLOW))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, YELLOW, BLACK, 1, rx=h / 2))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, YELLOW))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLACK) + rect(1, 1, w - 2, h - 2, WHITE) + rect(1, 1, w - 2, 3, YELLOW_DK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, CHEEK, 2, rx=2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CREAM))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, YELLOW_DK, 1.2, rx=6, fill=WHITE))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, CREAM, BLACK))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, YELLOW) + rect(w - 3, 0, 2, h, BROWN) + rect(w - 1, 0, 1, h, BLACK))
        return svg(w, h, rect(0, 0, w, h, YELLOW) + rect(0, h - 3, w, 2, BROWN) + rect(0, h - 1, w, 1, BLACK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
