"""
Plug-in Parasite — Camera setup for Track B clay renders
========================================================

Creates 5 named views (cam_B1 ... cam_B5) in the active Rhino document.
Camera positions are PROPORTIONAL to the model height (H), so they
auto-scale regardless of document unit (mm / cm / m / inch).

USAGE
-----
1. Open PlugInParasite.3dm in Rhino 8.
2. Activate the "Perspective" viewport.
3. Rhino command line:
     _-RunPythonScript "<repo>\\cinematic\\scripts\\setup_views.py"
   (or use _EditPythonScript and Open this file.)
4. Check the Named Views panel — 5 new views should appear.
5. To preview: _-NamedView Restore cam_B1_folded

NOTES
-----
- Coords are multiples of H (deployed model height). If you tweak the
  model, change H below and re-run.
- Tested with Rhino 8 IronPython 2.7 and Python 3.9+ (rhinoscriptsyntax).
"""

import rhinoscriptsyntax as rs

# ============================================================
# CONFIG
# ============================================================
# Document unit detection (Rhino unit system IDs: 2=mm, 3=cm, 4=m, 8=inch)
_unit_map = {2: ("mm", 2200.0), 3: ("cm", 220.0), 4: ("m", 2.2), 8: ("inch", 86.6)}
_us = rs.UnitSystem()
_unit_name, H = _unit_map.get(_us, ("unknown", 220.0))
print("Document unit: {0}  ->  using H = {1} {0} (deployed model height)".format(_unit_name, H))


def make_view(name, target, camera, lens=50):
    """Set Perspective viewport to (camera->target) with given lens, save as named view."""
    # Scale proportional coords by H
    t = [c * H for c in target]
    c = [c * H for c in camera]

    rs.CurrentView("Perspective")
    rs.ViewProjection("Perspective", 2)  # 2 = perspective
    rs.ViewCameraTarget(view="Perspective", camera=c, target=t)
    rs.ViewCameraLens(view="Perspective", length=lens)

    if rs.IsNamedView(name):
        rs.DeleteNamedView(name)
    rs.AddNamedView(name=name, view="Perspective")
    print("  + {0:24s}  target={1}  camera={2}  lens={3}mm".format(name, t, c, lens))


# ============================================================
# NAMED VIEWS  (all coords as multiples of H)
# ============================================================
# B1 — Folded reveal: eye-level, mid-distance turntable start position
make_view("cam_B1_folded",
          target=(0.00, 0.00, 0.10),
          camera=(0.45, -0.45, 0.18),
          lens=50)

# B2 — Phased fold up: 3/4 front, slightly elevated, framing entire deployed height
make_view("cam_B2_foldup",
          target=(0.00, 0.00, 0.45),
          camera=(0.70, -0.70, 0.55),
          lens=35)

# B3 — Hook lock close-up: top of mast, 85mm telefoto, looking down ~30°
make_view("cam_B3_hooklock",
          target=(0.00, 0.00, 0.92),
          camera=(0.12, -0.22, 1.05),
          lens=85)

# B4 — Lower drop: 3/4 side, framing storage frame + hammock + canopy
make_view("cam_B4_lowerdrop",
          target=(0.00, 0.00, 0.50),
          camera=(0.80, -0.80, 0.55),
          lens=50)

# B5 — Absence composition: 7/8 front, low eye-level (gear-level), pushes in
make_view("cam_B5_absence",
          target=(0.00, 0.00, 0.30),
          camera=(0.55, -0.62, 0.32),
          lens=35)

print("\nDone — 5 named views created.")
print("Open  Panels -> Named Views  to see and restore them.")
print("Render test:  _-NamedView Restore cam_B1_folded  then  _Render")
