"""
Generates index.html: an apology letter that unfolds one paragraph at a time.

Usage:  python make_apology.py
Then upload index.html to your GitHub repo (turn on GitHub Pages to get a link).

EDIT THE SECTION BELOW, especially the letter. Replace every line with your own
words and the real thing you're sorry for. Specific beats general.
"""
import base64
import html
import mimetypes
import os
from urllib.parse import quote

_P = "".join(f"<ellipse cx='0' cy='-14' rx='7' ry='13' transform='rotate({a})'/>" for a in range(0, 360, 60))
FLOWER_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='-30 -30 60 60'>"
              f"<g fill='#8ec5ff' fill-opacity='.16'>{_P}</g>"
              "<circle r='6' fill='#ffd86b' fill-opacity='.28'/></svg>")
FLOWER_URI = quote(FLOWER_SVG, safe="'=/:")

# ---------- EDIT THESE ----------
HER_NAME = "langga"
YOUR_NAME = ""   # optional: put your name here to add "With love, <name>" at the end
PAGE_TITLE = "For my langga"

# Optional picture at the top (keep the file in the same folder as this script).
HERO_IMAGE = ""   # e.g. "image1.png"; leave "" for no picture

# Background music. Upload your audio file (mp3, m4a, ogg) to the same GitHub
# folder as index.html and write its exact file name here. "" = no music.
MUSIC_FILE = "lovesong.mp3"      # e.g. "our-song.mp3"
MUSIC_START = 0      # start the song this many seconds in
MUSIC_VOLUME = 0.2   # 0.0 (silent) to 1.0 (full). 0.15 to 0.25 sounds like soft background music
MUSIC_FADE = 4       # seconds to fade in slowly when she opens the letter (0 = no fade)

# The letter. One string per paragraph. Add, remove, or rewrite freely.
LETTER = [
    "to my langga,",
    "i've been thinking about what u said, and i realized that i've been so caught up in my own routine and everything going on in my day that i haven't really stopped to consider how that might be making you feel.",
    "i know you've been trying to make me feel included in your days, sharing little things with me and making room for me in the middle of everything you have going on. and i want you to know that i notice those things, and i appreciate them more than i probably get to express. i'm sorry that i haven't been giving you that same effort.",
    "i love you, langga. i'm sorry for making you feel otherwise. you matter to me, and i want the way i treat you to make that something you never have to question.",
    # You said you'd add more later: put new paragraphs here, one string each.
]

