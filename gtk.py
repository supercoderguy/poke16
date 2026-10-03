"""Matching GTK3 themes, built from the same Art as the e16 and rofi themes.

Output: <out_dir>/gtk-3.0/gtk.css + assets/, and <out_dir>/index.theme, so the
whole build/<Name> directory doubles as a GTK theme (~/.themes/<Name>).

The theme's own art is reused: header bars get the e16 title bar and emblem,
title buttons are the e16 buttons, push buttons / entries / tooltips use the
e16 dialog art as 9-slice border images, check and radio buttons are the e16
ones, and selections reuse the rofi highlight.  Everything else is plain CSS
driven by the palette.  Per-theme overrides go in an Art's GTK dict.
"""

import copy
import re
import subprocess
from pathlib import Path
from string import Template


HB_H = 34          # header bar height (px) the header art is rendered for
TB = 20            # title button size (px)

WEIGHTS = {"thin": 100, "extralight": 200, "light": 300, "regular": 400, "medium": 500,
           "semibold": 600, "bold": 700, "extrabold": 800, "black": 900, "heavy": 900}


# ---- small colour helpers -------------------------------------------------

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in c)


def mix(a, b, t):
    """Blend colour a toward b by t (0..1)."""
    return _hex(x + (y - x) * t for x, y in zip(_rgb(a), _rgb(b)))


