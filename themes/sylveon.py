"""Sylveon: pastel pink ribbons on powder blue, polka dots, bow, stars and hearts."""

import math

from base import Art, circle, frame, hgrad, path, rect, star5, svg, vgrad

POWDER = "#d0e2f2"
POWDER_LT = "#eaf3fb"
DOT = "#e4eff9"
PINK_LT = "#f8cfda"
PINK = "#f2b4c4"
PINK_MID = "#e89ab0"
ROSE = "#e27a9c"
MAUVE = "#7a4a5a"          # the cartoon outline colour
MAUVE_DK = "#5a3444"
WHITE = "#fdf8fb"
SKY = "#9ad0e8"
PURPLE = "#8a86d8"
STAR_PINK = "#f4a0b0"
GREY_LT = "#dfe6ee"        # inactive
GREY = "#c3cfdc"
GREY_LINE = "#8a9aae"


def heart(cx, cy, r, fill, stroke=None, sw=1):
    d = (f"M{cx},{cy + r * 0.9} C{cx - r * 1.4},{cy} {cx - r},{cy - r * 1.1} {cx},{cy - r * 0.35} "
         f"C{cx + r},{cy - r * 1.1} {cx + r * 1.4},{cy} {cx},{cy + r * 0.9} Z")
    return path(d, fill=fill, stroke=stroke, sw=sw)


def bow(cx, cy, k, fill=PINK, tip=WHITE, edge=MAUVE):
    """Sylveon's neck bow: two looped wings and a knot."""
    wing = (f"M0,0 C-3,-5 -9,-7 -10,-3 C-11,1 -8,5 0,0 Z")
    inner = f"M-1,0 C-3,-3 -6,-4 -7,-2 C-6,-1 -3,0 -1,0 Z"
    g = f'<g transform="translate({cx},{cy}) scale({k})">'
    for sx in (1, -1):
        g += f'<g transform="scale({sx},1)">' + path(wing, fill=fill, stroke=edge, sw=1.1) + path(inner, fill=tip) + "</g>"
    g += circle(0, 0, 2.2, fill, edge, 1.1)
    return g + "</g>"


