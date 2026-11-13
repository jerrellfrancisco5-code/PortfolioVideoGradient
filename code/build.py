# Builds the two new case studies (Tori Richard & Kahala, Philosophy Cans) into a COPY of the live site code,
# plus a local preview. The live file (../1_PASTE_INTO_After_body_UPDATED.html) is only read.
#
#   python build.py                -> preview build (images from ./assets/, served by preview_server.py)
#   python build.py --live URL     -> live build, images from URL (the folder that CONTAINS ./assets/)
#
# Layout: every deliverable section is a "mosaic" on a 12-column unit grid (unit = column width, 12px gaps).
# Each tile is (kind, file, cols, rows[, object-position]); tiles are packed top-left first-fit, so rows always fill.
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(os.path.dirname(HERE), '1_PASTE_INTO_After_body_UPDATED.html')
MAN = json.load(open(os.path.join(HERE, 'assets', 'manifest.json'), encoding='utf-8'))
BASE = './assets/'
if '--live' in sys.argv:
    BASE = sys.argv[sys.argv.index('--live') + 1].rstrip('/') + '/assets/'

def dims(proj, name):
    m = MAN[proj][name]; return m.get('w', 0), m.get('h', 0)
def A(proj, name):
    w, h = dims(proj, name); return [BASE + proj + '/' + name, w, h]

def js(v, ind=0):
    pad = '  ' * ind
    if isinstance(v, dict):
        return '{\n' + ',\n'.join(pad + '  ' + (k if re.match(r'^[A-Za-z_]\w*$', k) else json.dumps(k)) + ': ' + js(x, ind + 1) for k, x in v.items()) + '\n' + pad + '}'
    if isinstance(v, list):
        inner = [js(x, ind + 1) for x in v]
        if all(not isinstance(x, (dict, list)) for x in v) and sum(len(s) for s in inner) < 200:
            return '[' + ', '.join(inner) + ']'
        return '[\n' + ',\n'.join(pad + '  ' + s for s in inner) + '\n' + pad + ']'
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    return json.dumps(v)

# ---------------------------------------------------------------- the mosaic packer
COLS = 12
def pack(tiles):
    """Adds col,row (1-based) to each tile by top-left first-fit on a 12-column grid; returns (tiles, total rows)."""
    height = [0] * COLS
    out = []
    for t in tiles:
        cw, rh = t['cw'], t['rh']
        best = None
        for c in range(0, COLS - cw + 1):
            top = max(height[c:c + cw])
            if best is None or top < best[0]: best = (top, c)
        top, c = best
        for i in range(c, c + cw): height[i] = top + rh
        t = dict(t); t['col'] = c + 1; t['row'] = top + 1; out.append(t)
    return out, max(height)

def M(kind, proj, name, cw, rh, pos=None, poster=None):
    w, h = dims(proj, name)
    t = {'kind': kind, 'src': BASE + proj + '/' + name, 'w': w, 'h': h, 'cw': cw, 'rh': rh}
    if pos: t['pos'] = pos
    if poster: t['poster'] = BASE + proj + '/' + poster
    return t

def mosaic(tiles):
    placed, rows = pack(tiles)
    return {'rows': rows, 'tiles': [[t['kind'], t['src'], t['w'], t['h'], t['col'], t['row'], t['cw'], t['rh'], t.get('pos', ''), t.get('poster', '')] for t in placed]}

