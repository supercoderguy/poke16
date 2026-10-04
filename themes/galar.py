"""Galar: Zacian and Zamazenta - sword-blue and shield-red, gold armour, sparkling light."""

from base import circle, path, rect, sparkle
from themes._kit import Kit

ZACIAN = "#2a5ac8"
ZACIAN_DK = "#16306e"
ZAMA = "#c8283a"
ZAMA_DK = "#6e1620"
GOLD = "#f0c040"
GOLD_LT = "#ffe28a"
SKY = "#8ac8f0"
WHITE = "#f4f6fc"
STEEL = "#1a2240"


def sword(x, y, k, blade=GOLD, edge=STEEL):
    """Zacian's sword, laid along the title bar."""
    return (path(f"M{x},{y + 4 * k} L{x + 30 * k},{y + 2.5 * k} L{x + 36 * k},{y + 4 * k} L{x + 30 * k},{y + 5.5 * k} Z",
                 fill=blade, stroke=edge, sw=0.7)
            + rect(x + 6 * k, y, 2.4 * k, 8 * k, ZAMA, edge, 0.6))


def shield(cx, cy, r, fill=ZAMA, rim=GOLD):
    """Zamazenta's shield."""
    d = f"M{cx},{cy - r} L{cx + r},{cy - r * 0.6} L{cx + r * 0.8},{cy + r * 0.4} L{cx},{cy + r} L{cx - r * 0.8},{cy + r * 0.4} L{cx - r},{cy - r * 0.6} Z"
    return path(d, fill=fill, stroke=rim, sw=1.2) + path(f"M{cx},{cy - r * 0.55} L{cx},{cy + r * 0.6}", stroke=rim, sw=1)


class Galar(Kit):
    NAME = "Galar"
    WALLPAPER = "24/wp4884503-pokemon-sword-shield-wallpapers.jpg"
    BG_SOLID = ZACIAN_DK

    TITLE = ("#3a6ad8", ZACIAN_DK)
    TITLE_DIM = ("#2a3044", "#20263a")
    TITLE_HI = "#6a9af0"
    BAND, BAND2, BAND_DIM, OUTER = GOLD, ZAMA, "#343a4e", "#080e24"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = STEEL, GOLD, "#20263a", "#343a4e"
    BG, BG_DK, MENU_BG, LINE = "#141c3a", "#0c1228", "#101834", "#2a3a6e"
    ACCENT, ACCENT_HI, ACCENT_FG = GOLD, GOLD_LT, STEEL
    SEL, SEL_EDGE = (ZACIAN, ZAMA), GOLD
    POPUP_BG, POPUP_EDGE = WHITE, GOLD
    BTN_SHAPE = "square"
    BTN = dict(inactive=("#262c40", "#4a5064", "#8a90a4"), active=(STEEL, GOLD, GOLD),
               hover=(SKY, "#ffffff", STEEL), close_hover=(ZAMA, "#ffffff", "#ffffff"),
               clicked=(ZACIAN, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 24
    FONTS = dict(Kit.FONTS, border="pango:DejaVu Serif Bold 9")
    TEXT = dict(title_active=WHITE, title_inactive="#8a90a4", menu_title=WHITE,
                menu="#dce4f8", menu_hilite="#ffffff", dialog="#dce4f8", tooltip=STEEL)
    CURSOR = (GOLD_LT, STEEL)

    def ornament(self, active):
        return sword(4, 7, 1.15, GOLD if active else "#5a5a54", STEEL)

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return shield(cx, cy, 7.5, "#3a3a48", "#5a5a64")
        b = circle(cx, cy, 9, GOLD, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        return b + shield(cx, cy, 7.5)

    def corner_mark(self, x, y, active, which):
        return sparkle(x, y, 3, GOLD_LT) if active else ""

    def check_mark(self, s, hover):
        return sparkle(s / 2, s / 2, s / 2 - 1.5, GOLD)

    def radio_mark(self, s, hover):
        return shield(s / 2, s / 2, s / 2 - 2.5)

    def bubble_art(self, s, i):
        return sparkle(s / 2, s / 2, s / 2 - 0.3, [GOLD_LT, SKY, WHITE, GOLD][i - 1])

    def menu_tile(self, w, h):
        return rect(0, 0, w, h, self.MENU_BG) + sparkle(6, 7, 2.5, "#2a3a70") + sparkle(18, 17, 2, "#2a3a70")


    # ---- shape: Zacian's sword rising from the top, Zamazenta's shield on the left side ----

    SHAPE = dict(top=30, left=24)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def blade(active):
            b, e, g = (GOLD, STEEL, ZAMA) if active else ("#5a5a54", STEEL, "#4a3a3e")
            # an upright sword: blade from the title bar up to a point, red crossguard near the base
            s = path(f"M12,{T + 3} L12,8 L16,0 L20,8 L20,{T + 3} Z", fill=b, stroke=e, sw=1)
            s += rect(5, T - 6, 22, 5, g, e, 0.8) + rect(14, T - 1, 4, 4, g)
            return svg(32, T + 3, s)

        def guard(active):
            fill, rim = (ZAMA, GOLD) if active else ("#4a3a3e", "#5a5a54")
            return svg(29, 32, shield(14, 15, 13, fill, rim))

        return [("sword", 32, T + 3, "tl", 50, 0, blade),
                ("shield", 29, 32, "tl", 0, T + 14, guard)]
