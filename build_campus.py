import os, json
HERE=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(HERE,'campus_tex.json')))
D=json.load(open(os.path.join(HERE,'strat.json')))

HTML=r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The College Playbook — Campus Walk</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='88'>🎓</text></svg>">
<link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='88'>🎓</text></svg>">
<script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&family=Montserrat:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --p-hi:#2d3349; --p-lo:#1f2538;
    --panel:linear-gradient(180deg,var(--p-hi),var(--p-lo));
    --panel2:#333b54; --edge:#4a5474; --edge-dark:#0e111c;
    --ink:#f0f3fb; --mut:#a2adc8; --hair:rgba(255,255,255,.07);
    --gold:#ffd24a; --gold-d:#b07f1f;
    --go:#46c46e; --go-d:#2a8c48;
    --shadow:0 6px 0 var(--edge-dark),0 18px 38px rgba(0,0,0,.45);
    --shadow-lg:0 8px 0 var(--edge-dark),0 26px 60px rgba(0,0,0,.55);
    --ease:cubic-bezier(.22,1,.36,1);
    --pop:cubic-bezier(.2,1.2,.4,1);
  }
  *{box-sizing:border-box;font-family:'Montserrat',system-ui,sans-serif}
  html,body{margin:0;height:100%;background:#bcd6f0;overflow:hidden}
  button{font-family:inherit}

  /* ---- Campus HUD (top-left) ---- */
  #hud{position:fixed;top:16px;left:16px;z-index:9;width:300px;max-width:calc(100vw - 32px);
    background:var(--panel);border:2px solid var(--edge);border-radius:18px;
    box-shadow:var(--shadow),inset 0 1px 0 var(--hair);color:var(--ink);overflow:hidden}
  .hud-head{display:flex;align-items:center;gap:10px;padding:12px 12px 11px}
  .hud-mascot{flex:none;width:36px;height:36px;display:grid;place-items:center;font-size:19px;
    background:linear-gradient(180deg,#3a4160,#2a3047);border:1px solid var(--edge);border-radius:12px;
    box-shadow:inset 0 1px 0 var(--hair),0 2px 0 var(--edge-dark)}
  .hud-titles{flex:1;min-width:0}
  #hud .title{font-weight:800;font-size:14.5px;letter-spacing:.1px;line-height:1.1}
  #hud .sub{color:var(--mut);font-weight:600;font-size:11px;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  #hud .sub i{font-family:'Fraunces',Georgia,serif;font-style:italic;color:#d2dbed}
  .hud-min,.snd{flex:none;width:27px;height:27px;border:none;cursor:pointer;border-radius:9px;
    background:#39415a;border-bottom:3px solid #20263a;color:#d2d9eb;font-size:12px;line-height:1;
    display:grid;place-items:center;transition:transform .07s}
  .hud-min:active,.snd:active{transform:translateY(2px);border-bottom-width:1px}
  .hud-body{display:grid;gap:12px;padding:1px 13px 13px}
  #hud.min .hud-body{display:none}
  #hud.min .hud-min{transform:rotate(180deg)}
  .keys{display:flex;flex-wrap:wrap;gap:6px}
  .key{display:inline-flex;align-items:center;gap:5px;background:var(--panel2);
    border:1px solid var(--edge);border-bottom:3px solid var(--edge-dark);
    border-radius:9px;padding:5px 9px;font-weight:700;font-size:11px;color:var(--ink)}
  .key b{color:#9fc2ff;font-weight:800}
  .legend{display:flex;flex-wrap:wrap;gap:5px 12px}
  .legend span{display:inline-flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--mut)}
  .legend i{width:10px;height:10px;border-radius:3px;box-shadow:0 1px 0 rgba(0,0,0,.4)}

  /* ---- Lesson card (slides up on approach) ---- */
  #card{position:fixed;left:0;right:0;bottom:0;z-index:20;display:none;justify-content:center;
    pointer-events:none;padding:0 14px 18px}
  #card.show{display:flex;animation:slideup .34s var(--pop)}
  @keyframes slideup{from{transform:translateY(40px);opacity:0}to{transform:translateY(0);opacity:1}}
  .card-box{pointer-events:auto;position:relative;width:min(620px,96vw);background:var(--panel);
    border:3px solid var(--edge);border-radius:22px;
    box-shadow:var(--shadow-lg),inset 0 1px 0 var(--hair);overflow:hidden;color:var(--ink)}
  .card-top{padding:18px 22px 15px;position:relative;overflow:hidden;
    background:
      radial-gradient(130% 150% at 90% -20%, color-mix(in srgb,var(--accent) 32%, transparent), transparent 60%),
      linear-gradient(180deg, color-mix(in srgb,var(--accent) 13%, transparent), transparent)}
  .card-top::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--accent)}
  .card-watermark{position:absolute;top:-30px;right:8px;font-size:128px;font-weight:800;line-height:1;
    color:var(--accent);opacity:.12;pointer-events:none;letter-spacing:-.04em}
  .card-eyebrow{display:flex;align-items:center;gap:10px;position:relative}
  .card-badge{display:inline-flex;align-items:center;font-weight:800;font-size:12px;color:#11161f;
    background:var(--accent);padding:4px 11px;border-radius:9px;border-bottom:3px solid rgba(0,0,0,.28)}
  .card-cat{font-weight:800;font-size:10.5px;letter-spacing:1.6px;color:var(--accent)}
  .card-title{font-weight:800;font-size:25px;line-height:1.1;margin:12px 0 4px;letter-spacing:-.02em;
    text-wrap:balance;position:relative}
  .card-tag{color:var(--mut);font-weight:600;font-size:14px;margin:0;position:relative}
  .card-body{padding:6px 22px 18px}
  .moves{display:flex;flex-direction:column;gap:8px;margin:14px 0 0}
  .move{display:flex;gap:11px;align-items:flex-start;background:var(--panel2);
    border:1px solid var(--edge);border-bottom:3px solid var(--edge-dark);border-radius:12px;
    padding:10px 13px;font-weight:600;font-size:13.5px;line-height:1.4;color:#dde4f3}
  .move i{flex:none;width:18px;height:18px;border-radius:6px;margin-top:1px;display:grid;place-items:center;
    background:color-mix(in srgb,var(--accent) 24%, transparent)}
  .move i::before{content:"";width:7px;height:7px;border-radius:2px;background:var(--accent)}
  .quote{margin:16px 0 2px;padding:14px 16px;
    background:color-mix(in srgb,var(--accent) 9%, rgba(255,255,255,.03));
    border:1px solid color-mix(in srgb,var(--accent) 24%, var(--edge));border-radius:12px;
    font-family:'Fraunces',Georgia,serif;font-style:italic;font-weight:400;color:#eaf0fb;font-size:16px;line-height:1.45}
  .card-actions{display:flex;gap:10px;padding:0 22px 20px}
  .btn{flex:1;cursor:pointer;border:none;border-radius:13px;padding:12px;font-weight:800;font-size:14px;color:#fff;
    border-bottom:4px solid rgba(0,0,0,.32);transition:transform .07s,filter .15s}
  .btn:hover{filter:brightness(1.07)}
  .btn:active{transform:translateY(2px);border-bottom-width:2px}
  .btn.prev{background:#39415a;border-bottom-color:#20263a}
  .btn.next{background:linear-gradient(180deg,#4fd07b,var(--go));border-bottom-color:var(--go-d)}
  .card-close{position:absolute;top:-13px;right:-13px;width:36px;height:36px;border:none;cursor:pointer;
    border-radius:50%;background:#ff5b6e;border-bottom:4px solid #b83145;color:#fff;font-weight:800;font-size:20px;
    box-shadow:0 6px 16px rgba(0,0,0,.4);z-index:2;transition:transform .07s}
  .card-close:active{transform:translateY(2px);border-bottom-width:2px}
  /* progress */
  .prog-top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;gap:8px}
  .prog-year{font-weight:800;font-size:12px;color:var(--gold);letter-spacing:.2px;white-space:nowrap}
  .prog-count{font-weight:600;font-size:11px;color:var(--mut);white-space:nowrap}
  .prog-count b{color:var(--ink);font-weight:800;font-size:12.5px}
  .bar{position:relative;height:11px;border-radius:6px;background:#161b29;
    border:1px solid var(--edge);overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,.55)}
  .bar i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:6px;
    background:linear-gradient(90deg,var(--go-d),var(--go));
    box-shadow:0 0 10px rgba(70,196,110,.55);transition:width .5s var(--ease)}
  .bar i::after{content:"";position:absolute;inset:0;border-radius:6px;
    background:linear-gradient(90deg,transparent 20%,rgba(255,255,255,.4),transparent 80%);
    background-size:220% 100%;animation:shine 2.4s linear infinite}
  @keyframes shine{0%{background-position:120% 0}100%{background-position:-120% 0}}
  /* graduation */
  #grad{position:fixed;inset:0;z-index:40;display:none;align-items:center;justify-content:center;
    background:radial-gradient(120% 90% at 50% 28%,rgba(46,34,78,.55),rgba(8,10,20,.84));backdrop-filter:blur(5px);overflow:hidden}
  #grad.show{display:flex}
  #confetti{position:absolute;inset:0;pointer-events:none;overflow:hidden}
  @keyframes fall{to{transform:translateY(112vh) rotate(720deg)}}
  .grad-box{position:relative;text-align:center;width:min(440px,92vw);background:var(--panel);
    border:3px solid var(--gold);border-radius:24px;padding:30px 26px 24px;color:var(--ink);
    box-shadow:0 10px 0 var(--gold-d),0 26px 70px rgba(0,0,0,.6),inset 0 1px 0 var(--hair);animation:gpop .42s var(--pop)}
  @keyframes gpop{from{transform:scale(.85);opacity:0}to{transform:scale(1);opacity:1}}
  .grad-box .cap{font-size:62px;line-height:1;filter:drop-shadow(0 6px 14px rgba(255,210,74,.4));animation:capfloat 3s ease-in-out infinite}
  @keyframes capfloat{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-8px) rotate(4deg)}}
  .grad-box h2{margin:10px 0 4px;font-weight:800;font-size:27px;letter-spacing:-.01em}
  .grad-box p{margin:0 0 18px;color:var(--mut);font-weight:600;font-size:14px}
  .grad-box .btn{width:100%;background:linear-gradient(180deg,#ffe07a,var(--gold));color:#3a2a05;border-bottom-color:var(--gold-d)}
  /* talk */
  #talk{position:fixed;left:0;right:0;bottom:0;z-index:21;display:none;justify-content:center;pointer-events:none;padding:0 14px 18px}
  #talk.show{display:flex;animation:slideup .3s var(--pop)}
  .talk-box{pointer-events:auto;position:relative;width:min(560px,96vw);background:var(--panel);
    border:3px solid var(--edge);border-radius:18px;box-shadow:var(--shadow-lg),inset 0 1px 0 var(--hair);
    padding:15px 18px;color:var(--ink);display:flex;gap:14px;align-items:flex-start}
  .talk-avatar{flex:none;width:46px;height:46px;border-radius:14px;display:grid;place-items:center;font-size:23px;
    background:linear-gradient(180deg,#3a4160,#2a3047);border:1px solid var(--edge);
    box-shadow:inset 0 1px 0 var(--hair),0 2px 0 var(--edge-dark)}
  .talk-main{flex:1;min-width:0}
  .talk-name{font-weight:800;font-size:14px;color:var(--gold);margin-bottom:4px;display:flex;align-items:center;gap:7px}
  .talk-name::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--gold);box-shadow:0 0 8px var(--gold)}
  .talk-line{margin:0 0 12px;font-weight:600;font-size:14.5px;line-height:1.5;color:#e7edf7}
  /* "press E to talk" interaction hint */
  #prompt{position:fixed;left:50%;bottom:120px;z-index:19;display:flex;align-items:center;gap:9px;
    padding:9px 15px 9px 11px;border-radius:13px;background:var(--panel);border:2px solid var(--edge);
    color:var(--ink);box-shadow:var(--shadow),inset 0 1px 0 var(--hair);font-weight:700;font-size:13.5px;
    white-space:nowrap;pointer-events:none;visibility:hidden;opacity:0;
    transform:translateX(-50%) translateY(8px);transition:opacity .18s ease,transform .18s var(--ease)}
  #prompt.show{visibility:visible;opacity:1;transform:translateX(-50%) translateY(0)}
  #prompt kbd{display:inline-grid;place-items:center;min-width:24px;height:24px;padding:0 6px;font-family:inherit;
    background:var(--panel2);border:1px solid var(--edge);border-bottom:3px solid var(--edge-dark);
    border-radius:7px;font-weight:800;font-size:12px;color:#9fc2ff}
  #prompt b{color:var(--gold);font-weight:800}
  /* learned toast */
  #toast{position:fixed;top:18px;left:50%;transform:translate(-50%,-150%);z-index:30;
    display:flex;align-items:center;gap:11px;padding:11px 16px 11px 12px;border-radius:15px;
    background:var(--panel);border:2px solid var(--go);color:var(--ink);
    box-shadow:0 6px 0 var(--go-d),0 16px 36px rgba(0,0,0,.45),inset 0 1px 0 var(--hair);
    font-weight:800;font-size:14px;opacity:0;pointer-events:none;
    transition:transform .45s var(--pop),opacity .3s ease}
  #toast.show{transform:translate(-50%,0);opacity:1}
  #toast .t-ic{flex:none;width:26px;height:26px;border-radius:50%;background:var(--go);color:#06210f;
    display:grid;place-items:center;font-size:15px;box-shadow:0 0 12px rgba(70,196,110,.5)}
  #toast small{display:block;font-weight:600;font-size:11px;color:var(--mut);margin-top:1px}
  /* minimap / radar (top-right) */
  #map{position:fixed;top:16px;right:16px;z-index:9;width:140px;height:140px;border-radius:50%;
    background:radial-gradient(circle at 50% 36%, #2c3349, #1a2032);
    border:2px solid var(--edge);box-shadow:var(--shadow),inset 0 1px 0 var(--hair);overflow:hidden}
  #map canvas{display:block;width:100%;height:100%}
  @media (max-width:600px){ #map{top:auto;bottom:16px} }
  /* generated image assets: NPC portraits + category icons */
  .talk-avatar img{width:100%;height:100%;object-fit:cover;object-position:50% 22%;display:block}
  .legend i.lg-ic{width:14px;height:14px;border-radius:0;box-shadow:none;
    -webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-position:center;mask-position:center}
  .card-cat-ic{flex:none;width:16px;height:16px;background:var(--accent);
    -webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-position:center;mask-position:center}
  @media (prefers-reduced-motion: reduce){
    *,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}
  }
  #cinematic{position:fixed;inset:0;z-index:5;pointer-events:none;
    background:
      radial-gradient(128% 96% at 50% 40%, rgba(0,0,0,0) 50%, rgba(8,6,12,0.36) 100%),
      linear-gradient(180deg, rgba(255,236,205,0.05) 0%, rgba(255,236,205,0) 26%, rgba(26,18,40,0.07) 100%);}
