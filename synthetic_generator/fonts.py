import os
from typing import Dict

import requests

FONT_URLS: Dict[str, str] = {
    "regular": "https://github.com/Phonbopit/sarabun-webfont/raw/master/fonts/thsarabunnew-webfont.ttf",
    "bold": "https://github.com/Phonbopit/sarabun-webfont/raw/master/fonts/thsarabunnew_bold-webfont.ttf",
}

FONT_PATHS: Dict[str, str] = {
    "regular": "th_sarabun.ttf",
    "bold": "th_sarabun_bold.ttf",
}


def download_fonts(font_dir: str = "synthetic_generator/fonts_file") -> Dict[str, str]:
    """Download Sarabun fonts if not present. Returns dict of font paths. Default path is '@/fonts_file'."""
    os.makedirs(font_dir, exist_ok=True)
    paths: Dict[str, str] = {}
    for style, url in FONT_URLS.items():
        path = os.path.join(font_dir, FONT_PATHS[style])
        if not os.path.exists(path):
            print(f"Downloading {style} font...")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            with open(path, "wb") as f:
                f.write(resp.content)
        paths[style] = path
    return paths
