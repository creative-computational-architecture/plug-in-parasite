"""
Plug-in Parasite — Fusion 360 parametric build script
======================================================

Run this as a Fusion script:
    Utilities > ADD-INS > Scripts and Add-Ins > Scripts > + > load this file
    then click Run.

It creates a new Fusion design containing:
  - 27 user parameters that drive every dimension
  - Mast              : 3 telescopic tube segments
  - Socket            : bollard-grabbing base + mast collar
  - LowerCanopy       : hub + 4 spars sweeping outward and upward
  - UpperCanopy       : smaller hub + 4 shorter spars
  - TopMast           : yard + rectangular topsail + pennant
  - Fabrics           : two loft surfaces (inverted-pyramid canopies)

Change parameters via Modify > Change Parameters to drive the geometry.

Author: caglarcelik architects (cca)
"""
import adsk.core
import adsk.fusion


# ----------------------------------------------------------------------- params
USER_PARAMS = [
    # name,                expression,    unit,  comment
    ('mast_height_open',  '2200 mm', 'mm',  'Total mast height when fully extended'),
    ('seg1_OD',           '32 mm',   'mm',  'Bottom segment outer diameter'),
    ('seg1_WT',           '1.5 mm',  'mm',  'Bottom segment wall thickness'),
    ('seg2_OD',           '25 mm',   'mm',  'Middle segment outer diameter'),
    ('seg2_WT',           '1.2 mm',  'mm',  'Middle segment wall thickness'),
    ('seg3_OD',           '19 mm',   'mm',  'Top segment outer diameter'),
    ('seg3_WT',           '1.0 mm',  'mm',  'Top segment wall thickness'),
    ('seg_overlap',       '80 mm',   'mm',  'Telescope overlap when extended'),
    ('seg_length',        '(mast_height_open + 2 * seg_overlap) / 3', 'mm',
        'Length of each telescopic segment (derived)'),

    ('socket_inner_dia',  '90 mm',   'mm',  'Bollard socket inner diameter'),
    ('socket_wall',       '8 mm',    'mm',  'Socket wall thickness'),
    ('socket_length',     '150 mm',  'mm',  'Socket length below mast base'),
    ('socket_mast_collar','60 mm',   'mm',  'Collar above ground gripping mast'),

    ('lower_hub_OD',      'seg1_OD + 12 mm', 'mm', 'Lower hub outer diameter'),
    ('lower_hub_H',       '30 mm',           'mm', 'Lower hub height'),
    ('lower_hub_z',       '600 mm',          'mm', 'Lower hub elevation on mast'),
    ('lower_spar_count',  '4',               '',   'Number of lower canopy spars'),
    ('lower_spar_length', '900 mm',          'mm', 'Lower spar length'),
    ('lower_spar_angle',  '35 deg',          'deg','Lower spar elevation angle'),
    ('lower_spar_dia',    '8 mm',            'mm', 'Lower spar rod diameter'),

    ('upper_hub_OD',      'seg2_OD + 10 mm', 'mm', 'Upper hub outer diameter'),
    ('upper_hub_H',       '25 mm',           'mm', 'Upper hub height'),
    ('upper_hub_z',       '1500 mm',         'mm', 'Upper hub elevation on mast'),
    ('upper_spar_count',  '4',               '',   'Number of upper canopy spars'),
    ('upper_spar_length', '450 mm',          'mm', 'Upper spar length'),
    ('upper_spar_angle',  '30 deg',          'deg','Upper spar elevation angle'),
    ('upper_spar_dia',    '6 mm',            'mm', 'Upper spar rod diameter'),

    ('yard_z',            '1950 mm', 'mm', 'Top horizontal yard elevation'),
    ('yard_length',       '350 mm',  'mm', 'Top yard length'),
    ('yard_dia',          '6 mm',    'mm', 'Yard rod diameter'),
    ('topsail_width',     '300 mm',  'mm', 'Top sail width'),
    ('topsail_height',    '200 mm',  'mm', 'Top sail height'),
    ('topsail_thickness', '1 mm',    'mm', 'Topsail fabric thickness'),
    ('topsail_gap',       '20 mm',   'mm', 'Gap between yard centerline and topsail bottom'),
    ('pennant_length',    '150 mm',  'mm', 'Pennant length above topsail'),
    ('pennant_dia',       '3 mm',    'mm', 'Pennant rod diameter'),

    ('rigging_dia',       '2 mm',    'mm', 'Paracord rigging line diameter (visualisation)'),
    ('rigging_base_z',    '60 mm',   'mm', 'Z height where rigging anchors on mast above socket'),
    ('rigging_sag',       '180 mm',  'mm', 'Visual catenary sag at the midpoint of each rope'),
]


