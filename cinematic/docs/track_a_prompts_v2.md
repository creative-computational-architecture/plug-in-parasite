# Track A Prompts V2 — paste-ready Kling submission

Three shots for the cinematic wrapper:

- **A1** — empty forest establishing (atmosphere setup, no structure)
- **A2** — empty forest pullback (closure, no structure)
- **A3** — **structure deployed in forest** (full description, hung from tree)

A1 and A2 are deliberately empty so Kling's hallucination risk stays
contained. A3 is the hero "in the wild" shot — it describes the
parasol explicitly: vertical mast, 4-prong curl hook at top hooking
around a tree branch, hanging hammock seat below, small flat canopy
above, tensile rigging ropes, storage ring frame around the lower
mast. Best run as **image-to-video** with a clay HERO keyframe as
the seed so Kling has the geometry locked in visually.

Total ~$15-25 at Kling Pro depending on how many re-rolls A3 needs.

> Rules across all three shots: **no people, no figures, no equipment**
> other than the parasol itself.

---

## A1 — Forest Establishing (5 seconds)

**Settings (klingai.com):**
- Mode: **Pro**
- Aspect: **16:9**
- Duration: **5s**
- Camera: **Forward Dolly Slow**
- Style: **Cinematic**

**Prompt:**
```
Cinematic morning shot in a temperate deciduous forest. Soft sunlight
streaming through tall beech and oak trees, dappled light spots on
the forest floor. Wide-angle establishing shot. Slow forward dolly
movement, very gentle. Light mist near the ground. No people, no
animals. Realistic, just after sunrise. Cinematic depth of field,
shallow focus on a single tree trunk in foreground. Anamorphic lens
look, slight film grain.
```

**Negative prompt:**
```
people, person, human, figure, animals, deer, text, logo, watermark,
blur, overexposed, cartoon, illustration, drone shot, top-down, snow
```

**Try count:** generate 3, pick best (mist consistency + dappled light
pattern matter most). Save the runners-up in `shots_A/A1_v01.mp4`,
`A1_v02.mp4`, etc. before deciding.

**Save as:** `cinematic/shots_A/A1_forest_establishing.mp4`

---

## A2 — Pull-back Reveal (6 seconds)

**Settings:**
- Mode: **Pro**
- Aspect: **16:9**
- Duration: **6s**  (trim to 5s in edit)
- Camera: **Pull Back**
- Style: **Cinematic**

**Prompt:**
```
Cinematic wide pull-back shot from forest clearing outward into a vast
quiet temperate forest. Slow continuous camera retreat. Late morning
light, golden tones, mist between distant trees. Empty clearing
visible center-frame. No people, no objects, no equipment. Realistic,
anamorphic, slight film grain. End on a still wide composition,
20-30% sky visible above tree line.
```

**Negative prompt:**
```
people, person, human, figure, animals, vehicles, text, logo,
watermark, drone shot, top-down, tent, camping equipment, structure,
tower, post, building, snow, rain
```

**Try count:** 3 generations. The "empty clearing center-frame" is the
hard constraint — if Kling hallucinates a structure in the middle,
re-roll.

**Save as:** `cinematic/shots_A/A2_pullback.mp4`

---

---

## A3 — Hero in Forest (5 seconds, image-to-video PREFERRED)

This is the shot where the AI needs to know what the structure is.
Two paths; **path 1 (image-to-video) is strongly preferred** because it
locks in the geometry from a real render.

### Structure description (used in BOTH paths)

The parasol is a minimalist white plaster-finish sculptural object:

- **Top:** a small 4-pronged curl hook in white pipe, like four
  question marks fanning outward, that wraps around a tree branch
  to suspend the entire assembly from above.
- **Vertical mast:** a slender 3-segment telescoping white cylinder
  running straight down from the hook, about 2.2 meters tall.
- **Just below the hook:** a small nearly-flat square white cloth
  canopy (about 40 × 30 cm) held taut by tensile ropes radiating
  from the hook above.
- **Middle of the mast:** a small white cylindrical hub from which
  four white spar pipes extend outward and slightly upward like an
  inverted umbrella, at about 35° from horizontal.
- **At the tips of the spars:** a large square hammock seat in
  taut white fabric, stretched between the four spar tips — like
  an architectural seat suspended in the air.
- **Around the lower mast:** horizontal rope rings forming a small
  storage frame.
- **Tensile rigging:** thin white ropes from the hook at the top
  down to the panel corners, spar tips, and edge midpoints —
  giving the whole assembly a sailboat-rigging appearance.

White plaster finish throughout. Soft skylight, shadow-only ground.

### Path 1 — Image-to-video on a clay keyframe (RECOMMENDED)

