# -*- coding: utf-8 -*-
"""Render GitHub-safe profile visuals: SVG sources, static PNG, animated GIF."""
from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
ASSETS.mkdir(parents=True, exist_ok=True)

W, H = 1200, 400
RX = 26

BG = (11, 18, 32, 255)
GRID = (26, 40, 64, 90)
CREAM = (247, 243, 234, 255)
INK = (244, 239, 230, 255)
MUTED = (154, 168, 190, 255)
TEAL = (95, 207, 192, 255)
PURPLE = (107, 99, 232, 255)
CORAL = (232, 122, 95, 255)
NAVY = (22, 28, 44, 255)
GREEN = (80, 196, 140, 255)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = {
        "ui": r"C:\Windows\Fonts\segoeui.ttf",
        "uib": r"C:\Windows\Fonts\segoeuib.ttf",
        "cn": r"C:\Windows\Fonts\msyh.ttc",
        "cnb": r"C:\Windows\Fonts\msyhbd.ttc",
        "mono": r"C:\Windows\Fonts\consola.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def ease_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return mask


def draw_grid(draw: ImageDraw.ImageDraw, alpha: int = 70) -> None:
    color = (26, 40, 64, alpha)
    step = 28
    for x in range(0, W + 1, step):
        draw.line([(x, 0), (x, H)], fill=color, width=1)
    for y in range(0, H + 1, step):
        draw.line([(0, y), (W, y)], fill=color, width=1)


def draw_title(layer: Image.Image, underline: float = 1.0, opacity: float = 1.0) -> None:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.text((56, 48), "GITHUB PROFILE  ·  BIGQ749", font=font("ui", 16), fill=MUTED)
    d.rounded_rectangle((56, 78, 104, 84), 2, fill=CORAL)
    d.text((56, 108), "齐赛军", font=font("cnb", 72), fill=INK)
    bar_w = int(236 * underline)
    if bar_w > 0:
        d.rounded_rectangle((56, 206, 56 + bar_w, 216), 4, fill=TEAL)
    d.text((56, 236), "硬件能拿在手里。工具能马上跑起来。", font=font("cn", 22), fill=(206, 214, 226, 255))
    d.text((56, 338), "HARDWARE   ·   DESKTOP TOOL   ·   AGENT SKILL", font=font("ui", 14), fill=MUTED)
    if opacity < 1:
        overlay.putalpha(overlay.getchannel("A").point(lambda a: int(a * opacity)))
    layer.alpha_composite(overlay)


def card_hardware() -> Image.Image:
    im = Image.new("RGBA", (320, 188), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 319, 187), 22, fill=CREAM)
    d.rounded_rectangle((18, 16, 118, 24), 2, fill=CORAL)
    d.text((18, 34), "TRAE K2", font=font("uib", 18), fill=(28, 32, 44, 255))
    d.rounded_rectangle((18, 66, 302, 168), 16, fill=NAVY)
    d.text((34, 80), "TRAE K2", font=font("ui", 12), fill=(180, 190, 210, 255))
    d.text((34, 98), "Shandian", font=font("uib", 20), fill=(90, 170, 255, 255))
    d.rounded_rectangle((34, 132, 170, 140), 4, fill=GREEN)
    d.ellipse((236, 86, 258, 108), fill=(232, 93, 76, 255))
    d.rounded_rectangle((268, 88, 288, 108), 3, fill=(20, 20, 24, 255))
    d.polygon([(248, 122), (268, 154), (228, 154)], fill=PURPLE[:3] + (255,))
    return im


def card_quota() -> Image.Image:
    im = Image.new("RGBA", (300, 168), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 299, 167), 22, fill=TEAL)
    d.text((22, 18), "QUOTADOCK", font=font("uib", 18), fill=(18, 48, 46, 255))
    bars = [(0.72, (255, 255, 255, 230)), (0.44, (18, 48, 46, 220)), (0.86, (255, 255, 255, 200))]
    y = 62
    for ratio, color in bars:
        d.rounded_rectangle((22, y, 278, y + 16), 8, fill=(18, 48, 46, 50))
        d.rounded_rectangle((22, y, 22 + int(256 * ratio), y + 16), 8, fill=color)
        y += 32
    return im


