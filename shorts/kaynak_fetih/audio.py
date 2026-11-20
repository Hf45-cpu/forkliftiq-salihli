# İstanbul'un Fethi — mehter esintili sentez müzik + SFX
import json, subprocess, numpy as np
from scipy.io import wavfile
from scipy import signal
SR = 44100
OUT = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/proj3"
rng = np.random.default_rng(1453)
S = [0, 5.0, 10.5, 16.5, 21.0, 30.0, 37.5, 42.0, 49.0, 54.3]
TOTAL = 59.5; N = int(TOTAL*SR)
FIRE, IMPACT = 35.6, 36.25          # Şahi topu atışı
BREACH = 51.6; PRESS = 57.0
json.dump({"scenes": S, "total": TOTAL, "fire": FIRE, "impact": IMPACT, "breach": BREACH, "press": PRESS}, open(f"{OUT}/timeline.json", "w"))

def tN(t): return int(t*SR)
def env(n, a=.005, d=.1, s=.6, r=.1):
    an, dn, rn = int(a*SR), int(d*SR), int(r*SR); sl = max(n-an-dn-rn, 0)
    e = np.concatenate([np.linspace(0, 1, an, endpoint=False), np.linspace(1, s, dn, endpoint=False), np.full(sl, s), np.linspace(s, 0, rn)])
    return np.pad(e, (0, max(0, n-len(e))))[:n]
def lp(x, f, o=2): b, a = signal.butter(o, min(f, SR/2*.95)/(SR/2), "low"); return signal.lfilter(b, a, x)
def hp(x, f, o=2): b, a = signal.butter(o, f/(SR/2), "high"); return signal.lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = signal.butter(o, [lo/(SR/2), hi/(SR/2)], "band"); return signal.lfilter(b, a, x)
def noise(n): return rng.standard_normal(n)
def add(buf, x, t, g=1.0):
    a = tN(t)
    if a >= len(buf): return
    if a < 0: x = x[-a:]; a = 0
    x = x[:len(buf)-a]
    if buf.ndim == 2 and x.ndim == 1: x = np.stack([x, x], 1)
    buf[a:a+len(x)] += g*x
def pan(x, p): return np.stack([x*np.sqrt((1-p)/2), x*np.sqrt((1+p)/2)], 1)
def mtof(m): return 440*2**((m-69)/12)
def section(t):
    for i in range(len(S)-1, -1, -1):
        if t >= S[i]: return i
    return 0

mus = np.zeros((N, 2)); sfx = np.zeros((N, 2))
BPM = 90; B = 60/BPM

# --- vurmalılar ---
def davul(g=1.0):
    n = int(.6*SR); x = np.arange(n)/SR; f = 62 + 70*np.exp(-x*30)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*6) + lp(noise(n), 900)*np.exp(-x*25)*.5)*g
def tek(g=1.0):    # davulun ince sopası (çubuk)
    n = int(.12*SR); x = np.arange(n)/SR
    return (bp(noise(n), 1500, 6000)*np.exp(-x*45) + np.sin(2*np.pi*420*x)*np.exp(-x*50)*.4)*g
def kos(g=1.0):    # kös: derin timpani
    n = int(2.2*SR); x = np.arange(n)/SR; f = 44 + 18*np.exp(-x*4)
    return (np.sin(2*np.pi*np.cumsum(f)/SR) + .3*np.sin(2*np.pi*np.cumsum(f*1.5)/SR))*np.exp(-x*1.6)*g
def zil(g=1.0):
    n = int(1.8*SR); x = np.arange(n)/SR; v = hp(noise(n), 4000)
    for f in (3170, 4410, 5230, 6880): v += .2*np.sin(2*np.pi*f*x + rng.random()*6)
    return v*np.exp(-x*2.6)*.35*g
D, ZK, KS, Z = davul(), tek(), kos(), zil()

