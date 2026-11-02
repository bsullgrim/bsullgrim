// Render every SVG in src/ to a PNG in out/ at its native size.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const src = path.join(__dirname, process.env.SRC || 'src');
  const out = path.join(__dirname, process.env.OUT || 'out');
  fs.mkdirSync(out, { recursive: true });
  const only = process.argv.slice(2);
  const b = await chromium.launch();
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.svg'))) {
    if (only.length && !only.some(o => f.includes(o))) continue;
    const svg = fs.readFileSync(path.join(src, f), 'utf8');
    const w = +svg.match(/width="(\d+)"/)[1], h = +svg.match(/height="(\d+)"/)[1];
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(out, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: w, height: h } });
    await p.close();
  }
  await b.close();
  console.log('rendered');
})();
