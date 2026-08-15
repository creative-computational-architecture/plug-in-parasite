#! python 3
# hook_geo — spire stub + riser pipe + 4 hook curl arcs, all anchored at HOOK_Z.
# spire_tip is the attachment point for rigging ropes.
import Rhino.Geometry as rg
import math

SPIRE_H = 3.0      # short stub on top of seg3
HOOK_RISE = 5.0    # vertical riser between spire and curl arcs
HOOK_CURL_R = 5.0  # curl arc radius
PIPE_R = 0.6
SPIRE_R = 0.6

hz = float(HOOK_Z)

def pipe_from_curve(crv, r):
    pipes = rg.Brep.CreatePipe(crv, r, False, rg.PipeCapMode.Flat, True, 0.001, 0.01)
    return list(pipes) if pipes else []

hook = []

# Spire stub on top of seg3
hook.append(
    rg.Cylinder(rg.Circle(rg.Plane(rg.Point3d(0, 0, hz), rg.Vector3d.ZAxis), SPIRE_R),
                SPIRE_H).ToBrep(True, True)
)
spire_tip = rg.Point3d(0, 0, hz + SPIRE_H)

# Riser pipe from spire tip up by HOOK_RISE
base_z = hz + SPIRE_H
riser = rg.LineCurve(rg.Point3d(0, 0, base_z), rg.Point3d(0, 0, base_z + HOOK_RISE))
hook.extend(pipe_from_curve(riser, PIPE_R))

# Four hook curl arcs at +X, +Y, -X, -Y
p_top = rg.Point3d(0, 0, base_z + HOOK_RISE)
for az in [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]:
    dx = math.cos(az); dy = math.sin(az)
    p_mid = rg.Point3d(HOOK_CURL_R*dx, HOOK_CURL_R*dy, base_z + HOOK_RISE + HOOK_CURL_R)
    p_end = rg.Point3d(2*HOOK_CURL_R*dx, 2*HOOK_CURL_R*dy, base_z + HOOK_RISE)
    arc = rg.ArcCurve(rg.Arc(p_top, p_mid, p_end))
    hook.extend(pipe_from_curve(arc, PIPE_R))
