#! python 3
# fold_phases — derives all phase fractions + telescope geometry constants
# from the master fold slider. Pure scalar math, no Rhino geometry.
# Phase chain: fold → telescope (0..0.5) → canopy (0.5..1)
#   canopy splits into rise (0.5..0.75) then open (0.75..1)
#   telescope splits into seg2 (0..0.25) then seg3 (0.25..0.5)

f = max(0.0, min(1.0, float(fold)))

# Mast cross-section + segment length constants
SEG1_R = 5.0
SEG1_L = 50.0
SEG_OVERLAP = 8.0

# Telescope/canopy phase fractions
f_telescope = max(0.0, min(1.0, f * 2.0))
f_canopy    = max(0.0, min(1.0, (f - 0.5) * 2.0))
f_rise      = max(0.0, min(1.0, f_canopy * 2.0))
f_open      = max(0.0, min(1.0, (f_canopy - 0.5) * 2.0))
f_seg2      = max(0.0, min(1.0, f_telescope * 2.0))
f_seg3      = max(0.0, min(1.0, (f_telescope - 0.5) * 2.0))

# Telescope section length (seg2 and seg3 share this length)
mast_open = float(mast_h)
SEG_L = max((mast_open - SEG1_L + 2.0 * SEG_OVERLAP) / 2.0, 30.0)

# HOOK_Z — the system's top. Drives seg3 and seg2 base/top positions
# in mast_geo. At fold=0: HOOK_Z=SEG1_L. At fold=0.5: HOOK_Z=mast top.
HOOK_Z_folded   = SEG1_L
HOOK_Z_deployed = SEG1_L + 2.0 * (SEG_L - SEG_OVERLAP)
HOOK_Z = HOOK_Z_folded + (HOOK_Z_deployed - HOOK_Z_folded) * f_telescope

# Human-readable phase label for QC panels
if f <= 0.01:   lbl = "CLOSED"
elif f < 0.5:   lbl = f"TELESCOPE {f_telescope:.0%}"
elif f < 0.99:  lbl = f"CANOPY {f_canopy:.0%}"
else:           lbl = "DEPLOYED"
phase_label = f"fold={f:.2f} [{lbl}] HOOK_Z={HOOK_Z:.0f}"