# ----------------------------------------------------------------------- helpers
def add_params(design):
    up = design.userParameters
    for name, expr, unit, comment in USER_PARAMS:
        if up.itemByName(name):
            continue
        up.add(name, adsk.core.ValueInput.createByString(expr), unit, comment)


def _draw_ring_profile(comp, sketch_name, OD_expr, WT_expr):
    P3 = adsk.core.Point3D.create
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = sketch_name
    circles = sk.sketchCurves.sketchCircles
    outer = circles.addByCenterRadius(P3(0, 0, 0), 2.0)
    inner = circles.addByCenterRadius(P3(0, 0, 0), 1.0)
    sk.geometricConstraints.addCoincident(outer.centerSketchPoint, sk.originPoint)
    sk.geometricConstraints.addCoincident(inner.centerSketchPoint, sk.originPoint)
    sk.sketchDimensions.addDiameterDimension(
        outer, P3(3, 3, 0), True).parameter.expression = OD_expr
    sk.sketchDimensions.addDiameterDimension(
        inner, P3(1.5, 1.5, 0), True).parameter.expression = \
        '({}) - 2 * ({})'.format(OD_expr, WT_expr)
    for p in sk.profiles:
        if p.profileLoops.count == 2:
            return p
    raise RuntimeError('Ring profile not found in ' + sketch_name)


def _extrude_offset(comp, profile, start_expr, distance_expr, body_name):
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(profile, FeatOp.NewBodyFeatureOperation)
    inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI(start_expr))
    inp.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI(distance_expr)),
        adsk.fusion.ExtentDirections.PositiveExtentDirection)
    f = ext.add(inp)
    if f.bodies.count > 0:
        f.bodies.item(0).name = body_name
    return f


# ----------------------------------------------------------------------- builders
def build_mast(root):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'Mast'
    p1 = _draw_ring_profile(comp, 'seg1_section', 'seg1_OD', 'seg1_WT')
    _extrude_offset(comp, p1, '0 mm', 'seg_length', 'Mast_Seg1')
    p2 = _draw_ring_profile(comp, 'seg2_section', 'seg2_OD', 'seg2_WT')
    _extrude_offset(comp, p2, 'seg_length - seg_overlap', 'seg_length', 'Mast_Seg2')
    p3 = _draw_ring_profile(comp, 'seg3_section', 'seg3_OD', 'seg3_WT')
    _extrude_offset(comp, p3, '2 * (seg_length - seg_overlap)', 'seg_length', 'Mast_Seg3')