# ------------------------------------------------------------------ Tori Richard & Kahala (Hale Tori)
T = lambda n: A('tori', n)
tm = lambda *a, **k: M('img', 'tori', *a, **k)
tori = {
  'focus': '50% 22%',
  'uri': 'tori-richard-kahala', 'name': 'Tori Richard & Kahala',
  'eyebrow': 'Hale Tori · 2026',
  'title': 'Two heritage aloha brands, one hand on the campaign calendar',
  'category': 'Email, paid social, product imagery & retail print',
  'cardTitle': 'Campaign Design for Two Heritage Brands', 'cardEyebrow': 'Hale Tori · Contract · 2026',
  'cover': T('ad_tilecabana_1_4x5.jpg'),
  'motion': BASE + 'tori/loop_bestselling.mp4',   # work-board cover loop (hover shows the still)
  'heroImg': T('hero_emails.jpg'),
  'accent': '#aa0001',
  'facts': { 'Role': 'Contract designer', 'Client': 'Hale Tori (Tori Richard and Kahala)', 'Year': '2026', 'Cadence': 'Something shipping nearly every week, September into October' },
  'tags': ['Email Design', 'Paid Social', 'Motion & Color Grade', 'Retouching & Compositing', 'Retail Print', 'Packaging'],
  'summary': [
    "Tori Richard and Kahala are two of Hawaiʻi's heritage apparel brands, and 2026 is Kahala's 90th year. From September into October I worked as a contract designer across both, taking each brief from the brand team's handoff through review rounds to the final files: fourteen email campaigns, paid ads and paid social, product-page imagery, and the print pieces a retail floor actually runs on.",
    "The job was consistency at speed. Every piece had to look like it came from the same hand as the one before it, and most of them had a week or less to get there."
  ],
  'brief': [
    ['The problem', "Two brands, one shared calendar, and something going out nearly every week: a 90th anniversary collection, new arrivals, bestseller roundups and paid placements on top."],
    ['My approach', "Learn each brand's build spec cold, then protect it: the house type, the measured spacing, the photography treated with respect. Variety comes from the content, not from reinventing the layout."],
    ['The result', "Fourteen emails, a full paid-ad set in three ratios, product imagery and store signage, all delivered inside eight weeks."]
  ],
  'sections': [
    { 'title': 'Email campaigns', 'sub': 'Fourteen sends in eight weeks',
      'body': [
        "Kahala's emails live on a warm ivory ground with the brand red reserved for the call to action. Klinic Slab for headings, Proxima Nova Condensed for body copy, product labels set small and bottom-right under every photo. Once that spec was measured and locked, each new send was a question of content and rhythm: a lifestyle hero, a headline and a line or two, a shoppable grid.",
        "The range inside that system was wide: new arrivals, the 90th anniversary collection, an artist-spotlight roundup, performance mailers, and an Anatomy of an Aloha Shirt piece that borrows the look of a tech pack, with numbered callouts on the shirt and a grid of detail boxes underneath."
      ],
      'mosaic': mosaic([tm('email_anatomy_fold.jpg', 4, 5, '50% 0%'), tm('email_vintage_fold.jpg', 4, 5, '50% 0%'), tm('email_90th_fold.jpg', 4, 5, '50% 0%'),
                        tm('email_performance_fold.jpg', 4, 5, '50% 0%'), tm('email_santas_fold.jpg', 4, 5, '50% 0%'), tm('email_artist_fold.jpg', 4, 5, '50% 0%')]) },
    { 'title': 'Animated heroes', 'sub': 'GIFs that still read as a still',
      'body': [
        "Two of the sends led with an animated hero: a bestseller roundup cycling six products with their colorway labels, and a vintage-boards drop that turns the shirt in place. Both were built frame by frame in Photoshop so the first frame works on its own for clients that don't animate, and the loop stays light enough for email."
      ],
      'mosaic': mosaic([tm('gif_bestselling.gif', 6, 8), tm('gif_vintage.gif', 6, 8)]) },
    { 'title': 'Paid ads & paid social', 'sub': 'One shoot, three ratios, color-matched',
      'body': [
        "For Tori Richard's Tile Cabana knitwear I built the paid set out of one photo shoot: two statics, a GIF and a video, each delivered in 1:1, 4:5 and 9:16. The video was stabilized and graded in After Effects with custom LUTs so the motion matched the photographer's stills instead of fighting them.",
        "For Kahala, the Apana jacquard paid-social set puts the fabric itself in the frame: the shirt's own pattern as the ground, a customer line in the center, the logo signed at the foot."
      ],
      'mosaic': mosaic([tm('ad_tilecabana_1_4x5.jpg', 4, 5), tm('ad_tilecabana_2_4x5.jpg', 4, 5), tm('social_apana_4x5.jpg', 4, 5),
                        tm('ad_tilecabana_1_9x16.jpg', 4, 7), tm('ad_tilecabana_2_9x16.jpg', 4, 7), tm('social_apana_9x16.jpg', 4, 7)]) },
    { 'title': 'Retail print', 'sub': 'Signs, hangtags and labels for the store floor',
      'body': [
        "The Be Right Back sign is one reusable system with two brand versions: a permanent printed face, a steel rail, and magnetic digits staff can change by hand. Fourteen rounds of review covered the part no one sees on a mood board, like the fact that magnets don't stick to aluminum, and how many of each digit a store needs to show any time of day.",
        "Alongside it: a Kahala × Fender guitar hangtag on a Duke's Pareo repeat, retail store cards for both brands, and a commercialization label for the Kahala × L&L Hawaiian Barbecue collaboration."
      ],
      'mosaic': mosaic([tm('sign_door_storefront.jpg', 8, 6), tm('sign_door_closeup.jpg', 4, 6), tm('tag_fender.jpg', 12, 9)]) },
    { 'title': 'Product imagery', 'sub': 'PDP comps and retouching',
      'body': [
        "Product pages needed images before samples existed. The Kahala coach jacket in navy, gold and paprika was comped front and back with its label, pocket and stripe details, clean enough to sell from. The same retouching pass covered Tori Richard's wallet line and the seasonal lifestyle crops."
      ],
      'mosaic': mosaic([tm('pdp_jacket_front.jpg', 3, 4), tm('pdp_jacket_back.jpg', 3, 4), tm('pdp_jacket_label.jpg', 3, 4), tm('pdp_jacket_stripe.jpg', 3, 4)]) }
  ],
  'outcome': { 'title': 'Two brands that still look like themselves.',
    'body': [
      "Every send, ad, sign and product page went out on the same spec as the one before it, through weekly review rounds with the brand team and into production. The measured build settings I documented along the way became the reference for the next piece, which is how fourteen emails in eight weeks stayed one voice.",
      "It's the kind of work a brand feels rather than notices: the inbox looks consistent, the paid ads match the catalog, the sign on the door matches the shirt in the window."
    ],
    'quote': "Fourteen emails, three ad formats, two brands, eight weeks. Every piece built to the same spec.",
    'mediaNote': 'Two full sends, top to bottom',
    'media': [T('email_anatomy.jpg'), T('email_performance.jpg')] },
  'cta': "Have a calendar like this one? Let's talk."
}

