const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

(async () => {
    const tasks = JSON.parse(fs.readFileSync('/tmp/render_tasks.json', 'utf8'));
    const viewerScript = fs.readFileSync('Đồ án/drawio/viewer-static.min.js', 'utf8');
    
    console.log(`Starting fast local compilation of all ${tasks.length} diagrams...`);
    const startTime = Date.now();
    
    const browser = await puppeteer.launch({
        executablePath: '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 2600, height: 2200, deviceScaleFactor: 2 });

    await page.setContent(`<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; padding: 25px; background: white; font-family: 'Times New Roman', serif; }
        .mxgraph { background: white; }
    </style>
</head>
<body>
    <div id="container"></div>
    <script>${viewerScript}</script>
</body>
</html>`, { waitUntil: 'load' });

    let successCount = 0;

    for (let i = 0; i < tasks.length; i++) {
        const { name, filename, outputPath } = tasks[i];
        const xml = fs.readFileSync(path.join('Đồ án/drawio', filename), 'utf8');
        process.stdout.write(`[${i+1}/${tasks.length}] Compiling ${filename} (${name})... `);
        
        try {
            await page.evaluate((xmlStr) => {
                const container = document.getElementById('container');
                container.innerHTML = '';
                const div = document.createElement('div');
                div.className = 'mxgraph';
                div.setAttribute('data-mxgraph', JSON.stringify({
                    highlight: 'none',
                    nav: false,
                    resize: true,
                    xml: xmlStr
                }));
                container.appendChild(div);
                GraphViewer.processElements();
            }, xml);
            
            await new Promise(r => setTimeout(r, 250));
            const svg = await page.$('svg');
            if (!svg) {
                throw new Error('SVG not generated');
            }
            await svg.screenshot({ path: outputPath });
            successCount++;
            console.log('OK');
        } catch (err) {
            console.log('FAILED: ' + err.message);
        }
    }
    
    await browser.close();
    console.log(`\n========================================`);
    console.log(`Successfully compiled ${successCount}/${tasks.length} diagrams in ${(Date.now() - startTime) / 1000}s!`);
    console.log(`Saved all images in: Đồ án/rendered_images/`);
    console.log(`========================================`);
})();
