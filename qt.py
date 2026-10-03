"""Matching Qt themes: a KDE colour scheme (.colors) per theme.

KDE colour schemes are what the Breeze style (and every KDE app, native or
Flatpak) paints with, so this is the way to theme Qt here without Kvantum.
The colours come from the GTK build's palette, including the ones it measured
from the rendered art (button faces, tooltip body, header bar), so Qt and GTK
apps match.  Per-theme overrides go in an Art's QT dict.

Output: <out_dir>/qt/<Name>.colors
"""

from pathlib import Path

from gtk import mix, pixel, readable

NEGATIVE, NEUTRAL, POSITIVE = "#e5484d", "#e5a50a", "#3fae6a"


def _c(h):
    """'#rrggbb' -> 'r,g,b' as KDE colour files want."""
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _group(name, bg, alt, fg, dim, accent, hover, link):
    return f"""[Colors:{name}]
BackgroundAlternate={_c(alt)}
BackgroundNormal={_c(bg)}
DecorationFocus={_c(accent)}
DecorationHover={_c(hover)}
ForegroundActive={_c(accent)}
ForegroundInactive={_c(dim)}
ForegroundLink={_c(link)}
ForegroundNegative={_c(NEGATIVE)}
ForegroundNeutral={_c(NEUTRAL)}
ForegroundNormal={_c(fg)}
ForegroundPositive={_c(POSITIVE)}
ForegroundVisited={_c(mix(link, fg, 0.4))}
"""


def build(art, out_dir, pal):
    """pal: the dict gtk.build() returned.  Returns the .colors path."""
    a, T = art, art.TEXT
    cfg = dict(getattr(a, "QT", {}))
    assets = pal["assets"]
    bg, fg, view_bg = pal["bg"], pal["fg"], pal["view_bg"]
    accent = cfg.get("accent", pal["accent"])
    hover = cfg.get("hover", mix(accent, "#ffffff", 0.25))
    link = pal["link"]
    texts = [T["dialog"], T["menu_hilite"], T["title_active"], T["tooltip"], T["menu"], "#ffffff", "#111111"]

    # measured from the rendered art
    button_bg = cfg.get("button_bg", pixel(assets / "button-c.png", 4, 2, bg))
    tooltip_bg = cfg.get("tooltip_bg", pixel(assets / "tooltip-c.png", 4, 2, bg))
    header_bg = cfg.get("header_bg", pixel(assets / "header-bg.png", 10, 12, bg))
    header_bd = cfg.get("header_bg_inactive", pixel(assets / "header-bg-backdrop.png", 10, 12, bg))

    sel_bg = cfg.get("selection", accent)
    sel_fg = readable(sel_bg, [T["menu_hilite"]] + texts)
    button_fg = readable(button_bg, [pal["button_fg"]] + texts)
    tooltip_fg = readable(tooltip_bg, [T["tooltip"]] + texts)
    title_fg = readable(header_bg, [T["title_active"]] + texts)
    dim = pal["dim"]

    groups = [
        _group("Button", button_bg, mix(button_bg, fg, 0.06), button_fg, mix(button_fg, button_bg, 0.45), accent, hover, link),
        _group("Complementary", header_bg, mix(header_bg, title_fg, 0.08), title_fg, mix(title_fg, header_bg, 0.45), accent, hover, link),
        _group("Header", header_bg, mix(header_bg, title_fg, 0.06), title_fg, mix(title_fg, header_bg, 0.45), accent, hover, link),
        _group("Header][Inactive", header_bd, mix(header_bd, T["title_inactive"], 0.06), readable(header_bd, [T["title_inactive"]] + texts),
               mix(T["title_inactive"], header_bd, 0.45), accent, hover, link),
        _group("Selection", sel_bg, mix(sel_bg, sel_fg, 0.1), sel_fg, mix(sel_fg, sel_bg, 0.35), accent, hover, link),
        _group("Tooltip", tooltip_bg, mix(tooltip_bg, tooltip_fg, 0.06), tooltip_fg, mix(tooltip_fg, tooltip_bg, 0.45), accent, hover, link),
        _group("View", view_bg, mix(view_bg, fg, 0.04), fg, dim, accent, hover, link),
        _group("Window", bg, pal["bg_dark"], fg, dim, accent, hover, link),
    ]

    text = f"""# {a.NAME} - KDE colour scheme generated alongside the e16 theme (see qt.py)

[ColorEffects:Disabled]
Color={_c(bg)}
ColorAmount=0.3
ColorEffect=2
ContrastAmount=0.55
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={_c(bg)}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

{chr(10).join(groups)}
[General]
ColorScheme={a.NAME}
Name={a.NAME}
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={_c(header_bg)}
activeBlend={_c(accent)}
activeForeground={_c(title_fg)}
inactiveBackground={_c(header_bd)}
inactiveBlend={_c(header_bd)}
inactiveForeground={_c(T["title_inactive"])}
"""
    path = Path(out_dir) / "qt" / f"{a.NAME}.colors"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path
