const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const mode = process.argv[2]; // 'preview' or 'full'
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => { if (m.type() === 'error' || m.type()==='warning') console.log('PAGE', m.type(), m.text().slice(0, 300)); });
  page.on('pageerror', e => console.log('PAGEERR', e.message));
  await page.goto('http://127.0.0.1:8769/index.html');
  await page.waitForFunction('window.READY === true', null, { timeout: 120000 });
  const tl = require('./timeline.json');
  if (mode === 'preview') {
    const ts = process.argv.slice(3).map(Number);
    for (const t of ts) { await page.evaluate(t => window.renderFrame(t), t); await page.screenshot({ path: `${process.env.PD||'prev'}/p_${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 80 }); console.log('shot', t); }
  } else {
    const fps = 30, n = Math.ceil(tl.total * fps);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', 'video_noaudio.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.renderFrame(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log(`frame ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
