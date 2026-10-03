"""Shared framework for the wallpaper-based e16 themes.

A theme module subclasses `Art`, sets its palette/metrics/fonts and overrides
whichever drawing methods it wants to style.  Every drawing method returns an
SVG string; `Builder` renders them to PNG with rsvg-convert and writes the
e16 config files that reference them.
"""

import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent


# --------------------------------------------------------------------------
# SVG helpers
# --------------------------------------------------------------------------

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>')


def rect(x, y, w, h, fill="none", stroke=None, sw=1, rx=0, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s} {extra}/>'


def frame(w, h, stroke, sw=1, rx=0, fill="none", inset=0):
    """A stroked rectangle whose stroke sits fully inside the w*h box."""
    o = inset + sw / 2
    return rect(o, o, w - 2 * o, h - 2 * o, fill=fill, stroke=stroke, sw=sw, rx=rx)


def line(x1, y1, x2, y2, stroke, sw=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def circle(cx, cy, r, fill="none", stroke=None, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s} {extra}/>'


def path(d, fill="none", stroke=None, sw=1, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'


def vgrad(gid, stops):
    """stops: [(offset 0..1, colour), ...] top to bottom."""
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def hgrad(gid, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{s}</linearGradient>'


def rgb(hexcol):
    """'#rrggbb' -> 'r g b' for e16 colour fields."""
    h = hexcol.lstrip("#")
    return " ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def sparkle(cx, cy, r, fill):
    """Four-point star, as in the Umbreon wallpaper."""
    k = r * 0.22
    d = (f"M{cx},{cy - r} Q{cx + k},{cy - k} {cx + r},{cy} "
         f"Q{cx + k},{cy + k} {cx},{cy + r} Q{cx - k},{cy + k} {cx - r},{cy} "
         f"Q{cx - k},{cy - k} {cx},{cy - r}Z")
    return path(d, fill=fill)


def star5(cx, cy, r, fill, stroke=None, sw=1, inner=0.5, rot=0):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot - 90 + i * 36)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return path("M" + " L".join(pts) + "Z", fill=fill, stroke=stroke, sw=sw)


# --------------------------------------------------------------------------
# Default art: flat, palette driven.  Themes override what they want.
# --------------------------------------------------------------------------

class Art:
    NAME = "Unnamed"
    WALLPAPER = None          # path relative to ROOT
    WALLPAPER_MODE = "fill"   # fill (stretch) | fit (letterbox) | crop (centre-crop to 16:9)
    BG_SOLID = "#000000"

    # Palette.  Themes replace this wholesale.
    P = dict(
        base="#202020", panel="#2a2a2a", raised="#383838",
        line="#909090", line_dim="#505050",
        accent="#4a90d9", accent_hi="#7ab4f0",
        text="#e0e0e0", text_dim="#808080",
        sel="#4a90d9", sel_text="#ffffff",
        danger="#d94a4a", shadow="#000000",
    )

    # Metrics (pixels)
    M = dict(
        title_h=24,     # title bar height
        side=4,         # left/right border width
        bottom=6,       # bottom border height
        corner=20,      # bottom corner grip length
        btn=16,         # title button size
        btn_gap=4,      # gap between title buttons
        btn_right=6,    # margin right of the last button
        title_w=240,    # title image width (middle is stretched)
        title_edge=(40, 40),   # unstretched title ends (left, right)
        title_pad_l=10,        # title text inset from title part's left
        menu_title_h=22,
        menu_item_pad=(10, 22, 3, 3),
    )

    FONTS = dict(
        border="pango:DejaVu Sans bold 9",
        menu="pango:DejaVu Sans 9",
        dialog="pango:DejaVu Sans 9",
        small="pango:DejaVu Sans bold 8",
    )

    TEXT = dict(
        title_active="#ffffff", title_inactive="#808080", menu_title="#ffffff",
        menu="#e0e0e0", menu_hilite="#ffffff", dialog="#e0e0e0", tooltip="#e0e0e0",
    )
    CURSOR = ("#ffffff", "#000000")   # native X cursor fg / outline

    @property
    def MATTE(self):
        """Colour underneath each family of overlay images (see Builder.png)."""
        p = self.P
        return dict(title=p["panel"], menu=p["panel"], dialog=p["base"], popup=p["panel"])

    TITLE_JUSTIFY = 512       # 0 left, 512 centre, 1024 right
    MENU_BG_TILE = 0          # >0: menu_bg is drawn at this size and tiled
    TEXT_EFFECT = "__EFFECT_NONE"

    # ---- window borders -------------------------------------------------

    def title(self, w, h, active):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["panel"])
                   + line(0, h - 1.5, w, h - 1.5, p["accent"] if active else p["line_dim"], 3))

    def menu_title(self, w, h):
        return self.title(w, h, True)

    def emblem(self, s, state):
        """Left-most title square; opens the window menu. state: inactive|active|hover"""
        p = self.P
        c = {"inactive": p["line_dim"], "active": p["accent"], "hover": p["accent_hi"]}[state]
        return svg(s, s, rect(0, 0, s, s, p["panel"]) + circle(s / 2, s / 2, s / 4, c))

    def button(self, kind, s, state):
        """kind: close|max|iconify  state: inactive|active|hover|clicked"""
        p = self.P
        col = {"inactive": p["line_dim"], "active": p["line"],
               "hover": p["danger"] if kind == "close" else p["accent_hi"],
               "clicked": p["accent"]}[state]
        g = {"close": path(f"M5,5 L{s-5},{s-5} M{s-5},5 L5,{s-5}", stroke=p["text"], sw=2),
             "max": frame(s, s, p["text"], 1.5, inset=4),
             "iconify": line(5, s - 5, s - 5, s - 5, p["text"], 2)}[kind]
        return svg(s, s, rect(0.5, 0.5, s - 1, s - 1, col, rx=3) + g)

    def side(self, w, h, active, which):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["panel"]))

    def bottom(self, w, h, active):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["panel"]))

    def corner(self, w, h, active, which):
        """which: left|right"""
        return self.bottom(w, h, active)

    # ---- menus ------------------------------------------------------------

    def menu_bg(self, w, h):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["panel"]))

    def menu_sel(self, w, h):
        p = self.P
        return svg(w, h, rect(1, 0, w - 2, h, p["sel"], rx=3))

    def menu_arrow(self, w, h, hilite):
        """Submenu item: transparent except for an arrow in the right 22px."""
        p = self.P
        base = self.menu_sel(w, h) if hilite else svg(w, h, "")
        x = w - 14
        arrow = path(f"M{x},{h/2-4} L{x+4},{h/2} L{x},{h/2+4}", stroke=p["sel_text"] if hilite else p["accent"], sw=1.6)
        return base.replace("</svg>", arrow + "</svg>")

    # ---- dialogs / widgets ------------------------------------------------

    def panel(self, w, h):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["base"]))

    def area(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["line_dim"], 1, rx=3, fill=p["panel"]))

    def push_button(self, w, h, state):
        """state: normal|hover|clicked"""
        p = self.P
        fill = {"normal": p["raised"], "hover": p["raised"], "clicked": p["sel"]}[state]
        st = {"normal": p["line_dim"], "hover": p["accent"], "clicked": p["accent"]}[state]
        return svg(w, h, frame(w, h, st, 1, rx=4, fill=fill))

    def check(self, s, on, hover):
        p = self.P
        body = frame(s, s, p["accent"] if hover else p["line"], 1.5, rx=2, fill=p["panel"])
        if on:
            body += path(f"M4,{s/2} L{s/2-1},{s-5} L{s-4},4", stroke=p["accent_hi"], sw=2)
        return svg(s, s, body)

    def radio(self, s, on, hover):
        p = self.P
        body = circle(s / 2, s / 2, s / 2 - 1, p["panel"], p["accent"] if hover else p["line"], 1.5)
        if on:
            body += circle(s / 2, s / 2, s / 4, p["accent_hi"])
        return svg(s, s, body)

    def separator(self, w, h):
        p = self.P
        return svg(w, h, rect(0, h / 2 - 0.5, w, 1, p["line_dim"]))

    def trough(self, w, h, vertical):
        p = self.P
        return svg(w, h, frame(w, h, p["line_dim"], 1, rx=min(w, h) / 2, fill=p["base"]))

    def knob(self, w, h, vertical, clicked):
        p = self.P
        return svg(w, h, frame(w, h, p["accent_hi"] if clicked else p["accent"], 1,
                               rx=min(w, h) / 2, fill=p["raised"]))

    def grip(self, s):
        """Small mark centred on the iconbox scrollbar knob."""
        p = self.P
        return svg(s, s, circle(s / 2, s / 2, s / 4, p["accent_hi"]))

    # ---- misc popups ------------------------------------------------------

    def tooltip(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["accent"], 1, rx=5, fill=p["panel"]))

    def bubble(self, s, i):
        """Tooltip trail bubbles, i = 1 (nearest pointer) .. 4"""
        p = self.P
        return svg(s, s, circle(s / 2, s / 2, s / 2 - 1, p["panel"], p["accent"], 1))

    def popup(self, w, h):
        """Coords / warp-focus / progress backgrounds."""
        return self.tooltip(w, h)

    def popup_sel(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["accent"], 1, rx=5, fill=p["sel"]))

    def progress_bar(self, w, h):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["accent"], rx=3))

    # ---- pager / iconbox ----------------------------------------------------

    def pager_bg(self, w, h):
        return self.panel(w, h)

    def pager_win(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["line"], 1, fill=p["raised"]))

    def pager_sel(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["accent_hi"], 2))

    def iconbox_bg(self, w, h):
        return self.panel(w, h)

    def icon_button(self, w, h):
        p = self.P
        return svg(w, h, frame(w, h, p["line_dim"], 1, rx=4, fill=p["panel"]))

    def arrow(self, s, direction):
        p = self.P
        d = {"up": f"M4,{s-6} L{s/2},5 L{s-4},{s-6}", "down": f"M4,6 L{s/2},{s-5} L{s-4},6",
             "left": f"M{s-6},4 L5,{s/2} L{s-6},{s-4}", "right": f"M6,4 L{s-5},{s/2} L6,{s-4}"}[direction]
        return svg(s, s, frame(s, s, p["line_dim"], 1, rx=3, fill=p["panel"])
                   + path(d, stroke=p["accent"], sw=1.8))

    # ---- desktop ----------------------------------------------------------

    def dragbar(self, w, h, vertical):
        """Desktop drag bar (shown along the screen edge with several desktops)."""
        return self.panel(w, h)

    def startup_bar(self, w, h):
        p = self.P
        return svg(w, h, rect(0, 0, w, h, p["base"]) + rect(0, h - 3, w, 3, p["accent"]))


