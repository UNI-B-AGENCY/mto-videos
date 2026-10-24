"""Render every jobs/<id>.json (queued by a content run through the hub) on the GitHub runner.
Job JSON = a story.py spec plus:
  "brand": "afrotech", "slug": "2026-10-24-yaounde-data", "audio_url": "<ElevenLabs content_url>", "tempo": 1.08,
  each scene: "media_url": "<image or video URL>" (downloaded here; any public URL works) and optional "media_start".
  optional "mode": "clip" + "clip_url" + "credit_short" to use clip.py instead.
Result: videos/<brand>/<slug>.mp4 + -cover.jpg, and jobs/done/<id>.json {"ok":true,"video":raw_url,"cover":raw_url,"duration":s}
or jobs/done/<id>.json {"ok":false,"error":"..."}; the job file is removed either way."""
import json, os, glob, subprocess, traceback, urllib.request, shutil
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); V = os.path.join(ROOT, 'tools', 'video')
RAW = 'https://raw.githubusercontent.com/UNI-B-AGENCY/mto-videos/main/'
os.makedirs(os.path.join(ROOT, 'jobs', 'done'), exist_ok=True)
def get(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (mto-video-renderer)'})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f: shutil.copyfileobj(r, f)
    if os.path.getsize(path) < 1000: raise RuntimeError(f'download too small: {url}')
for jp in sorted(glob.glob(os.path.join(ROOT, 'jobs', '*.json'))):
    jid = os.path.basename(jp)[:-5]; res = {'ok': False}
    try:
        job = json.load(open(jp)); brand = job['brand']; slug = job['slug']
        work = os.path.join(V, 'work', jid); os.makedirs(work, exist_ok=True)
        for i, sc in enumerate(job['scenes']):
            u = sc.get('media_url')
            if u:
                ext = '.mp4' if any(x in u.lower() for x in ('.mp4', '.mov', '.webm')) else '.jpg'
                p = os.path.join(work, f'm{i}{ext}'); get(u, p); sc['media'] = p
            elif sc.get('media') and not os.path.isabs(sc['media']):
                sc['media'] = os.path.join(ROOT, sc['media'])
        if not job['theme']['logo'].startswith('/'): job['theme']['logo'] = os.path.join(V, job['theme']['logo'])
        job['name'] = jid
        a = os.path.join(work, 'voice.mp3'); get(job['audio_url'], a)
        sp = os.path.join(work, 'spec.json'); json.dump(job, open(sp, 'w'))
        os.makedirs(os.path.join(V, 'out'), exist_ok=True)
        subprocess.run(['python3', 'vo.py', sp, a, f'out/{jid}_vo.wav', str(job.get('tempo', 1.08))], cwd=V, check=True)
        subprocess.run(['python3', 'story.py', sp], cwd=V, check=True, env={**os.environ, 'OVL_STEP': '2'})
        d = os.path.join(ROOT, 'videos', brand); os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(V, 'out', f'{jid}.mp4'), os.path.join(d, f'{slug}.mp4'))
        shutil.copy(os.path.join(V, 'out', f'{jid}-cover.jpg'), os.path.join(d, f'{slug}-cover.jpg'))
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(d, f'{slug}.mp4')], capture_output=True, text=True).stdout or 0)
        res = {'ok': True, 'video': RAW + f'videos/{brand}/{slug}.mp4', 'cover': RAW + f'videos/{brand}/{slug}-cover.jpg', 'duration': round(dur, 1)}
    except Exception as e:
        res = {'ok': False, 'error': f'{type(e).__name__}: {e}', 'trace': traceback.format_exc()[-1500:]}
    json.dump(res, open(os.path.join(ROOT, 'jobs', 'done', jid + '.json'), 'w'), indent=1)
    os.remove(jp); print(jid, res.get('ok'), res.get('error', res.get('video')))
shutil.rmtree(os.path.join(V, 'work'), ignore_errors=True); shutil.rmtree(os.path.join(V, 'out'), ignore_errors=True)
