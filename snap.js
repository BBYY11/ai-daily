const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/.home/.cache/puppeteer/chrome/linux-149.0.7827.22/chrome-linux64/chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await page.goto('http://127.0.0.1:8765/index.html', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));

  await page.screenshot({ path: '/workspace/ai-daily/assets/preview-top.png', fullPage: false });
  console.log('✓ top');

  await page.screenshot({ path: '/workspace/ai-daily/assets/preview-full.png', fullPage: true });
  console.log('✓ full');

  const heats = await page.$$('.heat');
  if (heats.length > 0) {
    const box = await heats[0].boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await new Promise(r => setTimeout(r, 600));
    await page.screenshot({ path: '/workspace/ai-daily/assets/preview-heat.png', fullPage: false });
    console.log('✓ heat tooltip');
  }

  const rising = await page.$('#rising-grid');
  if (rising) {
    await page.evaluate(el => el.scrollIntoView({ behavior: 'instant', block: 'start' }), rising);
    await new Promise(r => setTimeout(r, 500));
    await page.screenshot({ path: '/workspace/ai-daily/assets/preview-rising.png', fullPage: false });
    console.log('✓ rising');
  }

  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await page.reload({ waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: '/workspace/ai-daily/assets/preview-mobile.png', fullPage: true });
  console.log('✓ mobile');

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
