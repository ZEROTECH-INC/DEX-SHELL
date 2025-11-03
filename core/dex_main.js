// core/dex_main.js
// Node helper: serves static files from repository root (useful for quick UI previews)
const http = require('http');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const port = process.env.PORT || 8080;

const mime = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

http.createServer((req, res) => {
  let p = req.url;
  if (p === '/') p = '/core/dex_interface_preview.html';
  let file = path.join(root, p);
  if (!fs.existsSync(file)) {
    res.writeHead(404); res.end('Not Found'); return;
  }
  let ext = path.extname(file);
  res.writeHead(200, {'Content-Type': mime[ext] || 'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
}).listen(port, () => {
  console.log(`DEX helper server running at http://localhost:${port}`);
});
