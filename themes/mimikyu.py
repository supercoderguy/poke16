"""Mimikyu: the cream disguise cloth with its scribbled face, in a dappled sunlit forest."""

import math

from base import Art, circle, frame, hgrad, line, path, rect, svg, vgrad
from themes._common import frame_bottom, frame_corner, frame_side, glyph, title_grad, tri_arrow

CLOTH_LT = "#fbf4d8"
CLOTH = "#f2e8c4"
CLOTH_DK = "#d8c898"
SHADE = "#7a7460"          # the cloth in shadow (inactive)
SHADE_DK = "#5a5648"
INK = "#4a2a1a"            # scribbled-marker brown
BLUSH = "#e8887a"
TAIL = "#8a5a30"
BARK = "#2e2418"
BARK_DK = "#1a120a"
FOREST = "#1c2a1c"
FOREST_MID = "#2e4228"
LEAF = "#6a8a3a"
LEAF_LT = "#b8cc6a"
SUN = "#ffe882"


def spiral(cx, cy, r, colour, sw=1.2, turns=2.6):
    """Mimikyu's scribbled spiral eye."""
    pts = []
    for i in range(49):
        t = i / 48
        a = t * turns * 2 * math.pi
        rr = 0.6 + t * (r - 0.6)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a) * 1.1:.2f}")
    return path("M" + " L".join(pts), stroke=colour, sw=sw)


def zigzag_mouth(x, y, colour, sw=1.6):
    return path(f"M{x},{y + 3} L{x + 6},{y + 1} L{x + 9},{y + 5} L{x + 14},{y - 1} L{x + 17},{y + 4} L{x + 23},{y - 3}",
                stroke=colour, sw=sw)


def blush(x, y, colour):
    return "".join(line(x + i * 2.2, y + 4, x + i * 2.2 + 3, y, colour, 1.1, 'stroke-linecap="round"') for i in range(4))


def leaf(cx, cy, r, fill, rot=0):
    d = f"M{cx - r},{cy} Q{cx},{cy - r * 0.8} {cx + r},{cy} Q{cx},{cy + r * 0.8} {cx - r},{cy} Z"
    return f'<g transform="rotate({rot} {cx} {cy})">' + path(d, fill=fill) + "</g>"


