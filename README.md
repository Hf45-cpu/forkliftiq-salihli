# forkliftiq-salihli
değerlendirme
[ForkliftIQ_MASTER_v7 (3).html](https://github.com/user-attachments/files/29078628/ForkliftIQ_MASTER_v7.3.html)
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ForkliftIQ — Predictive Maintenance Platform</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<style>
:root{
  --bg:#07090f;--bg2:#0d1117;--bg3:#161b27;--bg4:#1e2535;
  --border:rgba(255,255,255,0.07);--border2:rgba(255,255,255,0.14);
  --text:#e8edf8;--text2:#7a8ba8;--text3:#3d4e68;
  --red:#f43f5e;--amber:#f59e0b;--green:#10b981;--blue:#3b82f6;--cyan:#22d3ee;--purple:#a78bfa;
  --red-bg:rgba(244,63,94,0.1);--amber-bg:rgba(245,158,11,0.1);
  --green-bg:rgba(16,185,129,0.1);--blue-bg:rgba(59,130,246,0.1);
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;height:100%;overflow:hidden;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}

/* UPLOAD */
#upload-screen{position:fixed;inset:0;background:var(--bg);z-index:999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;}
.up-logo{font-size:32px;font-weight:900;color:var(--cyan);letter-spacing:-.03em;}
.up-logo span{color:var(--text2);font-weight:300;}
.up-card{background:var(--bg3);border:1px solid var(--border2);border-radius:20px;padding:44px 52px;text-align:center;max-width:500px;width:92%;}
.up-title{font-size:21px;font-weight:700;margin-bottom:9px;}
.up-sub{font-size:13px;color:var(--text2);margin-bottom:28px;line-height:1.65;}
.up-zone{border:2px dashed var(--border2);border-radius:14px;padding:34px 20px;cursor:pointer;transition:all .2s;position:relative;margin-bottom:18px;}
.up-zone:hover,.up-zone.drag{border-color:var(--cyan);background:rgba(34,211,238,0.04);}
.up-zone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;}
.up-icon{font-size:40px;margin-bottom:10px;}
.up-zt{font-size:13px;color:var(--text2);}
.up-zt b{color:var(--cyan);}
.up-prog{display:none;margin-top:16px;}
.up-prog-bar{height:4px;background:var(--bg4);border-radius:2px;overflow:hidden;}
.up-prog-fill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--blue));width:0%;transition:width .15s;}
.up-prog-txt{font-size:11px;color:var(--text2);margin-top:8px;}
.up-demo{background:transparent;border:1px solid var(--border2);color:var(--text2);font-size:12px;padding:8px 22px;border-radius:8px;cursor:pointer;transition:all .2s;margin-top:4px;}
.up-demo:hover{border-color:var(--cyan);color:var(--cyan);}
.up-fmt{font-size:10px;color:var(--text3);margin-top:16px;line-height:1.7;}

/* APP LAYOUT */
#app{display:none;grid-template-columns:260px 1fr;grid-template-rows:50px 1fr;height:100vh;}

