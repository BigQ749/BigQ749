# -*- coding: utf-8 -*-
"""iOS / Apple-style profile visuals. Light, large type, clear information."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
ASSETS.mkdir(parents=True, exist_ok=True)

BG = (245, 245, 247)
CARD = (255, 255, 255)
INK = (29, 29, 31)
MUTED = (134, 134, 139)
BLUE = (0, 113, 227)
RX = 28


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    files = {
        "ui": r"C:\Windows\Fonts\segoeui.ttf",
        "uib": r"C:\Windows\Fonts\segoeuib.ttf",
        "cn": r"C:\Windows\Fonts\msyh.ttc",
        "cnb": r"C:\Windows\Fonts\msyhbd.ttc",
    }
    return ImageFont.truetype(files[kind], size)


def round_clip(im: Image.Image, r: int) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), r, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, mask=mask)
    return out


def sheet(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGB", size, BG)


def card(draw_im: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", draw_im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x0, y0 + 6, x1, y1 + 6), 22, fill=(0, 0, 0, 18))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    layer = draw_im.convert("RGBA")
    layer = Image.alpha_composite(layer, shadow)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x0, y0, x1, y1), 22, fill=CARD)
    draw_im.paste(layer.convert("RGB"))


def header() -> Image.Image:
    s = 2
    im = sheet((1200 * s, 300 * s))
    d = ImageDraw.Draw(im)
    d.text((72 * s, 56 * s), "齐赛军", font=font("cnb", 72 * s), fill=INK)
    d.text((76 * s, 148 * s), "Saijun Qi  ·  BigQ749", font=font("ui", 22 * s), fill=MUTED)
    d.text((72 * s, 198 * s), "硬件、桌面工具、Agent Skill。做到能用，再开源。", font=font("cn", 28 * s), fill=INK)
    return round_clip(im.resize((1200, 300), Image.Resampling.LANCZOS).convert("RGBA"), RX)


def works() -> Image.Image:
    s = 2
    W, H = 1200 * s, 520 * s
    im = sheet((W, H))
    items = [
        ("硬件", "TRAE K2", "大赛工牌做成口袋遥控器"),
        ("桌面", "QuotaDock", "额度浮窗，可分可合"),
        ("Skill", "抖音转写", "链接进，文字稿和摘要出"),
        ("工作台", "穹顶", "企业 Agent，本地优先"),
        ("小程序", "台风互助", "附近 SOS 和防灾科普"),
        ("Skill", "Growth Skills", "项目记忆和成长教练"),
    ]
    gap, pad = 20 * s, 28 * s
    cw = (W - pad * 2 - gap * 2) // 3
    ch = (H - pad * 2 - gap - 8 * s) // 2
    for i, (kind, title, desc) in enumerate(items):
        col, row = i % 3, i // 3
        x = pad + col * (cw + gap)
        y = pad + row * (ch + gap)
        card(im, (x, y, x + cw, y + ch))
        d = ImageDraw.Draw(im)
        d.text((x + 28 * s, y + 28 * s), kind, font=font("cn", 16 * s), fill=BLUE)
        d.text((x + 28 * s, y + 68 * s), title, font=font("cnb", 30 * s), fill=INK)
        d.text((x + 28 * s, y + 122 * s), desc, font=font("cn", 20 * s), fill=MUTED)
    return round_clip(im.resize((1200, 520), Image.Resampling.LANCZOS).convert("RGBA"), RX)


def contact() -> Image.Image:
    s = 2
    im = sheet((1200 * s, 140 * s))
    card(im, (28 * s, 16 * s, 1172 * s, 124 * s))
    d = ImageDraw.Draw(im)
    d.text((56 * s, 40 * s), "邮箱", font=font("cn", 16 * s), fill=BLUE)
    d.text((56 * s, 70 * s), "saijunqi@gmail.com", font=font("uib", 28 * s), fill=INK)
    d.text((720 * s, 40 * s), "GitHub", font=font("ui", 16 * s), fill=MUTED)
    d.text((720 * s, 70 * s), "BigQ749", font=font("uib", 28 * s), fill=INK)
    return round_clip(im.resize((1200, 140), Image.Resampling.LANCZOS).convert("RGBA"), 22)


def main() -> None:
    header().save(ASSETS / "hero.png", optimize=True)
    works().save(ASSETS / "works.png", optimize=True)
    contact().save(ASSETS / "contact.png", optimize=True)
    print("hero", (ASSETS / "hero.png").stat().st_size)
    print("works", (ASSETS / "works.png").stat().st_size)


if __name__ == "__main__":
    main()