</style>
</head>
<body>
<div id="cinematic"></div>
<div id="hud">
  <div class="hud-head">
    <span class="hud-mascot">🎓</span>
    <div class="hud-titles">
      <div class="title">The College Playbook</div>
      <div class="sub">16 strategies from <i>How to Win at College</i></div>
    </div>
    <button class="snd" id="snd" title="sound on/off">🔊</button>
    <button class="hud-min" id="hud-min" title="collapse panel" aria-label="collapse panel">▾</button>
  </div>
  <div class="hud-body">
    <div class="prog">
      <div class="prog-top">
        <span class="prog-year" id="prog-year">Freshman Year</span>
        <span class="prog-count"><b id="prog">0</b> / 16 found</span>
      </div>
      <div class="bar"><i id="progbar"></i></div>
    </div>
    <div class="keys">
      <span class="key"><b>drag</b> look</span>
      <span class="key"><b>WASD</b> walk</span>
      <span class="key"><b>shift</b> run</span>
      <span class="key"><b>walk up</b> learn</span>
    </div>
    <div class="legend" id="legend"></div>
  </div>
</div>

<div id="toast">
  <div class="t-ic">✓</div>
  <div>Lesson learned!<small id="toast-sub">1 / 16 found</small></div>
</div>

<div id="map" title="Gold = lesson boards (filled once learned) · blue = classmates · arrow = you"><canvas id="mapcv"></canvas></div>

<div id="card">
  <div class="card-box">
    <button class="card-close" id="card-close">×</button>
    <div class="card-top">
      <div class="card-watermark" id="card-num">01</div>
      <div class="card-eyebrow">
        <span class="card-badge" id="card-badge">Lesson 01</span>
        <span class="card-cat-ic" id="card-cat-ic"></span>
        <span class="card-cat" id="card-cat">CATEGORY</span>
      </div>
      <h2 class="card-title" id="card-title">Title</h2>
      <p class="card-tag" id="card-tag">tagline</p>
    </div>
    <div class="card-body">
      <div class="moves" id="card-moves"></div>
      <div class="quote" id="card-quote">"quote"</div>
    </div>
    <div class="card-actions">
      <button class="btn next" id="card-roger">Roger that ✓</button>
    </div>
  </div>
</div>

<div id="talk">
  <div class="talk-box">
    <div class="talk-avatar"><img id="talk-portrait" alt=""></div>
    <div class="talk-main">
      <div class="talk-name" id="talk-name">Student</div>
      <p class="talk-line" id="talk-line">Hi!</p>
      <div style="text-align:right"><button class="btn next" id="talk-next" style="flex:none;display:inline-block;width:auto;padding:9px 20px">Next ▸</button></div>
    </div>
  </div>
</div>

<div id="prompt"><kbd>E</kbd><span>Talk to <b id="prompt-name">Tommy</b></span></div>

<div id="grad">
  <div id="confetti"></div>
  <div class="grad-box">
    <div class="cap">🎓</div>
    <h2>You graduated!</h2>
    <p>All 16 strategies learned. Now go win at college.</p>
    <button class="btn next" id="grad-close">Nice!</button>
  </div>
</div>

<script>
window.STRATEGIES=__STRAT__;
window.CATS=__CATS__;

(function(){var L=document.getElementById('legend'),C=window.CATS;
  Object.keys(C).forEach(function(k){var s=document.createElement('span');
    s.innerHTML='<i class="lg-ic" style="background:'+C[k].color+';-webkit-mask-image:url(asset/icons/'+k+'.png);mask-image:url(asset/icons/'+k+'.png)"></i>'+C[k].label;L.appendChild(s);});})();


/* ---- generated campus sound (WebAudio, no files) ---- */
window.SFX=(function(){
  var ctx=null,master=null,on=false,started=false,muted=false;
  function ensure(){ if(ctx)return; try{ctx=new (window.AudioContext||window.webkitAudioContext)();master=ctx.createGain();master.gain.value=0.4;master.connect(ctx.destination);}catch(e){} }
  function tone(f,dur,type,vol,when){ if(!ctx)return; var t=when||ctx.currentTime,o=ctx.createOscillator(),g=ctx.createGain();
    o.type=type||'sine';o.frequency.value=f;g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(vol||0.2,t+0.01);
    g.gain.exponentialRampToValueAtTime(0.0001,t+dur);o.connect(g);g.connect(master);o.start(t);o.stop(t+dur); }
  function step(){ if(!ctx||!on)return; var t=ctx.currentTime,len=Math.floor(ctx.sampleRate*0.05),b=ctx.createBuffer(1,len,ctx.sampleRate),d=b.getChannelData(0);
    for(var i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3);
    var s=ctx.createBufferSource();s.buffer=b;var f=ctx.createBiquadFilter();f.type='lowpass';f.frequency.value=820;var g=ctx.createGain();g.gain.value=0.06;
    s.connect(f);f.connect(g);g.connect(master);s.start(t); }
  function chime(){ if(!ctx||!on)return; var t=ctx.currentTime; tone(784,0.45,'sine',0.16,t); tone(1175,0.55,'sine',0.12,t+0.09); tone(1568,0.5,'sine',0.08,t+0.18); }
  function chirp(){ if(!ctx||!on)return; var t=ctx.currentTime,o=ctx.createOscillator(),g=ctx.createGain(),f0=1900+Math.random()*1300;
    o.type='sine';o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(f0*1.6,t+0.07);o.frequency.exponentialRampToValueAtTime(f0*0.85,t+0.15);
    g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(0.035,t+0.02);g.gain.exponentialRampToValueAtTime(0.0001,t+0.2);
    o.connect(g);g.connect(master);o.start(t);o.stop(t+0.22); }
  function birds(){ if(on&&Math.random()<0.6){chirp(); if(Math.random()<0.4)setTimeout(chirp,150); if(Math.random()<0.2)setTimeout(chirp,330);} setTimeout(birds,2600+Math.random()*4200); }
  function resume(){ ensure(); if(ctx&&ctx.state==='suspended')ctx.resume(); on=true; if(!started){started=true;birds();} }
  function setMuted(m){ muted=m; if(master) master.gain.value=m?0:0.4; }
  function isMuted(){ return muted; }
  return {resume:resume,step:step,chime:chime,setMuted:setMuted,isMuted:isMuted};
})();
window.addEventListener('pointerdown',function(){window.SFX.resume();});
window.addEventListener('keydown',function(){window.SFX.resume();});

/* ---- progress + graduation ---- */
window.markLearned=function(i){
  var SG=window.SIGNS||[]; if(i<0||!SG[i]||SG[i].done) return;
  if(SG[i].addCheck) SG[i].addCheck();
  if(window.SFX) window.SFX.chime();
  var n=0,tot=SG.length,k; for(k=0;k<tot;k++) if(SG[k].done) n++;
  updateProgress(n,tot);
  if(n<tot) showToast(n,tot);
  if(n>=tot) graduate();
};
function updateProgress(n,tot){
  var pe=document.getElementById('prog'); if(pe) pe.textContent=n;
  var pb=document.getElementById('progbar'); if(pb) pb.style.width=(n/tot*100)+'%';
  var yr=document.getElementById('prog-year'); if(yr){ var f=n/tot;
    yr.textContent = f>=1?'🎓 Graduate' : f>=0.75?'Senior Year' : f>=0.5?'Junior Year' : f>=0.25?'Sophomore Year' : 'Freshman Year'; }
}
var _toastT;
function showToast(n,tot){
  var t=document.getElementById('toast'); if(!t)return;
  var s=document.getElementById('toast-sub'); if(s) s.textContent=n+' / '+tot+' found';
  t.classList.add('show'); clearTimeout(_toastT);
  _toastT=setTimeout(function(){ t.classList.remove('show'); },2400);
}
function graduate(){
  var gr=document.getElementById('grad'); if(!gr||gr.dataset.done)return; gr.dataset.done='1'; gr.classList.add('show');
  var c=document.getElementById('confetti'),cols=['#ffd54a','#3aa856','#e25b6a','#5a8fe6','#c08be0','#ff9f43'],i;
  for(i=0;i<150;i++){ var d=document.createElement('i');
    d.style.cssText='position:absolute;top:-20px;left:'+(Math.random()*100)+'vw;width:9px;height:14px;background:'+cols[i%6]+
      ';opacity:.92;border-radius:2px;transform:rotate('+(Math.random()*360)+'deg);animation:fall '+(2.6+Math.random()*2.8)+'s linear '+(Math.random()*1.6)+'s forwards';
    c.appendChild(d); }
}
(function(){var gc=document.getElementById('grad-close'); if(gc) gc.onclick=function(){document.getElementById('grad').classList.remove('show');document.getElementById('confetti').innerHTML='';};})();
(function(){var sb=document.getElementById('snd'); if(!sb)return; sb.onclick=function(){ if(!window.SFX)return; window.SFX.resume(); var m=!window.SFX.isMuted(); window.SFX.setMuted(m); sb.textContent=m?'🔇':'🔊'; };})();
(function(){var h=document.getElementById('hud'),b=document.getElementById('hud-min'); if(!h||!b)return;
  b.onclick=function(){ h.classList.toggle('min'); h.dataset.user='1'; };
  setTimeout(function(){ if(!h.dataset.user && !h.matches(':hover')) h.classList.add('min'); },14000);
})();

/* ---- Roblox-style info card logic ---- */
(function(){
  var S=window.STRATEGIES,C=window.CATS,cur=0;
  var card=document.getElementById('card');
  function render(){
    var s=S[cur],col=C[s.cat].color;
    var num=(s.n<10?'0':'')+s.n;
    document.querySelector('.card-box').style.setProperty('--accent',col);
    document.getElementById('card-num').textContent=num;
    var bd=document.getElementById('card-badge'); if(bd) bd.textContent='Lesson '+num;
    var ci=document.getElementById('card-cat-ic'); if(ci){ var mu='url(asset/icons/'+s.cat+'.png)'; ci.style.webkitMaskImage=mu; ci.style.maskImage=mu; }
    document.getElementById('card-cat').textContent=C[s.cat].label.toUpperCase();
    document.getElementById('card-title').textContent=s.title;
    document.getElementById('card-tag').textContent=s.tagline;
    var mv=document.getElementById('card-moves'); mv.innerHTML='';
    s.moves.forEach(function(m){var d=document.createElement('div');d.className='move';
      d.innerHTML='<i></i><span>'+m+'</span>';mv.appendChild(d);});
    document.getElementById('card-quote').textContent='\u201C'+s.quote+'\u201D';
  }
  window.openCard=function(s){ if(window.closeTalk) window.closeTalk(); cur=S.indexOf(s); render(); card.classList.add('show'); };
  window.closeCard=function(){ card.classList.remove('show'); };
  function close(){ window.closeCard(); }
  document.getElementById('card-close').onclick=close;
  var rb=document.getElementById('card-roger'); if(rb) rb.onclick=function(){ if(window.markLearned) window.markLearned(cur); window.closeCard(); };
  card.onclick=function(e){ if(e.target===card) close(); };
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') close(); });
})();

AFRAME.registerComponent('pixel-world',{
  init:function(){
    var sc=this.el;
    function pass(){
      sc.object3D.traverse(function(o){
        if(o.material){
          var ms=Array.isArray(o.material)?o.material:[o.material];
          ms.forEach(function(m){ if(m.map){ m.map.magFilter=THREE.NearestFilter; m.map.minFilter=THREE.NearestFilter; m.map.generateMipmaps=false; m.map.needsUpdate=true; } });
        }
      });
    }
    [300,900,1800,3200,5000].forEach(function(d){ setTimeout(pass,d); });
  }
});

