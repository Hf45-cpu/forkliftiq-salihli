# 90'lar Shorts — müzik + SFX sentezi ve miks
import json, subprocess, numpy as np
from scipy.io import wavfile
from scipy import signal

SR = 44100
VO = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/vo"
OUT = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/proj"
rng = np.random.default_rng(90)

# ---------- seslendirme + zaman çizelgesi ----------
lines = []
for i in range(8):
    sr, d = wavfile.read(f"{VO}/l{i}.wav")
    d = d.astype(np.float32) / 32768.0
    lines.append(d)
durs = [len(l) / SR for l in lines]
gaps = [1.4] * 6 + [1.8]
starts = [1.2]
for i in range(7):
    starts.append(starts[-1] + durs[i] + gaps[i])
TOTAL = round(starts[7] + durs[7] + 2.6, 2)
N = int(TOTAL * SR)
scene_starts = [0.0] + [s - 0.5 for s in starts[1:]]
json.dump({"starts": starts, "durs": durs, "scenes": scene_starts, "total": TOTAL},
          open(f"{OUT}/timeline.json", "w"), indent=1)
print("starts", [round(s, 2) for s in starts], "total", TOTAL)

def tN(t): return int(t * SR)

# voice chain: highpass, presence, gentle comp (ffmpeg)
vo = np.zeros(N, np.float32)
for i, l in enumerate(lines):
    a = tN(starts[i]); vo[a:a + len(l)] += l
wavfile.write(f"{OUT}/vo_raw.wav", SR, vo)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/vo_raw.wav", "-af",
    "highpass=f=85,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3.5,"
    "equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3.5:attack=8:release=120:makeup=4dB,"
    "aecho=0.8:0.5:35|60:0.12|0.07",
    f"{OUT}/vo_fx.wav"], check=True)
_, vo = wavfile.read(f"{OUT}/vo_fx.wav"); vo = vo.astype(np.float32)
if vo.ndim > 1: vo = vo.mean(1)
vo = vo[:N] if len(vo) >= N else np.pad(vo, (0, N - len(vo)))
if np.abs(vo).max() > 2: vo /= 32768.0

# ---------- yardımcılar ----------
def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.1, sus_len=None):
    a_n, d_n, r_n = int(a*SR), int(d*SR), int(r*SR)
    sl = (n - a_n - d_n - r_n) if sus_len is None else sus_len
    sl = max(sl, 0)
    e = np.concatenate([np.linspace(0, 1, a_n, endpoint=False), np.linspace(1, s, d_n, endpoint=False),
                        np.full(sl, s), np.linspace(s, 0, r_n)])
    return np.pad(e, (0, max(0, n - len(e))))[:n]

def saw(f, n, ph=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + ph) % 1.0) - 1

def sq(f, n, duty=0.5):
    t = np.arange(n) / SR
    return np.where(((f * t) % 1.0) < duty, 1.0, -1.0)

def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc, SR/2*0.95) / (SR/2), "low"); return signal.lfilter(b, a, x)
def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR/2), "high"); return signal.lfilter(b, a, x)
def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo/(SR/2), hi/(SR/2)], "band"); return signal.lfilter(b, a, x)

def add(buf, x, t, g=1.0):
    a = tN(t)
    if a >= len(buf): return
    if a < 0:
        x = x[-a:]; a = 0
    x = x[:len(buf) - a]
    if buf.ndim == 2 and x.ndim == 1: x = np.stack([x, x], 1)
    buf[a:a+len(x)] += g * x

def pan(x, p):  # p -1..1
    return np.stack([x * np.sqrt((1-p)/2), x * np.sqrt((1+p)/2)], 1)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)

# ---------- müzik ----------
BPM = 124; BEAT = 60 / BPM; BAR = 4 * BEAT
music = np.zeros((N, 2), np.float32)
drums = np.zeros((N, 2), np.float32)
T0 = starts[0]  # beat drop on first word
s = scene_starts
BREAK = (s[6], s[7])          # sokak lambası: breakdown
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G
roots = [45, 41, 48, 43]

