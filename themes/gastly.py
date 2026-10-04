"""Gastly: lavender gas clouds with glowing white edges, a dark grinning ball, tongue-pink."""

from base import Art, circle, frame, path, rect, svg, vgrad
from themes._common import frame_bottom, frame_corner, frame_side, glyph, starfield, title_grad, tri_arrow

SPACE = "#2a1840"
SPACE_DK = "#180c28"
SPACE_XDK = "#0c0614"
NEBULA = "#462a65"
GAS = "#8a6a9a"
GAS_DK = "#6a4e7a"
GAS_LT = "#b89ac8"
EDGE = "#ffffff"
BODY = "#3a2438"
BODY_DK = "#1a0c1c"
TONGUE = "#db705e"
TONGUE_DK = "#a8463a"
FANG = "#f4f0f4"
DIM = "#3a2c4a"
DIM_DK = "#2a2038"


def gas_blobs(blobs, fill=GAS, edge=EDGE, ew=1.2):
    """A merged cloud: every blob's halo first, then every fill, so only the
    outer silhouette gets the white edge."""
    return ("".join(circle(x, y, r + ew, edge) for x, y, r in blobs)
            + "".join(circle(x, y, r, fill) for x, y, r in blobs))


def gastly_face(cx, cy, r):
    b = circle(cx, cy, r, BODY, BODY_DK, 0.8)
    b += path(f"M{cx - r * 0.62},{cy - r * 0.62} L{cx - r * 0.02},{cy - r * 0.08} L{cx - r * 0.6},{cy + r * 0.02} Z", fill=FANG)
    b += path(f"M{cx + r * 0.12},{cy - r * 0.12} L{cx + r * 0.72},{cy - r * 0.42} L{cx + r * 0.62},{cy + r * 0.12} Z", fill=FANG)
    b += circle(cx - r * 0.3, cy - r * 0.18, r * 0.09, BODY_DK) + circle(cx + r * 0.42, cy - r * 0.12, r * 0.09, BODY_DK)
    b += path(f"M{cx - r * 0.35},{cy + r * 0.2} L{cx - r * 0.2},{cy + r * 0.5} L{cx - r * 0.05},{cy + r * 0.24} Z", fill=FANG)
    b += f'<ellipse cx="{cx + r * 0.38}" cy="{cy + r * 0.55}" rx="{r * 0.5}" ry="{r * 0.36}" fill="{TONGUE}" stroke="{TONGUE_DK}" stroke-width="0.6"/>'
    return b