/* ===== NPC conversations ===== */
(function(){
  var cur=null, idx=0, box=document.getElementById('talk');
  function render(){ if(!cur)return;
    var tp=document.getElementById('talk-portrait'); if(tp && cur.portrait) tp.src=cur.portrait;
    document.getElementById('talk-name').textContent=cur.name;
    document.getElementById('talk-line').textContent=cur.lines[idx];
    document.getElementById('talk-next').textContent=(idx>=cur.lines.length-1)?'Bye 👋':'Next ▸'; }
  window.openTalk=function(npc){ if(cur===npc && box.classList.contains('show'))return; if(window.closeCard) window.closeCard(); cur=npc; idx=0; render(); box.classList.add('show'); };
  window.closeTalk=function(){ box.classList.remove('show'); cur=null; };
  window.isTalking=function(){ return !!cur && box.classList.contains('show'); };
  function adv(){ if(!cur)return; if(idx>=cur.lines.length-1){ window.closeTalk(); } else { idx++; render(); } }
  window.talkAdvance=adv;
  var nb=document.getElementById('talk-next');
  if(nb) nb.onclick=adv;
})();

AFRAME.registerComponent('campus',{
  init:function(){
    var self=this, S=window.STRATEGIES, C=window.CATS, root=this.el;
    this.focused=null;
    function esc(t){return String(t).replace(/"/g,'&quot;');}
    function pad(n){return (n<10?'0':'')+n;}

    var tcol=['#4f7a3a','#5c8a44','#6f9a52','#477036'];
    for(var z=4; z>=-92; z-=8){
      [-5.6,5.6].forEach(function(x){
        var t=document.createElement('a-entity');
        var xx=(x+(Math.random()*0.8-0.4)).toFixed(2);
        var tz=(z+(Math.random()*3-1.5)).toFixed(2);
        t.setAttribute('position', xx+' 0 '+tz);
        (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:parseFloat(xx),z:parseFloat(tz),r:0.6});
        var c1=tcol[Math.floor(Math.random()*tcol.length)], c2=tcol[Math.floor(Math.random()*tcol.length)];
        var hgt=(1.4+Math.random()*0.5).toFixed(2);
        var H0=parseFloat(hgt);
        t.innerHTML=
          '<a-cylinder radius="0.17" height="'+hgt+'" position="0 '+(hgt/2)+' 0" material="color:#7a5a38; roughness:1" shadow="cast: true"></a-cylinder>'+
          '<a-sphere radius="'+(1.15+Math.random()*0.3).toFixed(2)+'" position="0 '+(H0+1.0).toFixed(2)+' 0" material="color:'+c1+'; roughness:1" shadow="cast: true"></a-sphere>'+
          '<a-sphere radius="'+(0.9+Math.random()*0.25).toFixed(2)+'" position="0.55 '+(H0+1.5).toFixed(2)+' 0.15" material="color:'+c2+'; roughness:1" shadow="cast: true"></a-sphere>'+
          '<a-sphere radius="'+(0.85+Math.random()*0.25).toFixed(2)+'" position="-0.55 '+(H0+1.4).toFixed(2)+' -0.15" material="color:'+c1+'; roughness:1"></a-sphere>'+
          '<a-sphere radius="'+(0.7+Math.random()*0.2).toFixed(2)+'" position="0.05 '+(H0+2.05).toFixed(2)+' 0.1" material="color:'+c2+'; roughness:1"></a-sphere>';
        t.setAttribute('animation','property: rotation; from: -1.5 0 1.1; to: 1.5 0 -1.1; dir: alternate; loop: true; dur: '+(3000+Math.random()*2600).toFixed(0)+'; easing: easeInOutSine');
        t.setAttribute('animation__sway','property: rotation.z; from: -1.3; to: 1.3; dir: alternate; loop: true; dur: '+(2600+Math.floor(Math.random()*1800))+'; easing: easeInOutSine');
        root.appendChild(t);
      });
    }

    function building(x,z,w,h,d,tx,roof){
      var e=document.createElement('a-entity'); e.setAttribute('position',x+' 0 '+z);
      (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:x,z:z,hw:w/2+0.4,hd:d/2+0.4});
      e.innerHTML=
        '<a-box position="0 0.4 0" width="'+(w+0.3)+'" height="0.8" depth="'+(d+0.3)+'" material="color:#8d8678; roughness:1" shadow="cast: true; receive: true"></a-box>'+
        '<a-box position="0 '+(h/2+0.4)+' 0" width="'+w+'" height="'+h+'" depth="'+d+'" material="src: '+tx+'; repeat: '+Math.round(w/3.2)+' '+Math.round(h/3.2)+'; roughness: 1" shadow="cast: true; receive: true"></a-box>'+
        '<a-box position="0 '+(h+0.7)+' 0" width="'+(w+0.5)+'" height="0.5" depth="'+(d+0.5)+'" material="color:'+roof+'; roughness:1" shadow="cast: true"></a-box>';
      root.appendChild(e);
    }
    var BR='#b5482f';
    building(-11.8,-12,9,9,10,'#tex-facade1',BR);  building(-12.2,-27,9,11,10,'#tex-facade1',BR);
    building(-12.4,-42,10,10,11,'#tex-facade1',BR); building(-12.1,-58,9,12,10,'#tex-facade1',BR);
    building(-12.4,-74,10,9,11,'#tex-facade1',BR);  building(-12,-89,9,11,10,'#tex-facade1',BR);
    building(11.8,-9,9,8,10,'#tex-facade1',BR);     building(12.2,-24,9,11,10,'#tex-facade1',BR);
    building(12.4,-40,10,10,11,'#tex-facade1',BR);  building(12.1,-56,9,12,10,'#tex-facade1',BR);
    building(12.4,-72,10,9,11,'#tex-facade1',BR);   building(12,-87,9,11,10,'#tex-facade1',BR);
    // back row (taller, fills the skyline)
    building(-21,-20,12,16,11,'#tex-facade1',BR); building(-21.5,-46,12,18,11,'#tex-facade1',BR); building(-21,-72,12,15,11,'#tex-facade1',BR);
    building(21,-15,12,16,11,'#tex-facade1',BR);  building(21.5,-42,12,18,11,'#tex-facade1',BR);  building(21,-68,12,15,11,'#tex-facade1',BR);
    building(-21,-94,12,14,11,'#tex-facade1',BR);  building(21,-92,12,14,11,'#tex-facade1',BR);

    // lampposts with warm lanterns
    for(var lz=-2; lz>=-90; lz-=15){
      [-2.55,2.55].forEach(function(lx){
        var lp=document.createElement('a-entity'); lp.setAttribute('position', lx+' 0 '+lz);
        lp.innerHTML=
          '<a-cylinder radius="0.07" height="3.2" position="0 1.6 0" material="color:#2b2f37; roughness:1" shadow="cast: true"></a-cylinder>'+
          '<a-sphere radius="0.16" position="0 3.25 0" material="shader: flat; color:#ffe6a4"></a-sphere>'+
          '<a-sphere radius="0.36" position="0 3.25 0" material="shader: flat; color:#ffe6a4; transparent: true; opacity: 0.22"></a-sphere>'+
          '<a-entity rotation="0 '+(lx<0?90:-90)+' 0">'+
            '<a-plane position="0 2.5 0.08" width="0.5" height="1.3" material="shader: flat; side: double; color:#7a1f24"></a-plane>'+
            '<a-plane position="0 3.05 0.09" width="0.5" height="0.18" material="shader: flat; side: double; color:#ffcc33"></a-plane>'+
            '<a-plane position="0 1.95 0.09" width="0.5" height="0.12" material="shader: flat; side: double; color:#ffcc33"></a-plane>'+
            '<a-text value="SC" position="0 2.62 0.11" align="center" width="2.0" color="#f6efde"></a-text>'+
            '<a-text value="EST 1880" position="0 2.18 0.11" align="center" width="1.2" color="#f0e6c8"></a-text>'+
          '</a-entity>';
        root.appendChild(lp);
      });
    }

    // scattered bushes on the lawn
    for(var bi=0; bi<26; bi++){
      var bx=(Math.random()<0.5?-1:1)*(4.5+Math.random()*4.5), bz=4-Math.random()*96;
      var bu=document.createElement('a-entity'); bu.setAttribute('position', bx.toFixed(2)+' 0 '+bz.toFixed(2));
      var bc=['#3f6e36','#4a7a3e','#386632'][Math.floor(Math.random()*3)];
      bu.innerHTML='<a-sphere radius="'+(0.5+Math.random()*0.35).toFixed(2)+'" position="0 0.35 0" material="color:'+bc+'; roughness:1" shadow="cast: true"></a-sphere>';
      root.appendChild(bu);
    }

    // clock tower landmark at the end of the quad
    var tw=document.createElement('a-entity'); tw.setAttribute('position','0 0 -100'); (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:0,z:-100,r:2.6});
    tw.innerHTML=
      '<a-box position="0 6 0" width="4.2" height="12" depth="4.2" material="src:#tex-facade1; repeat:1 4; roughness:1" shadow="cast: true; receive: true"></a-box>'+
      '<a-box position="0 12.3 0" width="4.8" height="0.7" depth="4.8" material="color:#c9b27a; roughness:1" shadow="cast: true"></a-box>'+
      '<a-cone position="0 14.4 0" radius-bottom="3.6" radius-top="0" height="3.6" material="color:#b5482f; roughness:1" shadow="cast: true"></a-cone>'+
      '<a-sphere position="0 16.5 0" radius="0.32" material="shader: flat; color:#ffcc33"></a-sphere>'+
      '<a-circle position="0 9.6 2.13" radius="1.15" material="shader: flat; color:#f5f0e2"></a-circle>'+
      '<a-ring position="0 9.6 2.14" radius-inner="1.05" radius-outer="1.25" material="shader: flat; color:#3a342b"></a-ring>'+
      '<a-box position="0 9.85 2.16" width="0.07" height="0.6" depth="0.02" material="shader: flat; color:#2c2c2c"></a-box>'+
      '<a-box position="0.26 9.6 2.16" width="0.5" height="0.07" depth="0.02" rotation="0 0 -12" material="shader: flat; color:#2c2c2c"></a-box>';
    root.appendChild(tw);

    S.forEach(function(s,i){
      var z=2 - i*5.6;
      var x=(i%2===0)?-3.1:3.1;
      var col=C[s.cat].color;
      var g=document.createElement('a-entity');
      g.setAttribute('position', x+' 0 '+z.toFixed(2));
      g.setAttribute('rotation','0 '+(i%2===0?14:-14)+' 0');
      g.innerHTML=
        '<a-box width="0.09" depth="0.09" height="1.5" position="-0.78 0.75 0" material="color:#6f5740; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box width="0.09" depth="0.09" height="1.5" position="0.78 0.75 0" material="color:#6f5740; roughness:1" shadow="cast: true"></a-box>';
      var panel=document.createElement('a-entity');
      panel.setAttribute('position','0 1.78 0.06');
      panel.classList.add('clickable');
      panel.innerHTML=
        '<a-plane src="#tex-sign" width="1.95" height="1.18" material="shader: flat; transparent: true; side: double" shadow="cast: true"></a-plane>'+
        '<a-plane width="1.95" height="0.1" position="0 0.6 0.01" material="shader: flat; color: '+col+'"></a-plane>'+
        '<a-text value="'+pad(s.n)+'" position="-0.82 0.40 0.02" width="1.0" wrap-count="6" color="#3a4048"></a-text>'+
        '<a-text value="'+esc(s.title)+'" position="-0.82 0.20 0.02" width="1.66" align="left" baseline="top" wrap-count="19" color="#23272e"></a-text>'+
        '<a-text value="'+esc(s.tagline)+'" position="-0.82 -0.34 0.02" width="1.5" align="left" baseline="top" wrap-count="34" color="#5a6068"></a-text>';
      panel.addEventListener('click',function(){ window.openCard(s); });
      g.appendChild(panel);
      root.appendChild(g);
      var entry={x:x,z:z,s:s,panel:panel,group:g,i:i,done:false};
      entry.addCheck=function(){ if(entry.done)return; entry.done=true;
        var c=document.createElement('a-entity'); c.setAttribute('position','0.86 2.5 0.14');
        c.innerHTML='<a-circle radius="0.2" material="shader: flat; color:#3aa856"></a-circle>'+
                    '<a-text value="\u2713" align="center" position="0 -0.02 0.01" width="2.4" color="#ffffff"></a-text>';
        g.appendChild(c); };
      (window.SIGNS=window.SIGNS||[]).push(entry);
    });

    if(window.updateProgress) window.updateProgress(0,S.length);

    function makePerson(shirt,pants,skin,hat){
      var e=document.createElement('a-entity');
      e.innerHTML=
        '<a-entity class="nlegL" position="-0.14 0.66 0"><a-box position="0 -0.33 0" width="0.22" height="0.66" depth="0.24" material="color:'+pants+'; roughness:1" shadow="cast: true"></a-box></a-entity>'+
        '<a-entity class="nlegR" position="0.14 0.66 0"><a-box position="0 -0.33 0" width="0.22" height="0.66" depth="0.24" material="color:'+pants+'; roughness:1" shadow="cast: true"></a-box></a-entity>'+
        '<a-box position="0 1.02 0" width="0.52" height="0.76" depth="0.3" material="color:'+shirt+'; roughness:1" shadow="cast: true"></a-box>'+
        '<a-entity class="narmL" position="-0.39 1.34 0"><a-box position="0 -0.3 0" width="0.17" height="0.6" depth="0.2" material="color:'+shirt+'; roughness:1" shadow="cast: true"></a-box></a-entity>'+
        '<a-entity class="narmR" position="0.39 1.34 0"><a-box position="0 -0.3 0" width="0.17" height="0.6" depth="0.2" material="color:'+shirt+'; roughness:1" shadow="cast: true"></a-box></a-entity>'+
        '<a-box position="0 1.64 0" width="0.42" height="0.42" depth="0.42" material="color:'+skin+'; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="-0.09 1.66 -0.213" width="0.12" height="0.13" depth="0.02" material="shader: flat; color:#ffffff"></a-box>'+
        '<a-box position="0.09 1.66 -0.213" width="0.12" height="0.13" depth="0.02" material="shader: flat; color:#ffffff"></a-box>'+
        '<a-box position="-0.09 1.645 -0.222" width="0.06" height="0.08" depth="0.02" material="shader: flat; color:#20242c"></a-box>'+
        '<a-box position="0.09 1.645 -0.222" width="0.06" height="0.08" depth="0.02" material="shader: flat; color:#20242c"></a-box>'+
        '<a-box position="-0.11 1.675 -0.226" width="0.025" height="0.025" depth="0.02" material="shader: flat; color:#ffffff"></a-box>'+
        '<a-box position="0.07 1.675 -0.226" width="0.025" height="0.025" depth="0.02" material="shader: flat; color:#ffffff"></a-box>'+
        '<a-box position="-0.09 1.735 -0.213" width="0.12" height="0.03" depth="0.02" material="shader: flat; color:#3a2a1a"></a-box>'+
        '<a-box position="0.09 1.735 -0.213" width="0.12" height="0.03" depth="0.02" material="shader: flat; color:#3a2a1a"></a-box>'+
        '<a-box position="0 1.55 -0.213" width="0.16" height="0.03" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>'+
        '<a-box position="-0.095 1.57 -0.213" width="0.05" height="0.03" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>'+
        '<a-box position="0.095 1.57 -0.213" width="0.05" height="0.03" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>'+
        '<a-box position="-0.16 1.585 -0.205" width="0.06" height="0.05" depth="0.02" material="shader: flat; color:#ef9a86"></a-box>'+
        '<a-box position="0.16 1.585 -0.205" width="0.06" height="0.05" depth="0.02" material="shader: flat; color:#ef9a86"></a-box>'+
        (hat?'<a-box position="0 1.9 0" width="0.46" height="0.14" depth="0.46" material="color:'+hat+'; roughness:1" shadow="cast: true"></a-box>':'');
      return e;
    }
    var pal=[['#c0552f','#2f3a52','#e8c89a','#2a2a30'],['#2f7d5b','#3a3550','#f4c542',''],['#7a4ca0','#33405e','#e8b48a','#b23a48'],
             ['#c83b5a','#444a5c','#f0d0a0',''],['#3a6ea5','#2e3340','#e8c89a','#1b294f'],['#d99a2b','#3b4250','#caa07a','']];
    var npcChat=[
      ['Tommy Trojan',["FIGHT ON! ...sorry, reflex. I've held a sword up since 1930, my arm is ASLEEP.","Real talk from a bronze guy: don't read everything — read for the argument and bounce.","Excuse me, a pigeon has claimed my helmet again."]],
      ['Prof. Quibble',["Ah! A student. In the wild. Fascinating.","Pop quiz — kidding. Or am I? ...I'm not. It's 40% of your grade.","Office hours are 3am in a broom closet. Bring snacks."]],
      ['Dean Marlowe',["Welcome to the University of Spoiled Children. Tuition is a vibe.","Care about your grades — just don't let them care about you back.","Parking's only $9,000 a year. A steal, frankly."]],
      ['Chip',["BRO. You should TOTALLY rush our club. We do... stuff. Big stuff.","Meetings are never, attendance is mandatory, snacks are theoretical.","Anyway — FIGHT ON, my dude!"]],
      ['Brenda',["Join the Underwater Basket-Weaving Club! Undefeated — nobody else competes.","The book swears by it: take one fun class so your schedule doesn't crush you.","We meet in the pool. Bring a basket. And a snorkel."]],
      ['Coach',["Playbook rule one: don't do all your reading — read for the argument.","Lectures are the spine; the textbook just rides the bench.","Now go give me one thoughtful essay!"]],
      ['Priya',["Hi! Still lost? Everyone's lost. The campus is 80% identical brick.","Claim one quiet study spot before the freshmen colonize the library.","See you around — probably also lost!"]],
      ['Bao',["I study in short bursts — fifty on, ten off. My ten-offs have ten-offs.","Marathons turn your brain into oatmeal. I am, in fact, oatmeal.","Catch ya!"]],
      ['Marcus',["Become someone, not a résumé. Go deep on one thing.","I joined twelve clubs to 'network.' Now twelve clubs email me. Send help.","Later!"]],
      ['Jaya',["Care about your grades, just don't let them own you.","Be a tough grader of your own work — be the villain in your own draft.","Good luck out there!"]],
      ['Tour Guide',["On your LEFT: brick. On your RIGHT: shockingly, also brick.","Fun fact: the dog statue has more followers than the whole faculty.","Walking backwards is my only real skill. FIGHT ON!"]]
    ];
    window.NPCS=[];
    for(var ni=0; ni<11; ni++){
      var pp=pal[ni%pal.length], per=makePerson(pp[0],pp[1],pp[2],pp[3]);
      var lane=(ni%2===0?-1:1)*(1.9+Math.random()*1.9);
      var nz0=-Math.random()*78, nz1=nz0-(18+Math.random()*40);
      per.setAttribute('position', lane.toFixed(2)+' 0 '+nz0.toFixed(2));
      per.setAttribute('npc','z0: '+nz0.toFixed(1)+'; z1: '+nz1.toFixed(1)+'; speed: '+(1.1+Math.random()*1.4).toFixed(2)+'; dir: '+(Math.random()<0.5?-1:1));
      per.setAttribute('scale','1.25 1.25 1.25'); per.__talking=false; root.appendChild(per);
      window.NPCS.push({el:per, name:npcChat[ni][0], lines:npcChat[ni][1], portrait:'asset/portraits/npc_'+ni+'.png'});
    }

    for(var ci=0; ci<7; ci++){
      var cl=document.createElement('a-plane'), cw=(16+Math.random()*16);
      cl.setAttribute('width',cw.toFixed(1)); cl.setAttribute('height',(cw*0.55).toFixed(1));
      cl.setAttribute('rotation','-90 0 0');
      cl.setAttribute('position',(Math.random()*120-60).toFixed(1)+' '+(20+Math.random()*8).toFixed(1)+' '+(-Math.random()*100).toFixed(1));
      cl.setAttribute('material','src: #tex-cloud; shader: flat; transparent: true; opacity: 0.85; depthWrite: false');
      cl.setAttribute('drift','speed: '+(0.4+Math.random()*0.7).toFixed(2)+'; range: 66');
      root.appendChild(cl);
    }

    for(var bi2=0; bi2<4; bi2++){
      var bd=document.createElement('a-entity');
      bd.innerHTML=
        '<a-box width="0.3" height="0.16" depth="0.5" material="shader: flat; color:#33373f"></a-box>'+
        '<a-entity class="wL" position="-0.12 0.04 0"><a-box position="-0.34 0 0" width="0.68" height="0.04" depth="0.32" material="shader: flat; color:#3b4047"></a-box></a-entity>'+
        '<a-entity class="wR" position="0.12 0.04 0"><a-box position="0.34 0 0" width="0.68" height="0.04" depth="0.32" material="shader: flat; color:#3b4047"></a-box></a-entity>';
      bd.setAttribute('bird','cx: '+(Math.random()*30-15).toFixed(1)+'; cz: '+(-20-Math.random()*60).toFixed(1)+'; r: '+(18+Math.random()*22).toFixed(1)+'; h: '+(14+Math.random()*7).toFixed(1)+'; sp: '+(0.12+Math.random()*0.16).toFixed(3)+'; ph: '+(Math.random()*6.28).toFixed(2));
      root.appendChild(bd);
    }

    var lv=document.createElement('a-entity'); lv.setAttribute('leaves',''); root.appendChild(lv);

    // palm trees lining the quad
    function makePalm(){ var e=document.createElement('a-entity'),h=4.2+Math.random()*1.4,html='';
      for(var ty=0;ty<h;ty+=0.5){ html+='<a-box position="'+(ty*0.05).toFixed(2)+' '+(ty+0.25).toFixed(2)+' 0" width="0.32" height="0.5" depth="0.32" material="color:'+(Math.round(ty*2)%2?'#9c7a48':'#8a6a3a')+'; roughness:1" shadow="cast: true"></a-box>'; }
      var tx=(h*0.05).toFixed(2);
      for(var a=0;a<8;a++){ html+='<a-entity position="'+tx+' '+(h+0.2).toFixed(2)+' 0" rotation="0 '+(a*45)+' 0"><a-box position="0 -0.18 1.15" rotation="34 0 0" width="0.46" height="0.09" depth="2.5" material="color:#3f8a3e; roughness:1" shadow="cast: true"></a-box></a-entity>'; }
      html+='<a-sphere position="'+tx+' '+(h-0.1).toFixed(2)+' 0.18" radius="0.15" material="color:#6b4f2a"></a-sphere>';
      e.innerHTML=html; return e; }
    for(var pz=0; pz>=-92; pz-=11){ [-4.2,4.2].forEach(function(pxx){
      var pm=makePalm(); var pmz=(pz+(Math.random()*2-1)).toFixed(2); pm.setAttribute('position', pxx+' 0 '+pmz); root.appendChild(pm);
      (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:pxx,z:parseFloat(pmz),r:0.55}); }); }

    // cardinal & gold flower beds to fill the lawn
    for(var fb=0; fb<42; fb++){
      var fx=(Math.random()<0.5?-1:1)*(4.6+Math.random()*5.2), fz=4-Math.random()*96;
      var fe=document.createElement('a-entity'); fe.setAttribute('position', fx.toFixed(2)+' 0 '+fz.toFixed(2));
      var fh='<a-box position="0 0.12 0" width="0.95" height="0.24" depth="0.62" material="color:#3a5e30; roughness:1" shadow="cast: true"></a-box>';
      var fc=['#8a0f1a','#ffcc33','#f2efe6','#c0182a','#ffcc33'];
      for(var fp=0; fp<7; fp++){ fh+='<a-sphere position="'+(Math.random()*0.74-0.37).toFixed(2)+' 0.3 '+(Math.random()*0.46-0.23).toFixed(2)+'" radius="0.08" material="shader: flat; color:'+fc[Math.floor(Math.random()*fc.length)]+'"></a-sphere>'; }
      fe.innerHTML=fh; root.appendChild(fe);
    }

    // Trojan statue at the gate
    var st=document.createElement('a-entity'); st.setAttribute('position','-5 0 6'); st.setAttribute('rotation','0 32 0'); (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:-5,z:6,r:1.0});
    st.innerHTML=
      '<a-box position="0 0.6 0" width="1.7" height="1.2" depth="1.7" material="color:#b9a98a; roughness:1" shadow="cast: true; receive: true"></a-box>'+
      '<a-box position="0 1.28 0" width="1.3" height="0.18" depth="1.3" material="color:#a89878; roughness:1"></a-box>'+
      '<a-text value="FIGHT ON" position="0 0.72 0.86" align="center" width="2.6" color="#7a1f24"></a-text>'+
      '<a-entity position="0 1.4 0">'+
        '<a-box position="-0.16 0.45 0" width="0.26" height="0.9" depth="0.28" material="color:#7d5a2c; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0.16 0.45 0" width="0.26" height="0.9" depth="0.28" material="color:#7d5a2c; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0 1.25 0" width="0.6" height="0.92" depth="0.34" material="color:#8a6630; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0 1.96 0" width="0.46" height="0.44" depth="0.46" material="color:#8a6630; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0 2.3 0" width="0.5" height="0.16" depth="0.5" material="color:#9a7636; roughness:1"></a-box>'+
        '<a-box position="0 2.56 0" width="0.12" height="0.36" depth="0.5" material="color:#a8843e; roughness:1"></a-box>'+
        '<a-box position="0.44 1.74 0" rotation="0 0 -58" width="0.16" height="1.3" depth="0.16" material="color:#9a7636; roughness:1"></a-box>'+
        '<a-box position="0.78 2.55 0" width="0.07" height="1.6" depth="0.07" material="color:#cdb46a; roughness:1"></a-box>'+
        '<a-box position="-0.42 1.4 0" width="0.16" height="0.92" depth="0.16" material="color:#8a6630; roughness:1"></a-box>'+
      '</a-entity>';
    root.appendChild(st);

    // entrance archway over the path
    var ar=document.createElement('a-entity'); ar.setAttribute('position','0 0 4.5');
    ar.innerHTML=
      '<a-box position="-2.7 2.2 0" width="0.85" height="4.4" depth="0.85" material="src:#tex-facade1; repeat:1 2; roughness:1" shadow="cast: true"></a-box>'+
      '<a-box position="2.7 2.2 0" width="0.85" height="4.4" depth="0.85" material="src:#tex-facade1; repeat:1 2; roughness:1" shadow="cast: true"></a-box>'+
      '<a-box position="0 4.7 0" width="6.3" height="0.85" depth="0.95" material="color:#7a1f24; roughness:1" shadow="cast: true"></a-box>'+
      '<a-box position="0 5.2 0" width="6.5" height="0.2" depth="1.05" material="color:#ffcc33; roughness:1"></a-box>'+
      '<a-text value="UNIVERSITY OF SPOILED CHILDREN" position="0 4.68 0.49" align="center" width="6.7" color="#ffcc33"></a-text>'+
      '<a-text value="UNIVERSITY OF SPOILED CHILDREN" position="0 4.68 -0.49" rotation="0 180 0" align="center" width="6.7" color="#ffcc33"></a-text>';
    root.appendChild(ar);

    // dog statue at the gate (good boy)
    var dg=document.createElement('a-entity'); dg.setAttribute('position','0 0 -9'); dg.setAttribute('rotation','0 0 0'); (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:0,z:-9,r:0.85});
    dg.innerHTML=
      '<a-box position="0 0.6 0" width="1.7" height="1.2" depth="1.7" material="color:#b9a98a; roughness:1" shadow="cast: true; receive: true"></a-box>'+
      '<a-box position="0 1.28 0" width="1.3" height="0.18" depth="1.3" material="color:#a89878; roughness:1"></a-box>'+
      '<a-text value="GOOD DOG" position="0 0.72 0.86" align="center" width="2.6" color="#7a1f24"></a-text>'+
      '<a-entity position="0 1.4 0">'+
        '<a-box position="0 0.58 0" width="0.5" height="0.5" depth="1.0" material="color:#8a6630; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="-0.18 0.22 0.32" width="0.14" height="0.44" depth="0.14" material="color:#7d5a2c"></a-box>'+
        '<a-box position="0.18 0.22 0.32" width="0.14" height="0.44" depth="0.14" material="color:#7d5a2c"></a-box>'+
        '<a-box position="-0.18 0.22 -0.32" width="0.14" height="0.44" depth="0.14" material="color:#7d5a2c"></a-box>'+
        '<a-box position="0.18 0.22 -0.32" width="0.14" height="0.44" depth="0.14" material="color:#7d5a2c"></a-box>'+
        '<a-box position="0 0.82 0.5" width="0.42" height="0.46" depth="0.32" material="color:#8a6630"></a-box>'+
        '<a-box position="0 1.04 0.74" width="0.44" height="0.42" depth="0.46" material="color:#9a7636; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0 0.95 1.0" width="0.22" height="0.2" depth="0.22" material="color:#8a6630"></a-box>'+
        '<a-box position="0 0.99 1.12" width="0.1" height="0.08" depth="0.06" material="shader: flat; color:#2a2a2a"></a-box>'+
        '<a-box position="-0.18 1.3 0.68" width="0.12" height="0.24" depth="0.06" material="color:#7d5a2c"></a-box>'+
        '<a-box position="0.18 1.3 0.68" width="0.12" height="0.24" depth="0.06" material="color:#7d5a2c"></a-box>'+
        '<a-box position="0 0.74 -0.56" rotation="42 0 0" width="0.1" height="0.52" depth="0.1" material="color:#7d5a2c"></a-box>'+
      '</a-entity>';
    root.appendChild(dg);

    // ---- Metro line at the campus edge ----
    var metro=document.createElement('a-entity'); metro.setAttribute('position','0 0 21');
    var mh='<a-box position="0 0.02 0" width="34" height="0.05" depth="2.6" material="color:#6b6b66; roughness:1" shadow="receive: true"></a-box>'+
      '<a-box position="0 0.1 -0.7" width="34" height="0.12" depth="0.14" material="color:#9aa0a8; metalness:0.5; roughness:0.4"></a-box>'+
      '<a-box position="0 0.1 0.7" width="34" height="0.12" depth="0.14" material="color:#9aa0a8; metalness:0.5; roughness:0.4"></a-box>';
    for(var mt=-16; mt<=16; mt+=1.3){ mh+='<a-box position="'+mt.toFixed(1)+' 0.06 0" width="0.3" height="0.08" depth="1.9" material="color:#5a4a36; roughness:1"></a-box>'; }
    metro.innerHTML=mh; root.appendChild(metro);

    var plat=document.createElement('a-entity'); plat.setAttribute('position','-13 0 21.2');
    plat.innerHTML=
      '<a-box position="0 0.32 0" width="9" height="0.64" depth="2.1" material="color:#cfc9bd; roughness:1" shadow="receive: true; cast: true"></a-box>'+
      '<a-box position="0 2.0 -0.95" width="9" height="0.14" depth="0.14" material="color:#3a3f48"></a-box>'+
      '<a-box position="-4 1.15 -0.95" width="0.14" height="1.7" depth="0.14" material="color:#3a3f48"></a-box>'+
      '<a-box position="4 1.15 -0.95" width="0.14" height="1.7" depth="0.14" material="color:#3a3f48"></a-box>'+
      '<a-plane position="0 1.45 -0.86" width="2.8" height="0.8" material="shader: flat; color:#7a1f24"></a-plane>'+
      '<a-text value="METRO" position="0 1.45 -0.83" align="center" width="4.6" color="#ffcc33"></a-text>';
    root.appendChild(plat);

    var train=document.createElement('a-entity'); train.setAttribute('position','-18 0 21'); train.setAttribute('drift','speed: 5; range: 19');
    var L=10.5, th='';
    th+='<a-box position="0 1.15 0" width="'+L+'" height="1.7" depth="1.55" material="color:#e7eaee; metalness:0.2; roughness:0.5" shadow="cast: true"></a-box>';
    th+='<a-box position="0 2.06 0" width="'+(L-0.5)+'" height="0.28" depth="1.36" material="color:#a9afb7; roughness:0.8"></a-box>';
    th+='<a-box position="-2.3 2.3 0" width="1.5" height="0.22" depth="0.9" material="color:#8f969f"></a-box>';
    th+='<a-box position="2.3 2.3 0" width="1.5" height="0.22" depth="0.9" material="color:#8f969f"></a-box>';
    th+='<a-box position="0.4 2.46 0" width="0.5" height="0.34" depth="0.1" material="color:#3a3f48"></a-box>';
    [0.79,-0.79].forEach(function(zz){ var zf=(zz*1.01).toFixed(3), zg=(zz*1.02).toFixed(3);
      th+='<a-box position="0 0.62 '+zz+'" width="'+L+'" height="0.26" depth="0.02" material="shader: flat; color:#7a1f24"></a-box>';
      th+='<a-box position="0 0.79 '+zz+'" width="'+L+'" height="0.07" depth="0.02" material="shader: flat; color:#ffcc33"></a-box>';
      th+='<a-box position="0 1.5 '+zz+'" width="'+(L-1.7)+'" height="0.66" depth="0.02" material="shader: flat; color:#26303c"></a-box>';
      for(var wx=-L/2+1.3; wx<=L/2-1.3; wx+=1.3){ th+='<a-box position="'+wx.toFixed(2)+' 1.5 '+zf+'" width="0.08" height="0.66" depth="0.02" material="shader: flat; color:#cdd2d8"></a-box>'; }
      [-3.3,0,3.3].forEach(function(dxp){ th+='<a-box position="'+dxp+' 1.05 '+zf+'" width="0.78" height="1.5" depth="0.02" material="shader: flat; color:#c5cad0"></a-box>'+'<a-box position="'+dxp+' 1.05 '+zg+'" width="0.05" height="1.5" depth="0.02" material="shader: flat; color:#7d848d"></a-box>'; });
      th+='<a-text value="USC · E LINE" position="0 1.92 '+zz+'" rotation="0 '+(zz>0?0:180)+' 0" align="center" width="6.2" color="#2b3340"></a-text>';
    });
    [L/2,-L/2].forEach(function(ex){ var ry=ex>0?-90:90, en=(ex*0.99).toFixed(2);
      th+='<a-box position="'+ex+' 1.55 0" width="0.12" height="0.72" depth="1.3" material="shader: flat; color:#1f2730"></a-box>';
      th+='<a-box position="'+en+' 0.72 0.5" width="0.14" height="0.2" depth="0.22" material="shader: flat; color:#fff2b0"></a-box>';
      th+='<a-box position="'+en+' 0.72 -0.5" width="0.14" height="0.2" depth="0.22" material="shader: flat; color:#fff2b0"></a-box>';
      th+='<a-box position="'+(ex*0.985).toFixed(2)+' 2.0 0" width="0.06" height="0.36" depth="0.36" material="shader: flat; color:#d31f2b"></a-box>';
      th+='<a-text value="M" position="'+(ex*0.96).toFixed(2)+' 2.0 0" rotation="0 '+ry+' 0" align="center" width="1.7" color="#ffffff"></a-text>';
    });
    train.innerHTML=th; root.appendChild(train);

    // ===== extended quad: flanking buildings continue past the clock tower =====
    building(-12.3,-104,9,11,10,'#tex-facade1',BR); building(12.3,-104,9,12,10,'#tex-facade1',BR);
    building(-21,-110,12,16,11,'#tex-facade1',BR);  building(21,-112,12,17,11,'#tex-facade1',BR);
    for(var ez=-100; ez>=-118; ez-=9){ [-4.2,4.2].forEach(function(epx){
      var pm=makePalm(); pm.setAttribute('position', epx+' 0 '+ez); root.appendChild(pm);
      (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:epx,z:ez,r:0.55}); }); }
    for(var elz=-103; elz>=-117; elz-=14){ [-2.55,2.55].forEach(function(elx){
      var lp2=document.createElement('a-entity'); lp2.setAttribute('position', elx+' 0 '+elz);
      lp2.innerHTML='<a-cylinder radius="0.07" height="3.2" position="0 1.6 0" material="color:#2b2f37; roughness:1" shadow="cast: true"></a-cylinder>'+
        '<a-sphere radius="0.16" position="0 3.25 0" material="shader: flat; color:#ffe6a4"></a-sphere>'+
        '<a-sphere radius="0.36" position="0 3.25 0" material="shader: flat; color:#ffe6a4; transparent:true; opacity:0.22"></a-sphere>';
      root.appendChild(lp2); }); }

    // ===== champagne fountain plaza (Spoiled-Children satire) =====
    var fnt=document.createElement('a-entity'); fnt.setAttribute('position','0 0 -117'); (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:0,z:-117,r:2.0});
    fnt.innerHTML=
      '<a-cylinder radius="2.0" height="0.5" position="0 0.25 0" material="color:#cfc6b0; roughness:1" shadow="cast: true; receive: true"></a-cylinder>'+
      '<a-cylinder radius="1.82" height="0.16" position="0 0.5 0" material="shader: flat; color:#f4d35e"></a-cylinder>'+
      '<a-cylinder radius="0.5" height="1.2" position="0 0.9 0" material="color:#d8cfb6; roughness:1"></a-cylinder>'+
      '<a-cylinder radius="0.95" height="0.14" position="0 1.5 0" material="shader: flat; color:#f4d35e"></a-cylinder>'+
      '<a-cylinder radius="0.28" height="0.9" position="0 1.95 0" material="color:#d8cfb6; roughness:1"></a-cylinder>'+
      '<a-cylinder radius="0.5" height="0.12" position="0 2.45 0" material="shader: flat; color:#f4d35e"></a-cylinder>'+
      '<a-sphere radius="0.16" position="0 2.65 0" material="shader: flat; color:#fff3c4"></a-sphere>'+
      '<a-text value="CHAMPAGNE FOUNTAIN" position="0 0.42 2.04" align="center" width="3.7" color="#7a1f24"></a-text>';
    root.appendChild(fnt);

    // ===== grand library terminus — ENTERABLE (Doheny-inspired hall + campanile) =====
    var lib=document.createElement('a-entity'); lib.setAttribute('position','0 0 -130');
    // hollow shell: wall colliders with a door gap at front-center
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:0,z:-134.5,hw:9,hd:0.4});       // back wall
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:-9,z:-130,hw:0.4,hd:4.7});       // left wall
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:9,z:-130,hw:0.4,hd:4.7});        // right wall
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:-5.35,z:-125.5,hw:3.65,hd:0.4}); // front-left of door
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:5.35,z:-125.5,hw:3.65,hd:0.4});  // front-right of door
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:-11.5,z:-126.5,hw:2.2,hd:2.2});  // corner tower
    // interior furniture colliders
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:-3.5,z:-129,hw:1.3,hd:0.7});
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:3.5,z:-129,hw:1.3,hd:0.7});
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:0,z:-131,hw:1.3,hd:0.7});
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'r',x:-5,z:-126.6,hw:1.7,hd:0.6});
    (window.COLLIDERS=window.COLLIDERS||[]).push({t:'c',x:5,z:-132,r:0.55});
    var lh='';
    // floor + ceiling + roof cap
    lh+='<a-box position="0 0.03 0" width="17.4" height="0.06" depth="8.6" material="color:#6b4a2e; roughness:1" shadow="receive: true"></a-box>';
    lh+='<a-box position="0 9.05 0" width="18" height="0.4" depth="9" material="color:#cabf9e; roughness:1" shadow="cast: true"></a-box>';
    lh+='<a-box position="0 9.55 0" width="18.8" height="0.7" depth="9.8" material="color:#b5482f; roughness:1" shadow="cast: true"></a-box>';
    // hollow brick walls with a door gap at front-center
    lh+='<a-box position="-5.35 4.5 4.5" width="7.3" height="9" depth="0.5" material="src:#tex-facade1; repeat:2 3; roughness:1" shadow="cast: true; receive: true"></a-box>';
    lh+='<a-box position="5.35 4.5 4.5" width="7.3" height="9" depth="0.5" material="src:#tex-facade1; repeat:2 3; roughness:1" shadow="cast: true; receive: true"></a-box>';
    lh+='<a-box position="0 6.8 4.5" width="3.4" height="4.4" depth="0.5" material="src:#tex-facade1; repeat:1 1; roughness:1" shadow="cast: true"></a-box>';
    lh+='<a-box position="0 4.5 -4.5" width="18" height="9" depth="0.5" material="src:#tex-facade1; repeat:5 3; roughness:1" shadow="cast: true; receive: true"></a-box>';
    lh+='<a-box position="-9 4.5 0" width="0.5" height="9" depth="9" material="src:#tex-facade1; repeat:3 3; roughness:1" shadow="cast: true; receive: true"></a-box>';
    lh+='<a-box position="9 4.5 0" width="0.5" height="9" depth="9" material="src:#tex-facade1; repeat:3 3; roughness:1" shadow="cast: true; receive: true"></a-box>';
    // stone door portal trim
    lh+='<a-box position="-1.95 2.35 4.62" width="0.4" height="4.7" depth="0.5" material="color:#e7ddc0; roughness:1"></a-box>';
    lh+='<a-box position="1.95 2.35 4.62" width="0.4" height="4.7" depth="0.5" material="color:#e7ddc0; roughness:1"></a-box>';
    lh+='<a-box position="0 4.75 4.62" width="4.3" height="0.45" depth="0.5" material="color:#e7ddc0; roughness:1"></a-box>';
    // rose window + name above the door
    lh+='<a-circle position="0 6.95 4.78" radius="0.9" material="shader: flat; color:#f3ecd6"></a-circle>';
    lh+='<a-ring position="0 6.95 4.79" radius-inner="0.78" radius-outer="0.96" material="shader: flat; color:#7a1f24"></a-ring>';
    lh+='<a-box position="0 6.95 4.8" width="0.09" height="1.8" depth="0.02" material="shader: flat; color:#7a1f24"></a-box>';
    lh+='<a-box position="0 6.95 4.8" width="1.8" height="0.09" depth="0.02" material="shader: flat; color:#7a1f24"></a-box>';
    lh+='<a-text value="DOUGHENY LIBRARY" position="0 5.2 4.79" align="center" width="6.2" color="#5a4a2a"></a-text>';
    // exterior arched windows on the front segments
    [-6.2,-3.4,3.4,6.2].forEach(function(wx){ lh+='<a-box position="'+wx+' 4.7 4.76" width="1.1" height="3.2" depth="0.06" material="shader: flat; color:#39506e"></a-box>'+'<a-box position="'+wx+' 6.45 4.76" width="1.1" height="0.12" depth="0.06" material="shader: flat; color:#c9b27a"></a-box>'; });
    // interior side windows
    [-2.6,0,2.6].forEach(function(zz){ lh+='<a-box position="-8.72 4.6 '+zz+'" width="0.08" height="3.6" depth="1.3" material="shader: flat; color:#bcd6ee"></a-box>'+'<a-box position="8.72 4.6 '+zz+'" width="0.08" height="3.6" depth="1.3" material="shader: flat; color:#bcd6ee"></a-box>'; });
    // warm reading-room light
    lh+='<a-light type="point" position="0 7.4 0" intensity="0.55" distance="24" color="#ffe6bf"></a-light>';
    // corner campanile tower (moved out of the interior)
    lh+='<a-entity position="-11.5 0 3.5">'+
        '<a-box position="0 9 0" width="4.4" height="18" depth="4.4" material="src:#tex-facade1; repeat:1 5; roughness:1" shadow="cast: true; receive: true"></a-box>'+
        '<a-box position="0 18.3 0" width="4.9" height="0.7" depth="4.9" material="color:#c9b27a; roughness:1" shadow="cast: true"></a-box>'+
        '<a-box position="0 16.6 2.21" width="1.0" height="2.2" depth="0.1" material="shader: flat; color:#241f1a"></a-box>'+
        '<a-box position="0 16.6 -2.21" width="1.0" height="2.2" depth="0.1" material="shader: flat; color:#241f1a"></a-box>'+
        '<a-box position="2.21 16.6 0" width="0.1" height="2.2" depth="1.0" material="shader: flat; color:#241f1a"></a-box>'+
        '<a-box position="-2.21 16.6 0" width="0.1" height="2.2" depth="1.0" material="shader: flat; color:#241f1a"></a-box>'+
        '<a-cone position="0 20.5 0" radius-bottom="3.7" radius-top="0" height="4.0" material="color:#b5482f; roughness:1" shadow="cast: true"></a-cone>'+
        '<a-sphere position="0 22.8 0" radius="0.3" material="shader: flat; color:#ffcc33"></a-sphere>'+
      '</a-entity>';
    // ---- interior: bookshelf stacks ----
    function shelfHTML(){ var h='<a-box position="0 1.55 0" width="2.2" height="3.1" depth="0.5" material="color:#5a3a22; roughness:1" shadow="cast: true"></a-box>';
      for(var sy=0.55; sy<3.0; sy+=0.72){ h+='<a-box position="0 '+sy.toFixed(2)+' 0.16" width="2.0" height="0.06" depth="0.42" material="color:#6b4a2e"></a-box>';
        for(var bx=-0.9; bx<0.92; bx+=0.2){ var bc=['#7a1f24','#2f5e8c','#3a6e3e','#caa02e','#7a4ca0','#b5482f','#cfc6b0'][Math.floor(Math.random()*7)];
          h+='<a-box position="'+bx.toFixed(2)+' '+(sy+0.27).toFixed(2)+' 0.16" width="0.13" height="'+(0.4+Math.random()*0.12).toFixed(2)+'" depth="0.34" material="color:'+bc+'; roughness:1"></a-box>'; } }
      return h; }
    [-6,-3,0,3,6].forEach(function(sx){ lh+='<a-entity position="'+sx+' 0 -4.0">'+shelfHTML()+'</a-entity>'; });
    lh+='<a-entity position="-7.6 0 -1.5" rotation="0 90 0">'+shelfHTML()+'</a-entity>';
    lh+='<a-entity position="7.6 0 -1.5" rotation="0 -90 0">'+shelfHTML()+'</a-entity>';
    // ---- interior: study tables with green banker lamps ----
    function tableHTML(){ return '<a-box position="0 1.0 0" width="2.4" height="0.12" depth="1.2" material="color:#6b4a2e; roughness:1" shadow="cast: true"></a-box>'+
      '<a-box position="-1.0 0.5 -0.45" width="0.12" height="1.0" depth="0.12" material="color:#4a3018"></a-box>'+
      '<a-box position="1.0 0.5 -0.45" width="0.12" height="1.0" depth="0.12" material="color:#4a3018"></a-box>'+
      '<a-box position="-1.0 0.5 0.45" width="0.12" height="1.0" depth="0.12" material="color:#4a3018"></a-box>'+
      '<a-box position="1.0 0.5 0.45" width="0.12" height="1.0" depth="0.12" material="color:#4a3018"></a-box>'+
      '<a-box position="0.7 1.17 0" width="0.18" height="0.14" depth="0.18" material="color:#2a2a2a"></a-box>'+
      '<a-cylinder position="0.7 1.32 0" radius="0.02" height="0.2" material="color:#caa02e"></a-cylinder>'+
      '<a-sphere position="0.7 1.45 0" radius="0.14" scale="1 0.62 1" material="shader: flat; color:#2f7d5b; emissive:#2f7d5b; emissiveIntensity:0.45"></a-sphere>'+
      '<a-sphere position="0.7 1.4 0" radius="0.08" material="shader: flat; color:#fff6cf"></a-sphere>'; }
    [[-3.5,1.0],[3.5,1.0],[0,-1.0]].forEach(function(tp){ lh+='<a-entity position="'+tp[0]+' 0 '+tp[1]+'">'+tableHTML()+'</a-entity>'; });
    // checkout desk near the entrance
    lh+='<a-box position="-5 0.55 3.4" width="3.2" height="1.1" depth="0.9" material="color:#5a3a22; roughness:1" shadow="cast: true"></a-box>';
    lh+='<a-box position="-5 1.12 3.4" width="3.4" height="0.1" depth="1.1" material="color:#6b4a2e"></a-box>';
    // interior easter egg: a glowing golden book on a pedestal
    lh+='<a-box position="5 0.7 -2" width="0.7" height="1.4" depth="0.7" material="color:#cabf9e; roughness:1" shadow="cast: true"></a-box>';
    lh+='<a-box position="5 1.5 -2" rotation="-18 0 0" width="0.62" height="0.1" depth="0.86" material="color:#caa02e; emissive:#8a6512; emissiveIntensity:0.35; metalness:0.5; roughness:0.3" shadow="cast: true"></a-box>';
    lh+='<a-sphere position="5 1.62 -2" radius="0.5" material="shader: flat; color:#ffe9a0; transparent: true; opacity: 0.16; side: double"></a-sphere>';
    lh+='<a-text value="the real treasure was the all-nighters" position="5 2.2 -2" align="center" width="3.0" color="#7a6a3a"></a-text>';
    lib.innerHTML=lh; root.appendChild(lib);

    // ===== little hidden litter scattered on the lawns =====
    function litterPiece(){ var t=Math.floor(Math.random()*6);
      if(t===0) return '<a-cylinder radius="0.07" height="0.18" position="0 0.09 0" material="color:#f2efe6; roughness:1"></a-cylinder><a-cylinder radius="0.075" height="0.03" position="0 0.19 0" material="color:#b5482f; roughness:1"></a-cylinder>';
      if(t===1) return '<a-cylinder radius="0.05" height="0.16" position="0 0.05 0" rotation="0 0 90" material="color:#c0392b; metalness:0.4; roughness:0.5"></a-cylinder>';
      if(t===2) return '<a-box width="0.16" height="0.13" depth="0.16" position="0 0.07 0" rotation="'+(Math.random()*60).toFixed(0)+' '+(Math.random()*90).toFixed(0)+' '+(Math.random()*60).toFixed(0)+'" material="color:#f4f1e8; roughness:1"></a-box>';
      if(t===3) return '<a-box width="0.5" height="0.06" depth="0.5" position="0 0.03 0" material="color:#caa472; roughness:1"></a-box><a-box width="0.5" height="0.02" depth="0.5" position="0 0.08 0" material="color:#b58a52; roughness:1"></a-box>';
      if(t===4) return '<a-box width="0.34" height="0.07" depth="0.24" position="0 0.04 0" rotation="0 '+(Math.random()*90).toFixed(0)+' 0" material="color:'+['#3a5e8c','#7a1f24','#2f7d5b'][Math.floor(Math.random()*3)]+'; roughness:1"></a-box>';
      return '<a-cylinder radius="0.06" height="0.34" position="0 0.06 0" rotation="0 0 78" material="color:#2f4a32; roughness:0.5"></a-cylinder><a-cylinder radius="0.045" height="0.08" position="0.17 0.12 0" rotation="0 0 78" material="color:#e9c64a"></a-cylinder>'; }
    for(var li=0; li<32; li++){
      var lx2=(Math.random()<0.5?-1:1)*(4.8+Math.random()*9.6), lz2=4-Math.random()*122;
      var le=document.createElement('a-entity'); le.setAttribute('position', lx2.toFixed(2)+' 0 '+lz2.toFixed(2));
      le.setAttribute('rotation','0 '+(Math.random()*360).toFixed(0)+' 0'); le.innerHTML=litterPiece(); root.appendChild(le);
    }
    // hidden letter easter eggs tucked off the path
    [['fight on ✌','-15.5 0.02 -30','-90 0 18','#7a1f24',2.2],
     ['tuition: $98,000 / yr  (a steal!)','15.2 1.5 -52','0 -90 0','#5a4a2a',2.7],
     ['you actually got this','-2 0.02 -120','-90 0 0','#3a5e30',2.2],
     ['SC 4 LYFE','14.8 0.45 -104','0 -90 0','#8a0f1a',1.7],
     ['bury me in the stacks','-15 1.2 -96','0 90 0','#4a3a6a',2.2]
    ].forEach(function(Lr){ var te=document.createElement('a-entity'); te.setAttribute('position',Lr[1]); te.setAttribute('rotation',Lr[2]);
      te.innerHTML='<a-text value="'+Lr[0]+'" align="center" width="'+Lr[4]+'" color="'+Lr[3]+'"></a-text>'; root.appendChild(te); });

    // ===== a literal hidden golden easter egg (off the path, for the curious) =====
    var egg=document.createElement('a-entity'); egg.setAttribute('position','-7.6 0.62 -44');
    egg.setAttribute('animation__bob','property: position; to: -7.6 0.9 -44; dir: alternate; loop: true; dur: 1500; easing: easeInOutSine');
    egg.setAttribute('animation__spin','property: rotation; from: 0 0 0; to: 0 360 0; loop: true; dur: 6000; easing: linear');
    egg.innerHTML=
      '<a-sphere radius="0.34" scale="1 1.38 1" material="color:#f4d35e; metalness:0.55; roughness:0.22; emissive:#8a6512; emissiveIntensity:0.3" shadow="cast: true"></a-sphere>'+
      '<a-torus radius="0.31" radius-tubular="0.032" rotation="90 0 0" position="0 0.12 0" material="color:#c0392b; metalness:0.3; roughness:0.4"></a-torus>'+
      '<a-torus radius="0.33" radius-tubular="0.03" rotation="90 0 0" position="0 -0.08 0" material="color:#3a5e8c; roughness:0.5"></a-torus>'+
      '<a-sphere radius="0.045" position="0.17 0.3 0.18" material="shader: flat; color:#ffffff"></a-sphere>'+
      '<a-sphere radius="0.045" position="-0.19 0.16 0.16" material="shader: flat; color:#7fb8e6"></a-sphere>'+
      '<a-sphere radius="0.045" position="0.1 -0.16 0.22" material="shader: flat; color:#c0392b"></a-sphere>'+
      '<a-sphere radius="0.62" material="shader: flat; color:#ffe9a0; transparent: true; opacity: 0.15; side: double"></a-sphere>';
    root.appendChild(egg);

    var sc=this.el.sceneEl;
    setTimeout(function(){var r=sc.components.raycaster; if(r) r.refreshObjects();},700);
  }
});

