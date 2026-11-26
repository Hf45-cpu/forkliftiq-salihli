# Gerçek yükseklik verisinden (AWS terrarium) İstanbul arazisi + kıyı + sur geometrisi
import json, math, glob, numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure, draw

G = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/geo"
OUT = "/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/proj3"
z, xa, xb, ya, yb = map(int, open(f"{G}/range.txt").read().split())
W, H = (xb - xa + 1) * 256, (yb - ya + 1) * 256
elev = np.zeros((H, W), np.float32)
for x in range(xa, xb + 1):
    for y in range(ya, yb + 1):
        a = np.asarray(Image.open(f"{G}/tiles/{z}_{x}_{y}.png").convert("RGB")).astype(np.float32)
        elev[(y-ya)*256:(y-ya+1)*256, (x-xa)*256:(x-xa+1)*256] = a[..., 0]*256 + a[..., 1] + a[..., 2]/256 - 32768
n = 2**z
def px(lat, lon):   # mozaik piksel koordinatı
    X = (lon + 180) / 360 * n; Y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return (X - xa) * 256, (Y - ya) * 256
# kırpma: lon 28.86-29.09, lat 40.965-41.115
c0 = px(41.115, 28.86); c1 = px(40.965, 29.09)
X0, Y0, X1, Y1 = int(c0[0]), int(c0[1]), int(c1[0]), int(c1[1])
E = elev[Y0:Y1, X0:X1].copy(); h, w = E.shape
print("crop", w, h)
mpp = 156543.03 * math.cos(math.radians(41.04)) / n   # metre/piksel
print("m/px", round(mpp, 2), "size km", round(w*mpp/1000, 2), round(h*mpp/1000, 2))
def P(lat, lon):
    a, b = px(lat, lon); return a - X0, b - Y0
water = E <= 0.5
# küçük gürültüleri temizle
water = ndimage.binary_opening(water, iterations=1)
lab, nl = ndimage.label(water); sizes = ndimage.sum(water, lab, range(1, nl+1))
water = np.isin(lab, 1 + np.where(sizes > 400)[0])
land = ~water
E2 = np.where(water, np.minimum(E, -2), np.maximum(E, 1.0))

# --- surlar (yaklaşık koordinatlar, kuzey->güney kara surları) ---
LAND_WALL = [(41.0418, 28.9447), (41.0392, 28.9420), (41.0352, 28.9398), (41.0318, 28.9335), (41.0290, 28.9290),
             (41.0250, 28.9245), (41.0213, 28.9205), (41.0170, 28.9198), (41.0136, 28.9202), (41.0063, 28.9196),
             (41.0005, 28.9199), (40.9960, 28.9213), (40.9928, 28.9237)]
lw = [P(*c) for c in LAND_WALL]
# şehir maskesi: kara surunun doğusu + Haliç'in güneyi (Ayasofya'dan flood-fill)
barrier = np.zeros_like(land)
for (a, b), (c, d) in zip(lw[:-1], lw[1:]):
    rr, cc = draw.line(int(b), int(a), int(d), int(c))
    for o in range(-2, 3):
        barrier[np.clip(rr, 0, h-1), np.clip(cc + o, 0, w-1)] = True
# kara surunun uçlarını denize kadar uzat
for (la, lo), (dla, dlo) in [((41.0418, 28.9447), (0.004, 0.002)), ((40.9928, 28.9237), (-0.004, 0.002))]:
    a, b = P(la, lo); c, d = P(la + dla, lo + dlo); rr, cc = draw.line(int(b), int(a), int(d), int(c))
    for o in range(-2, 3): barrier[np.clip(rr, 0, h-1), np.clip(cc + o, 0, w-1)] = True
fill_area = land & ~barrier
lab, _ = ndimage.label(fill_area)
hx, hy = P(41.0086, 28.9802)
city = lab == lab[int(hy), int(hx)]
print("city area km2", round(city.sum() * mpp * mpp / 1e6, 2))
# deniz surları = şehir kıyı konturu
cont = measure.find_contours(np.pad(city, 2).astype(float), .5)
cont = max(cont, key=len) - 2
step = max(1, int(60 / mpp))
seawall = [[float(p[1]), float(p[0])] for p in cont[::step]]
# kara suru noktaları uzerinde olanları deniz surundan çıkar (≈ batıdaki düz hat)
def near_land_wall(p):
    for (a, b), (c, d) in zip(lw[:-1], lw[1:]):
        vx, vy = c - a, d - b; t = max(0, min(1, ((p[0]-a)*vx + (p[1]-b)*vy) / (vx*vx + vy*vy)))
        if math.hypot(a + t*vx - p[0], b + t*vy - p[1]) < 120 / mpp: return True
    return False
keep = [not near_land_wall(p) for p in seawall]
# kapalı konturu, kara suru boşluğu sona gelecek şekilde döndür ve en uzun kesintisiz yayı al
runs=[]; cur=[]
for i in range(2*len(seawall)):
    j=i%len(seawall)
    if keep[j]: cur.append(seawall[j])
    else:
        if cur: runs.append(cur); cur=[]
    if i>=len(seawall) and not keep[j] and runs: break