/* TOPBAR */
.topbar{grid-column:1/-1;background:var(--bg2);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 16px;gap:10px;z-index:100;flex-shrink:0;}
.tpulse{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green);animation:pulse 2s infinite;flex-shrink:0;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.tlogo{font-size:14px;font-weight:900;color:var(--cyan);letter-spacing:.02em;}
.tdiv{width:1px;height:22px;background:var(--border);margin:0 2px;flex-shrink:0;}
.tsub{font-size:10px;color:var(--text2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px;}
.tspc{flex:1;}
.tstat{text-align:center;padding:0 4px;}
.tsv{font-size:17px;font-weight:700;line-height:1;}
.tsl{font-size:8px;color:var(--text2);margin-top:2px;text-transform:uppercase;letter-spacing:.06em;}
.t-btn{border:1px solid rgba(34,211,238,0.3);color:var(--cyan);font-size:10px;padding:5px 12px;border-radius:7px;cursor:pointer;transition:all .15s;white-space:nowrap;background:rgba(34,211,238,0.08);}
.t-btn:hover{background:rgba(34,211,238,0.18);}
.t-btn.sec{background:rgba(255,255,255,0.04);border-color:var(--border2);color:var(--text2);}
.t-btn.sec:hover{color:var(--text);border-color:var(--text2);}
#tclock{font-size:10px;color:var(--text3);white-space:nowrap;}

/* SIDEBAR */
.sidebar{background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;}
.sb-hdr{padding:11px 13px 8px;font-size:9px;font-weight:700;color:var(--text3);letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--border);flex-shrink:0;}
.sb-list{overflow-y:auto;flex:1;}
.dcard{padding:10px 13px;border-bottom:1px solid var(--border);cursor:pointer;transition:background .12s;border-left:3px solid transparent;}
.dcard:hover{background:rgba(255,255,255,0.025);}
.dcard.act{background:rgba(59,130,246,0.08);border-left-color:var(--blue);}
.dname{font-size:11px;font-weight:600;color:var(--text);margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.drow{display:flex;align-items:center;gap:5px;margin-bottom:4px;}
.badge{font-size:8px;font-weight:700;padding:1px 5px;border-radius:8px;text-transform:uppercase;letter-spacing:.04em;}
.bc{background:var(--red-bg);color:var(--red);border:1px solid rgba(244,63,94,.25);}
.bw{background:var(--amber-bg);color:var(--amber);border:1px solid rgba(245,158,11,.25);}
.bn{background:var(--green-bg);color:var(--green);border:1px solid rgba(16,185,129,.25);}
.bh{background:var(--red-bg);color:var(--red);}
.bm{background:var(--amber-bg);color:var(--amber);}
.bl{background:var(--green-bg);color:var(--green);}
.dbar{height:2px;background:var(--bg4);border-radius:1px;margin-bottom:3px;}
.dbar-fill{height:2px;border-radius:1px;transition:width .4s;}
.dmeta{display:flex;justify-content:space-between;font-size:9px;color:var(--text2);}

/* MAIN */
.main{display:flex;flex-direction:column;overflow:hidden;min-width:0;}

/* KPI ROW */
.kpi-row{flex:0 0 auto;display:grid;grid-template-columns:repeat(5,1fr);gap:7px;padding:8px 10px;border-bottom:1px solid var(--border);background:var(--bg2);}
.kpi{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:10px 12px;border-top:2px solid transparent;}
.kpi-l{font-size:9px;color:var(--text2);margin-bottom:4px;text-transform:uppercase;letter-spacing:.07em;}
.kpi-v{font-size:21px;font-weight:700;line-height:1;}
.kpi-s{font-size:9px;color:var(--text3);margin-top:3px;}

/* TABS */
.tab-bar{flex:0 0 auto;display:flex;align-items:center;border-bottom:1px solid var(--border);background:var(--bg2);padding:0 10px;overflow-x:auto;}
.tab-bar::-webkit-scrollbar{height:2px;}
.tab{font-size:11px;font-weight:500;color:var(--text2);padding:10px 13px;cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap;flex-shrink:0;}
.tab:hover{color:var(--text);}
.tab.act{color:var(--cyan);border-bottom-color:var(--cyan);}
.tab-spacer{flex:1;}
.tab-devname{font-size:10px;color:var(--text3);padding:0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;}

/* TAB CONTENT */
.tab-content{flex:1;overflow:hidden;position:relative;}
.tab-pane{position:absolute;inset:0;overflow-y:auto;display:none;padding:12px;}
.tab-pane.act{display:block;}

/* CARDS */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px;}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;}
.ct{font-size:9px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.09em;margin-bottom:11px;display:flex;align-items:center;gap:6px;}
.ctd{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.cw{position:relative;}

/* STAT TABLE */
.stbl{width:100%;font-size:11px;border-collapse:collapse;}
.stbl th{font-size:9px;color:var(--text3);font-weight:600;text-transform:uppercase;letter-spacing:.07em;padding:5px 4px;border-bottom:1px solid var(--border);text-align:right;}
.stbl th:first-child{text-align:left;}
.stbl td{padding:6px 4px;border-bottom:1px solid var(--border);color:var(--text2);text-align:right;}
.stbl td:first-child{text-align:left;color:var(--text);font-weight:600;}
.stbl tr:last-child td{border:none;}

/* ANOMALY TABLE */
.atable{width:100%;font-size:11px;border-collapse:collapse;}
.atable th{font-size:9px;color:var(--text3);font-weight:600;letter-spacing:.07em;text-transform:uppercase;padding:5px 8px;border-bottom:1px solid var(--border);text-align:left;background:var(--bg3);}
.atable td{padding:7px 8px;border-bottom:1px solid var(--border);color:var(--text2);}
.atable tr:hover td{background:rgba(255,255,255,0.012);}
.atable tr:last-child td{border:none;}
.pill{display:inline-block;font-size:8px;font-weight:700;padding:2px 6px;border-radius:8px;}

/* GAUGE */
.gauge-wrap{display:flex;flex-direction:column;align-items:center;padding:6px 0 2px;}
.gauge-svg{overflow:visible;}
.gauge-val{font-size:28px;font-weight:800;margin-top:2px;line-height:1;}
.gauge-lbl{font-size:10px;color:var(--text2);margin-top:3px;}

/* RUL BOX */
.rul-box{background:linear-gradient(135deg,rgba(34,211,238,0.07),rgba(59,130,246,0.05));border:1px solid rgba(34,211,238,0.18);border-radius:12px;padding:14px;text-align:center;}
.rul-v{font-size:34px;font-weight:900;color:var(--cyan);}
.rul-l{font-size:10px;color:var(--text2);margin-top:3px;}
.rul-sub{font-size:10px;color:var(--text3);margin-top:8px;line-height:1.5;}

/* INSIGHTS */
.insight{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px;}
.insight-h{font-size:11px;font-weight:700;margin-bottom:5px;}
.insight-b{font-size:11px;color:var(--text2);line-height:1.65;}
.arow{display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid var(--border);}
.arow:last-child{border:none;}
.adot{width:6px;height:6px;border-radius:50%;margin-top:4px;flex-shrink:0;}
.ared{background:var(--red);box-shadow:0 0 4px var(--red);}
.aamb{background:var(--amber);box-shadow:0 0 4px var(--amber);}
.ablu{background:var(--blue);box-shadow:0 0 4px var(--blue);}
.agrn{background:var(--green);box-shadow:0 0 4px var(--green);}
.atxt{font-size:11px;color:var(--text2);line-height:1.5;}

/* TIMELINE */
.tl{padding-left:16px;}
.tl-item{position:relative;padding:0 0 14px 18px;border-left:1px solid var(--border2);}
.tl-item:last-child{border-left-color:transparent;}
.tl-dot{position:absolute;left:-5px;top:3px;width:9px;height:9px;border-radius:50%;border:2px solid var(--bg2);}
.tl-time{font-size:9px;color:var(--text3);margin-bottom:2px;}
.tl-txt{font-size:11px;color:var(--text2);}
.tl-b{font-size:10px;font-weight:600;}

/* PODIUM */
.podium{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px;}
.pod{border-radius:12px;padding:14px;text-align:center;border:1px solid var(--border);}
.pod-rank{font-size:28px;font-weight:900;opacity:.12;line-height:1;}
.pod-name{font-size:10px;font-weight:600;margin:4px 0 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pod-score{font-size:24px;font-weight:800;margin:2px 0;}
.pod-lbl{font-size:9px;color:var(--text2);}

/* REPORT */
.rep-hdr{background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:12px;display:flex;align-items:center;gap:16px;}
.rep-icon{font-size:36px;flex-shrink:0;}
.rep-meta{flex:1;}
.rep-title{font-size:16px;font-weight:700;margin-bottom:4px;}
.rep-sub{font-size:11px;color:var(--text2);}
.rep-btn{background:var(--blue);border:none;color:#fff;font-size:11px;font-weight:600;padding:9px 18px;border-radius:8px;cursor:pointer;transition:opacity .15s;}
.rep-btn:hover{opacity:.85;}
.rep-sec{font-size:12px;font-weight:700;color:var(--text);margin:14px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--border);}
.rep-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;}
.rc{background:var(--bg3);border:1px solid var(--border);border-radius:9px;padding:12px;}
.rc-l{font-size:9px;color:var(--text2);margin-bottom:4px;}
.rc-v{font-size:16px;font-weight:700;}
.rc-s{font-size:9px;color:var(--text3);margin-top:2px;}

/* MINI STATS */
.stat-mini{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;}
.stat-mini-item{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:8px 12px;flex:1;min-width:80px;}
.smi-l{font-size:8px;color:var(--text3);}
.smi-v{font-size:14px;font-weight:700;margin-top:2px;}

/* BRAND ANALYSIS */
.brand-header{display:flex;align-items:center;gap:14px;background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:16px 20px;margin-bottom:12px;}
.brand-logo{width:52px;height:52px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;flex-shrink:0;}
.brand-logo.jung{background:linear-gradient(135deg,#003399,#0055cc);color:#fff;}
.brand-logo.still{background:linear-gradient(135deg,#cc0000,#ff2200);color:#fff;}
.brand-logo.other{background:linear-gradient(135deg,#1e2535,#2a3548);color:var(--text2);}
.brand-name{font-size:18px;font-weight:800;color:var(--text);}
.brand-sub{font-size:11px;color:var(--text2);margin-top:3px;}
.brand-badge{margin-left:auto;font-size:10px;font-weight:700;padding:5px 12px;border-radius:8px;}
.fault-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:10px;}
.fault-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;position:relative;overflow:hidden;}
.fault-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:12px 12px 0 0;}
.fault-card.sev-critical::before{background:var(--red);}
.fault-card.sev-high::before{background:var(--amber);}
.fault-card.sev-medium::before{background:var(--blue);}
.fault-card.sev-low::before{background:var(--green);}
.fault-icon{font-size:26px;margin-bottom:8px;}
.fault-title{font-size:12px;font-weight:700;color:var(--text);margin-bottom:4px;}
.fault-zone{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;}
.fault-desc{font-size:10px;color:var(--text2);line-height:1.55;}
.fault-sev{display:inline-block;font-size:8px;font-weight:700;padding:2px 6px;border-radius:6px;margin-top:6px;}
.fault-sev.sc{background:var(--red-bg);color:var(--red);}
.fault-sev.sh{background:var(--amber-bg);color:var(--amber);}
.fault-sev.sm{background:var(--blue-bg);color:var(--blue);}
.fault-sev.sl{background:var(--green-bg);color:var(--green);}
.fault-trigger{font-size:9px;color:var(--text3);margin-top:4px;font-style:italic;}
.body-diagram{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:10px;}
.diag-title{font-size:9px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.09em;margin-bottom:12px;display:flex;align-items:center;gap:6px;}
.diag-svg-wrap{display:flex;justify-content:center;}
.data-match-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px;display:flex;align-items:flex-start;gap:10px;}
.dmc-icon{font-size:20px;flex-shrink:0;margin-top:1px;}
.dmc-title{font-size:11px;font-weight:700;color:var(--text);margin-bottom:3px;}
.dmc-body{font-size:10px;color:var(--text2);line-height:1.55;}
.dmc-data{font-size:10px;font-weight:600;margin-top:4px;}
.maintenance-table{width:100%;font-size:11px;border-collapse:collapse;}
.maintenance-table th{font-size:9px;color:var(--text3);font-weight:600;text-transform:uppercase;letter-spacing:.07em;padding:5px 8px;border-bottom:1px solid var(--border);text-align:left;background:var(--bg3);}
.maintenance-table td{padding:7px 8px;border-bottom:1px solid var(--border);color:var(--text2);}
.maintenance-table tr:last-child td{border:none;}
.no-brand-msg{text-align:center;padding:60px 20px;color:var(--text2);}
.no-brand-icon{font-size:48px;margin-bottom:12px;}
.no-brand-title{font-size:16px;font-weight:600;color:var(--text);margin-bottom:8px;}
.no-brand-sub{font-size:12px;color:var(--text2);line-height:1.6;}
</style>
</head>
<body>

<!-- ══ UPLOAD ══ -->
<div id="upload-screen">
  <div class="up-logo">Forklift<span>IQ</span></div>
  <div class="up-card">
    <div class="up-title">Titreşim Verisi Yükle</div>
    <div class="up-sub">Excel dosyanızı yükleyin — sistem tüm analizi otomatik yapar ve tam dashboard'u kurar.</div>
    <div class="up-zone" id="drop-zone">
      <input type="file" id="file-input" accept=".xlsx,.xls">
      <div class="up-icon">📊</div>
      <div class="up-zt">Dosyayı buraya sürükleyin veya <b>tıklayın</b></div>
    </div>
    <div class="up-prog" id="up-prog">
      <div class="up-prog-bar"><div class="up-prog-fill" id="prog-fill"></div></div>
      <div class="up-prog-txt" id="prog-txt">Okunuyor...</div>
    </div>
    <button class="up-demo" id="demo-btn">Demo Verisi ile Başla →</button>
    <div class="up-fmt">Beklenen sütunlar: <b>Cihaz · xPeak (milli-g) · yPeak (milli-g) · zPeak (milli-g) · Şiddet (milli-g)</b></div>
  </div>
</div>

<!-- ══ APP ══ -->
<div id="app">
  <div class="topbar">
    <div class="tpulse"></div>
    <div class="tlogo">⚙ ForkliftIQ</div>
    <div class="tdiv"></div>
    <div class="tsub" id="t-source">—</div>
    <div class="tspc"></div>
    <div class="tstat"><div class="tsv" id="t-crit" style="color:var(--red)">0</div><div class="tsl">Kritik</div></div>
    <div class="tdiv"></div>
    <div class="tstat"><div class="tsv" id="t-warn" style="color:var(--amber)">0</div><div class="tsl">Uyarı</div></div>
    <div class="tdiv"></div>
    <div class="tstat"><div class="tsv" id="t-norm" style="color:var(--green)">0</div><div class="tsl">Normal</div></div>
    <div class="tdiv"></div>
    <div class="tstat"><div class="tsv" id="t-total">0</div><div class="tsl">Toplam</div></div>
    <div class="tdiv"></div>
    <button class="t-btn sec" id="pdf-btn">⬇ PDF Rapor</button>
    <button class="t-btn" id="newdata-btn">+ Yeni Veri</button>
    <div class="tdiv"></div>
    <div id="tclock"></div>
  </div>

  <div class="sidebar">
    <div class="sb-hdr">Risk Sıralaması</div>
    <div class="sb-list" id="device-list"></div>
  </div>

  <div class="main">
    <div class="kpi-row" id="kpi-row"></div>
    <div class="tab-bar">
      <div class="tab act" data-tab="overview">Genel Bakış</div>
      <div class="tab" data-tab="vibration">Titreşim Analizi</div>
      <div class="tab" data-tab="anomaly">Anomali Tespiti</div>
      <div class="tab" data-tab="predictive">Predictive Maint.</div>
      <div class="tab" data-tab="report">Rapor & Aksiyon</div>
      <div class="tab" data-tab="brand">🔧 Marka Analizi</div>
      <div class="tab-spacer"></div>
      <div class="tab-devname" id="tab-devname">—</div>
    </div>
    <div class="tab-content">
      <div class="tab-pane act" id="pane-overview"></div>
      <div class="tab-pane" id="pane-vibration"></div>
      <div class="tab-pane" id="pane-anomaly"></div>
      <div class="tab-pane" id="pane-predictive"></div>
      <div class="tab-pane" id="pane-report"></div>
      <div class="tab-pane" id="pane-brand"></div>
    </div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════════════════════
// GLOBAL STATE
// ══════════════════════════════════════════════════════════════
var ANALYSIS = {};
var SORTED = [];      // [[name, data], ...]
var DEVICE_MAP = {};  // index -> name  (no special-char onclick issues)
var SEL_IDX = 0;      // selected device index in SORTED
var ACTIVE_TAB = 'overview';
var CHARTS = {};
var rng = Math.random; // seeded per device for stable sim data

// ══════════════════════════════════════════════════════════════
// SAFE DEVICE SELECTION — index-based, no string in onclick
// ══════════════════════════════════════════════════════════════
function selDev(idx) {
  SEL_IDX = idx;
  renderSidebar();
  renderKPI();
  renderTab(ACTIVE_TAB);
}

function getD() { return SORTED[SEL_IDX] ? SORTED[SEL_IDX][1] : null; }
function getN() { return SORTED[SEL_IDX] ? SORTED[SEL_IDX][0] : ''; }

// ══════════════════════════════════════════════════════════════
// CLOCK
// ══════════════════════════════════════════════════════════════
(function tick() {
  var el = document.getElementById('tclock');
  if (el) {
    var n = new Date();
    el.textContent = n.toLocaleDateString('tr-TR') + ' ' + n.toLocaleTimeString('tr-TR');
  }
  setTimeout(tick, 1000);
})();

// ══════════════════════════════════════════════════════════════
// EVENT WIRING — all done in JS, no onclick strings in HTML
// ══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {
  // File input
  var fi = document.getElementById('file-input');
  fi.addEventListener('change', function() { if (fi.files[0]) handleFile(fi.files[0]); });

  // Drag & drop
  var dz = document.getElementById('drop-zone');
  dz.addEventListener('dragover', function(e) { e.preventDefault(); dz.classList.add('drag'); });
  dz.addEventListener('dragleave', function() { dz.classList.remove('drag'); });
  dz.addEventListener('drop', function(e) {
    e.preventDefault(); dz.classList.remove('drag');
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });

  // Demo button
  document.getElementById('demo-btn').addEventListener('click', loadDemo);

  // PDF button
  document.getElementById('pdf-btn').addEventListener('click', exportPDF);

  // New data button
  document.getElementById('newdata-btn').addEventListener('click', backToUpload);

  // Tabs — using data-tab attribute, no string injection
  document.querySelectorAll('.tab').forEach(function(el) {
    el.addEventListener('click', function() { switchTab(el.getAttribute('data-tab')); });
  });
});

// ══════════════════════════════════════════════════════════════
// FILE HANDLER
// ══════════════════════════════════════════════════════════════
function handleFile(file) {
  var prog = document.getElementById('up-prog');
  var fill = document.getElementById('prog-fill');
  var txt  = document.getElementById('prog-txt');
  prog.style.display = 'block';
  fill.style.background = 'linear-gradient(90deg,var(--cyan),var(--blue))';
  setProgress(fill, txt, 10, 'Dosya okunuyor...');

  var reader = new FileReader();
  reader.onerror = function() { txt.textContent = 'Dosya okunamadı.'; fill.style.background = 'var(--red)'; };
  reader.onload = function(e) {
    setProgress(fill, txt, 40, 'Excel parse ediliyor...');
    setTimeout(function() {
      try {
        var wb = XLSX.read(e.target.result, { type: 'binary' });
        if (!wb.SheetNames.length) throw new Error('Boş dosya');
        setProgress(fill, txt, 65, 'Veriler analiz ediliyor...');
        setTimeout(function() {
          var rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
          setProgress(fill, txt, 85, 'Risk skorları hesaplanıyor...');
          setTimeout(function() {
            var ok = parseAndAnalyze(rows, file.name);
            if (ok) {
              setProgress(fill, txt, 100, 'Tamamlandı!');
              setTimeout(function() { launchApp(file.name); }, 400);
            }
          }, 300);
        }, 200);
      } catch(err) {
        txt.textContent = 'Hata: ' + err.message;
        fill.style.background = 'var(--red)';
      }
    }, 100);
  };
  reader.readAsBinaryString(file);
}

function setProgress(fill, txt, pct, msg) {
  fill.style.width = pct + '%';
  txt.textContent = msg;
}

// ══════════════════════════════════════════════════════════════
// COLUMN DETECTION
// ══════════════════════════════════════════════════════════════
function detectCols(sample) {
  var keys = Object.keys(sample);
  function find() {
    var kws = Array.prototype.slice.call(arguments);
    return keys.find(function(k) {
      var kl = k.toLowerCase().replace(/\s/g,'');
      return kws.some(function(kw) { return kl.includes(kw.toLowerCase().replace(/\s/g,'')); });
    }) || null;
  }
  return {
    device: find('Cihaz','cihaz','device','makine','Device'),
    x:      find('xPeak','x_peak','XPeak','xpeak'),
    y:      find('yPeak','y_peak','YPeak','ypeak'),
    z:      find('zPeak','z_peak','ZPeak','zpeak'),
    sev:    find('Şiddet','siddet','Severity','severity','magnitude','şiddet'),
  };
}

// ══════════════════════════════════════════════════════════════
// PARSE & ANALYZE
// ══════════════════════════════════════════════════════════════
function parseAndAnalyze(rows, fname) {
  if (!rows || !rows.length) { alert('Dosya boş veya okunamadı.'); return false; }
  var cols = detectCols(rows[0]);
  if (!cols.device || !cols.x) {
    alert('Sütun adları tanınamadı.\nBeklenen: Cihaz, xPeak, yPeak, zPeak');
    return false;
  }
  var groups = {};
  rows.forEach(function(r) {
    var name = String(r[cols.device] || '').trim();
    if (!name) return;
    if (!groups[name]) groups[name] = [];
    var x = parseFloat(r[cols.x]) || 0;
    var y = parseFloat(r[cols.y]) || 0;
    var z = parseFloat(r[cols.z]) || 0;
    var s = cols.sev ? (parseFloat(r[cols.sev]) || Math.sqrt(x*x+y*y+z*z)) : Math.sqrt(x*x+y*y+z*z);
    groups[name].push({x:x, y:y, z:z, s:s});
  });
  ANALYSIS = {};
  Object.keys(groups).forEach(function(name) {
    ANALYSIS[name] = calcStats(name, groups[name]);
  });
  buildSorted();
  SEL_IDX = 0;
  document.getElementById('t-source').textContent = fname;
  updateTopbar();
  return true;
}

function buildSorted() {
  SORTED = Object.keys(ANALYSIS).map(function(k) { return [k, ANALYSIS[k]]; });
  SORTED.sort(function(a, b) { return b[1].risk_score - a[1].risk_score; });
  DEVICE_MAP = {};
  SORTED.forEach(function(pair, i) { DEVICE_MAP[i] = pair[0]; });
}

function calcStats(name, arr) {
  var axes = ['x','y','z','s'];
  var stats = {};
  axes.forEach(function(ax) {
    var vals = arr.map(function(r) { return r[ax]; }).filter(function(v) { return !isNaN(v) && v > 0; });
    if (!vals.length) { stats[ax] = {mean:0,std:0,rms:0,max:0,min:0,kurtosis:0,skewness:0,anomaly_count:0,iqr_out:0}; return; }
    var n = vals.length;
    var mean = vals.reduce(function(a,b){return a+b;},0) / n;
    var variance = vals.reduce(function(a,b){return a+(b-mean)*(b-mean);},0) / n;
    var std = Math.sqrt(variance);
    var rms = Math.sqrt(vals.reduce(function(a,b){return a+b*b;},0) / n);
    var max = Math.max.apply(null, vals);
    var min = Math.min.apply(null, vals);
    var m4 = vals.reduce(function(a,b){return a+Math.pow(b-mean,4);},0)/n;
    var kurtosis = std > 0 ? m4/(variance*variance) - 3 : 0;
    var m3 = vals.reduce(function(a,b){return a+Math.pow(b-mean,3);},0)/n;
    var skewness = std > 0 ? m3/Math.pow(std,3) : 0;
    var anomaly_count = vals.filter(function(v){return Math.abs((v-mean)/std)>3;}).length;
    var sorted2 = vals.slice().sort(function(a,b){return a-b;});
    var q1 = sorted2[Math.floor(n*0.25)], q3 = sorted2[Math.floor(n*0.75)], iqr = q3-q1;
    var iqr_out = vals.filter(function(v){return v<q1-1.5*iqr||v>q3+1.5*iqr;}).length;
    stats[ax] = {
      mean: Math.round(mean), std: Math.round(std), rms: Math.round(rms),
      max: Math.round(max), min: Math.round(min),
      kurtosis: parseFloat(kurtosis.toFixed(1)),
      skewness: parseFloat(skewness.toFixed(2)),
      anomaly_count: anomaly_count, iqr_out: iqr_out
    };
  });
  var sr = stats.s.rms;
  var health, iso, risk_level;
  if (sr < 500)      { health = 100-(sr/500)*20;          iso='Normal';   risk_level='Low'; }
  else if (sr < 1500){ health = 80-((sr-500)/1000)*30;    iso='Warning';  risk_level='Medium'; }
  else if (sr < 3000){ health = 50-((sr-1500)/1500)*30;   iso='Critical'; risk_level='High'; }
  else               { health = Math.max(0,20-((sr-3000)/1000)*10); iso='Critical'; risk_level='Critical'; }
  var totalAnom = stats.x.anomaly_count + stats.y.anomaly_count + stats.z.anomaly_count;
  var risk_score = Math.min(100, (sr/50) + (totalAnom/arr.length)*100*0.3);
  return {
    device: name, row_count: arr.length,
    stats: { X:stats.x, Y:stats.y, Z:stats.z, Severity:stats.s },
    health_index: parseFloat(health.toFixed(1)),
    iso_class: iso, risk_level: risk_level,
    risk_score: parseFloat(risk_score.toFixed(1)),
    total_anomalies: totalAnom
  };
}

// ══════════════════════════════════════════════════════════════
// DEMO DATA  (Salihli gerçek analiz sonuçları)
// ══════════════════════════════════════════════════════════════
function loadDemo() {
  ANALYSIS = {
    "Depo-2 Jung(106)":     {device:"Depo-2 Jung(106)",row_count:1443,health_index:38,iso_class:"Critical",risk_level:"High",risk_score:42.6,total_anomalies:29,stats:{X:{mean:575,std:449,rms:730,max:3440,min:32,kurtosis:2.3,skewness:0.96,anomaly_count:14,iqr_out:38},Y:{mean:1249,std:911,rms:1546,max:7552,min:32,kurtosis:1.4,skewness:0.45,anomaly_count:5,iqr_out:55},Z:{mean:979,std:725,rms:1218,max:6576,min:32,kurtosis:4.3,skewness:0.94,anomaly_count:10,iqr_out:42},Severity:{mean:1718,std:1208,rms:2099,max:10055,min:55,kurtosis:2.1,skewness:0.46,anomaly_count:4,iqr_out:60}}},
    "UYS1 Kaplama (701)":   {device:"UYS1 Kaplama (701)",row_count:6216,health_index:57.3,iso_class:"Warning",risk_level:"Medium",risk_score:26.1,total_anomalies:206,stats:{X:{mean:404,std:350,rms:535,max:6688,min:32,kurtosis:24.9,skewness:2.92,anomaly_count:87,iqr_out:210},Y:{mean:636,std:542,rms:836,max:7456,min:32,kurtosis:12.8,skewness:2.0,anomaly_count:53,iqr_out:180},Z:{mean:586,std:498,rms:769,max:7856,min:32,kurtosis:11.7,skewness:1.82,anomaly_count:66,iqr_out:195},Severity:{mean:977,std:788,rms:1255,max:10289,min:55,kurtosis:8.5,skewness:1.62,anomaly_count:50,iqr_out:220}}},
    "5163Sevkiyat Fork.(098)":{device:"5163Sevkiyat Fork.(098)",row_count:3743,health_index:71.7,iso_class:"Warning",risk_level:"Medium",risk_score:17.3,total_anomalies:220,stats:{X:{mean:254,std:328,rms:414,max:8757,min:29,kurtosis:129.9,skewness:6.92,anomaly_count:71,iqr_out:145},Y:{mean:332,std:364,rms:493,max:6438,min:31,kurtosis:23.3,skewness:2.61,anomaly_count:56,iqr_out:120},Z:{mean:265,std:348,rms:437,max:4846,min:27,kurtosis:22.7,skewness:3.77,anomaly_count:93,iqr_out:160},Severity:{mean:511,std:587,rms:778,max:11900,min:56,kurtosis:42.1,skewness:3.72,anomaly_count:84,iqr_out:175}}},
    "CıvataAyıklama Jung(076)":{device:"CıvataAyıklama Jung(076)",row_count:4284,health_index:72.8,iso_class:"Warning",risk_level:"Medium",risk_score:16.3,total_anomalies:222,stats:{X:{mean:225,std:291,rms:368,max:5104,min:32,kurtosis:37.3,skewness:4.31,anomaly_count:87,iqr_out:180},Y:{mean:246,std:326,rms:408,max:4880,min:16,kurtosis:36.7,skewness:4.45,anomaly_count:59,iqr_out:150},Z:{mean:289,std:402,rms:495,max:7552,min:32,kurtosis:50.8,skewness:5.04,anomaly_count:76,iqr_out:165},Severity:{mean:458,std:581,rms:740,max:9179,min:55,kurtosis:32.2,skewness:3.98,anomaly_count:79,iqr_out:200}}},
    "Çinko Nik-STILL-2 (732)":{device:"Çinko Nik-STILL-2 (732)",row_count:8512,health_index:72.1,iso_class:"Warning",risk_level:"Medium",risk_score:15.6,total_anomalies:95,stats:{X:{mean:298,std:485,rms:569,max:10216,min:15,kurtosis:208,skewness:12.34,anomaly_count:25,iqr_out:85},Y:{mean:275,std:316,rms:419,max:8793,min:16,kurtosis:172.6,skewness:8.1,anomaly_count:42,iqr_out:110},Z:{mean:196,std:210,rms:287,max:9310,min:52,kurtosis:784.3,skewness:20.52,anomaly_count:28,iqr_out:95},Severity:{mean:467,std:603,rms:762,max:16382,min:67,kurtosis:204.3,skewness:11.13,anomaly_count:26,iqr_out:120}}},
    "Jung FN717776":         {device:"Jung FN717776",row_count:8492,health_index:77.2,iso_class:"Warning",risk_level:"Medium",risk_score:12.4,total_anomalies:159,stats:{X:{mean:209,std:225,rms:307,max:10058,min:15,kurtosis:561,skewness:14.69,anomaly_count:40,iqr_out:110},Y:{mean:305,std:306,rms:432,max:9140,min:14,kurtosis:187,skewness:7.58,anomaly_count:39,iqr_out:130},Z:{mean:206,std:170,rms:267,max:5732,min:58,kurtosis:153.6,skewness:6.46,anomaly_count:80,iqr_out:165},Severity:{mean:438,std:401,rms:594,max:11584,min:64,kurtosis:196.7,skewness:8.21,anomaly_count:38,iqr_out:120}}},
    "Rack Forklifti (726)":  {device:"Rack Forklifti (726)",row_count:8742,health_index:80.1,iso_class:"Normal",risk_level:"Low",risk_score:10.8,total_anomalies:249,stats:{X:{mean:202,std:195,rms:281,max:1993,min:17,kurtosis:5.4,skewness:1.45,anomaly_count:80,iqr_out:200},Y:{mean:245,std:245,rms:347,max:3635,min:16,kurtosis:10.3,skewness:1.77,anomaly_count:69,iqr_out:180},Z:{mean:179,std:127,rms:220,max:2262,min:70,kurtosis:40.8,skewness:4.14,anomaly_count:100,iqr_out:220},Severity:{mean:378,std:323,rms:497,max:4416,min:76,kurtosis:10.7,skewness:1.91,anomaly_count:80,iqr_out:190}}},
    "Jung pkt(790)":         {device:"Jung pkt(790)",row_count:7789,health_index:80.8,iso_class:"Normal",risk_level:"Low",risk_score:10.5,total_anomalies:236,stats:{X:{mean:200,std:149,rms:249,max:2761,min:16,kurtosis:25.8,skewness:2.36,anomaly_count:80,iqr_out:170},Y:{mean:264,std:260,rms:370,max:8272,min:14,kurtosis:322.9,skewness:11.22,anomaly_count:37,iqr_out:140},Z:{mean:144,std:97,rms:174,max:1689,min:41,kurtosis:18.9,skewness:2.48,anomaly_count:119,iqr_out:200},Severity:{mean:374,std:299,rms:479,max:8815,min:48,kurtosis:218.7,skewness:8.45,anomaly_count:33,iqr_out:150}}},
    "Lamelli Forklift-1 (265)":{device:"Lamelli Forklift-1 (265)",row_count:4512,health_index:83.1,iso_class:"Normal",risk_level:"Low",risk_score:9.4,total_anomalies:147,stats:{X:{mean:159,std:218,rms:270,max:9197,min:16,kurtosis:651.5,skewness:16.53,anomaly_count:26,iqr_out:90},Y:{mean:166,std:223,rms:279,max:6237,min:12,kurtosis:130.1,skewness:6.57,anomaly_count:62,iqr_out:130},Z:{mean:98,std:134,rms:166,max:4870,min:18,kurtosis:364.7,skewness:12.01,anomaly_count:59,iqr_out:110},Severity:{mean:256,std:335,rms:422,max:12133,min:31,kurtosis:352.1,skewness:11.2,anomaly_count:50,iqr_out:120}}},
    "Depo Forklifti (779)":  {device:"Depo Forklifti (779)",row_count:5712,health_index:85.2,iso_class:"Normal",risk_level:"Low",risk_score:8.7,total_anomalies:248,stats:{X:{mean:110,std:193,rms:222,max:7536,min:16,kurtosis:388.7,skewness:11.65,anomaly_count:77,iqr_out:150},Y:{mean:112,std:178,rms:210,max:7648,min:14,kurtosis:578.4,skewness:15.36,anomaly_count:48,iqr_out:130},Z:{mean:103,std:182,rms:209,max:5703,min:21,kurtosis:188.2,skewness:9.1,anomaly_count:123,iqr_out:170},Severity:{mean:194,std:315,rms:370,max:12158,min:35,kurtosis:373.7,skewness:11.74,anomaly_count:87,iqr_out:160}}},
    "Çinko-Nik-STILL-1 (546)":{device:"Çinko-Nik-STILL-1 (546)",row_count:6339,health_index:85.8,iso_class:"Normal",risk_level:"Low",risk_score:8.0,total_anomalies:183,stats:{X:{mean:135,std:179,rms:224,max:7343,min:17,kurtosis:428.3,skewness:12.01,anomaly_count:40,iqr_out:100},Y:{mean:145,std:166,rms:220,max:2930,min:13,kurtosis:13.8,skewness:1.88,anomaly_count:62,iqr_out:130},Z:{mean:126,std:108,rms:166,max:3781,min:51,kurtosis:208.1,skewness:7.69,anomaly_count:81,iqr_out:150},Severity:{mean:244,std:258,rms:355,max:8764,min:57,kurtosis:190.7,skewness:6.95,anomaly_count:55,iqr_out:140}}}
  };
  buildSorted();
  SEL_IDX = 0;
  document.getElementById('t-source').textContent = 'Salihli — Demo (11 Cihaz)';
  updateTopbar();
  launchApp('Demo');
}

function launchApp(name) {
  document.getElementById('upload-screen').style.display = 'none';
  document.getElementById('app').style.display = 'grid';
  switchTab('overview');
}

function backToUpload() {
  document.getElementById('app').style.display = 'none';
  document.getElementById('upload-screen').style.display = 'flex';
  document.getElementById('up-prog').style.display = 'none';
  document.getElementById('prog-fill').style.width = '0%';
}

// ══════════════════════════════════════════════════════════════
// HELPERS
// ══════════════════════════════════════════════════════════════
function rC(s) { return s>=30 ? '#f43f5e' : s>=15 ? '#f59e0b' : '#10b981'; }
function hiC(h){ return h>79 ? '#10b981' : h>49 ? '#f59e0b' : '#f43f5e'; }
function rul(d){ return d.iso_class==='Critical' ? '7–14 gün' : d.iso_class==='Warning' ? '30–60 gün' : '90+ gün'; }
function bcl(i){ return i==='Critical'?'bc':i==='Warning'?'bw':'bn'; }
function brl(r){ return r==='Critical'||r==='High'?'bh':r==='Medium'?'bm':'bl'; }
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function sh(s,n){ return s.length>n ? s.substring(0,n-1)+'…' : s; }

function updateTopbar() {
  var v = Object.values(ANALYSIS);
  document.getElementById('t-crit').textContent = v.filter(function(d){return d.iso_class==='Critical';}).length;
  document.getElementById('t-warn').textContent = v.filter(function(d){return d.iso_class==='Warning';}).length;
  document.getElementById('t-norm').textContent = v.filter(function(d){return d.iso_class==='Normal';}).length;
  document.getElementById('t-total').textContent = v.length;
}

function dc(id) { if(CHARTS[id]){ try{CHARTS[id].destroy();}catch(e){} delete CHARTS[id]; } }

var CO_BASE = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { labels: { color:'#7a8ba8', font:{size:9}, boxWidth:8, padding:5 } } },
  scales: {
    x: { ticks:{color:'#7a8ba8',font:{size:8}}, grid:{color:'rgba(255,255,255,0.04)'}, border:{display:false} },
    y: { ticks:{color:'#7a8ba8',font:{size:8}}, grid:{color:'rgba(255,255,255,0.04)'}, border:{display:false} }
  }
};
function co(extra) {
  return Object.assign({}, CO_BASE, extra || {});
}

