import { mkdir, readFile, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import path from "node:path";

const root = process.cwd();
const config = JSON.parse(await readFile(path.join(root, "demo/audio/voice/scenes.json"), "utf8"));
const workDir = path.join(root, "demo/audio/processed");
const gap = 0.45;
await mkdir(workDir, { recursive: true });

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) throw new Error(`${command} failed:\n${result.stderr}`);
  return result.stdout.trim();
}

function duration(file) {
  return Number(run("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file]));
}

function stamp(seconds, srt = false) {
  const ms = Math.round(seconds * 1000);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const sec = Math.floor((ms % 60000) / 1000);
  const milli = ms % 1000;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}${srt ? "," : "."}${String(milli).padStart(3, "0")}`;
}

const silence = path.join(workDir, "silence.wav");
run("ffmpeg", ["-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", String(gap), "-c:a", "pcm_s24le", silence]);

const processed = [];
for (const take of config.takes) {
  const input = path.join(root, "demo/audio/voice/generated", `${take.id}.mp3`);
  const output = path.join(workDir, `${take.id}.wav`);
  run("ffmpeg", [
    "-y", "-i", input,
    "-af", "atempo=1.15,highpass=f=70,lowpass=f=14500,acompressor=threshold=0.16:ratio=1.8:attack=8:release=90:makeup=1.08",
    "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", output
  ]);
  processed.push({ ...take, file: output, duration: duration(output) });
}

const concatList = [];
for (let i = 0; i < processed.length; i += 1) {
  concatList.push(`file '${processed[i].file.replaceAll("'", "'\\''")}'`);
  if (i < processed.length - 1) concatList.push(`file '${silence}'`);
}
const concatPath = path.join(workDir, "concat.txt");
await writeFile(concatPath, concatList.join("\n") + "\n");
const rawMaster = path.join(workDir, "narration-raw.wav");
const master = path.join(root, "demo/audio/master.wav");
run("ffmpeg", ["-y", "-f", "concat", "-safe", "0", "-i", concatPath, "-c:a", "pcm_s24le", rawMaster]);
run("ffmpeg", ["-y", "-i", rawMaster, "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", master]);

let cursor = 0;
const timeline = [];
const cues = [];
let cueNumber = 1;
for (let i = 0; i < processed.length; i += 1) {
  const take = processed[i];
  const start = cursor;
  const end = start + take.duration;
  timeline.push({ id: take.id, start, end, duration: take.duration, gap_after: i < processed.length - 1 ? gap : 0, text: take.text });

  const clauses = take.text.match(/[^.!?;]+[.!?;]?/g).map((part) => part.trim()).filter(Boolean);
  const totalWords = clauses.reduce((sum, clause) => sum + clause.split(/\s+/).length, 0);
  let cueStart = start;
  for (let c = 0; c < clauses.length; c += 1) {
    const clause = clauses[c];
    const share = clause.split(/\s+/).length / totalWords;
    const cueEnd = c === clauses.length - 1 ? end : cueStart + take.duration * share;
    cues.push(`${cueNumber++}\n${stamp(cueStart, true)} --> ${stamp(cueEnd, true)}\n${clause}\n`);
    cueStart = cueEnd;
  }
  cursor = end + (i < processed.length - 1 ? gap : 0);
}

await writeFile(path.join(root, "demo/audio/narration-timeline.json"), JSON.stringify({ gap, duration: duration(master), scenes: timeline }, null, 2) + "\n");
await writeFile(path.join(root, "demo/audio/captions.srt"), cues.join("\n") + "\n");
await writeFile(path.join(root, "demo/audio/narration.txt"), config.takes.map((take) => take.text).join("\n\n") + "\n");
console.log(`Audio master: ${duration(master).toFixed(3)} seconds`);
