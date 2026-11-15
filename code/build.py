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
                        cm('face_hermetic.png', 3, 3), cm('face_absurdist.png', 3, 3), cm('face_stoic.png', 3, 3), cm('face_nihilist.png', 3, 3),
                        # sketch -> vector -> motion: the six-second expression loops, same order, same row rhythm
                        lp('motion/anim_hermetic.mp4', 3, 3), lp('motion/anim_absurdist.mp4', 3, 3), lp('motion/anim_stoic.mp4', 3, 3), lp('motion/anim_nihilist.mp4', 3, 3)]) },
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
#jf .fig.vid { cursor: default; background: transparent; }
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
     "  order: ['snow', 'tori', 'levain', 'cans', 'vr', 'itw', 'legendary', 'got', 'hotd', 'abbott', 'gilmore', 'lotr'],")
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
# which loop each existing project uses: ten-second muted MP4 clips cut from the Readymag videos (assets/covers/), so no tile needs an HLS player
# (Chrome caps simultaneous HLS/MediaSource players, which is why an all-HLS board dropped one tile)
CV = lambda k: BASE + 'covers/' + k + '.mp4'
must("      preview: '68a676f89cc37dc9e68ba9e9/CJLYRAPi9ToF1zFHWNehi',", "      preview: '68a676f89cc37dc9e68ba9e9/CJLYRAPi9ToF1zFHWNehi', motion: '" + CV('snow') + "',")
must("      preview: '69ae0d496bac13926469e736/0dQnfK8KSDPNWgRWEedDS',", "      preview: '69ae0d496bac13926469e736/0dQnfK8KSDPNWgRWEedDS', motion: '" + CV('levain') + "',")
must("      preview: '68a78fb32bbc7c33c46c39a6/_djUVxZcNqDVDaigdVFSL',", "      preview: '68a78fb32bbc7c33c46c39a6/_djUVxZcNqDVDaigdVFSL', motion: '" + CV('vr') + "',")
must("      cover: ['image-f85dda7a-baac-492b-a62f-f39d3c695d8c.png', 1047, 440],", "      cover: ['image-f85dda7a-baac-492b-a62f-f39d3c695d8c.png', 1047, 440], motion: '" + CV('got') + "',")
must("      cover: ['image-f6946e62-929a-4c75-819b-3ba9ad360937.webp', 1029, 440],", "      cover: ['image-f6946e62-929a-4c75-819b-3ba9ad360937.webp', 1029, 440], motion: '" + CV('hotd') + "',")
must("      cover: ['image-c946189a-5562-4c63-82cd-d3b3d8b2d0f6.png', 1028, 432],", "      cover: ['image-c946189a-5562-4c63-82cd-d3b3d8b2d0f6.png', 1028, 432], motion: '" + CV('gilmore') + "',")

# 9. work board as cards (v5): one ink frame shared by the statement block and the board (no texture on the frame);
#    cards are pristine white satin: a single-direction hatch under a soft sheen lit from one side. The thread colour survives only
#    as the hue of the hover shadow and a faint bloom. Button: frosted glass; on hover the arrow square swells into a reflective
#    gold fill while sliding right, and the label inverts to ink.
THREAD = {  # the flag palette: reds, greens, browns. Adjacent cards never share a thread.
  'snow': '#6b4423', 'itw': '#2f5d3a', 'tori': '#8c1d18', 'abbott': '#556b2f', 'got': '#1f4a2e', 'hotd': '#5b1f2b',
  'gilmore': '#6b4423', 'lotr': '#4a3222', 'levain': '#2f5d3a', 'cans': '#8c1d18', 'vr': '#5b1f2b', 'legendary': '#6b4423',
}
must("  function tile(k, sizes) {\n    var p = P[k];",
     "  var THREAD = " + json.dumps(THREAD) + ";\n  function tile(k, sizes) {\n    var p = P[k];")
must("    return '<a class=\"tile rv\" href=\"' + href(k) + '\"><div class=\"cover\">' + cv",
     "    return '<a class=\"tile rv\" href=\"' + href(k) + '\" style=\"--acc:' + (THREAD[k] || '#6b4423') + '\"><div class=\"cover\">' + cv")
must("      '<div class=\"meta\"><div><span class=\"eyebrow\">' + esc(p.cardEyebrow) + '</span><h3>' + esc(p.name === p.cardTitle ? p.name : p.name + ': ' + p.cardTitle) + '</h3></div><span class=\"round\" aria-hidden=\"true\">' + ARROW + '</span></div></a>';",
     "      '<div class=\"meta\"><div class=\"txt\"><h3>' + esc(p.name) + '</h3><p>' + esc(p.name === p.cardTitle ? p.cardEyebrow : p.cardTitle) + '</p></div><span class=\"cta\" aria-hidden=\"true\"><i class=\"sq\">' + ARROW + '</i><span>Case study</span></span></div></a>';")
