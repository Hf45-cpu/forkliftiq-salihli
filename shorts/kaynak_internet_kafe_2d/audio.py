# Kaybolan Meslekler: KAPICI — müzik + SFX sentezi ve miks
import json, subprocess, numpy as np
from scipy.io import wavfile
from scipy import signal

SR = 44100
BASE = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad"
VO, OUT = f"{BASE}/vo7", f"{BASE}/p7"
rng = np.random.default_rng(7)
MUSIC_GAIN = 0.42      # önceki videoda 0.85 idi -> müzik belirgin şekilde kısık
DUCK_DEPTH = 0.68      # konuşma altında daha derin kısma

lines = []
for i in range(8):
    _, d = wavfile.read(f"{VO}/l{i}.wav"); lines.append(d.astype(np.float32) / 32768.0)
durs = [len(l) / SR for l in lines]
gaps = [1.1, 1.1, 1.1, 1.1, 1.1, 1.3, 0.7]
starts = [0.9]
for i in range(7): starts.append(starts[-1] + durs[i] + gaps[i])
TOTAL = round(starts[7] + durs[7] + 2.6, 2)
N = int(TOTAL * SR)
scenes = [0.0] + [starts[i] - 0.4 for i in range(1, 7)]
json.dump({"starts": starts, "durs": durs, "scenes": scenes, "total": TOTAL}, open(f"{OUT}/timeline.json", "w"), indent=1)
print("starts", [round(s, 2) for s in starts], "total", TOTAL)
caps = json.load(open(f"{OUT}/captions.json"))
SUB = next(c["t0"] for c in caps if "ABONE" in c["text"])      # abone ol anı
PRESS = SUB + 0.55
HOOK = next(c["t0"] for c in caps if 'KALDI' in c["text"])

def tN(t): return int(t * SR)
vo = np.zeros(N, np.float32)
for i, l in enumerate(lines): vo[tN(starts[i]):tN(starts[i]) + len(l)] += l
wavfile.write(f"{OUT}/vo_raw.wav", SR, vo)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/vo_raw.wav", "-af",
    "highpass=f=85,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3.5,equalizer=f=9000:t=q:w=1:g=2,"
    "acompressor=threshold=-20dB:ratio=3.5:attack=8:release=120:makeup=4dB,aecho=0.8:0.5:35|60:0.12|0.07",
    f"{OUT}/vo_fx.wav"], check=True)
_, vo = wavfile.read(f"{OUT}/vo_fx.wav"); vo = vo.astype(np.float32)
if vo.ndim > 1: vo = vo.mean(1)
if np.abs(vo).max() > 2: vo /= 32768.0
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]

def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.1):
    a_n, d_n, r_n = int(a*SR), int(d*SR), int(r*SR); sl = max(n - a_n - d_n - r_n, 0)
    e = np.concatenate([np.linspace(0, 1, a_n, endpoint=False), np.linspace(1, s, d_n, endpoint=False), np.full(sl, s), np.linspace(s, 0, r_n)])
    return np.pad(e, (0, max(0, n - len(e))))[:n]
def saw(f, n, ph=0.0): return 2 * ((f * np.arange(n) / SR + ph) % 1.0) - 1
def sq(f, n, duty=0.5): return np.where(((f * np.arange(n) / SR) % 1.0) < duty, 1.0, -1.0)
def lp(x, fc, o=2): b, a = signal.butter(o, min(fc, SR/2*.95)/(SR/2), "low"); return signal.lfilter(b, a, x)
def hp(x, fc, o=2): b, a = signal.butter(o, fc/(SR/2), "high"); return signal.lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = signal.butter(o, [lo/(SR/2), hi/(SR/2)], "band"); return signal.lfilter(b, a, x)
def add(buf, x, t, g=1.0):
    a = tN(t)
    if a >= len(buf): return
    if a < 0: x = x[-a:]; a = 0
    x = x[:len(buf) - a]
    if buf.ndim == 2 and x.ndim == 1: x = np.stack([x, x], 1)
    buf[a:a+len(x)] += g * x
def pan(x, p): return np.stack([x*np.sqrt((1-p)/2), x*np.sqrt((1+p)/2)], 1)
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def noise(n): return rng.standard_normal(n)

# ---------- müzik: 100 BPM nostaljik, armonik minör ----------
BPM = 100; BEAT = 60/BPM; BAR = 4*BEAT; T0 = starts[0]
music = np.zeros((N, 2), np.float32)
chords = [[57, 60, 64], [50, 53, 57], [52, 56, 59], [57, 60, 64]]   # Am Dm E Am
roots = [45, 38, 40, 45]
BREAK = (starts[5] + durs[5]*0.55, scenes[6])       # "Ama hiçbiri..." duygusal an
def in_break(t): return BREAK[0] <= t < BREAK[1]

