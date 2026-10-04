"""Academy: the Scarlet/Violet battle splash - a dark stage, scarlet and violet flame streaks,
Terastal crystal sparkles."""

from base import circle, path, rect, sparkle
from themes._common import diamond, starfield
from themes._kit import Kit

STAGE = "#16161e"
STAGE_LT = "#262634"
SCARLET = "#e8302a"
VIOLET = "#7a3ac8"
ORANGE = "#ff8a2a"
TEAL = "#2ac8b8"
CRYSTAL = "#bfe8ff"
WHITE = "#f4f4fa"


def tera(cx, cy, r, fill=CRYSTAL, edge="#ffffff"):
    """A Tera crystal: a faceted diamond with a highlight facet."""
    return (diamond(cx, cy, r * 0.75, r, fill, edge, 0.7)
            + path(f"M{cx},{cy - r} L{cx + r * 0.75},{cy} L{cx},{cy + r * 0.2} Z", fill="#ffffff", extra='opacity="0.45"'))


def streaks(x, y, active):
    a, b = (SCARLET, VIOLET) if active else ("#4a3a40", "#3a3448")
    return (path(f"M{x},{y + 12} C{x + 12},{y + 2} {x + 24},{y + 10} {x + 40},{y + 2}", stroke=a, sw=2.4)
            + path(f"M{x},{y + 16} C{x + 14},{y + 8} {x + 26},{y + 15} {x + 40},{y + 8}", stroke=b, sw=2.4))


class Academy(Kit):
    NAME = "Academy"
    WALLPAPER = "18/wallpapersden.com_hd-pokemon-scarlet-and-violet_1920x1105.jpg"
    BG_SOLID = STAGE

    TITLE = (STAGE_LT, STAGE)
    TITLE_DIM = ("#22222a", "#1a1a20")
    TITLE_HI = "#3e3e50"
    BAND, BAND2, BAND_DIM, OUTER = SCARLET, VIOLET, "#2e2e38", "#08080c"
    FRAME, FRAME_IN, FRAME_DIM, FRAME_IN_DIM = STAGE, VIOLET, "#1a1a20", "#2e2e38"
    BG, BG_DK, MENU_BG, LINE = "#1a1a24", "#111118", "#14141c", "#34344a"
    ACCENT, ACCENT_HI, ACCENT_FG = VIOLET, "#a46cf0", "#ffffff"
    SEL, SEL_EDGE = (SCARLET, VIOLET), CRYSTAL
    POPUP_BG, POPUP_EDGE = "#20202c", CRYSTAL
    BTN_SHAPE = "diamond"
    BTN = dict(inactive=("#24242c", "#4a4a58", "#8a8a98"), active=(STAGE, CRYSTAL, CRYSTAL),
               hover=(TEAL, "#ffffff", "#ffffff"), close_hover=(SCARLET, "#ffffff", "#ffffff"),
               clicked=(VIOLET, "#ffffff", "#ffffff"))
    MENU_BG_TILE = 40
    FONTS = dict(Kit.FONTS, border="pango:Adwaita Sans ExtraBold 9")
    TEXT = dict(title_active=WHITE, title_inactive="#8a8a98", menu_title=WHITE,
                menu="#dcdcea", menu_hilite="#ffffff", dialog="#dcdcea", tooltip=WHITE)
    CURSOR = (WHITE, VIOLET)

    def ornament(self, active):
        return streaks(4, 2, active)

    def emblem_art(self, cx, cy, state):
        if state == "inactive":
            return tera(cx, cy, 8, "#3a3a48", "#5a5a6a")
        b = circle(cx, cy, 9, TEAL, extra='opacity="0.6" filter="url(#g)"') if state == "hover" else ""
        return b + tera(cx, cy, 8.5)

    def corner_mark(self, x, y, active, which):
        return sparkle(x, y, 3, CRYSTAL) if active else ""

    def check_mark(self, s, hover):
        return tera(s / 2, s / 2, s / 2 - 2)

    def radio_mark(self, s, hover):
        return circle(s / 2, s / 2, s / 2 - 3, SCARLET) + circle(s / 2 + 1.5, s / 2, s / 2 - 4.5, VIOLET)

    def bubble_art(self, s, i):
        return sparkle(s / 2, s / 2, s / 2 - 0.3, [CRYSTAL, SCARLET, VIOLET, TEAL][i - 1])

    def menu_tile(self, w, h):
        return rect(0, 0, w, h, self.MENU_BG) + starfield(w, h, 18, 6, [CRYSTAL, "#ffffff", ORANGE], 0.7)


    # ---- shape: a Terastal crystal crown rising off the top-left corner ----

    SHAPE = dict(top=26)

    def decorations(self):
        from base import circle, path, rect, svg
        from themes._common import mirror, mute, plump_ear
        T, SW = self.SHAPE.get("top", 0), self.M["side"]

        def crown(active):
            fill, edge = (CRYSTAL, "#ffffff") if active else ("#3a3a48", "#5a5a6a")
            b = tera(10, T - 8, 9, fill, edge) + tera(30, T - 13, 13, fill, edge) + tera(48, T - 6, 8, fill, edge)
            if active:
                b += sparkle(40, 4, 3, "#ffffff") + sparkle(4, 10, 2, ORANGE)
            return svg(58, T + 3, b)

        return [("crown", 58, T + 3, "tl", 0, 0, crown)]