def dots(w, h, step, r, fill, x0=0, y0=0):
    """Polka-dot grid, offset every other row like the wallpaper."""
    b = ""
    for j, y in enumerate(range(y0, h + step, step // 2)):
        off = (step // 2) if j % 2 else 0
        for x in range(x0 + off, w + step, step):
            b += circle(x, y, r, fill)
    return b


class Sylveon(Art):
    NAME = "Sylveon"
    WALLPAPER = "5/wp3753871-3816831169.jpg"
    BG_SOLID = POWDER

    P = dict(base=WHITE, panel=WHITE, raised=PINK_LT, line=PINK_MID, line_dim=GREY,
             accent=ROSE, accent_hi=PINK_MID, text=MAUVE_DK, text_dim=GREY_LINE,
             sel=ROSE, sel_text="#ffffff", danger=ROSE, shadow=WHITE)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(48, 26), title_pad_l=40, menu_title_h=24, menu_item_pad=(12, 22, 3, 3))

    FONTS = dict(border="pango:Adwaita Sans Bold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans SemiBold 8")

    TEXT = dict(title_active=MAUVE_DK, title_inactive="#6a7a8c", menu_title=MAUVE_DK,
                menu=MAUVE_DK, menu_hilite="#ffffff", dialog=MAUVE_DK, tooltip=MAUVE_DK)
    TITLE_JUSTIFY = 512
    TEXT_EFFECT = "__EFFECT_NONE"
    MENU_BG_TILE = 24
    CURSOR = (WHITE, MAUVE)
    ROFI = dict(border_color=MAUVE, radius=12, sel=(
        "background-image: linear-gradient(to bottom, #e89ab0, #e27a9c); "
        "border: 1px; border-color: #7a4a5a; border-radius: 12px;"))
    MATTE = dict(title=PINK, menu=POWDER_LT, dialog=WHITE, popup=POWDER_LT)

    # ---- window borders -----------------------------------------------------

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        top, bot = (PINK_LT, PINK_MID) if active else (GREY_LT, GREY)
        defs = (f'<linearGradient id="tb" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" x2="0" y2="{TH - dy}">'
                f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>')
        edge = MAUVE if active else GREY_LINE
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, edge) + rect(0, 1 - dy, w, 1.5, "#ffffff", extra='opacity="0.7"')
        b += rect(0, TH - 5 - dy, w, 3, WHITE)                       # white ribbon
        b += rect(0, TH - 2 - dy, w, 1, SKY if active else GREY)
        b += rect(0, TH - 1 - dy, w, 1, edge)
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += bow(20, 10.5, 1.25, ROSE)
        else:
            b += bow(20, 10.5, 1.25, GREY, GREY_LT, GREY_LINE)
        b += rect(w - 1, 0, 1, h, MAUVE if active else GREY_LINE)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, MAUVE) + rect(0, 1, w, 1.5, "#ffffff", extra='opacity="0.7"')
        b += rect(0, h - 5, w, 3, WHITE) + rect(0, h - 2, w, 1, SKY) + rect(0, h - 1, w, 1, MAUVE)
        b += rect(0, 0, 1, h, MAUVE) + rect(w - 1, 0, 1, h, MAUVE)
        b += star5(12, h / 2 - 2, 5.5, SKY, MAUVE, 0.9) + star5(w - 12, h / 2 - 2, 5.5, PURPLE, MAUVE, 0.9)
        return svg(w, h, b, vgrad("g", [(0, PINK_LT), (1, PINK_MID)]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 1, s, MAUVE if state != "inactive" else GREY_LINE)
        fill = {"inactive": GREY_LT, "active": SKY, "hover": PURPLE}[state]
        edge = GREY_LINE if state == "inactive" else MAUVE
        b += star5(s / 2 + 1, s / 2 - 1.5, 8, fill, edge, 1.2, inner=0.5)
        b += circle(s / 2 - 0.5, s / 2 - 4, 1.2, "#ffffff", extra='opacity="0.8"')
        return svg(s, s, b, defs)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        col = {"iconify": SKY, "max": PURPLE, "close": ROSE}[kind]
        fill, edge, glyph = {"inactive": (GREY_LT, GREY_LINE, GREY_LINE),
                             "active": (WHITE, MAUVE, col),
                             "hover": (col, MAUVE, "#ffffff"),
                             "clicked": (MAUVE, MAUVE_DK, WHITE)}[state]
        c = s / 2
        b += circle(c, c, c - 1.2, fill, edge, 1.2)
        if state == "active":
            b += circle(c - 3, c - 3.5, 1.4, "#ffffff")
        m = 6
        b += {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=glyph, sw=2),
              "max": rect(m, m, s - 2 * m, s - 2 * m, "none", glyph, 1.8, rx=1.5),
              "iconify": path(f"M{m},{c + 2} L{s-m},{c + 2}", stroke=glyph, sw=2)}[kind]
        return svg(s, s, b, defs)

    def _edge(self, active):
        return (PINK, MAUVE, WHITE) if active else (GREY, GREY_LINE, GREY_LT)

    def side(self, w, h, active, which):
        fill, out, inner = self._edge(active)
        b = rect(0, 0, w, h, fill)
        ox, ix = (0, w - 2) if which == "left" else (w - 1, 0)
        b += rect(ox, 0, 1, h, out) + rect(ix, 0, 2, h, inner)
        return svg(w, h, b)

    def bottom(self, w, h, active):
        fill, out, inner = self._edge(active)
        return svg(w, h, rect(0, 0, w, h, fill) + rect(0, 0, w, 2, inner) + rect(0, h - 1, w, 1, out))

    def corner(self, w, h, active, which):
        fill, out, inner = self._edge(active)
        b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, out)
        if which == "left":
            b += rect(0, 0, 1, h, out) + rect(3, 0, w - 3, 2, inner) + rect(3, 0, 2, 2, inner)
            hx = 11
        else:
            b += rect(w - 1, 0, 1, h, out) + rect(0, 0, w - 3, 2, inner)
            hx = w - 11
        b += heart(hx, h / 2 + 0.5, 2.6, ROSE if active else GREY_LINE)
        return svg(w, h, b)

    # ---- menus: powder blue polka dots ------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, POWDER_LT) + dots(w, h, w, 2, "#ffffff", w // 4, h // 4))

    def menu_sel(self, w, h):
        b = rect(2, 1, w - 4, h - 2, "url(#s)", MAUVE, 1, rx=(h - 2) / 2)
        b += rect(8, 2.5, w - 16, 1.5, "#ffffff", extra='opacity="0.45"')
        return svg(w, h, b, vgrad("s", [(0, PINK_MID), (1, ROSE)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        s = star5(w - 12, h / 2, 5, "#ffffff" if hilite else STAR_PINK, MAUVE, 0.9)
        return base.replace("</svg>", s + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, WHITE))

    def area(self, w, h):
        return svg(w, h, frame(w, h, PINK, 1.2, rx=6, fill=POWDER_LT))

    def push_button(self, w, h, state):
        top, bot, edge = {"normal": (PINK_LT, PINK), "hover": ("#fbe0e8", PINK_MID),
                          "clicked": (PINK_MID, ROSE)}[state] + (MAUVE,)
        b = rect(0.6, 0.6, w - 1.2, h - 1.2, "url(#g)", edge, 1.2, rx=h / 2 - 1)
        b += rect(7, 2.5, w - 14, 1.5, "#ffffff", extra='opacity="0.6"')
        return svg(w, h, b, vgrad("g", [(0, top), (1, bot)]))

    def check(self, s, on, hover):
        b = rect(0.6, 0.6, s - 1.2, s - 1.2, "#ffffff", ROSE if hover else MAUVE, 1.1, rx=3)
        if on:
            b += heart(s / 2, s / 2 + 0.5, 4.2, ROSE)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        b = circle(c, c, c - 0.6, "#ffffff", ROSE if hover else MAUVE, 1.1)
        if on:
            b += circle(c, c, c - 3.2, SKY) + circle(c - 1.2, c - 1.2, 1, "#ffffff")
        return svg(s, s, b)

    def separator(self, w, h):
        # stretched, so a soft fading line rather than dots
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1.2, "url(#g)"),
                   hgrad("g", [(0, WHITE), (0.5, PINK_MID), (1, WHITE)]))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, PINK_MID, 1, rx=min(w, h) / 2, fill=POWDER_LT))

    def knob(self, w, h, vertical, clicked):
        f = ROSE if clicked else SKY
        return svg(w, h, rect(0.6, 0.6, w - 1.2, h - 1.2, f, MAUVE, 1.1, rx=min(w, h) / 2 - 0.6)
                   + rect(4, 2.5, w - 8, 1.2, "#ffffff", extra='opacity="0.6"'))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, SKY) + heart(s / 2, s / 2 + 0.3, 2.6, "#ffffff"))

    # ---- popups: powder-blue bubbles with a mauve outline ----------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAUVE, rx=8) + rect(1.5, 1.5, w - 3, h - 3, POWDER_LT, rx=7)
                   + rect(6, 3, w - 12, 1.5, "#ffffff"))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAUVE, rx=8) + rect(1.5, 1.5, w - 3, h - 3, ROSE, rx=7))

    def bubble(self, s, i):
        c = [STAR_PINK, SKY, PURPLE, STAR_PINK][i - 1]
        return svg(s, s, star5(s / 2, s / 2 + 0.5, s / 2 - 0.3, c, MAUVE if s > 8 else None, 0.8))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=h / 2), hgrad("p", [(0, SKY), (0.5, PURPLE), (1, ROSE)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, POWDER) + dots(w, h, 16, 1.5, DOT, 4, 4))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAUVE) + rect(1, 1, w - 2, h - 2, WHITE) + rect(1, 1, w - 2, 4, PINK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, ROSE, 2, rx=3))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, POWDER_LT))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, PINK, 1.2, rx=6, fill=WHITE))

    def arrow(self, s, direction):
        c = s / 2
        d = {"up": f"M3,{s-4} L{c},4 L{s-3},{s-4}Z", "down": f"M3,4 L{c},{s-4} L{s-3},4Z",
             "left": f"M{s-4},3 L4,{c} L{s-4},{s-3}Z", "right": f"M4,3 L{s-4},{c} L4,{s-3}Z"}[direction]
        return svg(s, s, rect(0, 0, s, s, POWDER_LT) + path(d, fill=ROSE, stroke=MAUVE, sw=0.8))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, PINK) + rect(w - 4, 0, 2, h, WHITE) + rect(w - 1, 0, 1, h, MAUVE))
        return svg(w, h, rect(0, 0, w, h, PINK) + rect(0, h - 4, w, 2, WHITE) + rect(0, h - 1, w, 1, MAUVE))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: ribbon feelers trailing out of the right side, a bow on top ----

    SHAPE = dict(top=14, right=32)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def ribbons(active):
            k = (lambda c: c) if active else (lambda c: mute(c, "#c3cfdc", 0.55))
            b = ""
            for d, tip in (("M1,10 C14,2 22,24 33,14", PINK_MID), ("M1,26 C10,36 20,30 22,46 C23,54 30,58 34,54", SKY)):
                b += path(d, stroke=k(MAUVE), sw=7.5) + path(d, stroke=k(WHITE), sw=5)
                b += path(d, stroke=k(tip), sw=5, extra='stroke-dasharray="6 200" stroke-dashoffset="-200"')
            b += circle(33, 14, 3.2, k(PINK_MID), k(MAUVE), 1) + circle(34, 54, 3.2, k(SKY), k(MAUVE), 1)
            return svg(37, 60, b)

        def topbow(active):
            k = (lambda c: c) if active else (lambda c: mute(c, "#c3cfdc", 0.55))
            return svg(34, T + 3, bow(17, T - 3, 1.35, k(ROSE), k(WHITE), k(MAUVE)))

        return [("ribbons", 37, 60, "tr", 0, T + 8, ribbons),
                ("bow", 34, T + 3, "tl", 6, 0, topbow)]
