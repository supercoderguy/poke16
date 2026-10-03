"""Matching rofi themes, built from the same Art as the e16 themes.

The rofi window is laid out like an e16 menu: the input bar is a banner
rendered from the theme's own emblem + title bar, the selected row uses the
theme's menu highlight art, and colours/fonts come from the palette.
Per-theme tweaks go in an Art's ROFI dict (see DEFAULTS below).
"""

import re
import subprocess
from pathlib import Path

ZOOM = 1.5            # art is drawn at e16 size, rendered 1.5x for rofi
WIDTH = 400           # banner/row width in art units (600px on screen)

DEFAULTS = dict(
    radius=0,             # window corner radius (px)
    border=2,             # window border width (px)
    border_color=None,    # default: palette "line"
    bg=None,              # default: the menu matte colour
    lines=10,
    font_size=10,
    sel=None,             # rasi declarations for the selected row (the menu highlight)
    title_pad=None,       # prompt inset past the title ornament (art units); default M["title_pad_l"]
)


def _prefix_ids(src, pre):
    """Namespace an SVG's ids so several can be nested in one document."""
    ids = re.findall(r'id="([^"]+)"', src)
    for i in ids:
        src = src.replace(f'id="{i}"', f'id="{pre}{i}"').replace(f"url(#{i})", f"url(#{pre}{i})")
    return src


def _inner(src):
    """Strip the outer <svg ...> wrapper, keeping defs and body."""
    return src[src.index(">") + 1:src.rindex("</svg>")]


def _render(svgsrc, dst, zoom=ZOOM):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".svg")
    tmp.write_text(svgsrc)
    subprocess.run(["rsvg-convert", "-z", str(zoom), "-o", str(dst), str(tmp)], check=True)
    tmp.unlink()


def _font(pango, size):
    """'pango:Adwaita Sans Bold 9' -> 'Adwaita Sans Bold 10'"""
    name = pango.removeprefix("pango:").rsplit(" ", 1)[0]
    return f"{name} {size}"


def build(art, out_dir):
    """Write <out_dir>/rofi/<Name>.rasi plus its images; returns the .rasi path."""
    a, M, P, T = art, art.M, art.P, art.TEXT
    cfg = {**DEFAULTS, **getattr(a, "ROFI", {})}
    rdir = Path(out_dir) / "rofi"
    img = rdir / "img"

    bg = cfg["bg"] or a.MATTE["menu"]
    inner_w = round(WIDTH * ZOOM) - 2 * cfg["border"]      # px inside the window border
    W, H = inner_w / ZOOM, 900 / ZOOM                        # in art units

    # One tall background for the whole window, scaled by width only (rofi keeps
    # aspect ratio when scaling, so anything else tiles): the emblem + active
    # title bar across the top, the menu background below.
    TH = M["title_h"]
    emb = _prefix_ids(a.emblem(TH, "active"), "e_")
    tit = _prefix_ids(a.title(round(W - TH), TH, True), "t_")
    below = f'<rect x="0" y="{TH}" width="{W}" height="{H - TH}" fill="{bg}"/>'
    tile = a.MENU_BG_TILE
    if tile:
        pat = _prefix_ids(a.menu_bg(tile, tile), "p_")
        below += (f'<defs><pattern id="tile" patternUnits="userSpaceOnUse" width="{tile / ZOOM}" '
                  f'height="{tile / ZOOM}"><svg width="{tile / ZOOM}" height="{tile / ZOOM}" '
                  f'viewBox="0 0 {tile} {tile}">{_inner(pat)}</svg></pattern></defs>'
                  f'<rect x="0" y="{TH}" width="{W}" height="{H - TH}" fill="url(#tile)"/>')
    backdrop = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                + below
                + f'<svg x="0" y="0" width="{TH}" height="{TH}">{_inner(emb)}</svg>'
                + f'<svg x="{TH}" y="0" width="{round(W - TH)}" height="{TH}">{_inner(tit)}</svg></svg>')
    _render(backdrop, img / "window.png")

    border = cfg["border_color"] or P["line"]
    font = _font(a.FONTS["menu"], cfg["font_size"])
    tfont = _font(a.FONTS["border"], cfg["font_size"])
    pad_l = round((TH + (cfg["title_pad"] or M["title_pad_l"])) * ZOOM)
    bh = round(TH * ZOOM)
    sel = cfg["sel"] or f"background-color: {P['sel']};"

    rasi = f"""/* {a.NAME} - rofi theme generated alongside the e16 theme (see rofi.py) */

* {{
    font:             "{font}";
    bg:               {bg};
    fg:               {T['menu']};
    sel-fg:           {T['menu_hilite']};
    title-fg:         {T['title_active']};
    dim:              {T['title_inactive']};
    border-col:       {border};
    urgent:           {P['danger']};
    active:           {P['accent']};
    background-color: transparent;
    text-color:       @fg;
}}

window {{
    width:            {round(WIDTH * ZOOM)}px;
    background-color: @bg;
    background-image: url("{(img / "window.png").resolve()}", width);
    border:           {cfg['border']}px;
    border-color:     @border-col;
    border-radius:    {cfg['radius']}px;
    padding:          0;
}}

mainbox {{
    spacing:  0;
    children: [ inputbar, message, listview, mode-switcher ];
}}

/* the e16 title bar, emblem and all */
/* sits over the title-bar banner at the top of the window image */
inputbar {{
    padding:          0;
    spacing:          0;
    children:         [ prompt, textbox-prompt-colon, entry, num-filtered-rows ];
}}
prompt, entry, textbox-prompt-colon, num-filtered-rows {{
    font:           "{tfont}";
    text-color:     @title-fg;
    vertical-align: 0.5;
    padding:        {round(bh * 0.24)}px 0 {round(bh * 0.32)}px 8px;
}}
prompt            {{ padding: {round(bh * 0.24)}px 0 {round(bh * 0.32)}px {pad_l}px; }}
num-filtered-rows {{ padding: {round(bh * 0.24)}px 16px {round(bh * 0.32)}px 8px; }}
textbox-prompt-colon {{ str: "›"; expand: false; }}
prompt               {{ expand: false; }}
entry {{
    placeholder:       "type to search";
    placeholder-color: @dim;
    cursor:            text;
}}
num-filtered-rows {{ text-color: @dim; }}

listview {{
    lines:        {cfg['lines']};
    padding:      8px 0;
    spacing:      0;
    fixed-height: true;
    scrollbar:    false;
}}

element {{
    padding: 0;
    spacing: 0;
    margin:  0 4px;
}}
element selected.normal, element selected.active, element selected.urgent {{
    {sel}
    text-color: @sel-fg;
}}
element normal.urgent   {{ text-color: @urgent; }}
element normal.active   {{ text-color: @active; }}
element-icon            {{ size: 1.2em; padding: 0 0 0 12px; }}
element-text            {{ text-color: inherit; vertical-align: 0.5; padding: 7px 12px; }}

message {{ padding: 8px 14px; }}
textbox {{ text-color: @fg; }}

mode-switcher {{ spacing: 0; }}
button {{ padding: 6px; text-color: @dim; }}
button selected {{
    {sel}
    text-color: @sel-fg;
}}
"""
    extra = getattr(a, "ROFI_EXTRA", "")
    path = rdir / f"{a.NAME}.rasi"
    path.write_text(rasi + extra)
    return path
