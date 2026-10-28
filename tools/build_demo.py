#!/usr/bin/env python3
"""Build the MOBIUS demo (index.html) from the full game (source/mobius.html).

The full game ships as one minified bundle, so the demo is produced by a set of
exact-match patches. Each patch must match exactly once or the build fails, which
keeps the demo honest if the source game is ever re-exported.

Demo flow:
  1. Intro cutscene, then one walk around the service ring.
  2. About halfway round, the lights die and the HARLEQUIN is in your face.
  3. At the seam (end of the loop) THE THRUM forms and always lunges at you.
  4. Instead of the death screen / respawn: an "End of Demo" screen.

Usage: python3 tools/build_demo.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "mobius.html"
OUT = ROOT / "index.html"


# --- markup -----------------------------------------------------------------

CSS = """
/* DEMO: end screen (replaces the death screen) */
.demoend {
  position: fixed;
  inset: 0;
  z-index: 9;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: #000;
  user-select: none;
}

.demoend[hidden] { display: none; }

.end-chalk {
  position: relative;
  width: min(92vw, 860px);
  height: min(36vh, 200px);
}

.end-more {
  text-align: center;
  opacity: 0;
  transition: opacity 2s ease;
  pointer-events: none;
}

.end-more.show { opacity: 1; pointer-events: auto; }

.end-thanks {
  margin: 4px 0 20px;
  font-size: 12px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: #7d7a72;
}

.demo-tag {
  display: inline-block;
  margin-top: 10px;
  padding: 2px 10px;
  border: 1px solid #5a574f;
  font-size: 11px;
  letter-spacing: 0.4em;
  margin-right: -0.4em;
  color: #8f8b80;
}

</style>"""

END_SCREEN = """<div id="demoend" class="demoend" hidden>
    <div class="end-chalk"></div>
    <div class="end-more">
      <p class="end-thanks">Thank you for playing</p>
      <button id="again">Play again</button>
    </div>
  </div>