AFRAME.registerComponent('thirdperson',{
  init:function(){
    var self=this;
    this.keys={}; this.yaw=0; this.pitch=-9; this.phase=0; this.amp=0; this.active=-1; this.lastStep=0;
    this.nearNpc=-1; this.talkingNpc=-1; this.eWas=false;
    this.promptEl=document.getElementById('prompt'); this.promptNameEl=document.getElementById('prompt-name'); this.promptName=undefined;
    var q=function(s){return self.el.querySelector(s).object3D;};
    this.legL=q('.legL'); this.legR=q('.legR'); this.armL=q('.armL'); this.armR=q('.armR');
    this.avatar=q('#avatar'); this.cam=q('#cam');
    this.UP=new THREE.Vector3(0,1,0);
    window.addEventListener('keydown',function(e){ self.keys[e.code]=true; });
    window.addEventListener('keyup',function(e){ self.keys[e.code]=false; });
    var down=false,lx=0,ly=0;
    function start(x,y){down=true;lx=x;ly=y;}
    function move(x,y){ if(!down)return; self.yaw-=(x-lx)*0.28; self.pitch=Math.max(-32,Math.min(8,self.pitch-(y-ly)*0.2)); lx=x;ly=y; }
    function end(){down=false;}
    this.el.sceneEl.addEventListener('loaded',function(){
      var cv=self.el.sceneEl.canvas;
      cv.addEventListener('mousedown',function(e){start(e.clientX,e.clientY);});
      window.addEventListener('mousemove',function(e){move(e.clientX,e.clientY);});
      window.addEventListener('mouseup',end);
      cv.addEventListener('touchstart',function(e){var t=e.touches[0];start(t.clientX,t.clientY);},{passive:true});
      window.addEventListener('touchmove',function(e){var t=e.touches[0];move(t.clientX,t.clientY);},{passive:true});
      window.addEventListener('touchend',end);
    });
  },
  endTalk:function(){ var NP=window.NPCS||[]; if(this.talkingNpc>=0 && NP[this.talkingNpc]) NP[this.talkingNpc].el.__talking=false; this.talkingNpc=-1; if(window.closeTalk) window.closeTalk(); },
  showPrompt:function(name){ var el=this.promptEl; if(!el)return;
    if(name){ if(this.promptName!==name){ this.promptName=name; if(this.promptNameEl) this.promptNameEl.textContent=name; } el.classList.add('show'); }
    else { this.promptName=null; el.classList.remove('show'); } },
  tick:function(t,dt){
    dt=Math.min(dt,50)/1000;
    var k=this.keys, d2r=THREE.MathUtils.degToRad;
    var fwd=0,str=0;
    if(k['KeyW']||k['ArrowUp'])fwd+=1;
    if(k['KeyS']||k['ArrowDown'])fwd-=1;
    if(k['KeyA']||k['ArrowLeft'])str-=1;
    if(k['KeyD']||k['ArrowRight'])str+=1;
    var run=k['ShiftLeft']||k['ShiftRight'];
    var moving=(fwd!==0||str!==0);
    var sp=(run?7.0:3.6);
    this.el.object3D.rotation.y=d2r(this.yaw);
    this.cam.rotation.x=d2r(this.pitch);
    if(moving){
      var v=new THREE.Vector3(str,0,-fwd); v.normalize();
      v.applyAxisAngle(this.UP, d2r(this.yaw));
      var p=this.el.object3D.position, C=window.COLLIDERS||[], PR=0.42;
      var blocked=function(x,z){ for(var i=0;i<C.length;i++){ var o=C[i];
        if(o.t==='r'){ if(Math.abs(x-o.x)<o.hw+PR && Math.abs(z-o.z)<o.hd+PR) return true; }
        else { var ddx=x-o.x, ddz=z-o.z, rr=o.r+PR; if(ddx*ddx+ddz*ddz<rr*rr) return true; } }
        var NPc=window.NPCS||[]; for(var ic=0;ic<NPc.length;ic++){ var ep=NPc[ic].el.object3D.position, cx=x-ep.x, cz=z-ep.z, cr=0.6+PR; if(cx*cx+cz*cz<cr*cr) return true; } return false; };
      var nx=p.x+v.x*sp*dt, nz=p.z+v.z*sp*dt;
      if(!blocked(nx,p.z)) p.x=nx;
      if(!blocked(p.x,nz)) p.z=nz;
      p.x=Math.max(-10.5,Math.min(10.5,p.x)); p.z=Math.max(-137,Math.min(13,p.z));
      var want=Math.atan2(-v.x,-v.z)-d2r(this.yaw);
      var cur=this.avatar.rotation.y, df=Math.atan2(Math.sin(want-cur),Math.cos(want-cur));
      this.avatar.rotation.y=cur+df*Math.min(1,dt*12);
    }
    var pos=this.el.object3D.position, SG=window.SIGNS||[], NP=window.NPCS||[];
    var talking=!!(window.isTalking && window.isTalking());
    // interact key (E / Space), edge-detected so one press = one action
    var ek=!!(this.keys['KeyE']||this.keys['Space']); var ePressed=ek&&!this.eWas; this.eWas=ek;
    // nearest classmate within reach
    var nn=-1, nbest=2.6*2.6;
    for(var jn=0;jn<NP.length;jn++){ var ex=NP[jn].el.object3D.position, ax=pos.x-ex.x, az=pos.z-ex.z, ad=ax*ax+az*az; if(ad<nbest){nbest=ad;nn=jn;} }
    this.nearNpc=nn;

    if(talking){
      // end the chat if you walk away from the person you're talking to
      var tn=this.talkingNpc;
      if(tn>=0 && NP[tn]){ var tp=NP[tn].el.object3D.position, wx=pos.x-tp.x, wz=pos.z-tp.z; if(wx*wx+wz*wz>4.5*4.5) this.endTalk(); }
      if(ePressed){ if(window.talkAdvance) window.talkAdvance(); if(!(window.isTalking && window.isTalking())) this.endTalk(); }
      this.showPrompt(null);
    } else {
      // walk up to a sign -> expand it + teach the lesson (only when not chatting)
      var near=-1, best=2.8*2.8;
      for(var i=0;i<SG.length;i++){ var ddx=pos.x-SG[i].x, ddz=pos.z-SG[i].z, dd=ddx*ddx+ddz*ddz; if(dd<best){best=dd;near=i;} }
      if(near!==this.active){
        if(this.active>=0 && SG[this.active]) SG[this.active].panel.setAttribute('animation__f','property: scale; to: 1 1 1; dur: 260; easing: easeOutQuad');
        this.active=near;
        if(near>=0){
          SG[near].panel.setAttribute('animation__f','property: scale; to: 1.55 1.55 1.55; dur: 320; easing: easeOutBack');
          window.openCard(SG[near].s);
          if(window.markLearned) window.markLearned(near);
        } else if(window.closeCard){ window.closeCard(); }
      }
      // classmate in reach -> show "Press E", open chat on press
      if(nn>=0){
        this.showPrompt(NP[nn].name);
        if(ePressed){
          if(this.active>=0 && SG[this.active]) SG[this.active].panel.setAttribute('animation__f','property: scale; to: 1 1 1; dur: 200; easing: easeOutQuad');
          this.active=-1;
          this.talkingNpc=nn; NP[nn].el.__talking=true;
          if(window.closeCard) window.closeCard();
          if(window.openTalk) window.openTalk(NP[nn]);
          this.showPrompt(null);
        }
      } else { this.showPrompt(null); }
    }
    var target=moving?(run?0.9:0.58):0;
    this.amp+=(target-this.amp)*Math.min(1,dt*9);
    this.phase+=dt*(run?15:10)*(moving?1:0);
    if(moving){ var stp=Math.floor(this.phase/Math.PI); if(stp!==this.lastStep){ this.lastStep=stp; if(window.SFX) window.SFX.step(); } }
    var s=Math.sin(this.phase)*this.amp;
    this.legL.rotation.x=s; this.legR.rotation.x=-s;
    this.armL.rotation.x=-s; this.armR.rotation.x=s;
    this.avatar.position.y=Math.abs(Math.sin(this.phase))*0.06*(this.amp/0.58||0);
  }
});

