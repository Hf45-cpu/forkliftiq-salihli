# Ses tınısı şekillendirme: WORLD ile perde ortalaması + tonlama genişliği, ardından netlik
import sys, numpy as np, librosa, soundfile as sf, pyworld as pw
from scipy import signal
src, dst = sys.argv[1], sys.argv[2]; TARGET = float(sys.argv[3]) if len(sys.argv) > 3 else 140; SPREAD = float(sys.argv[4]) if len(sys.argv) > 4 else 1.7
y, sr = librosa.load(src, sr=44100); y = y.astype(np.float64)
f0, t = pw.harvest(y, sr, f0_floor=60, f0_ceil=400, frame_period=5)
sp = pw.cheaptrick(y, f0, t, sr); ap = pw.d4c(y, f0, t, sr)
v = f0 > 0; lf = np.log(f0[v]); m = np.median(lf)
lf2 = np.log(TARGET) + (lf - m) * SPREAD           # ortalamayı hedefe taşı, sapmayı genişlet
f0n = f0.copy(); f0n[v] = np.exp(lf2)
out = pw.synthesize(f0n, sp, ap, sr, frame_period=5)
# netlik: 3-6 kHz harmonik heyecanlandırıcı + yüksek raf
b, a = signal.butter(2, 3000/(sr/2), 'high'); hi = signal.lfilter(b, a, out); exc = np.tanh(hi*4)/4
out = out + exc*0.6
sf.write(dst, (out/np.abs(out).max()*.9).astype(np.float32), sr)