CARD_CSS = """
/* ---- the frame: one ink container, shared by the statement block and the work board. Flat, no texture. ---- */
#jf { --frame: #17140f; --frame-r: 22px; }
#jf .wrap { max-width: max(1240px, 68vw); }
#jf .statement, #jf .board { background: var(--frame); border-radius: var(--frame-r); box-shadow: inset 0 1px 0 rgba(255,255,255,.06), inset 0 0 0 1px rgba(255,255,255,.035), 0 30px 60px -40px rgba(0,0,0,.6); }
#jf .board { gap: clamp(14px, 1.8vw, 22px); padding: clamp(14px, 1.8vw, 22px); }
/* ---- the card: white satin. A single-direction hatch you only notice up close, under a sheen lit from the top-left seam. ---- */
#jf .tile { position: relative; isolation: isolate; overflow: hidden; color: var(--ink); border-radius: 14px; padding: var(--inset); border: 1px solid rgba(255,255,255,.55);
  background: #f7f6f2 url(@@UI@@satin_white.jpg) 0% 0% / 150% auto;
  box-shadow: inset 0 1px 0 #fff, 0 16px 36px -22px rgba(0,0,0,.75);
  transition: transform 1s cubic-bezier(.22,.61,.36,1), box-shadow 1s cubic-bezier(.22,.61,.36,1); }
#jf .tile:nth-child(3n+2) { background-position: 100% 40%; }
#jf .tile:nth-child(3n) { background-position: 40% 100%; }
#jf .tile:nth-child(4n+1) { background-size: 170% auto; }
#jf .tile::before { content: ''; position: absolute; inset: 0; z-index: -1; pointer-events: none; opacity: 0; transition: opacity .8s ease; background: radial-gradient(120% 70% at 50% 120%, color-mix(in srgb, var(--acc) 16%, transparent), transparent 65%); }
#jf .tile:hover { transform: translateY(-4px); box-shadow: inset 0 1px 0 #fff, 0 30px 54px -28px color-mix(in srgb, var(--acc) 55%, #000), 0 14px 28px -18px rgba(0,0,0,.55); }
#jf .tile:hover::before { opacity: 1; }
#jf .tile .cover, #jf .tile .meta { position: relative; z-index: 1; }
#jf .tile .cover { border-radius: 8px; background: #e6e2db; }
#jf .tile .cover::after { content: ''; position: absolute; inset: 0; z-index: 2; border-radius: inherit; pointer-events: none; box-shadow: inset 0 0 0 1px rgba(21,18,15,.10), inset 0 2px 6px rgba(0,0,0,.28), inset 0 18px 36px -22px rgba(0,0,0,.45), inset 0 -14px 30px -22px rgba(0,0,0,.30); }
#jf .tile .meta { display: flex; align-items: center; justify-content: space-between; gap: 28px; padding: 16px 6px 8px 12px; }
#jf .tile .meta .txt { flex: 1; min-width: 0; align-self: center; padding: 2px 0 4px; }
#jf .tile .meta h3, #jf .tile h3 { font-family: var(--serif); font-weight: 400; font-size: clamp(21px, 1.7vw, 26px); line-height: 1.1; letter-spacing: .045em; text-transform: uppercase; margin: 0; color: var(--ink); }
#jf .tile .meta p { font-weight: 400; font-size: 14px; line-height: 1.4; letter-spacing: .005em; margin: 7px 0 0; color: rgba(21,18,15,.56); text-wrap: balance; }
/* ---- the button: a recessed track of charcoal satin with a square spun-gold pin at the left. On hover the gold grows across the whole button; the arrow and label hold still and the label turns ink. ---- */
#jf .tile .meta .cta { position: relative; display: block; width: clamp(210px, 34%, 300px); height: 64px; align-self: center; border-radius: 10px; flex: none; overflow: hidden; white-space: nowrap;
  color: #f4efe6; font-weight: 600; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase;
  background: linear-gradient(rgba(27,23,20,.45), rgba(27,23,20,.45)), #1b1714 url(@@UI@@satin_ink.jpg) center / cover; transition: box-shadow 1.1s ease; }
#jf .tile .meta .cta::after { content: ''; position: absolute; inset: 0; z-index: 3; border-radius: inherit; pointer-events: none; box-shadow: inset 0 1px 1px rgba(0,0,0,.4), inset 0 4px 8px -4px rgba(0,0,0,.45), inset 0 0 0 1px rgba(0,0,0,.2); transition: opacity 1.1s ease; }
#jf .tile .meta .cta > span { position: absolute; inset: 0; z-index: 2; display: grid; place-items: center; padding: 0 16px 0 70px; transition: color .8s ease .2s, padding 1.1s cubic-bezier(.22,.61,.36,1); }
#jf .tile .meta .cta .sq { position: absolute; z-index: 1; top: 5px; left: 5px; width: 54px; height: 54px; border-radius: 7px; font-style: normal; color: #241b06;
  background: radial-gradient(90px 60px at var(--mx, 30%) 0%, rgba(255,250,232,.55), rgba(255,250,232,0) 70%), url(@@UI@@gold_spun.jpg) left center / 330px 100%;
  box-shadow: inset 0 1px 0 rgba(255,248,222,.75), inset 0 -1px 0 rgba(70,50,12,.5), 0 2px 6px rgba(0,0,0,.55);
  transition: top 1.1s cubic-bezier(.22,.61,.36,1), left 1.1s cubic-bezier(.22,.61,.36,1), width 1.1s cubic-bezier(.22,.61,.36,1), height 1.1s cubic-bezier(.22,.61,.36,1), border-radius 1.1s cubic-bezier(.22,.61,.36,1), box-shadow 1.1s ease; }
#jf .tile .meta .cta .sq svg { position: absolute; top: 50%; left: 20px; width: 14px; height: 14px; transform: translateY(-50%); transition: left 1.1s cubic-bezier(.22,.61,.36,1); }
#jf .tile:hover .meta .cta .sq { top: 0; left: 0; width: 100%; height: 100%; border-radius: 10px; box-shadow: none; }
#jf .tile:hover .meta .cta > span { color: #241b06; }
#jf .tile:hover .meta .cta::after { opacity: 0; }
#jf .tile:hover .meta .cta { box-shadow: 0 0 14px -2px rgba(214,180,100,.55), 0 6px 20px -8px rgba(201,162,75,.45); }
@media (max-width: 760px) { #jf .tile .meta .cta { width: 64px; } #jf .tile .meta .cta > span { display: none; } #jf .tile .meta .cta .sq svg { left: 20px; } }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + CARD_CSS.replace("@@UI@@", BASE + "ui/"))
must("  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);\n",
     "  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);\n  root.addEventListener('pointermove', function (e) { var t = e.target.closest && e.target.closest('.tile'); if (!t) return; var r = t.getBoundingClientRect(); t.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%'); t.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%'); }, { passive: true });\n")

# 10. Visual Response as a story: 28 posters, every one an exact 18x24, square corners, on a strict grid that changes pace:
#     one full-width detail piece, then pairs, threes and fours. Each poster drifts inside its own frame as it crosses the screen.
#     Files come from export_posters.py (assets/vr/NN.jpg for the grid, NN_full.jpg for the lightbox).
VR_ROWS = [[1], [8, 9], [24, 7, 22], [10, 16], [13], [4, 5, 11], [14, 20, 6, 27], [0, 3], [12, 25, 19], [21], [2, 17], [15, 18, 23, 26]]
VR_NAMES = {0: 'You Ever Wonder Why', 1: 'Seshat (Sophia)', 2: 'The Red Knight', 3: 'T.R.O.N', 4: 'Oysters In My Pocket', 5: "Da Art of Storytellin' Part 2", 6: 'On the Count of Three',
            7: 'Human Life', 8: 'A Horse With No Name', 9: 'A Horse With No Name, motorcycle', 10: 'Swim Good', 11: 'Her Pistol Go', 12: 'Lil Francisco', 13: 'Dots and Lines',
            14: 'Control Yourself', 15: 'Well It Feels Like That Again', 16: 'Nack Nostalgia', 17: 'Dead Ringers', 18: 'Untitled, blue', 19: 'The Man With Two Brains',
            20: 'Keep Going', 21: 'I Am', 22: 'Be Alright', 23: 'For Once In My Life', 24: 'Gone', 25: 'You Know That I Hide Them', 26: 'After Hours in the Goose House', 27: 'Untitled, cat'}
assert sorted(i for r in VR_ROWS for i in r) == list(range(28))
VR_JS = ("  var VR_ROWS = " + json.dumps(VR_ROWS) + ", VR_NAMES = " + json.dumps(VR_NAMES) + ", VR_BASE = '" + BASE + "vr/';\n"
  "  function vrStory() {\n"
  "    var n = 0, sp = [2.2, 3.4, 1.6, 2.8];\n"
  "    return '<section class=\"deliv vr\"><div class=\"metarow rv\"><span class=\"eyebrow\">The archive</span><span class=\"rule\"></span><span class=\"idx\">28 posters</span></div><div class=\"vrg\">' + VR_ROWS.map(function (row) {\n"
  "      return '<div class=\"vrr n' + row.length + '\">' + row.map(function (i, c) { var f = ('0' + i).slice(-2); n++;\n"
  "        return '<figure class=\"fig vp rv\" style=\"transition-delay:' + (c * 90) + 'ms\" data-sp=\"' + sp[(n + c) % 4] + '\" data-lb=\"' + VR_BASE + f + '_full.jpg\"><img src=\"' + VR_BASE + f + '.jpg\" alt=\"Visual Response poster: ' + esc(VR_NAMES[i]) + '\" width=\"1200\" height=\"1600\" loading=\"lazy\" decoding=\"async\"></figure>'; }).join('') + '</div>';\n"
  "    }).join('') + '</div></section>';\n"
  "  }\n")
must("  var THREAD = ", VR_JS + "  var THREAD = ")
must("    if (p.posters) out += '<section class=\"deliv\"><div class=\"metarow rv\"><span class=\"eyebrow\">The archive</span>",
     "    if (k === 'vr') out += vrStory(); else if (p.posters) out += '<section class=\"deliv\"><div class=\"metarow rv\"><span class=\"eyebrow\">The archive</span>")
VR_CSS = """
/* Visual Response: the poster story */
#jf .vrg { display: grid; gap: 12px; margin-top: clamp(36px, 5vw, 64px); }
#jf .vrr { display: grid; gap: 12px; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); }
#jf .vrr.n1 { --n: 1; } #jf .vrr.n2 { --n: 2; } #jf .vrr.n3 { --n: 3; } #jf .vrr.n4 { --n: 4; }
#jf .vrr .fig { margin: 0; border-radius: 0; aspect-ratio: 3 / 4; overflow: hidden; background: #15120f; }
#jf .vrr .fig img { width: 100%; height: 100%; object-fit: cover; border-radius: 0; }
#jf .vrr { transform: translate3d(0, var(--py, 0px), 0); will-change: transform; }
@media (max-width: 760px) {
  #jf .vrg, #jf .vrr { gap: 8px; }
  #jf .vrr.n3, #jf .vrr.n4 { --n: 2; }
  #jf .vrr.n3 .fig:first-child { grid-column: 1 / -1; }
}
@media (prefers-reduced-motion: reduce) { #jf .vrr { transform: none; } }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + VR_CSS)
must("  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);\n",
     """  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);
  /* Visual Response: each row drifts a few pixels against its neighbours as it crosses the screen, each at its own rate */
  (function () {
    var ps = [].slice.call(root.querySelectorAll('.vrr .fig')); if (!ps.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var tick = false;
    var rows = [].slice.call(root.querySelectorAll('.vrr')), amp = [18, 30, 12, 24];
    function run() { tick = false; var vh = window.innerHeight; rows.forEach(function (f, i) { var r = f.getBoundingClientRect(); if (r.bottom < -200 || r.top > vh + 200) return; var off = (r.top + r.height / 2 - vh / 2) / vh, y = Math.max(-1, Math.min(1, off)) * amp[i % 4]; f.style.setProperty('--py', y.toFixed(1) + 'px'); }); }
    function req() { if (!tick) { tick = true; requestAnimationFrame(run); } }
    root.addEventListener('scroll', req, { passive: true }); window.addEventListener('resize', req); run();
    /* the lightbox file starts loading as soon as the pointer is on a poster */
    ps.forEach(function (f) { f.addEventListener('pointerenter', function () { if (!f.__pre) { f.__pre = new Image(); f.__pre.src = f.getAttribute('data-lb'); } }, { passive: true }); });
  })();
""")
# lightbox: show the image already on screen at once, then swap in the full file when it has loaded (no blank wait)
must("var f = figs[at].getAttribute('data-lb'); lbImg.src = src(f, 2400);",
     "var f = figs[at].getAttribute('data-lb'), g = figs[at].querySelector('img'), hi = new Image(), cur = at; if (g && (g.currentSrc || g.src)) lbImg.src = g.currentSrc || g.src; hi.onload = function () { if (cur === at && lb.classList.contains('open')) lbImg.src = hi.src; }; hi.src = src(f, 2400);")

# 11. contact block: ink satin in a double gold-hairline frame, a faint brocade lattice that fades toward the centre, deep inner shadow.
#     Gold is spent on the label, the ornament and the Copy button's hover; everything else is cream on ink.
must("'><div class=\"contact rv\"><div class=\"eyebrow\">Contact</div><h2 class=\"h2\">'",
     "'><div class=\"contact rv\"><div class=\"eyebrow\">Contact</div><i class=\"orn\" aria-hidden=\"true\"></i><h2 class=\"h2\">'")
CONTACT_CSS = """
/* contact: the prestige block */
#jf .contact { position: relative; isolation: isolate; overflow: hidden; color: var(--paper); border-radius: var(--frame-r, 22px); padding: clamp(64px, 8vw, 128px) clamp(24px, 6vw, 88px) clamp(60px, 7.4vw, 116px);
  background: #15120f url(@@UI@@satin_ink.jpg) center / cover;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.07), inset 0 0 0 1px rgba(201,162,75,.22), inset 0 30px 80px -30px rgba(0,0,0,.85), inset 0 -40px 90px -40px rgba(0,0,0,.8), 0 30px 60px -40px rgba(0,0,0,.6); }
#jf .contact::before { content: ''; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background-image: radial-gradient(circle, rgba(214,180,100,.34) 0 1.1px, transparent 1.7px), repeating-linear-gradient(45deg, rgba(201,162,75,.085) 0 1px, transparent 1px 34px), repeating-linear-gradient(-45deg, rgba(201,162,75,.085) 0 1px, transparent 1px 34px);
  background-size: 48.08px 48.08px, auto, auto; background-position: center;
  -webkit-mask-image: radial-gradient(ellipse 62% 78% at 50% 50%, transparent 46%, #000 100%); mask-image: radial-gradient(ellipse 62% 78% at 50% 50%, transparent 46%, #000 100%); }
#jf .contact::after { content: ''; position: absolute; inset: 12px; z-index: -1; pointer-events: none; border-radius: calc(var(--frame-r, 22px) - 10px); border: 1px solid rgba(201,162,75,.3); box-shadow: inset 0 0 0 1px rgba(0,0,0,.35); }
#jf .contact .eyebrow { color: var(--gold); letter-spacing: .32em; margin-bottom: 0; }
#jf .contact .orn { display: block; width: min(220px, 50%); height: 9px; margin: 22px auto clamp(26px, 3vw, 40px); background: linear-gradient(90deg, transparent, rgba(201,162,75,.75) 30%, rgba(201,162,75,.75) 42%, transparent 42%, transparent 58%, rgba(201,162,75,.75) 58%, rgba(201,162,75,.75) 70%, transparent) center / 100% 1px no-repeat; position: relative; }
#jf .contact .orn::after { content: ''; position: absolute; left: 50%; top: 50%; width: 7px; height: 7px; transform: translate(-50%, -50%) rotate(45deg); background: var(--gold); box-shadow: 0 0 0 3px rgba(201,162,75,.18); }
#jf .contact .h2 { color: #f7f0ea; font-size: clamp(34px, 4.8vw, 72px); line-height: 1.04; letter-spacing: -.005em; max-width: 20ch; text-wrap: balance; text-shadow: 0 2px 30px rgba(0,0,0,.5); }
#jf .contact .email { margin-top: clamp(34px, 4vw, 56px); gap: 16px; }
#jf .contact .email code { color: #f7f0ea; font-weight: 400; font-size: clamp(17px, 1.9vw, 24px); letter-spacing: .02em; }
#jf .contact .email .pill { height: 36px; padding: 0 18px; border-radius: 8px; background: rgba(247,240,234,.06); color: var(--paper); border: 1px solid rgba(201,162,75,.45); box-shadow: inset 0 1px 2px rgba(0,0,0,.5); transition: background .4s, color .4s, border-color .4s; }
#jf .contact .email .pill:hover { color: #241b06; border-color: transparent; background: url(@@UI@@gold_spun.jpg) center / cover; }
#jf .contact .links { margin-top: clamp(26px, 3vw, 40px); display: flex; flex-wrap: wrap; justify-content: center; gap: 10px 0; }
#jf .contact .links .ulink { color: rgba(247,240,234,.72); font-weight: 600; font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase; border-bottom: 0; padding: 4px clamp(14px, 2vw, 28px); position: relative; transition: color .3s; }
#jf .contact .links .ulink + .ulink::before { content: ''; position: absolute; left: 0; top: 50%; width: 4px; height: 4px; transform: translate(-50%, -50%) rotate(45deg); background: rgba(201,162,75,.6); }
#jf .contact .links .ulink::after { content: ''; position: absolute; left: clamp(14px, 2vw, 28px); right: clamp(14px, 2vw, 28px); bottom: -2px; height: 1px; background: var(--gold); transform: scaleX(0); transform-origin: left; transition: transform .45s cubic-bezier(.3,.9,.2,1); }
#jf .contact .links .ulink:hover { color: #f7f0ea; }
#jf .contact .links .ulink:hover::after { transform: scaleX(1); }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + CONTACT_CSS.replace("@@UI@@", BASE + "ui/"))

# 12. phone header: menu button (two lines that cross into an X) on the left, wordmark dead centre, Resume on the right.
#     The three links move into a panel that drops from under the header. Desktop is untouched.
must("    return '<header class=\"hdr\" id=\"jf-hdr\"><nav aria-label=\"Primary\">'",
     "    return '<header class=\"hdr\" id=\"jf-hdr\"><button class=\"burger\" type=\"button\" aria-label=\"Menu\" aria-expanded=\"false\" aria-controls=\"jf-nav\"><i></i><i></i></button><nav id=\"jf-nav\" aria-label=\"Primary\">'")
NAV_CSS = """
/* phone header */
#jf .hdr .burger { display: none; }
@media (max-width: 760px) {
  #jf .hdr { grid-template-columns: 1fr auto 1fr; padding: 0 12px; gap: 8px; }
  #jf .hdr .burger { display: grid; place-items: center; justify-self: start; position: relative; width: 40px; height: 40px; margin-left: -6px; padding: 0; border: 0; background: none; color: var(--ink); cursor: pointer; -webkit-tap-highlight-color: transparent; }
  #jf .hdr .burger i { position: absolute; left: 10px; right: 10px; height: 1.5px; border-radius: 1px; background: currentColor; transition: transform .5s cubic-bezier(.22,.61,.36,1), top .5s cubic-bezier(.22,.61,.36,1); }
  #jf .hdr .burger i:first-child { top: 16px; } #jf .hdr .burger i:last-child { top: 23px; }
  #jf .hdr.open .burger i:first-child { top: 19.5px; transform: rotate(45deg); }
  #jf .hdr.open .burger i:last-child { top: 19.5px; transform: rotate(-45deg); }
  #jf .hdr .mark svg { height: 17px; }
  #jf .hdr .util .pill { height: 30px; padding: 0 12px; }
  #jf .hdr nav { position: absolute; top: var(--header); left: 0; right: 0; display: flex; flex-direction: column; align-items: stretch; gap: 0; padding: 6px 20px 18px; background: #fff; box-shadow: 0 1px 0 rgba(21,18,15,.07), 0 24px 40px -24px rgba(21,18,15,.35);
    font-family: var(--serif); font-weight: 400; font-size: 30px; letter-spacing: .02em; color: var(--ink);
    opacity: 0; visibility: hidden; transform: translateY(-10px); pointer-events: none; transition: opacity .45s ease, transform .5s cubic-bezier(.22,.61,.36,1), visibility 0s linear .5s; }
  #jf .hdr.open nav { opacity: 1; visibility: visible; transform: none; pointer-events: auto; transition: opacity .45s ease, transform .5s cubic-bezier(.22,.61,.36,1), visibility 0s; }
  #jf .hdr nav span { display: none; }
  #jf .hdr nav a { padding: 16px 0; border-bottom: 1px solid var(--line); }
  #jf .hdr nav a:last-child { border-bottom: 0; }
  #jf .hdr nav a.on { color: var(--gold-ink); border-bottom-color: var(--line); }
  #jf .hdr.open.is-hidden { transform: none; }
}
@media (max-width: 420px) { #jf .hdr nav { font-size: 28px; } #jf .hdr .mark svg { height: 16px; } #jf .hdr .util .pill { padding: 0 11px; } }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + NAV_CSS)
must("  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);\n",
     """  sizeMosaics(); window.addEventListener('resize', sizeMosaics); setTimeout(sizeMosaics, 300);
  /* phone menu */
  (function () {
    function hd() { return root.querySelector('.hdr'); }
    function set(on) { var h = hd(); if (!h) return; h.classList.toggle('open', on); var b = h.querySelector('.burger'); if (b) { b.setAttribute('aria-expanded', on ? 'true' : 'false'); b.setAttribute('aria-label', on ? 'Close menu' : 'Menu'); } }
    root.addEventListener('click', function (e) { var t = e.target, h = hd(); if (!h || !t.closest) return; if (t.closest('.burger')) { set(!h.classList.contains('open')); return; } if (h.classList.contains('open') && (t.closest('.hdr nav a') || !t.closest('.hdr'))) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 760) set(false); });
  })();
""")
# card type: the project name leads harder, and the button label reads at a glance
must("font-size: clamp(21px, 1.7vw, 26px); line-height: 1.1; letter-spacing: .045em; text-transform: uppercase; margin: 0; color: var(--ink); }",
     "font-size: clamp(25px, 2.1vw, 33px); line-height: 1.08; letter-spacing: .035em; text-transform: uppercase; margin: 0; color: var(--ink); text-wrap: balance; }")
must("color: #f4efe6; font-weight: 600; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase;\n  background: linear-gradient",
     "color: #f4efe6; font-weight: 700; font-size: clamp(13px, 1vw, 15px); letter-spacing: .16em; text-transform: uppercase;\n  background: linear-gradient")

# home carousel leads with the same top five
must("    selected: ['snow', 'itw', 'levain', 'vr', 'legendary'],", "    selected: ['snow', 'tori', 'levain', 'cans', 'vr'],")
must("      snow: ['Snow Commerce · 2023', \"High-impact e-commerce design for entertainment's biggest brands\"],",
     "      snow: ['Snow Commerce · 2023', \"High-impact e-commerce design for entertainment's biggest brands\"],\n      tori: ['Hale Tori · 2026', 'Campaign design for two heritage aloha brands'],\n      cans: ['Philosophy Cans · 2026', 'Packaging, characters, 3D and motion'],")

# 13. portrait: the green duotone headshot (assets/ui/portrait.jpg, 4:5, on the site's cream), used on About and as the small home avatar
must("  portrait: ['image-43eef762-3214-43a3-b25f-0e5dde8d47e6.png', 208, 231],", "  portrait: ['" + BASE + "ui/portrait.jpg', 1000, 1250],")

# 14. home "Selected work" uses the same white satin cards as the board (one card per slide), and the button goes light:
#     a cream pill with a round spun-gold pin. On hover the gold still grows across the whole pill; the label stays ink throughout.
must("  function tile(k, sizes) {\n    var p = P[k];", "  function tile(k, sizes, sub) {\n    var p = P[k];")
must("'</h3><p>' + esc(p.name === p.cardTitle ? p.cardEyebrow : p.cardTitle) + '</p></div><span class=\"cta\"",
     "'</h3><p>' + esc(sub || (p.name === p.cardTitle ? p.cardEyebrow : p.cardTitle)) + '</p></div><span class=\"cta\"")
must("      return '<a class=\"proj\" href=\"' + href(k) + '\"' + (p.preview ? ' data-preview=\"' + p.preview + '\"' : '') + '>' + img(p.cover, '', '(max-width: 760px) 90vw, 1000px', 'bg', false, p.focus) +\n        '<div><div class=\"eyebrow\">' + esc(c[0]) + '</div><h3>' + esc(c[1]) + '</h3></div></a>';",
     "      return tile(k, '(max-width: 760px) 90vw, 1000px', c[1]);")
LIGHT_CSS = """
/* ---- home carousel: the board's white card, one per slide, sitting straight on the page ---- */
/* the scroller clips whatever leaves its box, so it is padded out past the full reach of the card shadows (hover included) and pulled back with negative margins */
#jf .carousel { gap: 18px; padding: 24px 48px 130px; margin: -24px -48px -112px; scroll-padding-left: 48px; }
/* where the next card peeks in, it dissolves instead of being sliced */
#jf .carousel { --fade: clamp(110px, 17vw, 340px); -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 26px, #000 calc(100% - var(--fade)), rgba(0,0,0,.93) calc(100% - var(--fade) * .86), rgba(0,0,0,.78) calc(100% - var(--fade) * .70), rgba(0,0,0,.55) calc(100% - var(--fade) * .54), rgba(0,0,0,.32) calc(100% - var(--fade) * .40), rgba(0,0,0,.14) calc(100% - var(--fade) * .27), rgba(0,0,0,.04) calc(100% - var(--fade) * .15), transparent calc(100% - var(--fade) * .04)); mask-image: linear-gradient(90deg, transparent 0, #000 26px, #000 calc(100% - var(--fade)), rgba(0,0,0,.93) calc(100% - var(--fade) * .86), rgba(0,0,0,.78) calc(100% - var(--fade) * .70), rgba(0,0,0,.55) calc(100% - var(--fade) * .54), rgba(0,0,0,.32) calc(100% - var(--fade) * .40), rgba(0,0,0,.14) calc(100% - var(--fade) * .27), rgba(0,0,0,.04) calc(100% - var(--fade) * .15), transparent calc(100% - var(--fade) * .04)); }
/* over the same stretch the card also goes out of focus: a real blur that ramps up toward the edge, so it melts instead of just thinning out */
#jf .carwrap { position: relative; }
#jf .carwrap::after { content: ''; position: absolute; z-index: 3; top: 2px; bottom: -70px; right: -48px; width: clamp(110px, 17vw, 340px); pointer-events: none;
  -webkit-backdrop-filter: blur(16px); backdrop-filter: blur(16px); -webkit-mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,.35) 30%, #000 62%); mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,.35) 30%, #000 62%); }
@media (max-width: 760px) { #jf .carwrap::after { right: -20px; } }
@media (max-width: 760px) { #jf .carousel { padding-inline: 20px; margin-inline: -20px; scroll-padding-left: 20px; } }
#jf .carousel a.tile { flex: 0 0 min(80%, 980px); scroll-snap-align: start; border-color: rgba(21,18,15,.07);
  box-shadow: inset 0 1px 0 #fff, 0 22px 44px -30px rgba(21,18,15,.5), 0 4px 12px -8px rgba(21,18,15,.18); }
#jf .carousel a.tile:hover { box-shadow: inset 0 1px 0 #fff, 0 34px 56px -30px color-mix(in srgb, var(--acc) 45%, #000), 0 10px 22px -14px rgba(21,18,15,.35); }
#jf .carousel a.tile .cover { aspect-ratio: 16 / 9; }
#jf .carousel a.tile .meta { padding: 20px 10px 12px 16px; }
#jf .carousel a.tile .meta h3 { font-size: clamp(27px, 2.5vw, 40px); }
#jf .carousel a.tile .meta p { font-size: 15px; }
@media (max-width: 760px) { #jf .carousel a.tile { flex-basis: 90%; } #jf .carousel a.tile .cover { aspect-ratio: 4 / 3; } }
/* ---- the button, light: cream pill, round gold pin ---- */
#jf a.tile .meta .cta { border-radius: 999px; color: #241b06; background: linear-gradient(180deg, #ece4d3, #f3ecde 60%, #f6f0e4); }
#jf a.tile .meta .cta::after { box-shadow: inset 0 1px 2px rgba(70,52,20,.28), inset 0 5px 9px -6px rgba(70,52,20,.30), inset 0 0 0 1px rgba(70,52,20,.12); }
#jf a.tile .meta .cta .sq { border-radius: 999px; box-shadow: inset 0 1px 0 rgba(255,248,222,.8), inset 0 -1px 0 rgba(70,50,12,.45), 0 2px 5px rgba(70,48,10,.38); }
#jf a.tile:hover .meta .cta .sq { border-radius: 999px; box-shadow: none; }
/* full hover: the gold keeps a pressed-in inner shadow (warm umber at the top lip, a thin light catch along the bottom) */
/* no frame behind the board: cards sit straight on the page and carry their own shadow (a tight contact line, a mid lift, a long soft fall) */
#jf .board.board { background: none; box-shadow: none; border-radius: 0; padding: 0; gap: clamp(22px, 2.4vw, 34px); }
#jf .board.board a.tile, #jf .carousel.carousel a.tile { border-color: rgba(21,18,15,.07);
  box-shadow: inset 0 1px 0 #fff, 0 1px 2px rgba(21,18,15,.07), 0 10px 18px -12px rgba(21,18,15,.22), 0 34px 60px -36px rgba(21,18,15,.55); }
#jf .board.board a.tile:hover, #jf .carousel.carousel a.tile:hover { box-shadow: inset 0 1px 0 #fff, 0 2px 4px rgba(21,18,15,.08), 0 18px 28px -16px rgba(21,18,15,.26), 0 50px 80px -40px color-mix(in srgb, var(--acc) 40%, rgba(21,18,15,.7)); }
#jf a.tile .meta .cta::after { transition: box-shadow 1.1s ease; }
#jf a.tile:hover .meta .cta::after { opacity: 1; box-shadow: inset 0 2px 3px rgba(58,38,4,.50), inset 0 9px 14px -8px rgba(58,38,4,.55), inset 0 -1px 0 rgba(255,246,214,.55), inset 0 -8px 12px -10px rgba(58,38,4,.30), inset 0 0 0 1px rgba(80,56,10,.28); }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + LIGHT_CSS)
must("</div><div class=\"carousel\" id=\"jf-car\">' + cards + '</div></section>'", "</div><div class=\"carwrap\"><div class=\"carousel\" id=\"jf-car\">' + cards + '</div></div></section>'")

# 15. home intro spacing: one rhythm. label -> headline -> paragraph step up evenly (1 : 1.25), the block sits closer to the statement
#     it introduces than to the hero above it, and the tracked label is nudged so it centres optically (tracking adds a trailing gap).
POS_CSS = """
#jf section.sec.positioning { padding-top: clamp(64px, 8vw, 120px); padding-bottom: clamp(44px, 5.2vw, 76px); }
#jf section.positioning .eyebrow { margin-bottom: clamp(20px, 2vw, 28px); padding-left: .16em; }
#jf section.positioning .h2 { max-width: 23ch; line-height: 1.07; }
#jf section.positioning p { margin-top: clamp(24px, 2.5vw, 36px); max-width: 44ch; line-height: 1.6; }
"""
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n" + POS_CSS)

# 16. home avatar: its own square crop centred on the face (assets/ui/portrait_sq.jpg), so the circle is filled and the head sits dead centre
must("'<div class=\"who\"><img src=\"' + src(D.portrait[0], 200) + '\"", "'<div class=\"who\"><img src=\"" + BASE + "ui/portrait_sq.jpg\"")
must("#jf .tile .cover { aspect-ratio: 16 / 10; }\n", "#jf .tile .cover { aspect-ratio: 16 / 10; }\n#jf .who.who img { width: 72px; height: 72px; flex: none; border-radius: 50%; object-fit: cover; object-position: 50% 50%; background: #f7f0ea; box-shadow: 0 0 0 1px rgba(21,18,15,.08), 0 8px 18px -10px rgba(21,18,15,.35); }\n")

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
