# Edit Pipeline V2 — Bookend Track A + Clay HERO

Companion to `storyboard_v2.md`. The original `edit_pipeline.md` covers
the full 8-cut 42-second hybrid. This file documents the simpler 3-cut
bookend version (40 sec total) which can be assembled with pure ffmpeg
— no DaVinci required for the first portfolio cut.

---

## Inputs

```
cinematic/shots_A/A1_forest_establishing.mp4   1920×1080  5s   Kling
cinematic/shots_v2/HERO_v12_30s.mp4            1280×720  30s   Rhino clay
cinematic/shots_A/A2_pullback.mp4              1920×1080  5s   Kling
```

The clay HERO is 1280×720; Kling output is 1920×1080. ffmpeg will
upscale the clay to 1920×1080 with lanczos before concat.

---

## ffmpeg concat (one-shot)

```bash
# From repo root:
ffmpeg -y \
  -i cinematic/shots_A/A1_forest_establishing.mp4 \
  -i cinematic/shots_v2/HERO_v12_30s.mp4 \
  -i cinematic/shots_A/A2_pullback.mp4 \
  -filter_complex "\
[0:v]scale=1920:1080:flags=lanczos,setsar=1,fps=24[v0];\
[1:v]scale=1920:1080:flags=lanczos,setsar=1,fps=24[v1];\
[2:v]scale=1920:1080:flags=lanczos,setsar=1,fps=24[v2];\
[v0][v1][v2]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \
  cinematic/final/PlugInParasite_v2_40s.mp4
```

Output:
- 1920×1080 24fps 40s ~5-10MB H.264
- No audio yet (added in pass 2 below)

---

## Audio pass (after Kling shots arrive)

Two tracks:
1. **Music bed** — minimal cinematic ambient. Either Suno, Epidemic Sound,
   or a free Creative Commons piece. Recommended: 40-sec piece with one
   gentle swell around the 8-second mark (right when the HERO clay
   starts spreading).
2. **Forest ambient** — light wind + distant birds during A1/A2,
   silenced during the clay HERO middle.

Mix with:
```bash
ffmpeg -y \
  -i cinematic/final/PlugInParasite_v2_40s.mp4 \
  -i cinematic/audio/music_bed.mp3 \
  -i cinematic/audio/ambient_forest.mp3 \
  -filter_complex "[1:a]volume=0.7[m];\
[2:a]volume=0.4,atrim=0:5,apad,atrim=0:40[a1];\
[2:a]volume=0.4,atrim=0:5,adelay=35s|35s,apad,atrim=0:40[a2];\
[a1][a2]amix=inputs=2[ambient];\
[m][ambient]amix=inputs=2:duration=longest[outa]" \
  -map 0:v -map "[outa]" \
  -c:v copy -c:a aac -b:a 192k -ac 2 \
  -loudnorm I=-14 \
  cinematic/final/PlugInParasite_v2_40s_audio.mp4
```

Loudness normalized to -14 LUFS (Instagram / LinkedIn standard).

---

## Title cards (optional pass 3 — DaVinci or ffmpeg drawtext)

If you want a project name overlay, easiest path is DaVinci:
- 0:00–0:02 fade-in "PLUG-IN PARASITE"
- 0:38–0:40 fade-in "caglarcelik architects · 2026"

Or pure ffmpeg drawtext (no DaVinci):
```bash
ffmpeg -y -i cinematic/final/PlugInParasite_v2_40s_audio.mp4 \
  -vf "drawtext=fontfile=/path/to/InterTight-SemiBold.ttf:\
text='PLUG-IN PARASITE':fontcolor=white@0.9:fontsize=42:\
x=(w-text_w)/2:y=h-150:\
enable='between(t,0.5,2.0)':alpha='if(lt(t,0.5),0,if(lt(t,0.8),(t-0.5)/0.3,if(lt(t,1.7),1,(2.0-t)/0.3)))'" \
  -c:a copy \
  cinematic/final/PlugInParasite_v2_40s_titled.mp4
```

(Path the font file accordingly; on this machine fonts live in
`<your-fonts-dir>/` or via FontBase.)

---

## Output naming convention

```
PlugInParasite_v2_40s.mp4           video only (no audio)
PlugInParasite_v2_40s_audio.mp4     +music +ambient, -14 LUFS
PlugInParasite_v2_40s_titled.mp4    +intro/outro cards
PlugInParasite_v2_40s_FINAL.mp4     master, includes everything
```

Social variants (after FINAL):
- `_IG_9x16.mp4` — 1080×1920 vertical, parasol must stay centered
- `_LinkedIn.mp4` — copy of FINAL
- `_Twitter.mp4` — same as FINAL but capped at 2:20 (auto-loops)

---

## Track A still missing?

If Kling/Luma submission delayed, ship the **clay HERO alone** as a
single-piece portfolio asset:

```bash
ffmpeg -y -i cinematic/shots_v2/HERO_v12_30s.mp4 \
  -vf "scale=1920:1080:flags=lanczos,setsar=1" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \
  cinematic/final/PlugInParasite_clay_30s_1080p.mp4
```

A 30-second clean clay deploy/retract loop. Fine for LinkedIn /
Instagram on its own.