# mehter ritmi: DÜM . tek DÜM | tek . DÜM tek  (8 sekizlik)
pattern = [(0, 'D'), (1, 'T'), (1.5, 'T'), (2, 'D'), (3, 'T'), (3.5, 'D'), ]
t = S[4]
while t < S[9] - .01:
    sec = section(t)
    inten = {4: .8, 5: .35, 6: .5, 7: .85, 8: 1.15}.get(sec, 0)
    for off, k in pattern:
        tt = t + off*B
        if section(tt) == 5 and off not in (0,): continue
        if k == 'D': add(mus, pan(D, -.1), tt, .55*inten)
        else: add(mus, pan(ZK, .3), tt, .5*inten)
    if sec in (4, 7, 8): add(mus, pan(Z, .2), t, .55*inten)
    if sec == 8: add(mus, pan(KS, 0), t, .5)
    t += 4*B
# büyük kös vuruşları (vurgu anları)
for tt, g in [(.55, 1.1), (4.85, 1.2), (S[4], 1.1), (S[7], .9), (S[8], 1.2), (BREACH, 1.4), (S[9], 1.0)]:
    add(mus, pan(KS, 0), tt, g); add(mus, pan(Z, 0), tt, .7*g)

# --- dron ve yaylılar (D Hicaz) ---
def strings(notes, dur, g, cutoff=1500, att=.6):
    n = int(dur*SR); out = np.zeros((n, 2))
    for m in notes:
        for k, det in enumerate((-.08, 0, .08)):
            f = mtof(m + det); x = np.arange(n)/SR
            v = 2*((f*x + rng.random()) % 1) - 1
            out += pan(lp(v, cutoff), -.5 + .5*k)
    return out*env(n, att, .3, .9, .8)[:, None]*g
prog = [([50, 57, 62], 0, 5.0), ([50, 57, 62, 66], 5.0, 10.5), ([51, 55, 58, 62], 10.5, 16.5), ([50, 54, 57, 62], 16.5, 21.0),
        ([50, 57, 62, 66], 21, 30), ([46, 50, 53, 58], 30, 37.5), ([51, 55, 58, 63], 37.5, 42), ([50, 54, 57, 62], 42, 49),
        ([50, 57, 62, 66, 69], 49, 54.3), ([50, 54, 57, 62, 66, 69], 54.3, TOTAL)]
for notes, a, b in prog:
    add(mus, strings(notes, b - a + .8, .012 if a < 49 else .016, 1300 if a < 21 else 1900), a)
n = N; x = np.arange(n)/SR
drone = (np.sin(2*np.pi*mtof(38)*x) + .5*np.sin(2*np.pi*mtof(45)*x))*.05*(.7 + .3*np.sin(2*np.pi*.1*x))
add(mus, pan(drone, 0), 0)

# --- zurna benzeri melodi (Hicaz: D Eb F# G A Bb C D) ---
def zurna(m, dur, g=.1, bend=0):
    n = int(dur*SR); x = np.arange(n)/SR
    f = mtof(m)*(1 + .006*np.sin(2*np.pi*6.2*x)*np.minimum(1, x*4))
    if bend: f *= 2**(bend*np.exp(-x*18)/12)
    ph = np.cumsum(f)/SR; v = np.where((ph % 1) < .32, 1., -1.)
    v = bp(v, 700, 4200) + .6*bp(v, 2200, 3200)
    return v*env(n, .02, .05, .85, .06)*g
mel = [(0, 69, 1), (1, 67, .5), (1.5, 66, .5), (2, 63, 1), (3, 62, 1), (4, 62, .5), (4.5, 63, .5), (5, 66, 1), (6, 67, .5), (6.5, 69, 1.5),
       (8, 70, 1), (9, 69, .5), (9.5, 67, .5), (10, 66, 1), (11, 67, .5), (11.5, 69, .5), (12, 66, 1), (13, 63, 1), (14, 62, 2)]
def play_mel(t0, until, g=.09, oct=0):
    t = t0
    while t < until:
        for bt, m, ln in mel:
            tt = t + bt*B
            if tt + ln*B > until: return
            add(mus, pan(zurna(m + oct, ln*B*.95, g, bend=-1 if ln >= 1 else 0), .15), tt)
        t += 16*B