# ------------------------------------------------------------------ Philosophy Cans (Studio Francisco)
C = lambda n: A('cans', n)
cm = lambda *a, **k: M('img', 'cans', *a, **k)
lp = lambda *a, **k: M('loop', 'cans', *a, **k)
vd = lambda *a, **k: M('video', 'cans', *a, **k)
cans = {
  'focus': '50% 50%',
  'uri': 'philosophy-cans', 'name': 'Philosophy Cans',
  'eyebrow': 'Studio Francisco · Independent · 2026',
  'title': 'Crack open a worldview',
  'category': 'Packaging, characters, 3D & motion for a concept drink brand',
  'cardTitle': 'Packaging, 3D & Motion', 'cardEyebrow': 'Independent · 2026',
  'cover': C('lineup_dark.jpg'),
  'motion': BASE + 'cans/loops/loop_gravityfall.mp4',   # work-board cover loop (hover shows the still)
  'heroImg': C('banner.jpg'),
  'accent': '#15120f',
  'facts': { 'Role': 'Creator, self-directed', 'Type': 'Concept sparkling drink, four flavors', 'Year': '2026', 'Built in': 'Illustrator, Photoshop, Blender' },
  'tags': ['Brand Identity', 'Packaging', 'Character Design', 'Copywriting', '3D & Motion', 'Campaign'],
  'summary': [
    "Philosophy Cans is a sparkling drink with four flavors and four worldviews: Hermetic, Absurdist, Stoic and Nihilist. Each can gets its own hand-drawn character, its own color and its own voice, from the affirmation on the front to the mood facts on the back. The joke is that every can answers the same question differently.",
    "It started as pen on paper. The faces are my own ink, drawn as twelve expressions per character, then vectored, set on the label and rendered on a real can in Blender. From there the cans went out into the world: posters, a billboard, a four-pack and a launch reel."
  ],
  'brief': [
    ['The question', "What does a drink brand look like when the flavor is a philosophy?"],
    ['My approach', "One rule: my own ink on every can. Hand-drawn faces, a label that melts from color into bare aluminum, and copy that flatters the drinker and saves the cruelty for the universe."],
    ['The result', "Four cans, thirteen rounds of refinement, and a campaign system I'd pitch to a real brand tomorrow."]
  ],
  'sections': [
    { 'title': 'The characters', 'sub': 'Four faces, my own ink',
      'body': [
        "Herm, Albert, Marcus and Fred. Hermes Trismegistus, Camus, Marcus Aurelius and Nietzsche, if you want the long version. Each one started as a page of marker sketches and a short video of me pulling faces, then got a set of twelve expressions: the Hermetic is smug and ascending, the Absurdist is manic and in love with the void, the Stoic has exactly one face no matter what happens, and the Nihilist has a personal raincloud.",
        "The twelve expressions are the wrap. Point to how you feel and the can answers."
      ],
      'mosaic': mosaic([cm('sk_final_hermetic.jpg', 3, 3), cm('sk_final_absurdist.jpg', 3, 3), cm('sk_final_stoic.jpg', 3, 3), cm('sk_final_nihilist.jpg', 3, 3),
                        cm('face_hermetic.png', 3, 3), cm('face_absurdist.png', 3, 3), cm('face_stoic.png', 3, 3), cm('face_nihilist.png', 3, 3)]) },
    { 'title': 'The label', 'sub': 'Color that melts into metal',
      'body': [
        "The print runs from just above the chime to the top of the neck. The color sits solid at the top of the can, falls down the label and dissolves softly into bare aluminum at the base, so the metal is part of the design instead of something the label hides. A white medallion carries the face, the wordmark is set in my own lettering, and a band line runs round the shoulder: ZERO DOUBT, ZERO MEANING, ZERO COMPLAINTS, ZERO POINT.",
        "The back is where the writing lives: a mood-facts table in place of nutrition facts, an ingredients list, a warning, a disclaimer and a signature. The pull tab reads PULL TAB TO CONTINUE EXISTING. The bottom of the can says STILL HERE? NICE."
      ],
      'mosaic': mosaic([cm('label_hermetic.jpg', 6, 5), cm('label_absurdist.jpg', 6, 5), cm('label_stoic.jpg', 6, 5), cm('label_nihilist.jpg', 6, 5)]) },
    { 'title': 'The cans', 'sub': 'Rendered, not mocked up',
      'body': [
        "Every can is a real object in Blender, rendered in Cycles under a studio rig built for the job: the label is the can's own aluminum where the color fades out, so reflections, roughness and the melt all behave like metal. Light studio and dark studio, hero stills, close-ups, turntables, and animated faces that play on the can.",
        "Then the motion set, all rendered in the same studio: a turntable for each can, a light sweep across the lineup, a gravity fall, a domino run, a lid stamp, a studio fan and a wave. Every one of them loops, so they drop straight into a product page, a story or a reel.",
        "And the still-life set: a pile, a field of lids, diagonal rows, a cluster, a can on a stack of books. The kind of photography a drink brand would commission, built instead."
      ],
      'mosaic': mosaic([
        cm('lineup_dark.jpg', 12, 7),
        lp('loops/loop_hermetic_turntable.mp4', 3, 4), lp('loops/loop_absurdist_turntable.mp4', 3, 4), lp('loops/loop_stoic_turntable.mp4', 3, 4), lp('loops/loop_nihilist_turntable.mp4', 3, 4),
        cm('hero_absurdist.jpg', 4, 5), cm('hero_stoic.jpg', 4, 5), cm('hero_hermetic.jpg', 4, 5),
        cm('still_diagonal.jpg', 12, 7),
        lp('loops/loop_gravityfall.mp4', 12, 7),
        cm('hero_nihilist.jpg', 3, 4), lp('loops/loop_wave.mp4', 6, 8), cm('still_interior.jpg', 3, 4), cm('still_lids.jpg', 3, 4), cm('still_cluster.jpg', 3, 4),
        lp('loops/loop_lightsweep.mp4', 8, 4), lp('loops/loop_centrerotation.mp4', 4, 4),
        lp('loops/loop_domino.mp4', 8, 4), lp('loops/loop_studiofan.mp4', 4, 4),
        lp('loops/loop_lidstamp.mp4', 6, 6), cm('still_pile.jpg', 6, 3), cm('still_floating.jpg', 6, 3),
        cm('still_ledge.jpg', 6, 4), cm('still_whitefield.jpg', 6, 4)
      ]) },
    { 'title': 'Out in the world', 'sub': 'Posters, out-of-home and a four-pack',
      'body': [
        "The campaign takes one line per can and gives it room. Each poster is the affirmation in the world's color with the can standing in it: YOU ARE THE UNIVERSE, BUT HYDRATED. ONE MUST IMAGINE YOU THIRSTY. YOU'RE ALREADY ENOUGH. NOTHING MATTERS. YOU STILL LOOK GREAT.",
        "The same system runs out to a floodlit billboard at dusk, an advertising column wrapped with the four posters and a dark ring-carrier four-pack. Every cut-out on every piece is the render's own pixels, so the lighting never lies."
      ],
      'mosaic': mosaic([cm('poster_hermetic.jpg', 3, 5), cm('poster_absurdist.jpg', 3, 5), cm('poster_stoic.jpg', 3, 5), cm('poster_nihilist.jpg', 3, 5),
                        cm('column.jpg', 6, 8), cm('fourpack.jpg', 6, 8), cm('billboard.jpg', 12, 7)]) },
    { 'title': 'Social & launch', 'sub': 'The reels, the posts and the stories',
      'body': [
        "Two launch reels, cut to the beat: a 16:9 for LinkedIn, built to work silent because the feed autoplays muted, and a 9:16 for Instagram. Both run the whole story in under a minute: the sketchbook pages, the faces going from marker to vector on the drop, the four worlds a bar each, the cans landing on the beat, and the campaign at the end.",
        "Around them, the feed: a master post, the four worlds under \"Pick your existential crisis\", an affirmation post per can with the headline behind the cut-out, per-sip tables in place of nutrition facts, and a story per world. The LinkedIn post leads with the hook: I designed a drink that asks how you feel."
      ],
      'mosaic': mosaic([
        vd('reels/reel_16x9.mp4', 12, 7, poster='reels/reel_16x9_poster.jpg'),
        vd('reels/reel_9x16.mp4', 4, 7, poster='reels/reel_9x16_poster.jpg'), cm('story_hermetic.jpg', 4, 7), cm('story_nihilist.jpg', 4, 7),
        cm('ig_master.jpg', 4, 5), cm('ig_fourworlds.jpg', 4, 5), cm('ig_absurdist_aff.jpg', 4, 5),
        cm('ig_hermetic_aff.jpg', 4, 5), cm('ig_stoic_persip.jpg', 4, 5), cm('ig_nihilist_persip.jpg', 4, 5)
      ]) },
    { 'title': 'The brand book', 'sub': 'Every rule the cans follow, in one place',
      'body': [
        "Sixteen pages, dark first like the studio: the idea, the four worlds as full-bleed colour bands, the colour system with the measured melt curve, the type, the five layers of the front panel in reading order, the wrap and its zones, the faces and the rule that they are never redrawn, the four motion curves, the attention architecture, the lighting rig, the voice, and the applications.",
        "It's the document I'd hand a second designer so the next can still looks like the first four."
      ],
      'button': ['Open the brand book', BASE + 'cans/PhilosophyCans_BrandBook.pdf'],
      'mosaic': mosaic([cm('bookpages/book_cover.jpg', 12, 10, '50% 0%')]) }
  ],
  'outcome': { 'title': 'A whole world from one can.',
    'body': [
      "Philosophy Cans became a complete system: four characters, four labels, a 3D product set, a still-life and motion library, posters, out-of-home, social and a brand book, all built from one idea and one rule about whose ink goes on the can.",
      "Like Lévain, it's self-directed, which means every decision in it is mine to defend. That's the point of the personal work: it's the clearest look at how I think when nobody is briefing me."
    ],
    'quote': "Nobody asked for a philosophy drink. That's kind of the point." },
  'cta': "Have a brand that needs a world built around it? Let's talk."
}

