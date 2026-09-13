#!/usr/bin/env python3
"""Portable structural checks for the SYNC-01 Omarchy theme."""

from pathlib import Path
import struct
import tomllib
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLORS = {
    "mode", "accent", "selection", "muted", "background", "dark_background",
    "darker_background", "lighter_background", "foreground", "dark_foreground",
    "light_foreground", "bright_foreground", "red", "yellow", "orange", "green",
    "cyan", "blue", "magenta", "brown", "bright_red", "bright_yellow",
    "bright_green", "bright_cyan", "bright_blue", "bright_magenta",
}


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"Not a valid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> None:
    palette = tomllib.loads((ROOT / "colors.toml").read_text())
    missing = REQUIRED_COLORS - palette.keys()
    assert not missing, f"Missing palette keys: {sorted(missing)}"
    assert palette["mode"] == "dark"
    for key in REQUIRED_COLORS - {"mode"}:
        value = palette[key]
        assert isinstance(value, str) and len(value) == 7 and value.startswith("#"), (key, value)
        int(value[1:], 16)
    assert contrast(palette["foreground"], palette["background"]) >= 7
    assert contrast(palette["accent"], palette["background"]) >= 7
    assert contrast(palette["orange"], palette["background"]) >= 4.5

    images = sorted((ROOT / "backgrounds").glob("*.png"))
    assert len(images) == 3, f"Expected three wallpapers, found {len(images)}"
    for image in images:
        assert png_size(image) == (3840, 2160), f"Unexpected dimensions: {image} {png_size(image)}"

    for name in ("btop.theme", "chromium.theme", "icons.theme", "keyboard.rgb", "shell.toml", "README.md", "ARTWORK.md", "preview.png", "preview-unlock.png", "unlock.png"):
        assert (ROOT / name).is_file(), f"Missing {name}"
    shell = tomllib.loads((ROOT / "shell.toml").read_text())
    assert shell["hyprland"]["active-border"].count("rgba(") == 3
    assert shell["lock"]["border-active"] == palette["accent"]
    assert png_size(ROOT / "preview.png") == (1920, 1200)
    assert png_size(ROOT / "preview-unlock.png") == (1920, 1080)
    assert png_size(ROOT / "unlock.png") == (800, 188)
    ET.parse(ROOT / "assets/sync-01-mark.svg")
    print("SYNC-01 theme validation passed: palette + 3× 4K wallpapers + integrations")


if __name__ == "__main__":
    main()