def build_socket(root):
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations
    ExtDir = adsk.fusion.ExtentDirections

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'Socket'
    ext = comp.features.extrudeFeatures

    def make_circle(name, diameter_expr):
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = name
        c = sk.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 3.0)
        sk.geometricConstraints.addCoincident(c.centerSketchPoint, sk.originPoint)
        sk.sketchDimensions.addDiameterDimension(
            c, P3(4, 4, 0), True).parameter.expression = diameter_expr
        return sk.profiles.item(0)

    # Outer cylinder (downward, full length)
    p_outer = make_circle('socket_outer_section', 'socket_inner_dia + 2 * socket_wall')
    inp = ext.createInput(p_outer, FeatOp.NewBodyFeatureOperation)
    inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('0 mm'))
    inp.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI('socket_length + socket_mast_collar')),
        ExtDir.NegativeExtentDirection)
    f_outer = ext.add(inp)
    socket_body = f_outer.bodies.item(0)
    socket_body.name = 'Socket_Body'

    # Bollard cavity (lower bore)
    p_b = make_circle('bollard_bore_section', 'socket_inner_dia')
    inp_b = ext.createInput(p_b, FeatOp.CutFeatureOperation)
    inp_b.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('0 mm - socket_mast_collar'))
    inp_b.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI('socket_length')),
        ExtDir.NegativeExtentDirection)
    inp_b.participantBodies = [socket_body]
    ext.add(inp_b)

    # Mast collar bore (upper bore)
    p_m = make_circle('mast_collar_bore_section', 'seg1_OD + 0.5 mm')
    inp_m = ext.createInput(p_m, FeatOp.CutFeatureOperation)
    inp_m.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('0 mm'))
    inp_m.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI('socket_mast_collar')),
        ExtDir.NegativeExtentDirection)
    inp_m.participantBodies = [socket_body]
    ext.add(inp_m)


def _build_canopy_structure(root, comp_name, hub_OD_expr, hub_H_expr, hub_z_expr,
                            spar_count_expr, spar_length_expr, spar_angle_expr,
                            spar_dia_expr, hub_body_name, spar_body_name,
                            init_hub_R_cm, init_hub_z_cm, init_dr_cm, init_dz_cm,
                            init_spar_dia_cm):
    """Build a single canopy (hub + N spars).

    init_*_cm are seed numerical positions used to draw the initial sketch
    geometry that the parametric dimensions then override.  The seeds must be
    on the negative side of sketch local Y because Fusion's XZ-plane sketch
    maps local +Y to world -Z; with the seed on -Y, the absolute distance
    dimensions keep the geometry on the world +Z side.
    """
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations
    ExtDir = adsk.fusion.ExtentDirections
    DimOr = adsk.fusion.DimensionOrientations

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = comp_name

    # -- HUB (ring on XY)
    sk_hub = comp.sketches.add(comp.xYConstructionPlane)
    sk_hub.name = comp_name + '_hub_section'
    c = sk_hub.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 3.0)
    sk_hub.geometricConstraints.addCoincident(c.centerSketchPoint, sk_hub.originPoint)
    sk_hub.sketchDimensions.addDiameterDimension(
        c, P3(4, 4, 0), True).parameter.expression = hub_OD_expr
    prof_hub = sk_hub.profiles.item(0)

    ext = comp.features.extrudeFeatures
    inp_hub = ext.createInput(prof_hub, FeatOp.NewBodyFeatureOperation)
    inp_hub.startExtent = adsk.fusion.OffsetStartDefinition.create(
        VI('{} - {} / 2'.format(hub_z_expr, hub_H_expr)))
    inp_hub.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI(hub_H_expr)),
        ExtDir.PositiveExtentDirection)
    f_hub = ext.add(inp_hub)
    f_hub.bodies.item(0).name = hub_body_name

    # -- ONE SPAR on XZ plane, initial sketch-Y NEGATIVE
    sk_s = comp.sketches.add(comp.xZConstructionPlane)
    sk_s.name = comp_name + '_spar_path'
    start_pt = P3(init_hub_R_cm, -init_hub_z_cm, 0)
    end_pt   = P3(init_hub_R_cm + init_dr_cm, -(init_hub_z_cm + init_dz_cm), 0)
    line = sk_s.sketchCurves.sketchLines.addByTwoPoints(start_pt, end_pt)

    sk_s.sketchDimensions.addDistanceDimension(
        sk_s.originPoint, line.startSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(1, 2, 0)
    ).parameter.expression = '{} / 2'.format(hub_OD_expr)
    sk_s.sketchDimensions.addDistanceDimension(
        sk_s.originPoint, line.startSketchPoint,
        DimOr.VerticalDimensionOrientation, P3(-3, -30, 0)
    ).parameter.expression = hub_z_expr
    sk_s.sketchDimensions.addDistanceDimension(
        sk_s.originPoint, line.endSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(40, 3, 0)
    ).parameter.expression = '{} / 2 + ({}) * cos({})'.format(
        hub_OD_expr, spar_length_expr, spar_angle_expr)
    sk_s.sketchDimensions.addDistanceDimension(
        sk_s.originPoint, line.endSketchPoint,
        DimOr.VerticalDimensionOrientation, P3(120, -60, 0)
    ).parameter.expression = '{} + ({}) * sin({})'.format(
        hub_z_expr, spar_length_expr, spar_angle_expr)

    path = comp.features.createPath(line)
    planes = comp.constructionPlanes
    pi = planes.createInput()
    pi.setByDistanceOnPath(line, VI('0 mm'))
    perp_plane = planes.add(pi)

    sk_p = comp.sketches.add(perp_plane)
    sk_p.name = comp_name + '_spar_profile'
    c_p = sk_p.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), init_spar_dia_cm / 2)
    sk_p.geometricConstraints.addCoincident(c_p.centerSketchPoint, sk_p.originPoint)
    sk_p.sketchDimensions.addDiameterDimension(
        c_p, P3(0.6, 0.6, 0), True).parameter.expression = spar_dia_expr
    prof_spar = sk_p.profiles.item(0)

    sweeps = comp.features.sweepFeatures
    sw_inp = sweeps.createInput(prof_spar, path, FeatOp.NewBodyFeatureOperation)
    sw_feat = sweeps.add(sw_inp)
    spar_body = sw_feat.bodies.item(0)
    spar_body.name = spar_body_name

    # -- Circular pattern around Z axis
    patterns = comp.features.circularPatternFeatures
    coll = adsk.core.ObjectCollection.create()
    coll.add(spar_body)
    pat_inp = patterns.createInput(coll, comp.zConstructionAxis)
    pat_inp.quantity = VI(spar_count_expr)
    pat_inp.totalAngle = VI('360 deg')
    pat_inp.isSymmetric = False
    patterns.add(pat_inp)


