"""Clip-commentary short: source clip in a frame over a blurred copy of itself, our captions + ElevenLabs narration,
clip audio ducked underneath, on-screen credit. Usage: python3 clip.py specs/<name>.json  (spec: see clip spec example)"""
import sys, json, os, subprocess
from playwright.sync_api import sync_playwright
sp = json.load(open(sys.argv[1])); name = sp['name']; th = sp['theme']; FPS = 30
FS = os.environ.get('MTO_FONTS', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules/@fontsource'))
fam = th.get('font', 'montserrat')
ff = '\n'.join(f"@font-face{{font-family:F;src:url(file://{FS}/{fam}/files/{fam}-latin-{w}-normal.woff2);font-weight:{w}}}" for w in (600, 700, 800, 900))
S = []; t = 0
for sc in sp['scenes']: S.append([t, t + sc['dur']]); t += sc['dur']
T = t; acc, acc2 = th['acc'], th['acc2']
scenes_html = ''
for i, sc in enumerate(sp['scenes']):
    if sc.get('cta'):
        scenes_html += f'''<div class="sc cta" id="s{i}"><div class="ctabox"><img src="{th['logo']}" class="cl"><div class="q">{sc['q']}</div>
        <div class="sub">{sc.get('sub','Tell us in the comments')}</div><div class="url">{sc['url']}</div><div class="fine">{sc.get('fine','')}</div></div></div>'''
    else:
        scenes_html += f'<div class="sc" id="s{i}"><div class="cap"><div class="k">{sc["kicker"]}</div><div class="h">{sc["head"]}</div></div></div>'
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>{ff}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:transparent;font-family:F,sans-serif;overflow:hidden}}
#prog{{position:absolute;left:0;top:0;height:12px;background:{acc}}}
.top{{position:absolute;left:70px;top:60px;display:flex;align-items:center;gap:20px}}
.top .lg{{background:#fff;border-radius:18px;padding:10px 14px;height:96px;display:flex;align-items:center}} .top img{{max-height:76px;max-width:200px}}
.top .b{{color:#fff;font-weight:800;font-size:30px;letter-spacing:1px;text-shadow:0 2px 8px rgba(0,0,0,.6)}} .top small{{display:block;color:{acc2};font-size:22px;letter-spacing:3px;margin-top:4px}}
.frame{{position:absolute;left:222px;top:196px;width:636px;height:1128px;border:6px solid {acc};border-radius:28px;box-shadow:0 20px 60px rgba(0,0,0,.6)}}
.credit{{position:absolute;left:240px;top:1270px;background:rgba(0,0,0,.72);color:#fff;font-weight:700;font-size:24px;padding:8px 16px;border-radius:10px}}
.sc{{position:absolute;inset:0;opacity:0}}
.cap{{position:absolute;left:70px;right:150px;top:1352px;background:rgba(8,14,28,.92);border-radius:26px;padding:26px 32px 30px;border-left:12px solid {acc}}}
.k{{display:inline-block;background:{acc};color:{th.get('kickfg','#fff')};font-weight:800;font-size:26px;padding:8px 18px;border-radius:8px;letter-spacing:2px;text-transform:uppercase}}
.h{{color:#fff;font-weight:900;font-size:58px;line-height:1.08;margin-top:16px;letter-spacing:-1px}} .a{{color:{acc2}}}
.cta .ctabox{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:rgba(8,14,28,.94);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 150px 300px 70px;text-align:center}}
.cl{{max-width:380px;max-height:240px;background:#fff;border-radius:28px;padding:24px 30px}}
.q{{color:#fff;font-weight:900;font-size:84px;line-height:1.05;margin-top:44px}} .sub{{color:#cfd6e4;font-weight:600;font-size:44px;margin-top:30px}}
.url{{background:{acc};color:{th.get('kickfg','#fff')};font-weight:800;font-size:38px;padding:12px 26px;border-radius:12px;margin-top:40px}} .fine{{color:#9aa6b8;font-size:30px;margin-top:24px;font-weight:600}}
</style></head><body><div id="prog"></div>
<div class="frame"></div><div class="credit">{sp['credit_short']}</div>
<div class="top"><div class="lg"><img src="{th['logo']}"></div><div class="b">{th['name']}<small>{th['tag']}</small></div></div>
{scenes_html}
<script>const S={json.dumps(S)},T={T};const e=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const bk=x=>{{x=x<0?0:x>1?1:x;const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);}};
window.setTime=t=>{{document.getElementById('prog').style.width=(t/T*1080)+'px';
S.forEach(([a,b],i)=>{{const el=document.getElementById('s'+i);const l=t-a;const on=t>=a&&t<b;el.style.opacity=on?(i==0?1:e(l/0.25)):0;
 if(!on)return; const cap=el.querySelector('.cap,.ctabox'); const k=bk(l/0.45); cap.style.transform=`translateY(${{(1-k)*80}}px) scale(${{0.96+0.04*k}})`;
 const h=el.querySelector('.h'); if(h){{h.style.opacity=e((l-0.15)/0.3);}} }});}};setTime(0);</script></body></html>'''
os.makedirs('clip', exist_ok=True); hp = os.path.abspath(f'clip/{name}.html'); open(hp, 'w').write(page)
fd = f'clip/{name}_f'; os.makedirs(fd, exist_ok=True)
step = int(os.environ.get('OVL_STEP', '1'))  # overlay frames are re-used for `step` video frames
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + hp); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    n = int(T * FPS)
    for i in range(0, n, step):
        pg.evaluate(f'setTime({i/FPS})'); pg.screenshot(path=f'{fd}/o{i//step:05d}.png', omit_background=True)
    br.close()
src = sp['clip']; ss = sp.get('clip_start', 0); vo = f'out/{name}_vo.wav'
fc = (f"[0:v]trim=start={ss}:duration={T},setpts=PTS-STARTPTS,split[a][b];"
      f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25:saturation=0.8[bg];"
      f"[b]scale=636:1128:force_original_aspect_ratio=increase,crop=636:1128[fg];"
      f"[bg][fg]overlay=222:196[base];[2:v]setpts=N/({FPS/step}*TB),fps={FPS}[ov];[base][ov]overlay=0:0:shortest=1,format=yuv420p[v];"
      f"[0:a]atrim=start={ss}:duration={T},asetpts=PTS-STARTPTS,volume={sp.get('clip_volume',0.14)}[ca];[1:a]volume=1.0[va];[ca][va]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-i', vo, '-framerate', str(FPS / step), '-i', f'{fd}/o%05d.png',
                '-filter_complex', fc, '-map', '[v]', '-map', '[aout]', '-t', str(T), '-c:v', 'libx264', '-crf', '21', '-preset', 'medium',
                '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', f'out/{name}.mp4'], check=True)
print('done', name, T, os.path.getsize(f'out/{name}.mp4'))