# ------------------------------------------------------------------ patch a copy of the live code
src = open(LIVE, encoding='utf-8').read()
out = src

def must(old, new, count=1):
    global out
    assert out.count(old) == count, ('pattern not found exactly %d time(s): ' % count) + old[:80]
    out = out.replace(old, new)

# 1. absolute / relative image URLs pass straight through src() and img()
must("function src(f, w) { return /\\.gif$/i.test(f) ? GIF + f : IMG + f + (w ? '?w=' + w : ''); }",
     "function isUrl(f) { return /^(https?:)?\\/\\//.test(f) || /^\\.?\\//.test(f); }\n  function src(f, w) { if (isUrl(f)) return f; return /\\.gif$/i.test(f) ? GIF + f : IMG + f + (w ? '?w=' + w : ''); }")
must("    if (/\\.gif$/i.test(f)) return '<img src=\"' + src(f) + '\"' + a + '>';",
     "    if (/\\.gif$/i.test(f) || isUrl(f)) return '<img src=\"' + src(f) + '\"' + a + '>';")

# 2. a project can carry its own Vimeo reel (p.vimeo) and its own contact line (p.cta)
must("    if (k === 'itw' && p.youtube) out +=",
     "    if (p.vimeo) out += '<section class=\"deliv\"><div class=\"metarow rv\"><span class=\"eyebrow\">The reel</span><span class=\"rule\"></span></div><div class=\"stack rv\"><div class=\"player\"><iframe src=\"https://player.vimeo.com/video/' + p.vimeo + '?dnt=1&title=0&byline=0&portrait=0\" title=\"' + esc(p.name) + ' reel\" allow=\"autoplay; fullscreen; picture-in-picture\" allowfullscreen></iframe></div></div></section>';\n    if (k === 'itw' && p.youtube) out +=")