# --------------------------------

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💌</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,500;1,6..72,300&family=Figtree:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0d1b36; --bg-glow:#1f3f78; --ink:#eaf1fb; --muted:#9db4d6;
  --accent:#8ec5ff; --line:#33507f;
  --serif:"Newsreader",Georgia,"Times New Roman",serif;
  --sans:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif;
}
*{box-sizing:border-box}
html{height:100%}
body{
  margin:0; min-height:100%; color:var(--ink); font-family:var(--serif);
  background:radial-gradient(120% 80% at 50% 0%,var(--bg-glow),var(--bg) 70%) fixed;
  padding:max(2.5rem,env(safe-area-inset-top)) 1.5rem max(3rem,env(safe-area-inset-bottom));
}
main{max-width:34rem;margin:0 auto}
h1{
  font-weight:300; font-size:clamp(2.6rem,9vw,4.2rem); line-height:1.05;
  margin:1.5rem 0 2.5rem; letter-spacing:-.01em;
}
h1 em{font-style:italic;color:var(--accent)}
.music-btn{position:fixed;right:max(1rem,env(safe-area-inset-right));bottom:max(1rem,env(safe-area-inset-bottom));
  z-index:100;font-size:.9rem;padding:.7rem 1.2rem;background:rgba(13,27,54,.8);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.music-btn[hidden]{display:none}
.pic{display:block;height:auto;border-radius:14px;margin:0 0 1.2rem}
.pic.hero{width:min(240px,65%)}
h1{margin-top:0}
.letter{position:relative;padding:1.8rem 1.6rem .5rem;border:1px solid var(--line);border-radius:20px;
  background:url("data:image/svg+xml,__FLOWER__") no-repeat right -20px bottom -20px/120px,
             url("data:image/svg+xml,__FLOWER__") no-repeat left -26px top -26px/84px,
             rgba(142,197,255,.06)}
@media (max-width:420px){.letter{padding:1.4rem 1.2rem .3rem}}
.letter p{
  font-size:clamp(1.2rem,4.2vw,1.45rem); line-height:1.6; margin:0 0 1.4rem;
  opacity:0; transform:translateY(8px); transition:opacity .9s ease,transform .9s ease;
}
.letter p.show{opacity:1;transform:none}
.letter p:first-child{font-style:italic;color:var(--accent)}
.controls{margin-top:2rem;min-height:4.5rem}
button{
  font:500 1rem var(--sans); color:var(--ink); background:transparent; cursor:pointer;
  border:1px solid var(--line); border-radius:999px; padding:.8rem 1.5rem;
  transition:background .2s,border-color .2s,transform .15s;
}
button:hover{border-color:var(--accent)}
button:active{transform:scale(.97)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
button.primary{background:var(--accent);color:#0b1a33;border-color:var(--accent)}
button.primary:hover{background:#b3d8ff}
.progress{font:400 .85rem var(--sans);color:var(--muted);margin-top:.9rem}
.ask{display:none}
.ask.show{display:block}
.sign{margin-top:2.5rem;color:var(--muted);font-size:1.1rem}

.intro{position:fixed;inset:0;z-index:50;overflow:hidden;
  background:radial-gradient(120% 80% at 50% 0%,var(--bg-glow),var(--bg) 70%);
  transition:opacity .9s ease,visibility .9s}
.intro.done{opacity:0;visibility:hidden}
#garden{position:absolute;inset:0;width:100%;height:100%}
.stem{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);
  animation:grow 1.5s ease-out var(--dl) forwards}
@keyframes grow{to{stroke-dashoffset:0}}
.bloom{opacity:0;transform:scale(0) rotate(-50deg);animation:bloom 1.1s cubic-bezier(.3,1.4,.5,1) forwards}
.leaf{opacity:0;transform:scale(0);animation:leaf .8s ease-out forwards}
@keyframes bloom{to{opacity:1;transform:none}}
@keyframes leaf{to{opacity:1;transform:none}}
.intro-text{position:absolute;left:0;right:0;top:14%;text-align:center;padding:0 1.5rem;
  opacity:0;transform:translateY(6px);transition:opacity 1s,transform 1s}
.intro-text p{margin:0 0 1.4rem;font-weight:300;font-style:italic;color:var(--ink);
  font-size:clamp(1.9rem,7vw,3rem);line-height:1.15}
.intro.t .intro-text{opacity:1;transform:none}
.intro .open-btn{opacity:0;pointer-events:none;transition:opacity .8s,background .2s,border-color .2s,transform .15s}
.intro.ready .open-btn{opacity:1;pointer-events:auto}
body.locked{overflow:hidden}
@media (prefers-reduced-motion:reduce){
  .stem{animation:none;stroke-dashoffset:0}
  .bloom,.leaf{animation:none;opacity:1;transform:none}
  .intro,.intro-text{transition:none}
  .letter p{transition:none;transform:none}
}
</style>
</head>
<body class="locked">
<div class="intro" id="intro" role="dialog" aria-label="Welcome">
  <svg id="garden" viewBox="0 0 400 700" preserveAspectRatio="xMidYMax slice" aria-hidden="true"></svg>
  <div class="intro-text">
    <p>for you, __HER__</p>
    <button class="primary open-btn" id="openBtn" type="button">open letter</button>
  </div>
</div>
<main>
  __HERO__
  <h1>for my beloved</h1>
  <section class="letter" id="letter" aria-live="polite">__PARAGRAPHS__</section>
  <div class="controls">
    <button class="primary" id="next" type="button">keep reading</button>
    <div class="progress" id="progress"></div>
    <div class="ask" id="ask">__SIGN__</div>
  </div>
</main>
__AUDIO__
<script>
(function(){
  var paras=[].slice.call(document.querySelectorAll("#letter p"));
  var next=document.getElementById("next"), prog=document.getElementById("progress");
  var ask=document.getElementById("ask");
  var i=0;
  function reveal(){
    paras[i].classList.add("show"); i++;
    prog.textContent=i+" of "+paras.length;
    if(i===paras.length){
      next.style.display="none"; prog.style.display="none";
      ask.classList.add("show");
    }
    if(i>1){paras[i-1].scrollIntoView({behavior:"smooth",block:"center"});}
  }
  next.addEventListener("click",reveal);
  window.startLetter=reveal;
})();
</script>
<script>
(function(){
  var NS="http://www.w3.org/2000/svg", svg=document.getElementById("garden");
  var intro=document.getElementById("intro"), btn=document.getElementById("openBtn");
  var G="#6fbf9a";
  // x, head height, size, petal color
  var F=[[50,360,26,"#f6e6ee"],[120,300,32,"#cfe3ff"],[190,380,24,"#ffffff"],[260,280,34,"#ffd6e3"],
         [330,340,28,"#e5dcff"],[85,470,22,"#ffffff"],[155,430,26,"#ffd6e3"],[225,490,22,"#cfe3ff"],[300,450,24,"#f6e6ee"]];
  function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e;}
  F.forEach(function(f,i){
    var x=f[0],y=f[1],r=f[2],off=(i%2?18:-18),d=i*0.22,my=(700+y)/2;
    var stem=el("path",{d:"M"+x+",700 Q"+(x+off)+","+my+" "+x+","+y,fill:"none",stroke:G,"stroke-width":3,"stroke-linecap":"round","class":"stem"});
    svg.appendChild(stem);
    stem.style.setProperty("--len",stem.getTotalLength());
    stem.style.setProperty("--dl",d+"s");
    var lg=el("g",{transform:"translate("+(x+off/2)+","+my+")"});
    var leaf=el("g",{"class":"leaf"});
    leaf.style.animationDelay=(d+0.9)+"s";
    leaf.appendChild(el("ellipse",{cx:off>0?12:-12,cy:0,rx:12,ry:4.5,fill:G,transform:"rotate("+(off>0?-25:25)+" "+(off>0?12:-12)+" 0)"}));
    lg.appendChild(leaf); svg.appendChild(lg);
    var hg=el("g",{transform:"translate("+x+","+y+")"});
    var bloom=el("g",{"class":"bloom"});
    bloom.style.animationDelay=(d+1.1)+"s";
    for(var k=0;k<6;k++){
      bloom.appendChild(el("ellipse",{cx:0,cy:-r*0.8,rx:r*0.42,ry:r*0.8,fill:f[3],transform:"rotate("+(k*60)+")"}));
    }
    bloom.appendChild(el("circle",{cx:0,cy:0,r:r*0.28,fill:"#ffd86b"}));
    hg.appendChild(bloom); svg.appendChild(hg);
  });
  var calm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
  setTimeout(function(){intro.classList.add("t");},calm?0:2800);
  setTimeout(function(){intro.classList.add("ready");btn.focus({preventScroll:true});},calm?0:3700);
  btn.addEventListener("click",function(){
    intro.classList.add("done");
    document.body.classList.remove("locked");
    setTimeout(function(){intro.remove();},1000);
    if(window.startLetter){window.startLetter();}
  });
})();
</script>
</body>
</html>
"""


def js(s):
    """Safely quote a string for use inside the page's JavaScript."""
    import json
    return json.dumps(s).replace("</", "<\\/")


AUDIO_TEMPLATE = r"""<audio id="bgm" src="__SRC__" loop preload="auto"></audio>
<button class="music-btn" id="musicBtn" type="button" aria-pressed="false" hidden>♪ music off</button>
<script>
(function(){
  var a=document.getElementById("bgm"), b=document.getElementById("musicBtn"), open=document.getElementById("openBtn");
  function label(){var on=!a.paused;b.textContent=on?"♪ music on":"♪ music off";b.setAttribute("aria-pressed",on);}
  a.addEventListener("play",label);a.addEventListener("pause",label);
  open.addEventListener("click",function(){
    var target=__VOL__, secs=__FADE__, t0=Date.now();
    a.volume=secs>0?0:target;
    try{a.currentTime=__START__;}catch(e){}
    b.hidden=false;label();
    var p=a.play();if(p&&p.catch){p.catch(label);}
    if(secs>0){var iv=setInterval(function(){var k=Math.min(1,(Date.now()-t0)/(secs*1000));a.volume=target*k;if(k>=1){clearInterval(iv);}},100);}
  });
  b.addEventListener("click",function(){if(a.paused){var p2=a.play();if(p2&&p2.catch){p2.catch(label);}}else{a.pause();}});
})();
</script>"""


def audio_block():
    """Music player + on/off button. Starts when she taps 'open letter'."""
    if not MUSIC_FILE:
        return ""
    vol = min(1.0, max(0.0, float(MUSIC_VOLUME)))
    return (AUDIO_TEMPLATE
            .replace("__SRC__", html.escape(MUSIC_FILE, quote=True))
            .replace("__VOL__", str(vol))
            .replace("__FADE__", str(max(0, float(MUSIC_FADE))))
            .replace("__START__", str(max(0, float(MUSIC_START)))))


def img_tag(path, alt, cls):
    """Embed an image straight into the HTML so the page stays one file."""
    if not path or not os.path.exists(path):
        return ""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img class="pic {cls}" src="data:{mime};base64,{data}" alt="{html.escape(alt)}">'


def build():
    e = html.escape
    paragraphs = "\n    ".join(f"<p>{e(p)}</p>" for p in LETTER)
    page = (
        TEMPLATE
        .replace("__TITLE__", e(PAGE_TITLE))
        .replace("__HER__", e(HER_NAME))
        .replace("__SIGN__", f'<div class="sign">with love,<br>{e(YOUR_NAME)}</div>' if YOUR_NAME else "")
        .replace("__HERO__", img_tag(HERO_IMAGE, "Two little characters typing at keyboards in the rain", "hero"))
        .replace("__AUDIO__", audio_block())
        .replace("__FLOWER__", FLOWER_URI)
        .replace("__PARAGRAPHS__", paragraphs)
    )
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("Wrote index.html. Upload it to your GitHub repo.")


if __name__ == "__main__":
    build()
