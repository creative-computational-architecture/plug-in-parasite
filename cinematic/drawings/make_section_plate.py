#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plug-in Parasite — presentation section plate (A2 landscape, 1:10).
Proportions taken verbatim from the GH model (NOT corrected).
On-drawing annotation = keyed letters A..K only; descriptions live in LEGEND.
English. Detailed material hatches. Cast concrete footing added as a
plausible construction detail (does not alter structure proportions).
Map (1:10): px = CX + x_cm ;  py = GY - z_cm     (1 cm real = 1 mm paper)
"""
import math

CX, GY = 185.0, 335.0
def px(xcm): return CX + xcm
def py(zcm): return GY - zcm

S = []
def add(s): S.append(s)

# ---------------- header / defs ----------------
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" '
    'viewBox="0 0 594 420" font-family="Helvetica, Arial, sans-serif">')
add('<defs>')
# steel: fine 45 deg hatch
add('<pattern id="steel" patternUnits="userSpaceOnUse" width="0.9" height="0.9" '
    'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="0.9" '
    'stroke="#1a1a1a" stroke-width="0.07"/></pattern>')
# steel node (cross hatch) for hub
add('<pattern id="steelx" patternUnits="userSpaceOnUse" width="0.9" height="0.9" '
    'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="0.9" stroke="#1a1a1a" stroke-width="0.08"/>'
    '<line x1="0" y1="0" x2="0.9" y2="0" stroke="#1a1a1a" stroke-width="0.08"/></pattern>')
# concrete: diagonal lines + aggregate dots
add('<pattern id="concrete" patternUnits="userSpaceOnUse" width="3.2" height="3.2" patternTransform="rotate(45)">'
    '<line x1="0" y1="0" x2="0" y2="3.2" stroke="#333" stroke-width="0.12"/>'
    '<circle cx="1.6" cy="1.0" r="0.18" fill="#555"/><circle cx="0.6" cy="2.4" r="0.13" fill="#555"/></pattern>')
# earth
add('<pattern id="earth" patternUnits="userSpaceOnUse" width="4.5" height="4.5" patternTransform="rotate(45)">'
    '<line x1="0" y1="0" x2="0" y2="4.5" stroke="#555" stroke-width="0.1"/></pattern>')
# fabric membrane (fine vertical)
add('<pattern id="fabric" patternUnits="userSpaceOnUse" width="0.7" height="0.7">'
    '<line x1="0" y1="0" x2="0" y2="0.7" stroke="#444" stroke-width="0.05"/></pattern>')
add('<marker id="arr" markerWidth="7" markerHeight="6" refX="6" refY="2" orient="auto" markerUnits="userSpaceOnUse">'
    '<path d="M0,0 L6,2 L0,4 Z" fill="#000"/></marker>')
add('<marker id="kdot" markerWidth="2.4" markerHeight="2.4" refX="1.2" refY="1.2" orient="auto" markerUnits="userSpaceOnUse">'
    '<circle cx="1.2" cy="1.2" r="0.7" fill="#000"/></marker>')
add('</defs>')

# sheet border + inner frame
add('<rect x="6" y="6" width="582" height="408" fill="#fff" stroke="#000" stroke-width="0.4"/>')
add('<rect x="10" y="10" width="574" height="400" fill="none" stroke="#000" stroke-width="0.8"/>')

# ================= SECTION =================
def rect(x,y,w,h,fill,stroke="#000",sw=0.6):
    add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,sw,color="#000",dash=None,cap="butt"):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{sw}"{d} stroke-linecap="{cap}"/>')
def path(d,fill,stroke,sw):
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

# --- ground + earth ---
add(f'<rect x="40" y="{py(0):.2f}" width="290" height="45" fill="url(#earth)"/>')
# carve footing void out of earth
add(f'<rect x="{px(-25):.2f}" y="{py(0):.2f}" width="50" height="40" fill="#fff"/>')
line(40, py(0), 330, py(0), 0.8)  # ground line (heavy)

# --- concrete footing (K) ---
rect(px(-25), py(0), 50, 40, "url(#concrete)", "#000", 0.5)
# steel base flange at z0
rect(px(-12), py(0)-0.0, 24, 2, "url(#steelx)", "#000", 0.4)

# --- CUT steel members ---
rect(px(-4.5), py(0), 9, 15, "url(#steel)", "#000", 0.55)            # J socket (in footing)
rect(px(-5), py(50), 10, 50, "url(#steel)", "#000", 0.6)             # D seg1
rect(px(-2), py(135), 4, 85, "url(#steel)", "#000", 0.55)            # C seg2 visible
rect(px(-1), py(220), 2, 85, "url(#steel)", "#000", 0.5)             # B seg3 visible
rect(px(-4), py(21.5), 8, 3, "url(#steelx)", "#000", 0.5)            # I hub

# hidden telescoped overlaps (dashed)
for (xx,za,zb) in [(-2,42,50),(2,42,50)]:
    line(px(xx),py(za),px(xx),py(zb),0.18,"#000","1.0,0.7")
line(px(-2),py(42),px(2),py(42),0.18,"#000","1.0,0.7")
for (xx,za,zb) in [(-1,127,135),(1,127,135)]:
    line(px(xx),py(za),px(xx),py(zb),0.18,"#000","1.0,0.7")
line(px(-1),py(127),px(1),py(127),0.18,"#000","1.0,0.7")

# centreline
line(px(0),py(-18),px(0),py(232),0.12,"#000","4,1.2,0.7,1.2")

# --- spars (G) as Ø14.3 pipe = double line ---
def pipe(x1,y1,x2,y2,r):
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; nx,ny=-uy*r,ux*r
    line(x1+nx,y1+ny,x2+nx,y2+ny,0.35); line(x1-nx,y1-ny,x2-nx,y2-ny,0.35)
    line(x2+nx,y2+ny,x2-nx,y2-ny,0.35)
pipe(px(4),py(20), px(76.35),py(73.5), 0.715)
pipe(px(-4),py(20), px(-76.35),py(73.5), 0.715)

# --- hammock membrane (H) : filled band with fabric hatch + profile ---
hL=(px(-76.35),py(73.5)); hR=(px(76.35),py(73.5)); hC=(px(0),py(63.6))
ctrl=(px(0), 2*hC[1]-hL[1])
path(f'M{hL[0]:.2f},{hL[1]:.2f} Q{ctrl[0]:.2f},{ctrl[1]:.2f} {hR[0]:.2f},{hR[1]:.2f} '
     f'L{hR[0]:.2f},{hR[1]-1.4:.2f} Q{ctrl[0]:.2f},{ctrl[1]-1.4:.2f} {hL[0]:.2f},{hL[1]-1.4:.2f} Z',
     "url(#fabric)","#000",0.35)

# --- canopy panel (F) ---
pL=(px(-27),py(177.7)); pR=(px(27),py(177.7)); pC=(px(0),py(174.46))
pctrl=(px(0),2*pC[1]-pL[1])
path(f'M{pL[0]:.2f},{pL[1]:.2f} Q{pctrl[0]:.2f},{pctrl[1]:.2f} {pR[0]:.2f},{pR[1]:.2f} '
     f'L{pR[0]:.2f},{pR[1]-1.2:.2f} Q{pctrl[0]:.2f},{pctrl[1]-1.2:.2f} {pL[0]:.2f},{pL[1]-1.2:.2f} Z',
     "url(#fabric)","#000",0.35)

# --- hook (A) ---
line(px(0),py(220),px(0),py(228),0.5)
add(f'<path d="M{px(0):.2f},{py(228):.2f} A5,5 0 0 1 {px(10):.2f},{py(228):.2f}" fill="none" stroke="#000" stroke-width="0.5"/>')
add(f'<path d="M{px(0):.2f},{py(228):.2f} A5,5 0 0 0 {px(-10):.2f},{py(228):.2f}" fill="none" stroke="#000" stroke-width="0.5"/>')

# --- rigging cables (E) ---
spire=(px(0),py(223))
for tgt in [(px(27),py(177.7)),(px(-27),py(177.7)),(px(76.35),py(73.5)),(px(-76.35),py(73.5))]:
    line(spire[0],spire[1],tgt[0],tgt[1],0.25,"#000")

# ================= DIMENSIONS (mm) =================
DGREY="#000"
# vertical chain on right at x=300
levels=[233,220,177.7,73.5,50,0,-15]
objx={233:px(10),220:px(1),177.7:px(27),73.5:px(76.35),50:px(5),0:px(5),-15:px(4.5)}
dx=300
line(dx,py(233),dx,py(-15),0.13)
for z in levels:
    line(objx[z],py(z),dx,py(z),0.1)
    line(dx-1.4,py(z)+1.4,dx+1.4,py(z)-1.4,0.3)
chain=[(233,220,"130"),(220,177.7,"423"),(177.7,73.5,"1042"),(73.5,50,"235"),(50,0,"500"),(0,-15,"150")]
for a,b,v in chain:
    yy=(py(a)+py(b))/2.0
    add(f'<text x="{dx+4.5:.2f}" y="{yy:.2f}" font-size="3" text-anchor="middle" '
        f'transform="rotate(-90 {dx+4.5:.2f} {yy:.2f})">{v}</text>')
# level marks (datums) — kept (numeric, not descriptive)
lvl={233:"+2.330",220:"+2.200",177.7:"+1.777",73.5:"+0.735",50:"+0.500",0:"&#177;0.000 FFL",-15:"&#8722;0.150"}
for z in levels:
    yy=py(z)
    add(f'<text x="282" y="{yy-1.2:.2f}" font-size="3" text-anchor="end">{lvl[z]}</text>')
    add(f'<path d="M281,{yy:.2f} l2.4,-1.4 l0,2.8 Z" fill="#000"/>')  # datum triangle
# horizontal dims (broken at mast)
def hdim(z,xa,xb,yoff,val,gap):
    yy=py(z)-yoff
    line(px(xa),py(z),px(xa),yy-2,0.1); line(px(xb),py(z),px(xb),yy-2,0.1)
    line(px(xa),yy,px(0)-gap,yy,0.13); line(px(0)+gap,yy,px(xb),yy,0.13)
    add(f'<path d="M{px(xa):.2f},{yy:.2f} l6,-1.4 l0,2.8 Z" fill="#000"/>')
    add(f'<path d="M{px(xb):.2f},{yy:.2f} l-6,-1.4 l0,2.8 Z" fill="#000"/>')
    add(f'<text x="{px(0):.2f}" y="{yy+1.1:.2f}" font-size="3" text-anchor="middle" '
        f'fill="#000" paint-order="stroke" stroke="#fff" stroke-width="1.1">{val}</text>')
hdim(73.5,-76.35,76.35,18,"1527",16)
hdim(177.7,-27,27,12,"540",11)

# ================= KEY BUBBLES (A..K) =================
def bubble(letter, bx, by, tx, ty):
    line(bx,by,tx,ty,0.13,"#000")
    add(f'<circle cx="{tx:.2f}" cy="{ty:.2f}" r="0.7" fill="#000"/>')
    add(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="3" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    add(f'<text x="{bx:.2f}" y="{by+1.05:.2f}" font-size="3.3" font-weight="bold" text-anchor="middle">{letter}</text>')
keys=[
 ("A",238, 98, px(7),  py(229)),
 ("B",243,135, px(1),  py(180)),
 ("F",250,160, px(27), py(177.7)),
 ("E",112,150, 150.6,179.3),
 ("C",132,225, px(-2), py(100)),
 ("G",258,250, (px(4)+px(76.35))/2, (py(20)+py(73.5))/2),
 ("H",250,283, px(20), py(70)),
 ("D",146,300, px(-5), py(30)),
 ("I",140,318, px(-4), py(20)),
 ("J",140,345, px(-4.5),py(-7)),
 ("K",240,368, px(20), py(-25)),
]
for k in keys: bubble(*k)

# section tag
add('<text x="40" y="30" font-size="6" font-weight="bold">A</text>')
add('<text x="325" y="100" font-size="6" font-weight="bold">A</text>')

# ================= RIGHT COLUMN: LEGEND =================
LX=348
add(f'<line x1="{LX-6}" y1="42" x2="578" y2="42" stroke="#000" stroke-width="0.4"/>')
add(f'<text x="{LX-6}" y="38" font-size="5" font-weight="bold" letter-spacing="0.8">LEGEND  —  COMPONENTS</text>')
legend=[
 ("A","Stainless-steel four-prong suspension hook"),
 ("B","Telescopic mast &#8212; upper section, &#216;20"),
 ("C","Telescopic mast &#8212; intermediate section, &#216;40"),
 ("D","Telescopic mast &#8212; base section, &#216;100"),
 ("E","Pre-tensioned rigging cable, &#216;2.2"),
 ("F","Upper canopy panel, 540 &#215; 500"),
 ("G","Radial spreader spar, &#216;14.3  (&#215;4)"),
 ("H","PE woven hammock membrane"),
 ("I","Central distribution hub, &#216;80"),
 ("J","Driven ground socket, &#216;90"),
 ("K","Cast-in-situ concrete footing"),
]
yy=54
for k,desc in legend:
    add(f'<circle cx="{LX:.2f}" cy="{yy-1:.2f}" r="3" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    add(f'<text x="{LX:.2f}" y="{yy+0.05:.2f}" font-size="3.3" font-weight="bold" text-anchor="middle">{k}</text>')
    add(f'<text x="{LX+7:.2f}" y="{yy+0.3:.2f}" font-size="3.4">{desc}</text>')
    yy+=11.5

# materials sub-legend (hatch keys)
add(f'<text x="{LX-6}" y="{yy+4}" font-size="4.2" font-weight="bold" letter-spacing="0.6">MATERIALS</text>')
yy+=10
mats=[("steel","Structural steel (section)"),("concrete","Cast concrete"),
      ("earth","Compacted earth"),("fabric","Tensioned PE membrane")]
for pat,desc in mats:
    add(f'<rect x="{LX-2:.2f}" y="{yy-3:.2f}" width="8" height="5" fill="url(#{pat})" stroke="#000" stroke-width="0.3"/>')
    add(f'<text x="{LX+9:.2f}" y="{yy+0.6:.2f}" font-size="3.2">{desc}</text>')
    yy+=8

# ================= DEPLOYMENT SEQUENCE =================
seqY=300
add(f'<line x1="{LX-6}" y1="{seqY-12}" x2="578" y2="{seqY-12}" stroke="#000" stroke-width="0.4"/>')
add(f'<text x="{LX-6}" y="{seqY-15}" font-size="4.2" font-weight="bold" letter-spacing="0.6">DEPLOYMENT SEQUENCE</text>')
def silhouette(cx, mode, label):
    g="#cfcfcf"; st="#333"
    base=seqY+30
    def lx(x): return cx + x*0.2
    def ly(z): return base - z*0.2
    if mode==0:  # stowed
        add(f'<rect x="{lx(-5):.2f}" y="{ly(50):.2f}" width="{10*0.2:.2f}" height="{50*0.2:.2f}" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
        add(f'<path d="M{lx(0):.2f},{ly(52):.2f} q{3*0.2:.2f},{-6*0.2:.2f} {6*0.2:.2f},0" fill="none" stroke="{st}" stroke-width="0.25"/>')
    elif mode==1:  # telescoping
        add(f'<rect x="{lx(-5):.2f}" y="{ly(50):.2f}" width="{10*0.2:.2f}" height="{50*0.2:.2f}" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
        add(f'<rect x="{lx(-2):.2f}" y="{ly(135):.2f}" width="{4*0.2:.2f}" height="{85*0.2:.2f}" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
        add(f'<rect x="{lx(-1):.2f}" y="{ly(220):.2f}" width="{2*0.2:.2f}" height="{85*0.2:.2f}" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
    else:  # deployed
        add(f'<path d="M{lx(0):.2f},{ly(220):.2f} L{lx(76):.2f},{ly(73):.2f} L{lx(0):.2f},{ly(50):.2f} L{lx(-76):.2f},{ly(73):.2f} Z" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
        add(f'<path d="M{lx(0):.2f},{ly(220):.2f} L{lx(27):.2f},{ly(177):.2f} L{lx(-27):.2f},{ly(177):.2f} Z" fill="#bdbdbd" stroke="{st}" stroke-width="0.25"/>')
        add(f'<rect x="{lx(-1):.2f}" y="{ly(220):.2f}" width="{2*0.2:.2f}" height="{170*0.2:.2f}" fill="{g}" stroke="{st}" stroke-width="0.25"/>')
    add(f'<text x="{cx:.2f}" y="{base+5:.2f}" font-size="3" text-anchor="middle">{label}</text>')
silhouette(392,0,"1  STOWED")
silhouette(462,1,"2  DEPLOYING")
silhouette(532,2,"3  DEPLOYED")

# ================= TITLE BLOCK =================
add('<g transform="translate(348,356)">')
add('<rect x="0" y="0" width="230" height="48" fill="none" stroke="#000" stroke-width="0.6"/>')
add('<line x1="0" y1="14" x2="230" y2="14" stroke="#000" stroke-width="0.3"/>')
add('<line x1="0" y1="26" x2="230" y2="26" stroke="#000" stroke-width="0.3"/>')
add('<line x1="0" y1="37" x2="230" y2="37" stroke="#000" stroke-width="0.3"/>')
add('<line x1="150" y1="26" x2="150" y2="48" stroke="#000" stroke-width="0.3"/>')
add('<text x="4" y="10" font-size="6.5" font-weight="bold" letter-spacing="1">PLUG-IN PARASITE</text>')
add('<text x="4" y="21.5" font-size="3.6">Suspended micro-shelter &#8212; Section A&#8211;A (deployed)</text>')
add('<text x="4" y="33" font-size="3.4">caglarcelik architects</text>')
add('<text x="4" y="44" font-size="3.4">General arrangement &#183; structural section</text>')
add('<text x="154" y="33" font-size="3.4">Scale 1:10 (A2)</text>')
add('<text x="154" y="44" font-size="3.4">2026-06-01 &#183; Rev. C &#183; CCA</text>')
add('</g>')

# ================= SCALE BAR (1:10) =================
# 500 mm real = 50 mm paper; segments 100 mm = 10 mm
add('<g transform="translate(40,392)">')
for i in range(5):
    fill="#000" if i%2==0 else "#fff"
    add(f'<rect x="{i*10}" y="0" width="10" height="2" fill="{fill}" stroke="#000" stroke-width="0.2"/>')
for i,(v) in enumerate(["0","","200","","400","500"]):
    add(f'<text x="{i*10}" y="5.5" font-size="2.8" text-anchor="middle">{v}</text>')
add('<text x="0" y="-2" font-size="3.4" font-weight="bold">1:10</text>')
add('<text x="60" y="5.5" font-size="2.8">mm</text>')
add('</g>')

add('</svg>')

path_out=r"<repo>\cinematic\drawings\PlugInParasite_section_plate.svg"
with open(path_out,"w",encoding="utf-8") as f:
    f.write("\n".join(S))
print("SVG yazildi:", path_out, len("\n".join(S)), "bayt")
