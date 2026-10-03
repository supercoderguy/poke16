"""Armarouge: gilded armour title plates, psychic flame, helm emblem, sky-and-cloud popups."""

from base import Art, circle, frame, hgrad, path, rect, svg, vgrad

GOLD_HI = "#fff2c0"
GOLD_LT = "#f6dc8a"
GOLD = "#d9b050"
GOLD_DK = "#a8782a"
BRONZE = "#5a3a10"
MAROON = "#6a1e30"
MAROON_DK = "#2e1622"
MAROON_XDK = "#1c0c14"
CAPE = "#8a2a3a"
CORAL = "#d85f62"
PINK = "#f277ce"
CREAM = "#f6e6b0"
CYAN = "#3fe0e8"
HELM = "#393942"
EYE = "#f6f0a0"
SKY = "#1e95bc"
SKY_LT = "#7cc6e2"
CLOUD = "#eaf4fb"
STEEL_LT = "#b8c4cc"     # inactive: unpolished steel instead of gold
STEEL = "#8a96a0"
STEEL_DK = "#5c6872"


def flame(x, y, k=1.0, outer="url(#fl)", inner=CREAM, edge=CYAN):
    """The psychic flame on Armarouge's helm: coral/pink with a cyan rim."""
    o = ("M8,20 C2,20 0,15 2,11 C3,8 5,9 5,6 C5,4 4,2 6,0 C7,4 10,4 10,8 "
         "C11,6 12,5 12,3 C15,6 16,10 15,13 C14,18 12,20 8,20 Z")
    i = "M8,19 C5,19 4,16 5,14 C6,12 7,13 7,11 C8,12 10,12 10,10 C12,12 12,15 11,17 C10,19 9,19 8,19 Z"
    return (f'<g transform="translate({x},{y}) scale({k})">'
            + path(o, fill=outer, stroke=edge, sw=0.9) + path(i, fill=inner) + "</g>")


FLAME_GRAD = vgrad("fl", [(0, PINK), (0.55, CORAL), (1, "#f0a060")])


