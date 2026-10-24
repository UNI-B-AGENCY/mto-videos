"""Story short: every scene sits on a REAL image or video clip that matches what is said/shown
(press photo, product shot, location, news clip, AI image as last resort), with Ken Burns motion,
our kinetic captions, on-screen credits, narration (vo.py) and a ducked music bed.

Usage:
  python3 vo.py specs/x.json audio/x.mp3 out/x_vo.wav 1.12   # sets scene durations from the voice
  OVL_STEP=2 python3 story.py specs/x.json                    # -> out/x.mp4

Spec (JSON):
{ "name": "x",
  "theme": {"name":"MARKET PULSE AFRICA","tag":"AFRICAN EQUITIES","logo":"logo/mpa.webp","font":"montserrat",
            "acc":"#c99a13","acc2":"#f2b01e","kickfg":"#091930"},
  "scenes": [
    {"media":"media/refinery.jpg", "credit":"Photo: Dangote Group", "kicker":"Dangote refinery IPO",
     "head":"Last chance to buy in: closes <span class=a>Tuesday</span>", "sub":"N525 a share", "pos":"bottom",
     "big":{"to":525,"pre":"N","suf":"","dec":0}},
    {"media":"media/clip.mp4", "media_start":12, "credit":"Video: africanews / YouTube", "clip_audio":0.15, ...},
    {"cta":true, "media":"media/lagos.jpg", "credit":"Photo: Unsplash", "q":"Are you buying?", "sub":"Comment below",
     "url":"marketpulseafrica.com", "fine":"Not investment advice"}
  ] }
pos: "bottom" (default), "top" or "center". Every scene needs media; credit is shown on screen for that scene.
"""
import sys, json, os, subprocess, wave, numpy as np
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sp = json.load(open(sys.argv[1])); name = sp['name']; th = sp['theme']; FPS = 30
FS = os.environ.get('MTO_FONTS', os.path.join(HERE, 'node_modules/@fontsource'))
fam = th.get('font', 'montserrat')
def P(p): return p if os.path.isabs(p) else os.path.abspath(p)
logo = P(th['logo']) if os.path.exists(P(th['logo'])) else os.path.join(HERE, th['logo'])
ff = '\n'.join(f"@font-face{{font-family:F;src:url(file://{FS}/{fam}/files/{fam}-latin-{w}-normal.woff2);font-weight:{w}}}" for w in (600, 700, 800, 900))
S = []; t = 0
for sc in sp['scenes']:
    S.append([round(t, 3), round(t + sc['dur'], 3)]); t += sc['dur']
T = round(t, 3); acc, acc2, kfg = th['acc'], th['acc2'], th.get('kickfg', '#fff')
os.makedirs('out', exist_ok=True); os.makedirs(f'out/{name}_seg', exist_ok=True)

# ---------- 1. background segments (real media with motion) ----------
segs = []
for i, sc in enumerate(sp['scenes']):
    m = P(sc['media']); d = sc['dur']; out = f'out/{name}_seg/s{i:02d}.mp4'
    is_vid = m.lower().endswith(('.mp4', '.mov', '.webm', '.mkv'))
    dirn = [(1, 0), (-1, 0), (0, 1), (0, -1)][i % 4]
    if is_vid:
        ss = sc.get('media_start', 0)
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', m], capture_output=True, text=True).stdout.strip().split(',')
        w, h = int(probe[0]), int(probe[1])
        if w > h:   # landscape: blurred fill + full clip in the middle
            vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.22[bg];"
                  f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2-120,fps={FPS},format=yuv420p")
        else:
            vf = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},format=yuv420p"
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ss), '-t', str(d), '-stream_loop', '-1', '-i', m, '-filter_complex', vf, '-t', str(d), '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', out]
    else:       # still image: slow push-in + drift (Ken Burns)
        z0, z1 = (1.0, 1.12) if i % 2 == 0 else (1.12, 1.0)
        vf = (f"scale=1296:2304:force_original_aspect_ratio=increase,crop=1296:2304,"
              f"zoompan=z='{z0}+({z1}-{z0})*on/({int(d*FPS)})':x='(iw-iw/zoom)/2+{dirn[0]}*on*0.6':y='(ih-ih/zoom)/2+{dirn[1]}*on*0.6':d=1:s=1080x1920:fps={FPS},format=yuv420p")
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', str(FPS), '-t', str(d), '-i', m, '-vf', vf, '-frames:v', str(int(round(d * FPS))), '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', out]
    subprocess.run(cmd, check=True); segs.append(out)
with open(f'out/{name}_seg/list.txt', 'w') as f:
    for s in segs: f.write(f"file '{os.path.abspath(s)}'\n")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'out/{name}_seg/list.txt', '-c', 'copy', f'out/{name}_bg.mp4'], check=True)

