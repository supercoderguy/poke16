"""Koraidon: crimson and royal blue, feather crest, chest-tyre emblem, white zigzags."""

import math

from base import Art, circle, frame, hgrad, line, path, rect, svg, vgrad

MAROON = "#591713"
MAROON_DK = "#2e0d0f"
MAROON_XDK = "#1a0507"
CRIMSON = "#84231c"
CRIMSON_HI = "#a8302a"
SCARLET = "#f6463d"
BLUE = "#1d23b0"
BLUE_HI = "#2f3ae4"
BLUE_DK = "#10146a"
MAGENTA = "#c240df"
PINK = "#fd3fd3"
TYRE = "#292433"
BONE = "#f3eef3"
LAVENDER = "#c9c3d3"
YELLOW = "#f5b41c"
MUTED = "#4a2a2e"        # inactive crimson
MUTED_DK = "#34191c"
MUTED_BAND = "#3e3450"   # inactive blue band


def burst(cx, cy, r, n, inner, fill):
    """n-pointed starburst, like the red flash on Koraidon's chest."""
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(-90 + i * 180 / n)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return path("M" + " L".join(pts) + "Z", fill=fill)


def tyre(cx, cy, r, ring=BONE, core=SCARLET):
    """The black spiked wheel on Koraidon's chest."""
    b = ""
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        b += circle(cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a), r * 0.22, TYRE)
    b += circle(cx, cy, r * 0.86, TYRE)
    b += circle(cx, cy, r * 0.52, "none", ring, r * 0.18)
    b += burst(cx, cy, r * 0.36, 6, 0.45, core)
    return b


def zigzag(x, y, w, h, teeth, fill, up=True):
    """Row of sawtooth teeth, the white markings along Koraidon's body."""
    tw = w / teeth
    d = f"M{x},{y + h}" if up else f"M{x},{y}"
    for i in range(teeth):
        x0 = x + i * tw
        d += (f" L{x0 + tw / 2},{y} L{x0 + tw},{y + h}" if up
              else f" L{x0 + tw / 2},{y + h} L{x0 + tw},{y}")
    return path(d + "Z", fill=fill)