AFRAME.registerComponent('minimap',{
  init:function(){
    this.cv=document.getElementById('mapcv'); if(!this.cv)return;
    this.ctx=this.cv.getContext('2d');
    this.S=140; var dpr=Math.min(2,window.devicePixelRatio||1);
    this.cv.width=this.S*dpr; this.cv.height=this.S*dpr; this.ctx.scale(dpr,dpr);
    this.avatar=document.getElementById('avatar'); this.n=0;
  },
  tick:function(){
    if(!this.ctx)return; this.n++; if(this.n%3)return;
    var ctx=this.ctx, S=this.S, cx=S/2, cy=S/2, R=56, world=30, k=R/world, TAU=6.28318;
    var p=this.el.object3D.position, px=p.x, pz=p.z;
    var ry=this.el.object3D.rotation.y + (this.avatar?this.avatar.object3D.rotation.y:0);
    ctx.clearRect(0,0,S,S);
    ctx.strokeStyle='rgba(255,255,255,0.06)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.arc(cx,cy,R*0.5,0,TAU); ctx.stroke();
    var SG=window.SIGNS||[], learned=0, tot=SG.length, i;
    for(i=0;i<tot;i++){ if(SG[i].done) learned++;
      var dx=SG[i].x-px, dz=SG[i].z-pz, d=Math.hypot(dx,dz), mx,my,edge=false;
      if(d>world){ var a=Math.atan2(dz,dx); mx=cx+Math.cos(a)*(R-3); my=cy+Math.sin(a)*(R-3); edge=true; }
      else { mx=cx+dx*k; my=cy+dz*k; }
      ctx.beginPath(); ctx.arc(mx,my, edge?2:3.4, 0,TAU);
      if(SG[i].done){ ctx.fillStyle='#ffd24a'; ctx.fill(); }
      else { ctx.lineWidth=1.6; ctx.strokeStyle='#ffd24a'; ctx.stroke(); }
    }
    var NP=window.NPCS||[], j;
    for(j=0;j<NP.length;j++){ var ep=NP[j].el.object3D.position, ex=ep.x-px, ez=ep.z-pz;
      if(Math.hypot(ex,ez)>world) continue; ctx.beginPath(); ctx.arc(cx+ex*k, cy+ez*k, 2.3,0,TAU); ctx.fillStyle='#7fb8e6'; ctx.fill(); }
    ctx.save(); ctx.translate(cx,cy); ctx.rotate(-ry);
    ctx.beginPath(); ctx.moveTo(0,-7.5); ctx.lineTo(5,5.5); ctx.lineTo(0,2.5); ctx.lineTo(-5,5.5); ctx.closePath();
    ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
    ctx.lineWidth=3; ctx.strokeStyle='rgba(255,255,255,0.08)';
    ctx.beginPath(); ctx.arc(cx,cy,R+8,0,TAU); ctx.stroke();
    if(tot){ ctx.strokeStyle='#46c46e'; ctx.lineCap='round';
      ctx.beginPath(); ctx.arc(cx,cy,R+8, -Math.PI/2, -Math.PI/2 + TAU*(learned/tot)); ctx.stroke(); ctx.lineCap='butt'; }
  }
});