def in_break(t): return BREAK[0] <= t < BREAK[1]

def kick():
    n = int(0.45*SR); t = np.arange(n)/SR
    f = 45 + 95*np.exp(-t*28); ph = 2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph) * np.exp(-t*7.5) + 0.25*np.exp(-t*300)*rng.standard_normal(n)) * 0.95
def clap():
    n = int(0.3*SR); t = np.arange(n)/SR
    nz = bp(rng.standard_normal(n), 900, 5000)
    e = np.exp(-t*22); e[:int(.01*SR)] *= 1.3
    return nz*e*0.55 + np.sin(2*np.pi*190*t)*np.exp(-t*30)*0.25
def hat(open_=False):
    n = int((0.22 if open_ else 0.06)*SR); t = np.arange(n)/SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t*(12 if open_ else 70)) * 0.28
K, C, H, HO = kick(), clap(), hat(), hat(True)

b = 0; t = T0 - 4*BEAT
while t < TOTAL - 1.0:
    beat_in_bar = b % 4
    if t >= T0 - 0.01:
        brk = in_break(t)
        if not brk:
            add(drums, K, t, 1.0)
            if beat_in_bar in (1, 3): add(drums, pan(C, 0.1), t, 0.9)
            add(drums, pan(H, 0.35), t + BEAT/2, 0.9)
            if b % 2 == 1: add(drums, pan(HO, -0.3), t + BEAT/2, 0.35)
            add(drums, pan(H, -0.2), t + BEAT*0.75, 0.35)
    b += 1; t += BEAT

# akorlar: supersaw pad + offbeat bas + arpej + piano stab
bar = 0; t = T0 - BAR
while t < TOTAL:
    ci = bar % 4; ch = chords[ci]
    n = int(BAR*SR)
    brk = in_break(t + 0.01)
    if t >= T0 - BAR:
        # pad
        pad = np.zeros((n, 2))
        for m in ch + [ch[0] + 12]:
            for k, det in enumerate(np.linspace(-0.18, 0.18, 5)):
                v = saw(mtof(m + det), n, rng.random())
                pad += pan(v, -0.8 + 0.4*k)
        pad[:, 0] = lp(pad[:, 0], 1800 if not brk else 900); pad[:, 1] = lp(pad[:, 1], 1800 if not brk else 900)
        pad *= env_adsr(n, a=0.08, d=0.2, s=0.85, r=0.15)[:, None] * 0.018
        add(music, pad, t, 1.0 if t >= T0 else 0.5)
    if t >= T0 - 0.01 and not brk:
        # offbeat bass (eurodance)
        for k in range(4):
            for sub, mm in ((0.5, 0), (0.75, 12 if k % 2 else 0)):
                nn = int(BEAT*0.24*SR); f = mtof(roots[ci] - 12 + mm)
                v = saw(f, nn) * 0.6 + sq(f/2, nn) * 0.4
                v = lp(v, 650) * env_adsr(nn, 0.003, 0.08, 0.5, 0.03)
                add(music, v, t + (k + sub)*BEAT, 0.33)
        # 16'lık arpej
        arp = ch + [ch[0] + 12, ch[1] + 12, ch[2], ch[1], ch[0] + 12]
        for k in range(16):
            nn = int(BEAT/4*0.9*SR); m = arp[k % len(arp)] + 12
            v = sq(mtof(m), nn, 0.25) * np.exp(-np.arange(nn)/SR*18)
            v = lp(v, 3200)
            p = 0.5 if k % 2 else -0.5
            tt = t + k*BEAT/4
            add(music, pan(v, p), tt, 0.055)
            add(music, pan(v, -p), tt + 3*BEAT/4, 0.022)   # delay
        # 90'lar house piyano stab (2. ve 4. vuruş offbeat)
        for k in (1.5, 3.5) if bar % 2 else (1.5,):
            nn = int(0.5*SR); tt = np.arange(nn)/SR; v = np.zeros(nn)
            for m in ch + [ch[0]+12]:
                f = mtof(m + 12)
                for h, ga in ((1, 1), (2, .45), (3, .2), (4, .12)):
                    v += ga*np.sin(2*np.pi*f*h*tt)*np.exp(-tt*(6+h*3))
            add(music, pan(v, 0.15), t + k*BEAT, 0.035)
    bar += 1; t += BAR

