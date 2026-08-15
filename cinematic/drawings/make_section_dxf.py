#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plug-in Parasite — A-A boyuna kesit -> DXF (R12 ASCII, gercek olcek, mm).
Tum koordinatlar GH modelinden (2026-06-01).  Model cm -> DXF mm (x10).
Section plane = XZ ; DXF Y = kot (elevation).  1:1 cizim, 1:20 plot edilir.

Katmanlar:
  CUT      kesit elemanlari (mast, soket, hub)    ACI 7
  VISIBLE  gorunen kenarlar (hammock, panel, kanca) ACI 7
  HIDDEN   teleskop ic ice gizli kisimlar (dashed) ACI 8
  CENTER   mast ekseni (center linetype)           ACI 4
  SPARS    radyal spar borulari                    ACI 7
  ROPES    gergi halatlari                         ACI 3
  GROUND   zemin cizgisi                           ACI 7
  DIMS     olcu cizgileri + degerler               ACI 1
  LEVELS   kot isaretleri                           ACI 1
  TEXT     malzeme aciklamalari / baslik           ACI 2
"""
import math

# ---------- yardimcilar ----------
out = []
def g(code, val): out.append(f"{code}\n{val}")

def line(layer, x1, y1, x2, y2):
    g(0,"LINE"); g(8,layer)
    g(10,f"{x1:.3f}"); g(20,f"{y1:.3f}"); g(30,"0.0")
    g(11,f"{x2:.3f}"); g(21,f"{y2:.3f}"); g(31,"0.0")

def polyline(layer, pts, closed=False):
    g(0,"POLYLINE"); g(8,layer); g(66,1)
    g(10,"0.0"); g(20,"0.0"); g(30,"0.0"); g(70, 1 if closed else 0)
    for (x,y) in pts:
        g(0,"VERTEX"); g(8,layer); g(10,f"{x:.3f}"); g(20,f"{y:.3f}"); g(30,"0.0")
    g(0,"SEQEND"); g(8,layer)

def text(layer, x, y, h, s, halign=0, rot=0.0):
    # halign: 0=left 1=center 2=right  (vertical baseline)
    g(0,"TEXT"); g(8,layer)
    g(10,f"{x:.3f}"); g(20,f"{y:.3f}"); g(30,"0.0")
    g(40,f"{h:.2f}"); g(1,s)
    if rot: g(50,f"{rot:.2f}")
    if halign:
        g(72,halign)
        g(11,f"{x:.3f}"); g(21,f"{y:.3f}"); g(31,"0.0")

def arc_poly(layer, cx, cy, r, a1, a2, n=16):
    pts=[]
    for i in range(n+1):
        a=math.radians(a1+(a2-a1)*i/n)
        pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    polyline(layer, pts)

# ---------- DXF iskelet ----------
def header():
    g(0,"SECTION"); g(2,"HEADER")
    g(9,"$ACADVER"); g(1,"AC1009")
    g(9,"$INSUNITS"); g(70,4)            # 4 = millimetre
    g(9,"$EXTMIN"); g(10,-2200.0); g(20,-300.0); g(30,0.0)
    g(9,"$EXTMAX"); g(10,1300.0); g(20,2400.0); g(30,0.0)
    g(0,"ENDSEC")

def tables():
    g(0,"SECTION"); g(2,"TABLES")
    # LTYPE
    g(0,"TABLE"); g(2,"LTYPE"); g(70,3)
    g(0,"LTYPE"); g(2,"CONTINUOUS"); g(70,0); g(3,"Solid line"); g(72,65); g(73,0); g(40,0.0)
    g(0,"LTYPE"); g(2,"DASHED"); g(70,0); g(3,"__ __ __"); g(72,65); g(73,2); g(40,15.0); g(49,10.0); g(49,-5.0)
    g(0,"LTYPE"); g(2,"CENTER"); g(70,0); g(3,"____ _ ____"); g(72,65); g(73,4); g(40,50.0); g(49,30.0); g(49,-6.0); g(49,6.0); g(49,-6.0)
    g(0,"ENDTAB")
    # LAYER
    layers = [
        ("CUT",7,"CONTINUOUS"),("VISIBLE",7,"CONTINUOUS"),("HIDDEN",8,"DASHED"),
        ("CENTER",4,"CENTER"),("SPARS",7,"CONTINUOUS"),("ROPES",3,"CONTINUOUS"),
        ("GROUND",7,"CONTINUOUS"),("DIMS",1,"CONTINUOUS"),("LEVELS",1,"CONTINUOUS"),
        ("TEXT",2,"CONTINUOUS"),
    ]
    g(0,"TABLE"); g(2,"LAYER"); g(70,len(layers))
    for name,color,lt in layers:
        g(0,"LAYER"); g(2,name); g(70,0); g(62,color); g(6,lt)
    g(0,"ENDTAB")
    g(0,"ENDSEC")

# ======================================================================
#  GEOMETRI  (cm modelinden, x10 = mm)
# ======================================================================
def entities():
    g(0,"SECTION"); g(2,"ENTITIES")

    # --- CUT: kesit elemanlari (kapali polyline -> CAD'de kolay hatch) ---
    polyline("CUT", [(-45,-150),(45,-150),(45,0),(-45,0)], closed=True)        # soket
    polyline("CUT", [(-50,0),(50,0),(50,500),(-50,500)], closed=True)          # seg1
    polyline("CUT", [(-20,500),(20,500),(20,1350),(-20,1350)], closed=True)    # seg2 gorunen
    polyline("CUT", [(-10,1350),(10,1350),(10,2200),(-10,2200)], closed=True)  # seg3 gorunen
    polyline("CUT", [(-40,185),(40,185),(40,215),(-40,215)], closed=True)      # hub

    # --- HIDDEN: teleskop ic ice gecen (gizli) kisimlar ---
    line("HIDDEN", -20,420,-20,500); line("HIDDEN", 20,420,20,500); line("HIDDEN", -20,420,20,420)   # seg2 in seg1
    line("HIDDEN", -10,1270,-10,1350); line("HIDDEN", 10,1270,10,1350); line("HIDDEN", -10,1270,10,1270) # seg3 in seg2

    # --- CENTER: mast ekseni ---
    line("CENTER", 0,-160, 0,2300)

    # --- SPARS: 4 radyal spar (kesitte 2), %C14.3 boru -> cift cizgi ---
    def pipe(layer, x1,y1,x2,y2, r):
        dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; px,py=-uy*r,ux*r
        line(layer, x1+px,y1+py, x2+px,y2+py)
        line(layer, x1-px,y1-py, x2-px,y2-py)
        line(layer, x2+px,y2+py, x2-px,y2-py)   # uc kapak
    pipe("SPARS", 40,200, 763.5,735, 7.15)
    pipe("SPARS", -40,200, -763.5,735, 7.15)

    # --- VISIBLE: hammock, panel, kanca ---
    # hammock yayi (cok sig sarkma) center(0,3630.2) r2994.2  255.2->284.8 deg
    arc_poly("VISIBLE", 0,3630.2, 2994.2, 255.2, 284.8, n=20)
    # panel yayi center(0,2885.8) r1141.2  256.3->283.7 deg
    arc_poly("VISIBLE", 0,2885.8, 1141.2, 256.3, 283.7, n=16)
    # kanca: riser + 2 curl (yarim daire)
    line("VISIBLE", 0,2200, 0,2280)
    arc_poly("VISIBLE", 50,2280, 50, 0, 180, n=12)    # +X curl
    arc_poly("VISIBLE", -50,2280, 50, 0, 180, n=12)   # -X curl

    # --- ROPES: gergi halatlari (spire_tip 0,2230) ---
    for (tx,ty) in [(270,1777),(-270,1777),(763.5,735),(-763.5,735)]:
        line("ROPES", 0,2230, tx,ty)

    # --- GROUND ---
    line("GROUND", -1000,0, 1000,0)

    # ==================================================================
    #  OLCULER
    # ==================================================================
    H=42.0  # olcu/kot yazi yuksekligi
    # --- dikey olcu zinciri (sag, dim line x=1150) ---
    levels=[2330,2200,1777,735,500,0,-150]
    objx ={2330:100,2200:10,1777:270,735:763.5,500:50,0:50,-150:45}
    dimx=1150
    line("DIMS", dimx, -150, dimx, 2330)
    for z in levels:
        line("DIMS", objx[z], z, dimx, z)          # witness
        line("DIMS", dimx-15, z-15, dimx+15, z+15) # tick 45
    chain=[(2330,2200,"130"),(2200,1777,"423"),(1777,735,"1042"),
           (735,500,"235"),(500,0,"500"),(0,-150,"150")]
    for a,b,v in chain:
        text("DIMS", dimx+55, (a+b)/2.0, H, v, halign=1, rot=90.0)

    # --- kot isaretleri (sag ic, x=850) ---
    lvltxt={2330:"+2.330",2200:"+2.200",1777:"+1.777",735:"+0.735",
            500:"+0.500",0:"+0.000 FFL",-150:"-0.150"}
    for z in levels:
        line("LEVELS", objx[z], z, 820, z)
        text("LEVELS", 840, z+12, H, lvltxt[z], halign=0)

    # --- yatay olculer (mast hizasinda kirik) ---
    # hammock 1527 @ y=850
    yH=850
    line("DIMS", -763.5,735, -763.5,yH+20); line("DIMS", 763.5,735, 763.5,yH+20)
    line("DIMS", -763.5,yH, -150,yH); line("DIMS", 150,yH, 763.5,yH)
    text("DIMS", 0, yH-18, H, "1527", halign=1)
    # panel 540 @ y=1900
    yP=1900
    line("DIMS", -270,1777, -270,yP+20); line("DIMS", 270,1777, 270,yP+20)
    line("DIMS", -270,yP, -120,yP); line("DIMS", 120,yP, 270,yP)
    text("DIMS", 0, yP-18, H, "540", halign=1)

    # ==================================================================
    #  MALZEME ACIKLAMALARI (sol, sag-hizali x=-1100, leader -> eleman)
    # ==================================================================
    callouts=[
        ("4 kollu paslanmaz kanca",      2300, -100,2280),
        ("Teleskopik direk seg3 %%C20",  2080,    0,1900),
        ("Kanopi panel 540x500",         1820, -270,1777),
        ("Gergi halati %%C2.2",          1500, -424,1400),
        ("Teleskopik direk seg2 %%C40",  1150,    0, 900),
        ("4 radyal spar %%C14.3 / L900",  900, -361, 467),
        ("PE dokuma hammock",             650, -380, 690),
        ("Hub %%C80",                     430,  -40, 200),
        ("Taban segment seg1 %%C100",     220,  -50, 300),
        ("Zemin soketi %%C90 / 150 derin", 20,  -45, -75),
    ]
    tx0=-1100
    for s, ty, ex, ey in callouts:
        text("TEXT", tx0, ty, 45, s, halign=2)
        line("TEXT", tx0+30, ty+15, ex, ey)   # leader

    # --- baslik ---
    text("TEXT", -1100, -260, 70, "PLUG-IN PARASITE  -  BOYUNA KESIT A-A", halign=0)
    text("TEXT", -1100, -340, 45, "Acik konum (deployed) . Olcek 1:20 . Tum olculer mm . Kot +0.000 = FFL", halign=0)
    text("TEXT", -1100, -410, 45, "caglarcelik architects . CCA . 2026-06-01 . Rev. B", halign=0)

    g(0,"ENDSEC")

# ---------- yaz ----------
header(); tables(); entities(); g(0,"EOF")
data="\n".join(out)+"\n"
path=r"<repo>\cinematic\drawings\PlugInParasite_section.dxf"
with open(path,"w",encoding="utf-8") as f:
    f.write(data)
print("DXF yazildi:", path, "(", len(data), "bayt )")
