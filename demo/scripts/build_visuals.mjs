import { mkdir, readFile, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import path from "node:path";

const root = process.cwd();
const audio = JSON.parse(await readFile(path.join(root, "demo/audio/narration-timeline.json"), "utf8"));
const workDir = path.join(root, "demo/visuals/scenes");
await mkdir(workDir, { recursive: true });

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) throw new Error(`${command} failed:\n${result.stderr}`);
  return result.stdout.trim();
}

const sceneSpan = (index) => {
  const current = audio.scenes[index];
  const next = audio.scenes[index + 1];
  return (next ? next.start : audio.duration) - current.start;
};

const spans = audio.scenes.map((_, index) => sceneSpan(index));
const shots = [
  { id: "01-problem", kind: "still", src: "demo/deck/rendered/problem.png", duration: spans[0] },
  { id: "02-overview", kind: "still", src: "demo/assets/screenshots/01-overview.png", duration: spans[1] },
  { id: "03-loop", kind: "still", src: "demo/deck/rendered/loop.png", duration: spans[2] },
  { id: "04-real-input", kind: "video", src: "demo/capture/raw/authentic-product-tour.webm", sourceStart: 4.0, duration: spans[3] },
  { id: "05-agents", kind: "video", src: "demo/capture/raw/authentic-product-tour.webm", sourceStart: 19.2, duration: spans[4] },
  { id: "06-proof", kind: "still", src: "demo/assets/screenshots/03-agent-trace.png", duration: spans[5] },
  { id: "07-reveal", kind: "still", src: "demo/deck/rendered/proof.png", duration: spans[6] },
  { id: "08-memory", kind: "still", src: "demo/assets/screenshots/04-blast-radius.png", duration: spans[7] },
  { id: "09-people", kind: "still", src: "demo/assets/screenshots/08-capability.png", duration: spans[8] },
  { id: "10a-architecture", kind: "still", src: "demo/deck/rendered/architecture.png", duration: 8.0 },
  { id: "10b-cloud", kind: "cloud", src: "demo/assets/screenshots/10-google-cloud-function.png", duration: spans[9] - 8.0 },
  { id: "11-close", kind: "still", src: "demo/deck/rendered/close.png", duration: spans[10] }
];

const outputs = [];
for (const [index, shot] of shots.entries()) {
  const output = path.join(workDir, `${String(index + 1).padStart(2, "0")}-${shot.id}.mp4`);
  const input = path.join(root, shot.src);
  const args = ["-y"];
  if (shot.kind === "video") args.push("-ss", String(shot.sourceStart), "-i", input);
  else args.push("-loop", "1", "-framerate", "30", "-i", input);

  let filter = "scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0c1712,fps=30,format=yuv420p";
  if (shot.kind === "cloud") filter = "crop=1600:900:0:70,scale=1920:1080:flags=lanczos,fps=30,format=yuv420p";
  args.push(
    "-t", shot.duration.toFixed(6), "-vf", filter,
    "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", output
  );
  run("ffmpeg", args);
  outputs.push(output);
}

const concatPath = path.join(workDir, "concat.txt");
await writeFile(concatPath, outputs.map((file) => `file '${file.replaceAll("'", "'\\''")}'`).join("\n") + "\n");
const visualMaster = path.join(root, "demo/visuals/visual-master.mp4");
run("ffmpeg", ["-y", "-f", "concat", "-safe", "0", "-i", concatPath, "-c", "copy", "-movflags", "+faststart", visualMaster]);
await writeFile(path.join(root, "demo/visuals/visual-timeline.json"), JSON.stringify({ duration: audio.duration, shots }, null, 2) + "\n");
console.log(`Visual master: ${audio.duration.toFixed(3)} seconds across ${shots.length} shots.`);
