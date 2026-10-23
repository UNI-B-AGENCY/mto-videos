"""Fit a spec's scene durations to an ElevenLabs voice-over.
Usage: python3 vo.py specs/<brand>.json <voice.mp3> out/<brand>_vo.wav [tempo]
The voice-over script must put <break time="1.6s" /> between scenes (one segment per scene).
Writes the new durations back into the spec JSON and a voice track aligned to the scenes."""
import sys, json, re, subprocess, numpy as np
spec_p, mp3, out_wav = sys.argv[1:4]; tempo = float(sys.argv[4]) if len(sys.argv) > 4 else 1.12
SR = 44100
spec = json.load(open(spec_p)); n = len(spec['scenes'])
log = subprocess.run(['ffmpeg', '-i', mp3, '-af', 'silencedetect=noise=-38dB:d=1.2', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', log)]; en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', log)]
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-af', f'atempo={tempo}', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
total = len(a) / SR
cuts = [(0.0, st[0])] + [(en[i], st[i + 1]) for i in range(len(st) - 1)] + [(en[-1], total * tempo)] if st else [(0, total * tempo)]
if len(cuts) != n:
    sys.exit(f'voice has {len(cuts)} segments but spec has {n} scenes - add/remove breaks')
LEAD, GAP = 0.12, 0.35
out = []
for i, (s, e) in enumerate(cuts):
    s2, e2 = max(0, s / tempo - 0.05), min(total, e / tempo + 0.08)
    seg = a[int(s2 * SR):int(e2 * SR)]
    tail = 1.6 if i == n - 1 else GAP
    dur = round(LEAD + len(seg) / SR + tail, 2)
    spec['scenes'][i]['dur'] = max(dur, 2.4)
    buf = np.zeros(int(spec['scenes'][i]['dur'] * SR), np.float32); buf[int(LEAD * SR):int(LEAD * SR) + len(seg)] = seg
    out.append(buf)
v = np.concatenate(out); v = v / max(1e-6, np.abs(v).max()) * 0.95
import wave
with wave.open(out_wav, 'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((v * 32767).astype(np.int16).tobytes())
json.dump(spec, open(spec_p, 'w'), indent=1)
print('scene durations', [s['dur'] for s in spec['scenes']], 'total', round(len(v) / SR, 2))
