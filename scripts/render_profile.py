# -*- coding: utf-8 -*-
"""Profile visuals: rice-paper + 齐 seal. Not the dark-grid repo template."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"
ASSETS.mkdir(parents=True, exist_ok=True)

PAPER = Path(r"C:\Users\齐赛军\.grok\sessions\D%3A%5CAPP\01a0293d-fad9-7c10-a3b2-e4062c9f0153\images\3.jpg")
STAMP = ASSETS / "avatar.jpg"

W, H = 1200, 420
INK = (28, 24, 20, 255)
MUTED = (92, 78, 64, 255)
CINNABAR = (179, 51, 34, 255)
RX = 22


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    files = {
        "ui": r"C:\Windows\Fonts\segoeui.ttf",
        "uib": r"C:\Windows\Fonts\segoeuib.ttf",
        "cn": r"C:\Windows\Fonts\msyh.ttc",
        "cnb": r"C:\Windows\Fonts\msyhbd.ttc",
        "kai": r"C:\Windows\Fonts\simkai.ttf",
        "mono": r"C:\Windows\Fonts\consola.ttf",
    }
    path = files[kind]
    if kind == "kai" and not Path(path).exists():
        path = files["cnb"]
    return ImageFont.truetype(path, size)


def rounded_mask(size, r) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def knockout_paper(im: Image.Image, thresh: int = 232) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= thresh and g >= thresh and b >= thresh:
                px[x, y] = (255, 255, 255, 0)
    return im


def paper_sheet(size: tuple[int, int]) -> Image.Image:
    src = Image.open(PAPER).convert("RGB")
    # crop away the outer mount, keep the sheet
    w, h = src.size
    src = src.crop((int(w * 0.06), int(h * 0.08), int(w * 0.97), int(h * 0.93)))
    src = ImageEnhance.Contrast(src).enhance(1.05)
    return src.resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def stamp_layer(diameter: int) -> Image.Image:
    raw = Image.open(STAMP).convert("RGBA")
    ink = knockout_paper(raw)
    ink = ink.resize((diameter, diameter), Image.Resampling.LANCZOS)
    return ink


def frame(t: float = 1.0) -> Image.Image:
    im = paper_sheet((W, H))
    d = ImageDraw.Draw(im)

    # quiet letterpress margin
    d.rectangle((28, 28, W - 29, H - 29), outline=(120, 96, 78, 70), width=1)
    d.rectangle((34, 34, W - 35, H - 35), outline=(120, 96, 78, 40), width=1)

    p = max(0.0, min(1.0, t))
    seal = stamp_layer(268)
    if p < 1:
        seal.putalpha(seal.getchannel("A").point(lambda a: int(a * p)))
    shadow = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((16, 22, 284, 290), fill=(40, 24, 16, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(shadow, (46, 58))
    im.alpha_composite(seal, (58, 68))

    # cinnabar colophon bar
    bar_h = int(220 * p) if p else 220
    d.rectangle((360, 86, 366, 86 + bar_h), fill=CINNABAR)

    d.text((392, 78), "齐赛军", font=font("cnb", 64), fill=INK)
    d.text((396, 162), "SAIJUN QI  ·  BIGQ749", font=font("ui", 16), fill=MUTED)
    d.text((392, 210), "能摸到的硬件。能跑起来的工具。能交给 Agent 的 Skill。", font=font("cn", 22), fill=INK)
    d.text((392, 250), "做到能用，再开源。", font=font("cn", 22), fill=INK)

    d.text((392, 318), "saijunqi@gmail.com", font=font("ui", 20), fill=CINNABAR)
    d.text((392, 350), "github.com/BigQ749", font=font("ui", 16), fill=MUTED)

    # small square seal, lower right
    d.rounded_rectangle((1078, 318, 1148, 388), 4, outline=CINNABAR, width=3)
    d.text((1090, 332), "齐", font=font("cnb", 36), fill=CINNABAR)

    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(im, mask=rounded_mask((W, H), RX))
    return out


def works_board() -> Image.Image:
    im = paper_sheet((1200, 360))
    d = ImageDraw.Draw(im)
    d.rectangle((28, 28, 1171, 331), outline=(120, 96, 78, 70), width=1)
    d.text((56, 48), "WORKS", font=font("ui", 14), fill=CINNABAR)
    items = [
        ("01", "TRAE K2", "工牌 → 口袋遥控器"),
        ("02", "QuotaDock", "额度浮窗，可分可合"),
        ("03", "抖音转写", "链接进，文字出"),
        ("04", "穹顶", "企业 Agent 工作台"),
        ("05", "台风互助", "附近 SOS + 科普"),
        ("06", "Growth Skills", "记忆，和会看证据的教练"),
    ]
    for i, (n, title, desc) in enumerate(items):
        col, row = i % 3, i // 3
        x, y = 56 + col * 380, 96 + row * 118
        d.text((x, y), n, font=font("ui", 14), fill=CINNABAR)
        d.text((x, y + 24), title, font=font("cnb", 24), fill=INK)
        d.text((x, y + 62), desc, font=font("cn", 16), fill=MUTED)
    out = Image.new("RGBA", (1200, 360), (0, 0, 0, 0))
    out.paste(im, mask=rounded_mask((1200, 360), RX))
    return out


def contact_card() -> Image.Image:
    im = paper_sheet((840, 96))
    d = ImageDraw.Draw(im)
    d.rectangle((10, 10, 829, 85), outline=CINNABAR, width=2)
    d.text((28, 22), "MAIL", font=font("ui", 11), fill=CINNABAR)
    d.text((28, 46), "saijunqi@gmail.com", font=font("uib", 22), fill=INK)
    d.text((520, 28), "GITHUB", font=font("ui", 11), fill=MUTED)
    d.text((520, 50), "@BigQ749", font=font("uib", 20), fill=INK)
    out = Image.new("RGBA", (840, 96), (0, 0, 0, 0))
    out.paste(im, mask=rounded_mask((840, 96), 14))
    return out


def render_gif() -> None:
    still = frame(1.0)
    still.save(ASSETS / "hero.png")
    fps = 16
    times = [min(1.0, (i / fps) / 0.7) for i in range(int(0.7 * fps))] + [1.0]
    durations = [int(1000 / fps)] * (len(times) - 1) + [2800]
    frames = []
    for t in times:
        fr = frame(t)
        rgb = Image.new("RGB", (W, H), (236, 226, 208))
        rgb.paste(fr, mask=fr.split()[-1])
        frames.append(rgb.quantize(colors=128, dither=Image.Dither.NONE))
    frames[0].save(
        ASSETS / "hero.gif",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )


def main() -> None:
    render_gif()
    works_board().save(ASSETS / "works.png")
    contact_card().save(ASSETS / "contact.png")
    print("gif", (ASSETS / "hero.gif").stat().st_size)
    print("hero", (ASSETS / "hero.png").stat().st_size)


if __name__ == "__main__":
    main()
