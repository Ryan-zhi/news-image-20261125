// Entry for make.fun's news-image-20261125 contest: one picture that sums
// up the world news of Wednesday 25 November 2026.
//
// The picture ships in this folder as entry.png — a broadsheet front page
// drawn with PIL by draw.py out of the stories collected in day25.py:
// Houthi attacks on Saudi Arabia's Ras Tanura refinery and Riyadh's
// financial district, Pakistan's first astronaut docking at China's
// Tiangong station aboard Shenzhou-24, Beijing's graft purge reaching
// another Politburo member, a fresh US tariff threat rattling markets,
// and a record day of migrant arrivals in the Canary Islands.
// All this program does at grading time is place that picture where the
// judges look for it: MAKEFUN_OUTPUT_DIR if the harness sets it,
// otherwise /output.

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(join(here, 'entry.png'), target);
console.log(`news-image-20261125: front page for 25 November 2026 written to ${target}`);