// Deterministic pseudo-random with seed
function seededRand(seed) {
  var s = seed;
  return function() { s = (s * 1664525 + 1013904223) & 0xffffffff; return (s >>> 0) / 4294967296; };
}

function simDist(mean, std, n, seed) {
  var rand = seededRand(seed || 42);
  var pts = [];
  for (var i = 0; i < n; i++) {
    var u1 = rand() || 0.0001, u2 = rand();
    var z = Math.sqrt(-2*Math.log(u1)) * Math.cos(2*Math.PI*u2);
    pts.push(Math.max(0, Math.round(mean + z*std)));
  }
  return pts.sort(function(a,b){return a-b;});
}

function simTrend(mean, std, n, seed) {
  var rand = seededRand(seed || 99);
  var pts = [], spike = Math.floor(n * 0.6 + rand()*n*0.3);
  for (var i = 0; i < n; i++) {
    var base = mean * (0.75 + rand()*0.5);
    if (Math.abs(i-spike) < 3) base *= (1.8 + rand());
    pts.push(Math.round(Math.max(0, base)));
  }
  return pts;
}

// ══════════════════════════════════════════════════════════════
// SIDEBAR
// ══════════════════════════════════════════════════════════════
function renderSidebar() {
  var html = '';
  for (var i = 0; i < SORTED.length; i++) {
    var name = SORTED[i][0], d = SORTED[i][1];
    var act = (i === SEL_IDX) ? 'act' : '';
    html += '<div class="dcard ' + act + '" data-idx="' + i + '">' +
      '<div class="dname" title="' + esc(name) + '">' + esc(name) + '</div>' +
      '<div class="drow">' +
        '<span class="badge ' + bcl(d.iso_class) + '">' + d.iso_class + '</span>' +
        '<span class="badge ' + brl(d.risk_level) + '">' + d.risk_level + '</span>' +
      '</div>' +
      '<div class="dbar"><div class="dbar-fill" style="width:' + d.risk_score + '%;background:' + rC(d.risk_score) + '"></div></div>' +
      '<div class="dmeta">' +
        '<span>Risk <b style="color:' + rC(d.risk_score) + '">' + d.risk_score.toFixed(1) + '</b></span>' +
        '<span>H <b style="color:' + hiC(d.health_index) + '">' + d.health_index.toFixed(0) + '</b></span>' +
        '<span>⚠' + d.total_anomalies + '</span>' +
      '</div>' +
    '</div>';
  }
  var list = document.getElementById('device-list');
  list.innerHTML = html;
  // Wire click events using index — no string injection
  list.querySelectorAll('.dcard').forEach(function(el) {
    el.addEventListener('click', function() { selDev(parseInt(el.getAttribute('data-idx'), 10)); });
  });
}

// ══════════════════════════════════════════════════════════════
// KPI ROW
// ══════════════════════════════════════════════════════════════
function renderKPI() {
  var d = getD(); if (!d) return;
  var s = d.stats;
  var vals = Object.values(ANALYSIS);
  var avgH = (vals.reduce(function(a,b){return a+b.health_index;},0)/vals.length).toFixed(0);
  var devName = getN();
  document.getElementById('tab-devname').textContent = sh(devName, 22);
  document.getElementById('kpi-row').innerHTML =
    kpiCard('Health Index', d.health_index.toFixed(0) + '<span style="font-size:12px;color:var(--text2)">/100</span>', d.health_index>79?'✓ Sağlıklı':d.health_index>49?'⚠ Dikkat':'✗ KRİTİK', hiC(d.health_index)) +
    kpiCard('Failure Risk', d.risk_score.toFixed(1), d.risk_level + ' Risk', rC(d.risk_score)) +
    kpiCard('Severity RMS', d.stats.Severity.rms + '<span style="font-size:11px;color:var(--text2)"> mg</span>', 'Max: ' + d.stats.Severity.max + ' mg', 'var(--cyan)') +
    kpiCard('Toplam Anomali', d.total_anomalies, d.row_count.toLocaleString('tr-TR') + ' ölçüm', 'var(--amber)') +
    kpiCard('Filo Ort. Sağlık', avgH, vals.length + ' cihaz', 'var(--purple)');
}

function kpiCard(lbl, val, sub, color) {
  return '<div class="kpi" style="border-top-color:' + color + '">' +
    '<div class="kpi-l">' + lbl + '</div>' +
    '<div class="kpi-v" style="color:' + color + '">' + val + '</div>' +
    '<div class="kpi-s">' + sub + '</div>' +
    '</div>';
}

// ══════════════════════════════════════════════════════════════
// TAB SWITCH
// ══════════════════════════════════════════════════════════════
function switchTab(tab) {
  ACTIVE_TAB = tab;
  document.querySelectorAll('.tab').forEach(function(el) {
    el.classList.toggle('act', el.getAttribute('data-tab') === tab);
  });
  document.querySelectorAll('.tab-pane').forEach(function(el) {
    el.classList.remove('act');
  });
  document.getElementById('pane-' + tab).classList.add('act');
  renderSidebar();
  renderKPI();
  renderTab(tab);
}

function renderTab(tab) {
  if (tab === 'overview')   renderOverview();
  else if (tab === 'vibration')  renderVibration();
  else if (tab === 'anomaly')    renderAnomaly();
  else if (tab === 'predictive') renderPredictive();
  else if (tab === 'report')     renderReport();
  else if (tab === 'brand')      renderBrand();
}

