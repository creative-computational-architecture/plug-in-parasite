#! python 3
# fabric_hammock — TAUT V2.1 (2026-05-28 tweak from V2):
#   - edge midpoints sit AT spar tip plane (z = tip_z) so the rigging ropes
#     that terminate at the spar-tip-plane mid-edges actually meet the cloth.
#     Previously (V1) edge_mids dipped 30% of SAG below, leaving a visible gap.
#   - center SAG = 0.13 * tip_r (was 0.10 in V2, was 0.35 in V1) — slightly
#     more visible droop, still taut enough that corners look load-bearing.
import Rhino.Geometry as rg
import scriptcontext as sc
from System import Guid

def to_pt(p):
    if isinstance(p, rg.Point3d): return p
    if hasattr(p, 'Value') and isinstance(p.Value, rg.Point3d): return p.Value
    if isinstance(p, Guid):
        obj = sc.doc.Objects.Find(p)
        if obj is not None and isinstance(obj.Geometry, rg.Point):
            return obj.Geometry.Location
    if hasattr(p, 'X') and hasattr(p, 'Y') and hasattr(p, 'Z'):
        return rg.Point3d(float(p.X), float(p.Y), float(p.Z))
    raise TypeError(f"Cannot convert {type(p).__name__} to Point3d")

tips = [to_pt(p) for p in spar_tips]
tip_z = tips[0].Z
tip_r = abs(tips[0].X)

SAG = max(tip_r * 0.13, 4.0)
center = rg.Point3d(0.0, 0.0, tip_z - SAG)

# Edge midpoints AT the spar-tip plane — meets the rigging rope edge_mids
edge_mids = []
for i in range(4):
    t1 = tips[i]; t2 = tips[(i+1) % 4]
    edge_mids.append(rg.Point3d(
        (t1.X + t2.X) / 2.0,
        (t1.Y + t2.Y) / 2.0,
        tip_z))

m = rg.Mesh()
m.Vertices.Add(center)                     # v0
for tp in tips:      m.Vertices.Add(tp)    # v1..v4
for ep in edge_mids: m.Vertices.Add(ep)    # v5..v8
for i in range(4):
    m.Faces.AddFace(0, 1 + i, 5 + i)
    m.Faces.AddFace(0, 5 + i, 1 + ((i + 1) % 4))
m.Normals.ComputeNormals()
m.Compact()
fabric = [m]
