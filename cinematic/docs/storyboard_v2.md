# Plug-in Parasite — Cinematic Storyboard V2 (2026-05-28)

Updates the original `storyboard.md` for the current state: 10-component
GH canvas, V2.1 hammock, clay material on `#607080`, close-framing camera
(380,-180,280 → 0,0,120 lens 35mm), and a fresh 30s HERO render.

---

## What's already in `cinematic/shots_v2/`

| File | Source | Duration | Resolution | Notes |
|---|---|---:|---|---|
| `HERO_v11_30s.mp4` | render_queue_v2.py (550,-400,180) | 30s | 1280×720 | V12 close framing pending |
| `HERO_30s.mp4` (May 26) | V10 monolithic | 30s | 1280×720 | reference framing |
| `HERO_v4_30s.mp4` (May 26) | V10 earlier | 30s | 1280×720 | reference |
| `an1_rhino_animated.mp4` | Rhino animation export | 4s | 1500×1500 | square, user hand-animated |

> The "close-framing V12" render is in progress (background job
> `bfz2x1d3s`) — it will land at `cinematic/shots_v2/HERO_v12_30s.mp4`
> once ffmpeg composes the 720 PNGs.

## What's missing

- **Track A** (cinematic forest) — 3 atmospheric AI-generated shots
- **Final edit** — DaVinci timeline that interleaves Track A + clay
- **VO + music**

---

## Track A revised — 3 shots, ~$20 on Kling 2.0

**Bookend + hero structure-in-forest:**

```
0:00–0:05   A1  forest establishing               (empty, cinematic AI)
0:05–0:35   B   HERO_v12 30s deploy/retract cycle (clay)
0:35–0:40   A3  hero structure deployed in forest (image-to-video on
                                                   clay keyframe seed)
0:40–0:45   A2  pull-back forest reveal           (empty, cinematic AI)
```

Total **45 seconds**. Cinematic establishing → clay mechanics → hero
in nature → cinematic closure. A3 is the bridge that places the
parasol in its real environment; using image-to-video on a clay
keyframe locks the geometry so Kling doesn't hallucinate the structure
into something else.

If A3 is too hard or budget is tight, fall back to the simpler 3-cut
bookend (drop A3, total 40s) — `track_a_prompts_v2.md` Path 1 vs Path 2
section explains the trade-off.

### A1 — Forest establishing (0:00–0:05)

**Goal:** atmospheric setup. The viewer lands in a peaceful temperate
forest. No structure visible yet. A slow forward dolly draws them in.

**Tool:** Kling 2.0 (Pro), text-to-video.

**Prompt:**
```
Cinematic morning shot in a temperate deciduous forest. Soft sunlight
streaming through tall beech and oak trees, dappled light spots on
the forest floor. Wide-angle establishing shot. Slow forward dolly
movement, very gentle. Light mist near the ground. No people, no
animals. Realistic, just after sunrise. Cinematic depth of field,
shallow focus on a single tree trunk in foreground. Anamorphic lens
look, slight film grain. 16:9, 5 seconds.
```

**Negative:** people, person, human, figure, animals, deer, text, logo,
watermark, blur, overexposed, cartoon, illustration, drone shot.

**Output:** `shots_A/A1_forest_establishing.mp4` (1920×1080, 5s).

### A2 — Pull-back reveal (0:35–0:40)

**Goal:** scale + closure. The camera pulls back from a quiet forest
clearing where the deploy-then-retract cycle just happened. Empty,
serene, "just-departed" feeling. No structure required in this
shot — the cut before is the structure folding back into its bag.

**Prompt:**
```
Cinematic wide pull-back shot from forest clearing outward into a vast
quiet temperate forest. Slow continuous camera retreat. Late morning
light, golden tones, mist between distant trees. Empty clearing
visible center-frame. No people, no objects, no equipment. Realistic,
anamorphic, slight film grain. End on a still wide composition,
20-30% sky visible above tree line. 16:9, 6 seconds.
```

**Negative:** same as A1, plus "tent, camping equipment, structure,
tower, post."

**Output:** `shots_A/A2_pullback.mp4` (1920×1080, 6s — trim to 5s).

---

## Submission checklist for Kling

1. Account: <https://klingai.com> — starter pack ~$10 = 660 credit
2. Pro mode ~70 credit per shot. 2 shots × 3 attempts each = 420 credit
3. Settings per shot:
   - **Mode:** Pro
   - **Aspect:** 16:9
   - **Duration:** 5s (A1) or 6s (A2)
   - **Camera:** Forward Dolly (A1), Pull Back (A2)
   - **Style:** Cinematic
4. **Try 2-3 generations per shot, save all** — pick the best take in
   DaVinci, keep the others as reference.
5. **Download:** original quality MP4, no watermark (paid mode).

---

## Alternative: skip Kling entirely

If you want zero AI cost, the clay HERO is portfolio-ready as-is once
the V12 close-framing render lands. Add:
- 2-sec title card at start (project name + cca-architects)
- 2-sec end card (year + collaborators)
- Soft ambient music (Suno / Epidemic Sound)

Total ~34 sec, portfolio-grade, $0 AI spend.

---

## Files

- `storyboard.md` — original 6-cut hybrid plan (reference)
- `storyboard_v2.md` — this file
- `track_a_prompts.md` — prompts for full 3-shot version
- `track_b_shotlist.md` — clay shot inventory
- `vo_script.md` — EN voiceover + TR subtitle
- `edit_pipeline.md` — DaVinci + ffmpeg notes
- `shots_v2/HERO_v12_30s.mp4` — the new clay hero (in progress)
- `shots_A/` — empty, AI shots land here after Kling generation