def card_skill() -> Image.Image:
    im = Image.new("RGBA", (280, 156), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 279, 155), 22, fill=PURPLE)
    d.text((20, 16), "AGENT SKILL", font=font("uib", 18), fill=(245, 242, 255, 255))
    nodes = [(58, 96), (140, 72), (222, 108)]
    d.line([nodes[0], nodes[1], nodes[2]], fill=(245, 242, 255, 180), width=4)
    colors = [(95, 207, 192, 255), (247, 243, 234, 255), (232, 122, 95, 255)]
    for (x, y), c in zip(nodes, colors):
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=c)
    return im


def paste_rotated(base: Image.Image, card: Image.Image, xy: tuple[int, int], angle: float, opacity: float = 1.0) -> None:
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((6, 10, card.size[0] - 6, card.size[1] - 2), 22, fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    combo = Image.new("RGBA", (card.size[0] + 20, card.size[1] + 20), (0, 0, 0, 0))
    combo.alpha_composite(shadow, (0, 0))
    combo.alpha_composite(card, (0, 0))
    rotated = combo.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    if opacity < 1:
        rotated.putalpha(rotated.getchannel("A").point(lambda a: int(a * opacity)))
    base.alpha_composite(rotated, xy)


def frame(t: float) -> Image.Image:
    """t in seconds, 0-5 loop."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bg = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(bg)
    draw_grid(d)
    d.ellipse((860, -80, 1280, 260), fill=(90, 70, 160, 28))
    d.ellipse((980, 220, 1380, 560), fill=(40, 120, 130, 24))
    im.alpha_composite(bg)

    # First frame must already read as a finished hero on GitHub.
    draw_title(im, underline=1.0, opacity=1.0)

    def enter(start: float, dur: float, floor: float = 0.72) -> float:
        p = floor + (1.0 - floor) * ease_out((t - start) / dur)
        if t < 4.2:
            return min(1.0, p)
        back = ease_out((t - 4.2) / 0.75)
        return lerp(1.0, floor, back)

    p1 = enter(0.05, 0.85)
    p2 = enter(0.18, 0.85)
    p3 = enter(0.32, 0.85)
    o1 = o2 = o3 = 1.0
    exit_dx = 0
    exit_dy = 0

    paste_rotated(
        im,
        card_hardware(),
        (int(lerp(780, 688, p1)) + exit_dx, int(lerp(-4, 18, p1)) + exit_dy),
        lerp(-14, -8, p1),
        o1,
    )
    paste_rotated(
        im,
        card_quota(),
        (int(lerp(840, 738, p2)) + exit_dx, int(lerp(188, 148, p2)) + exit_dy),
        lerp(-9, -3.5, p2),
        o2,
    )
    paste_rotated(
        im,
        card_skill(),
        (int(lerp(900, 808, p3)) + exit_dx, int(lerp(280, 228, p3)) + exit_dy),
        lerp(11, 6.5, p3),
        o3,
    )

    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(im, mask=rounded_mask((W, H), RX))
    return out


def write_hero_svg() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-labelledby="title desc">
  <title id="title">齐赛军 · GitHub 个人主页</title>
  <desc id="desc">硬件能拿在手里。工具能马上跑起来。作品覆盖工牌固件、桌面工具与 Agent Skill。</desc>
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#1A2840" stroke-width="1"/>
    </pattern>
    <clipPath id="frame"><rect width="1200" height="400" rx="26"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1200" height="400" fill="#0B1220"/>
    <rect width="1200" height="400" fill="url(#grid)"/>
    <circle cx="1080" cy="80" r="220" fill="#5A46A0" opacity="0.12"/>
    <circle cx="1180" cy="390" r="210" fill="#287880" opacity="0.10"/>

    <g id="title-block">
      <text x="56" y="64" fill="#9AA8BE" font-size="16" font-family="Segoe UI, PingFang SC, Microsoft YaHei, sans-serif" letter-spacing="2.4">GITHUB PROFILE  ·  BIGQ749</text>
      <rect x="56" y="78" width="48" height="6" rx="3" fill="#E87A5F"/>
      <text x="56" y="168" fill="#F4EFE6" font-size="72" font-weight="700" font-family="Microsoft YaHei, PingFang SC, Segoe UI, sans-serif">齐赛军</text>
      <rect id="title-underline" x="56" y="186" width="236" height="10" rx="5" fill="#5FCFC0"/>
      <text x="56" y="236" fill="#CED6E2" font-size="22" font-family="Microsoft YaHei, PingFang SC, Segoe UI, sans-serif">硬件能拿在手里。工具能马上跑起来。</text>
      <text x="56" y="352" fill="#9AA8BE" font-size="14" font-family="Segoe UI, PingFang SC, sans-serif" letter-spacing="1.8">HARDWARE   ·   DESKTOP TOOL   ·   AGENT SKILL</text>
    </g>

    <g id="card-hardware" transform="rotate(-8 848 112)">
      <rect x="688" y="18" width="320" height="188" rx="22" fill="#F7F3EA"/>
      <rect x="726" y="52" width="100" height="8" rx="2" fill="#E87A5F"/>
      <text x="726" y="86" fill="#1C202C" font-size="18" font-weight="700" font-family="Segoe UI, sans-serif">TRAE K2</text>
      <rect x="726" y="102" width="284" height="102" rx="16" fill="#161C2C"/>
      <text x="742" y="126" fill="#B4BED2" font-size="12" font-family="Segoe UI, sans-serif">TRAE K2</text>
      <text x="742" y="150" fill="#5AAAFF" font-size="20" font-weight="700" font-family="Segoe UI, sans-serif">Shandian</text>
      <rect x="742" y="164" width="136" height="8" rx="4" fill="#50C48C"/>
      <circle cx="972" cy="128" r="11" fill="#E85D4C"/>
      <rect x="990" y="117" width="20" height="20" rx="3" fill="#141418"/>
    </g>

    <g id="card-quota" transform="rotate(-3.5 888 232)">
      <rect x="738" y="148" width="300" height="168" rx="22" fill="#5FCFC0"/>
      <text x="764" y="166" fill="#12302E" font-size="18" font-weight="700" font-family="Segoe UI, sans-serif">QUOTADOCK</text>
      <rect x="764" y="188" width="256" height="16" rx="8" fill="#12302E" opacity="0.18"/>
      <rect x="764" y="188" width="184" height="16" rx="8" fill="#FFFFFF"/>
      <rect x="764" y="220" width="256" height="16" rx="8" fill="#12302E" opacity="0.18"/>
      <rect x="764" y="220" width="112" height="16" rx="8" fill="#12302E"/>
      <rect x="764" y="252" width="256" height="16" rx="8" fill="#12302E" opacity="0.18"/>
      <rect x="764" y="252" width="220" height="16" rx="8" fill="#FFFFFF" opacity="0.85"/>
    </g>

    <g id="card-skill" transform="rotate(6.5 948 306)">
      <rect x="808" y="228" width="280" height="156" rx="22" fill="#6B63E8"/>
      <text x="832" y="246" fill="#F5F2FF" font-size="18" font-weight="700" font-family="Segoe UI, sans-serif">AGENT SKILL</text>
      <path d="M850 310 L932 286 L1014 322" fill="none" stroke="#F5F2FF" stroke-width="4" opacity="0.75"/>
      <circle cx="850" cy="310" r="16" fill="#5FCFC0"/>
      <circle cx="932" cy="286" r="16" fill="#F7F3EA"/>
      <circle cx="1014" cy="322" r="16" fill="#E87A5F"/>
    </g>
  </g>
</svg>
'''
    (ASSETS / "hero.svg").write_text(svg, encoding="utf-8")


def write_follow_svg() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="88" viewBox="0 0 420 88" role="img" aria-labelledby="t d">
  <title id="t">在 GitHub 关注 齐赛军 @BigQ749</title>
  <desc id="d">Follow the maker on GitHub at BigQ749</desc>
  <rect x="1" y="1" width="418" height="86" rx="18" fill="#F7F8FA" stroke="#E5E7EB"/>
  <path d="M18 18 h14 M18 18 v14" fill="none" stroke="#C5CAD3" stroke-width="1.5"/>
  <path d="M402 18 h-14 M402 18 v14" fill="none" stroke="#C5CAD3" stroke-width="1.5"/>
  <path d="M18 70 h14 M18 70 v-14" fill="none" stroke="#C5CAD3" stroke-width="1.5"/>
  <path d="M402 70 h-14 M402 70 v-14" fill="none" stroke="#C5CAD3" stroke-width="1.5"/>
  <text x="28" y="28" fill="#6B7280" font-size="10" font-family="Segoe UI, sans-serif" letter-spacing="2.2">FOLLOW THE MAKER</text>
  <circle cx="40" cy="56" r="14" fill="#111827"/>
  <text x="35" y="61" fill="#F9FAFB" font-size="14" font-weight="700" font-family="Microsoft YaHei, sans-serif">齐</text>
  <text x="62" y="61" fill="#111827" font-size="18" font-weight="700" font-family="Segoe UI, sans-serif">@BigQ749</text>
  <g transform="translate(332 22)">
    <circle cx="28" cy="22" r="22" fill="#111827"/>
    <path fill="#F9FAFB" d="M28 10.2c-7.2 0-13 5.8-13 13 0 5.7 3.7 10.6 8.9 12.3.6.1.9-.3.9-.6v-2.2c-3.6.8-4.4-1.7-4.4-1.7-.6-1.4-1.4-1.8-1.4-1.8-1.2-.8.1-.8.1-.8 1.3.1 2 1.3 2 1.3 1.1 2 3 1.4 3.7 1.1.1-.8.4-1.4.8-1.7-2.9-.3-5.9-1.4-5.9-6.4 0-1.4.5-2.6 1.3-3.5-.1-.3-.6-1.6.1-3.4 0 0 1.1-.3 3.6 1.3a12.4 12.4 0 0 1 6.6 0c2.5-1.6 3.6-1.3 3.6-1.3.7 1.8.2 3.1.1 3.4.8.9 1.3 2.1 1.3 3.5 0 5-3 6.1-5.9 6.4.5.4.9 1.2.9 2.4v3.5c0 .3.2.7.9.6A13 13 0 0 0 41 23.2c0-7.2-5.8-13-13-13z"/>
  </g>
</svg>
'''
    (ASSETS / "follow-github.svg").write_text(svg, encoding="utf-8")


def write_products_svg() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="220" viewBox="0 0 1200 220" role="img" aria-labelledby="t d">
  <title id="t">三类正在做的事</title>
  <desc id="d">工牌硬件、桌面工具、Agent Skill 三块工作方向。</desc>
  <rect width="1200" height="220" rx="26" fill="#0B1220"/>
  <g font-family="Segoe UI, Microsoft YaHei, PingFang SC, sans-serif">
    <rect x="24" y="24" width="368" height="172" rx="20" fill="#F7F3EA"/>
    <text x="48" y="64" fill="#E87A5F" font-size="18" letter-spacing="2">01  HARDWARE</text>
    <text x="48" y="104" fill="#161C2C" font-size="28" font-weight="700">TRAE K2</text>
    <text x="48" y="140" fill="#4B5563" font-size="20">大赛工牌 → 口袋遥控器</text>
    <text x="48" y="168" fill="#6B7280" font-size="18">ESP32-C3  ·  BLE HID  ·  三键</text>

    <rect x="416" y="24" width="368" height="172" rx="20" fill="#5FCFC0"/>
    <text x="440" y="64" fill="#12302E" font-size="18" letter-spacing="2">02  DESKTOP</text>
    <text x="440" y="104" fill="#12302E" font-size="28" font-weight="700">QuotaDock</text>
    <text x="440" y="140" fill="#12302E" font-size="20">额度浮窗，可分可合</text>
    <text x="440" y="168" fill="#1F4A47" font-size="18">Codex  ·  Grok  ·  OpenCode</text>

    <rect x="808" y="24" width="368" height="172" rx="20" fill="#6B63E8"/>
    <text x="832" y="64" fill="#DDD7FF" font-size="18" letter-spacing="2">03  AGENT SKILL</text>
    <text x="832" y="104" fill="#F5F2FF" font-size="28" font-weight="700">Douyin Analyzer</text>
    <text x="832" y="140" fill="#E4DEFF" font-size="20">链接进，文字稿和摘要出</text>
    <text x="832" y="168" fill="#C9C2F2" font-size="18">Playwright  ·  Whisper  ·  无付费 API</text>
  </g>
</svg>
'''
    (ASSETS / "products.svg").write_text(svg, encoding="utf-8")


def write_en_hero_svg() -> None:
    svg = Path(ASSETS / "hero.svg").read_text(encoding="utf-8")
    svg = svg.replace("齐赛军 · GitHub 个人主页", "Saijun Qi · GitHub profile")
    svg = svg.replace("硬件能拿在手里。工具能马上跑起来。作品覆盖工牌固件、桌面工具与 Agent Skill。", "Hardware you can hold. Tools you can run. Firmware, desktop overlays, and agent skills.")
    svg = svg.replace(">齐赛军<", ">saijun qi<")
    svg = svg.replace("硬件能拿在手里。工具能马上跑起来。", "Hardware you can hold. Tools you can run.")
    (ASSETS / "hero.en.svg").write_text(svg, encoding="utf-8")


def render_png_gif() -> None:
    still = frame(2.4)
    still_rgb = Image.new("RGB", (W, H), (255, 255, 255))
    still_rgb.paste(still, mask=still.split()[-1])
    still.save(ASSETS / "hero.png")

    fps = 20
    step = 1.0 / fps
    times = [round(i * step, 4) for i in range(int(1.2 * fps))]
    times += [2.4]  # one settled hold frame
    times += [round(4.2 + i * step, 4) for i in range(int(0.8 * fps))]
    durations = [int(1000 / fps)] * (len(times) - 1)
    # insert hold duration at the settled frame index
    hold_index = int(1.2 * fps)
    durations.insert(hold_index, 3000)

    rgba_frames = []
    for t in times:
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(frame(t))
        rgba_frames.append(canvas)

    # Shared palette, no dither: smaller and cleaner on GitHub.
    sheet = Image.new("RGBA", (W, H * len(rgba_frames)))
    for i, fr in enumerate(rgba_frames):
        sheet.paste(fr, (0, i * H))
    pal = sheet.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
    palette = pal.getpalette()
    indexed = []
    for fr in rgba_frames:
        q = fr.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)
        q.putpalette(palette)
        # Re-quantize against the shared sheet palette via RGB remap
        rgb = Image.new("RGB", fr.size, (11, 18, 32))
        rgb.paste(fr, mask=fr.split()[-1])
        indexed.append(rgb.quantize(palette=pal, dither=Image.Dither.NONE))

    indexed[0].save(
        ASSETS / "hero.gif",
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )


def main() -> None:
    write_hero_svg()
    write_en_hero_svg()
    write_follow_svg()
    write_products_svg()
    render_png_gif()
    gif = ASSETS / "hero.gif"
    print("wrote", ASSETS)
    if gif.exists():
        print("gif_bytes", gif.stat().st_size)


if __name__ == "__main__":
    main()
