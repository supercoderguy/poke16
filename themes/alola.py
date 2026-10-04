"""Alola: Solgaleo and Lunala - a sun-gold and moon-violet eclipse on deep navy."""

from base import Art, circle, frame, hgrad, path, rect, sparkle, svg, vgrad
from themes._common import burst, crescent, frame_bottom, frame_corner, frame_side, glyph, title_grad, tri_arrow

NAVY = "#0c0848"
NAVY_DK = "#06013c"
NAVY_LT = "#1a1666"
GOLD = "#f0d040"
GOLD_LT = "#f8e888"
WHITE = "#fbfaf2"
RED = "#d8402a"
PURPLE = "#3a2e8a"
VIOLET = "#5d3d91"
LAVENDER = "#9a9ae0"
SOLBLUE = "#2a4aa8"
DIM = "#1e1c40"
DIM_DK = "#141230"


def sun(cx, cy, r, ray=GOLD, disc=WHITE):
    """Solgaleo's mane as a sunburst."""
    return burst(cx, cy, r, 10, 0.6, ray) + circle(cx, cy, r * 0.5, disc)


class Alola(Art):
    NAME = "Alola"
    WALLPAPER = "10/wp1878295-pokemon-sun-and-moon-wallpapers.png"
    BG_SOLID = NAVY_DK

    P = dict(base=NAVY, panel=NAVY, raised=PURPLE, line=GOLD, line_dim="#3a3670",
             accent=GOLD, accent_hi=GOLD_LT, text="#e8e4ff", text_dim="#8a86b8",
             sel=GOLD, sel_text=NAVY_DK, danger=RED, shadow=NAVY_DK)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=46, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans ExtraBold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold 8")

    TEXT = dict(title_active=WHITE, title_inactive="#8a86b8", menu_title=WHITE,
                menu="#e8e4ff", menu_hilite=NAVY_DK, dialog="#e8e4ff", tooltip=NAVY_DK)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    CURSOR = (WHITE, PURPLE)
    MATTE = dict(title=NAVY_LT, menu=NAVY, dialog=NAVY, popup=WHITE)
    ROFI = dict(border_color=GOLD, radius=6, sel=(
        "background-image: linear-gradient(to right, #f0d040, #f8e888); "
        "border: 0 0 0 3px; border-color: #5d3d91; border-radius: 3px;"))

    # ---- window borders: night sky with a sun rule and a moon rule ----------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, NAVY_LT), (1, NAVY_DK)] if active else [(0, DIM), (1, DIM_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, TH - 4 - dy, w, 1.5, GOLD if active else "#4a4670")          # sun rule
        b += rect(0, TH - 2.5 - dy, w, 1.5, LAVENDER if active else "#33305a")    # moon rule
        b += rect(0, TH - 1 - dy, w, 1, "#020018")
        return title_grad(TH, dy, stops), b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:   # the eclipse: Lunala's crescent passing Solgaleo's sun
            b += sun(14, 10.5, 9) + crescent(26, 10.5, 8, LAVENDER, 0.5, 180)
            b += sparkle(38, 6, 2.5, GOLD_LT) + sparkle(36, 15, 1.6, LAVENDER)
        else:
            b += sun(14, 10.5, 9, "#4a4670", "#6a6690") + crescent(26, 10.5, 8, "#3a3866", 0.5, 180)
        b += rect(w - 1, 0, 1, h, "#020018")
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, h - 4, w, 1.5, GOLD) + rect(0, h - 2.5, w, 1.5, LAVENDER)
        b += sun(12, h / 2 - 2, 7) + crescent(w - 12, h / 2 - 2, 6.5, LAVENDER, 0.5, 180)
        return svg(w, h, b, vgrad("g", [(0, NAVY_LT), (1, NAVY_DK)]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        cx, cy = s / 2 + 1, s / 2 - 2
        if state == "inactive":
            b += burst(cx, cy, 9, 10, 0.65, "#4a4670") + circle(cx, cy, 5.5, DIM_DK)
        else:
            ray = GOLD_LT if state == "hover" else GOLD
            b += burst(cx, cy, 9.5, 10, 0.65, ray) + circle(cx, cy, 5.6, NAVY_DK)
            # Lunala's crescent rim lighting the edge of the eclipse
            b += crescent(cx, cy, 5.6, LAVENDER if state == "active" else "#ffffff", 0.72, 0)
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, g = {"inactive": (DIM, "#4a4670", "#8a86b8"),
                        "active": (WHITE, GOLD, NAVY_DK),
                        "hover": (RED if kind == "close" else GOLD, WHITE, WHITE if kind == "close" else NAVY_DK),
                        "clicked": (VIOLET, LAVENDER, WHITE)}[state]
        c = s / 2
        if state == "hover" and kind != "close":
            b += burst(c, c, c - 0.3, 12, 0.78, GOLD_LT)
        b += circle(c, c, c - 2, fill, rim, 1.3)
        b += glyph(kind, s, g, 1.8, 6.2)
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (NAVY_DK, "#020018", GOLD) if active else (DIM_DK, "#020018", "#3a3670")

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            b += sparkle(10 if which == "left" else w - 10, h / 2 + 0.5, 3, GOLD_LT if which == "left" else LAVENDER)
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, "url(#s)", rx=3) + rect(2, 1, 3, h - 2, VIOLET),
                   hgrad("s", [(0, GOLD), (1, GOLD_LT)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        spike = path(f"M{x},{m - 3.5} L{x + 8},{m} L{x},{m + 3.5} L{x + 2},{m} Z", fill=VIOLET if hilite else GOLD)
        return base.replace("</svg>", spike + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def area(self, w, h):
        return svg(w, h, frame(w, h, PURPLE, 1, rx=4, fill=NAVY_DK))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (PURPLE, GOLD), "hover": (VIOLET, GOLD_LT), "clicked": (SOLBLUE, WHITE)}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=4)
                   + rect(3, 2, w - 6, 1, "#ffffff", extra='opacity="0.2"'))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, NAVY_DK, GOLD_LT if hover else GOLD, 1, rx=2)
        if on:
            b += sparkle(s / 2, s / 2, s / 2 - 2, GOLD_LT)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, NAVY_DK, GOLD_LT if hover else GOLD, 1)
        if on:
            b += sun(c, c, c - 2.2)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 1, GOLD, extra='opacity="0.6"') + rect(0, h / 2, w, 1, LAVENDER, extra='opacity="0.6"'))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, PURPLE, 1, rx=min(w, h) / 2, fill=NAVY_DK))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, LAVENDER if clicked else GOLD, WHITE, 0.8, rx=min(w, h) / 2))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, GOLD) + circle(s / 2, s / 2, 2, WHITE))

    # ---- popups: Solgaleo white with a gold edge --------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, GOLD, rx=5) + rect(2, 2, w - 4, h - 4, WHITE, rx=4)
                   + rect(2, h - 4, w - 4, 2, LAVENDER))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, GOLD, rx=5) + rect(2, 2, w - 4, h - 4, WHITE, rx=4))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, VIOLET, rx=5) + rect(2, 2, w - 4, h - 4, GOLD, rx=4))

    def bubble(self, s, i):
        return svg(s, s, sparkle(s / 2, s / 2, s / 2 - 0.3, [GOLD, LAVENDER, GOLD_LT, LAVENDER][i - 1]))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, GOLD), (1, VIOLET)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY_DK))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, LAVENDER) + rect(1, 1, w - 2, h - 2, PURPLE) + rect(1, 1, w - 2, 3, GOLD))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, GOLD, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, PURPLE, 1, rx=4, fill=NAVY_DK))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, NAVY, GOLD))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, NAVY_DK) + rect(w - 3, 0, 1, h, GOLD) + rect(w - 2, 0, 1, h, LAVENDER))
        return svg(w, h, rect(0, 0, w, h, NAVY_DK) + rect(0, h - 3, w, 1, GOLD) + rect(0, h - 2, w, 1, LAVENDER))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: Solgaleo's sun rays fanning up behind the emblem, Lunala's crescent hanging off the right side ----

    SHAPE = dict(top=22, right=22)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def rays(active):
            import math
            gold, light = (GOLD, GOLD_LT) if active else ("#4a4670", "#6a6690")
            cx, cy = 16, T + 3
            b = ""
            for i in range(9):
                a = math.radians(180 + 10 + i * 20)
                tip = 22 if i % 2 == 0 else 15
                x1, y1 = cx + 6 * math.cos(a - 0.22), cy + 6 * math.sin(a - 0.22)
                x2, y2 = cx + 6 * math.cos(a + 0.22), cy + 6 * math.sin(a + 0.22)
                b += path(f"M{x1:.1f},{y1:.1f} L{cx + tip * math.cos(a):.1f},{cy + tip * math.sin(a):.1f} L{x2:.1f},{y2:.1f} Z",
                          fill=gold if i % 2 == 0 else light)
            return svg(40, T + 3, b)

        def moon(active):
            from themes._common import crescent
            c = LAVENDER if active else "#3a3866"
            return svg(27, 30, crescent(12, 15, 12, c, 0.5, 0) + (sparkle(22, 5, 2.4, GOLD_LT) if active else ""))

        return [("rays", 40, T + 3, "tl", 0, 0, rays),
                ("moon", 27, 30, "tr", 0, T + 10, moon)]
