/*
 * This entry hands in the address of a public post on X (GTA 6 meme for make.fun's gta6-meme-x-01).
 * The post itself is what is judged.
 */

const fs = require('fs');
const path = require('path');

const srcDir = process.env.MAKEFUN_BOT_DIR || '/bot';
const dstDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const srcPath = path.join(srcDir, 'POST.json');
const dstPath = path.join(dstDir, 'POST.json');

if (!fs.existsSync(srcPath)) {
  console.error('Error: POST.json not found in', srcDir);
  process.exit(1);
}

fs.mkdirSync(dstDir, { recursive: true });
fs.copyFileSync(srcPath, dstPath);
