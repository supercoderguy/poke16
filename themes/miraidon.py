"""Miraidon: indigo night, cyan neon glow, lightning mane, glowing ear-disc emblem."""

from base import Art, circle, frame, hgrad, path, rect, sparkle, svg, vgrad

NAVY = "#1c1a45"
NAVY_DK = "#13112f"
INDIGO = "#3a3a86"
INDIGO_DK = "#262259"
VIOLET = "#6a5ac8"
SKY = "#2c5aa8"
CYAN = "#82f7f2"
CYAN_DIM = "#4fb6c4"
PINK = "#ecabcc"
DISC = "#f2c8ee"
HOTPINK = "#ff8fd0"
CREAM = "#fee5c0"
SLATE = "#34325e"        # inactive surfaces
SLATE_DK = "#24223f"
SLATE_LINE = "#5a5790"

GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{}"/></filter>'


def bolt(x, y, fill, stroke, sw=1.1):
    """A streak of lightning pointing right, like the mane sweeping back."""
    pts = [(0, 13), (10, 4), (12, 9), (24, 1), (23, 7), (38, 2), (26, 12), (27, 8), (14, 15), (13, 11)]
    d = "M" + " L".join(f"{x + px},{y + py}" for px, py in pts) + "Z"
    return path(d, fill=fill, stroke=stroke, sw=sw)


def ear_disc(cx, cy, r, core=DISC, ring=CYAN, glow=True):
    """Miraidon's round, glowing ear/headphone disc."""
    b = ""
    if glow:
        b += circle(cx, cy, r, ring, extra='opacity="0.6" filter="url(#glow)"')
    b += circle(cx, cy, r, NAVY_DK, ring, r * 0.24)
    b += circle(cx, cy, r * 0.62, core)
    b += circle(cx - r * 0.2, cy - r * 0.22, r * 0.16, "#ffffff", extra='opacity="0.8"')
    return b


