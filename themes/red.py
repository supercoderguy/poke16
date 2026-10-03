"""Red: black-and-white manga — ink panels, screentone, speed lines, speech bubbles,
and a single spot colour for the Poke Ball."""

from base import Art, circle, frame, line, path, rect, svg

INK = "#111111"
INK_SOFT = "#2a2a2a"
PAPER = "#fbfbf8"
PAPER_DK = "#e6e6e2"
TONE = "#c8c8c4"          # screentone dot grey
GREY = "#8a8a88"
RED = "#d8202a"


def screentone(w, h, step, r, fill, x0=None, y0=None):
    """Offset halftone dot grid (the dot pattern shading manga panels)."""
    b = ""
    x0 = step / 2 if x0 is None else x0
    y0 = step / 2 if y0 is None else y0
    row, y = 0, y0
    while y < h + step:
        x = x0 + (step / 2 if row % 2 else 0)
        while x < w + step:
            b += circle(round(x, 2), round(y, 2), r, fill)
            x += step
        y += step / 2
        row += 1
    return b


def pokeball(cx, cy, r, top=RED, edge=INK, bottom=PAPER, sw=1.4):
    b = circle(cx, cy, r, bottom, edge, sw)
    b += path(f"M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy} Z", fill=top, stroke=edge, sw=sw)
    b += line(cx - r, cy, cx + r, cy, edge, sw)
    b += circle(cx, cy, r * 0.34, bottom, edge, sw)
    return b


def speed_lines(x, y, lengths, gap, colour, sw=1):
    """Horizontal motion streaks, longest first."""
    return "".join(line(x, y + i * gap, x + L, y + i * gap, colour, sw, 'stroke-linecap="round"')
                   for i, L in enumerate(lengths))