class Armarouge(Art):
    NAME = "Armarouge"
    WALLPAPER = "2/armarogue-pokemon-scarlet-and-violet-528@1@j-pc-4k-512130743.jpg"
    BG_SOLID = SKY

    P = dict(base=MAROON_DK, panel=MAROON_DK, raised=MAROON, line=GOLD, line_dim=STEEL_DK,
             accent=GOLD, accent_hi=GOLD_LT, text=CREAM, text_dim=STEEL,
             sel=CORAL, sel_text="#ffffff", danger=PINK, shadow=MAROON_XDK)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(48, 24), title_pad_l=40, menu_title_h=24)

    FONTS = dict(border="pango:DejaVu Serif Condensed Bold 9", menu="pango:DejaVu Sans 9",
                 dialog="pango:DejaVu Sans 9", small="pango:DejaVu Sans Bold 8")

    TEXT = dict(title_active="#4a1420", title_inactive="#3e4852", menu_title="#4a1420",
                menu="#f3e2c0", menu_hilite="#ffffff", dialog="#f3e2c0", tooltip="#123a52")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_NONE"    # dark text on gold plates
    CURSOR = (GOLD_LT, MAROON_DK)
    ROFI = dict(border_color=GOLD, radius=4, sel=(
        "background-image: linear-gradient(to right, #d85f62, #f277ce); "
        "border: 0 0 0 2px; border-color: #3fe0e8; border-radius: 3px;"))
    MATTE = dict(title=GOLD, menu=MAROON_DK, dialog=MAROON_DK, popup=CLOUD)

    # ---- window borders -----------------------------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        stops = ([(0, GOLD_LT), (0.5, GOLD), (1, GOLD_DK)] if active
                 else [(0, STEEL_LT), (0.5, STEEL), (1, STEEL_DK)])
        s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        defs = (f'<linearGradient id="tb" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" '
                f'x2="0" y2="{TH - 4 - dy}">{s}</linearGradient>')
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, GOLD_HI if active else "#dde4e8")                # polished edge
        b += rect(0, TH - 5 - dy, w, 1, BRONZE if active else "#3e4852")
        b += rect(0, TH - 4 - dy, w, 4, CAPE if active else "#4a4e5a")            # cape band
        b += rect(0, TH - 1 - dy, w, 1, MAROON_XDK)
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += flame(8, 1, 0.95)
        else:
            b += flame(8, 1, 0.95, "#9aa6ae", "#c8d0d6", "#6a7680")
        b += rect(w - 1, 0, 1, h, MAROON_XDK)
        return svg(w, h, b, defs + FLAME_GRAD)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, GOLD_HI)
        b += rect(0, h - 5, w, 1, BRONZE) + rect(0, h - 4, w, 4, CAPE) + rect(0, h - 1, w, 1, MAROON_XDK)
        b += flame(5, 1, 0.85) + flame(w - 19, 1, 0.85)
        return svg(w, h, b, vgrad("g", [(0, GOLD_LT), (0.5, GOLD), (1, GOLD_DK)]) + FLAME_GRAD)

    def emblem(self, s, state):
        """Armarouge's dark helm and its two glowing eyes."""
        defs, b = self._title_bg(s, state != "inactive")
        cx, cy = s / 2 + 1, s / 2 - 1
        helm = HELM if state != "inactive" else "#4a525c"
        eye = {"inactive": "#aab4ba", "active": EYE, "hover": CYAN}[state]
        if state == "hover":
            b += circle(cx, cy, 9, CYAN, extra='opacity="0.5" filter="url(#g)"')
        # dome with a pointed crest, flaring out at the jaw
        b += path(f"M{cx},{cy - 9} L{cx + 2},{cy - 6} C{cx + 7},{cy - 5} {cx + 8},{cy} {cx + 7},{cy + 5} "
                  f"L{cx + 3},{cy + 6} L{cx},{cy + 4} L{cx - 3},{cy + 6} L{cx - 7},{cy + 5} "
                  f"C{cx - 8},{cy} {cx - 7},{cy - 5} {cx - 2},{cy - 6} Z",
                  fill=helm, stroke=BRONZE if state != "inactive" else "#3e4852", sw=0.8)
        b += f'<ellipse cx="{cx - 3}" cy="{cy}" rx="1.8" ry="1.3" fill="{eye}"/>'
        b += f'<ellipse cx="{cx + 3}" cy="{cy}" rx="1.8" ry="1.3" fill="{eye}"/>'
        return svg(s, s, b, defs + '<filter id="g"><feGaussianBlur stdDeviation="1.5"/></filter>')

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        fill, rim, glyph = {"inactive": ("url(#bs)", "#c8d0d6", "#e0e6ea"),
                            "active": ("url(#bm)", GOLD_LT, CREAM),
                            "hover": ("url(#fl)", CYAN, "#ffffff"),
                            "clicked": (CYAN, "#ffffff", MAROON)}[state]
        defs += (vgrad("bm", [(0, CAPE), (1, "#4e1224")]) + vgrad("bs", [(0, STEEL), (1, STEEL_DK)])
                 + FLAME_GRAD)
        b += rect(1, 1, s - 2, s - 2, fill, rim, 1.3, rx=5)
        m = 5.5
        b += {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=glyph, sw=2),
              "max": rect(m, m, s - 2 * m, s - 2 * m, "none", glyph, 1.7, rx=1),
              "iconify": path(f"M{m},{s - m - 0.5} L{s-m},{s - m - 0.5}", stroke=glyph, sw=2)}[kind]
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (MAROON, GOLD) if active else ("#4a4e5a", STEEL)

    def side(self, w, h, active, which):
        fill, inner = self._edge(active)
        b = rect(0, 0, w, h, fill)
        ox, ix = (0, w - 1) if which == "left" else (w - 1, 0)
        b += rect(ox, 0, 1, h, MAROON_XDK) + rect(ix, 0, 1, h, inner)
        return svg(w, h, b)

    def bottom(self, w, h, active):
        fill, inner = self._edge(active)
        return svg(w, h, rect(0, 0, w, h, fill) + rect(0, 0, w, 1, inner) + rect(0, h - 1, w, 1, MAROON_XDK))

    def corner(self, w, h, active, which):
        fill, inner = self._edge(active)
        b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, MAROON_XDK)
        if which == "left":
            b += rect(0, 0, 1, h, MAROON_XDK) + rect(4, 0, w - 4, 1, inner)
            rx = 9
        else:
            b += rect(w - 1, 0, 1, h, MAROON_XDK) + rect(0, 0, w - 5, 1, inner)
            rx = w - 9
        b += circle(rx, h / 2 + 0.5, 1.8, inner) + circle(rx - 0.5, h / 2, 0.6, GOLD_HI if active else "#dde4e8")
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def menu_sel(self, w, h):
        b = rect(2, 1, w - 4, h - 2, "url(#s)", rx=3) + rect(2, 1, 2, h - 2, CYAN, rx=1)
        b += rect(5, 1.5, w - 9, 1, "#ffffff", extra='opacity="0.3"')
        return svg(w, h, b, hgrad("s", [(0, CORAL), (1, PINK)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=CREAM if hilite else GOLD)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#6a3040", 1, rx=3, fill="#24101a"))

    def push_button(self, w, h, state):
        fill, rim = {"normal": ("url(#bm)", GOLD), "hover": ("url(#bm)", GOLD_HI),
                     "clicked": ("url(#fl)", CYAN)}[state]
        b = rect(0.5, 0.5, w - 1, h - 1, fill, rim, 1, rx=4)
        b += rect(3, 2, w - 6, 1, "#ffffff", extra='opacity="0.2"')
        return svg(w, h, b, vgrad("bm", [(0, CAPE), (1, "#4e1224")]) + FLAME_GRAD)

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, MAROON_XDK, GOLD_HI if hover else GOLD, 1, rx=2)
        if on:
            b += flame(2.2, 1, 0.6)
        return svg(s, s, b, FLAME_GRAD)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.5, MAROON_XDK, GOLD_HI if hover else GOLD, 1)
        if on:   # gold boss with a cyan gem
            b += circle(c, c, c - 3, "url(#g)") + circle(c, c, 1.6, CYAN)
        return svg(s, s, b, vgrad("g", [(0, GOLD_LT), (1, GOLD_DK)]))

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 1, "#1a0a12") + rect(0, h / 2, w, 1, "#6a3040"))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#6a3040", 1, rx=min(w, h) / 2, fill=MAROON_XDK))

    def knob(self, w, h, vertical, clicked):
        g = vgrad("k", [(0, GOLD_LT), (1, GOLD_DK)]) if not clicked else FLAME_GRAD.replace('id="fl"', 'id="k"')
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", BRONZE, 1, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, GOLD) + circle(s / 2, s / 2, 2, CYAN))

    # ---- popups: bright sky and cloud ------------------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SKY, rx=5) + rect(2, 2, w - 4, h - 4, CLOUD, rx=4)
                   + rect(2, h - 5, w - 4, 3, SKY_LT))

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, SKY, rx=5) + rect(2, 2, w - 4, h - 4, CLOUD, rx=4))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "#0e5a78", rx=5) + rect(2, 2, w - 4, h - 4, SKY, rx=4))

    def bubble(self, s, i):
        # little cloud puffs
        c = s / 2
        return svg(s, s, circle(c, c, c - 0.5, SKY) + circle(c, c, c - 1.8, "#ffffff"))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, CORAL), (1, PINK)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#g)"), vgrad("g", [(0, SKY), (1, "#0e5a78")]))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BRONZE) + rect(1, 1, w - 2, h - 2, GOLD) + rect(1, 1, w - 2, 3, GOLD_LT))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, CYAN, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#6a3040", 1, rx=4, fill="#24101a"))

    def arrow(self, s, direction):
        c = s / 2
        d = {"up": f"M3,{s-4} L{c},4 L{s-3},{s-4}Z", "down": f"M3,4 L{c},{s-4} L{s-3},4Z",
             "left": f"M{s-4},3 L4,{c} L{s-4},{s-3}Z", "right": f"M4,3 L{s-4},{c} L4,{s-3}Z"}[direction]
        return svg(s, s, rect(0, 0, s, s, MAROON_DK) + path(d, fill=GOLD))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, MAROON) + rect(w - 2, 0, 1, h, GOLD) + rect(w - 1, 0, 1, h, MAROON_XDK))
        return svg(w, h, rect(0, 0, w, h, MAROON) + rect(0, h - 2, w, 1, GOLD) + rect(0, h - 1, w, 1, MAROON_XDK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
