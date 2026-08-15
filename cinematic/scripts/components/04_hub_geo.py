#! python 3
# hub_geo — short cylinder that rises out of seg1 during canopy-rise phase.
# Spars attach radially from this hub.
import Rhino.Geometry as rg

HUB_R = 4.0   # hub radius (constant — passed downstream)
HUB_H = 3.0   # hub thickness

hub_folded_z = float(SEG1_L) * 0.5             # midpoint of seg1, hidden inside
hub_z_a = hub_folded_z + (float(hub_z) - hub_folded_z) * float(f_rise)

hub = [
    rg.Cylinder(
        rg.Circle(
            rg.Plane(rg.Point3d(0, 0, hub_z_a - HUB_H / 2.0), rg.Vector3d.ZAxis),
            HUB_R),
        HUB_H).ToBrep(True, True)
]
hub_R = HUB_R
