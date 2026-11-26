function kid(X, Y, s, p = {}) { x.save(); x.translate(X, Y); x.scale(s, s); const { leg = 0, arm = 0, shirt = '#e8432f' } = p;
  for (const [sx, ph] of [[-16, 0], [16, Math.PI]]) { x.save(); x.translate(sx, -100); x.rotate(Math.sin(leg + ph) * .4); shape(rr(-11, 0, 22, 95, 10), '#e0ac82'); shape(rr(-15, 85, 34, 18, 8), '#1d1d1d'); x.restore(); }
  shape(rr(-34, -120, 68, 40, 12), '#2f4f8f'); shape(rr(-38, -210, 76, 100, 30), shirt);
  x.save(); x.translate(36, -200); x.rotate(arm); shape(rr(-10, 0, 20, 85, 10), shirt); shape(circ(0, 90, 12), '#e0ac82'); x.restore();
  shape(circ(0, -250, 42), '#e0ac82'); shape(() => { x.arc(0, -262, 44, Math.PI, 0); x.closePath(); }, '#3a2414');
  shape(circ(-14, -248, 5), '#111', null); shape(circ(14, -248, 5), '#111', null); shape(() => { x.arc(0, -232, 12, .1, Math.PI - .1); }, null, OL, 4); x.restore(); }
function shop(X, Y, w, closed = 0, sign = 'BAKKAL') {
  shape(rr(X, Y - 700, w, 700, 4), '#e3cfb0');
  for (let i = 0; i < 8; i++) shape(rr(X - 10 + i * (w + 20) / 8, Y - 520, (w + 20) / 8, 80, 0), i % 2 ? '#fff' : '#d8333a', OL, 4);
  shape(rr(X + 40, Y - 660, w - 80, 110, 14), '#1d5fb8'); x.fillStyle = '#ffe53b'; x.font = 'bold 84px Cap'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(sign, X + w / 2, Y - 603);
  shape(rr(X + 40, Y - 430, w - 80, 430, 6), '#6b4a2a'); shape(rr(X + 60, Y - 410, w - 120, 300, 4), '#8fb3c9');
  for (let i = 0; i < 5; i++) shape(rr(X + 80 + i * (w - 160) / 5, Y - 300, (w - 160) / 5 - 14, 80, 8), ['#e84d5b', '#ffcf4a', '#4aa36a', '#ff9e1b', '#7b5cd6'][i]);
  shape(rr(X + 70, Y - 120, 160, 100, 6), '#a8763e'); for (let i = 0; i < 5; i++) shape(circ(X + 100 + i * 25, Y - 128, 16), '#e8432f', OL, 3);
  if (closed > 0) { const h = 430 * closed; shape(rr(X + 40, Y - 430, w - 80, h, 4), '#9aa1a8'); for (let k = 0; k < h; k += 26) shape(() => { x.moveTo(X + 40, Y - 430 + k); x.lineTo(X + w - 40, Y - 430 + k); }, null, '#6d747a', 4);
    if (closed > .98) label(X + w / 2, Y - 230, 'KİRALIK', '#fff', '#d8333a', 64, -.06); }
}
function jar(X, Y, s, c) { x.save(); x.translate(X, Y); x.scale(s, s); for (let i = 0; i < 22; i++) shape(circ(-55 + hash(i * 3 + c.length) * 110, -20 - hash(i * 7) * 170, 18), c[i % c.length], OL, 3);
  x.globalAlpha = .35; shape(rr(-80, -230, 160, 230, 30), '#cfe8ff', OL, 6); x.globalAlpha = 1; shape(rr(-80, -230, 160, 230, 30), null, OL, 6); shape(rr(-70, -265, 140, 40, 10), '#d8333a'); x.restore(); }