must("    out += contactBlock(\"Like what you see? Let's talk.\", true) + footer()",
     "    out += contactBlock(p.cta || \"Like what you see? Let's talk.\", true) + footer()")

# 3. the mosaic: a 12-column unit grid; tiles = [kind, src, w, h, col, row, cols, rows, pos, poster]
MOSAIC_JS = r"""    function mosaicTile(t) {
      var kind = t[0], f = t[1], w = t[2], h = t[3], st = 'grid-column:' + t[4] + ' / span ' + t[6] + ';grid-row:' + t[5] + ' / span ' + t[7] + ';--cw:' + t[6] + ';--rh:' + t[7] + (t[8] ? ';--pos:' + t[8] : '');
      if (kind === 'loop') return '<div class="fig vid" style="' + st + '"><video autoplay muted loop playsinline preload="metadata" src="' + f + '" width="' + w + '" height="' + h + '" aria-label="' + esc(alt) + ' - loop"></video></div>';
      if (kind === 'video') return '<div class="fig vid play" style="' + st + '"><video controls playsinline preload="metadata" src="' + f + '" poster="' + (t[9] || '') + '" width="' + w + '" height="' + h + '" aria-label="' + esc(alt) + ' - reel"></video></div>';
      return '<figure class="fig" style="' + st + '" data-lb="' + esc(f) + '"><img src="' + f + '" alt="' + esc(alt) + '" width="' + w + '" height="' + h + '" loading="lazy" decoding="async"' + (t[8] ? ' style="object-position:' + t[8] + '"' : '') + '></figure>';
    }
    if (s.mosaic) m += '<div class="mg" style="--rows:' + s.mosaic.rows + '">' + s.mosaic.tiles.map(mosaicTile).join('') + '</div>';
"""
must("    if (s.gif) m += fig(s.gif, alt);", MOSAIC_JS + "    if (s.gif) m += fig(s.gif, alt);")
# a section button (pill) under the copy, e.g. the brand book PDF
must("    return '<section class=\"deliv\"><div class=\"metarow rv\"><span class=\"eyebrow\"><b>' + n + '</b>",
     "    if (s.button) link += '<p style=\"margin-top:22px\"><a class=\"pill\" href=\"' + s.button[1] + '\" target=\"_blank\" rel=\"noopener\">' + esc(s.button[0]) + ' <span class=\"arr\">\\u2197</span></a></p>';\n    return '<section class=\"deliv\"><div class=\"metarow rv\"><span class=\"eyebrow\"><b>' + n + '</b>")