class Mimikyu(Art):
    NAME = "Mimikyu"
    WALLPAPER = "7/mimikyu-shy-tree-hide-cute-pokemon-desktop-wallpaper-4k.jpg"
    BG_SOLID = FOREST

    P = dict(base=FOREST, panel=FOREST, raised=FOREST_MID, line=LEAF_LT, line_dim="#4a5040",
             accent=LEAF, accent_hi=SUN, text=CLOTH, text_dim="#8a8870",
             sel=SUN, sel_text=INK, danger=BLUSH, shadow=BARK_DK)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=48, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans Bold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans SemiBold 8")

    TEXT = dict(title_active=INK, title_inactive="#ddd5b4", menu_title=INK,
                menu="#ece4c4", menu_hilite="#3a2414", dialog="#ece4c4", tooltip=INK)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_NONE"
    MENU_BG_TILE = 32
    CURSOR = (CLOTH, INK)
    MATTE = dict(title=CLOTH, menu=FOREST, dialog=FOREST, popup=CLOTH)
    ROFI = dict(border_color=TAIL, radius=6, sel=(
        "background-image: linear-gradient(to right, #ffe882, #c8d878); "
        "border: 0 0 0 3px; border-color: #e8887a; border-radius: 4px;"))

    # ---- window borders: the disguise cloth -----------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, CLOTH_LT), (0.7, CLOTH), (1, CLOTH_DK)] if active else [(0, SHADE), (1, SHADE_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, TAIL if active else "#4a4638")
        b += rect(0, TH - 3 - dy, w, 2, TAIL if active else "#4a4638")      # hem
        b += rect(0, TH - 1 - dy, w, 1, BARK_DK)
        return title_grad(TH, dy, stops), b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        c = INK if active else "#c8c0a0"
        b += blush(4, 9, BLUSH if active else "#9a8a7a") + zigzag_mouth(16, 11, c)
        b += rect(w - 1, 0, 1, h, BARK_DK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, TAIL)
        b += rect(0, h - 3, w, 2, TAIL) + rect(0, h - 1, w, 1, BARK_DK)
        b += spiral(12, h / 2 - 1.5, 6, INK) + spiral(w - 12, h / 2 - 1.5, 6, INK)
        return svg(w, h, b, vgrad("g", [(0, CLOTH_LT), (0.7, CLOTH), (1, CLOTH_DK)]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, BARK_DK)
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "hover":
            b += circle(cx, cy, 8.5, BLUSH, extra='opacity="0.55"')
        b += spiral(cx, cy, 7.5, INK if state != "inactive" else "#c8c0a0", 1.3)
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, ring, g = {"inactive": (SHADE, "#c8c0a0", "#c8c0a0"),
                         "active": (CLOTH_LT, INK, INK),
                         "hover": (BLUSH, INK, "#ffffff"),
                         "clicked": (TAIL, INK, CLOTH_LT)}[state]
        c = s / 2
        b += circle(c, c, c - 1.4, fill)
        # a hand-drawn ring: two slightly offset passes of the marker
        b += circle(c, c, c - 1.4, "none", ring, 1.1) + circle(c + 0.4, c - 0.3, c - 1.8, "none", ring, 0.6)
        b += glyph(kind, s, g, 1.8, 6)
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (BARK, BARK_DK, LEAF_LT) if active else ("#2a2820", BARK_DK, "#5a5648")

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            b += leaf(10 if which == "left" else w - 10, h / 2 + 0.5, 4, LEAF_LT, -20 if which == "left" else 200)
        return svg(w, h, b)

    # ---- menus: dappled forest light ---------------------------------------

    def menu_bg(self, w, h):
        b = rect(0, 0, w, h, FOREST)
        for x, y, r, o in ((6, 8, 4, 0.10), (22, 20, 5, 0.08), (14, 28, 2.5, 0.12), (28, 4, 2, 0.12)):
            b += circle(x, y, r, SUN, extra=f'opacity="{o}"')
        return svg(w, h, b)

    def menu_sel(self, w, h):
        b = rect(2, 1, w - 4, h - 2, "url(#s)", rx=4) + rect(2, 1, 3, h - 2, BLUSH, rx=1)
        return svg(w, h, b, hgrad("s", [(0, SUN), (1, "#c8d878")]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=INK if hilite else LEAF_LT)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, FOREST))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#3a5030", 1, rx=4, fill="#16221a"))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (FOREST_MID, LEAF), "hover": (FOREST_MID, SUN), "clicked": (TAIL, CLOTH)}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=5)
                   + rect(4, 2, w - 8, 1, "#ffffff", extra='opacity="0.15"'))

    def check(self, s, on, hover):
        b = rect(0.6, 0.6, s - 1.2, s - 1.2, CLOTH, BLUSH if hover else INK, 1.1, rx=2)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=INK, sw=1.6)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, CLOTH, BLUSH if hover else INK, 1.1)
        if on:
            b += spiral(c, c, c - 2.5, INK, 1)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 1, "#0e160e") + rect(0, h / 2, w, 1, "#3a5030"))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#3a5030", 1, rx=min(w, h) / 2, fill="#101a10"))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, BLUSH if clicked else CLOTH, INK, 1, rx=min(w, h) / 2))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, CLOTH) + circle(s / 2, s / 2, 1.6, INK))

    # ---- popups: a scrap of the cloth ----------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, TAIL, rx=6) + rect(1.5, 1.5, w - 3, h - 3, CLOTH, rx=5))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, TAIL, rx=6) + rect(1.5, 1.5, w - 3, h - 3, SUN, rx=5))

    def bubble(self, s, i):
        return svg(s, s, leaf(s / 2, s / 2, s / 2 - 0.5, [LEAF_LT, LEAF, SUN, LEAF_LT][i - 1], 30 * i))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, LEAF), (1, SUN)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, FOREST))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, TAIL) + rect(1, 1, w - 2, h - 2, CLOTH) + rect(1, 1, w - 2, 3, CLOTH_DK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, SUN, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, FOREST))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#3a5030", 1, rx=4, fill="#16221a"))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, FOREST, LEAF_LT))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, BARK) + rect(w - 2, 0, 1, h, LEAF_LT) + rect(w - 1, 0, 1, h, BARK_DK))
        return svg(w, h, rect(0, 0, w, h, BARK) + rect(0, h - 2, w, 1, LEAF_LT) + rect(0, h - 1, w, 1, BARK_DK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: the disguise's floppy ear on top, its wooden tail out of the right side ----

    SHAPE = dict(top=26, right=20)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def ear(active):
            fill, edge = (CLOTH, INK) if active else (SHADE, SHADE_DK)
            # the drawn-on Pikachu ear: rises, then flops over at the tip
            d = (f"M8,{T + 3} C10,{T - 10} 16,8 26,3 C32,0 40,2 46,10 C40,8 34,9 30,13 "
                 f"C26,18 30,{T - 6} 34,{T + 3} Z")
            b = path(d, fill=fill, stroke=edge, sw=1.3)
            b += path("M46,10 C40,8 34,9 30,13 C34,10 40,9 46,10 Z", fill=edge)   # the scribbled black tip
            return svg(48, T + 3, b)

        def tail(active):
            fill, edge = (TAIL, BARK_DK) if active else (SHADE_DK, BARK_DK)
            d = "M0,22 L10,18 L6,12 L18,6 L15,1 L25,0 L22,9 L13,12 L17,18 L5,26 L0,30 Z"
            return svg(25, 31, path(d, fill=fill, stroke=edge, sw=1.1))

        return [("ear", 48, T + 3, "tl", 4, 0, ear),
                ("tail", 25, 31, "tr", 0, T + 60, tail)]