play_mel(S[4] + 4*B, S[5], .07)
play_mel(S[7], S[8], .06)
play_mel(S[8], S[9], .085, 0); play_mel(S[8], S[9], .04, 12)
# ney benzeri nefesli (giriş/surlar)
def ney(m, dur, g=.05):
    n = int(dur*SR); x = np.arange(n)/SR; f = mtof(m)*(1 + .004*np.sin(2*np.pi*5*x))
    v = np.sin(2*np.pi*np.cumsum(f)/SR) + .25*np.sin(2*np.pi*np.cumsum(2*f)/SR) + bp(noise(n), mtof(m), mtof(m)*3)*.6
    return v*env(n, .25, .2, .8, .4)*g
for tt, m, d in [(5.6, 69, 1.6), (7.3, 67, .8), (8.1, 66, .8), (8.9, 63, 1.4), (11.2, 62, 2), (13.4, 63, .8), (14.2, 66, 1), (15.3, 67, 1.2), (17.0, 69, 2.2), (19.3, 70, 1.6)]:
    add(mus, pan(ney(m, d), -.2), tt)
# final çözülme (Re majör hissi)
for m in (62, 66, 69, 74):
    add(mus, pan(zurna(m, 2.6, .03), 0), S[9] + .2)

# --- SFX ---
def whoosh(dur=.7, up=True):
    n = int(dur*SR); nz = noise(n); out = np.zeros(n); fc = np.linspace(300, 5000, n) if up else np.linspace(5000, 300, n)
    for i in range(0, n, 512):
        f = fc[i]; seg = bp(nz[max(0, i-2048):i+512], f*.6, min(f*1.6, 20000)); out[i:i+512] = seg[-len(out[i:i+512]):]
    return out*np.sin(np.pi*np.arange(n)/n)**2*.5
def boom(g=1.0, dur=3.0):
    n = int(dur*SR); x = np.arange(n)/SR; f = 28 + 60*np.exp(-x*7)
    v = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*1.4) + lp(noise(n), 1800)*np.exp(-x*3)*.7 + lp(noise(n), 300)*np.exp(-x*.9)*.5
    return v*g
def crumble(dur=2.2):
    n = int(dur*SR); x = np.arange(n)/SR; v = lp(noise(n), 2500)*np.exp(-x*1.2)*.3
    for k in range(70):
        p = int(rng.random()*n*.8); m = int(.03*SR); v[p:p+m] += bp(noise(m), 300, 4000)*np.exp(-np.arange(m)/SR*80)*rng.uniform(.2, .8)
    return v
def wind(dur, g=.08):
    n = int(dur*SR); x = np.arange(n)/SR; v = noise(n); out = np.zeros(n)
    for i in range(0, n, 1024):
        f = 500 + 200*np.sin(i/SR*.7) + 120*np.sin(i/SR*1.9); seg = bp(v[max(0, i-3000):i+1024], f*.5, f*2); out[i:i+1024] = seg[-len(out[i:i+1024]):]
    return out*g
add(sfx, np.stack([wind(21.5), wind(21.5)[::-1]], 1), 0, 1.0)
for i in range(1, 10): add(sfx, pan(whoosh(.7, i % 2 == 0), -.3 if i % 2 else .3), S[i] - .35, .55)
# kara suru vurgusu
for k in range(5):
    add(sfx, pan(bp(noise(int(.25*SR)), 200, 1500)*np.hanning(int(.25*SR))*.3, 0), S[1] + 1.2 + k*.35)
# ordu: uzaktan uğultu + ayak sesleri
n = int((S[5]-S[4])*SR); x = np.arange(n)/SR
crowd = lp(noise(n), 600)*.05*np.minimum(1, x/3)
for k in range(int(n/SR*7)):
    p = int(rng.random()*(n-3000)); crowd[p:p+2500] += lp(noise(2500), 250)*np.hanning(2500)*rng.uniform(.04, .1)