def kick():
    n = int(.4*SR); t = np.arange(n)/SR; f = 48 + 80*np.exp(-t*25)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)*.9
def snap():
    n = int(.25*SR); t = np.arange(n)/SR; return bp(noise(n), 1200, 6000)*np.exp(-t*28)*.45
def shaker():
    n = int(.08*SR); t = np.arange(n)/SR; return hp(noise(n), 6000)*np.sin(np.pi*t/.08)*.16
K, SN, SH = kick(), snap(), shaker()
b = 0; t = T0
while t < TOTAL - 1:
    if not in_break(t):
        if b % 4 in (0,) or (b % 8 == 6): add(music, K, t, .9)
        if b % 4 in (1, 3): add(music, pan(SN, .1), t, .8)
        for k in (0, .5): add(music, pan(SH, .4 if k else -.4), t + k*BEAT, .8)
    b += 1; t += BEAT
bar = 0; t = T0 - BAR
while t < TOTAL:
    ci = bar % 4; ch = chords[ci]; n = int(BAR*SR); brk = in_break(t + .01)
    # sıcak pad (yavaş atak)
    pad = np.zeros((n, 2))
    for m in ch + [ch[0]+12]:
        for k, det in enumerate(np.linspace(-.12, .12, 4)): pad += pan(saw(mtof(m+det), n, rng.random()), -.6 + .4*k)
    pad[:, 0] = lp(pad[:, 0], 1400); pad[:, 1] = lp(pad[:, 1], 1400)
    add(music, pad * env_adsr(n, .25, .2, .85, .3)[:, None] * .016, t, 1.0 if t >= T0 else .5)
    if t >= T0 - .01:
        # bağlama/saz benzeri pluck arpej (Karplus-Strong)
        arp = [ch[0]+12, ch[2]+12, ch[1]+12, ch[2]+12, ch[0]+24, ch[2]+12, ch[1]+12, ch[2]]
        for k in range(8):
            f = mtof(arp[k]); P = int(SR/f); nn = int(BEAT*.5*SR*1.6)
            buf = noise(P)*.5; out = np.zeros(nn)
            for i in range(nn):
                out[i] = buf[i % P]; buf[i % P] = .5*(buf[i % P] + buf[(i+1) % P])*.996
            out = hp(out, 150)
            add(music, pan(out, .35 if k % 2 else -.35), t + k*BEAT/2, .16 if not brk else .2)
        if not brk:
            for k in range(4):   # yumuşak bas
                nn = int(BEAT*.8*SR); v = lp(saw(mtof(roots[ci]-12), nn)*.5 + np.sin(2*np.pi*mtof(roots[ci]-12)*np.arange(nn)/SR), 400)
                add(music, v*env_adsr(nn, .01, .2, .6, .1), t + k*BEAT, .22)
    bar += 1; t += BAR
# outro melodisi (armonik minör)
mel = [(0, 76, 1), (1, 77, .5), (1.5, 76, .5), (2, 74, 1), (3, 72, 1), (4, 71, 1.5), (5.5, 72, .5), (6, 69, 2),
       (8, 72, 1), (9, 74, .5), (9.5, 76, .5), (10, 77, 1), (11, 76, 1), (12, 74, 1), (13, 71, 1), (14, 69, 2)]
lt0 = T0 + np.ceil((scenes[6] - T0)/BAR)*BAR
for (bt, m, ln) in mel:
    tt = lt0 + bt*BEAT
    if tt > TOTAL - 1.5: continue
    nn = int(ln*BEAT*SR); x = np.arange(nn)/SR
    v = sum(np.sin(2*np.pi*mtof(m)*h*(1+.003*np.sin(2*np.pi*5*x))*x)*g for h, g in ((1, 1), (2, .4), (3, .25), (4, .1)))
    v *= env_adsr(nn, .02, .1, .75, .1)
    add(music, pan(v, 0), tt, .09); add(music, pan(v, .6), tt+.3, .035)

# ---------- SFX ----------
sfx = np.zeros((N, 2), np.float32)
def whoosh(dur=.6, up=True):
    n = int(dur*SR); nz = noise(n); out = np.zeros(n); fc = np.linspace(400, 6000, n) if up else np.linspace(6000, 400, n)
    for i in range(0, n, 512):
        f = fc[i]; seg = bp(nz[max(0, i-2048):i+512], f*.6, min(f*1.6, 20000)); out[i:i+512] = seg[-len(out[i:i+512]):]
    return out*np.sin(np.pi*np.clip(np.arange(n)/n, 0, 1))**2*.5