# outro: lead melodi
lead_notes = [(0, 76, 1), (1, 74, .5), (1.5, 72, .5), (2, 71, 1), (3, 72, 1), (4, 69, 2), (6, 67, .5), (6.5, 69, 1.5),
              (8, 72, 1), (9, 71, .5), (9.5, 72, .5), (10, 74, 1.5), (11.5, 76, .5), (12, 74, 2), (14, 71, 2)]
lt0 = T0 + np.ceil((s[7] - T0) / BAR) * BAR
for rep in range(2):
    for (bt, m, ln) in lead_notes:
        tt = lt0 + rep*16*BEAT + bt*BEAT
        if tt > TOTAL - 2: continue
        nn = int(ln*BEAT*SR); x = np.arange(nn)/SR
        vib = 1 + 0.004*np.sin(2*np.pi*5.5*x)
        v = sum(saw(mtof(m+d)*vib, nn) for d in (-0.1, 0, 0.1)) / 3
        v = lp(v, 2600) * env_adsr(nn, .01, .15, .7, .08)
        add(music, pan(v, 0.0), tt, 0.10); add(music, pan(v, 0.6), tt + 0.36, 0.04); add(music, pan(v, -0.6), tt + 0.72, 0.025)

# ---------- SFX ----------
sfx = np.zeros((N, 2), np.float32)
def noise(n): return rng.standard_normal(n)

def whoosh(dur=0.7, up=True):
    n = int(dur*SR); x = np.arange(n)/SR; out = np.zeros(n)
    nz = noise(n); seg = 512
    fc = np.linspace(400, 6000, n) if up else np.linspace(6000, 400, n)
    for i in range(0, n, seg):
        f = fc[i]; out[i:i+seg] = bp(nz[max(0, i-2048):i+seg], f*0.6, min(f*1.6, 20000))[-len(out[i:i+seg]):]
    e = np.sin(np.pi * np.clip(x/dur, 0, 1))**2
    return out*e*0.5
def impact():
    n = int(1.6*SR); x = np.arange(n)/SR
    f = 30 + 70*np.exp(-x*9); v = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2.2)
    v += lp(noise(n), 2500)*np.exp(-x*6)*0.35
    return v*0.9
def glitch(dur=0.25):
    n = int(dur*SR); x = np.arange(n)/SR
    v = sq(60 + 40*np.floor(x*40 % 5), n) * 0.3 + hp(noise(n), 2000)*0.4
    v *= (np.floor(x*60) % 2 > 0.5) * 0.5 + 0.5
    return v*np.exp(-x*6)*0.35
def click(g=0.6):
    n = int(0.03*SR); x = np.arange(n)/SR
    return (bp(noise(n), 1500, 7000)*np.exp(-x*300) + np.sin(2*np.pi*2200*x)*np.exp(-x*400))*g

# VHS açılış: kaset takma + mekanizma motoru + riser
add(sfx, pan(click(1.0), 0), 0.05); add(sfx, pan(click(0.8), 0), 0.12)
n = int(1.1*SR); x = np.arange(n)/SR
motor = (sq(55, n)*0.3 + saw(110 + 30*x, n)*0.2); motor = lp(motor, 800)*np.minimum(1, x*6)*np.exp(-np.maximum(0, x-0.8)*10)
add(sfx, pan(motor, 0), 0.15, 0.35)
r = whoosh(1.15, True); add(sfx, pan(r, 0), 0.05, 0.8)
add(sfx, pan(impact(), 0), T0 - 0.02, 1.0)
# rewind squeal intro
n = int(0.9*SR); x = np.arange(n)/SR
sq_ = np.sin(2*np.pi*np.cumsum(1200 + 900*x + 120*np.sin(2*np.pi*13*x))/SR) * 0.12 * np.sin(np.pi*x/0.9)
add(sfx, pan(sq_, 0.2), 0.2, 0.6)