class Miraidon(Art):
    NAME = "Miraidon"
    WALLPAPER = "3/miraidon-pokemon-scarlet-and-violet-483@1@j-pc-4k-2832167655.jpg"
    BG_SOLID = NAVY

    P = dict(base=NAVY, panel=NAVY, raised=INDIGO, line=CYAN, line_dim=SLATE_LINE,
             accent=CYAN, accent_hi="#c8fffc", text=CREAM, text_dim="#8a86b8",
             sel=VIOLET, sel_text="#ffffff", danger=HOTPINK, shadow=NAVY_DK)

    M = dict(Art.M, title_h=26, side=5, bottom=6, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=48, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans Bold 9", menu="pango:Adwaita Sans Medium 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans SemiBold 8")

    TEXT = dict(title_active="#eafcff", title_inactive="#8a86b8", menu_title="#eafcff",
                menu="#dcd8ff", menu_hilite="#ffffff", dialog="#dcd8ff", tooltip=CREAM)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    CURSOR = ("#ffffff", "#3a3a86")
    ROFI = dict(border_color=CYAN_DIM, radius=8, sel=(
        "background-image: linear-gradient(to right, #6a5ac8, #b77ac8, #ecabcc); "
        "border: 0 0 0 2px; border-color: #82f7f2; border-radius: 4px;"))
    MATTE = dict(title=INDIGO_DK, menu=NAVY, dialog=NAVY, popup=INDIGO_DK)

    # ---- window borders -----------------------------------------------------

    def _title_bg(self, w, active, dy=0):
        """Title background seen through a w-wide window dy px down the bar."""
        TH = self.M["title_h"]
        top, bot = (INDIGO, INDIGO_DK) if active else (SLATE, SLATE_DK)
        defs = (f'<linearGradient id="tb" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" x2="0" y2="{TH - dy}">'
                f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>'
                + GLOW.format(1.2))
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, "#5b5bb0" if active else "#44426e")
        if active:   # neon light strip: blurred halo + crisp core
            b += rect(0, TH - 4 - dy, w, 3, CYAN, extra='opacity="0.7" filter="url(#glow)"')
            b += rect(0, TH - 3 - dy, w, 1.5, "#e8fffe")
        else:
            b += rect(0, TH - 3 - dy, w, 1.5, SLATE_LINE)
        b += rect(0, TH - 1 - dy, w, 1, NAVY_DK)
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        if active:
            b += '<g filter="url(#glow)" opacity="0.8">' + bolt(4, 4, CYAN, CYAN, 2) + "</g>"
            b += bolt(4, 4, CREAM, CYAN)
        else:
            b += bolt(4, 4, "#4a4878", SLATE_LINE)
        b += rect(w - 1, 0, 1, h, NAVY_DK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, "#5b5bb0")
        b += rect(0, h - 4, w, 3, CYAN, extra='opacity="0.7" filter="url(#glow)"') + rect(0, h - 3, w, 1.5, "#e8fffe")
        b += rect(0, h - 1, w, 1, NAVY_DK)
        b += sparkle(12, h / 2 - 1.5, 5, CREAM) + sparkle(w - 12, h / 2 - 1.5, 5, DISC)
        return svg(w, h, b, vgrad("g", [(0, INDIGO), (1, INDIGO_DK)]) + GLOW.format(1.2))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "inactive":
            b += ear_disc(cx, cy, 7.5, "#6c5f86", SLATE_LINE, glow=False)
        elif state == "active":
            b += ear_disc(cx, cy, 7.5)
        else:
            b += ear_disc(cx, cy, 8, "#ffffff", HOTPINK)
        return svg(s, s, b, defs + GLOW.format(1.5))

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        c = s / 2
        ring, fill, glyph = {"inactive": (SLATE_LINE, SLATE_DK, "#8a86b8"),
                             "active": (CYAN, NAVY_DK, CYAN),
                             "hover": (HOTPINK if kind == "close" else CYAN, "#5a2f78" if kind == "close" else VIOLET, "#ffffff"),
                             "clicked": ("#ffffff", CYAN, NAVY_DK)}[state]
        if state in ("hover", "clicked"):
            b += circle(c, c, c - 2.5, ring, extra='opacity="0.8" filter="url(#bglow)"')
        b += circle(c, c, c - 1.6, fill, ring, 1.3)
        m = 6
        b += {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=glyph, sw=1.8),
              "max": rect(m, m, s - 2 * m, s - 2 * m, "none", glyph, 1.6, rx=1.5),
              "iconify": path(f"M{m},{c + 2} L{s-m},{c + 2}", stroke=glyph, sw=1.8)}[kind]
        return svg(s, s, b, defs + '<filter id="bglow" x="-50%" y="-50%" width="200%" height="200%">'
                   '<feGaussianBlur stdDeviation="1.3"/></filter>')

    def _edge(self, active):
        return (NAVY, CYAN_DIM) if active else (SLATE_DK, SLATE_LINE)

    def side(self, w, h, active, which):
        fill, inner = self._edge(active)
        b = rect(0, 0, w, h, fill)
        ox, ix = (0, w - 1) if which == "left" else (w - 1, 0)
        b += rect(ox, 0, 1, h, NAVY_DK) + rect(ix, 0, 1, h, inner)
        return svg(w, h, b)

    def bottom(self, w, h, active):
        fill, inner = self._edge(active)
        return svg(w, h, rect(0, 0, w, h, fill) + rect(0, 0, w, 1, inner) + rect(0, h - 1, w, 1, NAVY_DK))

    def corner(self, w, h, active, which):
        fill, inner = self._edge(active)
        b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, NAVY_DK)
        if which == "left":
            b += rect(0, 0, 1, h, NAVY_DK) + rect(4, 0, w - 4, 1, inner)
            spark_x = 10
        else:
            b += rect(w - 1, 0, 1, h, NAVY_DK) + rect(0, 0, w - 5, 1, inner)
            spark_x = w - 10
        if active:   # a tiny pink spark where the frame turns
            b += sparkle(spark_x, h / 2, 2.6, DISC)
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def menu_sel(self, w, h):
        # the pink/violet sunset clouds behind Miraidon
        b = rect(2, 1, w - 4, h - 2, "url(#s)", rx=4)
        b += rect(2, 1, 2, h - 2, CYAN, rx=1)
        b += rect(5, 1.5, w - 9, 1, "#ffffff", extra='opacity="0.3"')
        return svg(w, h, b, hgrad("s", [(0, VIOLET), (0.7, "#b77ac8"), (1, PINK)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 16, h / 2
        c = "#ffffff" if hilite else CYAN
        d = f"M{x + 1},{m - 4.5} L{x + 5.5},{m} L{x + 1},{m + 4.5}"
        chev = (path(d, stroke=c, sw=3, extra='opacity="0.5" filter="url(#cg)"')
                + path(d, stroke=c, sw=1.6))
        return base.replace("<defs>", '<defs><filter id="cg"><feGaussianBlur stdDeviation="1"/></filter>', 1
                            ).replace("</svg>", chev + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#3c3a7a", 1, rx=6, fill=NAVY_DK))

    def push_button(self, w, h, state):
        top, bot, st = {"normal": (INDIGO, INDIGO_DK, CYAN_DIM),
                        "hover": ("#4a4aa0", INDIGO, HOTPINK),
                        "clicked": (CYAN, CYAN_DIM, "#ffffff")}[state]
        b = rect(0.5, 0.5, w - 1, h - 1, "url(#g)", st, 1, rx=h / 2 - 1)
        b += rect(6, 2, w - 12, 1, "#ffffff", extra='opacity="0.25"')
        return svg(w, h, b, vgrad("g", [(0, top), (1, bot)]))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, NAVY_DK, HOTPINK if hover else CYAN_DIM, 1, rx=3)
        if on:  # a little lightning tick
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 4} L{s / 2 + 1},{s / 2} L{s - 3},3",
                      stroke=HOTPINK if hover else CYAN, sw=1.8)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        if on:
            return svg(s, s, ear_disc(s / 2, s / 2, s / 2 - 1.5, DISC, HOTPINK if hover else CYAN, glow=False))
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 1, NAVY_DK, HOTPINK if hover else CYAN_DIM, 1))

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, "url(#g)"),
                   hgrad("g", [(0, NAVY), (0.5, CYAN_DIM), (1, NAVY)]))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#3c3a7a", 1, rx=min(w, h) / 2, fill=NAVY_DK))

    def knob(self, w, h, vertical, clicked):
        g = hgrad("k", [(0, CYAN), (1, "#7aa8ff")]) if not clicked else hgrad("k", [(0, PINK), (1, HOTPINK)])
        return svg(w, h, rect(1, 1, w - 2, h - 2, "url(#k)", "#ffffff", 0.8, rx=min(w, h) / 2 - 1), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, CYAN) + sparkle(s / 2, s / 2, s / 2, "#ffffff"))

    # ---- popups: frosted indigo glass with a cyan edge ------------------------

    def tooltip(self, w, h):
        b = rect(0, 0, w, h, CYAN_DIM, rx=6) + rect(1, 1, w - 2, h - 2, "url(#g)", rx=5)
        b += rect(8, 2, w - 16, 1, "#ffffff", extra='opacity="0.25"')
        return svg(w, h, b, vgrad("g", [(0, "#35337a"), (1, INDIGO_DK)]))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CYAN, rx=6) + rect(1, 1, w - 2, h - 2, "url(#s)", rx=5),
                   hgrad("s", [(0, VIOLET), (1, "#b77ac8")]))

    def bubble(self, s, i):
        c = [CYAN, DISC, CREAM, CYAN][i - 1]
        return svg(s, s, sparkle(s / 2, s / 2, s / 2 - 0.5, c))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=h / 2), hgrad("p", [(0, CYAN), (0.6, "#b77ac8"), (1, PINK)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#g)"), vgrad("g", [(0, INDIGO_DK), (1, NAVY_DK)]))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CYAN_DIM) + rect(1, 1, w - 2, h - 2, VIOLET) + rect(1, 1, w - 2, 3, INDIGO))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, HOTPINK, 2, rx=2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#3c3a7a", 1, rx=6, fill=NAVY_DK))

    def arrow(self, s, direction):
        c = s / 2
        d = {"up": f"M4,{s-5} L{c},4 L{s-4},{s-5}", "down": f"M4,5 L{c},{s-4} L{s-4},5",
             "left": f"M{s-5},4 L4,{c} L{s-5},{s-4}", "right": f"M5,4 L{s-4},{c} L5,{s-4}"}[direction]
        return svg(s, s, rect(0, 0, s, s, NAVY) + path(d, stroke=CYAN, sw=1.6))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, INDIGO_DK) + rect(w - 3, 0, 1.5, h, CYAN) + rect(w - 1, 0, 1, h, NAVY_DK))
        return svg(w, h, rect(0, 0, w, h, INDIGO_DK) + rect(0, h - 3, w, 1.5, CYAN) + rect(0, h - 1, w, 1, NAVY_DK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