def impact():
    n = int(1.4*SR); x = np.arange(n)/SR; f = 30 + 70*np.exp(-x*9)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*2.4) + lp(noise(n), 2500)*np.exp(-x*6)*.3)*.85
def click(g=.6):
    n = int(.03*SR); x = np.arange(n)/SR
    return (bp(noise(n), 1500, 7000)*np.exp(-x*300) + np.sin(2*np.pi*2200*x)*np.exp(-x*400))*g
def tone(f, d, g=.1, harm=((1, 1),), dec=None):
    n = int(d*SR); x = np.arange(n)/SR
    v = sum(gg*np.sin(2*np.pi*f*h*x) for h, gg in harm)
    return v*(np.exp(-x*dec) if dec else env_adsr(n, .005, .05, .9, .05))*g
def glitch(dur=.22):
    n = int(dur*SR); x = np.arange(n)/SR
    v = sq(60 + 40*np.floor(x*40 % 5), n)*.3 + hp(noise(n), 2000)*.4
    return v*((np.floor(x*60) % 2 > .5)*.5 + .5)*np.exp(-x*6)*.3



add(sfx, pan(click(1), 0), .05); add(sfx, pan(whoosh(.85), 0), .05, .7); add(sfx, pan(impact(), 0), T0 - .02, .8)
for i in range(1, 7):
    add(sfx, pan(whoosh(.55, i % 2 == 0), -.3 if i % 2 else .3), scenes[i] - .28, .65); add(sfx, pan(glitch(), 0), scenes[i] - .03, .6)
def capT(k): return next(c["t0"] for c in caps if k in c["text"])
def beep(f, d, g=.05): return tone(f, d, g)
def nz(d, lo, hi, g, dec): n = int(d*SR); x = np.arange(n)/SR; return bp(noise(n), lo, hi)*np.exp(-x*dec)*g
add(sfx, pan(impact(), 0), scenes[6], .6); add(sfx, pan(whoosh(.5), 0), SUB - .35, .6)
add(sfx, pan(click(1.2), 0), PRESS)
for k, (f, d) in enumerate([(1568, 1.6), (2093, 1.4)]): add(sfx, pan(tone(f, d, .06, ((1, 1), (2.76, .35), (5.4, .15)), 2.2), .25), PRESS + .45 + k*.18)
for k in range(28): add(sfx, pan(nz(.04, 2000, 9000, .25, 80), rng.uniform(-.9, .9)), PRESS + .05 + rng.random()*.6)
for k in range(40): add(sfx, pan(click(.18), rng.uniform(-.7, .7)), scenes[1] + .3 + k*.17 + rng.random()*.05)   # klavye
for k in range(8): add(sfx, pan(beep(880 + 220*(k % 4), .08, .05), (-1)**k*.3), capT('TAKIMLAR') + k*.18)          # oyun bipleri
n = int(.8*SR); xs = np.arange(n)/SR; add(sfx, pan(sq(55, n)*np.exp(-xs*2)*.12, 0), capT('TİTREŞİM'))                # titreşim vızıltısı
for k in range(6): add(sfx, pan(beep(1400 if k % 2 else 1000, .14, .06), 0), capT('SÜRENİZ') + k*.25)             # süre alarmı
add(sfx, pan(lp(noise(int(.4*SR)), 400)*np.hanning(int(.4*SR))*.3, 0), capT('ARTIK'))                               # ekran kapanma

# ---------- miks ----------
envv = np.abs(vo); a1 = np.exp(-1/(.03*SR)); envv = signal.lfilter([1-a1], [1, -a1], envv); envv /= envv.max() + 1e-9
duck = 1 - DUCK_DEPTH*np.clip(envv*4, 0, 1); a2 = np.exp(-1/(.15*SR)); duck = signal.lfilter([1-a2], [1, -a2], duck)
music *= duck[:, None]; music = np.tanh(music*1.2)/1.2
mix = music*MUSIC_GAIN + sfx*.8 + np.stack([vo, vo], 1)*1.2
fo = int(1.2*SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
hiss = hp(noise(N), 6000)*.004; mix += np.stack([hiss, np.roll(hiss, 333)], 1)
mix /= np.abs(mix).max()*1.05
wavfile.write(f"{OUT}/mix_pre.wav", SR, (mix*32767).astype(np.int16))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/mix_pre.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", f"{OUT}/mix.wav"], check=True)
# müzik/ses oranı kontrolü (konuşma anlarında)
m_rms = np.sqrt(np.mean((music[:, 0]*MUSIC_GAIN)[np.abs(vo) > .05]**2)); v_rms = np.sqrt(np.mean((vo*1.2)[np.abs(vo) > .05]**2))
print("ok", TOTAL, "PRESS", round(PRESS, 2), "music-vs-voice dB under speech:", round(20*np.log10(m_rms/v_rms), 1))
