# Contributing

Contributions should preserve the theme's semantic hierarchy and public-repo hygiene.

- Make `colors.toml` the source of truth; do not commit generated terminal configs.
- Keep essential text warm white. Reserve green for live state, orange for warning,
  and alarm pink-red for failures or destructive actions.
- New wallpapers must be original, documented, and at least 3840×2160.
- Do not submit official artwork, anime frames, logos, traced character art, product
  photography, copied interfaces, commercial fonts, or unlicensed third-party media.
- Screenshots must not expose private windows, notifications, account data, or third-party
  copyrighted media.
- Run `python3 tests/validate_theme.py` before opening a pull request.
