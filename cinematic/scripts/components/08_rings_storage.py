#! python 3
# rings_storage — horizontal rope rings at multiple heights along the spars.
# Each ring is 4 pipe segments connecting consecutive (interpolated) spar points
# at a fixed fraction along the spar length.
import Rhino.Geometry as rg
import math

AZIMUTHS = [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]

n = max(1, int(ring_count))
rope_R = float(rope_dia) / 2.0
hz = float(hub_z_a)
hR = float(hub_R)
sla = float(spar_len_a)
saa = float(spar_angle_a)
ang_rad = math.radians(saa)
cos_a = math.cos(ang_rad); sin_a = math.sin(ang_rad)

def spar_point(az, frac):
    r = hR + frac * sla * cos_a
    zp = hz + frac * sla * sin_a
    r = max(r, hR)
    return rg.Point3d(r * math.cos(az), r * math.sin(az), zp)

# Ring height fractions: bottom ring at 10% up the spar, top at 55%
fracs = [0.10 + 0.45 * (i / float(max(n - 1, 1))) for i in range(n)]

rings = []
for fr in fracs:
    pts = [spar_point(az, fr) for az in AZIMUTHS]
    for i in range(4):
        line = rg.LineCurve(pts[i], pts[(i+1) % 4])
        pipes = rg.Brep.CreatePipe(line, rope_R, False, rg.PipeCapMode.Flat, True, 0.001, 0.01)
        if pipes:
            rings.extend(pipes)
