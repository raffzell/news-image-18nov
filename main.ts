// Entry program for the news-image competition: deliver the finished
// front-page image to the harness output directory. The image itself is
// pre-drawn (see render.py); this program only places a copy of it at
// the path the grader reads.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const entryDir = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || "/output");
const destination = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(entryDir, "entry.png"), destination);
