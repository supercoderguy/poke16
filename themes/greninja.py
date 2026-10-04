"""Greninja (Ash-Greninja): navy body, the water shuriken, red crest, bright cyan water splashes."""

from base import circle, path, rect
from themes._kit import Kit

NAVY = "#1a2a6a"
NAVY_DK = "#0e1840"
BLUE = "#2a6ae0"
CYAN = "#3ae8f0"
AQUA = "#a8f4f8"
WATER = "#0a6aa8"
RED = "#d8203a"
CREAM = "#f8e8b0"
PINK = "#e8a0c0"      # the tongue scarf


def shuriken(cx, cy, r, fill=CYAN, core=NAVY):
    """The water shuriken: four curved blades."""
    blade = f"M0,0 C{r * 0.3},{-r * 0.5} {r * 0.9},{-r * 0.7} {r},{-r * 0.2} C{r * 0.6},{-r * 0.3} {r * 0.3},{-r * 0.1} 0,0 Z"
    b = f'<g transform="translate({cx},{cy})">'
    b += "".join(f'<g transform="rotate({a})">' + path(blade, fill=fill) + "</g>" for a in (0, 90, 180, 270))
    return b + circle(0, 0, r * 0.22, core) + "</g>"


def splash(x, y, k, fill=AQUA):
    return path(f"M{x},{y + 8 * k} C{x + 4 * k},{y} {x + 8 * k},{y + 10 * k} {x + 12 * k},{y + 2 * k} "
                f"C{x + 14 * k},{y + 9 * k} {x + 20 * k},{y + 4 * k} {x + 22 * k},{y + 8 * k} Z", fill=fill)


class Greninja(Kit):
    NAME = "Greninja"
    WALLPAPER = "23/wp3725297-greninja-hd-wallpapers.jpg"
    BG_SOLID = WATER

    TITLE = ("#2a3e8a", NAVY_DK)
    TITLE_DIM = ("#262e44", "#1c2234")
    TITLE_HI = "#4a62b8"
    BAND, BAND2, BAND_DIM, OUTER = CYAN, RED, "#2e3648", "#060c24"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = NAVY_DK, CYAN, "#1c2234", "#2e3648"
    BG, BG_DK, MENU_BG, LINE = "#0f1e48", "#091434", NAVY_DK, "#22408a"
    ACCENT, ACCENT_HI, ACCENT_FG = CYAN, AQUA, NAVY_DK
    SEL, SEL_EDGE = (BLUE, WATER), RED
    POPUP_BG, POPUP_EDGE = AQUA, NAVY
    BTN = dict(inactive=("#262e44", "#4a5468", "#8a94a8"), active=(NAVY_DK, CYAN, CYAN),
               hover=(CYAN, "#ffffff", NAVY_DK), close_hover=(RED, "#ffffff", "#ffffff"),
               clicked=(BLUE, "#ffffff", "#ffffff"))
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans Black Italic 9")
    TEXT = dict(title_active="#f0fcff", title_inactive="#8a94a8", menu_title="#f0fcff",
                menu="#d8ecf8", menu_hilite="#ffffff", dialog="#d8ecf8", tooltip=NAVY_DK)
    CURSOR = (AQUA, NAVY_DK)

    def ornament(self, active):
        return splash(4, 5, 1.6, AQUA if active else "#3a4458") + (
            path("M30,4 L42,10 L30,16 L34,10 Z", fill=RED if active else "#4a3a44"))

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return shuriken(cx, cy, 8, "#3a4458", "#1c2234")
        b = circle(cx, cy, 10, CYAN, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        return b + shuriken(cx, cy, 8.5)

    def corner_mark(self, x, y, active, which):
        return splash(x - 5, y - 3, 0.45, AQUA) if active else ""

    def check_mark(self, s, hover):
        return shuriken(s / 2, s / 2, s / 2 - 2)

    def radio_mark(self, s, hover):
        return circle(s / 2, s / 2, s / 2 - 3, CYAN) + circle(s / 2, s / 2, 1.5, RED)

    def bubble_art(self, s, i):
        return circle(s / 2, s / 2, s / 2 - 0.5, AQUA, CYAN, 0.8)


    # ---- shape: its tongue scarf trailing out of the left side, a water splash on top ----

    SHAPE = dict(top=14, left=34)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def scarf(active):
            c, e = (PINK, "#a0607a") if active else ("#3a3a48", "#2a2a34")
            d = "M39,6 C26,4 20,14 10,12 C4,11 2,6 0,4 C2,14 8,20 16,20 C24,20 30,14 39,18 Z"
            d2 = "M39,20 C30,22 26,32 14,34 C8,35 4,32 2,30 C6,40 16,42 24,38 C30,35 34,30 39,30 Z"
            return svg(39, 44, path(d, fill=c, stroke=e, sw=1.2) + path(d2, fill=c, stroke=e, sw=1.2))

        def spray(active):
            return svg(40, T + 3, splash(2, T + 3 - 10 * 1.6, 1.6, AQUA if active else "#3a4458"))

        return [("scarf", 39, 44, "tl", 0, T + 8, scarf),
                ("splash", 40, T + 3, "tl", 40, 0, spray)]