# --------------------------------------------------------------------------
# Builder: art -> PNGs + e16 config
# --------------------------------------------------------------------------

BUTTON_ACTIONS = {"close": "ACTION_KILL", "max": "ACTION_MAX", "iconify": "ACTION_ICONIFY"}
BUTTON_ICLASS = {"close": "B_CLOSE", "max": "B_MAX", "iconify": "B_ICONIFY"}


def region(x1p, x1, y1p, y1, x2p, x2, y2p, y2):
    return f"BORDER_PART_REGION(-1, {x1p}, {x1}, {y1p}, {y1}, -1, {x2p}, {x2}, {y2p}, {y2})"


class Builder:
    def __init__(self, art: Art):
        self.a = art
        self.out = ROOT / "build" / art.NAME
        self.e16 = self.out / "e16"
        self.svgdir = ROOT / "build" / ".svg" / art.NAME
        self.jobs = {}                      # rel png path -> svg source
        self.files = {}                     # cfg name -> text

    # -- image registration -------------------------------------------------

    def png(self, rel, svgsrc, matte=None, crisp=False):
        """e16 blends partial alpha against white, so anything drawn over
        something else is flattened onto a matte colour; shaped popups use
        crisp (un-antialiased) edges so their mask stays clean."""
        rel = "img/" + rel + ".png"
        head, body = svgsrc.split("</defs>", 1)
        body = body[:-len("</svg>")]
        if crisp:
            body = f'<g shape-rendering="crispEdges">{body}</g>'
        if matte:
            body = f'<rect width="100%" height="100%" fill="{matte}"/>' + body
        self.jobs[rel] = head + "</defs>" + body + "</svg>"
        return f'"{rel}"'

    def render(self):
        self.svgdir.mkdir(parents=True, exist_ok=True)

        def one(item):
            rel, src = item
            s = self.svgdir / rel.replace("/", "_").replace(".png", ".svg")
            s.write_text(src)
            dst = self.e16 / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["rsvg-convert", "-o", str(dst), str(s)], check=True)

        with ThreadPoolExecutor(8) as ex:
            list(ex.map(one, self.jobs.items()))

    # -- config emitters ----------------------------------------------------

    def image(self, name, states, pad=None, fill="__STRETCH"):
        """states: list of (MACRO_SUFFIX, png_ref, (l, r, t, b) edges)"""
        out = [f"BEGIN_IMAGE({name})"]
        for st, ref, e in states:
            out.append(f"  IMAGE_{st}({ref}, {fill}, {e[0]}, {e[1]}, {e[2]}, {e[3]})")
        if pad:
            out.append(f"  IMAGE_PADDING({pad[0]}, {pad[1]}, {pad[2]}, {pad[3]})")
        out.append("END_IMAGE")
        return "\n".join(out)

    def text(self, name, font, fg, justify=0, hilite=None, active=None, clicked=None, effect="__EFFECT_NONE"):
        a = self.a
        eff = effect
        sh = rgb(a.P["shadow"])
        out = [f'BEGIN_TEXT("{name}")',
               f"  TEXT_NORMAL(\"*{font}\", {eff}, {rgb(fg)}, {sh})"]
        if active:
            out.append(f"  TEXT_NORMAL_ACTIVE(\"*{font}\", {eff}, {rgb(active)}, {sh})")
        if hilite:
            out.append(f"  TEXT_HILITED(\"*{font}\", {eff}, {rgb(hilite)}, {sh})")
        if clicked:
            out.append(f"  TEXT_CLICKED(\"*{font}\", {eff}, {rgb(clicked)}, {sh})")
        out.append(f"  __JUSTIFICATION {justify}")
        out.append("END_TEXT")
        return "\n".join(out)

    # -- the big one ---------------------------------------------------------

    def build(self):
        a, M, P = self.a, self.a.M, self.a.P
        mt = a.MATTE
        if self.out.exists():
            shutil.rmtree(self.out)
        self.e16.mkdir(parents=True)

        img, txt = [], []
        TH, SW, BB, C, BS = M["title_h"], M["side"], M["bottom"], M["corner"], M["btn"]
        TW = M["title_w"]
        el, er = M["title_edge"]

        # ---------- border image classes ----------
        ti = self.png("border/title", a.title(TW, TH, False))
        ta = self.png("border/title_a", a.title(TW, TH, True))
        for nb in (0, 1, 2, 3):
            pad_r = M["btn_right"] + nb * (BS + M["btn_gap"]) + 4
            img.append(self.image(f"TITLE_{nb}", [
                ("NORMAL", ti, (el, er, 0, 0)), ("NORMAL_ACTIVE", ta, (el, er, 0, 0))],
                pad=(M["title_pad_l"], pad_r, 0, 0)))

        img.append(self.image("EMBLEM", [
            ("NORMAL", self.png("border/emblem", a.emblem(TH, "inactive"), mt["title"]), (0, 0, 0, 0)),
            ("NORMAL_ACTIVE", self.png("border/emblem_a", a.emblem(TH, "active"), mt["title"]), (0, 0, 0, 0)),
            ("HILITED", self.png("border/emblem_h", a.emblem(TH, "hover"), mt["title"]), (0, 0, 0, 0)),
            ("HILITED_ACTIVE", self.png("border/emblem_h", a.emblem(TH, "hover"), mt["title"]), (0, 0, 0, 0)),
        ]))

        for kind, name in BUTTON_ICLASS.items():
            r = {st: self.png(f"border/{kind}_{st}", a.button(kind, BS, st), mt["title"])
                 for st in ("inactive", "active", "hover", "clicked")}
            z = (0, 0, 0, 0)
            img.append(self.image(name, [
                ("NORMAL", r["inactive"], z), ("HILITED", r["hover"], z), ("CLICKED", r["clicked"], z),
                ("NORMAL_ACTIVE", r["active"], z), ("HILITED_ACTIVE", r["hover"], z),
                ("CLICKED_ACTIVE", r["clicked"], z)]))

        SH = 64
        for which in ("left", "right"):
            img.append(self.image(f"SIDE_{which[0].upper()}", [
                ("NORMAL", self.png(f"border/side_{which}", a.side(SW, SH, False, which)), (0, 0, 8, 8)),
                ("NORMAL_ACTIVE", self.png(f"border/side_{which}_a", a.side(SW, SH, True, which)), (0, 0, 8, 8))]))
            img.append(self.image(f"CORNER_{which[0].upper()}", [
                ("NORMAL", self.png(f"border/corner_{which}", a.corner(C, BB, False, which)), (0, 0, 0, 0)),
                ("NORMAL_ACTIVE", self.png(f"border/corner_{which}_a", a.corner(C, BB, True, which)), (0, 0, 0, 0))]))
        img.append(self.image("BOTTOM", [
            ("NORMAL", self.png("border/bottom", a.bottom(64, BB, False)), (8, 8, 0, 0)),
            ("NORMAL_ACTIVE", self.png("border/bottom_a", a.bottom(64, BB, True)), (8, 8, 0, 0))]))

        MTH = M["menu_title_h"]
        img.append(self.image("MENU_TITLE", [
            ("NORMAL", self.png("menu/title", a.menu_title(TW, MTH)), (el, er, 0, 0))],
            pad=(M["title_pad_l"], M["title_pad_l"], 0, 0)))

        # ---------- menus ----------
        if a.MENU_BG_TILE:   # a small repeating pattern instead of a stretched image
            t = a.MENU_BG_TILE
            img.append(self.image("MENU_BG", [
                ("NORMAL", self.png("menu/bg", a.menu_bg(t, t)), (0, 0, 0, 0))], pad=(2, 2, 4, 4), fill="__TILE"))
        else:
            img.append(self.image("MENU_BG", [
                ("NORMAL", self.png("menu/bg", a.menu_bg(96, 96)), (12, 12, 12, 12))], pad=(2, 2, 4, 4)))
        blank = self.png("blank", svg(4, 4, ""))
        mbg = self.png("menu/item", svg(4, 4, ""), mt["menu"])
        mp = M["menu_item_pad"]
        img.append(self.image("MENU_ITEM", [
            ("NORMAL", blank if a.MENU_BG_TILE else mbg, (0, 0, 0, 0)),
            ("HILITED", self.png("menu/sel", a.menu_sel(96, 22), mt["menu"]), (10, 10, 4, 4)),
            ("CLICKED", self.png("menu/sel", a.menu_sel(96, 22), mt["menu"]), (10, 10, 4, 4))], pad=mp))
        img.append(self.image("MENU_SUB", [
            ("NORMAL", self.png("menu/sub", a.menu_arrow(96, 22, False), None if a.MENU_BG_TILE else mt["menu"]), (10, 24, 4, 4)),
            ("HILITED", self.png("menu/sub_h", a.menu_arrow(96, 22, True), mt["menu"]), (10, 24, 4, 4)),
            ("CLICKED", self.png("menu/sub_h", a.menu_arrow(96, 22, True), mt["menu"]), (10, 24, 4, 4))], pad=mp))

        # ---------- dialogs ----------
        panel = self.png("dlg/panel", a.panel(96, 96))
        areap = self.png("dlg/area", a.area(48, 48), mt["dialog"])
        e8 = (8, 8, 8, 8)
        img.append(self.image("DIALOG", [("NORMAL", panel, e8)], pad=(6, 6, 6, 6)))
        for n in ("DIALOG_WIDGET_AREA", "DIALOG_WIDGET_TABLE", "SETTINGS_DESKTOP_AREA",
                  "SETTINGS_AREA_AREA", "SETTINGS_AREADESK_AREA"):
            img.append(self.image(n, [("NORMAL", areap, e8)], pad=(4, 4, 4, 4)))
        pb = {st: self.png(f"dlg/button_{st}", a.push_button(64, 24, st), mt["dialog"]) for st in ("normal", "hover", "clicked")}
        for n in ("DIALOG_BUTTON", "DIALOG_WIDGET_BUTTON", "DEFAULT_DOCK_BUTTON"):
            img.append(self.image(n, [
                ("NORMAL", pb["normal"], e8), ("HILITED", pb["hover"], e8), ("CLICKED", pb["clicked"], e8),
                ("NORMAL_ACTIVE", pb["clicked"], e8), ("HILITED_ACTIVE", pb["hover"], e8)],
                pad=(10, 10, 4, 4)))
        for n, fn in (("DIALOG_WIDGET_CHECK_BUTTON", a.check), ("DIALOG_WIDGET_RADIO_BUTTON", a.radio)):
            k = n.split("_")[2].lower()
            s = {(on, hv): self.png(f"dlg/{k}_{int(on)}{int(hv)}", fn(14, on, hv), mt["dialog"])
                 for on in (False, True) for hv in (False, True)}
            z = (0, 0, 0, 0)
            img.append(self.image(n, [
                ("NORMAL", s[(False, False)], z), ("HILITED", s[(False, True)], z),
                ("CLICKED", s[(False, True)], z),
                ("NORMAL_ACTIVE", s[(True, False)], z), ("HILITED_ACTIVE", s[(True, True)], z),
                ("CLICKED_ACTIVE", s[(True, True)], z)], pad=(2, 2, 2, 2)))
        img.append(self.image("DIALOG_WIDGET_SEPARATOR", [
            ("NORMAL", self.png("dlg/sep", a.separator(32, 4), mt["dialog"]), (4, 4, 0, 0)),
            ("CLICKED", self.png("dlg/sep", a.separator(32, 4), mt["dialog"]), (4, 4, 0, 0))], pad=(1, 1, 1, 1)))
        th = self.png("dlg/trough_h", a.trough(48, 12, False), mt["dialog"])
        tv = self.png("dlg/trough_v", a.trough(12, 48, True), mt["dialog"])
        kh = {c: self.png(f"dlg/knob_h{int(c)}", a.knob(24, 12, False, c), mt["dialog"]) for c in (False, True)}
        kv = {c: self.png(f"dlg/knob_v{int(c)}", a.knob(12, 24, True, c), mt["dialog"]) for c in (False, True)}
        # NB: edge sizes must stay below the drawn size or e16 renders garbage,
        # so the small bars only keep their ends along the long axis.
        eh, ev = (6, 6, 0, 0), (0, 0, 6, 6)
        for pre in ("DIALOG_WIDGET_SLIDER", "ICONBOX_SCROLLBAR"):
            img.append(self.image(f"{pre}_BASE_HORIZONTAL", [("NORMAL", th, eh)]))
            img.append(self.image(f"{pre}_BASE_VERTICAL", [("NORMAL", tv, ev)]))
            img.append(self.image(f"{pre}_KNOB_HORIZONTAL", [
                ("NORMAL", kh[False], eh), ("HILITED", kh[True], eh), ("CLICKED", kh[True], eh)]))
            img.append(self.image(f"{pre}_KNOB_VERTICAL", [
                ("NORMAL", kv[False], ev), ("HILITED", kv[True], ev), ("CLICKED", kv[True], ev)]))
        # grip drawn centred on the iconbox scrollbar knob
        grip = self.png("ibox/grip", a.grip(8), mt["dialog"])
        img.append(self.image("ICONBOX_SCROLLKNOB_HORIZONTAL", [("NORMAL", grip, (0, 0, 0, 0))]))
        img.append(self.image("ICONBOX_SCROLLKNOB_VERTICAL", [("NORMAL", grip, (0, 0, 0, 0))]))

        # ---------- popups ----------
        pop = self.png("pop/popup", a.popup(64, 32), crisp=True)
        pops = self.png("pop/popup_sel", a.popup_sel(64, 32), crisp=True)
        e10 = (10, 10, 10, 10)
        img.append(self.image("TT_MAIN", [("NORMAL", self.png("pop/tooltip", a.tooltip(64, 40), crisp=True), e10)],
                              pad=(10, 10, 6, 6)))
        for i, s in enumerate((12, 9, 7, 5), 1):
            img.append(self.image(f"TT_BUBBLE{i}", [("NORMAL", self.png(f"pop/bubble{i}", a.bubble(s, i), crisp=True), (0, 0, 0, 0))]))
        img.append(self.image("TT_CLEAR", [("NORMAL", blank, (0, 0, 0, 0))]))
        img.append(self.image("COORDS", [("NORMAL", pop, e10)], pad=(8, 8, 4, 4)))
        img.append(self.image("WARPFOCUS", [("NORMAL", pop, e10), ("CLICKED", pops, e10)], pad=(10, 10, 4, 4)))
        img.append(self.image("PAGER_TITLE_MAIN", [("NORMAL", pop, e10)], pad=(8, 8, 4, 4)))
        img.append(self.image("ICONBOX_TITLE_MAIN", [("NORMAL", pop, e10)], pad=(8, 8, 4, 4)))

        # ---------- pager / iconbox ----------
        img.append(self.image("PAGER_BACKGROUND", [("NORMAL", self.png("pager/bg", a.pager_bg(64, 48)), e8)]))
        img.append(self.image("PAGER_WIN", [("NORMAL", self.png("pager/win", a.pager_win(32, 24), crisp=True), (4, 4, 4, 4))]))
        img.append(self.image("PAGER_SEL", [("NORMAL", self.png("pager/sel", a.pager_sel(32, 24), crisp=True), (4, 4, 4, 4))],
                              pad=(2, 2, 2, 2)))
        ib = self.png("ibox/bg", a.iconbox_bg(64, 64))
        for n in ("ICONBOX_HORIZONTAL", "ICONBOX_VERTICAL", "ICONBOX_COVER_HORIZONTAL", "ICONBOX_COVER_VERTICAL"):
            img.append(self.image(n, [("NORMAL", ib, e8)], pad=(4, 4, 4, 4)))
        img.append(self.image("DEFAULT_ICON_BUTTON", [
            ("NORMAL", self.png("ibox/button", a.icon_button(40, 40), mt["dialog"]), e8)], pad=(4, 4, 4, 4)))
        for d in ("up", "down", "left", "right"):
            img.append(self.image(f"ICONBOX_ARROW_{d.upper()}", [
                ("NORMAL", self.png(f"ibox/arrow_{d}", a.arrow(14, d), mt["dialog"]), (0, 0, 0, 0))]))

        # ---------- startup / progress / dragbar ----------
        img.append(self.image("STARTUP_BAR", [("NORMAL", self.png("init/bar", a.startup_bar(64, 16)), (0, 0, 0, 4))]))
        img.append(self.image("PROGRESS_BAR", [
            ("NORMAL", pop, e10), ("CLICKED", pop, e10),
            ("NORMAL_ACTIVE", self.png("init/progress", a.progress_bar(32, 12), mt["popup"]), (4, 4, 4, 4))], pad=(4, 4, 4, 4)))
        for o, vert in (("HORIZ", False), ("VERT", True)):
            bar = self.png(f"desk/drag_{o}", a.dragbar(16 if vert else 64, 64 if vert else 16, vert))
            img.append(self.image(f"DESKTOP_DRAGBUTTON_{o}", [("NORMAL", bar, (0, 0, 6, 6) if vert else (6, 6, 0, 0))]))
            for n, d in (("RAISE", "left" if vert else "up"), ("LOWER", "right" if vert else "down")):
                img.append(self.image(f"DESKTOP_{n}BUTTON_{o}", [
                    ("NORMAL", self.png(f"desk/{d}", a.arrow(16, d), mt["dialog"]), (0, 0, 0, 0))]))
            img.append(self.image(f"DESKTOP_DESKRAY_{o}", [("NORMAL", blank, (0, 0, 0, 0))]))

        # ---------- text classes ----------
        F, J = "font-", a.TITLE_JUSTIFY
        C_ = a.TEXT
        fx = a.TEXT_EFFECT   # only on title bars and menus; popups stay plain
        txt.append(self.text("TITLE", F + "border", C_["title_inactive"], J, active=C_["title_active"], effect=fx))
        txt.append(self.text("MENU_TITLE", F + "border", C_["menu_title"], J, effect=fx))
        txt.append(self.text("MENU", F + "menu", C_["menu"], 0, hilite=C_["menu_hilite"], clicked=C_["menu_hilite"], effect=fx))
        for n in ("DIALOG", "DIALOG_WIDGET_TEXT", "DIALOG_WIDGET_CHECK_BUTTON", "DIALOG_WIDGET_RADIO_BUTTON"):
            txt.append(self.text(n, F + "dialog", C_["dialog"], 0))
        for n in ("DIALOG_BUTTON", "DIALOG_WIDGET_BUTTON"):
            txt.append(self.text(n, F + "dialog-hilite", C_["dialog"], 512, hilite=C_["menu_hilite"]))
        for n in ("TT_TEXT", "PAGER_WINDOW_TITLE", "ICONBOX_WINDOW_TITLE", "COORDS"):
            txt.append(self.text(n, F + "tooltip", C_["tooltip"], 512 if n != "COORDS" else 0))
        txt.append(self.text("WARPFOCUS", F + "focus", C_["tooltip"], 0, clicked=C_["menu_hilite"]))
        txt.append(self.text("PROGRESS_TEXT", F + "init", C_["tooltip"], 0))
        txt.append(self.text("PROGRESS_TEXT_NUMBER", F + "init", C_["tooltip"], 512))

        # ---------- borders ----------
        brd = [self.border("DEFAULT", buttons=("iconify", "max", "close")),
               self.border("TRANSIENT", buttons=("close",)),
               self.border("FIXED_SIZE", buttons=("iconify", "close")),
               self.border("DIALOG", buttons=("close",)),
               self.border("PAGER", buttons=()),
               self.border("ICONBOX", buttons=()),
               self.border("SHAPED", buttons=("close",), frame=False),
               self.border("MENU", buttons=(), menu=True),
               "BEGIN_BORDER(BORDERLESS, 0, 0, 0, 0)\nEND_BORDER"]

        hdr = "#include <definitions>\n__E_CFG_VERSION 1\n"
        self.files["imageclasses.cfg"] = hdr + "\n\n".join(img) + "\n"
        self.files["textclasses.cfg"] = hdr + "\n\n".join(txt) + "\n"
        self.files["borders.cfg"] = hdr + "\n\n".join(brd) + "\n"
        self.files["menustyles.cfg"] = hdr + "".join(
            f'NORMAL_MENU_STYLE_VERTICAL("{n}", "MENU", "MENU", "MENU_BG", "MENU_ITEM", "MENU_SUB", 40)\n'
            for n in ("DEFAULT", "EMPTY", "ROOT"))
        self.files["tooltips.cfg"] = hdr + (
            'TOOLTIP_WITH_LOGO("DEFAULT", "TT_MAIN", "TT_BUBBLE1", "TT_BUBBLE2", "TT_BUBBLE3", "TT_BUBBLE4", "TT_TEXT", 24, "TT_CLEAR")\n'
            'TOOLTIP_SIMPLE("PAGER", "PAGER_TITLE_MAIN", "PAGER_WINDOW_TITLE", 16)\n'
            'TOOLTIP_SIMPLE("ICONBOX", "ICONBOX_TITLE_MAIN", "ICONBOX_WINDOW_TITLE", 16)\n')
        cf, cb = rgb(a.CURSOR[0]), rgb(a.CURSOR[1])
        self.files["cursors.cfg"] = hdr + "".join(
            f"NATIVE_CURSOR({n}, {cf}, {cb}, {x})\n" for n, x in (
                ("DEFAULT", "XC_LEFT_PTR"), ("MOVE", "XC_FLEUR"),
                ("RESIZE_H", "XC_SB_H_DOUBLE_ARROW"), ("RESIZE_V", "XC_SB_V_DOUBLE_ARROW"),
                ("RESIZE_BR", "XC_BOTTOM_RIGHT_CORNER"), ("RESIZE_BL", "XC_BOTTOM_LEFT_CORNER")))
        self.files["fonts.theme.cfg"] = hdr + "BEGIN_FONTS\n" + "".join(
            f'  font-{k} "{a.FONTS[v]}"\n' for k, v in (
                ("default", "border"), ("border", "border"), ("border-small", "small"),
                ("coords", "small"), ("dialog", "dialog"), ("dialog-hilite", "dialog"),
                ("focus", "menu"), ("iconbox", "small"), ("init", "border"), ("menu", "menu"),
                ("pager", "small"), ("tooltip", "small"),
                ("epplet", "small"), ("epplet-small", "small"), ("epplet-medium", "dialog"),
                ("epplet-large", "border"))) + "END_FONTS\n"

        # ---------- backgrounds ----------
        wp = ROOT / a.WALLPAPER
        (self.e16 / "backgrounds").mkdir()
        dst = self.e16 / "backgrounds" / ("wallpaper" + wp.suffix.lower())
        if a.WALLPAPER_MODE == "crop":
            # centre-crop to 16:9 so a wide (or tall) image fills without stretching
            ww, hh = (int(subprocess.run(["vipsheader", "-f", f, str(wp)], capture_output=True,
                                         text=True, check=True).stdout) for f in ("width", "height"))
            cw, ch = min(ww, round(hh * 16 / 9)), min(hh, round(ww * 9 / 16))
            subprocess.run(["vips", "crop", str(wp), str(dst), str((ww - cw) // 2), str((hh - ch) // 2),
                            str(cw), str(ch)], check=True, env={**os.environ, "VIPS_WARNING": "0"})
        else:
            shutil.copy(wp, dst)
        layer = {"fill": "ADD_BACKGROUND_SCALED", "crop": "ADD_BACKGROUND_SCALED",
                 "fit": "ADD_BACKGROUND_SCALED_RETAIN_ASPECT"}[a.WALLPAPER_MODE]
        self.files["desktops.cfg"] = hdr + (
            f'BEGIN_BACKGROUND("{a.NAME}")\n  SET_SOLID("{rgb(a.BG_SOLID)}")\n'
            f'  {layer}("backgrounds/wallpaper{wp.suffix.lower()}")\n  DEFAULT_BACKGROUND\nEND_BACKGROUND\n')
        self.files["init.cfg"] = hdr + (
            f'BEGIN_BACKGROUND("STARTUP_BACKGROUND")\n  SET_SOLID("{rgb(a.BG_SOLID)}")\n'
            f'  ADD_BACKGROUND_SCALED("backgrounds/wallpaper{wp.suffix.lower()}")\nEND_BACKGROUND\n')

        for name, body in self.files.items():
            (self.e16 / name).write_text(body)
        self.render()
        (self.out / "README").write_text(f"{a.NAME} - e16 theme generated from {a.WALLPAPER}\n")
        return self.out

    # -- border geometry -----------------------------------------------------

    def border(self, name, buttons, frame=True, menu=False):
        M = self.a.M
        TH = M["menu_title_h"] if menu else M["title_h"]
        SW, BB, C, BS = M["side"], M["bottom"], M["corner"], M["btn"]
        if not frame:
            SW = BB = 0
        o = [f"BEGIN_BORDER({name}, {SW}, {SW}, {TH}, {BB})", "  BORDER_SHADE_DIRECTION(__UP)"]

        def part(iclass, w, h, reg, action=None, cursor=None, title=None, shaded=True, top=False):
            o.append(f"  BEGIN_BORDER_PART({iclass}, {w[0]}, {w[1]}, {h[0]}, {h[1]})")
            o.append("    " + reg)
            if title:
                o.append(f"    BORDER_PART_TITLE({title})")
            if action:
                o.append(f"    BORDER_PART_ACTION({action})")
            if cursor:
                o.append(f"    BORDER_PART_CURSOR({cursor})")
            o.append(f"    BORDER_PART_KEEP_WHEN_SHADED({'__ON' if shaded else '__OFF'})")
            if top:
                o.append("    BORDER_PART_KEEP_ON_TOP")
            o.append("  END_BORDER_PART")

        big = 99999
        if menu:
            part("MENU_TITLE", (0, big), (TH, TH), region(0, 0, 0, 0, 1024, -1, 0, TH - 1),
                 "ACTION_MOVE", "MOVE", "MENU_TITLE")
        else:
            part("EMBLEM", (TH, TH), (TH, TH), region(0, 0, 0, 0, 0, TH - 1, 0, TH - 1), "ACTION_MENU")
            part(f"TITLE_{len(buttons)}", (0, big), (TH, TH), region(0, TH, 0, 0, 1024, -1, 0, TH - 1),
                 "ACTION_MOVE", "MOVE", "TITLE")
            by = (TH - BS) // 2
            x2 = -M["btn_right"]
            for kind in reversed(buttons):
                part(BUTTON_ICLASS[kind], (BS, BS), (BS, BS),
                     region(1024, x2 - BS, 0, by, 1024, x2 - 1, 0, by + BS - 1),
                     BUTTON_ACTIONS[kind], top=True)
                x2 -= BS + M["btn_gap"]
        if frame:
            part("SIDE_L", (SW, SW), (0, big), region(0, 0, 0, TH, 0, SW - 1, 1024, -BB - 1),
                 "ACTION_RESIZE_H", "RESIZE_H", shaded=False)
            part("SIDE_R", (SW, SW), (0, big), region(1024, -SW, 0, TH, 1024, -1, 1024, -BB - 1),
                 "ACTION_RESIZE_H", "RESIZE_H", shaded=False)
            part("BOTTOM", (0, big), (BB, BB), region(0, C, 1024, -BB, 1024, -C - 1, 1024, -1),
                 "ACTION_RESIZE_V", "RESIZE_V", shaded=False)
            part("CORNER_L", (C, C), (BB, BB), region(0, 0, 1024, -BB, 0, C - 1, 1024, -1),
                 "ACTION_RESIZE", "RESIZE_BL", shaded=False)
            part("CORNER_R", (C, C), (BB, BB), region(1024, -C, 1024, -BB, 1024, -1, 1024, -1),
                 "ACTION_RESIZE", "RESIZE_BR", shaded=False)
        o.append("END_BORDER")
        return "\n".join(o)
