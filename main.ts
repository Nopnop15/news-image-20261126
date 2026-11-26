// The World in One Page — Thursday 26 November 2026.
//
// generate_image.py draws the front page and saves it beside this file as
// entry.png. This script copies those exact bytes to the location the
// grader reads: MAKEFUN_OUTPUT_DIR/entry.png (./out/entry.png by default).
//
//   python3 generate_image.py
//   MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");

if (!existsSync(sourcePath)) {
  throw new Error(
    "entry.png not found — run python3 generate_image.py first",
  );
}
mkdirSync(outputDir, { recursive: true });
const destination = join(outputDir, "entry.png");
copyFileSync(sourcePath, destination);
// Guard against a truncated copy: the output must be the same size.
if (statSync(sourcePath).size !== statSync(destination).size) {
  throw new Error("copied entry.png does not match the source size");
}
console.log(`entry.png -> ${destination}`);
