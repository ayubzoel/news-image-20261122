import { copyFileSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const here = new URL("./entry.png", import.meta.url);
const payload = readFileSync(here);
const magic = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < magic.length; i++) {
  if (payload[i] !== magic[i]) {
    throw new Error("entry.png is not a PNG file");
  }
}
const size = statSync(here).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
}
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");
copyFileSync(here, target);
console.log(`copied entry.png (${size} bytes) to ${target}`);