def luminance(h):
    r, g, b = (v / 255 for v in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    """WCAG contrast ratio between two colours."""
    def lin(h):
        c = [v / 255 for v in _rgb(h)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    la, lb = sorted((lin(a), lin(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def readable(on, candidates):
    """First candidate that reads well on `on` (4.5:1), else the best one."""
    for c in candidates:
        if contrast(c, on) >= 4.5:
            return c
    return max(candidates, key=lambda c: contrast(c, on))


def pixel(png, x, y, under):
    """Colour of one pixel of a rendered PNG, composited over `under`."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(png), "-vf", f"crop=1:1:{x}:{y}",
                          "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True, check=True).stdout
    r, g, b, a = raw[:4]
    return mix(under, _hex((r, g, b)), a / 255)


def alpha(h, a):
    r, g, b = _rgb(h)
    return f"rgba({r},{g},{b},{a})"


# ---- art adapters ---------------------------------------------------------

def _bare(art):
    """The same art, but buttons/emblem drawn without the title-bar slice behind
    them (e16 needed them opaque; GTK composites properly)."""
    if not hasattr(art, "_title_bg"):
        return art
    orig = art._title_bg
    a = copy.copy(art)
    a._title_bg = lambda *args, **kw: (orig(*args, **kw)[0], "")
    return a


def _slice(src, x, y, w, h):
    """Crop an SVG to a sub-rectangle (by nesting it under a new viewBox)."""
    inner = src[src.index(">") + 1:src.rindex("</svg>")]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}">'
            f"{inner}</svg>")


def _font(pango):
    """'pango:DejaVu Serif Condensed Bold 9' -> CSS declarations."""
    words = pango.removeprefix("pango:").split()[:-1]
    weight, style, stretch, family = 400, "normal", "normal", []
    for w in words:
        lw = w.lower()
        if lw in WEIGHTS:
            weight = WEIGHTS[lw]
        elif lw in ("italic", "oblique"):
            style = lw
        elif lw == "condensed":
            stretch = "condensed"
        else:
            family.append(w)
    return (f'font-family: "{" ".join(family)}"; font-weight: {weight}; '
            f"font-style: {style}; font-stretch: {stretch};")


def _selection(rofi_sel, accent, accent_fg):
    """Turn a theme's rofi highlight into GTK CSS: background + an accent
    edge drawn as an inset shadow (borders would make rows jump in size)."""
    css = re.sub(r"rgba\((\d+),(\d+),(\d+),(\d+)%\)",
                 lambda m: f"rgba({m[1]},{m[2]},{m[3]},{int(m[4]) / 100})", rofi_sel or "")
    out = []
    bg = re.search(r"background-image:\s*([^;]+);", css)
    col = re.search(r"background-color:\s*([^;]+);", css)
    out.append(f"background-image: {bg[1]};" if bg else "background-image: none;")
    out.append(f"background-color: {col[1] if col else (accent if not bg else 'transparent')};")
    edge = re.search(r"border-color:\s*([^;]+);", css)
    if edge:
        out.append(f"box-shadow: inset 3px 0 {edge[1]};")
    out.append(f"color: {accent_fg};")
    return " ".join(out)


# ---- the stylesheet --------------------------------------------------------
# NB: GTK3 parses border-image `fill` but never draws the centre slice, so each
# 9-slice image's centre is also rendered on its own (<name>-c.png) and painted
# as a stretched background inside the border.

CSS = Template(r"""/* $name - GTK3 theme generated alongside the e16 theme (see gtk.py) */

@define-color theme_bg_color $bg;
@define-color theme_fg_color $fg;
@define-color theme_base_color $view_bg;
@define-color theme_text_color $fg;
@define-color theme_selected_bg_color $accent;
@define-color theme_selected_fg_color $accent_fg;
@define-color theme_unfocused_bg_color $bg;
@define-color theme_unfocused_fg_color $fg;
@define-color theme_unfocused_base_color $view_bg;
@define-color theme_unfocused_text_color $fg;
@define-color theme_unfocused_selected_bg_color $accent;
@define-color theme_unfocused_selected_fg_color $accent_fg;
@define-color insensitive_bg_color $bg;
@define-color insensitive_fg_color $dim;
@define-color insensitive_base_color $view_bg;
@define-color borders $border;
@define-color unfocused_borders $border;
@define-color warning_color #e5a50a;
@define-color error_color #e5484d;
@define-color success_color #3fae6a;
@define-color link_color $link;

* {
    -GtkScrollbar-has-backward-stepper: false;
    -GtkScrollbar-has-forward-stepper: false;
    -GtkWidget-text-handle-width: 20;
    -GtkWidget-text-handle-height: 24;
    -GtkDialog-button-spacing: 6;
    -GtkDialog-action-area-border: 0;
    outline-color: $focus;
    outline-style: dashed;
    outline-offset: -3px;
    outline-width: 1px;
    -gtk-secondary-caret-color: $accent;
}

/* ---- base -------------------------------------------------------------- */

window, .background { background-color: $bg; color: $fg; }
*:disabled { color: $dim; -gtk-icon-effect: dim; }
label.dim-label, .dim-label { color: $dim; }
label selection { background-color: $accent; color: $accent_fg; }
label:disabled { color: $dim; }
.view, iconview, textview text, treeview.view, .cell { background-color: $view_bg; color: $fg; }
textview { background-color: $view_bg; }
.view:selected, .view:selected:focus, iconview:selected, flowbox flowboxchild:selected {
    $selection
}
/* tree views paint each cell separately, so a gradient would restart per column */
treeview.view:selected, treeview.view:selected:focus {
    background-image: none; background-color: $sel_solid; color: $accent_fg; box-shadow: none;
}
selection, text selection, entry selection, *:selected selection { background-color: $accent; color: $accent_fg; }
.view:hover, treeview.view:hover { background-color: $hover; }
a, *:link, button:link { color: $link; }
*:visited { color: mix($link, $fg, 0.4); }
separator { background-color: $border; min-width: 1px; min-height: 1px; }
rubberband, .rubberband { border: 1px solid $accent; background-color: $accent_a20; }
.frame, frame > border, scrolledwindow.frame { border: 1px solid $border; }
frame > label { color: $dim; }
spinner { color: $accent; }

/* ---- header bars: the e16 title bar ------------------------------------ */

headerbar, .titlebar:not(headerbar) {
    min-height: ${hb_min}px;
    padding: 0 6px 0 ${hb_pad}px;
    border: none;
    color: $title_fg;
    background-color: $header_bg;
    background-image: url("assets/header-emblem.png"), url("assets/header-bg.png");
    background-size: auto 100%, 100% 100%;
    background-repeat: no-repeat;
    background-position: left center, center;
    box-shadow: none;
}
headerbar:backdrop, .titlebar:backdrop:not(headerbar) {
    color: $title_dim;
    background-image: url("assets/header-emblem-backdrop.png"), url("assets/header-bg-backdrop.png");
}
headerbar .title, .titlebar .title { $title_font color: $title_fg; padding: 0 12px; }
headerbar .subtitle { font-size: smaller; color: $title_dim; }
headerbar:backdrop .title, .titlebar:backdrop .title { color: $title_dim; }
headerbar entry, headerbar button:not(.titlebutton) { margin-top: 3px; margin-bottom: 3px; }
headerbar separator.titlebutton { background: none; min-width: 6px; }

/* the e16 title buttons */
button.titlebutton {
    min-width: ${tb}px; min-height: ${tb}px;
    padding: 0; margin: 0 2px;
    border: none; border-radius: 0; box-shadow: none;
    background-color: transparent;
    background-size: ${tb}px ${tb}px; background-repeat: no-repeat; background-position: center;
    color: transparent; -gtk-icon-shadow: none;
}
button.titlebutton image { opacity: 0; }
$titlebuttons

/* client-side decorations (dialogs and headerbar apps) */
decoration { border-radius: 0; box-shadow: 0 0 0 1px $border, 0 3px 9px 1px rgba(0,0,0,0.45); margin: 4px; }
decoration:backdrop { box-shadow: 0 0 0 1px $border, 0 2px 6px rgba(0,0,0,0.3); }
.solid-csd decoration { box-shadow: 0 0 0 1px $border; margin: 0; }
.maximized decoration, .fullscreen decoration, .tiled decoration { box-shadow: none; margin: 0; }

/* ---- buttons: the e16 dialog button as a 9-slice ----------------------- */

button {
    min-height: 18px; min-width: 18px;
    padding: 0 6px;
    border-style: solid; border-width: 8px;
    border-image: url("assets/button.png") 8 8 8 8 fill stretch; background-image: url("assets/button-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box;
    border-radius: 0;
    background-color: transparent;
    color: $button_fg;
    box-shadow: none;
    text-shadow: none;
}
button:hover { border-image: url("assets/button-hover.png") 8 8 8 8 fill stretch; background-image: url("assets/button-hover-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box; }
button:active, button:checked { border-image: url("assets/button-active.png") 8 8 8 8 fill stretch; background-image: url("assets/button-active-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box; color: $button_active_fg; }
button:disabled { opacity: 0.55; }
button.flat, button.flat:backdrop, headerbar button.flat, .inline-toolbar button,
toolbar button, button.sidebar-button, modelbutton.flat, popover button.flat {
    border-image: none; border-width: 0; padding: 4px 8px; background: none;
}
button.flat:hover, toolbar button:hover { border-image: none; background-color: $hover; }
button.flat:active, button.flat:checked { border-image: none; background-color: $accent_a35; }
button.suggested-action { color: $button_active_fg; }
button.suggested-action, button.suggested-action:hover { border-image: url("assets/button-active.png") 8 8 8 8 fill stretch; background-image: url("assets/button-active-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box; }
button.destructive-action { color: #ffffff; border-image: none; border-width: 1px; border-color: #b02a30; background-color: #d0343c; border-radius: 4px; }
button.circular, button.image-button { padding: 0 2px; }
.linked > button { margin: 0; }
button label { color: inherit; }

/* ---- entries: the e16 field art ------------------------------------------ */

entry, spinbutton:not(.vertical), .entry {
    min-height: 16px;
    padding: 0 4px;
    border-style: solid; border-width: 8px;
    border-image: url("assets/field.png") 8 8 8 8 fill stretch; background-image: url("assets/field-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box;
    border-radius: 0;
    background-color: transparent;
    color: $view_fg;
    caret-color: $accent;
    box-shadow: none;
}
entry:focus, spinbutton:focus:not(.vertical) { border-image: url("assets/field-focus.png") 8 8 8 8 fill stretch; background-image: url("assets/field-focus-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box; }
entry:disabled { opacity: 0.6; }
entry image { color: $dim; }
entry progress { border-bottom: 2px solid $accent; background: none; }
spinbutton:not(.vertical) entry { border: none; border-image: none; padding: 0; min-height: 20px; }
spinbutton:not(.vertical) button { border-image: none; border-width: 0; padding: 0 6px; background: none; color: $fg; }
spinbutton:not(.vertical) button:hover { background-color: $hover; }
combobox button.combo { padding: 0 6px; }
combobox arrow { min-width: 16px; min-height: 16px; }

/* ---- check / radio: the e16 widgets -------------------------------------- */

check, radio { min-width: 16px; min-height: 16px; margin: 0 4px; border: none; background: none; }
check { -gtk-icon-source: url("assets/check.png"); }
check:hover { -gtk-icon-source: url("assets/check-hover.png"); }
check:checked, check:indeterminate { -gtk-icon-source: url("assets/check-on.png"); }
check:checked:hover, check:indeterminate:hover { -gtk-icon-source: url("assets/check-on-hover.png"); }
radio { -gtk-icon-source: url("assets/radio.png"); }
radio:hover { -gtk-icon-source: url("assets/radio-hover.png"); }
radio:checked, radio:indeterminate { -gtk-icon-source: url("assets/radio-on.png"); }
radio:checked:hover { -gtk-icon-source: url("assets/radio-on-hover.png"); }
check:disabled, radio:disabled { opacity: 0.5; }
menuitem check, menuitem radio, modelbutton check, modelbutton radio { margin: 0 6px 0 0; }

/* ---- switch / scale / progress ---------------------------------------------- */

switch {
    min-width: 40px; min-height: 20px;
    border: 1px solid $border; border-radius: 12px;
    background-color: $view_bg; color: transparent; font-size: 0;
}
switch:checked { background-image: $accent_fill; background-color: $accent; border-color: $accent; }
switch slider {
    min-width: 18px; min-height: 18px; margin: -1px;
    border: 1px solid $border; border-radius: 50%;
    background-color: $knob;
}
switch:disabled { opacity: 0.5; }

scale { min-height: 16px; min-width: 16px; padding: 8px; }
scale trough { min-height: 4px; min-width: 4px; border-radius: 3px; background-color: $trough; border: 1px solid $border; }
scale highlight { border-radius: 3px; background-image: $accent_fill; background-color: $accent; }
scale slider {
    min-width: 14px; min-height: 14px; margin: -7px;
    border: 1px solid $border; border-radius: 50%;
    background-color: $knob;
}
scale slider:hover { border-color: $accent; }
scale marks, scale value { color: $dim; }

progressbar trough { min-height: 8px; min-width: 8px; border-radius: 4px; background-color: $trough; border: 1px solid $border; }
progressbar progress {
    min-height: 8px; min-width: 8px; border-radius: 4px; border: none;
    background-image: url("assets/progress.png"); background-size: 100% 100%;
}
progressbar text { color: $fg; font-size: smaller; }
levelbar block { min-height: 6px; min-width: 32px; border-radius: 2px; }
levelbar block.filled, levelbar block.high { background-color: $accent; }
levelbar block.low { background-color: #e5a50a; }
levelbar block.empty { background-color: $trough; }

/* ---- scrollbars --------------------------------------------------------- */

scrollbar { background-color: transparent; border: none; }
scrollbar slider {
    min-width: 6px; min-height: 6px; margin: 2px;
    border: none; border-radius: 4px;
    background-color: $scroll;
}
scrollbar slider:hover { background-color: $scroll_hover; }
scrollbar slider:active { background-color: $accent; }
scrollbar.overlay-indicator:not(.dragging):not(.hovering) slider { min-width: 3px; min-height: 3px; margin: 2px; }
scrollbar button { min-width: 0; min-height: 0; padding: 0; border: none; border-image: none; }

/* ---- notebooks ----------------------------------------------------------- */

notebook > header { background-color: $bg_dark; border-color: $border; }
notebook > header.top { border-bottom: 1px solid $border; }
notebook > header tab { min-height: 24px; padding: 2px 12px; color: $dim; border: none; }
notebook > header tab:hover { color: $fg; background-color: $hover; }
notebook > header tab:checked { color: $fg; box-shadow: inset 0 -3px $accent; }
notebook > header.bottom tab:checked { box-shadow: inset 0 3px $accent; }
notebook > header.left tab:checked { box-shadow: inset -3px 0 $accent; }
notebook > header.right tab:checked { box-shadow: inset 3px 0 $accent; }
notebook > header tab button.flat { padding: 0; min-width: 16px; min-height: 16px; }
notebook > stack:not(:only-child) { background-color: $bg; }

/* ---- menus and popovers: the e16 menu ---------------------------------------- */

menubar, .menubar { padding: 0; background-color: $bg_dark; box-shadow: inset 0 -1px $border; }
menubar > menuitem { min-height: 18px; padding: 4px 8px; }
menubar > menuitem:hover { box-shadow: inset 0 -3px $accent; color: $fg; }
menu, .menu, .context-menu {
    margin: 4px; padding: 4px 0;
    background-color: $menu_bg;
    $menu_tile
    border: 1px solid $menu_border;
}
.csd menu, .csd .menu { border: 1px solid $menu_border; }
menu menuitem, .menu menuitem { min-height: 20px; min-width: 40px; padding: 3px 12px; color: $menu_fg; }
menu menuitem:hover, .menu menuitem:hover { $selection }
menu menuitem:disabled { color: $menu_dim; }
menu menuitem arrow { min-width: 16px; min-height: 16px; }
menu separator, .menu separator { margin: 3px 0; background-color: $menu_border; }
menu > arrow { min-height: 16px; background-color: $menu_bg; color: $menu_fg; }
popover, popover.background {
    padding: 4px; border: 1px solid $menu_border; border-radius: 4px;
    background-color: $menu_bg; color: $menu_fg;
    box-shadow: 0 3px 8px rgba(0,0,0,0.35);
}
popover modelbutton { min-height: 22px; padding: 2px 10px; color: $menu_fg; }
popover modelbutton:hover { $selection }

/* ---- tooltips: the e16 tooltip ------------------------------------------------ */

tooltip, tooltip.background {
    padding: 2px;
    border-style: solid; border-width: 8px;
    border-image: url("assets/tooltip.png") 10 10 10 10 fill stretch; background-image: url("assets/tooltip-c.png"); background-size: 100% 100%; background-origin: border-box; background-clip: padding-box;
    border-radius: 0;
    background-color: transparent;
    box-shadow: none;
}
tooltip label, tooltip * { color: $tooltip_fg; }

/* ---- lists, trees, sidebars --------------------------------------------------- */

list, listview { background-color: $view_bg; color: $fg; }
list row, list > row { padding: 2px; }
list row:hover, row.activatable:hover { background-color: $hover; }
list row:selected, row:selected, row.activatable:selected, placessidebar row:selected { $selection }
row:selected label, row:selected image { color: inherit; }
treeview.view header button {
    padding: 2px 6px; border-width: 0 1px 1px 0; border-style: solid; border-color: $border;
    border-image: none; background-color: $bg_dark; color: $dim; font-weight: bold;
}
treeview.view header button:hover { color: $fg; background-color: $hover; }
treeview.view { -GtkTreeView-grid-line-width: 1; -GtkTreeView-tree-line-width: 1; border-left-color: $border; border-top-color: $border; }
treeview.view.expander { color: $dim; }
treeview.view.expander:hover { color: $fg; }
.sidebar, placessidebar, stacksidebar { background-color: $bg_dark; border-right: 1px solid $border; }
stacksidebar row { padding: 6px 12px; }

/* ---- misc ---------------------------------------------------------------- */

toolbar, .toolbar, actionbar > revealer > box { padding: 4px; background-color: $bg; }
paned > separator { min-width: 1px; min-height: 1px; background-color: $border; }
paned > separator.wide { min-width: 6px; min-height: 6px; background-color: $bg_dark; }
infobar.info, infobar.question { background-color: $accent_a20; }
infobar.warning { background-color: rgba(229,165,10,0.25); }
infobar.error { background-color: rgba(229,72,77,0.3); }
calendar { color: $fg; border: 1px solid $border; }
calendar:selected { background-color: $accent; color: $accent_fg; }
calendar.header { border-bottom: 1px solid $border; }
calendar.highlight { color: $accent; }
messagedialog .titlebar { min-height: 20px; background-image: none; background-color: $bg; }
messagedialog .dialog-action-area button { margin: 4px; }
.osd, .app-notification { background-color: rgba(0,0,0,0.75); color: #ffffff; border-radius: 4px; }
cursor-handle { background: none; }
""")


def _render(src, dst, zoom=1.0):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".svg")
    tmp.write_text(src)
    subprocess.run(["rsvg-convert", "-z", f"{zoom}", "-o", str(dst), str(tmp)], check=True)
    tmp.unlink()


def build(art, out_dir):
    """Write <out_dir>/gtk-3.0/... and <out_dir>/index.theme.  Returns the
    palette it settled on (incl. colours measured from the art) for qt.py."""
    a, M, P, T = art, art.M, art.P, art.TEXT
    bare = _bare(art)
    out = Path(out_dir)
    assets = out / "gtk-3.0" / "assets"
    cfg = dict(getattr(a, "GTK", {}))

    # -- palette -----------------------------------------------------------
    bg = cfg.get("bg", a.MATTE["dialog"])
    fg = cfg.get("fg", T["dialog"])
    dark = luminance(bg) < 0.5
    view_bg = cfg.get("view_bg", mix(bg, "#000000", 0.28) if dark else mix(bg, "#ffffff", 0.65))
    accent = cfg.get("accent", P["accent"])
    accent_fg = cfg.get("accent_fg", T["menu_hilite"])
    border = cfg.get("border", mix(bg, fg, 0.22))
    v = dict(
        name=a.NAME, bg=bg, fg=fg, view_bg=view_bg, view_fg=fg,
        bg_dark=mix(bg, "#000000", 0.15) if dark else mix(bg, "#000000", 0.05),
        dim=mix(fg, bg, 0.45), border=border, hover=alpha(fg, 0.08),
        accent=accent, accent_fg=accent_fg, accent_a20=alpha(accent, 0.2), accent_a35=alpha(accent, 0.35),
        accent_fill=cfg.get("accent_fill", "none"),
        focus=alpha(accent, 0.6), link=cfg.get("link", P["accent_hi"]),
        knob=cfg.get("knob", mix(fg, bg, 0.1)), trough=mix(view_bg, fg, 0.08),
        scroll=alpha(fg, 0.35), scroll_hover=alpha(fg, 0.55),
        menu_bg=a.MATTE["menu"], menu_fg=T["menu"], menu_dim=mix(T["menu"], a.MATTE["menu"], 0.45),
        menu_border=cfg.get("menu_border", P["line"]),
        menu_tile=('background-image: url("assets/menu-tile.png"); background-repeat: repeat;'
                   if a.MENU_BG_TILE else ""),
        header_bg=a.MATTE["title"], title_fg=T["title_active"], title_dim=T["title_inactive"],
        title_font=_font(a.FONTS["border"]), tooltip_fg=T["tooltip"],
        selection=_selection((getattr(a, "ROFI", {}) or {}).get("sel"), P["sel"], accent_fg),
        tb=TB,
    )
    v["sel_solid"] = cfg.get("sel_solid", mix(accent, view_bg, 0.45))

    # -- header bar: emblem + a slice from the stretchable middle of the title --
    TH, el = M["title_h"], M["title_edge"][0]
    zoom = HB_H / TH
    for suffix, active in (("", True), ("-backdrop", False)):
        _render(_slice(a.title(el + 40, TH, active), el + 8, 0, 16, TH), assets / f"header-bg{suffix}.png", zoom)
        _render(bare.emblem(TH, "active" if active else "inactive"), assets / f"header-emblem{suffix}.png", zoom)
    v["hb_min"] = HB_H
    v["hb_pad"] = round(TH * zoom) + 4

    # -- title buttons ---------------------------------------------------------
    rules = []
    for gtk_name, kind in (("close", "close"), ("maximize", "max"), ("minimize", "iconify")):
        for st in ("inactive", "active", "hover", "clicked"):
            _render(bare.button(kind, M["btn"], st), assets / f"tb-{kind}-{st}.png", TB / M["btn"])
        sel = f"button.titlebutton.{gtk_name}"
        rules += [f'{sel} {{ background-image: url("assets/tb-{kind}-active.png"); }}',
                  f'{sel}:hover {{ background-image: url("assets/tb-{kind}-hover.png"); }}',
                  f'{sel}:active {{ background-image: url("assets/tb-{kind}-clicked.png"); }}',
                  f'{sel}:backdrop {{ background-image: url("assets/tb-{kind}-inactive.png"); }}']
    v["titlebuttons"] = "\n".join(rules)

    # -- 9-slice widgets, check/radio, progress, menu tile ----------------------------
    def nine(src, name, edge):
        """A 9-slice image plus its centre on its own (see the NB above)."""
        _render(src, assets / f"{name}.png")
        m = re.search(r'width="([\d.]+)" height="([\d.]+)"', src)
        w, h = float(m[1]), float(m[2])
        _render(_slice(src, edge, edge, w - 2 * edge, h - 2 * edge), assets / f"{name}-c.png")

    nine(a.push_button(64, 24, "normal"), "button", 8)
    nine(a.push_button(64, 24, "hover"), "button-hover", 8)
    nine(a.push_button(64, 24, "clicked"), "button-active", 8)
    nine(a.area(48, 32), "field", 8)
    nine(_focus_ring(a.area(48, 32), accent), "field-focus", 8)
    nine(a.tooltip(64, 40), "tooltip", 10)
    for name, fn in (("check", a.check), ("radio", a.radio)):
        for on in (False, True):
            for hv in (False, True):
                _render(fn(16, on, hv), assets / f"{name}{'-on' if on else ''}{'-hover' if hv else ''}.png")
    _render(a.progress_bar(64, 8), assets / "progress.png")
    if a.MENU_BG_TILE:
        _render(a.menu_bg(a.MENU_BG_TILE, a.MENU_BG_TILE), assets / "menu-tile.png")

    # text colours from the art actually drawn (centre pixel of each 9-slice)
    texts = [T["dialog"], T["menu_hilite"], T["title_active"], T["tooltip"], T["menu"], "#ffffff", "#111111"]
    v["button_fg"] = cfg.get("button_fg") or readable(pixel(assets / "button.png", 32, 12, bg), texts)
    v["button_active_fg"] = cfg.get("button_active_fg") or readable(pixel(assets / "button-active.png", 32, 12, bg), texts)
    v["view_fg"] = readable(pixel(assets / "field.png", 24, 16, bg), [fg] + texts)
    v["tooltip_fg"] = readable(pixel(assets / "tooltip.png", 32, 20, bg), [T["tooltip"]] + texts)

    css = CSS.substitute(v)
    missing = sorted({u for u in re.findall(r'url\("(assets/[^"]+)"\)', css) if not (out / "gtk-3.0" / u).exists()})
    if missing:
        raise SystemExit(f"{a.NAME}: gtk.css references missing assets: {', '.join(missing)}")
    (out / "gtk-3.0" / "gtk.css").write_text(css + cfg.get("extra", ""))
    (out / "index.theme").write_text(
        "[Desktop Entry]\nType=X-GNOME-Metatheme\n"
        f"Name={a.NAME}\nComment={a.NAME} - matches the e16 theme of the same name\nEncoding=UTF-8\n\n"
        f"[X-GNOME-Metatheme]\nGtkTheme={a.NAME}\n")
    v["assets"] = assets
    return v


def _focus_ring(src, colour):
    """The field art with a 1.5px accent ring on top (focused entries)."""
    m = re.search(r'width="(\d+)" height="(\d+)"', src)
    w, h = int(m[1]), int(m[2])
    ring = (f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="3" fill="none" '
            f'stroke="{colour}" stroke-width="1.5"/>')
    return src[:src.rindex("</svg>")] + ring + "</svg>"
