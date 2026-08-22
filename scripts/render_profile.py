# -*- coding: utf-8 -*-
"""Work-first profile header. Name stays small. No seal, no rice paper."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
ASSETS.mkdir(parents=True, exist_ok=True)
STILL = Path(r"C:\Users\齐赛军\.grok\sessions\D%3A%5CAPP\01a0293d-fad9-7c10-a3b2-e4062c9f0153\images\4.jpg")

W, H, RX = 1200, 400, 22
INK = (22, 24, 28, 255)
MUTED = (110, 116, 126, 255)
LINE = (210, 216, 224, 255)


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    files = {
        "ui": r"C:\Windows\Fonts\segoeui.ttf",
        "uib": r"C:\Windows\Fonts\segoeuib.ttf",
        "cn": r"C:\Windows\Fonts\msyh.ttc",
        "cnb": r"C:\Windows\Fonts\msyhbd.ttc",
    }
    return ImageFont.truetype(files[kind], size)


def rounded(im: Image.Image) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), RX, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, mask=mask)
    return out


def main() -> None:
    photo = Image.open(STILL).convert("RGB")
    # sample studio gray from a quiet corner
    bg = photo.getpixel((20, 20))
    canvas = Image.new("RGB", (W, H), bg)

    # photo occupies the right 58%
    target_h = H
    scale = target_h / photo.height
    pw = int(photo.width * scale)
    photo = photo.resize((pw, target_h), Image.Resampling.LANCZOS)
    # shift so objects sit in the right panel
    canvas.paste(photo, (W - pw + 40, 0))

    d = ImageDraw.Draw(canvas)
    d.line([(40, 36), (40, H - 36)], fill=(22, 24, 28, 255), width=3)

    d.text((64, 40), "BUILD", font=font("ui", 13), fill=MUTED)
    d.text((64, 78), "硬件", font=font("cnb", 44), fill=INK)
    d.text((64, 140), "桌面工具", font=font("cnb", 44), fill=INK)
    d.text((64, 202), "Agent Skill", font=font("cnb", 44), fill=INK)
    d.text((64, 278), "能用，再开源。", font=font("cn", 20), fill=MUTED)
    d.text((64, 348), "齐赛军  ·  BigQ749", font=font("cn", 14), fill=MUTED)

    rounded(canvas.convert("RGBA")).save(ASSETS / "hero.png")
    print("wrote", ASSETS / "hero.png", (ASSETS / "hero.png").stat().st_size)


if __name__ == "__main__":
    main()
