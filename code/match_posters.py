# Matches the 28 posters shown on the live Visual Response page to their source files in the Posters folder.
import os, io, json, re, urllib.request
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\Users\Administrator\Desktop\01 Projects\_Studio_Francisco\_Personal_Campaigns\Posters'
OUT = os.path.join(HERE, '_vr'); os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(OUT, 'live'), exist_ok=True)
IMG = 'https://i-p.rmcdn.net/6797f7b58f4ab44487126bec/5583592/'
code = io.open(os.path.join(HERE, '..', '1_PASTE_INTO_After_body_UPDATED.html'), encoding='utf-8-sig').read()
a = code.index('posters: [['); b = code.index(']]', a)
live = re.findall(r"\['([^']+)', (\d+), (\d+)\]", code[a:b + 2])
print('live posters', len(live))
def sig(im, size=(24, 32)):
    g = im.convert('L').resize(size, Image.LANCZOS); v = np.asarray(g, dtype=np.float32); v = (v - v.mean()) / (v.std() + 1e-6); return v
lives = []
for i, (n, w, h) in enumerate(live):
    p = os.path.join(OUT, 'live', '%02d.jpg' % i)
    if not os.path.exists(p):
        req = urllib.request.Request(IMG + n + '?w=600', headers={'User-Agent': 'Mozilla/5.0'})
        Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert('RGB').save(p, quality=90)
    lives.append(Image.open(p))
cache = os.path.join(OUT, 'cands.json'); cands = json.load(open(cache)) if os.path.exists(cache) else {}
for root, _, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith(('.png', '.jpg', '.jpeg')): continue
        p = os.path.join(root, f); rel = os.path.relpath(p, SRC)
        if rel in cands: continue
        try:
            im = Image.open(p); w, h = im.size; im.draft('RGB', (400, 400)); im = im.convert('RGB'); im.thumbnail((400, 400))
            im.save(os.path.join(OUT, 'c_%d.jpg' % len(cands)), quality=80)
            cands[rel] = {'w': w, 'h': h, 't': 'c_%d.jpg' % len(cands)}
        except Exception as e: print('skip', rel, e)
json.dump(cands, open(cache, 'w'))
print('candidates', len(cands))
csig = {}
for rel, c in cands.items():
    im = Image.open(os.path.join(OUT, c['t'])); csig[rel] = im
res = []
sheet = Image.new('RGB', (7 * 330, 4 * 260), 'white'); d = ImageDraw.Draw(sheet)
for i, L in enumerate(lives):
    ls = sig(L); best = []
    for rel, im in csig.items():
        ar = im.width / im.height; lar = L.width / L.height
        # compare the candidate centre-cropped to the live aspect
        if ar > lar: nw = int(im.height * lar); x = (im.width - nw) // 2; cim = im.crop((x, 0, x + nw, im.height))
        else: nh = int(im.width / lar); y = (im.height - nh) // 2; cim = im.crop((0, y, im.width, y + nh))
        s = float(((sig(cim) - ls) ** 2).mean()); best.append((s, rel))
    best.sort(); top = best[:3]; res.append({'i': i, 'live': live[i][0], 'top': [(round(s, 3), r, cands[r]['w'], cands[r]['h']) for s, r in top]})
    x = (i % 7) * 330; y = (i // 7) * 260
    a1 = L.copy(); a1.thumbnail((150, 200)); sheet.paste(a1, (x + 5, y + 5))
    b1 = csig[top[0][1]].copy(); b1.thumbnail((150, 200)); sheet.paste(b1, (x + 165, y + 5))
    d.text((x + 5, y + 210), '%02d  %.2f' % (i, top[0][0]), fill='black'); d.text((x + 5, y + 225), top[0][1][:50], fill='black'); d.text((x + 5, y + 240), '%dx%d' % (cands[top[0][1]]['w'], cands[top[0][1]]['h']), fill='black')
sheet.save(os.path.join(OUT, 'match_sheet.jpg'), quality=80)
json.dump(res, open(os.path.join(OUT, 'matches.json'), 'w'), indent=1)
for r in res: print(r['i'], r['top'][0], '| 2nd', r['top'][1][0], r['top'][1][1])