AFRAME.registerComponent('npc',{
  schema:{z0:{default:0},z1:{default:-60},speed:{default:1.4},dir:{default:-1}},
  init:function(){ this.dir=this.data.dir; this.t=Math.random()*6.28;
    this.legL=this.el.querySelector('.nlegL').object3D; this.legR=this.el.querySelector('.nlegR').object3D;
    this.armL=this.el.querySelector('.narmL').object3D; this.armR=this.el.querySelector('.narmR').object3D; },
  tick:function(t,dt){ dt=Math.min(dt,50)/1000; var p=this.el.object3D.position;
    if(this.el.__talking){ var rg=document.getElementById('rig');
      if(rg){ var rp=rg.object3D.position, dx=rp.x-p.x, dz=rp.z-p.z, want=Math.atan2(-dx,-dz),
        cu=this.el.object3D.rotation.y, dff=Math.atan2(Math.sin(want-cu),Math.cos(want-cu));
        this.el.object3D.rotation.y=cu+dff*Math.min(1,dt*9); }
      this.legL.rotation.x*=0.8; this.legR.rotation.x*=0.8; this.armL.rotation.x*=0.8; this.armR.rotation.x*=0.8;
      this.el.object3D.position.y=0; return; }
    p.z+=this.dir*this.data.speed*dt;
    if(p.z<this.data.z1){p.z=this.data.z1;this.dir=1;} if(p.z>this.data.z0){p.z=this.data.z0;this.dir=-1;}
    this.el.object3D.rotation.y=this.dir<0?0:Math.PI;
    this.t+=dt*9; var s=Math.sin(this.t)*0.5;
    this.legL.rotation.x=s;this.legR.rotation.x=-s;this.armL.rotation.x=-s;this.armR.rotation.x=s;
    this.el.object3D.position.y=Math.abs(Math.sin(this.t))*0.04; }
});
AFRAME.registerComponent('drift',{
  schema:{speed:{default:0.5},range:{default:66}},
  tick:function(t,dt){ var p=this.el.object3D.position; p.x+=this.data.speed*Math.min(dt,50)/1000; if(p.x>this.data.range)p.x=-this.data.range; }
});
AFRAME.registerComponent('bird',{
  schema:{cx:{default:0},cz:{default:-40},r:{default:28},h:{default:16},sp:{default:0.18},ph:{default:0}},
  init:function(){ this.t=this.data.ph; this.wL=this.el.querySelector('.wL').object3D; this.wR=this.el.querySelector('.wR').object3D; },
  tick:function(t,dt){ dt=Math.min(dt,50)/1000; this.t+=dt*this.data.sp*6.28; var a=this.t,p=this.el.object3D.position;
    p.x=this.data.cx+Math.cos(a)*this.data.r; p.z=this.data.cz+Math.sin(a)*this.data.r*0.72; p.y=this.data.h+Math.sin(a*2)*1.4;
    this.el.object3D.rotation.y=-a; var f=Math.sin(this.t*16)*0.7; this.wL.rotation.z=f; this.wR.rotation.z=-f; }
});
AFRAME.registerComponent('leaves',{
  schema:{count:{default:36}},
  init:function(){ this.rig=document.getElementById('rig'); this.items=[]; var cols=['#d98a2b','#c85a3a','#e0b94a','#b5612e','#8a9a3a','#cf7a2a'];
    for(var i=0;i<this.data.count;i++){ var l=document.createElement('a-plane'); l.setAttribute('width',0.17); l.setAttribute('height',0.21);
      l.setAttribute('material','shader: flat; side: double; transparent: true; opacity: 0.95; color: '+cols[i%cols.length]);
      this.el.appendChild(l); var it={o:l.object3D, sp:0.7+Math.random()*0.9, sw:Math.random()*6.28, swsp:1+Math.random()*2, vr:(Math.random()-0.5)*3.5};
      this.items.push(it); this.reset(it,true); } },
  reset:function(it,init){ var rx=0,rz=0; if(this.rig){rx=this.rig.object3D.position.x;rz=this.rig.object3D.position.z;}
    it.o.position.set(rx+(Math.random()*16-8), init?Math.random()*7:6+Math.random()*2.5, rz+(Math.random()*16-8));
    it.o.rotation.set(Math.random()*6.28,Math.random()*6.28,Math.random()*6.28); },
  tick:function(t,dt){ dt=Math.min(dt,50)/1000;
    for(var i=0;i<this.items.length;i++){ var it=this.items[i],o=it.o;
      o.position.y-=it.sp*dt; it.sw+=it.swsp*dt; o.position.x+=Math.sin(it.sw)*0.5*dt; o.rotation.z+=it.vr*dt; o.rotation.x+=it.vr*0.6*dt;
      if(o.position.y<0.12) this.reset(it,false); } }
});
</script>

