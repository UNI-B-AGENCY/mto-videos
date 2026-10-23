import os
import sys, json
from playwright.sync_api import sync_playwright
from PIL import Image
b=sys.argv[1]; meta=json.load(open(f'out/{b}.html.json')); tot=meta['total']
cuts=[0]+meta['cuts']+[tot]; ts=[min(c2-0.3, c1+3.2) for c1,c2 in zip(cuts,cuts[1:])]
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'file://'+os.path.abspath('out')+f'/{b}.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    ims=[]
    for i,t in enumerate([0.05]+ts):
        pg.evaluate(f'setTime({t})'); f=f'out/{b}_snap{i}.jpg'; pg.screenshot(path=f,type='jpeg',quality=70); ims.append(Image.open(f).resize((360,640)))
    br.close()
sh=Image.new('RGB',(360*len(ims),640)); [sh.paste(im,(i*360,0)) for i,im in enumerate(ims)]; sh.save(f'out/{b}_sheet.jpg',quality=80)