**Seed image:** pick a single frame from
`cinematic/shots_v2/HERO_v12_30s.mp4` where the structure is fully
deployed (around mid-video, 15 seconds in). Extract with:

```bash
ffmpeg -y -ss 15 -i cinematic/shots_v2/HERO_v12_30s.mp4 \
  -frames:v 1 cinematic/shots_A/A3_seed.png
```

Upload that PNG to Kling's image-to-video.

**Motion prompt (paste into Kling):**
```
A white minimalist sculptural object suspended from a high tree
branch in a quiet temperate forest clearing. The four-pronged hook at
the top grips the branch from above. Dappled morning sunlight
filtering through leaves overhead casts shifting light spots on the
clay-white surfaces. Subtle wind: the hammock fabric below sways
very gently, the small canopy above lifts and settles, the tensile
ropes vibrate softly. Dust particles drift in the sunbeams. Static
camera, locked off, slight handheld breath. Realistic, photographic,
shallow depth of field, anamorphic lens, 5 seconds.
```

**Negative prompt:**
```
people, person, human, figure, hands, arms, animals, deer, birds,
text, logo, watermark, structure changes shape, structure deforms,
structure spins, camera zoom, camera pan, drone shot
```

**Settings:** Pro, 16:9, 5s, Camera = Static, Style = Cinematic,
Image weight = high (so Kling preserves the structure faithfully).

**Try count:** 3. Watch for hammock distortion and hook hallucinations
into something else (often becomes a wind chime or lantern).

**Save as:** `cinematic/shots_A/A3_hero_in_forest.mp4`

### Path 2 — Text-only fallback (riskier, may hallucinate geometry)

If image-to-video isn't available or the seed approach fails, try
text-to-video with the full description:

```
A minimalist white plaster sculptural object suspended from a high
oak tree branch in a quiet temperate forest clearing. The object has
a small 4-pronged curl hook at the very top wrapping around the
branch like four question marks. Directly below the hook hangs a
slender 3-segment vertical white mast, about 2 meters long, with a
small flat square white canopy near the top. Mid-mast, four white
spars extend outward and slightly upward like an inverted umbrella,
with a large taut square white hammock fabric stretched between
their tips. Thin tensile ropes connect the hook down to every
attachment point. Dappled morning sunlight, subtle wind moving the
hammock and the leaves. Static camera. Realistic photographic
architectural product film aesthetic, shallow depth of field. 5
seconds, 16:9, anamorphic.
```

Same negative prompt as path 1. Expect 5-6 re-rolls; this is the
hardest shot to nail.

---

## Budget plan

| Item | Credit | USD |
|---|---:|---:|
| Kling starter pack | 660 | ~$10 |
| A1 × 3 generations (Pro) | 210 | (covered) |
| A2 × 3 generations (Pro) | 210 | (covered) |
| A3 × 3 generations image-to-video (Pro) | 240 | top-up needed |
| Buffer for A3 re-rolls | 300 | top-up needed |
| **Total** | **1160** | **~$20** |

A3 image-to-video runs a bit more credit per generation than text-to-
video (image weight processing). Budget two top-ups of $10 each in case
A3 needs 5-6 re-rolls.

---

## Acceptance criteria

A1 passes if:
- [ ] No human visible anywhere in 5 sec
- [ ] Forward dolly motion is smooth (no jitter)
- [ ] Dappled light pattern is consistent across the 5 sec
- [ ] Foreground tree trunk in focus, background bokeh

A2 passes if:
- [ ] Center frame stays empty (no structure hallucination)
- [ ] Pull-back is smooth and continuous (no jump cuts)
- [ ] End frame composition can hold a 1-2 sec still (for outro
      typography to land)
- [ ] Sky visible at the top of the frame at the end

A3 passes if:
- [ ] Structure shape stays close to the seed image (hook + mast +
      hammock + canopy + spars + rigging all preserved)
- [ ] Hook is wrapping around the tree branch from above (not floating
      next to it)
- [ ] No people / hands appear
- [ ] Hammock swing is subtle (a few cm of motion, not whipping)
- [ ] Lighting is dappled forest morning, not harsh studio or sunset

---

## Once both shots are downloaded

Use `cinematic/edit_pipeline_v2.md` ffmpeg concat recipe:

```bash
ffmpeg -y \
  -i cinematic/shots_A/A1_forest_establishing.mp4 \
  -i cinematic/shots_v2/HERO_v12_30s.mp4 \
  -i cinematic/shots_A/A2_pullback.mp4 \
  -filter_complex "[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[2:v]scale=1920:1080[v2];[v0][v1][v2]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" -c:v libx264 -pix_fmt yuv420p -crf 18 \
  cinematic/final/PlugInParasite_v2_40s.mp4
```

That's the portfolio-ready first cut. Audio mix is a separate pass
(see `edit_pipeline_v2.md`).