// ══════════════════════════════════════════════════════════════
// TAB 1 — GENEL BAKIŞ
// ══════════════════════════════════════════════════════════════
function renderOverview() {
  var pane = document.getElementById('pane-overview');
  var top3 = SORTED.slice(0,3);
  var podColors = ['rgba(244,63,94,0.12)','rgba(245,158,11,0.1)','rgba(59,130,246,0.08)'];
  var podBorders = ['rgba(244,63,94,0.4)','rgba(245,158,11,0.3)','rgba(59,130,246,0.25)'];

  var podHTML = '<div class="podium">';
  top3.forEach(function(pair, i) {
    var n=pair[0], d=pair[1];
    podHTML += '<div class="pod" style="background:'+podColors[i]+';border-color:'+podBorders[i]+'">' +
      '<div class="pod-rank">'+(i+1)+'</div>' +
      '<div class="pod-name" title="'+esc(n)+'">'+esc(n)+'</div>' +
      '<div class="pod-score" style="color:'+rC(d.risk_score)+'">'+d.risk_score.toFixed(1)+'</div>' +
      '<div class="pod-lbl">Risk Skoru</div>' +
      '<div style="margin-top:6px;display:flex;gap:4px;justify-content:center;">' +
        '<span class="badge '+bcl(d.iso_class)+'">'+d.iso_class+'</span>' +
        '<span style="font-size:9px;color:'+hiC(d.health_index)+'">H:'+d.health_index.toFixed(0)+'</span>' +
      '</div></div>';
  });
  podHTML += '</div>';

  pane.innerHTML = podHTML +
    '<div class="g2">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--red)"></div>Risk Skoru Sıralaması</div><div class="cw"><canvas id="ch-rank" height="220" role="img" aria-label="rank"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--cyan)"></div>ISO 20816 Sınıf Dağılımı</div><div class="cw"><canvas id="ch-iso" height="220" role="img" aria-label="iso"></canvas></div></div>' +
    '</div>' +
    '<div class="g2">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--amber)"></div>Fleet Health Index Karşılaştırması</div><div class="cw"><canvas id="ch-health" height="180" role="img" aria-label="health"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--purple)"></div>Severity RMS — Tüm Cihazlar</div><div class="cw"><canvas id="ch-sev" height="180" role="img" aria-label="sev"></canvas></div></div>' +
    '</div>';

  setTimeout(function() {
    // Risk rank
    dc('rank');
    var labels = SORTED.map(function(p){return sh(p[0],12);});
    var rdata  = SORTED.map(function(p){return p[1].risk_score;});
    var rcolors= SORTED.map(function(p){return rC(p[1].risk_score);});
    CHARTS['rank'] = new Chart(document.getElementById('ch-rank'), {
      type:'bar', data:{labels:labels, datasets:[{data:rdata, backgroundColor:rcolors, borderWidth:0, borderRadius:4}]},
      options: Object.assign({}, CO_BASE, {indexAxis:'y', plugins:{legend:{display:false}},
        scales:{y:{ticks:{color:'#7a8ba8',font:{size:8}},grid:{display:false},border:{display:false}},
                x:{ticks:{color:'#7a8ba8',font:{size:8}},grid:{color:'rgba(255,255,255,0.04)'},border:{display:false},max:100}}})
    });

    // ISO pie
    dc('iso');
    var vals = Object.values(ANALYSIS);
    var cnts = {Normal:0, Warning:0, Critical:0};
    vals.forEach(function(d){ cnts[d.iso_class]++; });
    CHARTS['iso'] = new Chart(document.getElementById('ch-iso'), {
      type:'doughnut',
      data:{labels:['Normal','Warning','Critical'], datasets:[{data:[cnts.Normal,cnts.Warning,cnts.Critical],
        backgroundColor:['rgba(16,185,129,0.85)','rgba(245,158,11,0.85)','rgba(244,63,94,0.85)'],borderWidth:0,borderRadius:4}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:'60%',
        plugins:{legend:{position:'right',labels:{color:'#7a8ba8',font:{size:10},boxWidth:10,padding:8}}}}
    });

    // Health all
    dc('health');
    CHARTS['health'] = new Chart(document.getElementById('ch-health'), {
      type:'bar',
      data:{labels:SORTED.map(function(p){return sh(p[0],10);}),
        datasets:[{label:'Health Index', data:SORTED.map(function(p){return p[1].health_index;}),
          backgroundColor:SORTED.map(function(p){return hiC(p[1].health_index)+'cc';}), borderWidth:0, borderRadius:3}]},
      options: Object.assign({}, CO_BASE, {plugins:{legend:{display:false}}, scales:Object.assign({},CO_BASE.scales,{y:{ticks:{color:'#7a8ba8',font:{size:8}},grid:{color:'rgba(255,255,255,0.04)'},border:{display:false},max:100,min:0}})})
    });

    // Severity all
    dc('sev');
    CHARTS['sev'] = new Chart(document.getElementById('ch-sev'), {
      type:'bar',
      data:{labels:SORTED.map(function(p){return sh(p[0],10);}),
        datasets:[{label:'Severity RMS (mg)', data:SORTED.map(function(p){return p[1].stats.Severity.rms;}),
          backgroundColor:'rgba(167,139,250,0.65)', borderWidth:0, borderRadius:3}]},
      options: Object.assign({}, CO_BASE, {plugins:{legend:{display:false}}})
    });
  }, 30);
}

// ══════════════════════════════════════════════════════════════
// TAB 2 — TİTREŞİM ANALİZİ
// ══════════════════════════════════════════════════════════════
function renderVibration() {
  var d = getD(), s = d.stats, n = getN();
  var seed = n.length * 137;

  document.getElementById('pane-vibration').innerHTML =
    '<div class="g3">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--blue)"></div>X Ekseni — Peak Dağılımı</div><div class="cw"><canvas id="ch-xd" height="160" role="img" aria-label="xd"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--amber)"></div>Y Ekseni — Peak Dağılımı</div><div class="cw"><canvas id="ch-yd" height="160" role="img" aria-label="yd"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--red)"></div>Z Ekseni — Peak Dağılımı</div><div class="cw"><canvas id="ch-zd" height="160" role="img" aria-label="zd"></canvas></div></div>' +
    '</div>' +
    '<div class="g2">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--cyan)"></div>X / Y / Z — Mean · RMS · Std</div><div class="cw"><canvas id="ch-rms" height="170" role="img" aria-label="rms"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--purple)"></div>Detaylı İstatistik Tablosu</div>' +
        '<div style="overflow-x:auto"><table class="stbl">' +
          '<thead><tr><th>Eksen</th><th>Ort.</th><th>Std</th><th>RMS</th><th>Max</th><th>Kurt.</th><th>Skew.</th></tr></thead>' +
          '<tbody>' +
            ['X','Y','Z','Severity'].map(function(ax){
              return '<tr><td>'+ax+'</td><td>'+s[ax].mean+'</td><td>'+s[ax].std+'</td><td style="color:var(--cyan)">'+s[ax].rms+'</td><td style="color:var(--red)">'+s[ax].max+'</td><td>'+s[ax].kurtosis+'</td><td>'+s[ax].skewness+'</td></tr>';
            }).join('') +
          '</tbody></table></div>' +
        '<div style="margin-top:12px"><div class="ct"><div class="ctd" style="background:var(--green)"></div>Kurtosis Karşılaştırması</div><div class="cw"><canvas id="ch-kurt" height="90" role="img" aria-label="kurt"></canvas></div></div>' +
      '</div>' +
    '</div>' +
    '<div class="card"><div class="ct"><div class="ctd" style="background:var(--blue)"></div>X · Y · Z — Şiddet Trendi (Simüle)</div><div class="cw"><canvas id="ch-trend" height="120" role="img" aria-label="trend"></canvas></div></div>';

  setTimeout(function() {
    var axDefs = [
      {id:'ch-xd', ax:'X', as:s.X, color:'rgba(59,130,246,0.7)'},
      {id:'ch-yd', ax:'Y', as:s.Y, color:'rgba(245,158,11,0.7)'},
      {id:'ch-zd', ax:'Z', as:s.Z, color:'rgba(244,63,94,0.7)'},
    ];
    axDefs.forEach(function(def, i) {
      dc(def.id);
      var vals = simDist(def.as.mean, def.as.std, 50, seed + i*31);
      CHARTS[def.id] = new Chart(document.getElementById(def.id), {
        type:'bar', data:{labels:vals.map(function(_,j){return j+1;}), datasets:[{label:def.ax+' Peak (mg)', data:vals, backgroundColor:def.color, borderWidth:0, borderRadius:1}]},
        options: Object.assign({}, CO_BASE, {plugins:{legend:{display:false}}, scales:{x:{display:false}, y:{ticks:{color:'#7a8ba8',font:{size:8}},grid:{color:'rgba(255,255,255,0.04)'},border:{display:false}}}})
      });
    });

    dc('rms');
    CHARTS['rms'] = new Chart(document.getElementById('ch-rms'), {
      type:'bar',
      data:{labels:['X','Y','Z'], datasets:[
        {label:'Mean', data:[s.X.mean,s.Y.mean,s.Z.mean], backgroundColor:'rgba(59,130,246,0.65)', borderWidth:0, borderRadius:3},
        {label:'RMS',  data:[s.X.rms, s.Y.rms, s.Z.rms],  backgroundColor:'rgba(245,158,11,0.7)',  borderWidth:0, borderRadius:3},
        {label:'Std',  data:[s.X.std, s.Y.std, s.Z.std],  backgroundColor:'rgba(122,139,168,0.4)', borderWidth:0, borderRadius:3},
      ]},
      options: CO_BASE
    });

    dc('kurt');
    CHARTS['kurt'] = new Chart(document.getElementById('ch-kurt'), {
      type:'bar',
      data:{labels:['X','Y','Z'], datasets:[{label:'Kurtosis', data:[s.X.kurtosis,s.Y.kurtosis,s.Z.kurtosis],
        backgroundColor:['rgba(59,130,246,0.7)','rgba(245,158,11,0.7)','rgba(244,63,94,0.7)'], borderWidth:0, borderRadius:3}]},
      options: Object.assign({}, CO_BASE, {plugins:{legend:{display:false}}})
    });

    var tN = 50, tLabels = [], tX=[], tY=[], tZ=[];
    var tr = seededRand(seed + 7);
    for (var i=0;i<tN;i++) {
      tLabels.push('T'+i);
      tX.push(Math.round(Math.max(0, s.X.mean*(0.6+tr()*0.8))));
      tY.push(Math.round(Math.max(0, s.Y.mean*(0.6+tr()*0.8))));
      tZ.push(Math.round(Math.max(0, s.Z.mean*(0.6+tr()*0.8))));
    }
    dc('trend');
    CHARTS['trend'] = new Chart(document.getElementById('ch-trend'), {
      type:'line',
      data:{labels:tLabels, datasets:[
        {label:'X',data:tX,borderColor:'rgba(59,130,246,0.8)', backgroundColor:'rgba(59,130,246,0.05)', borderWidth:1.5, pointRadius:0, tension:0.4, fill:true},
        {label:'Y',data:tY,borderColor:'rgba(245,158,11,0.8)',  backgroundColor:'rgba(245,158,11,0.05)',  borderWidth:1.5, pointRadius:0, tension:0.4, fill:true},
        {label:'Z',data:tZ,borderColor:'rgba(244,63,94,0.8)',   backgroundColor:'rgba(244,63,94,0.05)',   borderWidth:1.5, pointRadius:0, tension:0.4, fill:true},
      ]},
      options: CO_BASE
    });
  }, 30);
}

// ══════════════════════════════════════════════════════════════
// TAB 3 — ANOMALİ TESPİTİ
// ══════════════════════════════════════════════════════════════
function renderAnomaly() {
  var d = getD(), s = d.stats, n = getN();
  var seed = n.length * 211;

  var atRows = SORTED.map(function(pair, i) {
    var nm=pair[0], dd=pair[1];
    var pct = (dd.total_anomalies/dd.row_count*100).toFixed(1);
    return '<tr>' +
      '<td style="font-weight:600;color:var(--text);max-width:130px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(sh(nm,16))+'</td>' +
      '<td>'+dd.stats.X.anomaly_count+'</td>' +
      '<td>'+dd.stats.Y.anomaly_count+'</td>' +
      '<td>'+dd.stats.Z.anomaly_count+'</td>' +
      '<td style="font-weight:600;color:var(--amber)">'+dd.total_anomalies+'</td>' +
      '<td>'+pct+'%</td>' +
      '<td><span class="pill" style="background:'+rC(dd.risk_score)+'22;color:'+rC(dd.risk_score)+'">'+dd.risk_score.toFixed(1)+'</span></td>' +
      '<td><span class="badge '+bcl(dd.iso_class)+'">'+dd.iso_class+'</span></td>' +
    '</tr>';
  }).join('');

  document.getElementById('pane-anomaly').innerHTML =
    '<div class="g4" style="margin-bottom:10px">' +
      '<div class="card"><div class="kpi-l">X Anomali</div><div class="kpi-v" style="color:var(--blue)">'+s.X.anomaly_count+'</div><div class="kpi-s">Z-score &gt; 3σ</div></div>' +
      '<div class="card"><div class="kpi-l">Y Anomali</div><div class="kpi-v" style="color:var(--amber)">'+s.Y.anomaly_count+'</div><div class="kpi-s">Z-score &gt; 3σ</div></div>' +
      '<div class="card"><div class="kpi-l">Z Anomali</div><div class="kpi-v" style="color:var(--red)">'+s.Z.anomaly_count+'</div><div class="kpi-s">Z-score &gt; 3σ</div></div>' +
      '<div class="card"><div class="kpi-l">IQR Dışı</div><div class="kpi-v" style="color:var(--purple)">'+s.Severity.iqr_out+'</div><div class="kpi-s">1.5× IQR filtresi</div></div>' +
    '</div>' +
    '<div class="g2">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--red)"></div>Eksen Bazlı Anomali (Z>3σ & IQR)</div><div class="cw"><canvas id="ch-ab" height="180" role="img" aria-label="ab"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--amber)"></div>Cihaz Bazlı Anomali Yoğunluğu (%)</div><div class="cw"><canvas id="ch-ad" height="180" role="img" aria-label="ad"></canvas></div></div>' +
    '</div>' +
    '<div class="card" style="margin-bottom:10px"><div class="ct"><div class="ctd" style="background:var(--cyan)"></div>Anomali Zaman Serisi (Simüle) — Spike Noktaları</div><div class="cw"><canvas id="ch-ats" height="120" role="img" aria-label="ats"></canvas></div></div>' +
    '<div class="card"><div class="ct"><div class="ctd" style="background:var(--purple)"></div>Tüm Cihazlar — Anomali & Risk Matrisi</div>' +
      '<div style="overflow-x:auto"><table class="atable">' +
        '<thead><tr><th>Cihaz</th><th>X Anom.</th><th>Y Anom.</th><th>Z Anom.</th><th>Toplam</th><th>Oran</th><th>Risk</th><th>ISO</th></tr></thead>' +
        '<tbody>'+atRows+'</tbody>' +
      '</table></div>' +
    '</div>';

  setTimeout(function() {
    dc('ab');
    CHARTS['ab'] = new Chart(document.getElementById('ch-ab'), {
      type:'bar',
      data:{labels:['X','Y','Z'], datasets:[
        {label:'Z-score >3σ', data:[s.X.anomaly_count,s.Y.anomaly_count,s.Z.anomaly_count], backgroundColor:['rgba(59,130,246,0.8)','rgba(245,158,11,0.8)','rgba(244,63,94,0.8)'], borderWidth:0, borderRadius:4},
        {label:'IQR Dışı',   data:[s.X.iqr_out,s.Y.iqr_out,s.Z.iqr_out], backgroundColor:['rgba(59,130,246,0.3)','rgba(245,158,11,0.3)','rgba(244,63,94,0.3)'], borderWidth:0, borderRadius:4},
      ]},
      options: CO_BASE
    });

    dc('ad');
    CHARTS['ad'] = new Chart(document.getElementById('ch-ad'), {
      type:'bar',
      data:{labels:SORTED.map(function(p){return sh(p[0],9);}),
        datasets:[{label:'Anomali %', data:SORTED.map(function(p){return parseFloat((p[1].total_anomalies/p[1].row_count*100).toFixed(2));}),
          backgroundColor:SORTED.map(function(p){return rC(p[1].risk_score)+'aa';}), borderWidth:0, borderRadius:3}]},
      options: Object.assign({}, CO_BASE, {plugins:{legend:{display:false}}})
    });

    // Simulated anomaly time series
    var atN=60, atVals=[], atAnoms=[], atLabels=[];
    var ar = seededRand(seed+3), spikePos = Math.floor(ar()*40)+10;
    for (var i=0;i<atN;i++) {
      atLabels.push('T'+i);
      var base = s.Severity.mean*(0.7+ar()*0.6);
      var isAnom = Math.abs(i-spikePos)<4 || (ar()<0.05);
      var val = Math.round(isAnom ? base*(1.8+ar()*1.2) : base);
      atVals.push(Math.max(0,val));
      atAnoms.push(isAnom ? Math.max(0,val) : null);
    }
    dc('ats');
    CHARTS['ats'] = new Chart(document.getElementById('ch-ats'), {
      type:'line',
      data:{labels:atLabels, datasets:[
        {label:'Severity (mg)',data:atVals,borderColor:'rgba(34,211,238,0.6)',backgroundColor:'rgba(34,211,238,0.05)',borderWidth:1.5,pointRadius:0,tension:0.3,fill:true},
        {label:'Anomali',data:atAnoms,borderColor:'transparent',backgroundColor:'transparent',pointBackgroundColor:'rgba(244,63,94,0.9)',pointRadius:5,showLine:false},
      ]},
      options: CO_BASE
    });
  }, 30);
}

// ══════════════════════════════════════════════════════════════
// TAB 4 — PREDİCTİVE MAINTENANCE
// ══════════════════════════════════════════════════════════════
function renderPredictive() {
  var d = getD(), s = d.stats;

  // Build timeline HTML
  var tlItems = '';
  var tlColors = {Critical:'var(--red)',High:'var(--red)',Medium:'var(--amber)',Low:'var(--green)'};
  SORTED.slice(0,7).forEach(function(pair, i) {
    var nm=pair[0], dd=pair[1];
    var days = dd.iso_class==='Critical' ? 7+i*2 : dd.iso_class==='Warning' ? 30+i*8 : 90+i*15;
    var dt = new Date(); dt.setDate(dt.getDate()+days);
    var label = dd.iso_class==='Critical' ? 'Acil servis gerekli' : dd.iso_class==='Warning' ? 'Planlı bakım' : 'Rutin kontrol';
    tlItems += '<div class="tl-item">' +
      '<div class="tl-dot" style="background:'+tlColors[dd.risk_level]+'"></div>' +
      '<div class="tl-time">'+dt.toLocaleDateString('tr-TR')+' (+'+days+' gün)</div>' +
      '<div class="tl-txt">'+esc(nm)+' <span class="tl-b" style="color:'+rC(dd.risk_score)+'">Risk: '+dd.risk_score.toFixed(1)+'</span></div>' +
      '<div style="font-size:9px;color:var(--text3);margin-top:1px">'+label+'</div>' +
    '</div>';
  });

  document.getElementById('pane-predictive').innerHTML =
    '<div class="g3" style="margin-bottom:10px">' +
      '<div class="card" style="text-align:center">' +
        '<div class="ct" style="justify-content:center"><div class="ctd" style="background:var(--green)"></div>Health Index</div>' +
        '<div class="gauge-wrap"><svg class="gauge-svg" width="130" height="72" id="gauge-svg" role="img" aria-label="gauge"></svg><div class="gauge-val" id="gauge-val">—</div><div class="gauge-lbl" id="gauge-lbl">—</div></div>' +
      '</div>' +
      '<div class="rul-box">' +
        '<div class="ct" style="justify-content:center"><div class="ctd" style="background:var(--cyan)"></div>Kalan Kullanım Ömrü (RUL)</div>' +
        '<div class="rul-v" id="rul-v">—</div>' +
        '<div class="rul-l">Remaining Useful Life</div>' +
        '<div class="rul-sub" id="rul-sub">—</div>' +
      '</div>' +
      '<div class="card" style="text-align:center">' +
        '<div class="ct" style="justify-content:center"><div class="ctd" style="background:var(--red)"></div>Failure Risk Score</div>' +
        '<div style="position:relative;width:110px;height:110px;margin:0 auto">' +
          '<canvas id="ch-rg" width="110" height="110" role="img" aria-label="risk gauge"></canvas>' +
          '<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">' +
            '<div id="rg-val" style="font-size:22px;font-weight:800">—</div>' +
            '<div style="font-size:9px;color:var(--text2)">/100</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>' +
    '<div class="g2">' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--amber)"></div>Risk Seviyesi Dağılımı — Filo</div><div class="cw"><canvas id="ch-rdist" height="180" role="img" aria-label="rdist"></canvas></div></div>' +
      '<div class="card"><div class="ct"><div class="ctd" style="background:var(--blue)"></div>Health vs Risk — Scatter</div><div class="cw"><canvas id="ch-sc" height="180" role="img" aria-label="scatter"></canvas></div></div>' +
    '</div>' +
    '<div class="card"><div class="ct"><div class="ctd" style="background:var(--purple)"></div>Bakım Öncelik Zaman Çizelgesi</div><div class="tl" id="pm-tl">'+tlItems+'</div></div>';

  // Gauge
  var hi = d.health_index;
  var gaugeColor = hiC(hi);
  var DEG = function(a){ return a*Math.PI/180; };
  var cx=65, cy=65, r=50;
  var startAngle = -210, endAngle = startAngle + hi*2.4;
  var sa = DEG(startAngle), ea = DEG(endAngle), fullEnd = DEG(startAngle+240);
  var bgX1=cx+r*Math.cos(sa), bgY1=cy+r*Math.sin(sa), bgX2=cx+r*Math.cos(fullEnd), bgY2=cy+r*Math.sin(fullEnd);
  var fgX2=cx+r*Math.cos(ea), fgY2=cy+r*Math.sin(ea);
  var bgLarge=1, fgLarge=(hi>50)?1:0;
  document.getElementById('gauge-svg').innerHTML =
    '<path d="M'+bgX1+' '+bgY1+' A'+r+' '+r+' 0 '+bgLarge+' 1 '+bgX2+' '+bgY2+'" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="9" stroke-linecap="round"/>' +
    (hi>0 ? '<path d="M'+bgX1+' '+bgY1+' A'+r+' '+r+' 0 '+fgLarge+' 1 '+fgX2+' '+fgY2+'" fill="none" stroke="'+gaugeColor+'" stroke-width="9" stroke-linecap="round"/>' : '');
  document.getElementById('gauge-val').textContent = hi.toFixed(0);
  document.getElementById('gauge-val').style.color = gaugeColor;
  document.getElementById('gauge-lbl').textContent = hi>79?'Sağlıklı':hi>49?'Dikkat':'KRİTİK';
  document.getElementById('rul-v').textContent = rul(d);
  document.getElementById('rul-sub').textContent =
    d.iso_class==='Critical' ? 'Acil bakım — 7 gün içinde servis' :
    d.iso_class==='Warning'  ? 'Planlı bakım — 30–60 gün içinde' :
    'Rutin bakım yeterli — 3 aylık periyot';

  setTimeout(function() {
    dc('rg');
    CHARTS['rg'] = new Chart(document.getElementById('ch-rg'), {
      type:'doughnut',
      data:{datasets:[{data:[d.risk_score, 100-d.risk_score],
        backgroundColor:[rC(d.risk_score)+'cc','rgba(255,255,255,0.05)'],
        borderWidth:0, cutout:'72%', circumference:270, rotation:-135}]},
      options:{responsive:false,plugins:{legend:{display:false},tooltip:{enabled:false}}}
    });
    document.getElementById('rg-val').textContent = d.risk_score.toFixed(1);
    document.getElementById('rg-val').style.color = rC(d.risk_score);

    dc('rdist');
    var rcounts = {Low:0,Medium:0,High:0,Critical:0};
    Object.values(ANALYSIS).forEach(function(dd){ rcounts[dd.risk_level]++; });
    CHARTS['rdist'] = new Chart(document.getElementById('ch-rdist'), {
      type:'doughnut',
      data:{labels:['Low','Medium','High','Critical'],
        datasets:[{data:[rcounts.Low||0,rcounts.Medium||0,rcounts.High||0,rcounts.Critical||0],
          backgroundColor:['rgba(16,185,129,0.85)','rgba(245,158,11,0.85)','rgba(244,63,94,0.75)','rgba(244,63,94,1)'],
          borderWidth:0,borderRadius:4}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:'55%',
        plugins:{legend:{position:'right',labels:{color:'#7a8ba8',font:{size:9},boxWidth:9,padding:6}}}}
    });

    dc('sc');
    var scData = Object.values(ANALYSIS).map(function(dd){ return {x:dd.health_index,y:dd.risk_score}; });
    var scColors = Object.values(ANALYSIS).map(function(dd){ return rC(dd.risk_score)+'bb'; });
    CHARTS['sc'] = new Chart(document.getElementById('ch-sc'), {
      type:'scatter',
      data:{datasets:[{label:'Cihazlar', data:scData, backgroundColor:scColors, pointRadius:6, pointHoverRadius:8}]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false}},
        scales:{
          x:{title:{display:true,text:'Health Index',color:'#7a8ba8',font:{size:9}},ticks:{color:'#7a8ba8',font:{size:8}},grid:{color:'rgba(255,255,255,0.04)'},border:{display:false}},
          y:{title:{display:true,text:'Risk Score',color:'#7a8ba8',font:{size:9}},ticks:{color:'#7a8ba8',font:{size:8}},grid:{color:'rgba(255,255,255,0.04)'},border:{display:false}}
        }}
    });
  }, 30);
}

