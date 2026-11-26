function kid(X, Y, s, p = {}) { x.save(); x.translate(X, Y); x.scale(s, s); const { leg = 0, arm = 0, shirt = '#e8432f', back: bk = 0 } = p;
  for (const [sx, ph] of [[-16, 0], [16, Math.PI]]) { x.save(); x.translate(sx, -100); x.rotate(Math.sin(leg + ph) * .4); shape(rr(-11, 0, 22, 95, 10), '#2f4f8f'); shape(rr(-15, 85, 34, 18, 8), '#1d1d1d'); x.restore(); }
  shape(rr(-38, -210, 76, 120, 30), shirt); x.save(); x.translate(36, -200); x.rotate(arm); shape(rr(-10, 0, 20, 85, 10), shirt); shape(circ(0, 90, 12), '#e0ac82'); x.restore();
  shape(circ(0, -250, 42), bk ? '#3a2414' : '#e0ac82'); if (!bk) { shape(() => { x.arc(0, -262, 44, Math.PI, 0); x.closePath(); }, '#3a2414'); shape(circ(-14, -248, 5), '#111', null); shape(circ(14, -248, 5), '#111', null); shape(() => { x.arc(0, -232, 12, .1, Math.PI - .1); }, null, OL, 4); }
  if (p.phones) { shape(() => { x.arc(0, -255, 50, Math.PI * 1.05, Math.PI * 1.95); }, null, '#222', 12); shape(rr(-58, -270, 22, 40, 8), '#222'); shape(rr(36, -270, 22, 40, 8), '#222'); }
  x.restore(); }
function crt(X, Y, s, screen) { x.save(); x.translate(X, Y); x.scale(s, s); shape(rr(-150, -260, 300, 240, 18), '#d9d2c0'); shape(rr(-125, -238, 250, 190, 10), '#0b1a2a'); x.save(); x.beginPath(); x.rect(-125, -238, 250, 190); x.clip(); screen && screen(); x.restore();
  shape(rr(-110, -20, 220, 40, 8), '#cfc7b3'); shape(rr(-170, 30, 340, 40, 8), '#e8e2d0'); x.restore(); }
