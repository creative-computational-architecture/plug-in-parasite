# PLUG-IN PARASITE — STRUCTURAL GEOMETRY SPEC (canonical, locked)

**Source of truth:** live Grasshopper model `PlugInParasite.gh` (fold slider GUID
`13550bea-2222-4361-a414-2a1fd2069271`; deployed = fold **1.0**). Measured
2026-06-24 from exact slider reads + baked-geometry bounding boxes.

> **RULE:** every render / AI image MUST match these proportions. Do **not**
> redesign, do **not** change any lengths, do **not** move GH sliders to "scale"
> the object for a scene — scale only in the prompt. The repeated failures came
> from (a) soft/ambiguous references and (b) ignoring the aspect ratio below.

Coordinate system: **Z-up, centimetres**, mast on the Z axis (x = y = 0), ground
plane at z = 0.

---

## GH parameters (deployed)

| param | value | meaning |
|---|---|---|
| `mast_h` | **220 cm** | telescopic mast full height |
| `socket_h` | **15 cm** | ground-anchor sleeve depth (z −15→0) |
| `panel_z` | **175 cm** | top canopy panel height |
| `panel_L × panel_W` | **54 × 50 cm** | canopy panel size |
| `panel_t` | 0.86 cm | canopy thickness |
| `spar_len` | **90 cm** | radial spar length |
| `spar_angle` | **36.5°** | spar splay (deployed) |
| `spar_dia` | 1.43 cm | spar tube diameter |
| `ring_count` | **6** | storage rings |
| `rope_dia` | 0.22 cm | rigging rope diameter (very thin) |
| `hub_z` | 20 | hub rise param |
| `fold` | **0 = folded · 0.5 = extended (canopy closed) · 1 = deployed** |

---

## Vertical stack (deployed, ground = z0)

1. **Socket** — z −15 → 0. Short ground-anchor sleeve the mast plugs into.
   **THE ONLY GROUND-CONTACT POINT, directly beneath the mast.** Nothing else
   touches the earth.
2. **Telescopic mast** — z 0 → 220. Slim vertical pole, **3 nested segments
   narrowing upward**: base seg ≈ Ø10 cm (z 0–50), mid ≈ Ø4 (z 42–135), top ≈ Ø2
   (z 127–220). Brushed aluminium.
3. **Bottom bed (hammock)** — 4 corners at **z 73.5**, reaching **±76.3 cm** on
   the X and Y axes (diamond / rotated-45° square, ~108 cm side). Warm-red
   (`#C43D1C`) ripstop fabric. Sits in the **lower third** (30 % of total height).
4. **6 storage rings** — z ≈ 19 → 50. Concentric horizontal rope rings around the
   lower mast, **below** the bed.
5. **Top canopy panel** — z **175**, **54 × 50 cm** near-horizontal flat cloth,
   upper third (70 % up). Rigging nodes at its 4 edge mid-points.
6. **Hook spire** — z 220 → 233.6. Central spire topped by **4 curved prongs**
   that splay to ±10.6 cm (**span ≈ 21 cm, ≈ 13 cm tall**). Steel. Hooks over a
   tree branch. *In renders show it clearly / slightly emphasised — it reads too
   small otherwise (user note).*

---

## PROPORTIONS / ASPECT RATIO — **LOCK THESE**

- Bounding box: **152.6 (W) × 152.6 (D) × 248.6 (H) cm**.
- **Front silhouette aspect  W : H ≈ 1 : 1.63** — the structure is **~1.6× TALLER
  than it is wide. Distinctly vertical / portrait.** Never squat.
- Mast (220) ≈ **1.44 × bed width** (152.6).
- Heights as fraction of total: bed **30 %**, canopy panel **70 %**, hook **100 %**.
  **Widest point = the bed** (lower third).
- Silhouette read: a slim vertical mast carrying a tall slender **DIAMOND / KITE**
  — rigging fans from the hook (top) down-and-out to the 4 bed corners (widest,
  lower third), then tapers back in to the socket.

---

## Rigging — **STRAIGHT tension lines (tensegrity)**

- **12 ropes**, very thin (Ø 0.22), from the spire/hook down to the canopy-panel
  nodes and the 4 bed corners.
- **Ropes are STRAIGHT, taut, in tension. Never curved, never slack, never
  lengthened.**
- Where a rope meets a **canopy-panel node, its axis does NOT change** — the line
  continues straight through the node (no kink / no direction break).

---

## Membrane (bed) sag

- The warm-red bed is a **shallow catenary** slung between the 4 corners at z 73.5.
- Ideal look = a **soft, comfortable sag** (like the first hero, occupied) — centre
  drops ≈ **25–40 cm** below the corner line. **NOT taut/flat, NOT extreme.**

---

## Recurring AI mistakes — DO NOT REPEAT

- Hook → 2-prong / anchor / too small. **Must be 4 splayed curved prongs, clearly
  visible.**
- Ropes → curved / slack / lengthened. **Keep straight & original length; no kink
  at nodes.**
- Ground contact → drifting off the mast. **Socket only, under the mast.**
- Proportions → squat / wide. **Hold 1 : 1.63 tall; slim mast taller than the bed
  is wide.**
- Storage rings dropped. **Keep all 6.**
- Soft/ambiguous reference (Arctic white-on-white). **Use the edged Technical
  render on grey as the primary lock.**

---

## Canonical reference renders — `geometry_ref/`

| file | state | use |
|---|---|---|
| `deployed_edged.png` | deployed, Technical **edged** (crisp boundaries) | **primary geometry lock** |
| `deployed_clay.png` | deployed clay on grey | solid form |
| `extended_clay.png` | fold 0.5 (mast up, canopy closed) | EXTEND / HOOK beats |
| `folded_clay.png` | fold 0 (compact column + 4-prong hook + strap + socket) | CARRY / SETDOWN beats |

Render recipe: Rhino display mode **Arctic** or **Technical** (edged) ·
background solid `#5D6B7A` · sun alt 40°/az 135° + skylight · `gh_document
capture_viewport` to a **non-Turkish path** (Turkish path fails). GH live preview
is NOT captured → **bake** the 9 geometry script components to a temp layer per
fold state, capture, then delete the layer and restore `fold` + show `PIP_compare`.