// ══════════════════════════════════════════════════════════════
// TAB 5 — RAPOR & AKSİYON
// ══════════════════════════════════════════════════════════════
function renderReport() {
  var d = getD(), s = d.stats, n = getN();
  var vals = Object.values(ANALYSIS);
  var now = new Date().toLocaleDateString('tr-TR');

  var avgRisk  = (vals.reduce(function(a,b){return a+b.risk_score;},0)/vals.length).toFixed(1);
  var avgHealth= (vals.reduce(function(a,b){return a+b.health_index;},0)/vals.length).toFixed(0);

  // Actions
  var acts = [];
  if (vals.some(function(x){return x.iso_class==='Critical';}))
    acts.push({c:'ared', t:'ACİL: Kritik cihazlar için motor ve tahrik sistemi derhal incelenmeli'});
  if (d.stats.Y.rms > 800)
    acts.push({c:'ared', t:'Rulman/yatak arızası riski — Y ekseni titreşimi kritik seviyede'});
  if (d.stats.Z.rms > 600)
    acts.push({c:'aamb', t:'Z ekseni dikey yük sistemi kontrol edilmeli (motor yükü)'});
  if (d.total_anomalies > 150)
    acts.push({c:'aamb', t:'Yüksek anomali yoğunluğu — hidrolik sistem basınç & sızdırmazlık'});
  acts.push({c:'ablu', t:'Tüm cihazlar: tekerlek, lastik ve aks bağlantı vidaları kontrolü'});
  acts.push({c:'ablu', t:'Fork kol bağlantı vidaları ve torklama periyodik kontrolü'});
  acts.push({c:'agrn', t:'Aylık titreşim izleme ve trend raporlama planı oluşturulmalı'});

  var critList = SORTED.filter(function(p){return p[1].iso_class==='Critical'||p[1].risk_score>=20;});

  document.getElementById('pane-report').innerHTML =
    '<div class="rep-hdr">' +
      '<div class="rep-icon">📋</div>' +
      '<div class="rep-meta">' +
        '<div class="rep-title">'+esc(n)+' — Titreşim Analiz Raporu</div>' +
        '<div class="rep-sub">'+now+' · ISO 20816 · '+d.row_count.toLocaleString('tr-TR')+' ölçüm · '+d.iso_class+' Sınıf</div>' +
      '</div>' +
      '<button class="rep-btn" id="rep-pdf-btn">⬇ PDF İndir</button>' +
    '</div>' +
    '<div class="rep-sec">Filo Özeti</div>' +
    '<div class="rep-grid">' +
      ['Toplam Cihaz|'+vals.length+'||var(--text)',
       'Kritik Cihaz|'+vals.filter(function(x){return x.iso_class==='Critical';}).length+'|Acil bakım|var(--red)',
       'Uyarı Cihazı|'+vals.filter(function(x){return x.iso_class==='Warning';}).length+'|Planlı bakım|var(--amber)',
       'Normal Cihaz|'+vals.filter(function(x){return x.iso_class==='Normal';}).length+'|Rutin kontrol|var(--green)',
       'Ort. Risk Skoru|'+avgRisk+'|/100|var(--cyan)',
       'Ort. Sağlık İnd.|'+avgHealth+'|/100|var(--purple)',
      ].map(function(row){
        var p=row.split('|');
        return '<div class="rc"><div class="rc-l">'+p[0]+'</div><div class="rc-v" style="color:'+p[3]+'">'+p[1]+'</div><div class="rc-s">'+p[2]+'</div></div>';
      }).join('') +
    '</div>' +
    '<div class="g2">' +
      '<div>' +
        '<div class="rep-sec">Yüksek Riskli Cihazlar</div>' +
        (critList.length ? critList.map(function(pair){
          var nm=pair[0], dd=pair[1];
          return '<div class="insight" style="border-left:3px solid '+rC(dd.risk_score)+';margin-bottom:6px">' +
            '<div class="insight-h" style="color:'+rC(dd.risk_score)+'">⚠ '+esc(nm)+'</div>' +
            '<div class="insight-b">Risk: '+dd.risk_score.toFixed(1)+' · Health: '+dd.health_index.toFixed(0)+' · RMS: '+dd.stats.Severity.rms+' mg · Anomali: '+dd.total_anomalies+' · RUL: '+rul(dd)+'</div>' +
          '</div>';
        }).join('') : '<div style="color:var(--text3);font-size:11px;padding:8px">Yüksek riskli cihaz yok.</div>') +
      '</div>' +
      '<div>' +
        '<div class="rep-sec">Bakım Aksiyon Planı</div>' +
        '<div class="insight">' +
          acts.map(function(a){return '<div class="arow"><div class="adot '+a.c+'"></div><div class="atxt">'+a.t+'</div></div>';}).join('') +
        '</div>' +
      '</div>' +
    '</div>' +
    '<div class="rep-sec">Seçili Cihaz Detay Analizi — '+esc(sh(n,30))+'</div>' +
    '<div class="g4">' +
      ['X','Y','Z','Severity'].map(function(ax){
        return '<div class="rc">' +
          '<div class="rc-l">'+ax+' Ekseni</div>' +
          '<div class="rc-v" style="color:var(--cyan)">'+s[ax].rms+'</div>' +
          '<div class="rc-s">mg RMS</div>' +
          '<div style="margin-top:8px;font-size:10px;color:var(--text2)">Ort: '+s[ax].mean+' · Std: '+s[ax].std+'</div>' +
          '<div style="font-size:10px;color:var(--text2)">Max: '+s[ax].max+' · Kurt: '+s[ax].kurtosis+'</div>' +
          '<div style="font-size:10px;color:var(--amber)">Anomali: '+s[ax].anomaly_count+'</div>' +
        '</div>';
      }).join('') +
    '</div>' +
    '<div class="rep-sec">ISO 20816 Standart Eşikleri</div>' +
    '<div class="g3">' +
      [['✅','< 500 mg RMS','Normal — Titreşim kabul edilebilir sınırda','var(--green)'],
       ['⚠','500–1500 mg RMS','Uyarı — Planlı bakım gereklidir','var(--amber)'],
       ['🔴','> 1500 mg RMS','Kritik — Acil müdahale zorunlu','var(--red)'],
      ].map(function(row){
        return '<div class="rc" style="text-align:center">' +
          '<div style="font-size:24px;margin-bottom:6px">'+row[0]+'</div>' +
          '<div class="rc-v" style="color:'+row[3]+';font-size:14px">'+row[1]+'</div>' +
          '<div style="font-size:10px;color:var(--text2);margin-top:4px;line-height:1.4">'+row[2]+'</div>' +
        '</div>';
      }).join('') +
    '</div>';

  // Wire PDF button safely
  setTimeout(function() {
    var btn = document.getElementById('rep-pdf-btn');
    if (btn) btn.addEventListener('click', exportPDF);
  }, 10);
}

// ══════════════════════════════════════════════════════════════
// PDF EXPORT
// ══════════════════════════════════════════════════════════════
function exportPDF() {
  var d = getD(), s = d.stats, n = getN();
  var vals = Object.values(ANALYSIS);
  var now = new Date().toLocaleString('tr-TR');
  var avgRisk=(vals.reduce(function(a,b){return a+b.risk_score;},0)/vals.length).toFixed(1);
  var avgH=(vals.reduce(function(a,b){return a+b.health_index;},0)/vals.length).toFixed(0);

  var rows = SORTED.map(function(pair){
    var nm=pair[0], dd=pair[1];
    return '<tr><td>'+esc(nm)+'</td><td>'+dd.iso_class+'</td><td>'+dd.risk_score.toFixed(1)+'</td><td>'+dd.health_index.toFixed(0)+'</td><td>'+dd.stats.Severity.rms+'</td><td>'+dd.total_anomalies+'</td><td>'+rul(dd)+'</td></tr>';
  }).join('');

  var axRows = ['X','Y','Z','Severity'].map(function(ax){
    return '<tr><td><b>'+ax+'</b></td><td>'+s[ax].mean+'</td><td>'+s[ax].std+'</td><td><b>'+s[ax].rms+'</b></td><td>'+s[ax].max+'</td><td>'+s[ax].kurtosis+'</td><td>'+s[ax].anomaly_count+'</td></tr>';
  }).join('');

  var cls = d.iso_class==='Critical'?'critical':d.iso_class==='Warning'?'warning':'normal';
  var msg = d.iso_class==='Critical'?'ACİL BAKIM GEREKLİ — Motor, rulman ve hidrolik sistem acil incelenmeli.':
            d.iso_class==='Warning' ?'PLANLI BAKIM ÖNERİLİR — 30–60 gün içinde kapsamlı bakım yapılmalı.':
            'NORMAL İZLEME YETERLİ — Rutin bakım programı sürdürülmeli.';

  var html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>ForkliftIQ Raporu</title><style>' +
    'body{font-family:Arial,sans-serif;margin:32px;color:#1a1a2e;font-size:12px;}' +
    'h1{font-size:20px;color:#1e3a5f;border-bottom:3px solid #3b82f6;padding-bottom:8px;margin-bottom:20px;}' +
    'h2{font-size:14px;color:#1e3a5f;margin:20px 0 8px;border-left:4px solid #3b82f6;padding-left:8px;}' +
    'table{width:100%;border-collapse:collapse;margin-bottom:16px;}' +
    'th{background:#1e3a5f;color:#fff;padding:7px 8px;text-align:left;font-size:11px;}' +
    'td{padding:6px 8px;border-bottom:1px solid #e8edf0;}' +
    'tr:nth-child(even) td{background:#f8fafc;}' +
    '.kpi-row{display:flex;gap:14px;margin:16px 0;flex-wrap:wrap;}' +
    '.kpi-box{flex:1;min-width:100px;background:#f0f4ff;border-radius:8px;padding:12px;text-align:center;border:1px solid #dde8ff;}' +
    '.kpi-box .val{font-size:20px;font-weight:700;}.kpi-box .lbl{font-size:10px;color:#666;margin-top:3px;}' +
    '.critical{background:#fff0f0;border-left:4px solid #f43f5e;padding:10px;margin:6px 0;border-radius:4px;}' +
    '.warning{background:#fffbf0;border-left:4px solid #f59e0b;padding:10px;margin:6px 0;border-radius:4px;}' +
    '.normal{background:#f0fff8;border-left:4px solid #10b981;padding:10px;margin:6px 0;border-radius:4px;}' +
    'footer{margin-top:40px;font-size:10px;color:#999;border-top:1px solid #ddd;padding-top:8px;}' +
    '</style></head><body>' +
    '<h1>⚙ ForkliftIQ — Predictive Maintenance Raporu</h1>' +
    '<p><b>Cihaz:</b> '+esc(n)+' &nbsp;|&nbsp; <b>Tarih:</b> '+now+' &nbsp;|&nbsp; <b>ISO Sınıfı:</b> '+d.iso_class+'</p>' +
    '<div class="kpi-row">' +
      '<div class="kpi-box"><div class="val">'+d.health_index.toFixed(0)+'/100</div><div class="lbl">Health Index</div></div>' +
      '<div class="kpi-box"><div class="val">'+d.risk_score.toFixed(1)+'</div><div class="lbl">Risk Skoru</div></div>' +
      '<div class="kpi-box"><div class="val">'+s.Severity.rms+' mg</div><div class="lbl">Severity RMS</div></div>' +
      '<div class="kpi-box"><div class="val">'+d.total_anomalies+'</div><div class="lbl">Anomali</div></div>' +
      '<div class="kpi-box"><div class="val">'+rul(d)+'</div><div class="lbl">RUL Tahmini</div></div>' +
    '</div>' +
    '<h2>Titreşim İstatistikleri — '+esc(n)+'</h2>' +
    '<table><tr><th>Eksen</th><th>Ortalama</th><th>Std</th><th>RMS</th><th>Maksimum</th><th>Kurtosis</th><th>Anomali</th></tr>'+axRows+'</table>' +
    '<h2>Filo Karşılaştırması</h2>' +
    '<table><tr><th>Cihaz</th><th>ISO Sınıfı</th><th>Risk</th><th>Health</th><th>RMS</th><th>Anomali</th><th>RUL</th></tr>'+rows+'</table>' +
    '<h2>Genel Bakış — '+vals.length+' Cihaz</h2>' +
    '<p>Ortalama Risk: <b>'+avgRisk+'</b> &nbsp;|&nbsp; Ortalama Sağlık: <b>'+avgH+'</b> &nbsp;|&nbsp; ' +
      'Kritik: <b>'+vals.filter(function(x){return x.iso_class==='Critical';}).length+'</b> &nbsp;|&nbsp; ' +
      'Uyarı: <b>'+vals.filter(function(x){return x.iso_class==='Warning';}).length+'</b></p>' +
    '<h2>Bakım Değerlendirmesi</h2>' +
    '<div class="'+cls+'"><b>'+msg+'</b></div>' +
    '<footer>ForkliftIQ Predictive Maintenance Platform · ISO 20816 · '+now+'</footer>' +
    '</body></html>';

  var w = window.open('', '_blank');
  if (w) { w.document.write(html); w.document.close(); setTimeout(function(){w.print();}, 600); }
  else alert('Popup engellendi. Tarayıcı popup iznini açın.');
}