def build_lower_canopy(root):
    _build_canopy_structure(
        root, 'LowerCanopy',
        'lower_hub_OD', 'lower_hub_H', 'lower_hub_z',
        'lower_spar_count', 'lower_spar_length', 'lower_spar_angle',
        'lower_spar_dia',
        'LowerHub', 'LowerSpar_1',
        init_hub_R_cm=2.2, init_hub_z_cm=60.0,
        init_dr_cm=73.7, init_dz_cm=51.6, init_spar_dia_cm=0.8)


def build_upper_canopy(root):
    _build_canopy_structure(
        root, 'UpperCanopy',
        'upper_hub_OD', 'upper_hub_H', 'upper_hub_z',
        'upper_spar_count', 'upper_spar_length', 'upper_spar_angle',
        'upper_spar_dia',
        'UpperHub', 'UpperSpar_1',
        init_hub_R_cm=1.75, init_hub_z_cm=150.0,
        init_dr_cm=38.97, init_dz_cm=22.5, init_spar_dia_cm=0.6)


def build_top_mast(root):
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations
    ExtDir = adsk.fusion.ExtentDirections
    DimOr = adsk.fusion.DimensionOrientations

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'TopMast'

    # YARD — horizontal rod along world X at z = yard_z
    sk_y = comp.sketches.add(comp.xZConstructionPlane)
    sk_y.name = 'yard_path'
    line_y = sk_y.sketchCurves.sketchLines.addByTwoPoints(
        P3(-17.0, -194.7, 0), P3(18.0, -195.3, 0))
    sk_y.geometricConstraints.addHorizontal(line_y)
    sk_y.sketchDimensions.addDistanceDimension(
        sk_y.originPoint, line_y.startSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(-10, 5, 0)
    ).parameter.expression = 'yard_length / 2'
    sk_y.sketchDimensions.addDistanceDimension(
        sk_y.originPoint, line_y.startSketchPoint,
        DimOr.VerticalDimensionOrientation, P3(-25, -100, 0)
    ).parameter.expression = 'yard_z'
    sk_y.sketchDimensions.addDistanceDimension(
        sk_y.originPoint, line_y.endSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(10, 5, 0)
    ).parameter.expression = 'yard_length / 2'

    path_y = comp.features.createPath(line_y)
    planes = comp.constructionPlanes
    pi = planes.createInput()
    pi.setByDistanceOnPath(line_y, VI('0 mm'))
    perp_y = planes.add(pi)
    sk_yp = comp.sketches.add(perp_y)
    sk_yp.name = 'yard_profile'
    c_yp = sk_yp.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 0.3)
    sk_yp.geometricConstraints.addCoincident(c_yp.centerSketchPoint, sk_yp.originPoint)
    sk_yp.sketchDimensions.addDiameterDimension(
        c_yp, P3(0.5, 0.5, 0), True).parameter.expression = 'yard_dia'
    prof_yp = sk_yp.profiles.item(0)

    sweeps = comp.features.sweepFeatures
    sw_inp = sweeps.createInput(prof_yp, path_y, FeatOp.NewBodyFeatureOperation)
    sw_feat = sweeps.add(sw_inp)
    sw_feat.bodies.item(0).name = 'Yard'

    # TOPSAIL — rectangle on XZ plane, extruded thin in Y
    sk_t = comp.sketches.add(comp.xZConstructionPlane)
    sk_t.name = 'topsail_outline'
    rect_lines = sk_t.sketchCurves.sketchLines.addTwoPointRectangle(
        P3(-15.2, -197.1, 0), P3(14.8, -217.4, 0))
    pts = {}
    for ln in rect_lines:
        for sp in (ln.startSketchPoint, ln.endSketchPoint):
            key = (round(sp.geometry.x, 4), round(sp.geometry.y, 4))
            pts[key] = sp
    bl_sp = pts[min(pts, key=lambda k: (k[0], -k[1]))]
    tr_sp = pts[max(pts, key=lambda k: (k[0], -k[1]))]

    sk_t.sketchDimensions.addDistanceDimension(
        sk_t.originPoint, bl_sp,
        DimOr.HorizontalDimensionOrientation, P3(-8, 5, 0)
    ).parameter.expression = 'topsail_width / 2'
    sk_t.sketchDimensions.addDistanceDimension(
        sk_t.originPoint, bl_sp,
        DimOr.VerticalDimensionOrientation, P3(-20, -100, 0)
    ).parameter.expression = 'yard_z + topsail_gap'
    sk_t.sketchDimensions.addDistanceDimension(
        sk_t.originPoint, tr_sp,
        DimOr.HorizontalDimensionOrientation, P3(8, 5, 0)
    ).parameter.expression = 'topsail_width / 2'
    sk_t.sketchDimensions.addDistanceDimension(
        sk_t.originPoint, tr_sp,
        DimOr.VerticalDimensionOrientation, P3(20, -100, 0)
    ).parameter.expression = 'yard_z + topsail_gap + topsail_height'

    rect_prof = sk_t.profiles.item(0)
    ext = comp.features.extrudeFeatures
    inp_t = ext.createInput(rect_prof, FeatOp.NewBodyFeatureOperation)
    inp_t.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('0 mm - topsail_thickness / 2'))
    inp_t.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI('topsail_thickness')),
        ExtDir.PositiveExtentDirection)
    f_t = ext.add(inp_t)
    f_t.bodies.item(0).name = 'Topsail'

    # PENNANT — short vertical rod at top center
    sk_p = comp.sketches.add(comp.xYConstructionPlane)
    sk_p.name = 'pennant_section'
    c_p = sk_p.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 0.15)
    sk_p.geometricConstraints.addCoincident(c_p.centerSketchPoint, sk_p.originPoint)
    sk_p.sketchDimensions.addDiameterDimension(
        c_p, P3(0.3, 0.3, 0), True).parameter.expression = 'pennant_dia'
    prof_p = sk_p.profiles.item(0)
    inp_p = ext.createInput(prof_p, FeatOp.NewBodyFeatureOperation)
    inp_p.startExtent = adsk.fusion.OffsetStartDefinition.create(
        VI('yard_z + topsail_gap + topsail_height'))
    inp_p.setOneSideExtent(
        adsk.fusion.DistanceExtentDefinition.create(VI('pennant_length')),
        ExtDir.PositiveExtentDirection)
    f_p = ext.add(inp_p)
    f_p.bodies.item(0).name = 'Pennant'