# sahne geçişleri
for i in range(1, 8):
    add(sfx, pan(whoosh(0.6, i % 2 == 0), -0.3 if i % 2 else 0.3), s[i] - 0.3, 0.75)
    add(sfx, pan(glitch(), 0), s[i] - 0.05, 0.8)
add(sfx, pan(impact(), 0), s[7], 0.8)

# sahne 1: kaset — kapak tık + kalemle sarma (tırtıklı plastik + bant sesi)
add(sfx, pan(click(0.9), -0.2), s[1] + 0.25)
for k in range(30):
    tt = starts[1] + 2.4 + k*0.115
    if tt > starts[1] + durs[1] - 0.2: break
    add(sfx, pan(click(0.28) , 0.25), tt)
n = int(3.2*SR); x = np.arange(n)/SR
tape = bp(noise(n), 1500, 4500) * (0.5 + 0.5*np.sin(2*np.pi*8.7*x)**2) * np.sin(np.pi*x/3.2) * 0.12
add(sfx, pan(tape, 0.2), starts[1] + 2.4)

# sahne 2: TV karıncası + "Tamam!" anında düzelme
tamam = starts[2] + durs[2] * (79/105) - 0.35
n = int((tamam - s[2])*SR); x = np.arange(n)/SR
st = hp(noise(n), 300) * (0.75 + 0.25*np.sin(2*np.pi*2.3*x)) * 0.11
st *= np.minimum(1, x*8)
add(sfx, pan(st, 0), s[2])
add(sfx, pan(click(1.0), 0), tamam)
n = int(0.6*SR); x = np.arange(n)/SR
add(sfx, pan(np.sin(2*np.pi*1000*x)*env_adsr(n, .01, .05, .8, .2)*0.08, 0), tamam + 0.05)
# anten ayarlarken kısa cızırtı varyasyonları
n = int(0.5*SR)
for k in range(3):
    add(sfx, pan(hp(noise(n), 1500)*np.hanning(n)*0.12, (-1)**k*0.5), s[2] + 2.3 + k*1.1)

# sahne 3: telefon — kart takma, DTMF tuşlar, kontör bip geri sayımı
add(sfx, pan(click(0.9), 0), s[3] + 0.55); add(sfx, pan(click(0.7), 0), s[3] + 0.62)
dtmf = {'0': (941, 1336), '2': (697, 1336), '1': (697, 1209), '5': (770, 1336), '3': (697, 1477), '6': (770, 1477), '9': (852, 1477)}
for k, d in enumerate("0232615"):
    lo_, hi_ = dtmf[d]; n = int(0.11*SR); x = np.arange(n)/SR
    v = (np.sin(2*np.pi*lo_*x) + np.sin(2*np.pi*hi_*x)) * 0.5 * env_adsr(n, .003, .01, 1, .01) * 0.12
    add(sfx, pan(v, 0.3), s[3] + 0.9 + k*0.17)
for k in range(6):
    n = int(0.08*SR); x = np.arange(n)/SR
    add(sfx, pan(np.sin(2*np.pi*1400*x)*env_adsr(n, .002, .01, 1, .01)*0.09, -0.2), starts[3] + 2.6 + k*0.42)

# sahne 4: disket sürücü — kafa arama "grr grr"
for k, (tt, ln) in enumerate([(0.35, 0.35), (0.85, 0.22), (1.2, 0.5), (1.9, 0.18), (2.2, 0.4)]):
    n = int(ln*SR); x = np.arange(n)/SR
    f = 95 if k % 2 else 130
    v = sq(f, n, 0.3) * 0.5 + bp(noise(n), 600, 2400) * 0.5
    v = bp(v, 150, 3500) * env_adsr(n, .005, .02, .9, .03) * 0.13
    add(sfx, pan(v, 0.4), s[4] + tt)
    for c in range(int(ln*25)): add(sfx, pan(click(0.12), 0.4), s[4] + tt + c/25)