// ══════════════════════════════════════════════════════════════
// MARKA KNOWLEDGE BASE
// ══════════════════════════════════════════════════════════════
var BRAND_KB = {
  jungheinrich: {
    name: 'Jungheinrich',
    abbr: 'JUNG',
    logoClass: 'jung',
    color: '#0055cc',
    keywords: ['jung','jungheinrich','pkt','fn71','fn72'],
    description: 'Alman üretimi elektrikli ve LPG\'li forkliftler. EFG, ERE, EKS, ETV serileri yaygın. AC tahrik motoru ve özel elektronik kontrol sistemi.',
    models: 'EFG / ERE / EKS / ETV / EJE / AM serileri',
    faults: [
      {icon:'⚡',title:'AC Tahrik Motoru Arızası',zone:'Motor Bölgesi',sev:'critical',sevLabel:'Kritik',
       desc:'Jungheinrich AC motorlarında en yaygın arıza stator sargı bozulması ve rotor dengesizliğidir. Yüksek Z-ekseni titreşimi ile kendini gösterir. EFG/ERE serilerinde özellikle soğutma kanalları tıkanabilir.',
       trigger:'Z-RMS > 800 mg veya Z Kurtosis > 10',
       axes:['Z'],when:'z_rms>800 || z_kurtosis>10'},
      {icon:'🔄',title:'Hidrolik Pompa Titremesi',zone:'Hidrolik Sistem',sev:'critical',sevLabel:'Kritik',
       desc:'JH hidrolik birimlerinde pompa plakası yıpranması ve basınç regülatörü arızası kritik öneme sahiptir. Y-ekseni titreşimi spesifik frekanslarda spike üretir. Model: EFG 320-430.',
       trigger:'Y-RMS > 900 mg veya Severity > 1500 mg',
       axes:['Y','Severity'],when:'y_rms>900 || sev_rms>1500'},
      {icon:'🎯',title:'Tekerlek Rulmanı Aşınması',zone:'Aks & Tekerlek',sev:'high',sevLabel:'Yüksek',
       desc:'Jungheinrich ön aks rulmanları yüksek yükte erken aşınır. X-Y çift eksen titreşimi ile tespit edilir. Bilhassa EKS yüksek raf forkliftlerinde kritik güvenlik sorunu oluşturur.',
       trigger:'X-RMS > 500 mg VE Y-RMS > 600 mg eşzamanlı',
       axes:['X','Y'],when:'x_rms>500 && y_rms>600'},
      {icon:'🔌',title:'Fren Elektroniği / Chopper',zone:'Kontrol Elektroniği',sev:'high',sevLabel:'Yüksek',
       desc:'JH elektronik sisteminde chopper kartı arızaları ani yük değişimlerinde spike titreşim üretir. Kurtosis değeri aniden yükselir. Modüler kontrol kartı değişimi gerektirir.',
       trigger:'Kurtosis > 50 herhangi bir eksende',
       axes:['X','Y','Z'],when:'x_kurtosis>50 || y_kurtosis>50 || z_kurtosis>50'},
      {icon:'🛞',title:'Direksiyon Sistemi Gevşemesi',zone:'Direksiyon & Arka Aks',sev:'medium',sevLabel:'Orta',
       desc:'Jungheinrich elektrikli direksiyon sisteminde (EFG serisi) mafsal ve üniversal mil bağlantıları serbest oynama yapabilir. X-ekseni lateral titreşim artışına neden olur.',
       trigger:'X-RMS 400–700 mg aralığında, yüksek skewness',
       axes:['X'],when:'x_rms>400 && x_rms<700 && x_skewness>4'},
      {icon:'🔋',title:'Batarya Konektör Arızası',zone:'Güç & Batarya',sev:'medium',sevLabel:'Orta',
       desc:'JH litiyum ve traksiyon batarya bağlantı noktaları vibrasyon altında gevşeyebilir. Düzensiz güç iletimi tüm eksenlerde intermittent spike üretir. Bakım periyodunda kontrol edilmeli.',
       trigger:'Düzensiz spike patlamaları, IQR dışı veri > %3',
       axes:['X','Y','Z'],when:'iqr_out_rate>3'},
      {icon:'🏗️',title:'Mast Hizalama Bozukluğu',zone:'Kaldırma Direği',sev:'low',sevLabel:'Düşük',
       desc:'Özellikle ETV/EKS çoklu kaldırma sistemlerinde iç ve dış direk ray sürtünmesi ve hizalama kayması oluşabilir. Kaldırma sırasında Z-ekseninde periyodik titreşim piki gözlemlenir.',
       trigger:'Z-ekseni kaldırma sırasında periodik spike',
       axes:['Z'],when:'z_anomaly>20'},
    ],
    maintenance: [
      {interval:'250 saat',item:'AC motor soğutma kanalları temizlenmeli, yalıtım direnci ölçülmeli'},
      {interval:'500 saat',item:'Hidrolik pompa basınç ve debisi test edilmeli, filtreler değiştirilmeli'},
      {interval:'500 saat',item:'Ön ve arka aks rulmanları titreşim ölçümü ile kontrol edilmeli'},
      {interval:'1000 saat',item:'Chopper ve kontrol kartları thermal kamera ile taranmalı'},
      {interval:'1000 saat',item:'Batarya konektörleri ve kablo bağlantıları torklama kontrolü'},
      {interval:'2000 saat',item:'Mast ray yağlaması, hizalama ve yük kolu zinciri gerilimi'},
      {interval:'Yıllık',item:'Tam direk revizyonu, rulman seti değişimi, fren kaliperleri'},
    ]
  },
  still: {
    name: 'Still',
    abbr: 'STILL',
    logoClass: 'still',
    color: '#cc0000',
    keywords: ['still','rx','rx60','rx70','rx20','fm-x','rkm','516','lml','cinko','çinko'],
    description: 'Hamburg merkezli premium forklift markası. RX 60/70 elektrikli seriler ve FM-X depo sistemleri. Çok jantlı AC tahrik ve entegre hydraulics.',
    models: 'RX 60 / RX 70 / RX 20 / FM-X / LTX / RKM serileri',
    faults: [
      {icon:'🔥',title:'Traksiyon Motoru Isı Arızası',zone:'Traksiyon Motoru',sev:'critical',sevLabel:'Kritik',
       desc:'Still RX serisi motorlarda aşırı ısınma erken rulman bozulmasına yol açar. Motor bloğuna monte sensörün titreşim imzası Z-ekseni yüksek RMS + düşük kurtosis kombinasyonu gösterir — titreşim sürekli yüksek, impulsif değil.',
       trigger:'Z-RMS > 1000 mg, Z Kurtosis < 5 (sürekli yüksek)',
       axes:['Z'],when:'z_rms>1000 && z_kurtosis<5'},
      {icon:'⚙️',title:'Diferansiyel Dişli Aşınması',zone:'Tahrik Aksı',sev:'critical',sevLabel:'Kritik',
       desc:'Still RX 60/70 modellerinde diferansiyel planet dişlileri uzun vadede aşınır. X-Y kombinasyonu yüksek kurtosis üretir. Ses kuplajı ve dişli vuruşu titreşim imzası oluşturur.',
       trigger:'X veya Y Kurtosis > 100, eşzamanlı yüksek RMS',
       axes:['X','Y'],when:'(x_kurtosis>100 || y_kurtosis>100) && (x_rms>400 || y_rms>500)'},
      {icon:'🌊',title:'Hidrolik Silindir Sızdırmazlığı',zone:'Kaldırma Silindiri',sev:'high',sevLabel:'Yüksek',
       desc:'Still FM-X ve LTX serilerinde kaldırma silindiri O-ring ve sızdırmazlık elemanları basınç altında yorulur. Y-ekseninde yavaş periyotlu titreşim + ani basınç düşüşü spike\'ı oluşur.',
       trigger:'Y-RMS 700–1200 mg, yüksek skewness Y > 5',
       axes:['Y'],when:'y_rms>700 && y_skewness>5'},
      {icon:'🎛️',title:'CAN Bus / Kontrol Ünitesi Hatası',zone:'Elektronik Kontrol',sev:'high',sevLabel:'Yüksek',
       desc:'Still\'in entegre CAN Bus sistemi titreşim altında intermittent bağlantı hatası üretebilir. Tüm eksenlerde düzensiz spike pattern, yüksek IQR dışı nokta sayısı ile tespit edilir.',
       trigger:'Tüm eksenlerde yüksek IQR dışı nokta, ani multiaxis spike',
       axes:['X','Y','Z'],when:'iqr_out_rate>4 && total_anom>100'},
      {icon:'🛠️',title:'Forwarder Zinciri Gerginliği',zone:'Kaldırma Zinciri',sev:'medium',sevLabel:'Orta',
       desc:'Still yüksek kaldırmalı sistemlerde (5m+) zincir gerginliği zamanla bozulur. Kaldırma hareketi sırasında Z-ekseninde periyodik titreşim burst\'leri gözlemlenir.',
       trigger:'Z-anomali sayısı yüksek, periyodik spike patlamaları',
       axes:['Z'],when:'z_anomaly>30'},
      {icon:'💧',title:'Soğutma Sistemi Tıkanması',zone:'Motor Soğutma',sev:'medium',sevLabel:'Orta',
       desc:'Still RX serilerinde kapalı devre sıvı soğutma sistemi tıkanabilir. Termal yük arttıkça titreşim seviyesi yavaşça tırmanır — trend eğimi pozitif. Severity RMS sürekli artış gösterir.',
       trigger:'Severity trend artışı, RMS 600-900 mg stabil yüksek',
       axes:['Severity'],when:'sev_rms>600 && sev_rms<1500 && sev_kurtosis<10'},
      {icon:'🔩',title:'Şasi Bağlantı Torku Kayıpları',zone:'Şasi & Kaporta',sev:'low',sevLabel:'Düşük',
       desc:'Still\'de ergonomik kabin tasarımı nedeniyle şasi-kabin bağlantı noktaları bakım periyotları arasında gevşeyebilir. Tüm eksenlerde düşük frekanslı genel titreşim artışı.',
       trigger:'Genel titreşim seviyesi ılımlı yüksek, tek eksen dominant değil',
       axes:['X','Y','Z'],when:'sev_rms>400 && x_rms<500 && y_rms<600 && z_rms<500'},
    ],
    maintenance: [
      {interval:'250 saat',item:'Traksiyon motor sıcaklığı ve yalıtım direnci ölçümü'},
      {interval:'500 saat',item:'Diferansiyel yağı analizi ve dişli kontrolü, torklama'},
      {interval:'500 saat',item:'Hidrolik silindir O-ring ve contalar görsel + sızdırmazlık testi'},
      {interval:'1000 saat',item:'CAN Bus diagnostik tarama, kontrol ünitesi firmware güncelleme'},
      {interval:'1000 saat',item:'Kaldırma zinciri gerginlik ölçümü ve yağlama'},
      {interval:'2000 saat',item:'Soğutma sistemi flush ve antifriz değişimi'},
      {interval:'Yıllık',item:'Tam şasi vida torklama, kabin bağlantı kontrolü, güvenlik denetimi'},
    ]
  }
};

// ══════════════════════════════════════════════════════════════
// BRAND DETECTION
// ══════════════════════════════════════════════════════════════
function detectBrand(deviceName) {
  var lower = deviceName.toLowerCase();
  var jungKW = BRAND_KB.jungheinrich.keywords;
  var stillKW = BRAND_KB.still.keywords;
  for (var i=0; i<jungKW.length; i++) { if (lower.indexOf(jungKW[i]) !== -1) return 'jungheinrich'; }
  for (var i=0; i<stillKW.length; i++) { if (lower.indexOf(stillKW[i]) !== -1) return 'still'; }
  return null;
}

function evalFaultTrigger(cond, d) {
  var s = d.stats;
  var x_rms = s.X.rms, y_rms = s.Y.rms, z_rms = s.Z.rms, sev_rms = s.Severity.rms;
  var x_kurtosis = s.X.kurtosis, y_kurtosis = s.Y.kurtosis, z_kurtosis = s.Z.kurtosis;
  var x_skewness = s.X.skewness, y_skewness = s.Y.skewness;
  var z_anomaly = s.Z.anomaly_count, total_anom = d.total_anomalies;
  var iqr_out_rate = (s.Severity.iqr_out / d.row_count) * 100;
  try { return eval(cond); } catch(e) { return false; }
}

// ══════════════════════════════════════════════════════════════
// TAB 6 — MARKA ANALİZİ
// Mimari: global state + tek delegated listener, no closure bugs
// ══════════════════════════════════════════════════════════════
var G_ZONE_MAP = {};    // arıza haritası zone verisi
var G_BRAND_D  = null;  // aktif cihaz datası
var G_BRAND_N  = '';    // aktif cihaz adı
var G_BRAND_BK = '';    // aktif marka anahtarı
var G_FLEET    = {};    // filo marka grupları
var BRAND_LISTENER_ADDED = false; // listener'ı sadece bir kez ekle

function renderBrand() {
  var pane = document.getElementById('pane-brand');
  var d = getD(), n = getN();
  var bk = detectBrand(n) || 'jungheinrich';

  // Globals güncelle
  G_BRAND_D  = d;
  G_BRAND_N  = n;
  G_BRAND_BK = bk;
  G_FLEET    = {jungheinrich:[], still:[], other:[]};
  SORTED.forEach(function(pair) {
    var b = detectBrand(pair[0]);
    if (b === 'jungheinrich') G_FLEET.jungheinrich.push(pair);
    else if (b === 'still')   G_FLEET.still.push(pair);
    else                       G_FLEET.other.push(pair);
  });

  // Skeleton HTML — tek seferlik, listener sonradan eklenir
  pane.innerHTML =
    '<div id="brand-tab-bar" style="display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;align-items:center">' +
      brandTabBtn('jungheinrich') + brandTabBtn('still') +
      '<div style="flex:1"></div>' +
      '<div id="brand-sel-label" style="font-size:10px;color:var(--text3)">' +
        'Seçili: <b style="color:var(--text)">' + esc(sh(n,22)) + '</b>' +
      '</div>' +
    '</div>' +
    '<div id="brand-content"></div>';

  // Delegated listener — sadece BİR KEZ eklenir
  if (!BRAND_LISTENER_ADDED) {
    BRAND_LISTENER_ADDED = true;
    document.addEventListener('click', function(e) {
      // Tab button
      var btn = e.target.closest('.btab');
      if (btn && document.getElementById('pane-brand') && document.getElementById('pane-brand').contains(btn)) {
        var newBk = btn.getAttribute('data-bk');
        G_BRAND_BK = newBk;
        document.querySelectorAll('.btab').forEach(function(b) {
          var kb2 = BRAND_KB[b.getAttribute('data-bk')];
          var isA = b.getAttribute('data-bk') === newBk;
          b.style.background  = isA ? kb2.color + '22' : 'var(--bg3)';
          b.style.borderColor = isA ? kb2.color : 'var(--border)';
          b.style.color       = isA ? kb2.color : 'var(--text2)';
        });
        drawBrandContent(newBk);
        return;
      }
      // Zone click (SVG g.fzone veya child elementi)
      var g = e.target.closest('.fzone');
      if (g && document.getElementById('fault-detail-panel') && document.getElementById('fault-detail-panel').contains(g) === false) {
        var zid = g.getAttribute('data-zid');
        if (zid && G_ZONE_MAP[zid]) {
          fillDetailPanel(G_ZONE_MAP[zid]);
        }
      }
    });
  }

  // İlk çizim
  drawBrandContent(bk);
}

function brandTabBtn(bk) {
  var kb = BRAND_KB[bk];
  var isA = (bk === G_BRAND_BK);
  return '<button class="btab" data-bk="' + bk + '" style="' +
    'background:' + (isA ? kb.color+'22' : 'var(--bg3)') + ';' +
    'border:1px solid ' + (isA ? kb.color : 'var(--border)') + ';' +
    'color:' + (isA ? kb.color : 'var(--text2)') + ';' +
    'padding:7px 18px;border-radius:8px;cursor:pointer;font-size:11px;font-weight:700;' +
    'transition:all .15s;letter-spacing:.02em;">' +
    kb.name + ' <span style="font-size:9px;font-weight:400;opacity:.6">(' + (G_FLEET[bk]||[]).length + ')</span>' +
  '</button>';
}

