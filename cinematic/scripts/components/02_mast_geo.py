#! python 3
# mast_geo — telescoping mast (3 segments) + ground socket.
# Hook-leads-telescope: HOOK_Z drives seg3 top, which drives seg2 top.
# seg1 is fixed at z=0..SEG1_L (base segment, holds everything else folded).
import Rhino.Geometry as rg

SEG1_R = 5.0
SEG2_R = 2.0
SEG3_R = 1.0
SOCKET_R = 4.5

L1 = float(SEG1_L)
L_other = float(SEG_L)
overlap = float(SEG_OVERLAP)
hook = float(HOOK_Z)
sh = float(socket_h)

# seg3 hangs below hook, clamped so its base never goes below ground
seg3_top  = hook
seg3_base = max(0.0, hook - L_other)

# seg2 sits below seg3 with overlap; stays nested in seg1 until seg3 has climbed
seg2_top  = max(L1, seg3_base + overlap)
seg2_base = max(0.0, seg2_top - L_other)

def cyl(z_base, length, radius):
    return rg.Cylinder(
        rg.Circle(rg.Plane(rg.Point3d(0, 0, z_base), rg.Vector3d.ZAxis), radius),
        length).ToBrep(True, True)

mast = [
    cyl(0.0,       L1,                       SEG1_R),
    cyl(seg2_base, seg2_top - seg2_base,     SEG2_R),
    cyl(seg3_base, seg3_top - seg3_base,     SEG3_R),
]
socket = [cyl(-sh, sh, SOCKET_R)]