# ---------- 2. transparent overlay (captions, credits, header, progress, CTA) ----------
def words(html):  # wrap words for kinetic reveal, keep <span class=a>...</span>
    import re
    out = []; n = 0
    for tok in re.split(r'(<span class=a>.*?</span>)', html):
        if not tok: continue
        if tok.startswith('<span'):
            inner = re.sub(r'</?span[^>]*>', '', tok)
            for w in inner.split(): out.append(f'<i class="w a" style="--n:{n}">{w}</i>'); n += 1
        else:
            for w in tok.split(): out.append(f'<i class="w" style="--n:{n}">{w}</i>'); n += 1
    return ' '.join(out)
scenes_html = ''
for i, sc in enumerate(sp['scenes']):
    cred = f'<div class="cred">{sc["credit"]}</div>' if sc.get('credit') else ''
    if sc.get('cta'):
        scenes_html += f'''<div class="sc" id="s{i}">{cred}<div class="ctabox"><img src="file://{logo}" class="cl"><div class="q">{sc['q']}</div>
          <div class="sub">{sc.get('sub','Tell us in the comments')}</div><div class="url">{sc['url']}</div><div class="fine">{sc.get('fine','')}</div></div></div>'''
        continue
    big = ''
    if sc.get('big'):
        b = sc['big']; big = f'<div class="big" data-to="{b["to"]}" data-pre="{b.get("pre","")}" data-suf="{b.get("suf","")}" data-dec="{b.get("dec",0)}"></div>'
    sub = f'<div class="sub2">{sc["sub"]}</div>' if sc.get('sub') else ''
    scenes_html += f'''<div class="sc pos-{sc.get('pos','bottom')}" id="s{i}">{cred}<div class="cap"><div class="k">{sc.get('kicker','')}</div>{big}
      <div class="h">{words(sc['head'])}</div>{sub}</div></div>'''
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>{ff}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:transparent;font-family:F,sans-serif;overflow:hidden}}
#shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 45%,rgba(0,0,0,.78) 72%,rgba(0,0,0,.86) 100%)}}
#prog{{position:absolute;left:0;top:0;height:12px;background:{acc}}}
.top{{position:absolute;left:70px;top:70px;display:flex;align-items:center;gap:20px}}
.top .lg{{background:#fff;border-radius:18px;padding:10px 14px;height:96px;display:flex;align-items:center}} .top img{{max-height:76px;max-width:200px}}
.top .b{{color:#fff;font-weight:800;font-size:30px;letter-spacing:1px;text-shadow:0 2px 10px rgba(0,0,0,.7)}} .top small{{display:block;color:{acc2};font-size:22px;letter-spacing:3px;margin-top:4px}}
.sc{{position:absolute;inset:0;opacity:0}}
.cred{{position:absolute;left:70px;top:1540px;background:rgba(0,0,0,.66);color:#fff;font-weight:700;font-size:24px;padding:8px 16px;border-radius:10px}}
.cap{{position:absolute;left:70px;right:150px}}
.pos-bottom .cap{{top:auto;bottom:420px}} .pos-top .cap{{top:240px}} .pos-center .cap{{top:760px}}
.k{{display:inline-block;background:{acc};color:{kfg};font-weight:800;font-size:28px;padding:9px 20px;border-radius:8px;letter-spacing:2px;text-transform:uppercase}}
.h{{color:#fff;font-weight:900;font-size:76px;line-height:1.06;margin-top:18px;letter-spacing:-1px;text-shadow:0 4px 24px rgba(0,0,0,.75)}}
.w{{font-style:normal;display:inline-block;opacity:0}} .a{{color:{acc2}}}
.sub2{{color:#eef2f8;font-weight:700;font-size:42px;margin-top:18px;text-shadow:0 2px 14px rgba(0,0,0,.8)}}
.big{{color:{acc2};font-weight:900;font-size:190px;line-height:1;margin-top:10px;letter-spacing:-5px;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.ctabox{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:rgba(6,10,20,.80);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 150px 300px 70px;text-align:center}}
.cl{{max-width:380px;max-height:240px;background:#fff;border-radius:28px;padding:24px 30px}}
.q{{color:#fff;font-weight:900;font-size:84px;line-height:1.05;margin-top:44px}} .sub{{color:#cfd6e4;font-weight:600;font-size:44px;margin-top:30px}}
.url{{background:{acc};color:{kfg};font-weight:800;font-size:38px;padding:12px 26px;border-radius:12px;margin-top:40px}} .fine{{color:#aab4c4;font-size:30px;margin-top:24px;font-weight:600}}
</style></head><body><div id="shade"></div><div id="prog"></div>
<div class="top"><div class="lg"><img src="file://{logo}"></div><div class="b">{th['name']}<small>{th['tag']}</small></div></div>
{scenes_html}
<script>const S={json.dumps(S)},T={T};const e=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const bk=x=>{{x=x<0?0:x>1?1:x;const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);}};
window.setTime=t=>{{document.getElementById('prog').style.width=(t/T*1080)+'px';
 S.forEach(([a,b],i)=>{{const el=document.getElementById('s'+i);const l=(i==0?t+0.6:t-a);const on=t>=a&&t<b;el.style.opacity=on?1:0;if(!on)return;
  const k=el.querySelector('.k'); if(k){{k.style.transform=`scale(${{0.6+0.4*bk(l/0.35)}})`;k.style.opacity=e(l/0.2);}}
  el.querySelectorAll('.w').forEach(w=>{{const n=+w.style.getPropertyValue('--n');const q=bk((l-0.15-n*0.09)/0.3);w.style.opacity=e((l-0.15-n*0.09)/0.15);w.style.transform=`translateY(${{(1-q)*40}}px) scale(${{0.85+0.15*q}})`;}});
  const s2=el.querySelector('.sub2'); if(s2) s2.style.opacity=e((l-0.9)/0.3);
  const bg=el.querySelector('.big'); if(bg){{const q=e((l-0.3)/1.1);const v=+bg.dataset.to*q;bg.textContent=bg.dataset.pre+v.toLocaleString('en-US',{{minimumFractionDigits:+bg.dataset.dec,maximumFractionDigits:+bg.dataset.dec}})+bg.dataset.suf;}}
  const cb=el.querySelector('.ctabox'); if(cb){{cb.style.opacity=e(l/0.3);const lg=cb.querySelector('.cl');lg.style.transform=`scale(${{0.5+0.5*bk(l/0.6)}})`;}}
  const cr=el.querySelector('.cred'); if(cr) cr.style.opacity=e(l/0.3);
 }});}};setTime(0);</script></body></html>'''
hp = os.path.abspath(f'out/{name}_ovl.html'); open(hp, 'w').write(page)
fd = f'out/{name}_ovl'; os.makedirs(fd, exist_ok=True)
step = int(os.environ.get('OVL_STEP', '2'))
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + hp); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    for i in range(0, int(T * FPS), step):
        pg.evaluate(f'setTime({i/FPS})'); pg.screenshot(path=f'{fd}/o{i//step:05d}.png', omit_background=True)
    br.close()

# ---------- 3. audio: narration + original music bed ducked + whooshes + optional clip audio ----------
SR = 44100; n = int(T * SR); tt = np.arange(n) / SR; mus = np.zeros(n); rng = np.random.default_rng(len(name))
bpm = th.get('bpm', 100); beat = 60 / bpm
ch = [[220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7], [164.8, 207.7, 246.9]]
for bi in range(int(T / (4 * beat)) + 1):
    s = int(bi * 4 * beat * SR); m = min(int(4 * beat * SR), n - s)
    if m <= 0: break
    x = np.arange(m) / SR; env = np.minimum(1, x / 0.3) * np.minimum(1, (m / SR - x) / 0.5)
    for f in ch[bi % 4]: mus[s:s + m] += 0.045 * env * np.sin(2 * np.pi * f * x)
for k in range(int(T / beat)):
    s = int(k * beat * SR); m = int(0.25 * SR)
    if s + m > n: break
    x = np.arange(m) / SR; mus[s:s + m] += 0.28 * np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-x * 30)) / SR) * np.exp(-x * 14)
for a, b in S[1:]:
    s = int(max(0, a - 0.35) * SR); m = int(0.5 * SR)
    if s + m < n: mus[s:s + m] += 0.14 * np.convolve(rng.standard_normal(m), np.ones(30) / 30, 'same') * np.sin(np.linspace(0, np.pi, m)) ** 2
mus = mus / np.abs(mus).max() * 0.5
vo = np.zeros(n)
if os.path.exists(f'out/{name}_vo.wav'):
    with wave.open(f'out/{name}_vo.wav') as w: v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    vo[:min(n, len(v))] = v[:n]
envv = np.convolve(np.abs(vo), np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same'); duck = np.convolve(np.where(envv > 0.01, 0.25, 0.75), np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
clip = np.zeros(n)
for i, sc in enumerate(sp['scenes']):
    if sc.get('clip_audio') and P(sc['media']).lower().endswith(('.mp4', '.mov', '.webm', '.mkv')):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(sc.get('media_start', 0)), '-t', str(sc['dur']), '-i', P(sc['media']), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
        c = np.frombuffer(raw, np.int16).astype(np.float32) / 32768 * sc['clip_audio']; s = int(S[i][0] * SR); clip[s:s + len(c)] += c[:n - s]
mix = mus * duck + vo * 0.95 + clip; mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
with wave.open(f'out/{name}_mix.wav', 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 4. composite ----------
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'out/{name}_bg.mp4', '-framerate', str(FPS / step), '-i', f'{fd}/o%05d.png', '-i', f'out/{name}_mix.wav',
                '-filter_complex', f'[1:v]fps={FPS}[ov];[0:v][ov]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-map', '2:a', '-t', str(T),
                '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', f'out/{name}.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '1.0', '-i', f'out/{name}.mp4', '-frames:v', '1', '-q:v', '3', f'out/{name}-cover.jpg'])
print('done', name, T, os.path.getsize(f'out/{name}.mp4'))