// ── drawBrandContent: tüm içeriği yeniden çiz ────────────────────────────────
function drawBrandContent(bk) {
  var kb      = BRAND_KB[bk];
  var d       = G_BRAND_D;
  var n       = G_BRAND_N;
  var fleet   = G_FLEET[bk] || [];
  var isSel   = (detectBrand(n) === bk);

  // Zone haritasını hesapla ve global'e kaydet
  G_ZONE_MAP = computeZoneMap(bk, d, isSel);

  var html = '';

  // ── 1. MARKA BAŞLIĞI ─────────────────────────────────────────────────────
  html += '<div class="brand-header">' +
    '<div class="brand-logo ' + kb.logoClass + '">' + kb.abbr.charAt(0) + '</div>' +
    '<div style="flex:1">' +
      '<div class="brand-name">' + kb.name + '</div>' +
      '<div class="brand-sub">' + kb.models + '</div>' +
      '<div style="font-size:10px;color:var(--text3);margin-top:4px;line-height:1.5">' + kb.description + '</div>' +
    '</div>' +
    '<div style="text-align:right;flex-shrink:0">' +
      '<div style="font-size:26px;font-weight:800;color:' + kb.color + '">' + fleet.length + '</div>' +
      '<div style="font-size:9px;color:var(--text2)">filodaki cihaz</div>' +
    '</div>' +
  '</div>';

  // ── 2. SEÇİLİ CİHAZ UYARI BLOĞU ─────────────────────────────────────────
  if (isSel && d) {
    var triggered = kb.faults.filter(function(f){ return evalFaultTrigger(f.when, d); });
    if (triggered.length > 0) {
      html += '<div style="background:rgba(244,63,94,0.07);border:1px solid rgba(244,63,94,0.3);' +
        'border-radius:12px;padding:16px;margin-bottom:14px;">' +
        '<div style="font-size:12px;font-weight:800;color:var(--red);margin-bottom:12px;display:flex;align-items:center;gap:8px;">' +
          '<span style="font-size:16px">⚠</span>' +
          '<span>' + esc(sh(n,26)) + ' — ' + triggered.length + ' Aktif Arıza Tespiti</span>' +
        '</div>';
      triggered.forEach(function(f) {
        var fc = f.sev==='critical'?'#f43f5e':f.sev==='high'?'#f59e0b':'#3b82f6';
        html += '<div style="display:flex;gap:12px;padding:10px;background:rgba(255,255,255,0.03);' +
          'border:1px solid var(--border);border-left:3px solid ' + fc + ';' +
          'border-radius:8px;margin-bottom:8px;">' +
          '<div style="font-size:22px;flex-shrink:0;margin-top:1px">' + f.icon + '</div>' +
          '<div style="flex:1">' +
            '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:4px">' + f.title + '</div>' +
            '<div style="font-size:11px;color:var(--text2);line-height:1.6;margin-bottom:6px">' + f.desc + '</div>' +
            '<div style="font-size:10px;color:var(--amber);margin-bottom:6px">📌 ' + f.trigger + '</div>' +
            '<div style="display:flex;gap:5px;flex-wrap:wrap">' +
              f.axes.map(function(ax){ return '<span style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:5px;background:rgba(59,130,246,0.15);color:#3b82f6">' + ax + '</span>'; }).join('') +
              '<span style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:5px;background:' + fc + '20;color:' + fc + '">' + f.sevLabel + '</span>' +
            '</div>' +
          '</div>' +
        '</div>';
      });
      html += '</div>';
    } else {
      html += '<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.25);' +
        'border-radius:10px;padding:12px;margin-bottom:14px;display:flex;align-items:center;gap:10px;">' +
        '<span style="font-size:20px">✅</span>' +
        '<div><div style="font-size:11px;font-weight:700;color:var(--green)">' + esc(sh(n,26)) + ' — Kritik Eşik Aşılmadı</div>' +
        '<div style="font-size:10px;color:var(--text2);margin-top:2px">Bu markaya özgü arıza eşikleri normal sınırlar içinde. Rutin izleme yeterli.</div></div>' +
      '</div>';
    }
  } else if (!isSel) {
    html += '<div style="background:var(--bg3);border:1px solid var(--border);border-radius:10px;' +
      'padding:12px;margin-bottom:14px;font-size:11px;color:var(--text2);">' +
      '💡 Seçili cihaz ' + kb.name + ' markasına ait değil. Genel marka bilgileri gösteriliyor.' +
    '</div>';
  }

  // ── 3. FİLO TABLOSU ──────────────────────────────────────────────────────
  if (fleet.length > 0) {
    html += '<div class="card" style="margin-bottom:14px">' +
      '<div class="ct"><div class="ctd" style="background:' + kb.color + '"></div>' +
        kb.name + ' — Filodaki ' + fleet.length + ' Cihaz' +
      '</div>' +
      '<div style="overflow-x:auto"><table style="width:100%;font-size:11px;border-collapse:collapse">' +
        '<thead><tr style="border-bottom:1px solid var(--border)">' +
          '<th style="text-align:left;padding:6px 8px;font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:.07em">Cihaz</th>' +
          '<th style="text-align:center;padding:6px 4px;font-size:9px;color:var(--text3)">ISO</th>' +
          '<th style="text-align:right;padding:6px 4px;font-size:9px;color:var(--text3)">Risk</th>' +
          '<th style="text-align:right;padding:6px 4px;font-size:9px;color:var(--text3)">Health</th>' +
          '<th style="text-align:right;padding:6px 4px;font-size:9px;color:var(--text3)">Z-RMS</th>' +
          '<th style="text-align:right;padding:6px 4px;font-size:9px;color:var(--text3)">Y-RMS</th>' +
          '<th style="text-align:right;padding:6px 4px;font-size:9px;color:var(--text3)">Anomali</th>' +
          '<th style="text-align:center;padding:6px 4px;font-size:9px;color:var(--text3)">RUL</th>' +
          '<th style="text-align:center;padding:6px 4px;font-size:9px;color:var(--text3)">Durum</th>' +
        '</tr></thead><tbody>';
    fleet.forEach(function(pair) {
      var nm=pair[0], dd=pair[1];
      var fc = kb.faults.filter(function(f){ return evalFaultTrigger(f.when, dd); }).length;
      html += '<tr style="border-bottom:1px solid var(--border)">' +
        '<td style="padding:7px 8px;font-weight:600;color:var(--text);max-width:140px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="'+esc(nm)+'">'+esc(sh(nm,17))+'</td>' +
        '<td style="text-align:center;padding:7px 4px"><span class="badge '+bcl(dd.iso_class)+'">'+dd.iso_class+'</span></td>' +
        '<td style="text-align:right;padding:7px 4px;font-weight:600;color:'+rC(dd.risk_score)+'">'+dd.risk_score.toFixed(1)+'</td>' +
        '<td style="text-align:right;padding:7px 4px;font-weight:600;color:'+hiC(dd.health_index)+'">'+dd.health_index.toFixed(0)+'</td>' +
        '<td style="text-align:right;padding:7px 4px;color:var(--text2)">'+dd.stats.Z.rms+'</td>' +
        '<td style="text-align:right;padding:7px 4px;color:var(--text2)">'+dd.stats.Y.rms+'</td>' +
        '<td style="text-align:right;padding:7px 4px;color:var(--text2)">'+dd.total_anomalies+'</td>' +
        '<td style="text-align:center;padding:7px 4px;color:var(--cyan);font-size:10px">'+rul(dd)+'</td>' +
        '<td style="text-align:center;padding:7px 4px">'+(fc>0
          ? '<span style="color:var(--red);font-weight:700;font-size:10px">⚠ '+fc+' arıza</span>'
          : '<span style="color:var(--green);font-size:10px">✓ Normal</span>'
        )+'</td>' +
      '</tr>';
    });
    html += '</tbody></table></div></div>';
  }

  // ── 4. İNTERAKTİF ARIZA HARİTASI + DETAY PANELİ ─────────────────────────
  html += buildInteractiveDiagram(bk, d, isSel, n);

  // ── 5. TÜM BİLİNEN ARIZA KARTLARI ────────────────────────────────────────
  html += '<div style="font-size:13px;font-weight:800;color:var(--text);margin:18px 0 10px;' +
    'padding-bottom:6px;border-bottom:1px solid var(--border);">' +
    kb.name + ' — Bilinen Arıza Noktaları (' + kb.faults.length + ')' +
  '</div>';
  html += '<div class="fault-grid">';
  kb.faults.forEach(function(f) {
    var trig = isSel && d && evalFaultTrigger(f.when, d);
    var fc = f.sev==='critical'?'var(--red)':f.sev==='high'?'var(--amber)':'var(--blue)';
    html += '<div class="fault-card sev-' + f.sev + '" style="' +
      (trig ? 'border-color:' + (f.sev==='critical'?'var(--red)':'var(--amber)') + ';' : '') + '">' +
      (trig ? '<div style="position:absolute;top:8px;right:8px;font-size:8px;font-weight:800;' +
        'background:var(--red);color:#fff;padding:2px 7px;border-radius:4px;letter-spacing:.04em">AKTIF</div>' : '') +
      '<div class="fault-icon">' + f.icon + '</div>' +
      '<div class="fault-title">' + f.title + '</div>' +
      '<div class="fault-zone" style="color:' + kb.color + '">' + f.zone + '</div>' +
      '<div class="fault-desc">' + f.desc + '</div>' +
      '<div class="fault-trigger">' + f.trigger + '</div>' +
      '<div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:8px">' +
        f.axes.map(function(ax){ return '<span style="font-size:8px;font-weight:700;padding:2px 6px;border-radius:4px;background:rgba(59,130,246,0.15);color:var(--blue)">' + ax + '</span>'; }).join('') +
        '<span class="fault-sev s' + f.sev.charAt(0) + '">' + f.sevLabel + '</span>' +
      '</div>' +
    '</div>';
  });
  html += '</div>';

  // ── 6. BAKIM TAKVİMİ ─────────────────────────────────────────────────────
  html += '<div style="font-size:13px;font-weight:800;color:var(--text);margin:18px 0 10px;' +
    'padding-bottom:6px;border-bottom:1px solid var(--border);">' +
    kb.name + ' — Periyodik Bakım Takvimi' +
  '</div>' +
  '<div class="card"><table style="width:100%;font-size:11px;border-collapse:collapse">' +
  '<thead><tr style="border-bottom:1px solid var(--border)">' +
    '<th style="text-align:left;padding:6px 8px;font-size:9px;color:var(--text3);text-transform:uppercase">Periyot</th>' +
    '<th style="text-align:left;padding:6px 8px;font-size:9px;color:var(--text3);text-transform:uppercase">Bakım İşlemi</th>' +
  '</tr></thead><tbody>' +
  kb.maintenance.map(function(m,i) {
    return '<tr style="border-bottom:1px solid var(--border);background:' + (i%2===0?'transparent':'rgba(255,255,255,0.01)') + '">' +
      '<td style="padding:8px;color:var(--cyan);font-weight:700;white-space:nowrap;font-size:11px">' + m.interval + '</td>' +
      '<td style="padding:8px;color:var(--text2)">' + m.item + '</td>' +
    '</tr>';
  }).join('') +
  '</tbody></table></div>';

  document.getElementById('brand-content').innerHTML = html;
}

// ── computeZoneMap: titreşim verisinden zone yoğunluklarını hesapla ──────────
function computeZoneMap(bk, d, isSel) {
  var kb = BRAND_KB[bk];
  var s  = isSel && d ? d.stats : null;

  // Eşikler ISO 20816 ve endüstriyel pratik bazlı
  // Normal: <500 mg, Uyarı: 500-1500, Kritik: >1500
  function intensity(val, warnThr, critThr) {
    if (!s) return 0.12;
    if (val >= critThr) return 0.75 + Math.min(0.25, (val-critThr)/critThr*0.5);
    if (val >= warnThr) return 0.30 + (val-warnThr)/(critThr-warnThr)*0.45;
    return Math.max(0.05, val/warnThr*0.30);
  }

  var motorT   = intensity(s?s.Z.rms:0,         600, 1400);
  var hydT     = intensity(s?s.Y.rms:0,          700, 1500);
  var wheelT   = intensity(s?Math.max(s.X.rms,s.Y.rms):0, 500, 1200);
  var mastT    = intensity(s?s.Z.rms:0,          800, 1800);
  var chassisT = intensity(s?s.Severity.rms:0,  1000, 2500);
  var forkT    = intensity(s?s.Z.rms:0,          900, 2000);
  var elektT   = s ? Math.min(1, Math.max(s.X.kurtosis||0, s.Y.kurtosis||0, s.Z.kurtosis||0)/400) : 0.12;
  var aksT     = intensity(s?Math.max(s.X.rms,s.Y.rms):0, 550, 1300);

  function faultsFor(axArr, zoneKws) {
    if (!isSel || !d) return [];
    return kb.faults.filter(function(f) {
      if (!evalFaultTrigger(f.when, d)) return false;
      var aOk = !axArr || axArr.some(function(a){ return f.axes.indexOf(a)!==-1; });
      var zOk = !zoneKws || zoneKws.some(function(w){ return f.zone.indexOf(w)!==-1 || f.title.indexOf(w)!==-1; });
      return aOk && zOk;
    });
  }

  function zcolor(t) {
    if (t>=0.75) return {fill:'#f43f5e',stroke:'#e11d48',label:'KRİTİK',lvl:3};
    if (t>=0.30) return {fill:'#f59e0b',stroke:'#d97706',label:'RİSKLİ',lvl:2};
    return {fill:'#10b981',stroke:'#059669',label:'Normal',lvl:1};
  }

  var zones = {
    'fz-motor':   {label:'Motor / Tahrik',        t:motorT,   rms:s?s.Z.rms:0,   axis:'Z-ekseni',   faults:faultsFor(['Z'],['Motor','Traksiyon','Tahrik','Isı'])},
    'fz-hidro':   {label:'Hidrolik Sistem',        t:hydT,     rms:s?s.Y.rms:0,   axis:'Y-ekseni',   faults:faultsFor(['Y'],['Hidrolik','Silindir','Pompa'])},
    'fz-wheel':   {label:'Tekerlek / Ön Aks',      t:wheelT,   rms:s?Math.max(s.X.rms,s.Y.rms):0, axis:'X/Y-ekseni', faults:faultsFor(['X','Y'],['Aks','Rulman','Tekerlek'])},
    'fz-mast':    {label:'Mast / Kaldırma Direği', t:mastT,    rms:s?s.Z.rms:0,   axis:'Z-ekseni',   faults:faultsFor(['Z'],['Mast','Kaldırma','Zincir','Direk','Forwarder'])},
    'fz-chassis': {label:'Şasi / Gövde',           t:chassisT, rms:s?s.Severity.rms:0, axis:'Severity', faults:faultsFor(null,['asi','Kaporta','Bağlantı','Torku'])},
    'fz-fork':    {label:'Fork Kolları',            t:forkT,    rms:s?s.Z.rms:0,   axis:'Z-ekseni',   faults:[]},
    'fz-elek':    {label:'Elektronik / CAN',        t:elektT,   rms:s?Math.round(Math.max(s.X.kurtosis||0,s.Y.kurtosis||0,s.Z.kurtosis||0)):0, axis:'Kurtosis', faults:faultsFor(['X','Y','Z'],['Kontrol','CAN','Chopper','Elektronik','Fren','Batarya'])},
    'fz-aks':     {label:'Arka Aks / Direksiyon',   t:aksT,     rms:s?Math.max(s.X.rms,s.Y.rms):0, axis:'X/Y-ekseni', faults:faultsFor(['X','Y'],['Direksiyon','Diferansiyel','Aks'])},
  };

  Object.keys(zones).forEach(function(k) {
    var z = zones[k], c = zcolor(z.t);
    z.color  = c.fill; z.stroke = c.stroke; z.statusLabel = c.label; z.lvl = c.lvl;
  });
  return zones;
}

