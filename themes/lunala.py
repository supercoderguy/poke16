"""Lunala: deep purple wings ribbed in silver, a gold crescent head, nebula light."""

from base import Art, circle, frame, hgrad, path, rect, sparkle, svg, vgrad
from themes._common import crescent, diamond, frame_bottom, frame_corner, frame_side, glyph, starfield, title_grad, tri_arrow

WING = "#3b267e"
WING_DK = "#24165a"
WING_XDK = "#140c38"
NIGHT = "#1a1046"
NEB_BLUE = "#3c8ae0"
NEB_VIOLET = "#7a4ab8"
NEB_PINK = "#c3559b"
SILVER = "#e4e8f4"
SILVER_DK = "#a5afcd"
CRESCENT = "#c8c870"
CRESCENT_DK = "#8a8a40"
EYE = "#e0306a"
VISOR = "#3a2a7a"
DIM = "#2e2a48"
DIM_DK = "#1e1a34"


def lunala_head(cx, cy, r, gold=CRESCENT, visor=VISOR, eye=EYE):
    """The crescent crown (horns up) cradling a dark visor with a pink glint."""
    b = crescent(cx, cy, r, gold, 0.25, -90)
    b += circle(cx, cy + r * 0.12, r * 0.5, visor, gold, 0.8)
    b += diamond(cx + r * 0.12, cy + r * 0.16, r * 0.22, r * 0.15, eye)
    return b


