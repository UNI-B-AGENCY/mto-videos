import sys, json, os, subprocess, numpy as np, wave
from playwright.sync_api import sync_playwright
b=sys.argv[1]; meta=json.load(open(f'out/{b}.html.json')); T=meta['total']; FPS=30
fd=f'frames/{b}'; os.makedirs(fd,exist_ok=True)
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'file://'+os.path.abspath('out')+f'/{b}.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    for i in range(int(FPS*T)):
        pg.evaluate(f'setTime({i/FPS})'); pg.screenshot(path=f'{fd}/f{i:05d}.jpg',type='jpeg',quality=90)
    br.close()
# music: brand-specific tempo & chords
P={'ainewsreport':(118,[[146.8,174.6,220],[130.8,164.8,196],[116.5,146.8,174.6],[110,138.6,164.8]]),
   'ainewsround':(104,[[220,261.6,329.6],[174.6,220,261.6],[196,246.9,293.7],[164.8,207.7,246.9]]),
   'opportunities-to-apply':(112,[[261.6,329.6,392],[196,246.9,293.7],[220,261.6,329.6],[174.6,220,261.6]]),
   'afrotech':(100,[[196,246.9,293.7],[164.8,196,246.9],[130.8,164.8,196],[146.8,185,220]]),
   'cameroonbusinessreview':(92,[[174.6,220,261.6],[146.8,174.6,220],[196,233.1,293.7],[130.8,164.8,196]]),
   'marketpulseafrica':(96,[[220,261.6,329.6],[174.6,220,261.6],[130.8,164.8,196],[196,246.9,293.7]])}
BPM,ch=P[b]; SR=44100; beat=60/BPM; t=np.arange(int(SR*T))/SR; out=np.zeros_like(t); rng=np.random.default_rng(len(b))
bar=4*beat
for i in range(int(T/bar)+1):
    s=int(i*bar*SR)
    if s>=len(t): break
    n=min(int(bar*SR),len(t)-s); tt=np.arange(n)/SR; e=np.minimum(1,tt/0.3)*np.minimum(1,(n/SR-tt)/0.5)
    for f in ch[i%4]: out[s:s+n]+=0.045*e*(np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt))
    for k in range(8):  # arp
        a=s+int(k*beat/2*SR); m=int(beat/2*SR)
        if a+m>len(t): break
        ta=np.arange(m)/SR; f=ch[i%4][k%3]*2; out[a:a+m]+=0.03*np.sin(2*np.pi*f*ta)*np.exp(-ta*7)
    bf=ch[i%4][0]/2
    for k in range(4):
        a=s+int(k*beat*SR); m=int(beat*0.9*SR)
        if a+m>len(t): break
        tb=np.arange(m)/SR; out[a:a+m]+=0.09*np.sin(2*np.pi*bf*tb)*np.exp(-tb*3)
for k in range(int(T/beat)):
    s=int(k*beat*SR); n=int(0.25*SR)
    if s+n>len(t): break
    tk=np.arange(n)/SR; f=55+90*np.exp(-tk*30); out[s:s+n]+=0.32*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tk*14)
    if k%2==1:
        n2=int(0.12*SR); out[s:s+n2]+=0.08*rng.standard_normal(n2)*np.exp(-np.arange(n2)/SR*30)
    hs=s+int(beat/2*SR); hn=int(0.05*SR)
    if hs+hn<len(t): out[hs:hs+hn]+=0.035*rng.standard_normal(hn)*np.exp(-np.arange(hn)/SR*80)
for c in meta['cuts']:
    s=int((c-0.35)*SR); n=int(0.5*SR); nz=np.convolve(rng.standard_normal(n),np.ones(30)/30,'same'); out[s:s+n]+=0.14*nz*np.sin(np.linspace(0,np.pi,n))**2
# riser impact at start
n=int(0.4*SR); tk=np.arange(n)/SR; out[:n]+=0.4*np.sin(2*np.pi*45*tk)*np.exp(-tk*8)
fo=int(1.5*SR); out[-fo:]*=np.linspace(1,0,fo); out=out/np.max(np.abs(out))*0.7
vo=f'out/{b}_vo.wav'
if os.path.exists(vo):  # voice-over present: duck the music under it
    with wave.open(vo) as w: v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    v=np.pad(v,(0,max(0,len(out)-len(v))))[:len(out)]
    env=np.convolve(np.abs(v),np.ones(int(0.25*SR))/int(0.25*SR),'same'); duck=np.where(env>0.01,0.22,0.6)
    duck=np.convolve(duck,np.ones(int(0.3*SR))/int(0.3*SR),'same')
    out=out*duck+v*0.95; out=out/np.max(np.abs(out))*0.92
with wave.open(f'out/{b}.wav','w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{fd}/f%05d.jpg','-i',f'out/{b}.wav','-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p','-profile:v','high','-c:a','aac','-b:a','160k','-ar','44100','-shortest','-movflags','+faststart',f'out/{b}.mp4'],check=True)
print(b,'done',os.path.getsize(f'out/{b}.mp4'))
