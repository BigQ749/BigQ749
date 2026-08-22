# -*- coding: utf-8 -*-
"""Cinematic product header from the real TRAE K2 studio shot."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
ASSETS.mkdir(parents=True, exist_ok=True)
BADGE = Path(r"D:\APP\trae-k2-remote\assets\product\shandian.jpg")

W, H = 1200, 480
RX = 20


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    files = {
        "light": r"C:\Windows\Fonts\segoeuil.ttf",
        "ui": r"C:\Windows\Fonts\segoeui.ttf",
        "cn": r"C:\Windows\Fonts\msyh.ttc",
        "cnb": r"C:\Windows\Fonts\msyhbd.ttc",
    }
    path = files[kind]
    if kind == "light" and not Path(path).exists():
        path = files["ui"]
    return ImageFont.truetype(path, size)


def main() -> None:
    scale = 2
    cw, ch = W * scale, H * scale
    canvas = Image.new("RGB", (cw, ch), (0, 0, 0))

    badge = Image.open(BADGE).convert("RGB")
    badge = ImageEnhance.Contrast(badge).enhance(1.08)
    badge = ImageEnhance.Brightness(badge).enhance(1.04)
    # scale badge to canvas height
    nh = int(ch * 1.12)
    nw = int(badge.width * nh / badge.height)
    badge = badge.resize((nw, nh), Image.Resampling.LANCZOS)
    bx = cw - nw + int(90 * scale)
    by = (ch - nh) // 2
    canvas.paste(badge, (bx, by))

    # left falloff so type sits in true black
    fade = Image.new("L", (cw, ch), 0)
    fd = ImageDraw.Draw(fade)
    for x in range(int(cw * 0.50)):
        t = x / (cw * 0.50)
        a = int(255 * (1 - t) ** 1.35)
        fd.line([(x, 0), (x, ch)], fill=a)
    black = Image.new("RGB", (cw, ch), (0, 0, 0))
    canvas = Image.composite(black, canvas, fade)

    d = ImageDraw.Draw(canvas)
    x = int(72 * scale)
    d.text((x, int(64 * scale)), "BUILD", font=font("light", 22 * scale), fill=(140, 144, 150))
    d.text((x, int(108 * scale)), "硬件", font=font("cnb", 54 * scale), fill=(245, 245, 247))
    d.text((x, int(178 * scale)), "桌面工具", font=font("cnb", 54 * scale), fill=(245, 245, 247))
    d.text((x, int(248 * scale)), "Agent Skill", font=font("cnb", 54 * scale), fill=(245, 245, 247))
    d.text((x, int(334 * scale)), "能用，再开源。", font=font("cn", 22 * scale), fill=(150, 154, 160))
    d.text((x, int(420 * scale)), "齐赛军  ·  BigQ749", font=font("cn", 16 * scale), fill=(90, 94, 100))

    canvas = canvas.resize((W, H), Image.Resampling.LANCZOS)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), RX, fill=255)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(canvas.convert("RGBA"), mask=mask)
    dest = ASSETS / "hero.png"
    out.save(dest, optimize=True)
    print("wrote", dest, dest.stat().st_size)


if __name__ == "__main__":
    main()
