"""Matching YouTube Music themes for Pear Desktop (custom CSS).

YouTube Music paints with two layers of CSS variables: the newer design tokens
(--yt-sys-color-baseline--*) and the older --ytmusic-* ones mapped onto them,
so the palette is poured into both.  On top of that the theme's own art is
reused: the e16 title bar becomes the nav bar and the player bar, the menu
background fills the sidebar and popup menus, the progress art fills the
progress bar, the rofi/GTK highlight marks the active sidebar entry and menu
items, and the wallpaper shows faintly behind the pages.

Pear injects the stylesheet as text, so images are embedded as data URIs and
every declaration is !important (author-origin CSS has to beat the page's).

Output: <out_dir>/ytmusic/<Name>.css
"""

import base64
import json
import re
import subprocess
from pathlib import Path

from gtk import _selection, alpha, luminance, mix, pixel, readable


def _data_uri(png):
    return "data:image/png;base64," + base64.b64encode(Path(png).read_bytes()).decode()


def _wallpaper_uri(src, tmp):
    """The wallpaper, shrunk to 1600px wide JPEG so the CSS stays small."""
    tmp.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["vipsthumbnail", str(src), "--size", "1600x", "-o", f"{tmp}[Q=78,strip]"], check=True,
                   capture_output=True)
    return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()


def _important(css):
    """Add !important to every declaration (custom properties included).
    Declarations are split at ';' only where a property name follows, so the
    ';' inside data: URIs is left alone."""
    out = []
    for line in css.splitlines():
        body = line.rstrip()
        if body.endswith(";") and "{" not in body and "}" not in body:
            indent = body[:len(body) - len(body.lstrip())]
            decls = re.split(r";\s*(?=[a-z-]+\s*:)", body.strip()[:-1])
            body = indent + " ".join(d.strip() + ("" if "!important" in d else " !important") + ";" for d in decls)
        out.append(body)
    return "\n".join(out)