if False: must("", "    if (s.button) link += '<p style=\"margin-top:22px\"><a class=\"pill\" href=\"' + s.button[1] + '\" target=\"_blank\" rel=\"noopener\">' + esc(s.button[0]) + ' <span class=\"arr\">↗</span></a></p>';")

MOSAIC_CSS = """
/* mosaic: a 12-column unit grid; every tile snaps to the same columns and rows, cropped tiles open full size in the lightbox */
#jf .mg { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); grid-auto-rows: var(--u, 80px); gap: 12px; }
#jf .mg .fig { margin: 0; min-height: 0; min-width: 0; }
#jf .mg .fig img, #jf .mg .fig video { width: 100%; height: 100%; object-fit: cover; object-position: var(--pos, 50% 50%); display: block; }
#jf .fig.vid { cursor: default; background: #15120f; }
#jf .fig.vid.play { cursor: pointer; }
@media (max-width: 760px) {
  #jf .mg { grid-template-columns: 1fr 1fr; grid-auto-rows: auto; }
  #jf .mg .fig { grid-column: auto / span 1 !important; grid-row: auto !important; aspect-ratio: 1 / 1; }
  #jf .mg .fig.w2 { grid-column: 1 / -1 !important; aspect-ratio: var(--mar, 3 / 2); }
}
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + MOSAIC_CSS)

# unit size from the real column width, loops play only on screen
must("  if (!root.parentNode) document.body.appendChild(root);",
     """  if (!root.parentNode) document.body.appendChild(root);
  function sizeMosaics() { root.querySelectorAll('.mg').forEach(function (g) {
    var u = (g.clientWidth - 11 * 12) / 12; if (u > 0) g.style.setProperty('--u', u.toFixed(2) + 'px');
    /* phone: two columns; wide tiles take both, and a small tile that would sit alone on its row takes both too */
    var kids = Array.prototype.slice.call(g.children), narrow = window.innerWidth <= 760, col = 0;
    kids.forEach(function (k, i) {
      var cw = +k.style.getPropertyValue('--cw'), rh = +k.style.getPropertyValue('--rh'), big = cw >= 6, next = kids[i + 1];
      var wide = narrow && (big || (col === 0 && (!next || +next.style.getPropertyValue('--cw') >= 6)));
      k.classList.toggle('w2', wide);
      if (wide) k.style.setProperty('--mar', big ? (cw / rh).toFixed(3) : '1.5');
      col = wide ? 0 : (col + 1) % 2;
    });
  }); }
  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);
  if ('IntersectionObserver' in window) { var vio = new IntersectionObserver(function (es) { es.forEach(function (e) { var v = e.target; if (e.isIntersecting) { v.play && v.play().catch(function () {}); } else { v.pause && v.pause(); } }); }, { rootMargin: '200px 0px' }); root.querySelectorAll('.fig.vid:not(.play) video').forEach(function (v) { vio.observe(v); }); }""")

# 4. project links go straight to the trailing-slash URL Readymag serves (no 301 hop, nothing for a browser to cache wrong)
must("    return '/' + P[r].uri;\n", "    return '/' + P[r].uri + '/';\n")

# 5. the two projects, in the board order after their nearest neighbours
must("  order: ['snow', 'itw', 'abbott', 'got', 'hotd', 'gilmore', 'lotr', 'levain', 'vr', 'legendary'],",
     "  order: ['snow', 'itw', 'tori', 'abbott', 'got', 'hotd', 'gilmore', 'lotr', 'levain', 'cans', 'vr', 'legendary'],")
must("    vr: {\n      focus: '50% 55%',",
     "    tori: " + js(tori, 2) + ",\n\n    cans: " + js(cans, 2) + ",\n\n    vr: {\n      focus: '50% 55%',")

# 7. home statement: gold on "transforming" + "visual experiences", words roll up on scroll, metallic shimmer on the gold
must("    statement: ['Work focused on ', 'transforming ideas', ' into memorable visual experiences'],",
     "    statement: ['Work focused on ', 'transforming', ' ideas into memorable ', 'visual experiences'],   /* plain, gold, plain, gold */")
must("'<section class=\"statement on-dark rv\" aria-label=\"Statement\"><p class=\"big\">' + esc(h.statement[0]) + '<em>' + esc(h.statement[1]) + '</em>' + esc(h.statement[2]) + '</p>' +",
     "'<section class=\"statement on-dark rv\" aria-label=\"Statement\"><p class=\"big roll\" aria-label=\"' + esc(h.statement.join('')) + '\">' + (function () { var i = 0; return h.statement.map(function (seg, k) { var words = seg.trim().split(/\\s+/).filter(Boolean).map(function (wd) { return '<span class=\"w\"><span class=\"wi\" style=\"--d:' + (i++ * 70) + 'ms\">' + esc(wd) + '</span></span>'; }).join(' '); return k % 2 ? '<em>' + words + '</em>' : words; }).join(' '); })() + '</p>' +")
STATEMENT_CSS = """
/* home statement: words roll up when the block scrolls into view; the gold words carry a slow metallic shimmer */
#jf .statement .big.roll { text-wrap: balance; }
#jf .statement .big .w { display: inline-block; overflow: hidden; vertical-align: bottom; padding: 0.06em 0.02em 0.08em; margin: -0.06em -0.02em -0.08em; }
#jf .statement .big .wi { display: inline-block; transform: translateY(115%); transition: transform 0.95s cubic-bezier(0.2, 0.7, 0.2, 1); transition-delay: var(--d, 0ms); will-change: transform; }
#jf .statement.in .big .wi { transform: none; }
#jf .statement .big em { font-style: normal; color: var(--gold); }
@supports ((-webkit-background-clip: text) or (background-clip: text)) {
  #jf .statement .big em .wi { color: transparent; background: linear-gradient(100deg, #8a6a2c 0%, #c9a24b 30%, #f6e7b4 50%, #c9a24b 70%, #8a6a2c 100%); background-size: 260% 100%; -webkit-background-clip: text; background-clip: text; animation: jfshimmer 5.2s linear infinite; animation-delay: var(--d, 0ms); }
}
@keyframes jfshimmer { 0% { background-position: 120% 0; } 100% { background-position: -140% 0; } }
@media (prefers-reduced-motion: reduce) { #jf .statement .big .wi { transform: none; transition: none; animation: none; } }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + STATEMENT_CSS)

# 6. the work page intro mentions the new work
must("Entertainment e-commerce for Warner Bros. and Legendary, festival identities, and an ongoing poster practice.",
     "Entertainment e-commerce for Warner Bros. and Legendary, campaign work for two heritage aloha brands, festival identities, a concept drink brand and an ongoing poster practice.")

# 8. work board: a muted loop plays in every tile that has one (p.motion = mp4 URL or 'hls:<readymag id>'); hovering reveals the static cover underneath
must("    var p = P[k];\n    return '<a class=\"tile rv\" href=\"' + href(k) + '\"><div class=\"cover\">'",
     "    var p = P[k];\n    var cv = p.motion ? '<video class=\"cv\" muted loop playsinline preload=\"none\" data-cv=\"' + p.motion + '\" aria-hidden=\"true\"' + (p.focus ? ' style=\"object-position:' + p.focus + '\"' : '') + '></video>' : '';\n    return '<a class=\"tile rv\" href=\"' + href(k) + '\"><div class=\"cover\">' + cv")
COVER_CSS = """
/* work board: the cover loop plays while the tile is on screen; hover shows the still */
#jf .tile .cover { position: relative; }
#jf .tile .cover video.cv { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity .5s ease; pointer-events: none; z-index: 1; }
#jf .tile.cv-on .cover video.cv { opacity: 1; }
#jf .tile.cv-on:hover .cover video.cv { opacity: 0; }
@media (prefers-reduced-motion: reduce) { #jf .tile .cover video.cv { display: none; } }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + COVER_CSS)
must("  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);\n",
     """  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) root.querySelectorAll('.tile video.cv').forEach(function (v) {
    var id = v.getAttribute('data-cv'), tile = v.parentNode.parentNode;
    v.addEventListener('playing', function () { tile.classList.add('cv-on'); });
    function start() { if (id.indexOf('hls:') === 0) attach(v, id.slice(4), true); else { if (!v.getAttribute('src')) v.src = id; v.play().catch(function () {}); } }
    if ('IntersectionObserver' in window) { var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) start(); else v.pause(); }, { rootMargin: '200px 0px' }); o.observe(v); } else start();
  });
