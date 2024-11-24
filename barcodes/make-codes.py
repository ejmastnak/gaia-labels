#!/usr/bin/env python

from pathlib import Path
import json, subprocess

products = "../../products/products.json"
svg_outdir = Path("./svg")
png_outdir = Path("./png")

# Create parent directories
svg_outdir.mkdir(exist_ok=True)
png_outdir.mkdir(exist_ok=True)

XDIM_MM=0.264  # [mm]; for 80% magnification

# A value of 72 DPI (magic value, found empirically) makes dimensions in
# Scribus correspond to the X-Dimension used with with zint.
SCRIBUS_DPI=72

FONT_REMOVE="OCRB, monospace"
FONT_REPLACE="OCR B"

FONTSIZE_REMOVE="font-size=\"7.5\""
FONTSIZE_REPLACE="font-size=\"7\""

colors = {
        'amber10': "fffdf5",
        'amber990': "270e02",
        'yellow10': "fefef6",
        'yellow990': "271102",
        'rose10': "fffafa",
        'rose990': "26030b",
}

product_colors = {
        'sntolj100': {
            'fg': "rose990",
            'bg': "rose10",
            },
        'sntolj500': {
            'fg': "rose990",
            'bg': "rose10",
            },
        'jabsok330': {
            'fg': "amber990",
            'bg': "amber10",
            },
        'jabsok750': {
            'fg': "amber990",
            'bg': "amber10",
            },
        'jabkis500': {
            'fg': "amber990",
            'bg': "amber10",
            },
        'bzgkis500': {
            'fg': "yellow990",
            'bg': "yellow10",
            },
}

# And create QR codes
with open(products) as file:
    data = json.load(file)
    for product in data:
        encode_cmd = [
                "zint",
                "--barcode=EANX",
                f"--data={product['ean13']}",
                f"--scalexdimdp={XDIM_MM}mm,{SCRIBUS_DPI}dpi",
                "--quietzones",
                "--compliantheight",
                f"--fg={colors[product_colors[product['codename']]['fg']]}",
                f"--bg={colors[product_colors[product['codename']]['bg']]}",
                f"--output={str(svg_outdir.joinpath(product['codename'] + ".svg"))}",
                ]

        convert_cmd = ["magick",
                   str(svg_outdir.joinpath(product['codename'] + ".svg")),
                   str(png_outdir.joinpath(product['codename'] + ".png")),
                   ]

        font_sed_cmd = [
            "sed", 
            "-i",
            f"s/{FONT_REMOVE}/{FONT_REPLACE}/g",
        ] + [str(svg_file) for svg_file in svg_outdir.glob("*.svg")]

        fontsize_sed_cmd = [
            "sed", 
            "-i",
            f"s/{FONTSIZE_REMOVE}/{FONTSIZE_REPLACE}/g",
        ] + [str(svg_file) for svg_file in svg_outdir.glob("*.svg")]

        
        print(product['codename'])
        subprocess.run(encode_cmd)
        subprocess.run(font_sed_cmd)
        subprocess.run(fontsize_sed_cmd)
        # subprocess.run(convert_cmd)