class Red(Art):
    NAME = "Red"
    WALLPAPER = "1/1207213-759517466.jpg"
    WALLPAPER_MODE = "fit"     # not 16:9, so letterbox onto paper rather than stretch
    BG_SOLID = "#f4f4f2"

    P = dict(base=PAPER, panel=PAPER, raised=PAPER_DK, line=INK, line_dim=GREY,
             accent=INK, accent_hi=INK_SOFT, text=INK, text_dim=GREY,
             sel=INK, sel_text=PAPER, danger=RED, shadow=PAPER)

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(64, 24), title_pad_l=56, menu_title_h=24, menu_item_pad=(12, 22, 3, 3))

    FONTS = dict(border="pango:Adwaita Sans Black Italic 9", menu="pango:Adwaita Sans SemiBold 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold Italic 8")

    TEXT = dict(title_active=PAPER, title_inactive="#555555", menu_title=PAPER,
                menu=INK, menu_hilite=PAPER, dialog=INK, tooltip=INK)
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_NONE"
    MENU_BG_TILE = 12
    CURSOR = (PAPER, INK)
    ROFI = dict(border_color=INK, border=3, radius=0, sel=(
        "background-color: #111111; border: 0 0 0 4px; border-color: #d8202a;"))
    MATTE = dict(title=INK, menu=PAPER, dialog=PAPER, popup=PAPER)

    # ---- window borders -----------------------------------------------------
    # Active window = a black caption box; inactive = plain white paper.

    def _title_bg(self, w, active, dy=0):
        TH = self.M["title_h"]
        if active:
            b = rect(0, -dy, w, TH, INK)
            b += rect(0, 2 - dy, w, 1, PAPER) + rect(0, TH - 4 - dy, w, 1, PAPER)   # panel inner line
        else:
            b = rect(0, -dy, w, TH, PAPER)
            b += rect(0, -dy, w, 2, INK) + rect(0, TH - 3 - dy, w, 1, GREY)
        b += rect(0, TH - 2 - dy, w, 2, INK)
        return "", b

    def title(self, w, h, active):
        _, b = self._title_bg(w, active)
        if active:
            b += speed_lines(4, 7, (44, 30, 38, 22), 3, PAPER, 1)
        else:
            b += speed_lines(4, 7, (44, 30, 38, 22), 3, TONE, 1)
        b += rect(w - 2, 0, 2, h, INK)
        return svg(w, h, b)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, INK) + rect(0, 2, w, 1, PAPER) + rect(0, h - 4, w, 1, PAPER)
        b += speed_lines(4, 7, (30, 20, 26), 3, PAPER)
        # mirrored on the right, streaking toward the edge
        b += "".join(line(w - 4 - L, 7 + i * 3, w - 4, 7 + i * 3, PAPER, 1, 'stroke-linecap="round"')
                     for i, L in enumerate((30, 20, 26)))
        return svg(w, h, b)

    def emblem(self, s, state):
        _, b = self._title_bg(s, state != "inactive")
        b += rect(0, 0, 2, s, INK)
        cx, cy = s / 2 + 1, s / 2 - 1.5
        if state == "inactive":
            b += pokeball(cx, cy, 7.5, TONE, INK, PAPER)
        elif state == "active":
            b += pokeball(cx, cy, 7.5, RED, INK, PAPER, 1.2) + circle(cx, cy, 8.2, "none", PAPER, 1)
        else:
            b += circle(cx, cy, 9.5, "none", PAPER, 2) + pokeball(cx, cy, 7.5, "#ff3a44", INK, PAPER, 1.2)
        return svg(s, s, b)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        _, b = self._title_bg(s, state != "inactive", by)
        fill, edge, glyph = {"inactive": (PAPER, INK, INK),
                             "active": (PAPER, PAPER, INK),
                             "hover": (RED if kind == "close" else INK, PAPER, PAPER),
                             "clicked": (INK_SOFT, PAPER, PAPER)}[state]
        b += rect(1, 1, s - 2, s - 2, fill, edge, 2)
        if state == "clicked":   # screentone in the pressed panel
            b += screentone(s, s, 4, 0.7, GREY, 3, 3)
        m = 5.5
        b += {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=glyph, sw=2.4),
              "max": rect(m, m, s - 2 * m, s - 2 * m, "none", glyph, 2),
              "iconify": path(f"M{m},{s - m - 0.5} L{s-m},{s - m - 0.5}", stroke=glyph, sw=2.4)}[kind]
        return svg(s, s, b)

    def side(self, w, h, active, which):
        b = rect(0, 0, w, h, PAPER)
        ox, ix = (0, w - 1) if which == "left" else (w - 2, 0)
        b += rect(ox, 0, 2, h, INK) + rect(ix, 0, 1, h, INK if active else GREY)
        return svg(w, h, b)

    def bottom(self, w, h, active):
        return svg(w, h, rect(0, 0, w, h, PAPER) + rect(0, 0, w, 1, INK if active else GREY)
                   + rect(0, h - 2, w, 2, INK))

    def corner(self, w, h, active, which):
        inner = INK if active else GREY
        b = rect(0, 0, w, h, PAPER) + rect(0, h - 2, w, 2, INK)
        if which == "left":
            b += rect(0, 0, 2, h, INK) + rect(4, 0, w - 4, 1, inner)
            tone_x = 3
        else:
            b += rect(w - 2, 0, 2, h, INK) + rect(0, 0, w - 4, 1, inner)
            tone_x = w - 20
        if active:   # a patch of screentone in the corner gutter
            b += "".join(circle(tone_x + 2 + i * 3, 3.5, 0.4 + 0.18 * (i if which == "left" else 5 - i), TONE)
                         for i in range(6))
        return svg(w, h, b)

    # ---- menus: screentone paper, inverted selection ---------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PAPER) + screentone(w, h, w / 2, 0.9, "#d6d6d0"))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, INK) + rect(4, 3, w - 8, h - 6, "none", PAPER, 0.8))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=PAPER if hilite else INK)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PAPER))

    def area(self, w, h):
        return svg(w, h, frame(w, h, INK, 1.5, fill=PAPER))

    def push_button(self, w, h, state):
        if state == "normal":
            b = rect(1, 1, w - 2, h - 2, PAPER, INK, 2)
        elif state == "hover":
            b = rect(1, 1, w - 2, h - 2, PAPER, INK, 2) + screentone(w, h, 5, 0.9, TONE, 3, 3)
        else:
            b = rect(1, 1, w - 2, h - 2, INK, INK, 2)
        return svg(w, h, b)

    def check(self, s, on, hover):
        b = rect(1, 1, s - 2, s - 2, PAPER_DK if hover else PAPER, INK, 1.6)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 3.5} L{s - 2.5},2.5", stroke=RED if hover else INK, sw=2.4)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c = s / 2
        if on:
            return svg(s, s, pokeball(c, c, c - 1, RED, INK, PAPER, 1.3))
        return svg(s, s, circle(c, c, c - 1, PAPER_DK if hover else PAPER, INK, 1.4))

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 2, INK))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, INK, 1.4, fill=PAPER))

    def knob(self, w, h, vertical, clicked):
        return svg(w, h, rect(0, 0, w, h, RED if clicked else INK))

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, INK) + circle(s / 2, s / 2, 1.8, PAPER))

    # ---- popups: speech bubbles and a thought-bubble trail -----------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(1, 1, w - 2, h - 2, PAPER, INK, 2, rx=9))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(1, 1, w - 2, h - 2, INK, INK, 2, rx=9))

    def bubble(self, s, i):
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 1, PAPER, INK, 1.6 if s > 6 else 1.2))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, INK) + rect(0, 0, w, 2, RED))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PAPER))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, INK) + rect(1, 1, w - 2, h - 2, PAPER)
                   + screentone(w, h, 4, 0.8, TONE, 2, 2) + rect(1, 1, w - 2, 3, INK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, RED, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, PAPER))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, INK, 1.5, fill=PAPER))

    def arrow(self, s, direction):
        c = s / 2
        d = {"up": f"M3,{s-4} L{c},4 L{s-3},{s-4}Z", "down": f"M3,4 L{c},{s-4} L{s-3},4Z",
             "left": f"M{s-4},3 L4,{c} L{s-4},{s-3}Z", "right": f"M4,3 L{s-4},{c} L4,{s-3}Z"}[direction]
        return svg(s, s, rect(0, 0, s, s, PAPER) + path(d, fill=INK))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, PAPER) + rect(w - 2, 0, 2, h, INK) + rect(w - 5, 0, 1, h, INK))
        return svg(w, h, rect(0, 0, w, h, PAPER) + rect(0, h - 2, w, 2, INK) + rect(0, h - 5, w, 1, INK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
