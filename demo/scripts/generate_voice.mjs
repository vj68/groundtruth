import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const config = JSON.parse(await readFile(path.join(root, "demo/audio/voice/scenes.json"), "utf8"));
const outputDir = path.join(root, "demo/audio/voice/generated");
const apiKey = process.env.ELEVENLABS_API_KEY;

if (!apiKey) throw new Error("ELEVENLABS_API_KEY is required");
await mkdir(outputDir, { recursive: true });

const manifest = { generated_at: new Date().toISOString(), voice: config.voice, takes: [] };
for (const take of config.takes) {
  const output = path.join(outputDir, `${take.id}.mp3`);
  let exists = false;
  try { exists = (await stat(output)).size > 1000; } catch {}

  if (!exists) {
    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${config.voice.voice_id}?output_format=${config.voice.output_format}`,
      {
        method: "POST",
        headers: { "content-type": "application/json", "xi-api-key": apiKey },
        body: JSON.stringify({
          text: take.text,
          model_id: config.voice.model_id,
          voice_settings: {
            stability: 0.43,
            similarity_boost: 0.80,
            style: 0.16,
            use_speaker_boost: true
          }
        })
      }
    );
    if (!response.ok) throw new Error(`${take.id}: ${response.status} ${await response.text()}`);
    await writeFile(output, Buffer.from(await response.arrayBuffer()));
    await new Promise((resolve) => setTimeout(resolve, 350));
  }

  const data = await readFile(output);
  manifest.takes.push({
    ...take,
    file: path.relative(root, output),
    bytes: data.length,
    sha256: createHash("sha256").update(data).digest("hex")
  });
}
await writeFile(
  path.join(root, "demo/audio/voice/manifest.json"),
  JSON.stringify(manifest, null, 2) + "\n"
);
console.log(`Generated ${manifest.takes.length} narration scenes.`);
