import json, sys, os, html
FS = os.environ.get('MTO_FONTS', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_modules/@fontsource'))

def fontfaces(fam):
    out = []
    for w in (500, 600, 700, 800, 900):
        p = f'{FS}/{fam}/files/{fam}-latin-{w}-normal.woff2'
        if os.path.exists(p):
            out.append(f"@font-face{{font-family:F;src:url(file://{p});font-weight:{w}}}")
    return '\n'.join(out)

def esc(s):
    return s  # specs contain trusted inline html (<b>, <span class=a>)

def scene_html(i, sc, th):
    t = sc['type']; at = lambda x: f'data-at="{x}"'
    h = []
    top = sc.get('top', 700)
    h.append(f'<div class="scene" id="s{i}"><div class="inner" style="top:{top}px">')
    if sc.get('kicker'):
        h.append(f'<div class="kick" {at(0.1)}>{esc(sc["kicker"])}</div>')
    if sc.get('head'):
        fs = sc.get('fs', th.get('hfs', 92))
        h.append(f'<div class="h" style="font-size:{fs}px" {at(sc.get("head_at",0.25))}>{esc(sc["head"])}</div>')
    if t == 'hook' and 'count' in sc:
        c = sc['count']
        h.append(f'<div class="big" style="font-size:{c.get("fs",220)}px" data-at="{c.get("at",0.6)}" data-count="{c["to"]}" data-from="{c.get("from",0)}" data-dec="{c.get("dec",0)}" data-pre="{c.get("pre","")}" data-suf="{c.get("suf","")}" data-dur="{c.get("dur",1.6)}">{c.get("pre","")}0{c.get("suf","")}</div>')
        if c.get('label'):
            h.append(f'<div class="p" {at(c.get("at",0.6)+0.4)}>{esc(c["label"])}</div>')
    if t in ('text', 'hook'):
        for j, line in enumerate(sc.get('lines', [])):
            h.append(f'<div class="p" {at(sc.get("lat",1.2)+j*sc.get("lstep",1.0))}>{esc(line)}</div>')
    if t == 'stats':
        h.append('<div class="stats">')
        for j, s in enumerate(sc['items']):
            cnt = ''
            if 'count' in s:
                c = s['count']
                cnt = f'data-count="{c["to"]}" data-from="0" data-dec="{c.get("dec",0)}" data-pre="{c.get("pre","")}" data-suf="{c.get("suf","")}" data-dur="1.0" data-cat="{0.6+j*sc.get("step",0.9)}"'
            h.append(f'<div class="stat" {at(0.6+j*sc.get("step",0.9))}><div class="sv" {cnt}>{esc(s["v"])}</div><div class="sl">{esc(s["l"])}</div></div>')
        h.append('</div>')
    if t == 'list':
        h.append('<div class="list">')
        for j, s in enumerate(sc['items']):
            mark = sc.get('mark', 'num')
            m = str(j+1) if mark == 'num' else ('&#10003;' if mark == 'check' else '&#8226;')
            h.append(f'<div class="li" {at(0.7+j*sc.get("step",0.8))}><div class="lm">{m}</div><div class="lt">{esc(s)}</div></div>')
        h.append('</div>')
    if t == 'bars':
        mx = max(b['v'] for b in sc['items'])
        h.append('<div class="bars">')
        for j, b in enumerate(sc['items']):
            cls = ' hl' if b.get('hl') else ''
            h.append(f'<div class="brow{cls}" {at(0.5+j*0.35)}><div class="bl">{esc(b["l"])}</div><div class="btrack"><div class="bfill" data-w="{b["v"]/mx*100:.1f}" data-wat="{0.6+j*0.35}"></div></div><div class="bv">{esc(b["d"])}</div></div>')
        h.append('</div>')
    if t == 'versus':
        L, R = sc['left'], sc['right']
        h.append(f'<div class="vs"><div class="vcol l" {at(0.6)}><div class="vt">{esc(L["t"])}</div><div class="vv">{esc(L["v"])}</div><div class="vd">{esc(L.get("d",""))}</div></div>'
                 f'<div class="varr" {at(1.2)}>&#8594;</div>'
                 f'<div class="vcol r" {at(1.6)}><div class="vt">{esc(R["t"])}</div><div class="vv">{esc(R["v"])}</div><div class="vd">{esc(R.get("d",""))}</div></div></div>')
        if sc.get('note'):
            h.append(f'<div class="p" {at(2.4)}>{esc(sc["note"])}</div>')
    if t == 'cta':
        h.append(f'<div class="ctalogo" {at(0.1)}><img src="{th["logo"]}"></div>')
        h.append(f'<div class="h" style="font-size:{sc.get("fs",80)}px;text-align:center" {at(0.4)}>{esc(sc["q"])}</div>')
        h.append(f'<div class="p" style="text-align:center" {at(1.0)}>{esc(sc.get("sub","Tell us in the comments &#8595;"))}</div>')
        h.append(f'<div style="text-align:center"><div class="kick url" {at(1.6)}>{esc(sc["url"])}</div></div>')
        if sc.get('follow'):
            h.append(f'<div class="p small" style="text-align:center" {at(2.2)}>{esc(sc["follow"])}</div>')
    h.append('</div></div>')
    return '\n'.join(h)

def build(spec):
    th = spec['theme']
    scenes = spec['scenes']
    t = 0; S = []
    for i, sc in enumerate(scenes):
        S.append([f's{i}', t, t + sc['dur']]); t += sc['dur']
    total = t
    body = '\n'.join(scene_html(i, sc, th) for i, sc in enumerate(scenes))
    css = open(os.path.join(os.path.dirname(__file__), 'base.css')).read()
    for k, v in th['vars'].items():
        css = css.replace('{' + k + '}', v)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fontfaces(th.get('font','montserrat'))}
{css}
{th.get('extra_css','')}
</style></head><body class="{th.get('cls','')}"><div id="stage">
<div id="photo" style="background-image:url({th['bg']})"></div><div id="shade"></div><div id="grid"></div>
<div id="prog"></div>
<div class="top"><div class="logo"><img src="{th['logo']}"></div><div class="brand">{th['name']}<small>{th['tag']}</small></div></div>
{body}
<div class="foot" id="foot">{spec.get('source','')}</div>
</div>
<script>
const S={json.dumps(S)}; const TOTAL={total};
const ease=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const back=x=>{{x=x<0?0:x>1?1:x;const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);}};
const cl=(x,a,b)=>Math.max(a,Math.min(b,x));
function fmt(v,dec){{return v.toLocaleString('en-US',{{minimumFractionDigits:dec,maximumFractionDigits:dec}});}}
window.setTime=function(t){{
  document.getElementById('prog').style.width=(t/TOTAL*1080)+'px';
  const ph=document.getElementById('photo');
  ph.style.transform=`scale(${{1.08+t*0.006}}) translate(${{Math.sin(t*0.2)*14}}px,${{-t*2.5}}px)`;
  for(const [id,a,b] of S){{
    const e=document.getElementById(id); const loc=t-a;
    const vis=t>=a-0.001&&t<b+0.4;
    const out=ease((b-t)/0.3); const inn= a===0?1:ease(loc/0.35);
    e.style.opacity=vis?Math.min(inn,t<b?1:0)*1:0; if(t>=b) e.style.opacity=0;
    e.style.transform=`translateY(${{(1-(a===0?1:ease(loc/0.4)))*70}}px)`;
    if(!vis) continue;
    const lo=a===0?loc+0.75:loc;
    e.querySelectorAll('[data-at]').forEach(el=>{{const k=back((lo-parseFloat(el.dataset.at))/0.5);const k2=ease((lo-parseFloat(el.dataset.at))/0.4);
      el.style.opacity=k2; el.style.transform=`translateY(${{(1-k)*50}}px) scale(${{0.94+0.06*k}})`;}});
    e.querySelectorAll('[data-count]').forEach(el=>{{const st=parseFloat(el.dataset.cat||el.dataset.at);const k=ease((loc-st)/parseFloat(el.dataset.dur));
      const v=parseFloat(el.dataset.from)+(parseFloat(el.dataset.count)-parseFloat(el.dataset.from))*k;
      el.textContent=el.dataset.pre+fmt(v,parseInt(el.dataset.dec))+el.dataset.suf;}});
    e.querySelectorAll('[data-w]').forEach(el=>{{const k=ease((loc-parseFloat(el.dataset.wat))/0.9);el.style.width=(k*parseFloat(el.dataset.w))+'%';}});
    const lg=e.querySelector('.ctalogo'); if(lg){{const k=back(loc/0.7); lg.style.transform=`scale(${{0.5+0.5*k}}) rotate(${{(1-k)*-40}}deg)`;}}
  }}
  document.getElementById('foot').style.opacity=(t>S[0][2]&&t<S[S.length-1][1])?1:0;
}};
setTime(0);
</script></body></html>"""
    return page, total, [s[1] for s in S[1:]]

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    page, total, cuts = build(spec)
    out = sys.argv[2]
    open(out, 'w').write(page)
    json.dump({'total': total, 'cuts': cuts}, open(out + '.json', 'w'))
    print(total, cuts)