if cur: runs.append(cur)
seawall = max(runs, key=len)

# --- renk dokusu (gerçekçi harita) ---
from scipy.ndimage import gaussian_filter, distance_transform_edt
Es = gaussian_filter(E2, 1.2)
gy, gx = np.gradient(Es)
shade = np.clip(0.75 + (-gx*0.7 - gy*0.7) * 0.09, 0.35, 1.25)
col = np.zeros((h, w, 3), np.float32)
t = np.clip(E2 / 140, 0, 1)[..., None]
lowc = np.array([116, 128, 74]); midc = np.array([148, 140, 92]); hic = np.array([170, 156, 118])
landc = np.where(t < .5, lowc + (midc - lowc) * (t / .5), midc + (hic - midc) * ((t - .5) / .5))
rng = np.random.default_rng(1453)
landc = landc * (0.93 + 0.07 * gaussian_filter(rng.random((h, w)), 2)[..., None] * 2)
col[:] = landc * shade[..., None]
dw = distance_transform_edt(water) * mpp   # kıyıya uzaklık (m)
deep = np.clip(dw / 900, 0, 1)[..., None]
watc = np.array([52, 112, 128]) * (1 - deep) + np.array([18, 52, 78]) * deep
col = np.where(water[..., None], watc, col)
dl = distance_transform_edt(land) * mpp
shore = (water & (dw < 35))
col[shore] = col[shore] * .6 + np.array([190, 210, 200]) * .4
beach = land & (distance_transform_edt(land) * mpp < 30)
col[beach] = col[beach] * .6 + np.array([214, 196, 150]) * .4
# şehir dokusu: yoğun yapı lekeleri (Bizans şehri)
cityrng = gaussian_filter(rng.random((h, w)), 1.0)
col[city] = col[city] * .55 + np.array([200, 182, 150]) * .45
roofs = city & (gaussian_filter(rng.random((h, w)), .7) > .56)
col[roofs] = col[roofs] * .5 + np.array([168, 92, 64]) * .5
col = np.clip(col, 0, 255).astype(np.uint8)
Image.fromarray(col).save(f"{OUT}/map_color.jpg", quality=92)
# yükseklik (16-bit -> RG)
Hm = np.clip(E2 + 100, 0, 65535 / 100)    # +100 m ofset, 0.01 m hassasiyet
Hi = (Hm * 100).astype(np.uint32)
rgb = np.zeros((h, w, 3), np.uint8); rgb[..., 0] = Hi >> 8; rgb[..., 1] = Hi & 255
Image.fromarray(rgb).save(f"{OUT}/map_height.png")
Image.fromarray((city * 255).astype(np.uint8)).save(f"{OUT}/map_city.png")
pts = {
  "w": w, "h": h, "mpp": mpp,
  "landWall": lw, "seaWall": seawall,
  "hagia": P(41.0086, 28.9802), "galata": P(41.0256, 28.9741), "rumeli": P(41.0847, 29.0567),
  "romanus": P(41.0213, 28.9205), "adrianople": P(41.0318, 28.9335), "camp": P(41.0215, 28.9095),
  "cannon": P(41.0222, 28.9135), "chainA": P(41.0222, 28.9752), "chainB": P(41.0163, 28.9772),
  "fleet": P(41.0405, 29.0045), "goldenHornFleet": P(41.0300, 28.9650),
  "haulPath": [P(41.0262, 28.9838), P(41.0300, 28.9810), P(41.0330, 28.9775), P(41.0350, 28.9725), P(41.0365, 28.9670), P(41.0350, 28.9640)],
  "kasimpasa": P(41.0350, 28.9640), "tophane": P(41.0262, 28.9838),
  "bosphorus": P(41.0600, 29.0300), "marmara": P(40.9850, 28.9800), "uskudar": P(41.0250, 29.0150),
}
def snap_water(pt):
    a, b = int(pt[0]), int(pt[1])
    if water[b, a]: return pt
    d, idx = distance_transform_edt(~water, return_indices=True)
    return [float(idx[1][b, a]) + 0.0, float(idx[0][b, a])]
for k in ("fleet", "goldenHornFleet", "bosphorus", "marmara"): pts[k] = snap_water(pts[k])
fa, fb = pts["fleet"]; pts["fleet"] = [fa + 6, fb + 6] if water[int(fb + 6), int(fa + 6)] else pts["fleet"]
json.dump(pts, open(f"{OUT}/geo.json", "w"))
print("seawall pts", len(seawall), "elev range", E2.min(), E2.max(), "romanus elev", E2[int(pts['romanus'][1]), int(pts['romanus'][0])])
for k in ("hagia", "galata", "rumeli", "fleet", "kasimpasa", "tophane", "chainA", "chainB", "goldenHornFleet"):
    a, b = pts[k]; print(k, "water" if water[int(b), int(a)] else "land", round(float(E2[int(b), int(a)]), 1))