def build_fabrics(root):
    """Two loft surfaces (apex point -> 4-corner diamond) for the canopies.

    The Z elevations are parametric, but the polygon corner X/Y positions are
    fixed numerical seeds. To regenerate after changing lower_spar_length/angle,
    delete the Fabrics component and re-run this builder.
    """
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'Fabrics'

    def make_canopy(apex_z_expr, R_tip_cm, Z_tip_expr, name_prefix):
        planes = comp.constructionPlanes

        pi_top = planes.createInput()
        pi_top.setByOffset(comp.xYConstructionPlane, VI(Z_tip_expr))
        plane_top = planes.add(pi_top)

        sk_top = comp.sketches.add(plane_top)
        sk_top.name = name_prefix + '_outer_poly'
        pts = [P3(R_tip_cm, 0, 0), P3(0, R_tip_cm, 0),
               P3(-R_tip_cm, 0, 0), P3(0, -R_tip_cm, 0)]
        for i in range(4):
            sk_top.sketchCurves.sketchLines.addByTwoPoints(pts[i], pts[(i + 1) % 4])
        outer_prof = sk_top.profiles.item(0)

        pi_apex = planes.createInput()
        pi_apex.setByOffset(comp.xYConstructionPlane, VI(apex_z_expr))
        plane_apex = planes.add(pi_apex)
        sk_apex = comp.sketches.add(plane_apex)
        sk_apex.name = name_prefix + '_apex'
        apex_pt = sk_apex.sketchPoints.add(P3(0, 0, 0))

        lofts = comp.features.loftFeatures
        loft_inp = lofts.createInput(FeatOp.NewBodyFeatureOperation)
        loft_inp.isSolid = False
        loft_inp.loftSections.add(apex_pt)
        loft_inp.loftSections.add(outer_prof)
        f = lofts.add(loft_inp)
        for b in f.bodies:
            b.name = name_prefix + '_fabric'

    make_canopy('lower_hub_z',
                75.93,
                'lower_hub_z + lower_spar_length * sin(lower_spar_angle)',
                'lower_canopy')
    make_canopy('upper_hub_z',
                40.72,
                'upper_hub_z + upper_spar_length * sin(upper_spar_angle)',
                'upper_canopy')

    # === Top membrane: planar diamond patch connecting the 4 lower spar tips
    # at z = Z_tip (the z-max points where the rigging ropes terminate).
    Z_tip_expr = 'lower_hub_z + lower_spar_length * sin(lower_spar_angle)'
    pi_top = comp.constructionPlanes.createInput()
    pi_top.setByOffset(comp.xYConstructionPlane, VI(Z_tip_expr))
    plane_top = comp.constructionPlanes.add(pi_top)
    sk_top = comp.sketches.add(plane_top)
    sk_top.name = 'top_membrane_outline'
    R_tip = 75.93  # numerical seed in cm (matches lower spar tip reach)
    diamond = [P3(R_tip, 0, 0), P3(0, R_tip, 0),
               P3(-R_tip, 0, 0), P3(0, -R_tip, 0)]
    for i in range(4):
        sk_top.sketchCurves.sketchLines.addByTwoPoints(
            diamond[i], diamond[(i + 1) % 4])

    boundary = adsk.core.ObjectCollection.create()
    for sc in sk_top.sketchCurves.sketchLines:
        boundary.add(sc)
    patches = comp.features.patchFeatures
    patch_inp = patches.createInput(boundary, FeatOp.NewBodyFeatureOperation)
    patch_inp.isSolid = False
    patch_feat = patches.add(patch_inp)
    for b in patch_feat.bodies:
        b.name = 'top_membrane'

    plane_top.isLightBulbOn = False
    sk_top.isLightBulbOn = False