class Koraidon(Art):
    NAME = "Koraidon"
    WALLPAPER = "4/pokemon-scarletviolet-koraidon-01-2560x1440-1-2120901779.jpg"
    BG_SOLID = MAROON

    P = dict(base=MAROON_DK, panel=MAROON_DK, raised=CRIMSON, line=CRIMSON_HI, line_dim=MUTED,
             accent=BLUE, accent_hi=BLUE_HI, text=BONE, text_dim=LAVENDER,
             sel=BLUE, sel_text="#ffffff", danger=YELLOW, shadow="#240608")

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=28, btn=18, btn_gap=4, btn_right=7,
             title_edge=(60, 24), title_pad_l=50, menu_title_h=24)

    FONTS = dict(border="pango:Adwaita Sans ExtraBold 9", menu="pango:Adwaita Sans SemiBold 9",
                 dialog="pango:Adwaita Sans 9", small="pango:Adwaita Sans Bold 8")

    TEXT = dict(title_active="#ffffff", title_inactive="#b89a9c", menu_title="#ffffff",
                menu="#f1e2e2", menu_hilite="#ffffff", dialog="#f1e2e2", tooltip="#3a1216")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    CURSOR = (BONE, BLUE)
    ROFI = dict(border_color=BLUE, radius=4, sel=(
        "background-image: linear-gradient(to right, #2f3ae4, #1d23b0); "
        "border: 0 0 0 4px; border-color: #f3eef3; border-radius: 3px;"))
    MATTE = dict(title=CRIMSON, menu=MAROON_DK, dialog=MAROON_DK, popup=BONE)

    # ---- window borders -----------------------------------------------------

    def _title_bg(self, w, active, dy=0):
        """Title background as seen through a w-wide window starting dy px down
        the title bar, so buttons and the emblem can paint an exact slice."""
        TH = self.M["title_h"]
        top, bot = (CRIMSON_HI, "#6a1a15") if active else (MUTED, MUTED_DK)
        defs = (f'<linearGradient id="tb" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" x2="0" y2="{TH - dy}">'
                f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>')
        b = rect(0, -dy, w, TH, "url(#tb)")
        b += rect(0, -dy, w, 1, "#c8453a" if active else "#5c3438")                   # top highlight
        b += rect(0, TH - 4 - dy, w, 3, BLUE if active else MUTED_BAND)               # blue band
        b += rect(0, TH - 1 - dy, w, 1, MAROON_XDK)
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        # feather crest: a white blade behind a blue one tipped with magenta
        defs += (f'<linearGradient id="cr" x1="0" y1="0" x2="1" y2="0">'
                 f'<stop offset="0" stop-color="{BLUE if active else MUTED_BAND}"/>'
                 f'<stop offset="0.4" stop-color="{BLUE_HI if active else MUTED_BAND}"/>'
                 f'<stop offset="0.7" stop-color="{MAGENTA if active else "#5c4868"}"/>'
                 f'<stop offset="1" stop-color="{PINK if active else "#6c5470"}"/></linearGradient>')
        b += path("M2,15 C12,4 26,2 42,4 C30,7 18,10 6,17 Z", fill=LAVENDER if active else "#8a7a88")
        b += path("M3,20 C14,10 28,8 44,11 C32,13 19,16 7,21 Z", fill="url(#cr)")
        b += rect(w - 1, 0, 1, h, MAROON_XDK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, 0, w, 1, "#c8453a")
        b += rect(0, h - 4, w, 3, BLUE) + rect(0, h - 1, w, 1, MAROON_XDK)
        b += zigzag(4, h - 9, 18, 5, 3, BONE) + zigzag(w - 22, h - 9, 18, 5, 3, BONE)
        return svg(w, h, b, vgrad("g", [(0, CRIMSON_HI), (1, "#6a1a15")]))

    def emblem(self, s, state):
        defs, b = self._title_bg(s, state != "inactive")
        if state == "hover":
            b += circle(s / 2, s / 2 - 1.5, 10.5, YELLOW, extra='opacity="0.55" filter="url(#glow)"')
        ring = YELLOW if state == "hover" else (BONE if state == "active" else LAVENDER)
        core = SCARLET if state != "inactive" else "#a05050"
        b += tyre(s / 2, s / 2 - 1.5, 9.5, ring, core)
        return svg(s, s, b, defs + '<filter id="glow"><feGaussianBlur stdDeviation="1.6"/></filter>')

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", by)
        top, bot = {"inactive": ("#5a4a68", "#3a3048"), "active": (BLUE_HI, BLUE),
                    "hover": ("#d765f0", "#8a2aa8"), "clicked": (BLUE_DK, "#0a0d48")}[state]
        if kind == "close" and state == "hover":
            top, bot = "#ffd35a", "#d99200"
        defs += vgrad("bt", [(0, top), (1, bot)])
        b += rect(0.5, 0.5, s - 1, s - 1, "url(#bt)", "#0b0c3a" if state != "inactive" else "#241a2a", 1, rx=4)
        b += rect(2, 1.5, s - 4, 1, "#ffffff", extra='opacity="0.35"')         # gloss
        g = {"inactive": "#b8a8bc", "active": "#ffffff", "hover": "#ffffff", "clicked": LAVENDER}[state]
        if kind == "close" and state == "hover":
            g = "#3a1216"
        m = 5
        glyph = {"close": path(f"M{m},{m} L{s-m},{s-m} M{s-m},{m} L{m},{s-m}", stroke=g, sw=2.4),
                 "max": rect(m, m, s - 2 * m, s - 2 * m, "none", g, 2, rx=1) + rect(m, m, s - 2 * m, 2.5, g),
                 "iconify": rect(m, s - m - 2.5, s - 2 * m, 2.6, g, rx=1)}[kind]
        return svg(s, s, b + glyph, defs)

    def side(self, w, h, active, which):
        fill, inner = (CRIMSON, BLUE) if active else (MUTED, MUTED_BAND)
        b = rect(0, 0, w, h, fill)
        ox, ix = (0, w - 1) if which == "left" else (w - 1, 0)
        b += rect(ox, 0, 1, h, MAROON_XDK) + rect(ix, 0, 1, h, inner)
        return svg(w, h, b)

    def bottom(self, w, h, active):
        fill, inner = (CRIMSON, BLUE) if active else (MUTED, MUTED_BAND)
        return svg(w, h, rect(0, 0, w, h, fill) + rect(0, 0, w, 1, inner) + rect(0, h - 1, w, 1, MAROON_XDK))

    def corner(self, w, h, active, which):
        fill, inner = (CRIMSON, BLUE) if active else (MUTED, MUTED_BAND)
        tooth = BONE if active else "#8a7a88"
        b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, MAROON_XDK)
        # the inner blue line turns the corner from the side border into the bottom
        if which == "left":
            b += rect(4, 0, w - 4, 1, inner)
            b += rect(0, 0, 1, h, MAROON_XDK)
            b += zigzag(6, 2, 15, 4, 3, tooth)
        else:
            b += rect(0, 0, w - 5, 1, inner)
            b += rect(w - 1, 0, 1, h, MAROON_XDK)
            b += zigzag(w - 21, 2, 15, 4, 3, tooth)
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def menu_sel(self, w, h):
        b = rect(2, 1, w - 4, h - 2, "url(#s)", rx=3)
        b += path(f"M2,{1} L9,{h / 2} L2,{h - 1} Z", fill=BONE)                  # white fang
        b += rect(2, 1, w - 4, 1, "#ffffff", extra='opacity="0.25"')
        return svg(w, h, b, hgrad("s", [(0, BLUE_HI), (1, BLUE)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x, m = w - 15, h / 2
        tri = path(f"M{x},{m - 4.5} L{x + 6},{m} L{x},{m + 4.5} Z", fill=YELLOW if hilite else SCARLET)
        return base.replace("</svg>", tri + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#5a1a18", 1, rx=4, fill="#240a0c"))

    def push_button(self, w, h, state):
        top, bot, band = {"normal": (CRIMSON_HI, "#6a1a15", BLUE),
                          "hover": ("#c23a30", CRIMSON, MAGENTA),
                          "clicked": (BLUE, BLUE_DK, YELLOW)}[state]
        b = rect(0.5, 0.5, w - 1, h - 1, "url(#g)", MAROON_XDK, 1, rx=4)
        b += rect(3, h - 4, w - 6, 2, band, rx=1)
        b += rect(3, 1.5, w - 6, 1, "#ffffff", extra='opacity="0.25"')
        return svg(w, h, b, vgrad("g", [(0, top), (1, bot)]))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, BONE, YELLOW if hover else MAROON_XDK, 1, rx=2)
        if on:
            b += path(f"M3,{s / 2} L{s / 2 - 1},{s - 4} L{s - 3},3", stroke=BLUE, sw=2.4)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        b = circle(s / 2, s / 2, s / 2 - 0.5, BONE, YELLOW if hover else MAROON_XDK, 1)
        if on:
            b += tyre(s / 2, s / 2, s / 2 - 1.5, BONE, SCARLET)
        return svg(s, s, b)

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 1, w, 1, "#5a1a18") + rect(0, h / 2, w, 1, "#12040a"))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#5a1a18", 1, rx=min(w, h) / 2, fill=MAROON_XDK))

    def knob(self, w, h, vertical, clicked):
        g = vgrad("k", [(0, "#ffd35a"), (1, "#d99200")]) if clicked else vgrad("k", [(0, BLUE_HI), (1, BLUE)])
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", "#0b0c3a", 1, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, BLUE) + path(f"M1,{s - 2} L{s / 2},2 L{s - 1},{s - 2} Z", fill=BONE))

    # ---- popups: bone white with a crimson frame, like the white markings ----

    def tooltip(self, w, h):
        b = rect(0, 0, w, h, CRIMSON, rx=4) + rect(2, 2, w - 4, h - 4, BONE, rx=3)
        b += rect(2, h - 5, w - 4, 3, BLUE)
        return svg(w, h, b)

    def popup(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CRIMSON, rx=4) + rect(2, 2, w - 4, h - 4, BONE, rx=3))

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLUE_DK, rx=4) + rect(2, 2, w - 4, h - 4, BLUE, rx=3))

    def bubble(self, s, i):
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 0.5, BONE) + circle(s / 2, s / 2, s / 2 - 2.5, BLUE))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, BLUE, rx=3) + rect(2, 1, w - 4, 2, BLUE_HI, rx=1))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "#c23a30") + rect(1, 1, w - 2, h - 2, CRIMSON) + rect(1, 1, w - 2, 3, BLUE))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, YELLOW, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, MAROON_DK))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#5a1a18", 1, rx=4, fill="#240a0c"))

    def arrow(self, s, direction):
        c = s / 2
        d = {"up": f"M3,{s-4} L{c},4 L{s-3},{s-4}Z", "down": f"M3,4 L{c},{s-4} L{s-3},4Z",
             "left": f"M{s-4},3 L4,{c} L{s-4},{s-3}Z", "right": f"M4,3 L{s-4},{c} L4,{s-3}Z"}[direction]
        return svg(s, s, rect(0, 0, s, s, MAROON_DK) + path(d, fill=SCARLET))

    def dragbar(self, w, h, vertical):
        if vertical:
            return svg(w, h, rect(0, 0, w, h, CRIMSON) + rect(w - 4, 0, 3, h, BLUE) + rect(w - 1, 0, 1, h, MAROON_XDK))
        return svg(w, h, rect(0, 0, w, h, CRIMSON) + rect(0, h - 4, w, 3, BLUE) + rect(0, h - 1, w, 1, MAROON_XDK))

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)