class Gastly(Art):
    NAME = "Gastly"
    WALLPAPER = "8/pokemon-gastly-ghost-type-desktop-wallpaper.jpg"
    BG_SOLID = SPACE

    P = dict(base=SPACE_DK, panel=SPACE_DK, raised=BODY, line=GAS_LT, line_dim=DIM,
             accent=GAS, accent_hi=GAS_LT, text="#efe6f4", text_dim="#8a7a9a",
             sel=GAS, sel_text="#ffffff", danger=TONGUE, shadow=SPACE_XDK)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=50, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans Black 9", menu="pango:Adwaita Sans SemiBold 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold 8")

    TEXT = dict(title_active="#ffffff", title_inactive="#9a8aaa", menu_title="#ffffff",
                menu="#e6dcef", menu_hilite="#ffffff", dialog="#e6dcef", tooltip="#ffffff")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    MENU_BG_TILE = 40
    CURSOR = (EDGE, BODY)
    MATTE = dict(title=GAS_DK, menu=SPACE, dialog=SPACE_DK, popup=GAS)
    ROFI = dict(border_color=GAS_LT, radius=10, sel=(
        "background-color: #8a6a9a; border: 2px; border-color: #ffffff; border-radius: 12px;"))

    # ---- window borders: a band of gas --------------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, GAS_LT), (0.35, GAS), (1, GAS_DK)] if active else [(0, DIM), (1, DIM_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1.5, EDGE if active else "#5a4a6a")                 # glowing edge
        b += rect(0, TH - 3 - dy, w, 2, BODY if active else "#1e1628")
        b += rect(0, TH - 1 - dy, w, 1, SPACE_XDK)
        return title_grad(TH, dy, stops), b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        blobs = [(8, 12, 5), (16, 9, 4), (14, 17, 3.5), (25, 13, 4.5), (34, 10, 3), (38, 16, 2.5), (45, 12, 1.8)]
        b += gas_blobs(blobs, SPACE if active else DIM_DK, EDGE if active else "#6a5a7a", 1)
        b += rect(w - 1, 0, 1, h, SPACE_XDK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1.5, EDGE)
        b += rect(0, h - 3, w, 2, BODY) + rect(0, h - 1, w, 1, SPACE_XDK)
        b += gas_blobs([(8, 11, 4), (15, 9, 3), (13, 15, 2.5)], SPACE, EDGE, 1)
        b += gas_blobs([(w - 8, 11, 4), (w - 15, 9, 3), (w - 13, 15, 2.5)], SPACE, EDGE, 1)
        return svg(w, h, b, vgrad("g", [(0, GAS_LT), (0.35, GAS), (1, GAS_DK)]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, SPACE_XDK)
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "inactive":
            b += circle(cx, cy, 8, DIM_DK, "#6a5a7a", 1) + circle(cx - 2.5, cy - 2, 1.5, "#8a7a9a") + circle(cx + 3, cy - 1.5, 1.5, "#8a7a9a")
        else:
            if state == "hover":
                b += circle(cx, cy, 10, TONGUE, extra='opacity="0.6" filter="url(#g)"')
            b += circle(cx, cy, 9.2, EDGE) + gastly_face(cx, cy, 8.2)
        return svg(s, s, b, defs + '<filter id="g"><feGaussianBlur stdDeviation="1.4"/></filter>')

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, ring, g = {"inactive": (DIM_DK, "#6a5a7a", "#9a8aaa"),
                         "active": (BODY, EDGE, EDGE),
                         "hover": (TONGUE, EDGE, EDGE),
                         "clicked": (GAS_LT, EDGE, BODY)}[state]
        c = s / 2
        b += circle(c, c, c - 1.2, fill, ring, 1.3)
        b += glyph(kind, s, g, 1.8, 6)
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (SPACE_DK, SPACE_XDK, GAS_LT) if active else (DIM_DK, SPACE_XDK, DIM)

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            x = 10 if which == "left" else w - 10
            b += gas_blobs([(x, h / 2 + 0.5, 2), (x + 3, h / 2, 1.4)], GAS, EDGE, 0.8)
        return svg(w, h, b)

    # ---- menus: deep space ---------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE) + starfield(w, h, 8, 9, ["#ffffff", GAS_LT, "#d8c8ff"], 0.8))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, GAS, EDGE, 1.4, rx=(h - 2) / 2)
                   + rect(10, 3, w - 20, 1.5, EDGE, extra='opacity="0.3"'))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 14, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=EDGE if hilite else TONGUE)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE_DK))

    def area(self, w, h):
        return svg(w, h, frame(w, h, NEBULA, 1, rx=6, fill=SPACE_XDK))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (BODY, GAS_LT), "hover": (BODY, TONGUE), "clicked": (GAS, EDGE)}[state]
        return svg(w, h, rect(0.7, 0.7, w - 1.4, h - 1.4, fill, edge, 1.4, rx=h / 2 - 1))

    def check(self, s, on, hover):
        b = rect(0.7, 0.7, s - 1.4, s - 1.4, SPACE_XDK, TONGUE if hover else GAS_LT, 1.2, rx=3)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=TONGUE, sw=2)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        if on:
            return svg(s, s, circle(c, c, c - 0.5, EDGE) + gastly_face(c, c, c - 1.4))
        return svg(s, s, circle(c, c, c - 0.7, SPACE_XDK, TONGUE if hover else GAS_LT, 1.2))

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, NEBULA))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, NEBULA, 1, rx=min(w, h) / 2, fill=SPACE_XDK))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0.7, 0.7, w - 1.4, h - 1.4, TONGUE if clicked else GAS, EDGE, 1.2, rx=min(w, h) / 2 - 0.7))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, GAS) + circle(s / 2, s / 2, 1.8, EDGE))

    # ---- popups: puffs of gas -------------------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, EDGE, rx=10) + rect(1.5, 1.5, w - 3, h - 3, GAS, rx=9))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, EDGE, rx=10) + rect(1.5, 1.5, w - 3, h - 3, TONGUE_DK, rx=9))

    def bubble(self, s, i):
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 0.5, EDGE) + circle(s / 2, s / 2, s / 2 - 1.8, GAS))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, TONGUE, rx=h / 2) + rect(3, 1, w - 6, 1.5, "#ffffff", extra='opacity="0.4"'))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, EDGE) + rect(1, 1, w - 2, h - 2, GAS) + rect(1, 1, w - 2, 3, BODY))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, TONGUE, 2, rx=2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SPACE_DK))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, NEBULA, 1, rx=6, fill=SPACE_XDK))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, SPACE_DK, GAS_LT))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, SPACE_DK) + rect(w - 2.5, 0, 1.5, h, GAS_LT) + rect(w - 1, 0, 1, h, SPACE_XDK))
        return svg(w, h, rect(0, 0, w, h, SPACE_DK) + rect(0, h - 2.5, w, 1.5, GAS_LT) + rect(0, h - 1, w, 1, SPACE_XDK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: gas puffing off the top and out of the right side ----

    SHAPE = dict(top=18, right=20)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def top(active):
            fill, edge = (GAS, EDGE) if active else (DIM, "#6a5a7a")
            blobs = [(8, T + 3, 7), (19, T - 3, 8), (31, T + 1, 6), (41, T - 5, 6), (50, T + 1, 4), (57, T - 3, 3)]
            return svg(62, T + 3, gas_blobs(blobs, fill, edge, 1.3))

        def side(active):
            fill, edge = (GAS, EDGE) if active else (DIM, "#6a5a7a")
            blobs = [(2, 8, 7), (11, 12, 6), (18, 6, 4), (4, 24, 8), (14, 29, 6), (21, 34, 3), (3, 42, 6), (11, 48, 4)]
            return svg(25, 56, gas_blobs(blobs, fill, edge, 1.3))

        return [("puffs", 62, T + 3, "tl", 0, 0, top),
                ("side", 25, 56, "tr", 0, T + 10, side)]
