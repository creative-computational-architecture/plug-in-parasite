# Animation Rig Scripts (Rhino 8)

Python components that build the fold/deploy animation rig for the Track B clay renders.
Each file in `components/` is one stage of the parametric fold logic — mast, hook, hub,
spars, fabrics, straps — driven by a single `f_open` parameter (0 = folded, 1 = deployed).

## Usage

1. Open `PlugInParasite.3dm` in Rhino 8.
2. Run `setup_views.py` via `_-RunPythonScript` — it creates the named views
   (B1–B5 camera setups) used by the shot list.
3. Load the `components/*.py` files as GhPython components in Grasshopper
   (numbered in dependency order), wire `f_open` to a slider or animation driver.
4. Render frames per the edit pipeline in [`../docs/edit_pipeline_v2.md`](../docs/edit_pipeline_v2.md).