function chair(X, Y, s) { x.save(); x.translate(X, Y); x.scale(s, s); shape(rr(-60, -60, 120, 20, 6), '#222'); shape(rr(-50, -200, 100, 140, 20), '#2a2a2a'); shape(rr(-6, -40, 12, 60, 4), '#555'); x.restore(); }
function win(X, Y, w, h, title, body, shake = 0) { x.save(); x.translate(X + Math.sin(shake * 60) * 18 * (shake > 0), Y); shape(rr(-w / 2, -h / 2, w, h, 14), '#eef4fb'); shape(rr(-w / 2, -h / 2, w, 70, 14), '#2a7de1'); x.fillStyle = '#fff'; x.font = 'bold 40px Cap'; x.textAlign = 'left'; x.textBaseline = 'middle'; x.fillText(title, -w / 2 + 24, -h / 2 + 36); body && body(); x.restore(); }
const scenes = [
// 0 HOOK: tezgâh, "1 saat aç"
(lt, t) => {
  x.fillStyle = '#1c1a2e'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 4; i++) crt(140 + i * 270, 1100, .8, () => { x.fillStyle = ['#2a7de1', '#4aa36a', '#e84d5b', '#ffcf4a'][i]; x.fillRect(-125, -238, 250, 190); });
  const g = .7 + .3 * Math.sin(t * 9); x.save(); x.shadowColor = '#ff2bd6'; x.shadowBlur = 40 * g; x.font = 'bold 92px Cap'; x.textAlign = 'center'; x.fillStyle = '#ff7ae6'; x.fillText('İNTERNET CAFE', W / 2, 620); x.restore();
  shape(rr(-40, 1400, W + 80, 560, 20), '#5a3a22'); shape(rr(-40, 1400, W + 80, 40, 10), '#3a2414');
  man(760, 1430, 1.05, { armR: -.3, head: .05 }); kid(340, 1800, 1.55, { arm: -2.4 + Math.sin(lt * 8) * .2 });
  if (lt > .4 && lt < HOOK - S[0] - .2) bubble(360, 1020, '1 SAAT AÇ ABİ!', '#fff', 64);
  const tH = HOOK - S[0]; if (lt > tH - .1) { const s = back((lt - tH + .1) / .5); x.save(); x.translate(780, 1060); x.scale(s, s); shape(rr(-150, -70, 300, 140, 20), '#111', '#ff3b3b', 8); x.fillStyle = '#ff3b3b'; x.font = 'bold 90px Osd'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('00:20', 0, 4); x.restore(); }
},
// 1 SALON: sıra sıra CRT
(lt, t) => {
  x.fillStyle = '#23203a'; x.fillRect(0, 0, W, H);
  for (let r = 0; r < 3; r++) for (let i = 0; i < 4; i++) { const s = .6 + r * .25, y = 700 + r * 380; crt(130 + i * 275, y, s, () => { x.fillStyle = ['#2a7de1', '#4aa36a', '#e84d5b', '#7b5cd6'][(i + r) % 4]; x.fillRect(-125, -238, 250, 190); x.fillStyle = 'rgba(255,255,255,.15)'; x.fillRect(-125, -238 + ((t * 120 + i * 40) % 190), 250, 10); }); if (r === 2) { chair(130 + i * 275, y + 230, 1.1); kid(130 + i * 275, y + 210, 1.0, { back: 1, shirt: ['#e8432f', '#2a7de1', '#ffcf4a', '#4aa36a'][i] }); } }
  for (let i = 0; i < 6; i++) { const ph = ((lt * .3) + i / 6) % 1; x.globalAlpha = Math.sin(ph * Math.PI) * .25; shape(circ(150 + i * 160 + Math.sin(ph * 5 + i) * 40, 1500 - ph * 900, 60 + ph * 90), '#cfd6e0', null); x.globalAlpha = 1; }
  const tm = capT('TÜPLÜ') - S[1]; if (lt > tm && lt < tm + 1.4) label(540, 380, 'TÜPLÜ MONİTÖR', '#ffcf4a', '#111', 60, -.05);
  const tk = capT('KLAVYE') - S[1]; if (lt > tk) { const k = lt - tk; for (let i = 0; i < 5; i++) label(160 + i * 190, 460 + Math.sin(k * 10 + i) * 30, 'TIK', '#fff', '#111', 40, (i - 2) * .1); }
},
// 2 OYUN: takımlar
(lt, t) => {
  x.fillStyle = '#14122a'; x.fillRect(0, 0, W, H);
  crt(540, 1080, 2.6, () => { x.fillStyle = '#2b3a2a'; x.fillRect(-125, -238, 250, 190); x.fillStyle = '#556b2f'; x.fillRect(-125, -110, 250, 80); x.fillStyle = '#8a7a5a'; x.fillRect(-90, -200, 60, 100); x.fillRect(40, -190, 50, 90); x.strokeStyle = '#7fff7f'; x.lineWidth = 3; x.beginPath(); x.moveTo(-12, -143); x.lineTo(12, -143); x.moveTo(0, -155); x.lineTo(0, -131); x.stroke(); x.fillStyle = '#fff'; x.font = 'bold 18px Osd'; x.fillText('TAKIM A  3 - 2  TAKIM B', -110, -215); });
  kid(250, 1900, 1.4, { phones: 1, arm: -1.2 + Math.sin(t * 12) * .15, shirt: '#2a7de1' }); kid(830, 1900, 1.4, { phones: 1, arm: -1.2 + Math.cos(t * 12) * .15, shirt: '#e8432f' });
  const tt = capT('TAKIMLAR') - S[2]; if (lt > tt) { bubble(250, 1250, 'ATAAK!', '#ffe53b', 70); if (lt > tt + .8) bubble(830, 1180, 'ARKANDA!', '#7be0ff', 64); }
  const tk = capT('KULAKLIK') - S[2]; if (lt > tk && lt < tt) label(540, 420, 'KULAKLIKLAR TAKILDI', '#fff', '#111', 54);
},
// 3 MESAJLAŞMA
(lt, t) => {
  x.fillStyle = grad(0, H, [[0, '#3a6ea5'], [1, '#9cc3e6']]); x.fillRect(0, 0, W, H);
  win(540, 820, 760, 900, 'Sohbet', () => { const names = ['kral_1994', 'gizemli_kiz', 'mahallenin_abisi', 'okul_kaçağı']; names.forEach((n, i) => { shape(circ(-300, -300 + i * 120, 22), i % 2 ? '#4ad18a' : '#ffcf4a', OL, 3); x.fillStyle = '#111'; x.font = 'bold 40px Cap'; x.textAlign = 'left'; x.fillText(n, -260, -296 + i * 120); });
    const ts = capT('DURUM') - S[3]; if (lt > ts) { x.fillStyle = '#7b2bff'; x.font = 'italic bold 36px Cap'; x.fillText('♫ yalnızlık senfonisi... ♫', -320, 240); } }, 0);
  const tv = capT('TİTREŞİM') - S[3]; if (lt > tv) win(560, 1430, 640, 300, 'Uyarı', () => { x.fillStyle = '#d8333a'; x.font = 'bold 66px Cap'; x.textAlign = 'center'; x.fillText('TİTREŞİM!', 0, 40); }, clamp(1 - (lt - tv) / 1.2) * Math.sin(lt * 50));
},
// 4 EV İNTERNETİ + AKILLI TELEFON
(lt, t) => {
  sky('#8fc3ee', '#eaf3fb'); shape(rr(-100, 1480, W + 200, 600, 0), '#9a958c', null);
  const th = capT('HIZLI') - S[4], tp = capT('AKILLI') - S[4];
  if (lt < th) { const s = back(lt / .4); x.save(); x.translate(540, 700); x.scale(s, s); shape(rr(-110, -150, 220, 300, 40), '#ffe53b'); x.font = 'bold 230px Cap'; x.fillStyle = '#111'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('?', 0, 10); x.restore(); }
  apartment(260, 1480, 560, 760, '#e8d9b8', 9, .6);
  if (lt > th) for (let i = 0; i < 3; i++) { const k = clamp((lt - th - i * .2) / .3); x.globalAlpha = k * (.6 + .4 * Math.sin(t * 6 - i)); x.strokeStyle = '#2a7de1'; x.lineWidth = 22; x.beginPath(); x.arc(540, 640, 80 + i * 70, Math.PI * 1.2, Math.PI * 1.8); x.stroke(); x.globalAlpha = 1; }
  if (lt > tp) { const s = back((lt - tp) / .45); x.save(); x.translate(540, 1150); x.scale(s, s); x.rotate(.06); shape(rr(-170, -330, 340, 660, 50), '#111'); shape(rr(-145, -290, 290, 560, 24), grad(-290, 270, [[0, '#7b2bff'], [1, '#2a7de1']])); for (let i = 0; i < 12; i++) shape(rr(-120 + (i % 4) * 66, -250 + Math.floor(i / 4) * 80, 50, 50, 12), ['#ffcf4a', '#4ad18a', '#ff4f7b', '#fff'][i % 4], null); x.restore(); }
},
// 5 KAPANDI + SÜRENİZ DOLDU
(lt, t) => {
  sky('#6f7887', '#b9bec6'); apartment(-120, 1420, 300, 900, '#a9a69e', 3, .02); apartment(880, 1420, 300, 980, '#a3a8aa', 5, .02);
  shape(rr(180, 720, 720, 700, 4), '#c9c2b4'); shape(rr(220, 990, 640, 430, 4), '#9aa1a8'); for (let k = 0; k < 430; k += 26) shape(() => { x.moveTo(220, 990 + k); x.lineTo(860, 990 + k); }, null, '#6d747a', 4);
  x.save(); x.font = 'bold 76px Cap'; x.textAlign = 'center'; x.fillStyle = '#777'; x.fillText('İNTERNET CAFE', 540, 900); x.restore(); label(540, 1180, 'KAPANDI', '#fff', '#d8333a', 70, -.06);
  shape(rr(-100, 1420, W + 200, 600, 0), '#5d5b58', null);
  const td = capT('SÜRENİZ') - S[5]; if (lt > td) { const off = clamp((lt - capT('ARTIK') + S[5]) / .4); const s = back((lt - td) / .4) * (1 - off); if (s > .01) { x.save(); x.translate(540, 560); x.scale(s, s); win(0, 0, 720, 300, 'Uyarı', () => { x.fillStyle = (Math.floor(t * 3) % 2) ? '#d8333a' : '#111'; x.font = 'bold 64px Cap'; x.textAlign = 'center'; x.fillText('SÜRENİZ DOLDU', 0, 40); }); x.restore(); } }
},
