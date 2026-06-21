# -*- coding: utf-8 -*-
"""Regenerates the pixel-art textures used by build_campus.py -> campus_tex.json
Run:  python3 gen_textures.py    (requires pillow:  pip install pillow)
"""
import io, base64, json, os, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(7)

def uri(im, fmt='PNG'):
    b = io.BytesIO(); im.save(b, fmt)
    pre = "data:image/png;base64," if fmt == 'PNG' else "data:image/jpeg;base64,"
    return pre + base64.b64encode(b.getvalue()).decode()

tex = {}

# GRASS 32x32
g = Image.new('RGB', (32, 32), (86, 128, 58)); d = ImageDraw.Draw(g)
greens = [(74, 116, 50), (96, 140, 64), (110, 152, 74), (82, 124, 56)]
for y in range(32):
    for x in range(32):
        if random.random() < 0.5: d.point((x, y), fill=random.choice(greens))
for _ in range(18):
    x, y = random.randint(0, 31), random.randint(0, 31)
    d.point((x, y), fill=(126, 168, 84)); d.point((x, (y + 1) % 32), fill=(120, 160, 80))
tex['grass'] = uri(g.convert('RGB'))

# PATH 32x32 flagstone
p = Image.new('RGB', (32, 32), (196, 182, 158)); d = ImageDraw.Draw(p)
tans = [(186, 172, 148), (204, 190, 166), (176, 162, 138), (210, 198, 176)]
for y in range(32):
    for x in range(32):
        if random.random() < 0.45: d.point((x, y), fill=random.choice(tans))
for x in range(0, 33, 16): d.line([(x, 0), (x, 32)], fill=(150, 138, 116))
for y in range(0, 33, 16): d.line([(0, y), (32, y)], fill=(150, 138, 116))
tex['path'] = uri(p.convert('RGB'))

# FACADES 64x64 (brick + stone), white-framed windows
def facade(base, mortar, frame, glass, glasshi):
    f = Image.new('RGB', (64, 64), base); d = ImageDraw.Draw(f)
    for i, y in enumerate(range(0, 64, 8)):
        d.line([(0, y), (64, y)], fill=mortar)
        off = 8 if i % 2 else 0
        for x in range(off, 64, 16): d.line([(x, y), (x, y + 8)], fill=mortar)
    x0, y0, x1, y1 = 18, 15, 46, 49
    d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=frame)
    d.rectangle([x0, y0, x1, y1], fill=glass)
    d.rectangle([x0, y0, x1, (y0 + y1) // 2], fill=glasshi)
    d.line([((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1)], fill=frame, width=2)
    d.line([(x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2)], fill=frame, width=2)
    return f
tex['facade1'] = uri(facade((150, 72, 58), (186, 158, 142), (236, 232, 224), (74, 98, 120), (120, 150, 172)))
tex['facade2'] = uri(facade((176, 170, 156), (204, 198, 182), (248, 246, 240), (86, 108, 128), (132, 158, 178)))

# SIGN 64x40 cream board
s = Image.new('RGBA', (64, 40), (240, 236, 226, 255)); d = ImageDraw.Draw(s)
for _ in range(60):
    x, y = random.randint(2, 61), random.randint(2, 37)
    if random.random() < 0.5: d.point((x, y), fill=(232, 228, 216, 255))
d.rectangle([0, 0, 63, 39], outline=(120, 110, 96, 255), width=2)
d.rectangle([2, 2, 61, 37], outline=(206, 198, 182, 255), width=1)
tex['sign'] = uri(s)

# SKY 160x80 equirect, posterized bands + blocky clouds
sk = Image.new('RGB', (160, 80)); d = ImageDraw.Draw(sk)
bands = [(70, 120, 200), (92, 146, 212), (132, 176, 224), (176, 202, 232), (212, 224, 236), (238, 232, 216)]
for y in range(80):
    d.line([(0, y), (160, y)], fill=bands[min(len(bands) - 1, int(y / 80 * len(bands)))])
for _ in range(26):
    cx, cy = random.randint(0, 150), random.randint(8, 34); w = random.randint(6, 16); h = random.randint(3, 6)
    d.rectangle([cx, cy, cx + w, cy + h], fill=(248, 248, 250))
    d.rectangle([cx + 2, cy - 2, cx + w - 2, cy + 1], fill=(252, 252, 255))
tex['sky'] = uri(sk.convert('RGB'))

# CLOUD puff 40x22 RGBA
c = Image.new('RGBA', (40, 22), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
for (cx, cy, r) in [(12, 14, 7), (20, 11, 8), (28, 14, 7), (20, 15, 9)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 255, 235))
tex['cloud'] = uri(c)

json.dump(tex, open(os.path.join(HERE, 'campus_tex.json'), 'w'))
print("wrote campus_tex.json with keys:", sorted(tex.keys()))
