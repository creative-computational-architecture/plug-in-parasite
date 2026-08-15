#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plug-in Parasite — BRANCH ATTACHMENT DETAIL (A2 landscape, ~1:5, NO dimensions).
Design = workflow synthesis "The Apologetic Grip" + adversarial arborist/rigger fixes.
On-drawing annotation = keyed letters A..J only; all prose in legend + note blocks.
Tree-friendly: wide round sling BASKET over a cambium saver (only soft thing on bark),
near-vertical legs, redundant backup sling to a 2nd limb, basket seated against a
collar (anti-creep), clean oversized forged metal chain below, anti-spin swivel.
"""
import math, random
random.seed(7)
S=[]; A=S.append
def pl(pts, sw, color="#000", fill="none", dash=None, cap="round"):
    d=" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)
    dd=f' stroke-dasharray="{dash}"' if dash else ""
    A(f'<polyline points="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{dd} stroke-linecap="{cap}" stroke-linejoin="round"/>')
def ln(x1,y1,x2,y2,sw,color="#000",dash=None):
    dd=f' stroke-dasharray="{dash}"' if dash else ""
    A(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{sw}"{dd} stroke-linecap="round"/>')
def circ(cx,cy,r,sw,color="#000",fill="none"):
    A(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{color}" stroke-width="{sw}"/>')
def pathd(d,fill,stroke,sw):
    A(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
def txt(x,y,s,size,anchor="start",weight="normal",color="#000",ls=0):
    l=f' letter-spacing="{ls}"' if ls else ""
    A(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}"{l}>{s}</text>')

def arcpts(cx,cy,r,a0,a1,n=40):
    return [(cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
            for a in [a0+(a1-a0)*i/n for i in range(n+1)]]

# ---- sheet ----
A('<?xml version="1.0" encoding="UTF-8"?>')
A('<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" '
  'viewBox="0 0 594 420" font-family="Helvetica, Arial, sans-serif">')
A('<defs>')
A('<pattern id="steel" patternUnits="userSpaceOnUse" width="0.8" height="0.8" patternTransform="rotate(45)">'
  '<line x1="0" y1="0" x2="0" y2="0.8" stroke="#1a1a1a" stroke-width="0.08"/></pattern>')
A('<pattern id="steelx" patternUnits="userSpaceOnUse" width="0.9" height="0.9" patternTransform="rotate(45)">'
  '<line x1="0" y1="0" x2="0" y2="0.9" stroke="#1a1a1a" stroke-width="0.09"/>'
  '<line x1="0" y1="0" x2="0.9" y2="0" stroke="#1a1a1a" stroke-width="0.09"/></pattern>')
A('<pattern id="rubber" patternUnits="userSpaceOnUse" width="1.5" height="1.5">'
  '<rect width="1.5" height="1.5" fill="#b9b9b9"/><circle cx="0.5" cy="0.5" r="0.22" fill="#6f6f6f"/>'
  '<circle cx="1.1" cy="1.15" r="0.16" fill="#7d7d7d"/></pattern>')
A('<marker id="ld" markerWidth="6" markerHeight="6" refX="3" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
  '<path d="M0,0 L3,5 L6,0" fill="none" stroke="#888" stroke-width="0.4"/></marker>')
A('</defs>')
A('<rect x="6" y="6" width="582" height="408" fill="#fff" stroke="#000" stroke-width="0.4"/>')
A('<rect x="10" y="10" width="574" height="400" fill="none" stroke="#000" stroke-width="0.8"/>')

# ================= DETAIL DRAWING =================
CX=200.0
# ---------- primary host limb (A) in cross-section ----------
by=98.0; rB=25.0
# bark (thick irregular double outline)
barkpts=[(CX+(rB+1.1+0.5*math.sin(a*0.7))*math.cos(math.radians(a)),
          by+(rB+1.1+0.5*math.sin(a*0.7))*math.sin(math.radians(a))) for a in range(0,361,4)]
A(f'<path d="M{barkpts[0][0]:.2f},{barkpts[0][1]:.2f} '+" ".join(f"L{x:.2f},{y:.2f}" for x,y in barkpts[1:])+' Z" '
  f'fill="#efe9df" stroke="#3a2f25" stroke-width="0.9"/>')
circ(CX,by,rB,0.5,"#5a4a38")                       # inner bark line
# cambium / phloem ring (living layer)
circ(CX,by,rB-1.4,0.35,"#7c8a5a")
# growth rings (end grain)
rr=rB-3.6
while rr>3:
    circ(CX+0.6,by-0.4,rr,0.18,"#9c8e76"); rr-=2.7
# radial rays
for a in range(0,360,30):
    ln(CX+0.6+3*math.cos(math.radians(a)), by-0.4+3*math.sin(math.radians(a)),
       CX+0.6+(rB-3)*math.cos(math.radians(a)), by-0.4+(rB-3)*math.sin(math.radians(a)), 0.1, "#b3a596")
circ(CX+0.6,by-0.4,0.7,0,"#000","#000")            # pith

# anti-creep branch collar/nub (J) on lower-left
nub=[(CX-rB*0.78, by+rB*0.55),(CX-rB-7, by+rB*0.30),(CX-rB-6, by+rB*0.95),(CX-rB*0.72, by+rB*0.92)]
pathd("M"+ " L".join(f"{x:.2f},{y:.2f}" for x,y in nub)+" Z","#efe9df","#3a2f25",0.6)

# ---------- cambium saver (B) : rubber band over crown, past shoulders ----------
# screen angles: 90=bottom, 270=top. shoulders ~135 / 45. saver 120..420 (over top)
sv_out=arcpts(CX,by,rB+3.2,120,420,60)
sv_in =arcpts(CX,by,rB+0.4,420,120,60)
A('<path d="M'+f'{sv_out[0][0]:.2f},{sv_out[0][1]:.2f} '+" ".join(f"L{x:.2f},{y:.2f}" for x,y in sv_out[1:])
  +" "+" ".join(f"L{x:.2f},{y:.2f}" for x,y in sv_in)+' Z" fill="url(#rubber)" stroke="#444" stroke-width="0.4"/>')

# ---------- round sling (C) : webbing basket over saver + two near-vertical legs ----------
thim=(CX,165.0)
shL=(CX+ (rB+5.0)*math.cos(math.radians(135)), by+(rB+5.0)*math.sin(math.radians(135)))
shR=(CX+ (rB+5.0)*math.cos(math.radians(45)),  by+(rB+5.0)*math.sin(math.radians(45)))
crown=arcpts(CX,by,rB+5.0,135,405,60)
sling=[ (thim[0],thim[1]) ]+[shL]+crown+[shR]+[(thim[0],thim[1])]
pl(sling, 4.6, "#7d7d7d")     # webbing body
pl(sling, 4.6, "none")        # (noop keep)
# webbing edge lines
pl(sling, 5.2, "#333")        # dark outline behind (draw order: redo)
pl(sling, 4.4, "#cfcfcf")     # light fill on top
# anti-chafe ticks where legs leave saver
for sh in (shL,shR):
    ln(sh[0]-1.6,sh[1]-1.6,sh[0]+1.6,sh[1]+1.6,0.5,"#222")

# ---------- redundant backup sling (I) to a 2nd limb ----------
b2=(CX-92, by-30); rB2=12.0
b2bark=[(b2[0]+(rB2+0.8)*math.cos(math.radians(a)), b2[1]+(rB2+0.8)*math.sin(math.radians(a))) for a in range(0,361,8)]
A('<path d="M'+ " L".join(f"{x:.2f},{y:.2f}" for x,y in b2bark)+' Z" fill="#efe9df" stroke="#3a2f25" stroke-width="0.7"/>')
circ(b2[0],b2[1],rB2-1.2,0.3,"#9c8e76")
circ(b2[0]+0.3,b2[1]-0.2,0.5,0,"#000","#000")
# small saver + sling over backup limb, one leg down to master ring zone
ms=(CX,183.0)
bcrown=arcpts(b2[0],b2[1],rB2+2.2,150,390,30)
A('<path d="M'+ " L".join(f"{x:.2f},{y:.2f}" for x,y in bcrown)+'" fill="none" stroke="url(#rubber)" stroke-width="2.6"/>')
bleg=[(b2[0]+ (rB2+3.5)*math.cos(math.radians(60)), b2[1]+(rB2+3.5)*math.sin(math.radians(60))), (ms[0]-2,ms[1]-1)]
pl([bcrown[0]]+bleg, 3.2, "#333")
pl([bcrown[0]]+bleg, 2.6, "#dcdcdc")

# ---------- METAL CHAIN (D..H) ----------
def thimble(x,y):
    pathd(f"M{x-3.2:.2f},{y-3.0:.2f} C{x-3.2:.2f},{y+2.0:.2f} {x:.2f},{y+4.4:.2f} {x:.2f},{y+4.4:.2f} "
          f"C{x:.2f},{y+4.4:.2f} {x+3.2:.2f},{y+2.0:.2f} {x+3.2:.2f},{y-3.0:.2f}",
          "none","#111",0.5)
    pathd(f"M{x-1.7:.2f},{y-3.0:.2f} C{x-1.7:.2f},{y+1.2:.2f} {x:.2f},{y+2.6:.2f} {x:.2f},{y+2.6:.2f} "
          f"C{x:.2f},{y+2.6:.2f} {x+1.7:.2f},{y+1.2:.2f} {x+1.7:.2f},{y-3.0:.2f}",
          "none","#111",0.35)
thimble(*thim)
# master ring (E) — forged pear
A(f'<ellipse cx="{ms[0]:.2f}" cy="{ms[1]:.2f}" rx="6.2" ry="7.2" fill="url(#steelx)" stroke="#111" stroke-width="0.6"/>')
A(f'<ellipse cx="{ms[0]:.2f}" cy="{ms[1]:.2f}" rx="3.4" ry="4.4" fill="#fff" stroke="#111" stroke-width="0.5"/>')
# bolt-type bow shackle (F)
shy=201.0
pathd(f"M{CX-5.5:.2f},{shy:.2f} C{CX-7.5:.2f},{shy+9:.2f} {CX+7.5:.2f},{shy+9:.2f} {CX+5.5:.2f},{shy:.2f}",
      "none","#111",1.4)   # bow
ln(CX-7.2,shy,CX+7.2,shy,1.4,"#111")             # pin
A(f'<polygon points="{CX+7.2:.2f},{shy-1.6:.2f} {CX+9.4:.2f},{shy-0.9:.2f} {CX+9.4:.2f},{shy+0.9:.2f} {CX+7.2:.2f},{shy+1.6:.2f}" fill="url(#steel)" stroke="#111" stroke-width="0.3"/>')  # nut
ln(CX-7.2,shy-1.4,CX-7.2,shy+1.4,0.4,"#111")     # cotter
# swivel (G)
sy=222.0
circ(CX,sy,2.4,0.5,"#111","#fff")                # top eye
A(f'<rect x="{CX-3.2:.2f}" y="{sy+2.0:.2f}" width="6.4" height="9" rx="2.2" fill="url(#steelx)" stroke="#111" stroke-width="0.6"/>')  # barrel
circ(CX,sy+6.5,1.3,0.4,"#111","#fff")            # bearing
circ(CX,sy+13.0,2.4,0.5,"#111","#fff")           # bottom eye
# mast-top forged eye (H)
ey=243.0
A(f'<ellipse cx="{CX:.2f}" cy="{ey:.2f}" rx="4.6" ry="5.6" fill="url(#steel)" stroke="#111" stroke-width="0.7"/>')
A(f'<ellipse cx="{CX:.2f}" cy="{ey:.2f}" rx="2.1" ry="3.0" fill="#fff" stroke="#111" stroke-width="0.5"/>')
A(f'<polygon points="{CX-4.0:.2f},{ey+4.8:.2f} {CX+4.0:.2f},{ey+4.8:.2f} {CX+2.4:.2f},{ey+10:.2f} {CX-2.4:.2f},{ey+10:.2f}" fill="url(#steel)" stroke="#111" stroke-width="0.5"/>')  # machined plug
ln(CX-2.4,ey+10,CX+2.4,ey+10,0.6,"#111")
# Ø20 mast tube continues
rect_x=CX-1.4
A(f'<rect x="{rect_x:.2f}" y="{ey+10:.2f}" width="2.8" height="120" fill="url(#steel)" stroke="#111" stroke-width="0.5"/>')
ln(CX,ey+10,CX,ey+130,0.12,"#000","3,1,0.6,1")   # centreline
# rigging cables spring off just under eye
for dx in (28,-28,60,-60):
    ln(CX,ey+14, CX+dx, ey+70, 0.3,"#000")

# faint load-path chevrons
for yy in (150,236):
    A(f'<path d="M{CX-2.2:.2f},{yy:.2f} L{CX:.2f},{yy+3:.2f} L{CX+2.2:.2f},{yy:.2f}" fill="none" stroke="#bbb" stroke-width="0.4"/>')

# ---------- KEY BUBBLES ----------
def bub(letter,bx,by_,tx,ty):
    ln(bx,by_,tx,ty,0.13,"#000")
    circ(tx,ty,0.7,0,"#000","#000")
    circ(bx,by_,3.1,0.4,"#000","#fff")
    txt(bx,by_+1.05,letter,3.3,"middle","bold")
bub("A",300,68, CX+rB*0.86, by-rB*0.5)
bub("B",300,92, CX+ (rB+3)*math.cos(math.radians(18)), by+(rB+3)*math.sin(math.radians(18)))
bub("C",300,116, shR[0]+2, shR[1]+10)
bub("D",300,160, thim[0]+3, thim[1]+1)
bub("E",300,181, ms[0]+6, ms[1])
bub("F",300,202, CX+9.4, shy)
bub("G",300,226, CX+3.2, sy+7)
bub("H",300,248, CX+4.6, ey)
bub("I",92,54, b2[0], b2[1]-rB2)
bub("J",120,150, CX-rB-6, by+rB*0.62)

# detail tag
txt(28,28,"BRANCH ATTACHMENT &#8212; DETAIL",6.5,"start","bold",ls=0.5)
txt(28,35,"Vertical section &#183; host limb in cross-section &#183; suspended (tension) connection &#183; NO dimensions (design intent)",2.9)
A('<circle cx="200" cy="300" r="0" />')

# ================= RIGHT COLUMN =================
LX=372
def rule(y): A(f'<line x1="{LX-4}" y1="{y:.2f}" x2="578" y2="{y:.2f}" stroke="#000" stroke-width="0.4"/>')
def head(y,s): txt(LX-4,y,s,4.6,"start","bold",ls=0.7)

# LEGEND
head(34,"LEGEND &#8212; CONNECTION"); rule(37)
legend=[
 ("A","Host limb (live, sound, large-diameter) shown in cross-section &#8212; bark, living cambium ring, growth rings, pith"),
 ("B","Cambium-saver sleeve (EPDM / felt-lined) &#8212; the ONLY element bearing on bark; wraps past where the sling leaves the limb"),
 ("C","Wide polyester round sling, rigged as an open BASKET over B &#8212; near-vertical legs, demountable, never a choking ring"),
 ("D","Steel thimble &#8212; protects sling fibres at the bend"),
 ("E","Forged master ring / pear collector"),
 ("F","Bolt-type (safety-pin) bow shackle &#8212; will not unscrew under dynamic load"),
 ("G","Anti-spin swivel &#8212; frees occupant rotation, no torque into limb"),
 ("H","Forged mast-top eye capping the &#216;20 spire &#8212; engineered termination (replaces the 4-prong hook)"),
 ("I","Redundant backup sling to a 2nd sound limb &#8212; life-safety"),
 ("J","Basket seated against branch collar &#8212; anti-creep (no axial walk)"),
]
yy=44
for k,d in legend:
    circ(LX+1,yy-1,2.7,0.4,"#000","#fff"); txt(LX+1,yy+0.05,k,3.0,"middle","bold")
    txt(LX+6,yy+0.2,d,2.85)
    yy+=11.2 if len(d)<70 else 11.2

# MATERIALS
head(yy+3,"MATERIALS"); rule(yy+6); yy+=12
mats=[("steel","Forged / structural steel"),("rubber","Rubber / leather (cambium saver)")]
for pat,d in mats:
    A(f'<rect x="{LX-1:.2f}" y="{yy-3:.2f}" width="8" height="5" fill="url(#{pat})" stroke="#000" stroke-width="0.3"/>')
    txt(LX+10,yy+0.6,d,2.85); yy+=7.5
# webbing + timber swatches (drawn, not patterns)
A(f'<rect x="{LX-1:.2f}" y="{yy-3:.2f}" width="8" height="5" fill="#cfcfcf" stroke="#333" stroke-width="0.4"/>')
txt(LX+10,yy+0.6,"Polyester webbing (round sling)",2.85); yy+=7.5
A(f'<circle cx="{LX+3:.2f}" cy="{yy-0.5:.2f}" r="2.4" fill="#efe9df" stroke="#3a2f25" stroke-width="0.5"/>')
A(f'<circle cx="{LX+3:.2f}" cy="{yy-0.5:.2f}" r="1.4" fill="none" stroke="#9c8e76" stroke-width="0.25"/>')
txt(LX+10,yy+0.6,"Timber, cross-grain (host limb)",2.85); yy+=10

# NOTES
def notes(y0, title, items):
    head(y0,title); rule(y0+3); y=y0+9
    for it in items:
        txt(LX-2,y,"&#8226;",2.8); txt(LX+2.5,y,it,2.7); y+= 4.0*(1+ (len(it)//58))
    return y+3
yy=notes(yy,"ATTACHMENT-LIMB CRITERIA",[
 "Live hardwood limb, &#8805; ~150 mm dia at the grip; sound species only",
 "Sited near (not on) a structurally sound union; NO co-dominant / included-bark fork",
 "Sounded for decay; no deadwood, cavity or cracks on the load path",
])
yy=notes(yy,"LOADING &amp; HARDWARE",[
 "Design load = structure + occupant 100 kg, &#215;2.0 dynamic + canopy wind",
 "Sling: vertical WLL ~1 t, rigged basket (&#8805; ~1.9 t); all metal &#8805; 5:1 on design load",
 "Continuous metal-to-metal chain D&#8211;E&#8211;F&#8211;G&#8211;H; bolt shackle pinned + split-pin",
 "Base of mast is a sway-restraint only &#8212; branch grip carries 100% of vertical load",
])
yy=notes(yy,"INSPECTION &amp; MAINTENANCE",[
 "Re-seat / slacken sling every 1&#8211;2 seasons for radial (diameter) growth",
 "Re-rate or replace textile annually (UV / abrasion); re-sound limb",
 "Post-storm inspection before re-use",
])

# TITLE BLOCK
A('<g transform="translate(372,372)">')
A('<rect x="0" y="0" width="206" height="34" fill="none" stroke="#000" stroke-width="0.6"/>')
A('<line x1="0" y1="11" x2="206" y2="11" stroke="#000" stroke-width="0.3"/>')
A('<line x1="0" y1="23" x2="206" y2="23" stroke="#000" stroke-width="0.3"/>')
A('<line x1="135" y1="23" x2="135" y2="34" stroke="#000" stroke-width="0.3"/>')
txt(4,8,"PLUG-IN PARASITE",6.2,"start","bold",ls=0.8)
txt(4,18,"Branch attachment &#8212; tree-friendly suspension detail",3.3)
txt(4,30,"caglarcelik architects &#183; CCA",3.2)
txt(139,30,"Detail &#183; n.t.s.",3.2)
txt(139,34*0+30,"",3.2)
A('</g>')
txt(478,386,"2026-06-01 &#183; Rev. A",3.2,"start")

A('</svg>')
out=r"<repo>\cinematic\drawings\PlugInParasite_branch_detail.svg"
open(out,"w",encoding="utf-8").write("\n".join(S))
print("SVG yazildi:",out,len("\n".join(S)),"bayt")
