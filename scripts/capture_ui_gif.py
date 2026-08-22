# -*- coding: utf-8 -*-
"""Capture the interactive page as a GitHub-safe looping GIF via Chrome."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "docs" / "index.html"
OUT = ROOT / "assets" / "readme" / "hero.gif"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
W, H = 1280, 720


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="ui-gif-"))
    url = HTML.resolve().as_uri()
    user_data = tmp / "chrome-profile"
    user_data.mkdir()
    frames = []
    # One long capture isn't possible; take delayed screenshots by restarting with virtual time is flaky.
    # Use a single high-quality screenshot as poster, then duplicate with slight crops? Better: screenshot once
    # after the CSS animation has progressed using --virtual-time-budget.
    for i, budget in enumerate([300, 900, 1500, 2100, 2700, 3300, 3900, 4500]):
        shot = tmp / f"{i:02d}.png"
        cmd = [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            f"--window-size={W},{H}",
            f"--screenshot={shot}",
            f"--virtual-time-budget={budget}",
            f"--user-data-dir={user_data}",
            "--hide-scrollbars",
            url,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        im = Image.open(shot).convert("RGB").resize((1200, 675), Image.Resampling.LANCZOS)
        im = im.crop((0, 0, 1200, 620))
        frames.append(im.quantize(colors=128, dither=Image.Dither.NONE))
    durations = [180] * (len(frames) - 1) + [420]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True, disposal=1)
    print("gif", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
