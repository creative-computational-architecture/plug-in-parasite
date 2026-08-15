#! python 3
# panel_canopy — NEARLY-FLAT version (2026-05-27 v2):
#   The rigging ropes from the spire tip pull each corner taut.
#   Previous version had center_sag = 30% of panel_size — too bowl-like.
#   New ratios make the canopy almost planar with only a slight droop:
#     - center_sag  = 6%  (was 30%)
#     - edge_sag    = 2%  (was 10%)
#     - corner_pull = 5%  unchanged — rigging lifts corners
import Rhino.Geometry as rg
import math

pz = float(panel_z)
pL = float(panel_L)
pW = float(panel_W)
fr = float(f_rise)
fo = float(f_open)
L1 = float(SEG1_L)
hR = float(hub_R)

# panel_z_a — rises from inside seg1 during canopy-rise phase
panel_folded_z = L1 * 0.45
panel_z_a = panel_folded_z + (pz - panel_folded_z) * fr

# Nearly-flat sag parameters
panel_size = max(pL, pW)
center_sag  = panel_size * 0.06
edge_sag    = panel_size * 0.02
corner_pull = panel_size * 0.05

r_closed = hR + 0.8
z_gathered = panel_z_a + panel_size / 4.0

corner_specs = [(pL/2.0, 0.0),
                (pW/2.0, math.pi/2.0),
                (pL/2.0, math.pi),
                (pW/2.0, 3.0*math.pi/2.0)]

def lerp_pt(a, b, t):
    return rg.Point3d(a.X + (b.X-a.X)*t, a.Y + (b.Y-a.Y)*t, a.Z + (b.Z-a.Z)*t)

corners = []
for r_open, az in corner_specs:
    c_closed = rg.Point3d(r_closed*math.cos(az), r_closed*math.sin(az), z_gathered)
    c_open   = rg.Point3d(r_open *math.cos(az), r_open *math.sin(az), panel_z_a + corner_pull)
    corners.append(lerp_pt(c_closed, c_open, fo))

edge_mids = []
for i in range(4):
    c1 = corners[i]; c2 = corners[(i+1) % 4]
    mid_z = z_gathered + (panel_z_a - edge_sag - z_gathered) * fo
    edge_mids.append(rg.Point3d((c1.X+c2.X)/2.0, (c1.Y+c2.Y)/2.0, mid_z))

center_z = z_gathered + (panel_z_a - center_sag - z_gathered) * fo
center_pt = rg.Point3d(0.0, 0.0, center_z)

m = rg.Mesh()
m.Vertices.Add(center_pt)
for c in corners:  m.Vertices.Add(c)
for e in edge_mids: m.Vertices.Add(e)
for i in range(4):
    m.Faces.AddFace(0, 1 + i, 5 + i)
    m.Faces.AddFace(0, 5 + i, 1 + ((i+1) % 4))
m.Normals.ComputeNormals()
m.Compact()

panel = [m]
panel_corners = corners
