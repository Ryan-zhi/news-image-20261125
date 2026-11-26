// Entry point for the news-image-20261125 submission.
//
// The artwork itself is produced by the Python renderer in this folder
// (draw.py paints the page, day25.py holds the words). This script is the
// program the grader runs: it places the finished poster at
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the
// grader's container), then prints a short dossier -- the file inventory,
// the poster's SHA-256 and the day's front page in text form -- so the
// submission can be checked without opening the image.
//
// Run it from the kit with:  node main.ts   (or via the makefun CLI)

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

// The grader reads exactly the bytes this program leaves behind.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

function fingerprint(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

console.log("news-image-20261125 - one picture, one day: Wednesday 25 November 2026");
console.log(`poster written to ${join(outDir, "entry.png")}`);
console.log("files in this entry:");
for (const name of readdirSync(here).sort()) {
  const full = join(here, name);
  if (statSync(full).isFile()) {
    console.log(`  ${name}  ${statSync(full).size} bytes`);
  }
}
console.log(`entry.png sha256: ${fingerprint(join(here, "entry.png"))}`);
console.log("lead: Houthis widen strikes on Saudi ports and refinery");
console.log("cards: Pakistan's first astronaut at China's station; graft purge");
console.log("       reaches the Politburo; US proposes tariffs up to 25% on 14");
console.log("       partners; record 2,100 migrants reach the Canaries in a day");