// ── buildInteractiveDiagram: SVG + detail panel yanyana ─────────────────────
function buildInteractiveDiagram(bk, d, isSel, n) {
  var kb = BRAND_KB[bk];
  var zm = G_ZONE_MAP;
  var s  = isSel && d ? d.stats : null;

  function Z(id) { return zm[id] || {color:'#10b981',stroke:'#059669',t:0.1,rms:0,faults:[],label:'—',axis:'—',statusLabel:'Normal',lvl:1}; }
  function op(t)  { return (0.15 + Math.min(0.80, t*0.75)).toFixed(2); }
  function sw(t)  { return t>=0.75?'2.5':t>=0.30?'1.5':'1'; }
  function val(v) { return s ? String(v) : '—'; }

  // Glow filter sadece kritik bölgeler için
  var defs = '<defs>';
  Object.keys(zm).forEach(function(k) {
    if (zm[k].t>=0.75) {
      defs += '<filter id="glow'+k.replace('fz-','')+'" x="-50%" y="-50%" width="200%" height="200%">' +
        '<feGaussianBlur stdDeviation="4" result="blur"/>' +
        '<feFlood flood-color="'+zm[k].color+'" flood-opacity="0.45"/>' +
        '<feComposite in2="blur" operator="in" result="glow"/>' +
        '<feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>' +
      '</filter>';
    }
  });
  defs += '</defs>';

  function gf(id) { var k=id.replace('fz-',''); return zm[id]&&zm[id].t>=0.75?' filter="url(#glow'+k+')"':''; }
  function anim(id) {
    return zm[id]&&zm[id].t>=0.75
      ? '<animate attributeName="opacity" values="'+op(zm[id].t)+';0.95;'+op(zm[id].t)+'" dur="1.4s" repeatCount="indefinite"/>'
      : '';
  }
  function critLabel(id, x, y) {
    var z=zm[id]||{};
    if (z.t>=0.75) return '<text x="'+x+'" y="'+y+'" text-anchor="middle" font-size="8" fill="#f43f5e" font-weight="800">⚠ KRİTİK</text>';
    if (z.t>=0.30) return '<text x="'+x+'" y="'+y+'" text-anchor="middle" font-size="8" fill="#f59e0b">▲ Riskli</text>';
    return '';
  }

  var svg =
  '<svg viewBox="0 0 530 330" width="100%" style="max-height:320px;display:block;border-radius:8px;overflow:visible" id="brand-fault-svg">' +
  defs +

  // Başlık
  '<text x="265" y="15" text-anchor="middle" font-size="10" font-weight="700" fill="'+kb.color+'">' +
    kb.name + ' Titreşim Bazlı Arıza Haritası</text>' +
  '<text x="265" y="27" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.25)">Tıklanabilir • Yeşil=Normal • Sarı=Riskli • Kırmızı=Kritik</text>' +

  // Zemin gölgesi
  '<ellipse cx="255" cy="318" rx="218" ry="9" fill="rgba(0,0,0,0.3)"/>' +

  // ŞASİ (arka plan)
  '<g class="fzone" data-zid="fz-chassis" style="cursor:pointer">' +
    '<rect x="110" y="152" width="228" height="88" rx="9" fill="'+Z('fz-chassis').color+'" opacity="'+op(Z('fz-chassis').t)+'"'+gf('fz-chassis')+'>'+anim('fz-chassis')+'</rect>' +
    '<rect x="110" y="152" width="228" height="88" rx="9" fill="none" stroke="'+Z('fz-chassis').stroke+'" stroke-width="'+sw(Z('fz-chassis').t)+'" opacity="0.5"/>' +
    '<text x="224" y="190" text-anchor="middle" font-size="10" font-weight="600" fill="rgba(255,255,255,0.75)">Şasi</text>' +
    '<text x="224" y="203" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.45)">'+val(s?s.Severity.rms:0)+' mg</text>' +
    critLabel('fz-chassis',224,218) +
  '</g>' +

  // MOTOR
  '<g class="fzone" data-zid="fz-motor" style="cursor:pointer">' +
    '<rect x="240" y="158" width="86" height="65" rx="7" fill="'+Z('fz-motor').color+'" opacity="'+op(Z('fz-motor').t)+'"'+gf('fz-motor')+'>'+anim('fz-motor')+'</rect>' +
    '<rect x="240" y="158" width="86" height="65" rx="7" fill="none" stroke="'+Z('fz-motor').stroke+'" stroke-width="'+sw(Z('fz-motor').t)+'" opacity="0.7"/>' +
    '<text x="283" y="183" text-anchor="middle" font-size="11" font-weight="700" fill="rgba(255,255,255,0.95)">Motor</text>' +
    '<text x="283" y="196" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.6)">'+val(s?s.Z.rms:0)+' mg Z</text>' +
    critLabel('fz-motor',283,211) +
  '</g>' +

  // HİDROLİK
  '<g class="fzone" data-zid="fz-hidro" style="cursor:pointer">' +
    '<rect x="134" y="158" width="78" height="65" rx="7" fill="'+Z('fz-hidro').color+'" opacity="'+op(Z('fz-hidro').t)+'"'+gf('fz-hidro')+'>'+anim('fz-hidro')+'</rect>' +
    '<rect x="134" y="158" width="78" height="65" rx="7" fill="none" stroke="'+Z('fz-hidro').stroke+'" stroke-width="'+sw(Z('fz-hidro').t)+'" opacity="0.7"/>' +
    '<text x="173" y="183" text-anchor="middle" font-size="10" font-weight="700" fill="rgba(255,255,255,0.95)">Hidrolik</text>' +
    '<text x="173" y="196" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.6)">'+val(s?s.Y.rms:0)+' mg Y</text>' +
    critLabel('fz-hidro',173,211) +
  '</g>' +

  // ELEKTRONİK
  '<g class="fzone" data-zid="fz-elek" style="cursor:pointer">' +
    '<rect x="344" y="158" width="76" height="65" rx="7" fill="'+Z('fz-elek').color+'" opacity="'+op(Z('fz-elek').t)+'"'+gf('fz-elek')+'>'+anim('fz-elek')+'</rect>' +
    '<rect x="344" y="158" width="76" height="65" rx="7" fill="none" stroke="'+Z('fz-elek').stroke+'" stroke-width="'+sw(Z('fz-elek').t)+'" opacity="0.6"/>' +
    '<text x="382" y="181" text-anchor="middle" font-size="9" font-weight="700" fill="rgba(255,255,255,0.9)">Elektronik</text>' +
    '<text x="382" y="193" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.55)">Kurt:'+val(s?Math.round(Math.max(s.X.kurtosis||0,s.Y.kurtosis||0)):0)+'</text>' +
    critLabel('fz-elek',382,208) +
  '</g>' +

  // KARŞI AĞIRLIK / ARKA AKS
  '<g class="fzone" data-zid="fz-aks" style="cursor:pointer">' +
    '<rect x="344" y="90" width="76" height="62" rx="7" fill="'+Z('fz-aks').color+'" opacity="'+op(Z('fz-aks').t)+'"'+gf('fz-aks')+'>'+anim('fz-aks')+'</rect>' +
    '<rect x="344" y="90" width="76" height="62" rx="7" fill="none" stroke="'+Z('fz-aks').stroke+'" stroke-width="1" opacity="0.5"/>' +
    '<text x="382" y="115" text-anchor="middle" font-size="9" font-weight="600" fill="rgba(255,255,255,0.8)">Karşı Ağ.</text>' +
    '<text x="382" y="128" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.5)">Arka Aks</text>' +
    critLabel('fz-aks',382,143) +
  '</g>' +

  // KABİN
  '<rect x="112" y="88" width="96" height="64" rx="7" fill="rgba(45,90,145,0.38)"/>' +
  '<rect x="114" y="90" width="92" height="60" rx="6" fill="rgba(0,68,102,0.28)"/>' +
  '<text x="160" y="116" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.4)">Kabin</text>' +

  // ROPS
  '<rect x="112" y="70" width="9" height="82" rx="3" fill="rgba(30,58,95,0.95)"/>' +
  '<rect x="199" y="70" width="9" height="82" rx="3" fill="rgba(30,58,95,0.95)"/>' +
  '<rect x="112" y="70" width="96" height="8" rx="3" fill="rgba(37,61,92,1)"/>' +

  // MAST
  '<g class="fzone" data-zid="fz-mast" style="cursor:pointer">' +
    '<rect x="52" y="22" width="15" height="230" rx="4" fill="'+Z('fz-mast').color+'" opacity="'+op(Z('fz-mast').t)+'"'+gf('fz-mast')+'>'+anim('fz-mast')+'</rect>' +
    '<rect x="52" y="22" width="15" height="230" rx="4" fill="none" stroke="'+Z('fz-mast').stroke+'" stroke-width="1" opacity="0.65"/>' +
    '<rect x="76" y="22" width="15" height="230" rx="4" fill="'+Z('fz-mast').color+'" opacity="'+op(Z('fz-mast').t*0.75)+'"/>' +
    '<rect x="52" y="56"  width="39" height="7" rx="2" fill="rgba(55,65,81,0.9)"/>' +
    '<rect x="52" y="100" width="39" height="7" rx="2" fill="rgba(55,65,81,0.9)"/>' +
    '<rect x="52" y="144" width="39" height="7" rx="2" fill="rgba(55,65,81,0.9)"/>' +
    '<rect x="52" y="188" width="39" height="7" rx="2" fill="rgba(55,65,81,0.9)"/>' +
    '<text x="66" y="260" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.4)">Mast</text>' +
    critLabel('fz-mast',66,272) +
  '</g>' +

  // FORK
  '<g class="fzone" data-zid="fz-fork" style="cursor:pointer">' +
    '<rect x="12" y="205" width="50" height="34" rx="5" fill="'+Z('fz-fork').color+'" opacity="'+op(Z('fz-fork').t)+'"/>' +
    '<rect x="5"  y="239" width="63" height="13" rx="3" fill="'+Z('fz-fork').color+'" opacity="'+op(Z('fz-fork').t)+'"/>' +
    '<rect x="5"  y="256" width="63" height="13" rx="3" fill="'+Z('fz-fork').color+'" opacity="'+op(Z('fz-fork').t*0.75)+'"/>' +
    '<text x="36" y="224" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.7)">Fork</text>' +
  '</g>' +

  // ÖN TEKERLEK
  '<g class="fzone" data-zid="fz-wheel" style="cursor:pointer">' +
    '<ellipse cx="150" cy="260" rx="34" ry="34" fill="'+Z('fz-wheel').color+'" opacity="'+op(Z('fz-wheel').t)+'"'+gf('fz-wheel')+'>'+anim('fz-wheel')+'</ellipse>' +
    '<ellipse cx="150" cy="260" rx="34" ry="34" fill="none" stroke="'+Z('fz-wheel').stroke+'" stroke-width="'+sw(Z('fz-wheel').t)+'" opacity="0.6"/>' +
    '<ellipse cx="150" cy="260" rx="21" ry="21" fill="rgba(40,55,70,0.9)"/>' +
    '<ellipse cx="150" cy="260" rx="8"  ry="8"  fill="rgba(65,85,105,0.95)"/>' +
    '<text x="150" y="302" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.35)">Ön Aks</text>' +
    critLabel('fz-wheel',150,313) +
    '<text x="150" y="323" text-anchor="middle" font-size="7" fill="rgba(255,255,255,0.22)">'+val(s?Math.max(s.X.rms,s.Y.rms):0)+' mg</text>' +
  '</g>' +

  // ARKA TEKERLEK
  '<ellipse cx="313" cy="260" rx="26" ry="26" fill="'+Z('fz-aks').color+'" opacity="'+op(Z('fz-aks').t*0.55)+'"/>' +
  '<ellipse cx="313" cy="260" rx="16" ry="16" fill="rgba(40,55,70,0.9)"/>' +
  '<ellipse cx="313" cy="260" rx="6"  ry="6"  fill="rgba(65,85,105,0.95)"/>' +
  '<text x="313" y="295" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.28)">Arka</text>' +

  // LEGEND
  '<rect x="448" y="34" width="12" height="12" rx="2" fill="#10b981"/>' +
  '<text x="464" y="44" font-size="9" fill="rgba(255,255,255,0.45)">Normal</text>' +
  '<rect x="448" y="52" width="12" height="12" rx="2" fill="#f59e0b"/>' +
  '<text x="464" y="62" font-size="9" fill="rgba(255,255,255,0.45)">Riskli</text>' +
  '<rect x="448" y="70" width="12" height="12" rx="2" fill="#f43f5e"/>' +
  '<text x="464" y="80" font-size="9" fill="rgba(255,255,255,0.45)">Kritik</text>' +
  '<rect x="440" y="94" width="80" height="20" rx="4" fill="rgba(255,255,255,0.06)"/>' +
  '<text x="480" y="107" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.3)">👆 Tıkla</text>' +

  '</svg>';

  return '<div class="body-diagram" style="margin-bottom:14px">' +
    '<div class="diag-title">' +
      '<div class="ctd" style="background:' + kb.color + '"></div>' +
      kb.name + ' — Titreşim Bazlı Arıza Haritası' +
      (isSel&&d ? ' <span style="font-size:9px;font-weight:400;color:var(--text3)">('+esc(sh(n,18))+')</span>' : '') +
    '</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start">' +
      '<div>' + svg + '</div>' +
      '<div id="fault-detail-panel" style="background:var(--bg3);border:1px solid var(--border);' +
        'border-radius:12px;padding:18px;min-height:100px;transition:all .2s">' +
        '<div style="text-align:center;padding:30px 0;color:var(--text3);">' +
          '<div style="font-size:28px;margin-bottom:8px;opacity:.4">🎯</div>' +
          '<div style="font-size:11px">Soldaki haritadan bir bölgeye tıklayın</div>' +
          '<div style="font-size:10px;margin-top:4px;opacity:.6">Arıza detayları burada görünecek</div>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</div>';
}

// ── fillDetailPanel: zone tıklanınca detayı doldur ───────────────────────────
function fillDetailPanel(zone) {
  var panel = document.getElementById('fault-detail-panel');
  if (!panel) return;

  var sc = zone.t>=0.75?'#f43f5e':zone.t>=0.30?'#f59e0b':'#10b981';
  var sbg = zone.t>=0.75?'rgba(244,63,94,0.12)':zone.t>=0.30?'rgba(245,158,11,0.10)':'rgba(16,185,129,0.10)';
  var sbr = zone.t>=0.75?'rgba(244,63,94,0.4)' :zone.t>=0.30?'rgba(245,158,11,0.35)':'rgba(16,185,129,0.3)';

  var faultsHTML = '';
  if (zone.faults && zone.faults.length > 0) {
    faultsHTML = '<div style="margin-top:12px">';
    zone.faults.forEach(function(f) {
      var fc = f.sev==='critical'?'#f43f5e':f.sev==='high'?'#f59e0b':'#3b82f6';
      faultsHTML +=
        '<div style="background:rgba(255,255,255,0.025);border:1px solid var(--border);' +
        'border-left:3px solid '+fc+';border-radius:8px;padding:11px;margin-bottom:8px;">' +
          '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:5px">' + f.icon + ' ' + f.title + '</div>' +
          '<div style="font-size:10px;color:var(--text2);line-height:1.65;margin-bottom:7px">' + f.desc + '</div>' +
          '<div style="font-size:9px;color:var(--amber);margin-bottom:7px">📌 Tetikleyen eşik: ' + f.trigger + '</div>' +
          '<div style="display:flex;gap:4px;flex-wrap:wrap">' +
            f.axes.map(function(ax){ return '<span style="font-size:8px;font-weight:700;padding:2px 6px;border-radius:4px;background:rgba(59,130,246,0.15);color:#3b82f6">'+ax+'</span>'; }).join('') +
            '<span style="font-size:8px;font-weight:700;padding:2px 6px;border-radius:4px;background:'+fc+'20;color:'+fc+'">'+f.sevLabel+'</span>' +
          '</div>' +
        '</div>';
    });
    faultsHTML += '</div>';
  } else {
    faultsHTML = '<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.2);' +
      'border-radius:8px;padding:10px;margin-top:10px;font-size:10px;color:var(--green);">' +
      '✓ Bu bölgede veri bazlı kritik eşik aşılmıyor. Rutin izleme yeterli.' +
    '</div>';
  }

  panel.innerHTML =
    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border)">' +
      '<div style="width:10px;height:10px;border-radius:50%;background:'+zone.color+';box-shadow:0 0 6px '+zone.color+'"></div>' +
      '<div style="font-size:14px;font-weight:800;color:var(--text)">' + zone.label + '</div>' +
      '<div style="margin-left:auto;font-size:9px;font-weight:700;padding:3px 10px;border-radius:6px;background:'+sbg+';border:1px solid '+sbr+';color:'+sc+'">' + zone.statusLabel + '</div>' +
    '</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:4px">' +
      '<div style="background:var(--bg4);border-radius:7px;padding:9px 10px">' +
        '<div style="font-size:8px;color:var(--text3);margin-bottom:3px">RMS</div>' +
        '<div style="font-size:16px;font-weight:800;color:'+sc+'">' + zone.rms + '</div>' +
        '<div style="font-size:8px;color:var(--text3)">milli-g</div>' +
      '</div>' +
      '<div style="background:var(--bg4);border-radius:7px;padding:9px 10px">' +
        '<div style="font-size:8px;color:var(--text3);margin-bottom:3px">Risk</div>' +
        '<div style="font-size:16px;font-weight:800;color:'+sc+'">' + Math.round(zone.t*100) + '%</div>' +
        '<div style="font-size:8px;color:var(--text3)">ISO eşiğe oran</div>' +
      '</div>' +
      '<div style="background:var(--bg4);border-radius:7px;padding:9px 10px">' +
        '<div style="font-size:8px;color:var(--text3);margin-bottom:3px">Arıza</div>' +
        '<div style="font-size:16px;font-weight:800;color:'+sc+'">' + (zone.faults?zone.faults.length:0) + '</div>' +
        '<div style="font-size:8px;color:var(--text3)">aktif tespit</div>' +
      '</div>' +
    '</div>' +
    '<div style="font-size:9px;color:var(--text3);margin-bottom:4px;margin-top:6px">Eksen: ' + zone.axis + '</div>' +
    faultsHTML;
}

function buildNoBrandDetected(n, d, fleetBrands) {
  return '<div class="no-brand-msg">' +
    '<div class="no-brand-icon">🔍</div>' +
    '<div class="no-brand-title">Marka Tespit Edilemedi</div>' +
    '<div class="no-brand-sub">Cihaz adı "' + esc(n) + '" Jungheinrich/Still anahtar kelimesi içermiyor.<br>Yukarıdaki butonlardan marka seçin.</div>' +
  '</div>' +
  '<div class="g2">' +
    brandSummaryCard('jungheinrich', fleetBrands.jungheinrich) +
    brandSummaryCard('still', fleetBrands.still) +
  '</div>';
}

function brandSummaryCard(bk, devices) {
  var kb = BRAND_KB[bk];
  var crit = devices.filter(function(p){ return p[1].iso_class==='Critical'; }).length;
  var avg  = devices.length ? (devices.reduce(function(a,p){return a+p[1].risk_score;},0)/devices.length).toFixed(1) : '—';
  return '<div class="card">' +
    '<div class="ct"><div class="ctd" style="background:'+kb.color+'"></div>'+kb.name+'</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px">' +
      '<div class="rc"><div class="rc-l">Filo</div><div class="rc-v" style="color:'+kb.color+'">'+devices.length+'</div></div>' +
      '<div class="rc"><div class="rc-l">Kritik</div><div class="rc-v" style="color:var(--red)">'+crit+'</div></div>' +
      '<div class="rc"><div class="rc-l">Ort.Risk</div><div class="rc-v" style="color:var(--amber)">'+avg+'</div></div>' +
    '</div>' +
    kb.faults.slice(0,5).map(function(f){
      return '<div style="display:flex;align-items:center;gap:6px;padding:5px 0;border-bottom:1px solid var(--border);font-size:10px;color:var(--text2)">' +
        '<span>'+f.icon+'</span><span style="flex:1">'+f.title+'</span>' +
        '<span class="fault-sev s'+f.sev.charAt(0)+'">'+f.sevLabel+'</span></div>';
    }).join('') +
  '</div>';
}

</script>
</body>
</html>
