# Chatterbox seslendirmesini sahnelere oturt, işle, müziği duck et, miksle
import json, subprocess, numpy as np, librosa, soundfile as sf
from scipy import signal
P = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad"
OUT = f"{P}/proj3"; TTS = f"{P}/tts/out"
SR = 44100
L = json.load(open(f"{OUT}/narration.json")); TL = json.load(open(f"{OUT}/timeline.json"))
N = int(TL["total"] * SR); vo = np.zeros(N)
starts = [l["start"] for l in L]
starts[0] = 0.3; starts[8] = 49.1
limits = []
for i, l in enumerate(L):
    end = starts[i + 1] - 0.12 if i + 1 < len(L) else TL["total"] - 0.3
    if i == 5: end = TL["fire"] - 0.2          # top atışından önce bitmeli
    if i == 8: end = 54.45
    limits.append(end - starts[i])
report = []
for i, l in enumerate(L):
    y, sr = librosa.load(f"{TTS}/n{i}.wav", sr=SR)
    y, _ = librosa.effects.trim(y, top_db=38)
    d = len(y) / SR; tempo = max(1.0, d / limits[i])
    if tempo > 1.0:
        sf.write(f"{OUT}/_t.wav", y, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/_t.wav", "-af", f"rubberband=tempo={min(tempo, 1.22):.4f}:pitchq=quality", f"{OUT}/_t2.wav"], check=True)
        y, _ = librosa.load(f"{OUT}/_t2.wav", sr=SR)
    a = int(starts[i] * SR); y = y[:N - a]; vo[a:a + len(y)] += y
    report.append((i, round(d, 2), round(len(y) / SR, 2), round(limits[i], 2), round(tempo, 3)))
for r in report: print("line", r[0], "raw", r[1], "final", r[2], "limit", r[3], "tempo", r[4], "FITS" if r[2] <= r[3] + .05 else "OVER")
sf.write(f"{OUT}/vo_raw.wav", vo.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/vo_raw.wav", "-af",
    "highpass=f=80,equalizer=f=160:t=q:w=1:g=2,equalizer=f=300:t=q:w=1:g=-2,equalizer=f=3000:t=q:w=1.2:g=3,"
    "acompressor=threshold=-22dB:ratio=4:attack=6:release=120:makeup=5dB,aecho=0.8:0.6:40|70:0.10|0.06",
    "-ar", str(SR), f"{OUT}/vo_fx.wav"], check=True)
vo, _ = sf.read(f"{OUT}/vo_fx.wav"); vo = vo if vo.ndim == 1 else vo.mean(1); vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
bed, _ = sf.read(f"{OUT}/mix_pre.wav"); bed = bed[:N]
env = np.abs(vo); a1 = np.exp(-1 / (.03 * SR)); env = signal.lfilter([1 - a1], [1, -a1], env); env /= env.max() + 1e-9
duck = 1 - .62 * np.clip(env * 4, 0, 1); a2 = np.exp(-1 / (.15 * SR)); duck = signal.lfilter([1 - a2], [1, -a2], duck)
mix = bed * duck[:, None] * .55 + np.stack([vo, vo], 1) * 1.25
mix /= np.abs(mix).max() * 1.05
sf.write(f"{OUT}/mix_vo_pre.wav", mix.astype(np.float32), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/mix_vo_pre.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", f"{OUT}/mix_vo.wav"], check=True)
m = np.sqrt(np.mean((bed[:, 0] * duck * .55)[np.abs(vo) > .03] ** 2)); v = np.sqrt(np.mean((vo * 1.25)[np.abs(vo) > .03] ** 2))
print("music under voice dB:", round(20 * np.log10(m / v), 1))