class Lunala(Art):
    NAME = "Lunala"
    WALLPAPER = "11/wp2018670-lunala-wallpapers.jpg"
    BG_SOLID = WING_XDK

    P = dict(base=NIGHT, panel=NIGHT, raised=WING, line=SILVER_DK, line_dim="#3a3466",
             accent=NEB_PINK, accent_hi=SILVER, text="#e0dcff", text_dim="#9a90c8",
             sel=NEB_VIOLET, sel_text="#ffffff", danger=EYE, shadow=WING_XDK)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=40, menu_title_h=24)

    FONTS = dict(border="pango:DejaVu Serif Bold 9", menu="pango:DejaVu Sans 9",
                 dialog="pango:DejaVu Sans 9", small="pango:DejaVu Sans Bold 8")

    TEXT = dict(title_active="#f4f6ff", title_inactive="#9a90c8", menu_title="#f4f6ff",
                menu="#e0dcff", menu_hilite="#ffffff", dialog="#e0dcff", tooltip=WING_DK)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    MENU_BG_TILE = 40
    CURSOR = (SILVER, WING)
    MATTE = dict(title=WING, menu=WING_XDK, dialog=NIGHT, popup=SILVER)
    ROFI = dict(border_color=SILVER_DK, radius=8, sel=(
        "background-image: linear-gradient(to right, #3c8ae0, #7a4ab8, #c3559b); "
        "border: 0 0 0 2px; border-color: #c8c870; border-radius: 4px;"))

    # ---- window borders: a wing, ribbed in silver --------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = [(0, "#4a32a0"), (0.6, WING), (1, WING_DK)] if active else [(0, DIM), (1, DIM_DK)]
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 2, SILVER if active else "#4a4668")                  # wing rib
        b += rect(0, TH - 3 - dy, w, 2, "url(#neb)" if active else "#3a3466")       # nebula strip
        b += rect(0, TH - 1 - dy, w, 1, WING_XDK)
        defs = title_grad(TH, dy, stops) + hgrad("neb", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)])
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += crescent(14, 11, 7.5, CRESCENT, 0.35, 180)
            b += sparkle(26, 7, 2.6, SILVER) + sparkle(31, 15, 1.8, NEB_PINK) + circle(22, 15, 0.8, SILVER)
        else:
            b += crescent(14, 11, 7.5, "#5a5878", 0.35, 180)
        b += rect(w - 1, 0, 1, h, WING_XDK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 2, SILVER)
        b += rect(0, h - 3, w, 2, "url(#neb)") + rect(0, h - 1, w, 1, WING_XDK)
        b += crescent(12, h / 2, 6.5, CRESCENT, 0.35, 180) + crescent(w - 12, h / 2, 6.5, CRESCENT, 0.35, 0)
        return svg(w, h, b, vgrad("g", [(0, "#4a32a0"), (0.6, WING), (1, WING_DK)])
                   + hgrad("neb", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "inactive":
            b += lunala_head(cx, cy, 8.5, "#5a5878", DIM_DK, "#6a5a7a")
        else:
            if state == "hover":
                b += circle(cx, cy, 9, NEB_PINK, extra='opacity="0.6" filter="url(#g)"')
            b += lunala_head(cx, cy, 8.5)
        return svg(s, s, b, defs + '<filter id="g"><feGaussianBlur stdDeviation="1.5"/></filter>')

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, g = {"inactive": (DIM_DK, "#5a5878", "#8a86a8"),
                        "active": (WING_XDK, SILVER, SILVER),
                        "hover": ("url(#bh)", SILVER, "#ffffff"),
                        "clicked": (CRESCENT_DK, SILVER, "#ffffff")}[state]
        if kind == "close" and state == "hover":
            fill = EYE
        defs += hgrad("bh", [(0, NEB_BLUE), (1, NEB_PINK)])
        c = s / 2
        b += circle(c, c, c - 1.4, fill, rim, 1.3)
        b += glyph(kind, s, g, 1.7, 6.2)
        return svg(s, s, b, defs)

    def _edge(self, active):
        # the silver rib runs along the outside of the wing
        return (WING_DK, SILVER, CRESCENT) if active else (DIM_DK, "#4a4668", "#3a3466")

    def side(self, w, h, active, which):
        return svg(w, h, frame_side(w, h, which, *self._edge(active)))

    def bottom(self, w, h, active):
        return svg(w, h, frame_bottom(w, h, *self._edge(active)))

    def corner(self, w, h, active, which):
        b = frame_corner(w, h, which, *self._edge(active), self.M["side"])
        if active:
            b += sparkle(10 if which == "left" else w - 10, h / 2 + 0.5, 2.8, SILVER)
        return svg(w, h, b)

    # ---- menus: a starfield ------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WING_XDK)
                   + starfield(w, h, 11, 10, ["#ffffff", SILVER_DK, NEB_BLUE, NEB_PINK], 0.8))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, "url(#s)", rx=4) + rect(2, 1, 2, h - 2, CRESCENT, rx=1)
                   + rect(6, 1.5, w - 10, 1, "#ffffff", extra='opacity="0.3"'),
                   hgrad("s", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        return base.replace("</svg>", crescent(w - 12, h / 2, 4.5, "#ffffff" if hilite else CRESCENT, 0.35, 180) + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NIGHT))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#4a3a8a", 1, rx=5, fill=WING_XDK))

    def push_button(self, w, h, state):
        fill, edge = {"normal": (WING, SILVER_DK), "hover": (WING, NEB_PINK), "clicked": (NEB_BLUE, SILVER)}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=5)
                   + rect(4, 2, w - 8, 1, "#ffffff", extra='opacity="0.2"'))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, WING_XDK, NEB_PINK if hover else SILVER_DK, 1, rx=2)
        if on:
            b += sparkle(s / 2, s / 2, s / 2 - 2, CRESCENT)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, WING_XDK, NEB_PINK if hover else SILVER_DK, 1)
        if on:
            b += crescent(c, c, c - 2.6, CRESCENT, 0.35, 180)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, "url(#g)"), hgrad("g", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)]))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#4a3a8a", 1, rx=min(w, h) / 2, fill=WING_XDK))

    def knob(self, w, h, vertical, clicked):
        g = hgrad("k", [(0, NEB_BLUE), (1, NEB_PINK)]) if not clicked else hgrad("k", [(0, CRESCENT), (1, CRESCENT_DK)])
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", SILVER, 0.8, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, NEB_VIOLET) + sparkle(s / 2, s / 2, s / 2, "#ffffff"))

    # ---- popups: silver -------------------------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WING, rx=5) + rect(1.5, 1.5, w - 3, h - 3, SILVER, rx=4)
                   + rect(1.5, h - 3.5, w - 3, 2, "url(#neb)"),
                   hgrad("neb", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)]))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WING, rx=5) + rect(1.5, 1.5, w - 3, h - 3, SILVER, rx=4))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WING, rx=5) + rect(1.5, 1.5, w - 3, h - 3, "url(#s)", rx=4),
                   hgrad("s", [(0, NEB_VIOLET), (1, NEB_PINK)]))

    def bubble(self, s, i):
        return svg(s, s, sparkle(s / 2, s / 2, s / 2 - 0.3, ["#ffffff", SILVER_DK, NEB_PINK, "#ffffff"][i - 1]))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, NEB_BLUE), (0.5, NEB_VIOLET), (1, NEB_PINK)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WING_XDK))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SILVER) + rect(1, 1, w - 2, h - 2, WING) + rect(1, 1, w - 2, 3, NEB_VIOLET))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, NEB_PINK, 2, rx=2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NIGHT))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#4a3a8a", 1, rx=5, fill=WING_XDK))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, NIGHT, SILVER_DK))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, WING_DK) + rect(w - 2, 0, 2, h, SILVER))
        return svg(w, h, rect(0, 0, w, h, WING_DK) + rect(0, h - 2, w, 2, SILVER))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: its wings reaching out of both sides, ribbed in silver with crescent-gold claws ----

    SHAPE = dict(left=28, right=28)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        W, H = 33, 80

        def wing(active):
            body, rib, claw = (WING, SILVER, CRESCENT) if active else (DIM, "#4a4668", "#5a5878")
            d = f"M{W},4 C18,0 4,8 1,22 C8,22 12,28 10,36 C16,34 20,40 18,50 C24,48 28,56 {W},62 Z"
            b = path(d, fill=body, stroke=rib, sw=1.4)
            for y1, x2, y2 in ((10, 4, 22), (24, 11, 36), (40, 19, 50)):
                b += path(f"M{W},{y1} Q{(W + x2) / 2},{y1 + 2} {x2},{y2}", stroke=rib, sw=1.2)
                b += path(f"M{x2},{y2} l-3,-4 l5,1 Z", fill=claw)
            return b

        return [("wing_l", W, H, "tl", 0, 8, lambda a: svg(W, H, wing(a))),
                ("wing_r", W, H, "tr", 0, 8, lambda a: svg(W, H, mirror(W, wing(a))))]
