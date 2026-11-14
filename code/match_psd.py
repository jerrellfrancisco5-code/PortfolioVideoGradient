# Second pass: match the live posters that had no PNG export against the flattened composites inside the PSDs.
import os, json
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\Users\Administrator\Desktop\01 Projects\_Studio_Francisco\_Personal_Campaigns\Posters'
OUT = os.path.join(HERE, '_vr')
NEED = [2, 6, 7, 11, 12, 14, 15, 17, 18, 19, 20, 22, 26, 27]
cache = os.path.join(OUT, 'psd.json'); psd = json.load(open(cache)) if os.path.exists(cache) else {}
for root, _, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith('.psd'): continue
        p = os.path.join(root, f); rel = os.path.relpath(p, SRC)
        if rel in psd: continue
        try:
            im = Image.open(p); w, h = im.size; im = im.convert('RGB'); im.thumbnail((400, 400))
            t = 'p_%d.jpg' % len(psd); im.save(os.path.join(OUT, t), quality=80); psd[rel] = {'w': w, 'h': h, 't': t}; print('ok', rel, w, h, flush=True)
        except Exception as e: psd[rel] = {'err': str(e)[:80]}; print('skip', rel, str(e)[:80], flush=True)
        json.dump(psd, open(cache, 'w'))
def sig(im, size=(24, 32)):
    v = np.asarray(im.convert('L').resize(size, Image.LANCZOS), dtype=np.float32); return (v - v.mean()) / (v.std() + 1e-6)
ims = {r: Image.open(os.path.join(OUT, c['t'])) for r, c in psd.items() if 't' in c}
sheet = Image.new('RGB', (7 * 330, 2 * 260), 'white'); d = ImageDraw.Draw(sheet); res = {}
for n, i in enumerate(NEED):
    L = Image.open(os.path.join(OUT, 'live', '%02d.jpg' % i)); ls = sig(L); best = []
    for rel, im in ims.items():
        ar = im.width / im.height; lar = L.width / L.height
        if ar > lar: nw = int(im.height * lar); x = (im.width - nw) // 2; cim = im.crop((x, 0, x + nw, im.height))
        else: nh = int(im.width / lar); y = (im.height - nh) // 2; cim = im.crop((0, y, im.width, y + nh))
        best.append((float(((sig(cim) - ls) ** 2).mean()), rel))
    best.sort(); s, rel = best[0]; res[i] = (round(s, 3), rel, psd[rel]['w'], psd[rel]['h'])
    x = (n % 7) * 330; y = (n // 7) * 260
    a1 = L.copy(); a1.thumbnail((150, 200)); sheet.paste(a1, (x + 5, y + 5)); b1 = ims[rel].copy(); b1.thumbnail((150, 200)); sheet.paste(b1, (x + 165, y + 5))
    d.text((x + 5, y + 210), '%02d  %.2f' % (i, s), fill='black'); d.text((x + 5, y + 225), rel[:50], fill='black'); d.text((x + 5, y + 240), '%dx%d' % (psd[rel]['w'], psd[rel]['h']), fill='black')
sheet.save(os.path.join(OUT, 'match_sheet_psd.jpg'), quality=80)
for i in NEED: print(i, res[i])
