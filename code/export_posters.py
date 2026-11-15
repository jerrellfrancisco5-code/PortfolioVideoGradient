# Visual Response: exports every poster at an exact 18x24 (3:4) crop from the best source available.
#   assets/vr/NN.jpg       1200x1600  (grid)
#   assets/vr/NN_full.jpg  up to 2400x3200 (lightbox)
# 'orig' = no export or PSD in the Posters folder; uses the largest copy Readymag holds (_vr/orig/NN.*).
import os, glob, json
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); VR = os.path.join(HERE, '_vr'); OUT = os.path.join(HERE, 'assets', 'vr'); os.makedirs(OUT, exist_ok=True)
SRC = r'C:\Users\Administrator\Desktop\01 Projects\_Studio_Francisco\_Personal_Campaigns\Posters'
storytellin = [f for f in glob.glob(os.path.join(SRC, 'Da Art of Storytellin part 2', '*Part 2].png'))][0]
S = {0: r'Why\WHY_purple.png', 1: r'Sophia\Sophia.png', 2: 'orig', 3: r'T.R.O.N\TRON Final_normal color.png', 4: r'Oysters In My Pocket\Oysters In My Pocket (1).png',
     5: storytellin, 6: 'orig', 7: r'_Unsorted PSDs\Poster_33.psd', 8: r'AHorseWithNoName\A Horse With No Name shots.png', 9: r'AHorseWithNoName\A Horse With No Name - Bike.png',
     10: r'Swim Good\Swim Good.png', 11: 'orig', 12: r'LilFrancisco\LilFrancisco.png', 13: r'DotsAndLines\DotsandLines.png', 14: 'orig', 15: r'_Unsorted PSDs\BoosterSeat (1).psd',
     16: r'NackNostalgia\NackNostalgia-Poster.png', 17: 'orig', 18: 'orig', 19: r'_Unsorted PSDs\poster.psd', 20: 'orig', 21: r'I-Am\IAm.png', 22: 'orig',
     23: r'ForOnceInMyLife\ForOnceInMyLife_FullPoster.png', 24: r'The Flower\If Im gone by tommorrow.png', 25: r'Tears\Tearsfinal.png', 26: 'orig', 27: 'orig'}
PAD = {26: 'black'}   # 27 (cat cover) is composed separately as a tilted sleeve on black, like the Goose House mockup; do not re-export it here
SKIP = {27}   # true squares: keep the whole piece, extend the ground to 3:4
info = {}
for i in range(28):
    if i in SKIP: continue
    s = S[i]
    p = glob.glob(os.path.join(VR, 'orig', '%02d.*' % i))[0] if s == 'orig' else (s if os.path.isabs(s) else os.path.join(SRC, s))
    im = Image.open(p).convert('RGB'); w, h = im.size
    if i in PAD:
        H = round(w * 4 / 3); top = (H - h) // 2; cv = Image.new('RGB', (w, H), (0, 0, 0))
        if PAD[i] == 'mirror':
            cv.paste(im.transpose(Image.FLIP_TOP_BOTTOM).crop((0, h - top, w, h)), (0, 0)); cv.paste(im.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, w, H - h - top)), (0, top + h))
        cv.paste(im, (0, top)); im = cv
    else:
        w, h = im.size
        if w / h > 0.75: nw = round(h * 0.75); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else: nh = round(w / 0.75); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    fw = min(2400, im.width); full = im.resize((fw, round(fw * 4 / 3)), Image.LANCZOS) if im.width != fw else im
    full.save(os.path.join(OUT, '%02d_full.jpg' % i), quality=86, optimize=True, progressive=True)
    grid = im.resize((1200, 1600), Image.LANCZOS)
    grid.save(os.path.join(OUT, '%02d.jpg' % i), quality=82, optimize=True, progressive=True)
    info[i] = {'src': 'readymag copy' if s == 'orig' else os.path.relpath(p, SRC), 'srcpx': [w, h], 'full': list(full.size)}
    print(i, info[i], flush=True)
json.dump(info, open(os.path.join(VR, 'export_info.json'), 'w'), indent=1)
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)); print('total MB', round(tot / 1e6, 1))
sheet = Image.new('RGB', (7 * 210, 4 * 280), 'white')
for i in range(28):
    t = Image.open(os.path.join(OUT, '%02d.jpg' % i)); t.thumbnail((200, 267)); sheet.paste(t, ((i % 7) * 210 + 5, (i // 7) * 280 + 5))
sheet.save(os.path.join(VR, 'export_sheet.jpg'), quality=80)