def build(art, out_dir, pal):
    """pal: the dict gtk.build() returned.  Returns the .css path."""
    a, T, P = art, art.TEXT, art.P
    cfg = dict(getattr(a, "YTM", {}))
    assets = pal["assets"]
    out = Path(out_dir) / "ytmusic"

    base = cfg.get("base", a.MATTE["menu"])
    raised = cfg.get("raised", pal["bg"])
    fg = readable(base, [T["menu"], pal["fg"], "#ffffff", "#111111"])
    dim = mix(fg, base, 0.4)
    accent = cfg.get("accent", pal["accent"])
    accent_fg = readable(accent, [T["menu_hilite"], T["dialog"], "#ffffff", "#111111"])
    header_bg = pixel(assets / "header-bg.png", 10, 12, base)
    title_fg = readable(header_bg, [T["title_active"], T["title_inactive"], "#ffffff", "#111111"])
    tooltip_bg = pixel(assets / "tooltip-c.png", 4, 2, base)
    tooltip_fg = readable(tooltip_bg, [T["tooltip"], fg, "#ffffff", "#111111"])
    menu_border = cfg.get("menu_border", P["line"])
    sel = _selection((getattr(a, "ROFI", {}) or {}).get("sel"), P["sel"], T["menu_hilite"])
    sel = re.sub(r"color: [^;]+;$", f"color: {readable(P['sel'], [T['menu_hilite'], '#ffffff', '#111111'])};", sel)

    # the "Music" wordmark is a white image: outline it on light title bars
    logo = ("ytmusic-nav-bar #logo img, ytmusic-nav-bar .logo { filter: drop-shadow(0 0 1px #000) drop-shadow(0 0 1px #000); }"
            if luminance(header_bg) > 0.55 else "")
    hard = json.loads((Path(__file__).parent / "ytmusic_hardcoded.json").read_text())
    hard_primary = ",\n".join(hard["primary"])
    hard_secondary = ",\n".join(hard["secondary"])
    header = _data_uri(assets / "header-bg.png")
    progress = _data_uri(assets / "progress.png")
    tile = (f'background-image: url("{_data_uri(assets / "menu-tile.png")}"); background-repeat: repeat;'
            if a.MENU_BG_TILE else "")
    wall = _wallpaper_uri(Path(__file__).parent / a.WALLPAPER, out / ".wallpaper.jpg")
    veil = cfg.get("veil", 0.86)      # how much of the page colour covers the wallpaper

    css = f"""
/* ---- palette: the new design tokens and the older --ytmusic-* ones ---- */
/* declared on every element: YouTube Music redeclares tokens on inner components */
*, :root, html, html[dark], ytmusic-app {{
    --yt-sys-color-baseline--base-background: {alpha(base, veil)};
    --yt-sys-color-baseline--raised-background: {raised};
    --yt-sys-color-baseline--menu-background: {base};
    --yt-sys-color-baseline--text-primary: {fg};
    --yt-sys-color-baseline--text-secondary: {dim};
    --yt-sys-color-baseline--text-disabled: {mix(fg, base, 0.65)};
    --yt-sys-color-baseline--text-primary-inverse: {accent_fg};
    --yt-sys-color-baseline--inverted-background: {accent};
    --yt-sys-color-baseline--call-to-action: {accent};
    --yt-sys-color-baseline--call-to-action-inverse: {accent_fg};
    --yt-sys-color-baseline--suggested-action: {alpha(accent, 0.2)};
    --yt-sys-color-baseline--outline: {alpha(fg, 0.2)};
    --yt-sys-color-baseline--additive-background: {alpha(fg, 0.1)};
    --yt-sys-color-baseline--button-chip-background-hover: {alpha(fg, 0.16)};
    --yt-sys-color-baseline--mono-tonal-hover: {alpha(fg, 0.16)};
    --yt-sys-color-baseline--touch-response: {alpha(accent, 0.3)};
    --yt-sys-color-baseline--static-brand-red: {accent};
    --yt-sys-color-baseline--brand-red-contrast: {accent};
    --ytmusic-background: {alpha(base, veil)};
    --ytmusic-general-background-a: {raised};
    --ytmusic-general-background-c: {alpha(base, veil)};
    --ytmusic-brand-background-solid: {raised};
    --ytmusic-nav-bar: {header_bg};
    --ytmusic-player-bar-background: {header_bg};
    --ytmusic-color-black1: {raised};
    --ytmusic-color-black2: {base};
    --ytmusic-color-black4: {base};
    --ytmusic-color-white1: {fg};
    --ytmusic-color-white1-alpha10: {alpha(fg, 0.1)};
    --ytmusic-color-white1-alpha15: {alpha(fg, 0.15)};
    --ytmusic-color-white1-alpha20: {alpha(fg, 0.2)};
    --ytmusic-color-white1-alpha25: {alpha(fg, 0.25)};
    --ytmusic-color-white1-alpha30: {alpha(fg, 0.3)};
    --ytmusic-color-white1-alpha50: {alpha(fg, 0.5)};
    --ytmusic-color-white1-alpha70: {alpha(fg, 0.7)};
    --ytmusic-color-white1-alpha95: {alpha(fg, 0.95)};
    --ytmusic-text-primary: {fg};
    --ytmusic-text-secondary: {dim};
    --ytmusic-display-2_-_color: {fg};
    --premium-yt-spec-text-primary: {fg};
    --premium-yt-spec-text-secondary: {dim};
    --ytmusic-color-grey2: {dim};
    --ytmusic-color-grey3: {dim};
    --ytmusic-color-youtubered: {accent};
    --ytmusic-color-mediumred: {accent};
    --ytmusic-color-lightred: {accent};
    --ytmusic-brand-link-text: {pal["link"]};
    --ytmusic-play-button-background-color: {accent};
    --ytmusic-play-button-active-background-color: {mix(accent, "#ffffff", 0.2)};
    --ytmusic-play-button-icon-color: {accent_fg};
    --ytmusic-search-background: {base};
    --ytmusic-search-box-text-secondary: {dim};
    --ytmusic-color-blue-1: {accent};
    --ytmusic-color-lightblue: {accent};
    --paper-toggle-button-checked-bar-color: {accent};
    --paper-toggle-button-checked-button-color: {mix(accent, "#ffffff", 0.3)};
    --paper-toggle-button-checked-ink-color: {accent};
    --paper-toggle-button-unchecked-bar-color: {alpha(fg, 0.3)};
    --paper-toggle-button-unchecked-button-color: {mix(fg, base, 0.2)};
    --paper-slider-active-color: {accent};
    --paper-slider-knob-color: {accent};
    --paper-slider-knob-start-color: {accent};
    --paper-slider-knob-start-border-color: {accent};
    --paper-slider-container-color: {alpha(fg, 0.2)};
    --paper-slider-secondary-color: {alpha(fg, 0.35)};
}}

/* ---- the wallpaper, faintly, behind every page ---- */
html, body {{
    background: {base} url("{wall}") center / cover fixed no-repeat;
}}

/* ---- nav bar and player bar: the e16 title bar ---- */
#nav-bar-background.ytmusic-app-layout {{
    background: {header_bg} url("{header}") center / 100% 100% no-repeat;
    opacity: 1;
    border-bottom: none;
}}
#player-bar-background.ytmusic-app-layout {{
    background: {header_bg} url("{header}") center / 100% 100% no-repeat;
    transform: translateZ(0) scaleY(-1);
}}
ytmusic-nav-bar, ytmusic-nav-bar *, ytmusic-player-bar, ytmusic-player-bar * {{
    --yt-sys-color-baseline--text-primary: {title_fg};
    --yt-sys-color-baseline--text-secondary: {mix(title_fg, header_bg, 0.3)};
    --ytmusic-color-white1: {title_fg};
    --ytmusic-text-primary: {title_fg};
    --ytmusic-text-secondary: {mix(title_fg, header_bg, 0.3)};
    --iron-icon-fill-color: {title_fg};
    --yt-sys-color-baseline--text-primary-inverse: {readable(title_fg, [header_bg, base, "#111111", "#ffffff"])};
}}
ytmusic-nav-bar, ytmusic-player-bar {{ color: {title_fg}; }}
ytmusic-nav-bar {{
    --ytmusic-search-bar-background-bauhaus: {alpha(title_fg, 0.12)};
    --ytmusic-search-box-text-secondary: {mix(title_fg, header_bg, 0.3)};
}}
ytmusic-nav-bar yt-icon-button, ytmusic-nav-bar yt-icon, ytmusic-nav-bar .yt-icon-shape,
ytmusic-nav-bar ytmusic-search-box:not([opened]) {{
    color: {title_fg};
    fill: currentColor;
}}
ytmusic-player-bar {{ background: transparent; }}

/* text YouTube Music hard-codes as white / grey */
.title.ytmusic-two-row-item-renderer, .title.ytmusic-carousel-shelf-basic-header-renderer,
.title.ytmusic-responsive-list-item-renderer, .title.ytmusic-player-bar, .title.ytmusic-detail-header-renderer,
.title.ytmusic-immersive-header-renderer, .title.ytmusic-player-queue-item, h1, h2,
.song-title.ytmusic-player-queue-item, .content-info-wrapper.ytmusic-player-bar .title.ytmusic-player-bar {{
    color: var(--yt-sys-color-baseline--text-primary);
    --yt-endpoint-color: var(--yt-sys-color-baseline--text-primary);
    --yt-endpoint-hover-color: var(--yt-sys-color-baseline--text-primary);
    --yt-endpoint-visited-color: var(--yt-sys-color-baseline--text-primary);
}}
.subtitle.ytmusic-two-row-item-renderer, .strapline-text.ytmusic-carousel-shelf-basic-header-renderer,
.secondary-flex-columns.ytmusic-responsive-list-item-renderer, .byline.ytmusic-player-bar,
.byline.ytmusic-player-queue-item, .subtitle.ytmusic-detail-header-renderer,
.duration.ytmusic-player-queue-item, .time-info.ytmusic-player-bar {{
    color: var(--yt-sys-color-baseline--text-secondary);
    --yt-endpoint-color: var(--yt-sys-color-baseline--text-secondary);
    --yt-endpoint-hover-color: var(--yt-sys-color-baseline--text-primary);
    --yt-endpoint-visited-color: var(--yt-sys-color-baseline--text-secondary);
}}

/* everything else YouTube Music hard-codes as white / grey (ytmusic_hardcoded.json) */
{hard_primary} {{
    color: var(--yt-sys-color-baseline--text-primary);
    --yt-endpoint-color: var(--yt-sys-color-baseline--text-primary);
}}
{hard_secondary} {{
    color: var(--yt-sys-color-baseline--text-secondary);
    --yt-endpoint-color: var(--yt-sys-color-baseline--text-secondary);
}}
tp-yt-paper-tab, tp-yt-paper-tab .tab-content, ytmusic-guide-entry-renderer .title {{
    color: var(--yt-sys-color-baseline--text-secondary);
}}
tp-yt-paper-tab.iron-selected, tp-yt-paper-tab.iron-selected .tab-content {{
    color: var(--yt-sys-color-baseline--text-primary);
}}

/* sidebar sign-in promo */
ytmusic-guide-signin-promo-renderer {{
    --ytmusic-guide-signin-promo-text-secondary: {dim};
    --ytmusic-overlay-text-secondary: {dim};
}}
ytmusic-guide-signin-promo-renderer button {{
    background: {alpha(fg, 0.12)};
    color: {fg};
    border: 1px solid {alpha(fg, 0.2)};
}}

/* YouTube's promo bubbles ("Start playback" etc.) */
yt-bubble-hint-renderer, yt-bubble-hint-renderer *, yt-bubble-hint-renderer tp-yt-paper-dialog,
yt-tooltip-renderer, yt-tooltip-renderer #tooltip, yt-tooltip-renderer tp-yt-paper-dialog {{
    background-color: {accent};
    color: {accent_fg};
    --yt-sys-color-baseline--call-to-action: {accent};
    --ytmusic-color-blue-1: {accent};
}}

/* links inside titles/subtitles carry their own colour */
.title a, .subtitle a, .byline a, .secondary-flex-columns a, .strapline-text a {{
    --yt-endpoint-color: currentColor;
    --yt-endpoint-hover-color: {accent};
    color: inherit;
}}

/* mood / genre chips */
ytmusic-chip-cloud-chip-renderer a, ytmusic-chip-cloud-chip-renderer .gradient-box {{
    background: {alpha(fg, 0.1)};
    color: {fg};
    border: 1px solid {alpha(fg, 0.18)};
}}
ytmusic-chip-cloud-chip-renderer[is-selected] a, ytmusic-chip-cloud-chip-renderer[chip-style=STYLE_PRIMARY] a {{
    background: {accent};
    color: {accent_fg};
}}

{logo}

/* progress bar: the theme's progress art */
#progress-bar #primaryProgress {{
    background: {accent} url("{progress}") center / 100% 100% no-repeat;
}}
#progress-bar .slider-knob-inner, #progress-bar #sliderKnob .slider-knob-inner {{
    background-color: {accent};
    border-color: {accent};
}}

/* ---- sidebar: the e16 menu ---- */
tp-yt-app-drawer #contentContainer, #guide-wrapper.ytmusic-app, ytmusic-guide-renderer,
#mini-guide-background.ytmusic-app-layout, #guide-spacer.ytmusic-app {{
    background-color: {alpha(base, 0.94)};
    {tile}
}}
ytmusic-guide-entry-renderer[active] tp-yt-paper-item.ytmusic-guide-entry-renderer {{
    {sel}
}}
ytmusic-guide-entry-renderer[active] .title.ytmusic-guide-entry-renderer,
ytmusic-guide-entry-renderer[active] yt-icon {{
    color: inherit;
    fill: currentColor;
}}

/* ---- popup menus ---- */
tp-yt-iron-dropdown ytmusic-menu-popup-renderer, ytmusic-menu-popup-renderer, ytmusic-multi-select-menu-renderer {{
    background-color: {base};
    {tile}
    border: 1px solid {menu_border};
    border-radius: 6px;
}}
ytmusic-menu-navigation-item-renderer:hover, ytmusic-menu-service-item-renderer:hover,
ytmusic-toggle-menu-service-item-renderer:hover, ytmusic-menu-service-item-download-renderer:hover {{
    {sel}
}}

/* ---- tooltips ---- */
tp-yt-paper-tooltip #tooltip, tp-yt-paper-tooltip .tp-yt-paper-tooltip[id=tooltip] {{
    background: {tooltip_bg};
    color: {tooltip_fg};
    border: 1px solid {menu_border};
}}

/* ---- scrollbars ---- */
::-webkit-scrollbar-thumb {{ background-color: {alpha(fg, 0.3)}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background-color: {accent}; }}
::-webkit-scrollbar-track {{ background: transparent; }}
"""
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{a.NAME}.css"
    path.write_text(f"/* {a.NAME} - YouTube Music (Pear Desktop) theme, generated alongside the "
                    f"e16 theme (see ytmusic.py) */\n" + _important(css))
    return path
