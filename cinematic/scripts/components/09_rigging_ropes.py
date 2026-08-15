#! python 3
# rigging_ropes — pipes from spire_tip to all canopy attachment points:
#   - 4 panel corners
#   - 4 spar tips
#   - 4 edge midpoints between consecutive spar tips
# Only generated when f_canopy > 0.001 (no ropes during pure telescope phase).
import Rhino.Geometry as rg
import scriptcontext as sc
from System import Guid

def to_pt(p):
    if isinstance(p, rg.Point3d):
        return p
    if hasattr(p, 'Value') and isinstance(p.Value, rg.Point3d):
        return p.Value
    if isinstance(p, Guid):
        obj = sc.doc.Objects.Find(p)
        if obj is not None and isinstance(obj.Geometry, rg.Point):
            return obj.Geometry.Location
    if hasattr(p, 'X') and hasattr(p, 'Y') and hasattr(p, 'Z'):
        return rg.Point3d(float(p.X), float(p.Y), float(p.Z))
    raise TypeError(f"Cannot convert {type(p).__name__} to Point3d")

tip = to_pt(spire_tip)
corners = [to_pt(p) for p in panel_corners]
tips = [to_pt(p) for p in spar_tips]
fc = float(f_canopy)
rigging_R = max((float(rope_dia) / 2.0) * 0.8, 0.15)

rigging = []
if fc > 0.001:
    targets = list(corners) + list(tips)
    # Add edge midpoints between consecutive spar tips
    for i in range(4):
        a = tips[i]; b = tips[(i+1) % 4]
        targets.append(rg.Point3d((a.X+b.X)/2.0, (a.Y+b.Y)/2.0, (a.Z+b.Z)/2.0))
    for tgt in targets:
        line = rg.LineCurve(tip, tgt)
        pipes = rg.Brep.CreatePipe(line, rigging_R, False, rg.PipeCapMode.Flat, True, 0.001, 0.01)
        if pipes:
            rigging.extend(pipes)
