# Video engine (shorts, 1080x1920)
Setup once per run: `cd tools/video && npm i @fontsource/montserrat @fontsource/poppins @fontsource/inter && mkdir -p out`
1. Write a spec JSON in specs/ (see specs.py for six worked examples; scene types: hook, text, stats, list, bars, versus, cta; theme per brand: logo/, bg/ or your own photo).
2. `python3 gen.py specs/<brand>.json out/<brand>.html` → `python3 snap.py <brand>` (contact sheet out/<brand>_sheet.jpg, look at it) → `python3 render.py <brand>` (frames + original music + whooshes → out/<brand>.mp4).
Change layouts, colours and scene order every time; it's a starting point, not a template to repeat. Text stays out of the bottom 300 px and right 140 px.
