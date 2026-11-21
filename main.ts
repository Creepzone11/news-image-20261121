// News-image entry for make.fun news-image-20261121 (Node 22, stdlib only).
// The newspaper image sits beside this file as entry.png; the program
// validates it (a real 1024x1024 PNG under 1 MiB) and then copies it to
// the grader's output directory as entry.png. No network is used.
// Run locally with: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576;
const src = new URL('./entry.png', import.meta.url);
const png = readFileSync(src);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A, then the IHDR chunk (length 13,
// type 'IHDR') whose first 8 bytes are the big-endian width and height.
const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length > MAX_BYTES) {
  throw new Error(`entry.png is ${png.length} bytes, over the 1,048,576-byte limit`);
}
if (png.length < 33 || !png.subarray(0, 8).equals(signature)) {
  throw new Error('entry.png is not a PNG file (bad signature)');
}
if (png.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
