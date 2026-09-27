#!/usr/bin/env python3
"""Rebuild the featured image from the painting. Run from this folder.

The painting is 600x600 and cannot be a featured image on its own: a square
master gets center-cropped into mush at 1.91:1. This mats it onto a 1600x900
ground at 780px, which leaves 60px of vertical margin. That margin is the whole
point. The first cut placed the square at the full 900 height and the OG crop
(which eats 31px top and bottom) sliced the crown off the beanie.

Emits the shipped hero plus the runner-up. Check both with:
  python3 ~/.claude/skills/featured-image-forge/scripts/hero_qc.py <file> --out qc-<name>
and then actually look at all four previews, including thumb-300 at native size.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFilter

SRC = pathlib.Path("images/jspaint-portrait-final.png")
OUT = pathlib.Path("img")
W, H, S = 1600, 900, 780

OUT.mkdir(exist_ok=True)
art = Image.open(SRC).convert("RGB")
sq = art.resize((S, S), Image.NEAREST)  # pixel art: nearest keeps the strokes crisp
x0, y0 = (W - S) // 2, (H - S) // 2

# Shipped: flat dark ground with a warm wash left and a cool wash right, echoing
# the two rim lights in the painting itself.
ground = Image.new("RGB", (W, H), (20, 26, 31))
wash = Image.new("RGB", (W, H), (20, 26, 31))
d = ImageDraw.Draw(wash)
d.ellipse([x0 - 430, -300, x0 + 190, H + 300], fill=(74, 70, 60))
d.ellipse([x0 + S - 190, -300, x0 + S + 430, H + 300], fill=(44, 124, 146))
c = Image.blend(ground, wash.filter(ImageFilter.GaussianBlur(150)), 0.55)
c.paste(sq, (x0, y0))
c.save(OUT / "hero-c2-wash.png")

# Runner-up: the painting's own pixels, blown up and blurred, as the ground.
cover = art.resize((W, W), Image.LANCZOS).crop((0, (W - H) // 2, W, (W - H) // 2 + H))
a = cover.filter(ImageFilter.GaussianBlur(48))
a.paste(sq, (x0, y0))
a.save(OUT / "hero-a2-blurfill.png")

print("wrote", OUT / "hero-c2-wash.png", "(shipped) and", OUT / "hero-a2-blurfill.png")
