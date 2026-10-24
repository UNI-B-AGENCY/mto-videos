# Video engine (shorts, 1080x1920)
Setup once per run: `cd tools/video && npm i @fontsource/montserrat @fontsource/poppins @fontsource/inter && mkdir -p out`
1. Write a spec JSON in specs/ (see specs.py for six worked examples; scene types: hook, text, stats, list, bars, versus, cta; theme per brand: logo/, bg/ or your own photo).
2. `python3 gen.py specs/<brand>.json out/<brand>.html` → `python3 snap.py <brand>` (contact sheet out/<brand>_sheet.jpg, look at it) → `python3 render.py <brand>` (frames + original music + whooshes → out/<brand>.mp4).
Change layouts, colours and scene order every time; it's a starting point, not a template to repeat. Text stays out of the bottom 300 px and right 140 px.

## Clip commentary (repurpose a YouTube/TikTok/Instagram clip)
1. Find a real clip URL (WebSearch in "extended" mode returns youtube.com/watch and /shorts links; prefer news outlets and official company channels). fetch_media(url, brand, max_height 720, start/end for long sources) → git pull, the clip is under videos/<slug>-<ts>.mp4.
2. Narration in the BRAND voice (see table below), one line per caption scene, CTA last.
3. Copy clip-spec-example.json, set clip path, credit_short ("Video: <channel> / <platform>"), captions. `python3 vo.py specs/x.json audio/x.mp3 out/x_vo.wav 1.12` then `OVL_STEP=2 python3 clip.py specs/x.json` → out/x.mp4 (clip framed over a blurred copy, clip audio ducked, captions + CTA, credit always visible).
4. Put the credit in every caption ("Video: <channel> on YouTube"). Never crop the source watermark. git rm the raw source clip after rendering.

## Story videos (DEFAULT): real images/clips behind every line — `story.py`
Every scene needs a picture or clip that shows what the line is about (the person, company, product, place, building, document, chart). Text-only animation is not allowed any more.
1. Find media per scene: official press photos / company newsroom images / government pages (WebSearch), Unsplash connector (search_photos → download_asset gives the URL; credit "Photo: <name> / Unsplash"), news clips via fetch_media (YouTube/TikTok/Instagram), or mto-mcp generate_image only as a last resort (credit "AI image").
2. The sandbox cannot download images from most sites (proxy 403). Queue them: write the URL into `media-queue/<brand>-<slug>-<n>.jpg.txt`, commit + push, wait ~20 s, git pull → `media/<brand>-<slug>-<n>.jpg`. (Audio: `audio-queue/<name>.txt` → `audio/<name>.mp3`.)
3. Spec: see the docstring at the top of story.py. Each scene: media, credit (always), kicker, head (with <span class=a>…</span> highlight), optional big counter, pos. Last scene: cta.
4. `python3 vo.py specs/x.json audio/x.mp3 out/x_vo.wav 1.08` then `python3 story.py specs/x.json` → out/x.mp4 + out/x-cover.jpg. Look at 4–6 frames before posting.
5. After posting: git rm media/ and audio/ files you used and any raw third-party clip.

## Narration — ONE fixed voice PER BRAND (never mix, never change)
ElevenLabs creative_generate_speech, model `eleven_multilingual_v2` (keeps the accent), generations_count 1, never call twice for the same script:
- marketpulseafrica → `reGkImJki7uJOve2F4A0` Ifeoma Odumodu (Nigerian female, authoritative)
- afrotech → `i9sr2Eu9ynYVEaDDkF8I` Sulbyee (Nigerian male, tech)
- opportunities-to-apply → `BcpjRWrYhDBHmOnetmBl` Thandi (South African female, young)
- cameroonbusinessreview → `F18yf5BixLZCvKiiW0yJ` Steven (West African male, deep)
- ainewsreport → `t1yzxMpe9zK42bXmI1T2` K. V. Hagen (deep documentary male)
- ainewsround → `BuaKXS4Sv1Mccaw3flfU` Christina (energetic female)
Script: one spoken line per scene, scenes separated by `<break time="1.6s" />`, numbers spelled out, 90–110 words.
Download: content_url (from creative_get_flow_run_status) → `audio-queue/<brand>-<slug>.txt` → commit+push → ~20 s → git pull → `audio/<brand>-<slug>.mp3`. If the push is impossible, use mto-mcp fetch_media(url=content_url, brand, commit true) instead and git pull the file it commits.
