#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plug-in Parasite — DEPLOYMENT STORYBOARD (A1 landscape), graphite/hand-drawn.
2x2 cells, each with a DIFFERENT researched tree species (Lombardy poplar, silver
birch, umbrella pine, spreading oak) and an 8-heads elegant figure in 3 poses.
Narrative: carry compact -> extend mast up by hand -> hook over a limb -> canopy
opens, base anchors. Drawing follows the researched anti-"silly" technique rules
(broken silhouette edges, breathing white, tapered angled limbs, asymmetric massing,
jittered strokes, grounded roots).  Device geometry from the GH model fold math.
"""
import math, random
def clamp(v): return max(0.0,min(1.0,v))
def rad(d): return math.radians(d)

# ---------- model fold math (verbatim) ----------
SEG1_R,SEG1_L,OVL,MAST_H=5.0,50.0,8.0,220.0
SEG2_R,SEG3_R,SOCKET_R,SOCKET_H=2.0,1.0,4.5,15.0
HUB_R,HUB_H,HUB_Z=4.0,3.0,20.0
SPAR_ANG,SPAR_LEN=36.5,90.0
PANEL_Z,PL,PW=177.7,54.0,50.0
SEG_L=max((MAST_H-SEG1_L+2*OVL)/2.0,30.0)
def state(fold):
    f=clamp(fold)
    f_tel=clamp(f*2.0); f_can=clamp((f-0.5)*2.0)
    f_rise=clamp(f_can*2.0); f_open=clamp((f_can-0.5)*2.0)
    HOOKf,HOOKd=SEG1_L,SEG1_L+2*(SEG_L-OVL)
    HOOK_Z=HOOKf+(HOOKd-HOOKf)*f_tel
    seg3_top,seg3_base=HOOK_Z,max(0.0,HOOK_Z-SEG_L)
    seg2_top=max(SEG1_L,seg3_base+OVL); seg2_base=max(0.0,seg2_top-SEG_L)
    hub_z_a=SEG1_L*0.5+(HUB_Z-SEG1_L*0.5)*f_rise
    ang=89.0+(SPAR_ANG-89.0)*f_open; slen=0.5+(SPAR_LEN-0.5)*f_open
    r_tip=HUB_R+slen*math.cos(rad(ang)); z_tip=hub_z_a+slen*math.sin(rad(ang))
    tip_r=abs(r_tip); SAG=max(tip_r*0.13,4.0)
    panel_z_a=SEG1_L*0.45+(PANEL_Z-SEG1_L*0.45)*f_rise
    psize=max(PL,PW); cpull=psize*0.05; r_closed=HUB_R+0.8; z_gath=panel_z_a+psize/4.0
    pcx=r_closed+(PL/2.0-r_closed)*f_open; pcz=z_gath+((panel_z_a+cpull)-z_gath)*f_open
    return dict(HOOK_Z=HOOK_Z,seg2=(seg2_base,seg2_top),seg3=(seg3_base,seg3_top),hub_z=hub_z_a,
                tipR=(r_tip,z_tip),tipL=(-r_tip,z_tip),ham_c=(0.0,z_tip-SAG),
                panR=(pcx,pcz),panL=(-pcx,pcz),panel_apex=(0.0,panel_z_a if f_open>0 else z_gath),
                spire=(0.0,HOOK_Z+3.0),f_open=f_open)

# ---------- svg helpers ----------
S=[];A=S.append
def ln(x1,y1,x2,y2,sw,c="#000",dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    A(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
def rect(x,y,w,h,fill,c="#000",sw=0.4):
    A(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
def circ(cx,cy,r,sw,c="#000",fill="none"):
    A(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
def pathd(d,fill,c,sw):
    A(f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
def poly(pts,fill):
    A('<polygon points="'+" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)+f'" fill="{fill}"/>')
def txt(x,y,s,sz,a="start",w="normal",c="#000",ls=0):
    L=f' letter-spacing="{ls}"' if ls else ""
    A(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{sz}" text-anchor="{a}" font-weight="{w}" fill="{c}"{L}>{s}</text>')

# ---------- graphite helpers ----------
random.seed(11)
def gray(v): v=max(0,min(255,int(v))); return f"#{v:02x}{v:02x}{v:02x}"
def hstroke(x1,y1,x2,y2,w,grey,j=0.8):
    mx,my=(x1+x2)/2,(y1+y2)/2
    A(f'<path d="M{x1:.2f},{y1:.2f} Q{mx+(random.random()-0.5)*j:.2f},{my+(random.random()-0.5)*j:.2f} {x2:.2f},{y2:.2f}" '
      f'fill="none" stroke="{grey}" stroke-width="{w:.2f}" stroke-linecap="round"/>')
def limb(p0,p1,w0,w1,dark=0):
    # tapered graphite limb: scattered short dashes (no banding) + broken shadow edge
    dx,dy=p1[0]-p0[0],p1[1]-p0[1]; L=math.hypot(dx,dy)
    if L<0.6: return
    ux,uy=dx/L,dy/L; nx,ny=-uy,ux
    m=int(L*(w0+w1)*0.5*0.11)+4
    for _ in range(m):
        u=random.random(); o=random.uniform(-0.5,0.5); w=w0+(w1-w0)*u
        pxp=p0[0]+ux*u*L+nx*o*w; pyp=p0[1]+uy*u*L+ny*o*w
        dl=random.uniform(1.6,4.6); ja=random.uniform(-0.22,0.22); ca,sa=math.cos(ja),math.sin(ja)
        ddx=(ux*ca-uy*sa)*dl; ddy=(uy*ca+ux*sa)*dl
        t=0.5+0.5*o+0.12*abs(o)+random.uniform(-0.12,0.12); t=max(0,min(1,t))
        hstroke(pxp-ddx*0.5,pyp-ddy*0.5,pxp+ddx*0.5,pyp+ddy*0.5, random.uniform(0.14,0.32), gray(208-126*t-dark), j=0.5)
    for i in range(9):
        if random.random()<0.6:
            t0=i/9; t1=(i+0.8)/9; wa=w0+(w1-w0)*t0; wb=w0+(w1-w0)*t1
            a0=(p0[0]+ux*t0*L+nx*0.46*wa, p0[1]+uy*t0*L+ny*0.46*wa)
            a1=(p0[0]+ux*t1*L+nx*0.46*wb, p0[1]+uy*t1*L+ny*0.46*wb)
            hstroke(a0[0],a0[1],a1[0],a1[1],0.4,gray(86-dark),j=0.4)
def clump(cx,cy,rx,ry,n,base=190):
    # leaf mass: short c-shaped commas, denser underside/inner; lots of white
    for _ in range(n):
        a=random.uniform(0,6.283); rr=random.random()**0.55
        px=cx+math.cos(a)*rx*rr; py=cy+math.sin(a)*ry*rr + ry*0.10*rr
        l=random.uniform(1.1,2.6); ang=random.uniform(0,6.283)
        ex,ey=px+math.cos(ang)*l,py+math.sin(ang)*l
        cxp,cyp=(px+ex)/2+math.cos(ang+1.45)*l*0.45,(py+ey)/2+math.sin(ang+1.45)*l*0.45
        A(f'<path d="M{px:.2f},{py:.2f} Q{cxp:.2f},{cyp:.2f} {ex:.2f},{ey:.2f}" fill="none" stroke="{gray(base+random.uniform(-30,12))}" stroke-width="{random.uniform(0.13,0.28):.2f}" stroke-linecap="round"/>')
def edges(cx,cy,rx,ry,n,base=120):
    # broken scalloped silhouette ticks (never a closed outline)
    for _ in range(n):
        a=random.uniform(0,6.283)
        ex=cx+math.cos(a)*rx*random.uniform(0.94,1.08); ey=cy+math.sin(a)*ry*random.uniform(0.94,1.08)
        a2=a+random.uniform(-0.6,0.6); l=random.uniform(1.4,3.6)
        hstroke(ex,ey,ex+math.cos(a2)*l,ey+math.sin(a2)*l, random.uniform(0.16,0.3), gray(base+random.uniform(-18,46)))
def kinked(p,ang,length,w0,depth,spread=22):
    cur=p; a=ang; wc=w0; segs=2 if depth>=2 else 3
    for i in range(segs):
        sl=length/segs*random.uniform(0.8,1.2)
        a=a*0.86+random.uniform(-spread,spread)
        r=math.radians(a); nxt=(cur[0]+math.sin(r)*sl,cur[1]-math.cos(r)*sl)
        w1=wc*0.74; limb(cur,nxt,wc,w1); cur=nxt; wc=w1
    if depth>0 and wc>1.0:
        for _ in range(random.randint(2,3)):
            kinked(cur,a+random.uniform(-38,38),length*0.6,wc,depth-1,spread)
    return cur
def reach_limb(p,target,w0):
    mid=((p[0]+target[0])/2,min(p[1],target[1])-7)
    limb(p,mid,w0,w0*0.7); limb(mid,target,w0*0.7,w0*0.42)
def ground_tree(bx,gy,spread):
    A(f'<ellipse cx="{bx-spread*0.2:.2f}" cy="{gy+1.4:.2f}" rx="{spread*0.7:.2f}" ry="2.2" fill="#000" opacity="0.07"/>')
    for _ in range(6):
        x=bx+random.uniform(-spread,spread); hstroke(x,gy,x+random.uniform(-2,2),gy-random.uniform(2,5),0.3,gray(150))

# ============ FOUR SPECIES ============
def tree_poplar(bx,gy,H,reach=None):
    ground_tree(bx,gy,0.10*H)
    T=H*0.03
    limb((bx,gy),(bx,gy-H),T,T*0.6)
    pw=0.085*H
    for _ in range(int(H*0.9)):
        fr=random.random(); fy=gy-(0.06+0.92*fr)*H
        wcol=pw*max(0.12,1.0-abs(fr-0.30)*1.0)
        mx=bx+random.uniform(-wcol,wcol); l=random.uniform(3,6)
        hstroke(mx,fy,mx+random.uniform(-1,1),fy-l, random.uniform(0.15,0.3), gray(176+random.uniform(-34,12)))
    edges(bx,gy-0.5*H,pw,0.46*H,34,124)
    if reach: reach_limb((bx,gy-0.6*H),reach,T*0.6)

def tree_birch(bx,gy,H,reach=None):
    ground_tree(bx,gy,0.05*H)
    T=H*0.020; topy=gy-0.92*H
    limb((bx,gy),(bx+0.006*H,topy),T,T*0.7,dark=-80)        # pale slender trunk (mostly white)
    for _ in range(4):                                       # a FEW short lenticels (not a ladder)
        ly=gy-random.uniform(0.30,0.82)*H; hstroke(bx-T,ly,bx+T*0.7,ly,0.45,gray(95))
    for i in range(7):                                       # up-springing limbs, upper crown only
        fr=0.55+0.40*random.random(); fy=gy-fr*H; side=random.choice([-1,1])
        ang=side*random.uniform(40,52); r=math.radians(ang); ll=0.10*H*(1.25-fr)
        end=(bx+math.sin(r)*ll, fy-math.cos(r)*ll)
        limb((bx,fy),end,T*0.8,T*0.38,dark=-26)
        for _ in range(random.randint(2,4)):                 # drooping fine twigs (the weep)
            wx=end[0]+random.uniform(-2,2); dl=random.uniform(9,20)
            A(f'<path d="M{end[0]:.2f},{end[1]:.2f} Q{wx:.2f},{end[1]+dl*0.5:.2f} {wx+random.uniform(-2,2):.2f},{end[1]+dl:.2f}" fill="none" stroke="{gray(170+random.uniform(-16,18))}" stroke-width="0.3"/>')
    clump(bx,gy-0.76*H,0.15*H,0.28*H,80,base=198)            # faint airy crown
    edges(bx,gy-0.76*H,0.16*H,0.30*H,22,162)
    if reach: reach_limb((bx,gy-0.70*H),reach,T*0.8)

def tree_pine(bx,gy,H,reach=None):
    ground_tree(bx,gy,0.07*H)
    T=H*0.038; apex=(bx+0.05*H, gy-0.64*H)
    limb((bx,gy),apex,T,T*0.6)            # long bare leaning trunk (signature)
    for ang in (-58,-42,4,42,58):         # 5 umbrella ribs curving to horizontal
        r=math.radians(ang)
        midp=(apex[0]+math.sin(r)*0.20*H, apex[1]-math.cos(r)*0.20*H)
        end=(apex[0]+math.sin(r)*0.42*H, apex[1]-math.cos(r)*0.085*H)
        limb(apex,midp,T*0.6,T*0.4); limb(midp,end,T*0.4,T*0.22)
    uy=gy-0.82*H; uw=0.50*H               # flat-bottomed horizontal slab in top third
    for _ in range(9):
        mx=apex[0]+random.uniform(-uw,uw); my=uy-random.uniform(0,0.13*H)*abs(math.cos(mx*0.01))
        clump(mx,my,uw*0.26,0.06*H,34,196)
    edges(apex[0],uy-0.04*H,uw,0.10*H,42,128)
    if reach: reach_limb(apex,reach,T*0.55)

def tree_oak(bx,gy,H,reach=None):
    ground_tree(bx,gy,0.12*H)
    T=H*0.052; fy=gy-0.40*H
    limb((bx,gy),(bx-0.012*H,fy),T,T*0.5)
    for dx in (-1,1): limb((bx,gy-2),(bx+dx*T*0.9,gy-1),T*0.5,2)   # buttress
    for ang in (-44,-14,18,50):
        kinked((bx-0.006*H,fy),ang,0.32*H,T*0.5,2,22)
    cc=(bx, gy-0.72*H); rx=0.50*H; ry=0.32*H
    blobs=[(cc[0]-0.55*rx,cc[1]-0.16*ry,0.52*rx,0.48*ry,1.0),(cc[0]+0.5*rx,cc[1]-0.06*ry,0.48*rx,0.44*ry,0.9),
           (cc[0]-0.05*rx,cc[1]-0.5*ry,0.58*rx,0.44*ry,1.0),(cc[0]-0.22*rx,cc[1]+0.12*ry,0.44*rx,0.36*ry,0.8),
           (cc[0]+0.30*rx,cc[1]+0.18*ry,0.4*rx,0.34*ry,0.7),(cc[0]+0.04*rx,cc[1]-0.06*ry,0.5*rx,0.4*ry,0.85),
           (cc[0]-0.36*rx,cc[1]-0.34*ry,0.4*rx,0.36*ry,0.75)]
    for (mx,my,mrx,mry,sc) in blobs:
        clump(mx,my,mrx,mry,int(mrx*mry*0.95*sc),190); edges(mx,my,mrx,mry,int(mrx*0.5),114)
    if reach: reach_limb((bx,gy-0.42*H),reach,T*0.5)

# ============ ELEGANT 8-HEAD FIGURE (researched profile + poses) ============
# profile outline (forward dx, height frac), front crown->toes then back heel->skull
BODY=[(-0.020,1.000),(0.040,0.945),(0.085,0.925),(0.050,0.900),(0.045,0.875),(0.015,0.855),
      (0.070,0.690),(0.050,0.580),(0.052,0.380),(0.040,0.265),(0.042,0.180),(0.092,0.010),
      (-0.050,0.020),(-0.052,0.165),(-0.082,0.480),(-0.052,0.740),(-0.050,0.840),(-0.060,0.960)]
HEAD_I=set([0,1,2,3,4,5,17])  # points belonging to the head (rotate for tilt)
def gline(p0,p1,w,c="#2b2b2b",j=0.9):
    # one searching hand-drawn line (slight jitter + soft curve)
    mx,my=(p0[0]+p1[0])/2+(random.random()-0.5)*j,(p0[1]+p1[1])/2+(random.random()-0.5)*j
    A(f'<path d="M{p0[0]:.2f},{p0[1]:.2f} Q{mx:.2f},{my:.2f} {p1[0]:.2f},{p1[1]:.2f}" fill="none" stroke="{c}" stroke-width="{w:.2f}" stroke-linecap="round"/>')
def garm(sh,hand,bend,bw,col):
    dx,dy=hand[0]-sh[0],hand[1]-sh[1]; L=math.hypot(dx,dy) or 1
    ux,uy=dx/L,dy/L; nx,ny=-uy,ux
    el=((sh[0]+hand[0])/2+nx*bend,(sh[1]+hand[1])/2+ny*bend)
    # two contour edges of the arm + the hand
    for s in (1,-1):
        o0=2.0*bw; o1=1.1*bw
        gline((sh[0]+nx*o0*s,sh[1]+ny*o0*s),(el[0]+nx*o1*s,el[1]+ny*o1*s),bw*random.uniform(0.8,1.2),col)
        gline((el[0]+nx*o1*s,el[1]+ny*o1*s),(hand[0]+nx*0.7*bw*s,hand[1]+ny*0.7*bw*s),bw*random.uniform(0.8,1.2),col)
    A(f'<circle cx="{hand[0]:.2f}" cy="{hand[1]:.2f}" r="{1.5*bw:.2f}" fill="none" stroke="{col}" stroke-width="{bw*0.9:.2f}"/>')
def figure(fx,gy,H,tilt=0,lean=0,arm=None):
    col="#2b2b2b"; bw=H*0.0075
    A(f'<ellipse cx="{fx-H*0.06:.2f}" cy="{gy+1.3:.2f}" rx="{H*0.20:.2f}" ry="1.7" fill="#000" opacity="0.08"/>')
    def P(dx,f): return (fx+dx*H, gy-f*H)
    piv=P(-0.050,0.840); th=math.radians(tilt)
    def rot(p):
        ox,oy=p[0]-piv[0],p[1]-piv[1]
        return (piv[0]+ox*math.cos(th)-oy*math.sin(th), piv[1]+ox*math.sin(th)+oy*math.cos(th))
    pts=[(rot(P(dx,f)) if i in HEAD_I else P(dx,f)) for i,(dx,f) in enumerate(BODY)]
    A(f'<g transform="rotate({lean:.2f} {fx:.2f} {gy:.2f})">')
    # CONTOUR (croquis): searching hand-drawn outline, variable weight
    for i in range(len(pts)):
        a=pts[i]; b=pts[(i+1)%len(pts)]
        gline(a,b, bw*random.uniform(0.7,1.35), col)
        if random.random()<0.28: gline(a,b, bw*0.55, col, j=1.4)   # doubled searching line
    # interior gesture lines: front torso fold, inseam (reads as two legs), waist
    gline(P(0.018,0.855),P(0.052,0.69),bw*0.7,col); gline(P(0.052,0.69),P(0.028,0.50),bw*0.7,col)
    gline(P(0.005,0.455),P(0.02,0.17),bw*0.85,col)                 # inseam
    gline(P(-0.03,0.50),P(0.055,0.49),bw*0.6,col)                  # waist seam
    gline(P(0.02,0.815),P(0.055,0.80),bw*0.55,col)                 # collar hint
    # hair: a few flowing strands off the (tilted) crown/nape, falling back-down
    cr=pts[0]; nape=rot(P(-0.05,0.86))
    for k in range(5):
        sx=cr[0]+random.uniform(-0.004,0.02)*H; sy=cr[1]+random.uniform(-0.5,1.5)
        ex=nape[0]-random.uniform(0.005,0.04)*H; ey=nape[1]+random.uniform(0.02,0.10)*H
        A(f'<path d="M{sx:.2f},{sy:.2f} Q{(sx+ex)/2-0.03*H:.2f},{(sy+ey)/2:.2f} {ex:.2f},{ey:.2f}" fill="none" stroke="{col}" stroke-width="{bw*random.uniform(0.5,0.8):.2f}" stroke-linecap="round"/>')
    if arm is not None:
        garm(P(0.04,0.815),(arm[0],arm[1]),arm[2],bw,col)
    A('</g>')

A('<?xml version="1.0" encoding="UTF-8"?>')
A('<svg xmlns="http://www.w3.org/2000/svg" width="841mm" height="594mm" viewBox="0 0 841 594" font-family="Helvetica, Arial, sans-serif">')
A('<defs>')
A('<pattern id="steel" patternUnits="userSpaceOnUse" width="1.0" height="1.0" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.0" stroke="#1a1a1a" stroke-width="0.07"/></pattern>')
A('<pattern id="fabric" patternUnits="userSpaceOnUse" width="1.0" height="1.0"><line x1="0" y1="0" x2="0" y2="1.0" stroke="#666" stroke-width="0.05"/></pattern>')
A('<pattern id="earth" patternUnits="userSpaceOnUse" width="3.4" height="3.4" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="3.4" stroke="#9a9a9a" stroke-width="0.11"/></pattern>')
A('<radialGradient id="sky" cx="50%" cy="16%" r="95%"><stop offset="0%" stop-color="#fcfbf7"/><stop offset="100%" stop-color="#efeee7"/></radialGradient>')
A('</defs>')
A('<rect x="0" y="0" width="841" height="594" fill="url(#sky)"/>')

def draw_hook(cx, topy, s):
    ln(cx,topy,cx,topy-8*s,0.75,"#111")
    pathd(f"M{cx:.2f},{topy-8*s:.2f} Q{cx+5*s:.2f},{topy-18*s:.2f} {cx+10*s:.2f},{topy-8*s:.2f}","none","#111",0.75)
    pathd(f"M{cx:.2f},{topy-8*s:.2f} Q{cx-5*s:.2f},{topy-18*s:.2f} {cx-10*s:.2f},{topy-8*s:.2f}","none","#111",0.75)
    pathd(f"M{cx:.2f},{topy-8*s:.2f} Q{cx+1.8*s:.2f},{topy-16.5*s:.2f} {cx:.2f},{topy-13*s:.2f}","none","#111",0.6)
    pathd(f"M{cx:.2f},{topy-8*s:.2f} Q{cx-1.8*s:.2f},{topy-16.5*s:.2f} {cx:.2f},{topy-13*s:.2f}","none","#111",0.6)
def draw_parasite(cx, gy, st, s, planted=False):
    hz=st["HOOK_Z"]
    def X(x): return cx+x*s
    def Y(z): return gy-(z+SOCKET_H)*s
    if planted:
        A(f'<path d="M{X(-13):.2f},{gy:.2f} Q{X(0):.2f},{gy-8:.2f} {X(13):.2f},{gy:.2f} L{X(13):.2f},{gy+5:.2f} L{X(-13):.2f},{gy+5:.2f} Z" fill="url(#earth)" stroke="#8a8a8a" stroke-width="0.3"/>')
    sp=st["spire"]
    for tgt in (st["panR"],st["panL"],st["tipR"],st["tipL"]):
        ln(X(sp[0]),Y(sp[1]),X(tgt[0]),Y(tgt[1]),0.22,"#666")
    rect(X(-SEG1_R),Y(SEG1_L),2*SEG1_R*s,SEG1_L*s,"url(#steel)","#111",0.45)
    s2t=st["seg2"][1]; s3t=st["seg3"][1]
    if s2t>SEG1_L+0.5: rect(X(-SEG2_R),Y(s2t),2*SEG2_R*s,(s2t-SEG1_L)*s,"url(#steel)","#111",0.4)
    if s3t>s2t+0.5: rect(X(-SEG3_R),Y(s3t),2*SEG3_R*s,(s3t-s2t)*s,"url(#steel)","#111",0.35)
    rect(X(-SOCKET_R),Y(0),2*SOCKET_R*s,SOCKET_H*s,"url(#steel)","#111",0.4)
    rect(X(-HUB_R),Y(st["hub_z"]+HUB_H/2),2*HUB_R*s,HUB_H*s,"url(#steel)","#111",0.35)
    for tip in (st["tipR"],st["tipL"]):
        ln(X(HUB_R if tip[0]>0 else -HUB_R),Y(st["hub_z"]),X(tip[0]),Y(tip[1]),0.6,"#111")
    tL,tR,hc=st["tipL"],st["tipR"],st["ham_c"]
    if abs(tR[0])>HUB_R+1:
        ctrl=(X(0),2*Y(hc[1])-Y(tL[1]))
        pathd(f"M{X(tL[0]):.2f},{Y(tL[1]):.2f} Q{ctrl[0]:.2f},{ctrl[1]:.2f} {X(tR[0]):.2f},{Y(tR[1]):.2f} L{X(tR[0]):.2f},{Y(tR[1])-0.9:.2f} Q{ctrl[0]:.2f},{ctrl[1]-0.9:.2f} {X(tL[0]):.2f},{Y(tL[1])-0.9:.2f} Z","url(#fabric)","#222",0.28)
    else: circ(X(0),Y(hc[1]),1.0,0.28,"#222","url(#fabric)")
    pL,pR=st["panL"],st["panR"]; ap=st["panel_apex"]
    if abs(pR[0])>HUB_R+1:
        pathd(f"M{X(pL[0]):.2f},{Y(pL[1]):.2f} Q{X(0):.2f},{Y(ap[1])+1.0:.2f} {X(pR[0]):.2f},{Y(pR[1]):.2f} L{X(pR[0]):.2f},{Y(pR[1])-0.8:.2f} Q{X(0):.2f},{Y(ap[1])+0.2:.2f} {X(pL[0]):.2f},{Y(pL[1])-0.8:.2f} Z","url(#fabric)","#222",0.28)
    else:
        A(f'<path d="M{X(-2):.2f},{Y(ap[1]+6):.2f} L{X(0):.2f},{Y(ap[1]-2):.2f} L{X(2):.2f},{Y(ap[1]+6):.2f} Z" fill="url(#fabric)" stroke="#444" stroke-width="0.28"/>')
    return X(0), Y(hz)

# ============ STORYBOARD CELL ============
def cell(x0,y0,w,h, fold, num,label,cap, species,pose, seed):
    A(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="none" stroke="#000" stroke-width="0.5"/>')
    SCp=0.55; gy=y0+h-30; cx=x0+0.60*w; by=gy-240*SCp
    # faint far trees (atmosphere)
    random.seed(seed+100)
    for _ in range(3):
        fxk=x0+random.uniform(0.25,0.92)*w; fh=random.uniform(0.3,0.45)*h
        hstroke(fxk,gy,fxk,gy-fh*0.5,0.4,gray(214)); clump(fxk,gy-fh*0.6,fh*0.22,fh*0.16,40,base=216)
    # the panel's own tree
    random.seed(seed); Htree=0.82*h; bx=x0+0.17*w
    rch=(cx,by) if species in ("pine","oak") else None
    {"poplar":tree_poplar,"birch":tree_birch,"pine":tree_pine,"oak":tree_oak}[species](bx,gy,Htree,reach=rch)
    random.seed(11)
    # device + hook
    st=state(fold); tpx,tpy=draw_parasite(cx,gy,st,SCp, planted=(fold>=1.0)); draw_hook(tpx,tpy,SCp)
    # figure (8-head, researched poses)
    fH=104.0
    if pose=="carry":
        figure(cx-44,gy,fH, tilt=3, lean=1, arm=(cx-8, gy-fH*0.30, fH*0.05))
    elif pose=="extend":
        figure(cx-40,gy,fH, tilt=-16, lean=3, arm=(cx-5, gy-fH*0.92, -fH*0.045))
    else:  # gaze
        figure(cx-66,gy,fH, tilt=-25, lean=0, arm=(cx-66+fH*0.055, gy-fH*0.45, fH*0.04))
    # caption
    txt(x0+10,y0+h-12, num, 7.5,"start","bold","#111")
    txt(x0+22,y0+h-15, label, 4.6,"start","bold",ls=0.5)
    txt(x0+22,y0+h-9, cap, 3.0,"start","normal","#555")

# ============ TITLE + 2x2 GRID ============
txt(24,30,"PLUG-IN PARASITE &#8212; DEPLOYMENT SEQUENCE",9,"start","bold",ls=1.0)
txt(24,39,"Carried compact, telescoped up by hand, hooked over a living limb, then opened &#183; four forest settings &#183; graphite study &#183; no dimensions",3.6)
GX0,GY0,CW,CH,GAP=22,48,398,250,4
cells=[(0.0, "1","CARRY", "compact unit brought to site","poplar","carry", 5),
       (0.3, "2","EXTEND","telescopic mast pushed up by hand","birch","extend", 14),
       (0.5, "3","HOOK",  "4-prong hook set over a living limb","pine","extend", 23),
       (1.0, "4","OPEN",  "canopy deploys; socket base anchors to the ground","oak","gaze", 31)]
pos=[(GX0,GY0),(GX0+CW+GAP,GY0),(GX0,GY0+CH+GAP),(GX0+CW+GAP,GY0+CH+GAP)]
for (fold,num,label,cap,sp,pose,seed),(x0,y0) in zip(cells,pos):
    cell(x0,y0,CW,CH, fold,num,label,cap,sp,pose,seed)
txt(GX0+CW+GAP+CW-4, GY0+CH+GAP+CH-9, "figure &#8776; 1.8 m &#183; caglarcelik architects &#183; CCA &#183; Rev. E", 3.0,"end","normal","#555")

A('</svg>')
out=r"<repo>\cinematic\drawings\PlugInParasite_deployment.svg"
open(out,"w",encoding="utf-8").write("\n".join(S))
print("SVG:",out,len("\n".join(S)),"bayt")