add(sfx, np.stack([crowd, np.roll(crowd, 2000)], 1), S[4])
# top: ateşleme + uçuş + çarpma + yıkılma
add(sfx, pan(boom(1.3, 3.5), -.2), FIRE)
n = int((IMPACT-FIRE)*SR); x = np.arange(n)/SR
add(sfx, pan(bp(noise(n), 300, 1800)*np.linspace(.2, 1, n)*.25, .2), FIRE + .05)
add(sfx, pan(boom(1.0, 2.5), .3), IMPACT); add(sfx, pan(crumble(), .3), IMPACT + .05, 1.2)
# top tanıtımı: metal tını
add(sfx, pan(np.sin(2*np.pi*180*np.arange(int(1.5*SR))/SR)*np.exp(-np.arange(int(1.5*SR))/SR*2)*.15, 0), S[5] + .4)
# zincir
for k in range(9):
    m = int(.08*SR); xx = np.arange(m)/SR
    add(sfx, pan((bp(noise(m), 1500, 7000) + .5*np.sin(2*np.pi*(2600 + 300*k)*xx))*np.exp(-xx*40)*.35, .2), S[6] + .6 + k*.13 + (k//3)*.25)
add(sfx, pan(boom(.4, 1.5), .4), S[6] + 2.6)
# gemiler karadan: ahşap gıcırtısı + "hey" ritmi
for k in range(10):
    m = int(.5*SR); xx = np.arange(m)/SR
    cr = bp(np.sin(2*np.pi*np.cumsum(250 + 120*np.sin(2*np.pi*3*xx))/SR) + noise(m)*.3, 200, 1500)*np.hanning(m)*.12
    add(sfx, pan(cr, rng.uniform(-.6, .6)), S[7] + .4 + k*.62)
    hey = bp(noise(int(.18*SR)), 300, 1100)*np.hanning(int(.18*SR))*.25
    add(sfx, pan(hey, 0), S[7] + .4 + k*.62 + .3)
# final hücum: savaş uğultusu + çatışma
n = int((S[9]-S[8])*SR); x = np.arange(n)/SR
roar = bp(noise(n), 250, 1600)*.12*np.minimum(1, x/1.2)*(1 + .3*np.sin(2*np.pi*.7*x))
add(sfx, np.stack([roar, np.roll(roar, 3000)], 1), S[8])
for k in range(40):
    m = int(.05*SR); xx = np.arange(m)/SR
    add(sfx, pan((hp(noise(m), 2500) + .6*np.sin(2*np.pi*rng.uniform(2000, 4000)*xx))*np.exp(-xx*60)*.2, rng.uniform(-.8, .8)), S[8] + .5 + rng.random()*(S[9]-S[8]-.8))
add(sfx, pan(crumble(2.5), 0), BREACH, 1.4); add(sfx, pan(boom(.8, 3), 0), BREACH)
# abone
def click(g=.8):
    m = int(.03*SR); xx = np.arange(m)/SR; return (bp(noise(m), 1500, 7000)*np.exp(-xx*300) + np.sin(2*np.pi*2200*xx)*np.exp(-xx*400))*g
add(sfx, pan(whoosh(.5), 0), PRESS - 1.1, .5); add(sfx, pan(click(1.1), 0), PRESS)
for k, f in enumerate((1568, 2093)):
    m = int(1.4*SR); xx = np.arange(m)/SR
    add(sfx, pan(sum(g*np.sin(2*np.pi*f*h*xx) for h, g in ((1, 1), (2.76, .35), (5.4, .15)))*np.exp(-xx*2.2)*.06, .25), PRESS + .45 + k*.18)
for k in range(26):
    m = int(.04*SR); add(sfx, pan(bp(noise(m), 2000, 9000)*np.exp(-np.arange(m)/SR*80)*.22, rng.uniform(-.9, .9)), PRESS + .05 + rng.random()*.6)

mix = np.tanh(mus*1.1)*.9 + sfx*.85
fo = int(1.5*SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.abs(mix).max()*1.05
wavfile.write(f"{OUT}/mix_pre.wav", SR, (mix*32767).astype(np.int16))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/mix_pre.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=10", "-ar", "48000", f"{OUT}/mix.wav"], check=True)
print("ok", TOTAL)