def build_rigging(root):
    """Four paracord rigging lines, each from a lower-canopy spar tip down to
    the mast base. Modelled as thin swept pipes. Uses the same XZ-plane /
    negative-Y trick as the spar sweep so that the path lands on world +Z.
    """
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations
    DimOr = adsk.fusion.DimensionOrientations

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = 'Rigging'

    sk = comp.sketches.add(comp.xZConstructionPlane)
    sk.name = 'lower_rigging_path'
    # Seeds (cm): start anchor on mast at base, end at lower spar tip,
    # midpoint sagged downward in world Z (= upward in sketch local Y)
    start_pt = P3(1.6, -6.0, 0)
    end_pt   = P3(75.93, -111.62, 0)
    # mid world Z = average minus sag (= 8 cm seed). True sag is driven by
    # the rigging_sag parameter at run time via the spline being free in the
    # middle, so this is just a seed shape.
    mid_world_z = (6.0 + 111.62) / 2 - 8.0
    mid_pt = P3((1.6 + 75.93) / 2, -mid_world_z, 0)
    pts = adsk.core.ObjectCollection.create()
    pts.add(start_pt); pts.add(mid_pt); pts.add(end_pt)
    spline = sk.sketchCurves.sketchFittedSplines.add(pts)

    sk.sketchDimensions.addDistanceDimension(
        sk.originPoint, spline.startSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(0.5, 2, 0)
    ).parameter.expression = 'seg1_OD / 2'
    sk.sketchDimensions.addDistanceDimension(
        sk.originPoint, spline.startSketchPoint,
        DimOr.VerticalDimensionOrientation, P3(-3, -3, 0)
    ).parameter.expression = 'rigging_base_z'
    sk.sketchDimensions.addDistanceDimension(
        sk.originPoint, spline.endSketchPoint,
        DimOr.HorizontalDimensionOrientation, P3(40, 3, 0)
    ).parameter.expression = 'lower_hub_OD / 2 + lower_spar_length * cos(lower_spar_angle)'
    sk.sketchDimensions.addDistanceDimension(
        sk.originPoint, spline.endSketchPoint,
        DimOr.VerticalDimensionOrientation, P3(120, -60, 0)
    ).parameter.expression = 'lower_hub_z + lower_spar_length * sin(lower_spar_angle)'

    path = comp.features.createPath(spline)
    planes = comp.constructionPlanes
    pi = planes.createInput()
    pi.setByDistanceOnPath(spline, VI('0 mm'))
    perp = planes.add(pi)

    sk_prof = comp.sketches.add(perp)
    sk_prof.name = 'rigging_profile'
    c = sk_prof.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 0.1)
    sk_prof.geometricConstraints.addCoincident(c.centerSketchPoint, sk_prof.originPoint)
    sk_prof.sketchDimensions.addDiameterDimension(
        c, P3(0.2, 0.2, 0), True).parameter.expression = 'rigging_dia'
    prof = sk_prof.profiles.item(0)

    sweeps = comp.features.sweepFeatures
    sw_inp = sweeps.createInput(prof, path, FeatOp.NewBodyFeatureOperation)
    sw_feat = sweeps.add(sw_inp)
    line_body = sw_feat.bodies.item(0)
    line_body.name = 'LowerRig_1'

    patterns = comp.features.circularPatternFeatures
    coll = adsk.core.ObjectCollection.create()
    coll.add(line_body)
    pat_inp = patterns.createInput(coll, comp.zConstructionAxis)
    pat_inp.quantity = VI('lower_spar_count')
    pat_inp.totalAngle = VI('360 deg')
    pat_inp.isSymmetric = False
    patterns.add(pat_inp)


