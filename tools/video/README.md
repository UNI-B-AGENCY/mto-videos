# Video engine (shorts, 1080x1920)
Setup once per run: `cd tools/video && npm i @fontsource/montserrat @fontsource/poppins @fontsource/inter && mkdir -p out`
1. Write a spec JSON in specs/ (see specs.py for six worked examples; scene types: hook, text, stats, list, bars, versus, cta; theme per brand: logo/, bg/ or your own photo).
2. `python3 gen.py specs/<brand>.json out/<brand>.html` → `python3 snap.py <brand>` (contact sheet out/<brand>_sheet.jpg, look at it) → `python3 render.py <brand>` (frames + original music + whooshes → out/<brand>.mp4).
Change layouts, colours and scene order every time; it's a starting point, not a template to repeat. Text stays out of the bottom 300 px and right 140 px.

## Clip commentary (repurpose a YouTube/TikTok/Instagram clip)
1. Find a real clip URL (WebSearch in "extended" mode returns youtube.com/watch and /shorts links; prefer news outlets and official company channels). fetch_media(url, brand, max_height 720, start/end for long sources) → git pull, the clip is under videos/<slug>-<ts>.mp4.
2. Narration in the house voice (see above), one line per caption scene, CTA last.
3. Copy clip-spec-example.json, set clip path, credit_short ("Video: <channel> / <platform>"), captions. `python3 vo.py specs/x.json audio/x.mp3 out/x_vo.wav 1.12` then `OVL_STEP=2 python3 clip.py specs/x.json` → out/x.mp4 (clip framed over a blurred copy, clip audio ducked, captions + CTA, credit always visible).
4. Put the credit in every caption ("Video: <channel> on YouTube"). Never crop the source watermark. git rm the raw source clip after rendering.