# sahne 5: sanal bebek — acıkma alarmı
for k in range(8):
    n = int(0.07*SR); x = np.arange(n)/SR
    f = 2800 if k % 2 == 0 else 2100
    add(sfx, pan(sq(f, n)*env_adsr(n, .002, .01, 1, .01)*0.06, 0.3), starts[5] + 0.4 + k*0.1 + (k//4)*0.35)
for k in range(4):
    n = int(0.05*SR)
    add(sfx, pan(sq(1600 + 400*k, n)*0.05, -0.3), starts[5] + durs[5] - 0.6 + k*0.07)

# sahne 6: akşam — cırcır böceği + lamba yanma (tık + vızıltı)
n = int((s[7] - s[6] + 0.6)*SR); x = np.arange(n)/SR
cr = np.sin(2*np.pi*4400*x) * (np.sin(2*np.pi*28*x) > 0.3) * (np.sin(2*np.pi*1.6*x) > -0.2) * 0.018
cr2 = np.sin(2*np.pi*5100*x) * (np.sin(2*np.pi*31*x + 1) > 0.4) * (np.sin(2*np.pi*1.1*x + 2) > 0) * 0.012
amb = (cr + cr2) * np.minimum(1, x*2) * np.minimum(1, (x[-1]-x)*3)
add(sfx, np.stack([amb, np.roll(amb, 900)], 1), s[6])
yan = starts[6] + durs[6] * (25/44) - 0.25
for k, dt in enumerate((0, 0.12, 0.2, 0.55)):
    add(sfx, pan(click(0.6), [-0.5, 0.5, -0.2, 0.3][k]), yan + dt)
n = int(2.0*SR); x = np.arange(n)/SR
buzz = lp(saw(100, n), 1200) * np.exp(-x*1.5) * 0.04
add(sfx, pan(buzz, 0), yan)

# final: tape stop
music_t = music + drums

# ---------- miks ----------
# ducking: VO zarfı
envv = np.abs(vo)
envv = signal.lfilter([1 - np.exp(-1/(0.03*SR))], [1, -np.exp(-1/(0.03*SR))], envv)
envv = envv / (envv.max() + 1e-9)
duck = 1 - 0.55*np.clip(envv*4, 0, 1)
duck = signal.lfilter([1 - np.exp(-1/(0.12*SR))], [1, -np.exp(-1/(0.12*SR))], duck)
music_t *= duck[:, None]
# kick sidechain pump on pad (90'lar house hissi)
music_t = np.tanh(music_t * 1.3) / 1.3

mix = music_t * 0.85 + sfx * 0.9 + np.stack([vo, vo], 1) * 1.15
# tape stop at end
stop_len = int(0.9 * SR); a = N - int(1.6*SR)
seg = mix[a:a+stop_len].copy()
speed = np.linspace(1, 0.05, stop_len); pos = np.cumsum(speed); pos = pos[pos < stop_len - 1]
ts = np.stack([np.interp(pos, np.arange(stop_len), seg[:, c]) for c in range(2)], 1) * np.linspace(1, 0, len(pos))[:, None]
mix[a:] = 0; mix[a:a+len(ts)] = ts
# baştaki VHS tıslaması (tüm video boyunca hafif)
hiss = hp(noise(N), 6000) * 0.006
mix += np.stack([hiss, np.roll(hiss, 333)], 1)
mix /= np.abs(mix).max() * 1.05
wavfile.write(f"{OUT}/mix_pre.wav", SR, (mix * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/mix_pre.wav", "-af",
                "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", f"{OUT}/mix.wav"], check=True)
print("ok", TOTAL)
