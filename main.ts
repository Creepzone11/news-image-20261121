// News-image entry for make.fun news-image-20261121 (Node 22, stdlib only).
// The newspaper image sits beside this file as entry.png; the program copies
// it to the grader's output directory as entry.png. No network is used.
// Run locally with: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
