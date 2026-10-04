"""Kalos: Xerneas and Yveltal - life's teal light against destruction's crimson,
with Xerneas' rainbow antler gems."""

from base import Art, circle, frame, hgrad, path, rect, svg, vgrad
from themes._common import diamond, glyph, tri_arrow

TEAL_DK = "#00556c"
TEAL = "#1a8a9a"
CYAN = "#88eaf3"
NAVY = "#141a26"
NAVY_DK = "#0c1018"
XBLUE = "#3a5aa0"
CRIMSON = "#c02030"
CRIMSON_DK = "#7a1020"
YV_DK = "#2b0637"
PEACH = "#ff9f8e"
PURPLE = "#7c317a"
ANTLER = "#b8b080"
GEMS = ["#f08a30", "#f080c0", "#a070e0", "#60d8f0", "#f0d040"]
SLATE_L, SLATE_R = "#2a3a44", "#3a2a36"     # inactive ends

FILTERS = '<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.3"/></filter>'


class Kalos(Art):
    NAME = "Kalos"
    WALLPAPER = "9/wp1877108-yveltal-wallpapers.jpg"
    BG_SOLID = NAVY

    P = dict(base=NAVY, panel=NAVY, raised=XBLUE, line=CYAN, line_dim="#3a4458",
             accent=TEAL, accent_hi=CYAN, text="#d8e4f0", text_dim="#7a8498",
             sel=PURPLE, sel_text="#ffffff", danger=CRIMSON, shadow="#06080e")

    M = dict(Art.M, title_h=26, side=5, bottom=7, corner=26, btn=18, btn_gap=4, btn_right=7,
             title_edge=(56, 24), title_pad_l=50, menu_title_h=24)

    FONTS = dict(border="pango:DejaVu Serif Bold 9", menu="pango:DejaVu Sans 9",
                 dialog="pango:DejaVu Sans 9", small="pango:DejaVu Sans Bold 8")

    TEXT = dict(title_active="#ffffff", title_inactive="#8a94a8", menu_title="#ffffff",
                menu="#d8e4f0", menu_hilite="#ffffff", dialog="#d8e4f0", tooltip="#e8f0f8")
    TITLE_JUSTIFY = 0
    TEXT_EFFECT = "__EFFECT_SHADOW"
    CURSOR = ("#ffffff", PURPLE)
    MATTE = dict(title=TEAL_DK, menu=NAVY, dialog=NAVY, popup=NAVY)
    ROFI = dict(border_color=PURPLE, radius=6, sel=(
        "background-image: linear-gradient(to right, #1a8a9a, #7c317a, #c02030); border-radius: 4px;"))

    # ---- window borders: teal on the left fading to crimson on the right -------

    def _ends(self, active):
        return (TEAL_DK, CRIMSON_DK) if active else (SLATE_L, SLATE_R)

    def _title_bg(self, w, active, part="full", dy=0):
        """part: full (left->right blend) | left | right (the solid end colours,
        for the emblem and buttons that sit on each end of the bar)."""
        TH = self.M["title_h"]
        l, r = self._ends(active)
        defs = hgrad("tb", [(0, l), (0.5, PURPLE if active else "#34303e"), (1, r)])
        # vertical shading, in title-bar coordinates so slices line up
        defs += (f'<linearGradient id="shu" gradientUnits="userSpaceOnUse" x1="0" y1="{-dy}" x2="0" y2="{TH - dy}">'
                 '<stop offset="0" stop-color="#ffffff" stop-opacity="0.2"/>'
                 '<stop offset="0.45" stop-color="#ffffff" stop-opacity="0"/>'
                 '<stop offset="1" stop-color="#000000" stop-opacity="0.35"/></linearGradient>')
        fill = {"full": "url(#tb)", "left": l, "right": r}[part]
        b = rect(0, -dy, w, TH, fill) + rect(0, -dy, w, TH, "url(#shu)")
        b += rect(0, TH - 2 - dy, w, 1, CYAN if (active and part != "right") else (PEACH if active else "#4a4458"))
        b += rect(0, TH - 1 - dy, w, 1, NAVY_DK)
        return defs, b

    def title(self, w, h, active):
        defs, b = self._title_bg(w, active)
        # the right half of the accent line is Yveltal's peach
        if active:
            defs += hgrad("ln", [(0, CYAN), (1, PEACH)])
            b += rect(0, h - 2, w, 1, "url(#ln)")
        # Xerneas' antler: a branching beam tipped with rainbow gems
        c = ANTLER if active else "#6a6a70"
        b += path("M4,20 C14,16 24,12 42,6", stroke=c, sw=2)
        for (x1, y1, x2, y2) in ((12, 16.5, 13, 6), (22, 12.6, 26, 3), (31, 9.5, 40, 13)):
            b += path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=1.6)
        for (x, y), gem in zip(((13, 5), (26, 2.5), (42, 5.5), (40, 13.5)), GEMS):
            b += f'<ellipse cx="{x}" cy="{y}" rx="2.2" ry="1.6" fill="{gem if active else "#7a7a84"}"/>'
        b += rect(w - 1, 0, 1, h, NAVY_DK)
        return svg(w, h, b, defs)

    def menu_title(self, w, h):
        b = rect(0, 0, w, h, "url(#g)") + rect(0, h - 2, w, 1, "url(#ln)") + rect(0, h - 1, w, 1, NAVY_DK)
        for i, x in enumerate((8, 14, 20)):
            b += diamond(x, h / 2 - 1, 2.6, 4, GEMS[i]) + diamond(w - x, h / 2 - 1, 2.6, 4, GEMS[i + 1])
        return svg(w, h, b, hgrad("g", [(0, TEAL_DK), (0.5, PURPLE), (1, CRIMSON_DK)])
                   + hgrad("ln", [(0, CYAN), (1, PEACH)]))

    def emblem(self, s, state):
        """Life and destruction: a circle split teal/crimson around a gem."""
        defs, b = self._title_bg(s, state != "inactive", "left")
        cx, cy, r = s / 2 + 1, s / 2 - 1.5, 7.5
        lc, rc = (TEAL, CRIMSON) if state != "inactive" else ("#4a5a64", "#5a4a54")
        if state == "hover":
            b += circle(cx, cy, r + 1.5, CYAN, extra='opacity="0.6" filter="url(#g)"')
        b += path(f"M{cx},{cy - r} A{r},{r} 0 0 0 {cx},{cy + r} Z", fill=lc)
        b += path(f"M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} Z", fill=rc)
        b += circle(cx, cy, r, "none", CYAN if state != "inactive" else "#6a7484", 1)
        b += diamond(cx, cy, 2.8, 4.2, GEMS[1] if state != "inactive" else "#9a9aa4", "#ffffff", 0.6)
        return svg(s, s, b, defs + FILTERS)

    def button(self, kind, s, state):
        by = (self.M["title_h"] - s) // 2
        defs, b = self._title_bg(s, state != "inactive", "right", by)
        gem = {"iconify": GEMS[3], "max": GEMS[4], "close": PEACH}[kind]
        fill, rim, g = {"inactive": ("#2a2430", "#6a6474", "#8a8494"),
                        "active": (YV_DK, gem, "#ffffff"),
                        "hover": (gem, "#ffffff", YV_DK),
                        "clicked": (PURPLE, "#ffffff", "#ffffff")}[state]
        c = s / 2
        if state == "hover":
            b += '<g filter="url(#g)" opacity="0.7">' + diamond(c, c, c - 1.5, c - 1.5, gem) + "</g>"
        b += diamond(c, c, c - 0.8, c - 0.8, fill, rim, 1.3)
        b += glyph(kind, s, g, 1.7, 6.2)
        return svg(s, s, b, defs + FILTERS)

    # Xerneas' teal on the left of every window, Yveltal's crimson on the right.

    def side(self, w, h, active, which):
        l, r = self._ends(active)
        fill = l if which == "left" else r
        inner = (CYAN if which == "left" else PEACH) if active else "#4a4458"
        b = rect(0, 0, w, h, fill)
        b += (rect(0, 0, 1, h, NAVY_DK) + rect(w - 1, 0, 1, h, inner) if which == "left"
              else rect(w - 1, 0, 1, h, NAVY_DK) + rect(0, 0, 1, h, inner))
        return svg(w, h, b)

    def bottom(self, w, h, active):
        l, r = self._ends(active)
        defs = hgrad("b", [(0, l), (0.5, PURPLE if active else "#34303e"), (1, r)])
        defs += hgrad("ln", [(0, CYAN if active else "#4a4458"), (1, PEACH if active else "#4a4458")])
        return svg(w, h, rect(0, 0, w, h, "url(#b)") + rect(0, 0, w, 1, "url(#ln)") + rect(0, h - 1, w, 1, NAVY_DK), defs)

    def corner(self, w, h, active, which):
        l, r = self._ends(active)
        fill = l if which == "left" else r
        inner = (CYAN if which == "left" else PEACH) if active else "#4a4458"
        b = rect(0, 0, w, h, fill) + rect(0, h - 1, w, 1, NAVY_DK)
        if which == "left":
            b += rect(0, 0, 1, h, NAVY_DK) + rect(4, 0, w - 4, 1, inner)
            gx = 10
        else:
            b += rect(w - 1, 0, 1, h, NAVY_DK) + rect(0, 0, w - 4, 1, inner)
            gx = w - 10
        if active:
            b += diamond(gx, h / 2 + 0.5, 2, 2.6, GEMS[0] if which == "left" else GEMS[1])
        return svg(w, h, b)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def menu_sel(self, w, h):
        return svg(w, h, rect(2, 1, w - 4, h - 2, "url(#s)", rx=4)
                   + rect(4, 1.5, w - 8, 1, "#ffffff", extra='opacity="0.25"'),
                   hgrad("s", [(0, TEAL), (0.5, PURPLE), (1, CRIMSON)]))

    def menu_arrow(self, w, h, hilite):
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        return base.replace("</svg>", diamond(w - 12, h / 2, 3, 4.5, "#ffffff" if hilite else GEMS[1]) + "</svg>")

    # ---- dialogs ------------------------------------------------------------

    def panel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def area(self, w, h):
        return svg(w, h, frame(w, h, "#2a3a50", 1, rx=4, fill=NAVY_DK))

    def push_button(self, w, h, state):
        fill, edge = {"normal": ("#1e2a3a", CYAN), "hover": ("#2a2236", PEACH), "clicked": (PURPLE, "#ffffff")}[state]
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, fill, edge, 1, rx=4)
                   + rect(3, 2, w - 6, 1, "#ffffff", extra='opacity="0.15"'))

    def check(self, s, on, hover):
        b = rect(0.5, 0.5, s - 1, s - 1, NAVY_DK, PEACH if hover else CYAN, 1, rx=2)
        if on:
            b += diamond(s / 2, s / 2, 3.6, 4.8, GEMS[1], "#ffffff", 0.6)
        return svg(s, s, b)

    def radio(self, s, on, hover):
        c, r = s / 2, s / 2 - 1
        if on:
            b = path(f"M{c},{c - r} A{r},{r} 0 0 0 {c},{c + r} Z", fill=TEAL)
            b += path(f"M{c},{c - r} A{r},{r} 0 0 1 {c},{c + r} Z", fill=CRIMSON)
            b += circle(c, c, r, "none", "#ffffff", 1) + circle(c, c, 1.6, "#ffffff")
            return svg(s, s, b)
        return svg(s, s, circle(c, c, r, NAVY_DK, PEACH if hover else CYAN, 1))

    def separator(self, w, h):
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, "url(#g)"), hgrad("g", [(0, TEAL), (1, CRIMSON)]))

    def trough(self, w, h, vertical):
        return svg(w, h, frame(w, h, "#2a3a50", 1, rx=min(w, h) / 2, fill=NAVY_DK))

    def knob(self, w, h, vertical, clicked):
        g = hgrad("k", [(0, TEAL), (1, CRIMSON)]) if not clicked else hgrad("k", [(0, GEMS[1]), (1, GEMS[2])])
        return svg(w, h, rect(0.5, 0.5, w - 1, h - 1, "url(#k)", "#ffffff", 0.8, rx=min(w, h) / 2), g)

    def grip(self, s):
        return svg(s, s, rect(0, 0, s, s, PURPLE) + diamond(s / 2, s / 2, 2.4, 3.2, "#ffffff"))

    # ---- popups: dark glass edged teal-to-crimson ------------------------------

    def tooltip(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#e)", rx=5) + rect(1.5, 1.5, w - 3, h - 3, NAVY, rx=4),
                   hgrad("e", [(0, CYAN), (0.5, PURPLE), (1, PEACH)]))

    def popup(self, w, h):
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "#ffffff", rx=5) + rect(1.5, 1.5, w - 3, h - 3, "url(#s)", rx=4),
                   hgrad("s", [(0, TEAL), (0.5, PURPLE), (1, CRIMSON)]))

    def bubble(self, s, i):
        return svg(s, s, diamond(s / 2, s / 2, s / 2 - 1.5, s / 2 - 0.5, GEMS[i - 1], "#ffffff", 0.6))

    def progress_bar(self, w, h):
        return svg(w, h, rect(0, 0, w, h, "url(#p)", rx=3), hgrad("p", [(0, TEAL), (0.5, PURPLE), (1, CRIMSON)]))

    # ---- pager / iconbox ------------------------------------------------------

    def pager_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def pager_win(self, w, h):
        return svg(w, h, rect(0, 0, w, h, CYAN) + rect(1, 1, w - 2, h - 2, XBLUE) + rect(1, 1, w - 2, 3, TEAL_DK))

    def pager_sel(self, w, h):
        return svg(w, h, frame(w, h, PEACH, 2))

    def iconbox_bg(self, w, h):
        return svg(w, h, rect(0, 0, w, h, NAVY))

    def icon_button(self, w, h):
        return svg(w, h, frame(w, h, "#2a3a50", 1, rx=4, fill=NAVY_DK))

    def arrow(self, s, direction):
        return svg(s, s, tri_arrow(s, direction, NAVY, CYAN))

    def dragbar(self, w, h, vertical):
        g = (vgrad if vertical else hgrad)("d", [(0, TEAL_DK), (0.5, PURPLE), (1, CRIMSON_DK)])
        if vertical:
            return svg(w, h, rect(0, 0, w, h, "url(#d)") + rect(w - 1, 0, 1, h, NAVY_DK), g)
        return svg(w, h, rect(0, 0, w, h, "url(#d)") + rect(0, h - 1, w, 1, NAVY_DK), g)

    def startup_bar(self, w, h):
        return self.dragbar(w, h, False)


    # ---- shape: Xerneas' rainbow-gemmed antlers on top, Yveltal's wing out of the right side ----

    SHAPE = dict(top=30, right=30)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def antlers(active):
            c = ANTLER if active else "#6a6a70"
            gems = GEMS if active else ["#7a7a84"] * len(GEMS)
            b = ""
            for base, branches in ((14, ((14, 18, 6, 4), (12, 12, 2, 14), (13, 22, 24, 10))),
                                   (34, ((34, 18, 40, 4), (36, 12, 46, 12), (35, 22, 28, 9)))):
                b += path(f"M{base},{T + 3} L{base},{T - 8}", stroke=c, sw=2.6)
                for i, (x1, y1, x2, y2) in enumerate(branches):
                    b += path(f"M{x1},{y1 + T - 30} Q{(x1 + x2) / 2 + 3},{(y1 + y2) / 2 + T - 32} {x2},{y2 + T - 30}",
                              stroke=c, sw=2)
                    b += f'<ellipse cx="{x2}" cy="{y2 + T - 30}" rx="2.6" ry="1.9" fill="{gems[(i + base) % len(gems)]}"/>'
            return svg(50, T + 3, b)

        def wing(active):
            body, edge = (CRIMSON, YV_DK) if active else ("#4a3a44", "#2a2030")
            b = ""
            for y, reach, rise in ((4, 33, 0), (22, 30, -2), (40, 24, -4)):
                d = f"M0,{y} L0,{y + 14} L{reach},{y + rise + 2} L{reach - 9},{y + rise + 6} Z"
                b += path(d, fill=body, stroke=edge, sw=1.3)
                b += path(f"M2,{y + 7} L{reach - 4},{y + rise + 3}", stroke=edge, sw=1)
            return svg(35, 58, b)

        return [("antlers", 50, T + 3, "tl", 0, 0, antlers),
                ("wing", 35, 58, "tr", 0, T + 6, wing)]