""")
# which loop each existing project uses: the home-carousel preview where one exists, otherwise the case study's own video
must("      preview: '68a676f89cc37dc9e68ba9e9/CJLYRAPi9ToF1zFHWNehi',", "      preview: '68a676f89cc37dc9e68ba9e9/CJLYRAPi9ToF1zFHWNehi', motion: 'hls:68a676f89cc37dc9e68ba9e9/CJLYRAPi9ToF1zFHWNehi',")
must("      preview: '69ae0d496bac13926469e736/0dQnfK8KSDPNWgRWEedDS',", "      preview: '69ae0d496bac13926469e736/0dQnfK8KSDPNWgRWEedDS', motion: 'hls:69ae0d496bac13926469e736/0dQnfK8KSDPNWgRWEedDS',")
must("      preview: '68a78fb32bbc7c33c46c39a6/_djUVxZcNqDVDaigdVFSL',", "      preview: '68a78fb32bbc7c33c46c39a6/_djUVxZcNqDVDaigdVFSL', motion: 'hls:68a78fb32bbc7c33c46c39a6/_djUVxZcNqDVDaigdVFSL',")
must("      cover: ['image-f85dda7a-baac-492b-a62f-f39d3c695d8c.png', 1047, 440],", "      cover: ['image-f85dda7a-baac-492b-a62f-f39d3c695d8c.png', 1047, 440], motion: 'hls:689d315c988d1ed8411839c9/fS4P_Iat4oReYc0pB48ge',")
must("      cover: ['image-f6946e62-929a-4c75-819b-3ba9ad360937.webp', 1029, 440],", "      cover: ['image-f6946e62-929a-4c75-819b-3ba9ad360937.webp', 1029, 440], motion: 'hls:689d2ed71778e5504c438a3e/DM0PXW4ZfP519qP_KWSem',")
must("      cover: ['image-c946189a-5562-4c63-82cd-d3b3d8b2d0f6.png', 1028, 432],", "      cover: ['image-c946189a-5562-4c63-82cd-d3b3d8b2d0f6.png', 1028, 432], motion: 'hls:689d333fb37ad9e95413a20e/qtOyJ7cALekn6uIZH5hvO',")

name = '1_PASTE_INTO_After_body_WITH_NEW_CASE_STUDIES.html' if '--live' in sys.argv else '_preview_code.html'
open(os.path.join(HERE, name), 'w', encoding='utf-8').write(out)
print('wrote', name, len(out), 'chars (+%d)' % (len(out) - len(src)))

if '--live' not in sys.argv:
    fonts = ''
    fp = os.path.join(HERE, '_fonts.css')
    if os.path.exists(fp): fonts = '<style>' + open(fp, encoding='utf-8').read() + '</style>'
    shell = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Francisco - preview</title>' + fonts + '</head><body>' + out + '<script>/* preview only: load every image up front so review renders are complete */(function(){var n=0,t=setInterval(function(){document.querySelectorAll("#jf img[loading=lazy]").forEach(function(i){i.loading="eager";});if(++n>40)clearInterval(t);},250);})();</script></body></html>'
    open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(shell)
    print('wrote index.html (preview shell)')
