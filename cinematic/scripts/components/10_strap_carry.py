#! python 3
# strap_carry — diagonal NE shoulder strap (sits between ±X/±Y spars).
# Elastic: bulge factor lerps from 1.0 (loose loop at fold=0) to 0.06
# (retracted flat against body at fold=0.5+).
import Rhino.Geometry as rg

STRAP_R = 0.5
ft = float(f_telescope)
L1 = float(SEG1_L)
R1 = float(SEG1_R)

# NE diagonal anchor offset from mast axis (0.707 = cos(45°))
dx = R1 * 0.707
dy = R1 * 0.707

# Elastic bulge factor — loop collapses to body during telescope phase
bf = 1.0 + (0.06 - 1.0) * ft

pts = [
    rg.Point3d(dx,             dy,             L1 * 0.92),
    rg.Point3d(dx + 7.0  * bf, dy + 7.0  * bf, L1 + 14.0 * bf),
    rg.Point3d(dx + 13.0 * bf, dy + 13.0 * bf, L1 * 0.55),
    rg.Point3d(dx + 7.0  * bf, dy + 7.0  * bf, L1 * 0.10),
    rg.Point3d(dx,             dy,             L1 * 0.08),
]
crv = rg.Curve.CreateInterpolatedCurve(pts, 3)
pipes = rg.Brep.CreatePipe(crv, STRAP_R, False, rg.PipeCapMode.Round, True, 0.001, 0.01)
strap = list(pipes) if pipes else []