def build_storage(root):
    """Horizontal perimeter ropes between the spar tips at each canopy level.
    These 4 + 4 ropes form diamond frames at z = Z_tip_lower and Z_tip_upper —
    the 'storage' diamond shown in the concept sketches: a net you can drop
    gear into, or the base of a future folded-state storage volume.
    """
    P3 = adsk.core.Point3D.create
    VI = adsk.core.ValueInput.createByString
    FeatOp = adsk.fusion.FeatureOperations

    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    storage = occ.component
    storage.name = 'Storage'

    def perim_rope(z_offset_expr, R_tip_cm, body_prefix, pattern_qty_expr):
        planes = storage.constructionPlanes
        pi = planes.createInput()
        pi.setByOffset(storage.xYConstructionPlane, VI(z_offset_expr))
        plane_tip = planes.add(pi)

        sk = storage.sketches.add(plane_tip)
        sk.name = body_prefix + '_path'
        line = sk.sketchCurves.sketchLines.addByTwoPoints(
            P3(R_tip_cm, 0, 0), P3(0, R_tip_cm, 0))
        path = storage.features.createPath(line)

        pi2 = planes.createInput()
        pi2.setByDistanceOnPath(line, VI('0 mm'))
        perp = planes.add(pi2)

        sk_prof = storage.sketches.add(perp)
        sk_prof.name = body_prefix + '_profile'
        c = sk_prof.sketchCurves.sketchCircles.addByCenterRadius(P3(0, 0, 0), 0.1)
        sk_prof.geometricConstraints.addCoincident(
            c.centerSketchPoint, sk_prof.originPoint)
        sk_prof.sketchDimensions.addDiameterDimension(
            c, P3(0.2, 0.2, 0), True).parameter.expression = 'rigging_dia'
        prof = sk_prof.profiles.item(0)

        sweeps = storage.features.sweepFeatures
        sw_inp = sweeps.createInput(prof, path, FeatOp.NewBodyFeatureOperation)
        sw_feat = sweeps.add(sw_inp)
        body = sw_feat.bodies.item(0)
        body.name = body_prefix + '_1'

        patterns = storage.features.circularPatternFeatures
        coll = adsk.core.ObjectCollection.create()
        coll.add(body)
        pat_inp = patterns.createInput(coll, storage.zConstructionAxis)
        pat_inp.quantity = VI(pattern_qty_expr)
        pat_inp.totalAngle = VI('360 deg')
        pat_inp.isSymmetric = False
        patterns.add(pat_inp)

    perim_rope(
        'lower_hub_z + lower_spar_length * sin(lower_spar_angle)',
        75.93, 'LowerHorizRope', 'lower_spar_count')
    perim_rope(
        'upper_hub_z + upper_spar_length * sin(upper_spar_angle)',
        40.72, 'UpperHorizRope', 'upper_spar_count')

    for pl in storage.constructionPlanes:
        try:
            pl.isLightBulbOn = False
        except Exception:
            pass
    for sk_ in storage.sketches:
        try:
            sk_.isLightBulbOn = False
        except Exception:
            pass


# ----------------------------------------------------------------------- entry
def run(_context):
    app = adsk.core.Application.get()
    if app.activeProduct is None or not isinstance(app.activeProduct, adsk.fusion.Design):
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        raise RuntimeError('No active Fusion design')

    add_params(design)
    root = design.rootComponent

    build_mast(root)
    build_socket(root)
    build_lower_canopy(root)
    build_upper_canopy(root)
    build_top_mast(root)
    build_fabrics(root)
    build_rigging(root)
    build_storage(root)

    print('Plug-in Parasite built successfully.')