<script type="module">"""


# --- injected game code -------------------------------------------------------
# Written against the bundle's minified names: Ht player, Pe camera, pn facility,
# ye lighting, gn audio, je OBVERSE, Ji Harlequin, Nn Thrum, Xe intro,
# xi loop tracker, Vs flashlight model, we playing, Vn light transition.

DEMO_JS = r"""
var demoScare={
/* radians walked round the ring before the Harlequin strikes (~half a loop) */
at:2.9,
/* seconds the Thrum waits in its standoff before it lunges anyway */
lunge:2.8,
scared:!1,phase:0,t:0,p0:null,hit:!1,dir:new v,_p:new v,_a:new v,_b:new v,_c:new v,
update(i){
if(this.p0===null){!Xe.active&&we&&(this.p0=xi.progress);return 1}
if(this.phase===0){
if(this.scared||!i||Nn.active||Vn||Math.abs(xi.progress-this.p0)<this.at)return 1;
if(!Ji.mesh)return this.scared=!0,1;
let{sP:s,facing:f}=Rr(pn,Pe,this._a,this._b,this._c);
wh(s,this.dir).multiplyScalar(f);
this.phase=1,this.t=0,this.hit=!1,Rh=Math.max(Rh,25),Ht.enabled=!1;
ye.flashOn||(ye.toggleFlashlight(),Vs.pressButton());
je.silence(),gn.rustle(.5,.15)}
if(this.phase!==1)return 1;
if(!i)return this.t<.6||this.t>=1.5?.02:1;
let T=this.t+=i;
/* the lights stutter and die; in the dark, your head is turned to where it will be */
if(T<.6)return T>=.25&&(this.place(1.35,!1),this.aim(1)),T<.08?.35:T<.16?1:T<.24?.2:.02;
/* ...and they come back with it right in front of you */
if(T<1.5){
this.hit||(this.hit=!0,this.em=Ji.mesh.material.emissive.clone(),Ji.mesh.material.emissive.setRGB(.22,.21,.2),gn.shriek(),gn.boom(),Vs.jiggle());
this.place(1.35-.6*Math.min(1,(T-.6)/.12),!0),this.aim(Math.min(1,i*18));
Ht.yaw+=(Math.random()-.5)*.05,Ht.pitch+=(Math.random()-.5)*.05;
return Math.random()<.2?.45:1.15}
Ji.mesh.visible=!1,this.em&&Ji.mesh.material.emissive.copy(this.em);
if(T<2.2)return .02;
this.phase=2,this.scared=!0,Ht.enabled=we&&!Nn.cutscene;
je.memory.sawEntity=!0,je.urgent("What was that?",1.5),je.say("That isn’t one of mine.",{delay:2.5});
return 1},
/* its face, in model space: the model's ribbons push the body off-centre */
headOf(m){
if(this.head)return this.head;
let g=m.geometry.attributes.position,top=-1/0,x=0,z=0,n=0;
for(let j=0;j<g.count;j++)top=Math.max(top,g.getY(j));
for(let j=0;j<g.count;j++)g.getY(j)>top-.35&&(x+=g.getX(j),z+=g.getZ(j),n++);
return this.head=new v(x/n,top-.25,z/n)},
/* stand it k metres ahead with its face (this._p) on the corridor line */
place(k,show){
let p=pn.toFacility(this._p.copy(Ht.position)).addScaledVector(this.dir,k);
p.y=0,pn.toFacility(p);
let m=Ji.mesh;
m.rotation.set(0,Math.atan2(Pe.position.x-p.x,Pe.position.z-p.z),.12,"YXZ");
let o=this._a.copy(this.headOf(m)).applyEuler(m.rotation);
m.position.set(p.x-o.x,0,p.z-o.z),p.y=o.y,
m.scale.set(1,1,1),m.material.opacity=1,m.visible=show},
/* turn the player's head towards its face; k=1 snaps */
aim(k){
let m=this._p,o=m.x-Pe.position.x,a=m.z-Pe.position.z,c=Math.atan2(-o,-a)-Ht.yaw;
c=Math.atan2(Math.sin(c),Math.cos(c)),Ht.yaw+=c*k;
let h=Math.atan2(m.y-Pe.position.y,Math.hypot(o,a));
Ht.pitch+=(h-Ht.pitch)*k}};
var demoEndEl=Le("demoend"),demoChalk=new Ps(demoEndEl.querySelector(".end-chalk"));
function demoEnd(){
we=!1,Ht.enabled=!1,gn.deathMute(!0),document.pointerLockElement&&document.exitPointerLock(),demoEndEl.hidden=!1;
setTimeout(()=>{let b=demoEndEl.querySelector(".end-chalk").getBoundingClientRect(),t="END OF DEMO",e=Math.min(b.width/8.8,b.height*.7,110),
n=(b.width-demoChalk.measure(t,e))/2-e*.1,s=(b.height-e)/2,r=demoChalk.write(t,n,s,e,.2,.14);
gn.chalk(r-.2,.2,!0),setTimeout(()=>demoEndEl.querySelector(".end-more").classList.add("show"),(r+.8)*1e3)},1400)}
Le("again").addEventListener("click",()=>location.reload());
function kf("""

# Chalk glyphs the end screen needs that the death screen never did.
GLYPHS = (
    'rf={'
    'N:{w:7.5,s:[[[1,10],[1,0],[6.4,10],[6.4,0]]]},'
    'F:{w:6.5,s:[[[6,0],[1,0],[1,10]],[[1,5],[4.8,5]]]},'
    'M:{w:9,s:[[[1,10],[1.2,0],[4.5,6.5],[7.8,0],[8,10]]]},'
)


PATCHES = [
    # -- page chrome
    ("<title>Mobius</title>", "<title>Mobius Demo</title>"),
    ("</style>", CSS),
    ("<h1>M&Ouml;BIUS</h1>", '<h1>M&Ouml;BIUS</h1>\n      <span class="demo-tag">DEMO</span>'),
    ('<script type="module">', END_SCREEN),
    # -- every run is a fresh run: no saved memory, no save slots
    ("var IS=()=>da(yh),Qs=i=>cf(yh,i),", "var IS=()=>({}),Qs=i=>{},"),
    ("Lf.hidden=!kh&&i.length===1&&!i[0].m.visits,", "Lf.hidden=!0,"),
    # -- load the Harlequin up front so the scare never hitches
    ("Nr.disabled=!1,je.memory.visits", "Ji.preload(),Nr.disabled=!1,je.memory.visits"),
    # -- Harlequin jumpscare controller, end screen, chalk glyphs
    ("function kf(", DEMO_JS),
    ("let r=ox(t)*e*n;", "let r=ox(t)*e*n*demoScare.update(we?t:0);"),
    ("rf={", GLYPHS),
    # -- the Thrum only comes for you once the Harlequin has
    ("let e=Nn.onFlip(je.sawThrum);", "let e=Nn.onFlip(je.sawThrum||!demoScare.scared);"),
    # -- ...and in the demo, crouching won't save you
    ("o<qS||this.t>VS&&!(c.crouching&&h<.15)?", "o<qS||this.t>demoScare.lunge||this.t>VS&&!(c.crouching&&h<.15)?"),
    # -- no death screen, no respawn
    ("Nn.onDeath=tx,", "Nn.onDeath=demoEnd,"),
]


def main():
    html = SRC.read_text(encoding="utf-8")
    for old, new in PATCHES:
        n = html.count(old)
        if n != 1:
            raise SystemExit(f"patch expected 1 match, found {n}: {old[:60]!r}")
        html = html.replace(old, new)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