<a-scene pixel-world shadow="type: pcfsoft"
         fog="type: exponential; color: #e7ddc8; density: 0.0085"
         cursor="rayOrigin: mouse" raycaster="objects: .clickable; far: 30"
         renderer="colorManagement: true; antialias: true; physicallyCorrectLights: true; toneMapping: ACESFilmic; exposure: 1.15; sortObjects: true">

  <a-assets>
    <img id="tex-sky"     src="__SKY__">
    <img id="tex-grass"   src="__GRASS__">
    <img id="tex-path"    src="__PATH__">
    <img id="tex-facade1" src="__FACADE1__">
    <img id="tex-facade2" src="__FACADE2__">
    <img id="tex-sign"    src="__SIGN__">
    <img id="tex-cloud"   src="__CLOUD__">
  </a-assets>

  <a-sky src="#tex-sky" animation="property: rotation; to: 0 360 0; loop: true; dur: 260000; easing: linear"></a-sky>

  <a-entity light="type: hemisphere; color: #eaf3ff; groundColor: #72794f; intensity: 0.92"></a-entity>
  <a-entity light="type: directional; color: #acc4ff; intensity: 0.35" position="-14 10 -18"></a-entity>
  <a-entity light="type: directional; color: #ffe6bc; intensity: 1.35; castShadow: true;
                   shadowMapWidth: 2048; shadowMapHeight: 2048;
                   shadowCameraLeft: -30; shadowCameraRight: 30; shadowCameraTop: 30; shadowCameraBottom: -30; shadowCameraFar: 120"
            position="14 22 8"></a-entity>

  <a-plane position="0 0 -40" rotation="-90 0 0" width="150" height="240"
           material="src: #tex-grass; repeat: 30 48; roughness: 1" shadow="receive: true"></a-plane>
  <a-plane position="0 0.02 -40" rotation="-90 0 0" width="4.4" height="240"
           material="src: #tex-path; repeat: 2 60; roughness: 1" shadow="receive: true"></a-plane>

  <a-entity campus></a-entity>
  <a-entity leaves></a-entity>

  <a-entity id="rig" position="0 0 9" thirdperson minimap>
    <a-entity id="avatar">
      <a-entity class="legL" position="-0.17 0.82 0">
        <a-box position="0 -0.38 0" width="0.28" height="0.76" depth="0.3" material="color:#3b4250; roughness:1" shadow="cast: true"></a-box>
        <a-box position="0 -0.8 0.06" width="0.3" height="0.16" depth="0.42" material="color:#f2f2ee; roughness:1" shadow="cast: true"></a-box>
      </a-entity>
      <a-entity class="legR" position="0.17 0.82 0">
        <a-box position="0 -0.38 0" width="0.28" height="0.76" depth="0.3" material="color:#3b4250; roughness:1" shadow="cast: true"></a-box>
        <a-box position="0 -0.8 0.06" width="0.3" height="0.16" depth="0.42" material="color:#f2f2ee; roughness:1" shadow="cast: true"></a-box>
      </a-entity>
      <a-box position="0 1.28 0" width="0.66" height="0.94" depth="0.38" material="color:#2b3f73; roughness:1" shadow="cast: true"></a-box>
      <a-box position="-0.18 1.42 -0.2" width="0.07" height="0.62" depth="0.05" material="color:#9c2f3c; roughness:1"></a-box>
      <a-box position="0.18 1.42 -0.2" width="0.07" height="0.62" depth="0.05" material="color:#9c2f3c; roughness:1"></a-box>
      <a-box position="0 1.34 0.28" width="0.58" height="0.8" depth="0.22" material="color:#b23a48; roughness:1" shadow="cast: true"></a-box>
      <a-box position="0 1.52 0.4" width="0.34" height="0.32" depth="0.04" material="color:#9c2f3c; roughness:1"></a-box>
      <a-entity class="armL" position="-0.48 1.68 0">
        <a-box position="0 -0.36 0" width="0.22" height="0.72" depth="0.26" material="color:#2b3f73; roughness:1" shadow="cast: true"></a-box>
        <a-box position="0 -0.79 0" width="0.2" height="0.2" depth="0.24" material="color:#f4c542; roughness:1" shadow="cast: true"></a-box>
      </a-entity>
      <a-entity class="armR" position="0.48 1.68 0">
        <a-box position="0 -0.36 0" width="0.22" height="0.72" depth="0.26" material="color:#2b3f73; roughness:1" shadow="cast: true"></a-box>
        <a-box position="0 -0.79 0" width="0.2" height="0.2" depth="0.24" material="color:#f4c542; roughness:1" shadow="cast: true"></a-box>
      </a-entity>
      <a-box position="0 2.04 0" width="0.54" height="0.52" depth="0.52" material="color:#f4c542; roughness:1" shadow="cast: true"></a-box>
      <a-box position="0 2.345 0.02" width="0.58" height="0.2" depth="0.56" material="color:#23356a; roughness:1" shadow="cast: true"></a-box>
      <a-box position="0 2.3 -0.38" width="0.5" height="0.07" depth="0.22" material="color:#1b294f; roughness:1" shadow="cast: true"></a-box>
      <!-- face: eyes (white + pupil + glint), brows, smile, cheeks -->
      <a-box position="-0.115 2.07 -0.262" width="0.15" height="0.16" depth="0.02" material="shader: flat; color:#ffffff"></a-box>
      <a-box position="0.115 2.07 -0.262" width="0.15" height="0.16" depth="0.02" material="shader: flat; color:#ffffff"></a-box>
      <a-box position="-0.115 2.05 -0.272" width="0.08" height="0.10" depth="0.02" material="shader: flat; color:#20242c"></a-box>
      <a-box position="0.115 2.05 -0.272" width="0.08" height="0.10" depth="0.02" material="shader: flat; color:#20242c"></a-box>
      <a-box position="-0.14 2.09 -0.276" width="0.03" height="0.03" depth="0.02" material="shader: flat; color:#ffffff"></a-box>
      <a-box position="0.09 2.09 -0.276" width="0.03" height="0.03" depth="0.02" material="shader: flat; color:#ffffff"></a-box>
      <a-box position="-0.115 2.18 -0.262" width="0.15" height="0.035" depth="0.02" material="shader: flat; color:#3a2a1a"></a-box>
      <a-box position="0.115 2.18 -0.262" width="0.15" height="0.035" depth="0.02" material="shader: flat; color:#3a2a1a"></a-box>
      <a-box position="0 1.93 -0.262" width="0.2" height="0.035" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>
      <a-box position="-0.12 1.955 -0.262" width="0.06" height="0.035" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>
      <a-box position="0.12 1.955 -0.262" width="0.06" height="0.035" depth="0.02" material="shader: flat; color:#6a3b2a"></a-box>
      <a-box position="-0.205 2.0 -0.252" width="0.07" height="0.06" depth="0.02" material="shader: flat; color:#ef9a86"></a-box>
      <a-box position="0.205 2.0 -0.252" width="0.07" height="0.06" depth="0.02" material="shader: flat; color:#ef9a86"></a-box>
      <!-- ears -->
      <a-box position="-0.285 2.0 -0.02" width="0.06" height="0.16" depth="0.14" material="color:#f4c542; roughness:1"></a-box>
      <a-box position="0.285 2.0 -0.02" width="0.06" height="0.16" depth="0.14" material="color:#f4c542; roughness:1"></a-box>
      <!-- brown hair: fringe, sideburns, back -->
      <a-box position="0 2.2 -0.235" width="0.48" height="0.085" depth="0.07" material="color:#4a3526; roughness:1"></a-box>
      <a-box position="-0.265 2.05 -0.04" width="0.05" height="0.2" depth="0.2" material="color:#4a3526; roughness:1"></a-box>
      <a-box position="0.265 2.05 -0.04" width="0.05" height="0.2" depth="0.2" material="color:#4a3526; roughness:1"></a-box>
      <a-box position="0 2.12 0.265" width="0.5" height="0.2" depth="0.06" material="color:#4a3526; roughness:1" shadow="cast: true"></a-box>
      <!-- hoodie hood (down, on back) -->
      <a-box position="0 1.8 0.2" width="0.52" height="0.28" depth="0.16" material="color:#23356a; roughness:1" shadow="cast: true"></a-box>
      <!-- backpack on back + straps over the chest -->
      <a-box position="0 1.34 0.36" width="0.5" height="0.66" depth="0.22" material="color:#c0392b; roughness:1" shadow="cast: true"></a-box>
      <a-box position="0 1.5 0.48" width="0.4" height="0.26" depth="0.05" material="color:#a52f24; roughness:1"></a-box>
      <a-box position="0 1.62 0.5" width="0.42" height="0.04" depth="0.04" material="color:#7e221a; roughness:1"></a-box>
      <a-box position="0 1.7 0.36" width="0.12" height="0.07" depth="0.07" material="color:#7e221a; roughness:1"></a-box>
      <a-box position="-0.18 1.45 -0.22" width="0.07" height="0.62" depth="0.05" material="color:#7e221a; roughness:1"></a-box>
      <a-box position="0.18 1.45 -0.22" width="0.07" height="0.62" depth="0.05" material="color:#7e221a; roughness:1"></a-box>
      <!-- kangaroo pocket -->
      <a-box position="0 1.08 -0.205" width="0.36" height="0.22" depth="0.05" material="color:#243a6b; roughness:1"></a-box>
      <!-- lanyard + ID badge -->
      <a-box position="-0.11 1.62 -0.2" width="0.03" height="0.34" depth="0.03" material="color:#c23b4a; roughness:1"></a-box>
      <a-box position="0.11 1.62 -0.2" width="0.03" height="0.34" depth="0.03" material="color:#c23b4a; roughness:1"></a-box>
      <a-box position="0 1.42 -0.225" width="0.14" height="0.18" depth="0.02" material="color:#f7f7f2; roughness:1" shadow="cast: true"></a-box>
      <a-box position="0 1.47 -0.232" width="0.14" height="0.05" depth="0.01" material="shader: flat; color:#c0392b"></a-box>
    </a-entity>
    <a-entity id="cam" camera position="0 2.8 5.6" rotation="-10 0 0"></a-entity>
  </a-entity>

</a-scene>
</body>
</html>'''

for k,v in [('__STRAT__',json.dumps(D['STRATEGIES'])),('__CATS__',json.dumps(D['CATS'])),
            ('__SKY__',T['sky']),('__GRASS__',T['grass']),('__PATH__',T['path']),
            ('__FACADE1__',T['facade1']),('__FACADE2__',T['facade2']),('__SIGN__',T['sign']),('__CLOUD__',T['cloud'])]:
    HTML=HTML.replace(k,v)
open(os.path.join(HERE,'..','index.html'),'w').write(HTML)
print("written",len(HTML)//1024,"KB")
