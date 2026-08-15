#! python 3
# spars_geo — 4 radial spars (pipes) sprouting from the hub at f_open.
# At f_open=0: spars are vertical stubs (angle=89°, length=0.5 — invisible).
# At f_open=1: angle=spar_angle slider, length=spar_len slider.
import Rhino.Geometry as rg
import math

AZIMUTHS = [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]

fo = float(f_open)
hz = float(hub_z_a)
hR = float(hub_R)

spar_angle_a = 89.0 + (float(spar_angle) - 89.0) * fo
spar_len_a   = 0.5  + (float(spar_len)   - 0.5)  * fo
ang_rad = math.radians(spar_angle_a)
cos_a = math.cos(ang_rad); sin_a = math.sin(ang_rad)
spar_R = float(spar_dia) / 2.0

def spar_pt(az, frac):
    r = hR + frac * spar_len_a * cos_a
    zp = hz + frac * spar_len_a * sin_a
    r = max(r, hR)
    return rg.Point3d(r * math.cos(az), r * math.sin(az), zp)

spars = []
spar_tips = []
for az in AZIMUTHS:
    p0 = spar_pt(az, 0.0)
    p1 = spar_pt(az, 1.0)
    spar_tips.append(p1)
    line = rg.LineCurve(p0, p1)
    pipes = rg.Brep.CreatePipe(line, spar_R, False, rg.PipeCapMode.Flat, True, 0.001, 0.01)
    if pipes:
        spars.extend(pipes)