const scenes = [
// 0 HOOK: bakkal önü, çocuk koşar
(lt, t) => {
  sky('#7fb6e8', '#ffe2b8', 380, '#ffe9a0'); cloud(80 + lt * 12, 430, 1); cloud(620 + lt * 8, 330, .8);
  apartment(-120, 1420, 300, 900, '#d9c7a7', 3); apartment(880, 1420, 300, 980, '#c9d3d6', 5);
  shop(180, 1420, 720); shape(rr(-100, 1420, W + 200, 600, 0), '#9a958c', null);
  man(700, 1440, 1.0, { armR: -.4, head: .05 });
  const k = eout(lt / 1.6); kid(lerp(-150, 330, k), 1720, 1.6, { leg: lt * 12 * (1 - k), arm: -2.6 + Math.sin(lt * 9) * .2 });
  if (lt > .5 && lt < HOOK - S[0] - .1) bubble(380, 1060, 'BAKKAL AMCA!', '#fff', 64);
  const tH = HOOK - S[0]; if (lt > tH - .1) { const s = back((lt - tH + .1) / .5); x.save(); x.translate(W / 2, 620); x.scale(s, s); x.rotate(-.04); x.font = 'bold 230px Cap'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineWidth = 40; x.strokeStyle = '#3a1d05'; x.lineJoin = 'round'; x.strokeText('BAKKAL', 0, 0); x.fillStyle = grad(-100, 100, [[0, '#fff3b0'], [.5, '#ffd34a'], [1, '#c47a10']]); x.fillText('BAKKAL', 0, 0); x.restore(); }
},
// 1 İÇERİ: raflar, defter
(lt) => {
  x.fillStyle = '#e9d6b0'; x.fillRect(0, 0, W, H);
  for (let r = 0; r < 4; r++) { shape(rr(40, 420 + r * 210, 1000, 20, 4), '#8b5a2b'); for (let k = 0; k < 7; k++) shape(rr(70 + k * 138, 420 + r * 210 - 120, 110, 120, 10), ['#e84d5b', '#ffcf4a', '#4aa36a', '#2a7de1', '#ff9e1b', '#7b5cd6', '#d8333a'][(k + r) % 7]); }
  man(540, 1560, 1.35, { armR: -.3 + Math.sin(lt * 2) * .1, armL: .3, head: Math.sin(lt * 1.5) * .05 });
  shape(rr(-40, 1420, W + 80, 520, 20), '#a0643a'); shape(rr(-40, 1420, W + 80, 40, 10), '#7a4a2a');
  const items = [['EKMEK', capT('EKMEK')], ['GAZETE', capT('EKMEK') + .6], ['GOFRET', capT('EKMEK') + 1.2]];
  items.forEach(([n, tt], i) => { const s = back((lt - (tt - S[1])) / .35); if (s > 0) { x.save(); x.translate(220 + i * 320, 1560); x.scale(s, s); label(0, 0, n, ['#ffcf4a', '#fff', '#e84d5b'][i], '#111', 56, (i - 1) * .08); x.restore(); } });
  const tv = capT('VERESİYE') - S[1]; if (lt > tv) { const s = back((lt - tv) / .45); x.save(); x.translate(540, 1000); x.scale(s, s); x.rotate(-.06); shape(rr(-230, -160, 460, 320, 16), '#2f4f8f'); shape(rr(-200, -130, 400, 260, 10), '#f4ead2'); x.fillStyle = '#1d3cbf'; x.font = 'italic bold 52px Cap'; x.textAlign = 'center'; x.fillText('VERESİYE', 0, -40); x.fillText('DEFTERİ', 0, 30); x.restore(); }
},
// 2 DEFTER: ay sonu ödenir
(lt) => {
  x.fillStyle = '#a0643a'; x.fillRect(0, 0, W, H);
  x.save(); x.translate(540, 1000); x.rotate(-.05); shape(rr(-440, -520, 880, 1040, 20), '#2f4f8f'); shape(rr(-410, -490, 820, 980, 10), '#f4ead2');
  x.strokeStyle = '#9fb6d9'; x.lineWidth = 3; for (let i = 0; i < 11; i++) { x.beginPath(); x.moveTo(-380, -380 + i * 80); x.lineTo(380, -380 + i * 80); x.stroke(); }
  x.fillStyle = '#1d3cbf'; x.font = 'italic bold 48px Cap'; x.textAlign = 'left';
  const rows = [['Ahmet Bey', '2 ekmek'], ['Ayşe Hanım', 'süt, yağ'], ['Kapıcı Ali', 'gazete'], ['Mehmet Bey', 'şeker, çay'], ['Fatma Teyze', 'deterjan'], ['Hasan Bey', '1 kg peynir']];
  rows.forEach(([a, b], i) => { if (lt > .2 + i * .35) { x.fillText(a, -370, -330 + i * 120); x.fillText(b, 60, -330 + i * 120); } });
  const tp = capT('SAYFA') - S[2]; if (lt > tp) { const k = clamp((lt - tp) / .6); x.strokeStyle = '#d8333a'; x.lineWidth = 12; x.beginPath(); x.moveTo(-380, 300); x.lineTo(-380 + 760 * k, -420 + 0 * k); x.stroke(); }
  if (lt > tp + .5) { const s = back((lt - tp - .5) / .35); x.save(); x.translate(120, 120); x.rotate(-.25); x.scale(s, s); shape(rr(-220, -70, 440, 140, 16), 'rgba(216,51,58,.15)', '#d8333a', 12); x.fillStyle = '#d8333a'; x.font = 'bold 90px Cap'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('ÖDENDİ', 0, 6); x.restore(); }
  x.restore();
  const tg = capT('GÜVEN') - S[2]; if (lt > tg) { const s = back((lt - tg) / .4); x.save(); x.translate(540, 500); x.scale(s, s); label(0, 0, 'GÜVEN ✓', '#4aa36a', '#fff', 80); x.restore(); }
},
// 3 ŞEKERLER
(lt) => {
  sky('#ffe7c2', '#ffd0a0'); shape(rr(-40, 1300, W + 80, 700, 20), '#a0643a');
  jar(230, 1300, 1.5, ['#ff4f7b', '#ffd34a', '#4ad18a']); jar(540, 1300, 1.7, ['#3a86ff', '#ff9e1b', '#fff']); jar(850, 1300, 1.5, ['#b05cd6', '#ff4f7b', '#ffe53b']);
  const ta = capT('AVUÇ') - S[3]; const h = eout((lt - ta + .8) / .6);
  x.save(); x.translate(540, lerp(2100, 1620, h)); shape(() => { x.ellipse(0, 0, 180, 90, 0, 0, Math.PI); x.closePath(); }, '#e0ac82'); shape(rr(-90, 70, 180, 300, 40), '#9cc3e6');
  for (let i = 0; i < 18; i++) { const k = clamp((lt - ta - i * .05) / .4); if (k > 0) shape(circ(-130 + (i % 9) * 32, lerp(-500, -10 - Math.floor(i / 9) * 28, eout(k)), 18), ['#ff4f7b', '#ffd34a', '#4ad18a', '#3a86ff'][i % 4], OL, 3); }
  x.restore();
  for (let i = 0; i < 3; i++) { const k = clamp((lt - .4 - i * .2) / .4); if (k > 0) { x.save(); x.translate(380 + i * 70, lerp(1500, 1700, eout(k))); shape(circ(0, 0, 30), '#d9c27a', OL, 5); x.fillStyle = '#7a5a10'; x.font = 'bold 28px Cap'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('25', 0, 2); x.restore(); } }
},
// 4 MARKETLER
(lt) => {
  sky('#8fc3ee', '#eaf3fb'); shape(rr(-100, 1480, W + 200, 600, 0), '#9a958c', null);
  const tm = capT('MARKETLER') - S[4], tz = capT('ZİNCİR') - S[4];
  const s0 = 1 - .45 * clamp((lt - tm) / 1.2); x.save(); x.translate(540, 1480); x.scale(s0, s0); shop(-360, 0, 720); x.restore();
  if (lt < tm) { const s = back(lt / .4); x.save(); x.translate(540, 600); x.scale(s, s); shape(rr(-110, -150, 220, 300, 40), '#ffe53b'); x.font = 'bold 230px Cap'; x.fillStyle = '#111'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('?', 0, 10); x.restore(); }
  const big = (X, w, col, txt, tt) => { const k = back((lt - tt) / .5); if (k <= 0) return; x.save(); x.translate(X, 1480); x.scale(1, k); shape(rr(-w / 2, -900, w, 900, 6), '#f2f4f6'); shape(rr(-w / 2, -900, w, 150, 6), col); x.fillStyle = '#fff'; x.font = 'bold 64px Cap'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, 0, -825); shape(rr(-w / 2 + 40, -650, w - 80, 400, 6), '#bfe0f5'); shape(rr(-80, -240, 160, 240, 4), '#8fb3c9'); x.restore(); };
  big(170, 330, '#e8432f', 'MARKET', tm); big(910, 330, '#2a7de1', 'ZİNCİR', tz); if (lt > tz + .4) big(540, 280, '#4aa36a', 'MARKET', tz + .4);
},
// 5 KREDİ KARTI + KEPENK
(lt) => {
  sky('#7a8696', '#c9cdd2'); cloud(100 + lt * 8, 380, 1.2, '#dfe3e8'); apartment(-120, 1420, 300, 900, '#a9a69e', 3, .02); apartment(880, 1420, 300, 980, '#a3a8aa', 5, .02);
  const tk = capT('KEPENK') - S[5], tc = capT('KREDİ') - S[5];
  shop(180, 1420, 720, clamp((lt - tk + .6) / 1.2)); shape(rr(-100, 1420, W + 200, 600, 0), '#5d5b58', null);
  if (lt > tc && lt < tk - .8) { const s = back((lt - tc) / .45); x.save(); x.translate(540, 980); x.rotate(-.12); x.scale(s, s); shape(rr(-260, -165, 520, 330, 30), grad(-165, 165, [[0, '#3a86ff'], [1, '#1b3c7a']])); shape(rr(-200, -70, 90, 70, 10), '#e2b23f'); x.fillStyle = '#fff'; x.font = 'bold 40px Osd'; x.fillText('**** **** **** 1994', -210, 100); x.restore(); }
  for (let i = 0; i < 20; i++) { const ph = ((lt * .25) + hash(i)) % 1; x.save(); x.translate(-40 + ph * 1200, 1550 + Math.sin(ph * 9 + i) * 50 + hash(i * 3) * 250); x.rotate(lt * 3 + i); shape(ell(0, 0, 16, 9), '#b5812e', null); x.restore(); }
},
