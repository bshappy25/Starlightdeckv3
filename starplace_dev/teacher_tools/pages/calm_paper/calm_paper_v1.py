<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Calm Paper — STARPLACE (Base + Packs)</title>

<style>
  :root{
    --text:#eaf2ff;
    --muted:#b8c7e6;

    --ui: rgba(10,14,24,0.86);
    --ui2: rgba(7,10,18,0.62);
    --border: rgba(160,190,255,0.22);

    --neonA:#58f7ff;
    --neonB:#c77dff;
    --neonC:#66ff99;
    --warn:#ffd166;

    --shadowDeep: 0 24px 70px rgba(0,0,0,0.62);

    /* Base paper palette (more varied, still calm) */
    --p1:#fbf7ef; /* ivory */
    --p2:#eef2ff; /* lavender mist */
    --p3:#eaf7f1; /* mint fog */
    --p4:#fff1e6; /* peach veil */
    --p5:#f1f5f9; /* cool slate */
    --p6:#f7efff; /* lilac */
    --p7:#fff7d6; /* butter */
    --p8:#e9f3ff; /* sky */

    --paperColor: var(--p1);

    --safeTop: env(safe-area-inset-top);
    --safeBot: env(safe-area-inset-bottom);

    --tabH: 56px;
    --panelMax: 310px;

    /* Stage padding: maximize paper height */
    --stagePadTop: calc(10px + var(--safeTop));
    --stagePadBot: calc(var(--tabH) + 14px + var(--safeBot));
  }

  *{box-sizing:border-box}
  html,body{height:100%}

  body{
    margin:0;
    background:#050814;
    color:var(--text);
    overflow:hidden;
    /* Script writing feel */
    font-family: "Snell Roundhand","Apple Chancery","Segoe Script","Brush Script MT","Comic Sans MS",cursive;

    /* Wand cursor (SVG data URL) */
    cursor: url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'>\
<defs>\
  <linearGradient id='wood' x1='0' y1='0' x2='1' y2='1'>\
    <stop offset='0' stop-color='%238b5a2b'/>\
    <stop offset='0.5' stop-color='%236b3f1f'/>\
    <stop offset='1' stop-color='%239a6a3a'/>\
  </linearGradient>\
  <radialGradient id='gem' cx='50%25' cy='50%25' r='60%25'>\
    <stop offset='0' stop-color='%23ffffff' stop-opacity='0.9'/>\
    <stop offset='0.35' stop-color='%2358f7ff' stop-opacity='0.9'/>\
    <stop offset='1' stop-color='%23c77dff' stop-opacity='0.9'/>\
  </radialGradient>\
</defs>\
<path d='M10 52 L52 10' stroke='url(%23wood)' stroke-width='6' stroke-linecap='round'/>\
<path d='M14 56 L56 14' stroke='%23000000' stroke-opacity='0.25' stroke-width='2' stroke-linecap='round'/>\
<circle cx='54' cy='12' r='6' fill='url(%23gem)' stroke='%23ffffff' stroke-opacity='0.35' stroke-width='1.2'/>\
</svg>") 6 58, auto;
  }

  /* Wood table background (always visible) */
  .wood{
    position:fixed; inset:0;
    background:
      radial-gradient(1200px 700px at 20% 0%, rgba(255,255,255,0.10), transparent 58%),
      radial-gradient(900px 600px at 90% 15%, rgba(0,0,0,0.26), transparent 62%),
      repeating-linear-gradient(90deg,
        rgba(0,0,0,0.08) 0px,
        rgba(0,0,0,0.00) 12px,
        rgba(255,255,255,0.040) 22px,
        rgba(0,0,0,0.00) 34px
      ),
      linear-gradient(135deg, #5e3f27, #7b5636 45%, #4b2f1b);
  }

  /* CRT overlay */
  .crt::before{
    content:"";
    position:fixed; inset:0;
    pointer-events:none;
    background: repeating-linear-gradient(
      to bottom,
      rgba(0,0,0,0.22) 0px,
      rgba(0,0,0,0.22) 1px,
      rgba(0,0,0,0.0) 2px,
      rgba(0,0,0,0.0) 4px
    );
    opacity: 0.26;
    mix-blend-mode: multiply;
  }
  .crt::after{
    content:"";
    position:fixed; inset:0;
    pointer-events:none;
    background: radial-gradient(900px 600px at 50% 35%, rgba(255,255,255,0.08), transparent 60%);
    opacity: 0.48;
  }

  /* Wand glow follower */
  #wandGlow, #wandTrail{
    position: fixed;
    border-radius: 999px;
    pointer-events:none;
    transform: translate(-50%, -50%);
    z-index: 9999;
  }
  #wandGlow{
    width: 18px; height: 18px;
    background: radial-gradient(circle at 35% 35%,
      rgba(255,255,255,0.95),
      rgba(88,247,255,0.55) 35%,
      rgba(199,125,255,0.25) 65%,
      rgba(0,0,0,0) 72%);
    opacity: 0.95;
  }
  #wandTrail{
    width: 44px; height: 44px;
    background: radial-gradient(circle at 50% 50%,
      rgba(88,247,255,0.18),
      rgba(199,125,255,0.08) 45%,
      rgba(0,0,0,0) 70%);
    opacity: 0.55;
    z-index: 9998;
  }

  /* Forced full stage */
  .paperStage{
    position:fixed; inset:0;
    padding: var(--stagePadTop) 10px var(--stagePadBot);
    display:grid;
    place-items:center;
  }

  .paperFrame{
    position:relative;
    width: min(1040px, 100%);
    height: 100%;
    border-radius: 26px;
    overflow:hidden;
    box-shadow:
      0 0 0 2px rgba(88,247,255,0.14),
      0 0 0 6px rgba(199,125,255,0.10),
      0 24px 70px rgba(0,0,0,0.58);
    transform: rotate(-0.10deg);
    background: rgba(255,255,255,0.03);
  }

  /* shimmer sweep */
  .paperFrame::before{
    content:"";
    position:absolute; inset:-40%;
    background: linear-gradient(120deg, transparent 42%, rgba(88,247,255,0.12) 50%, transparent 58%);
    transform: translateX(-45%) rotate(10deg);
    animation: sweep 6.5s ease-in-out infinite;
    pointer-events:none;
    opacity: 0.55;
  }
  @keyframes sweep{
    0%{ transform: translateX(-48%) rotate(10deg); }
    50%{ transform: translateX(12%) rotate(10deg); }
    100%{ transform: translateX(-48%) rotate(10deg); }
  }

  .paper{
    position:absolute; inset:0;
    background: var(--paperColor);
    transition: background 160ms ease;
  }

  /* Texture layer (can be swapped to image textures later) */
  .paper::before{
    content:"";
    position:absolute; inset:0;
    background:
      radial-gradient(1100px 900px at 10% 0%, rgba(255,255,255,0.22), transparent 60%),
      radial-gradient(900px 700px at 100% 35%, rgba(0,0,0,0.10), transparent 60%),
      repeating-linear-gradient(0deg,
        rgba(0,0,0,0.020) 0px,
        rgba(0,0,0,0.000) 6px
      );
    opacity: 0.62;
    pointer-events:none;
    mix-blend-mode: multiply;
  }

  /* Optional: texture image overlay (future packs) */
  .paper.hasTexture::after{
    content:"";
    position:absolute; inset:0;
    background-image: var(--paperTexture, none);
    background-size: cover;
    background-position: center;
    opacity: 0.22;
    mix-blend-mode: multiply;
    pointer-events:none;
  }

  /* Paper types */
  .paper.postit{ border-radius: 16px; }
  .paper.postit::before{ opacity: 0.55; }
  .paper.postit::after{
    content:"";
    position:absolute; top:0; left:0; right:0; height: 58px;
    background: linear-gradient(180deg, rgba(0,0,0,0.10), rgba(0,0,0,0.00));
    opacity: 0.28;
    pointer-events:none;
  }

  .paper.note::after{
    content:"";
    position:absolute; inset:0;
    background:
      repeating-linear-gradient(to bottom,
        rgba(17,24,39,0.00) 0px,
        rgba(17,24,39,0.00) 26px,
        rgba(17,24,39,0.12) 27px,
        rgba(17,24,39,0.00) 28px
      ),
      linear-gradient(to right, rgba(239,68,68,0.16), rgba(239,68,68,0.16));
    background-size: auto, 2px 100%;
    background-position: 0 0, 78px 0;
    background-repeat: repeat, no-repeat;
    opacity: 0.44;
    pointer-events:none;
  }

  .paper.book{
    background:
      linear-gradient(135deg, rgba(0,0,0,0.06), rgba(0,0,0,0.00) 40%),
      var(--paperColor);
  }
  .paper.book::after{
    content:"";
    position:absolute; left:0; top:0; bottom:0; width: 22%;
    background: linear-gradient(90deg, rgba(0,0,0,0.16), rgba(0,0,0,0.02));
    opacity: 0.55;
    pointer-events:none;
  }

  /* Cute stamps */
  .stamps{ position:absolute; inset:0; pointer-events:none; }
  .stamp{
    position:absolute;
    padding: 8px 10px;
    border-radius: 14px;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
    box-shadow: 0 12px 24px rgba(0,0,0,0.22);
    opacity: 0.88;
    z-index: 7;
  }
  .stamp.star{ top: 14px; left: 14px; transform: rotate(7deg);
    background: rgba(255,255,255,0.58); border: 1px dashed rgba(0,0,0,0.18); color:#111827; }
  .stamp.heart{ top: 14px; right: 14px; transform: rotate(-7deg);
    background: rgba(255,255,255,0.58); border: 1px dashed rgba(0,0,0,0.18); color:#111827; }
  .stamp.mode{ bottom: 14px; left: 14px; transform: rotate(-3deg);
    background: rgba(255,255,255,0.50); border: 1px dashed rgba(0,0,0,0.18); color:#111827; opacity:0.84; }

  .stamp.pack{ bottom: 14px; right: 14px; transform: rotate(2deg);
    background: rgba(255,255,255,0.50); border: 1px dashed rgba(0,0,0,0.18); color:#111827; opacity:0.84; }

  .stamp.level{
    left: 50%;
    top: 46%;
    transform: translate(-50%,-50%) rotate(-12deg) scale(0.7);
    background: rgba(255,255,255,0.66);
    border: 2px solid rgba(0,0,0,0.18);
    color:#111827;
    opacity: 0.0;
    transition: opacity 160ms ease, transform 160ms ease;
    z-index: 9;
    pointer-events:none;
  }
  .stamp.level.show{
    opacity: 0.92;
    transform: translate(-50%,-50%) rotate(-12deg) scale(1.0);
  }

  /* Sparkle canvas */
  #sparkCanvas{
    position:absolute; inset:0;
    pointer-events:none;
    z-index: 8;
  }

  /* Text overlay */
  .boxes{
    position:absolute; inset:0;
    padding: 28px 24px 68px; /* extra bottom space for long writing */
    display:grid;
    gap: 14px;
    z-index: 6;
  }

  textarea, input[type="text"]{
    width:100%;
    border-radius: 18px;
    border: 1px solid rgba(0,0,0,0.18);
    background: rgba(255,255,255,0.56);
    outline:none;
    padding: 14px 14px;
    color:#111827;
    resize:none;
    box-shadow: 0 12px 20px rgba(0,0,0,0.16);
    font-family: inherit;
    font-size: clamp(1.05rem, 2.1vw, 1.45rem);
  }
  textarea:focus, input[type="text"]:focus{
    border-color: rgba(88,247,255,0.52);
    box-shadow: 0 0 0 4px rgba(88,247,255,0.16), 0 12px 20px rgba(0,0,0,0.16);
  }

  /* Layouts */
  .layout-postit .boxes{ grid-template-rows: 1fr 1fr 1fr; }
  .layout-note .boxes{ grid-template-rows: auto 1fr auto; }
  .layout-book .boxes{ grid-template-rows: 1fr auto auto; align-content: center; }
  .layout-book input[type="text"]{ text-align:center; }
  .layout-blank .boxes{ grid-template-rows: 1fr; }

  /* Hint bar */
  .hint{
    position:absolute;
    bottom: 12px; left: 14px; right:14px;
    display:flex; justify-content:space-between; gap:10px;
    pointer-events:none;
    color: rgba(8,10,18,0.62);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    font-size: 0.80rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
    z-index: 6;
  }

  /* ===== Dock ===== */
  .dock{
    position:fixed;
    left: 10px;
    right: 10px;
    bottom: calc(10px + var(--safeBot));
    z-index: 40;
    pointer-events: none;
  }
  @media (min-width: 1100px){
    .dock{ left: 50%; right: auto; transform: translateX(-50%); width: 1100px; }
  }

  .dockPanel{
    pointer-events: auto;
    border-radius: 22px;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, var(--ui), rgba(8,10,18,0.78));
    box-shadow: var(--shadowDeep);
    backdrop-filter: blur(12px);
    overflow:hidden;
    max-height: 0px;
    opacity: 0;
    transform: translateY(8px);
    transition: max-height 200ms ease, opacity 180ms ease, transform 180ms ease;
    margin-bottom: 10px;
  }
  .dockPanel.open{
    max-height: var(--panelMax);
    opacity: 1;
    transform: translateY(0px);
  }

  .panelInner{
    padding: 12px;
    display:grid;
    gap: 10px;
  }

  .block{
    border-radius: 18px;
    border: 1px solid rgba(160,190,255,0.18);
    background: rgba(7,10,18,0.46);
    padding: 10px;
  }

  .labelTiny{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    font-size: 0.72rem;
    color: #cfe2ff;
    opacity: 0.95;
    margin-bottom: 6px;
  }

  .sel{
    width: 100%;
    min-width: 0;
    padding: 10px 10px;
    border-radius: 16px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(7,10,18,0.55);
    color: var(--text);
    outline:none;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }

  .chips{
    display:flex; gap:8px; align-items:center; flex-wrap:wrap;
  }
  .chip{
    width: 30px; height: 30px;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.18);
    box-shadow: 0 10px 18px rgba(0,0,0,0.35);
    cursor:pointer;
    position: relative;
    overflow:hidden;
    flex: 0 0 auto;
  }
  .chip[aria-pressed="true"]{ outline: 3px solid rgba(88,247,255,0.35); }
  .chip::after{
    content:"";
    position:absolute; inset:0;
    background: radial-gradient(80px 28px at 20% 0%, rgba(255,255,255,0.28), transparent 60%);
    pointer-events:none;
  }

  .tog{
    display:flex; align-items:center; gap:10px;
    padding: 10px 10px;
    border-radius: 16px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(7,10,18,0.45);
    min-width:0;
  }
  .tog small{
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    color: var(--muted);
    font-weight: 700;
    line-height: 1.1rem;
  }
  input[type="checkbox"]{ transform: scale(1.2); accent-color: var(--neonA); }

  .btnRow{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .btn{
    padding: 12px 10px;
    border-radius: 18px;
    border: 1px solid rgba(160,190,255,0.22);
    background: linear-gradient(180deg, rgba(14,18,34,0.92), rgba(8,10,18,0.88));
    color: var(--text);
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    cursor:pointer;
    transition: transform 120ms ease, filter 120ms ease;
    user-select:none;
    -webkit-tap-highlight-color: transparent;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .btn:active{ transform: translateY(1px) scale(0.995); }
  .btn.primary{ border-color: rgba(88,247,255,0.38); }
  .btn.warn{ border-color: rgba(255,209,102,0.45); }
  .btn.good{ border-color: rgba(102,255,153,0.30); }

  .tabBar{
    pointer-events: auto;
    height: var(--tabH);
    border-radius: 22px;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, var(--ui), rgba(8,10,18,0.78));
    box-shadow: var(--shadowDeep);
    backdrop-filter: blur(12px);
    display:grid;
    grid-template-columns: repeat(5, 1fr);
    overflow:hidden;
  }
  .tab{
    border:0;
    background: transparent;
    color: rgba(234,242,255,0.92);
    font-weight: 1000;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.76rem;
    cursor:pointer;
    position:relative;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .tab:hover{ background: rgba(255,255,255,0.04); }
  .tab[aria-selected="true"]{
    background: rgba(88,247,255,0.08);
    color: #eaffff;
  }
  .tab[aria-selected="true"]::after{
    content:"";
    position:absolute;
    left: 16px; right: 16px;
    bottom: 8px;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(88,247,255,0.85), rgba(199,125,255,0.75));
    box-shadow: 0 0 18px rgba(88,247,255,0.22);
  }

  /* Toast */
  .toast{
    position: fixed;
    left: 50%;
    bottom: calc(var(--tabH) + 22px + var(--safeBot));
    transform: translateX(-50%);
    padding: 10px 12px;
    border-radius: 16px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(10,14,24,0.90);
    color: var(--text);
    font-weight: 900;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    box-shadow: 0 18px 40px rgba(0,0,0,0.55);
    opacity: 0;
    pointer-events:none;
    transition: opacity 180ms ease, transform 180ms ease;
    z-index: 60;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .toast.show{ opacity:1; transform: translateX(-50%) translateY(-2px); }

  /* Splash */
  .splash{
    position:fixed; inset:0;
    display:grid; place-items:center;
    background:
      radial-gradient(900px 600px at 50% 35%, rgba(88,247,255,0.12), transparent 60%),
      radial-gradient(900px 600px at 20% 15%, rgba(199,125,255,0.10), transparent 55%),
      linear-gradient(180deg, rgba(5,8,20,0.96), rgba(0,0,0,0.86));
    z-index: 80;
  }
  .sCard{
    width:min(760px, 92vw);
    border-radius: 22px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(10,14,24,0.78);
    box-shadow: 0 22px 70px rgba(0,0,0,0.60);
    padding: 18px;
  }
  .logo{
    font-weight: 1000;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 1.05rem;
    margin: 0 0 8px 0;
    text-shadow: 0 0 18px rgba(88,247,255,0.20);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .sSmall{
    color: var(--muted);
    font-size:0.95rem;
    line-height:1.35rem;
    margin:0 0 12px;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }
  .meter{
    height: 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(160,190,255,0.18);
    overflow:hidden;
    margin: 12px 0 10px;
  }
  .meter > div{
    height:100%;
    width:0%;
    background: linear-gradient(90deg, rgba(88,247,255,0.75), rgba(199,125,255,0.65), rgba(102,255,153,0.55));
    animation: load 1.05s ease-out forwards;
  }
  @keyframes load{ to{ width: 100%; } }
  .sBtn{
    width:100%;
    padding: 12px 12px;
    border-radius: 18px;
    border: 1px solid rgba(88,247,255,0.38);
    background: linear-gradient(180deg, rgba(15,22,44,0.92), rgba(8,10,18,0.88));
    color: var(--text);
    font-weight: 1000;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    cursor:pointer;
    box-shadow: 0 0 0 5px rgba(88,247,255,0.10), 0 18px 40px rgba(0,0,0,0.55);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .hidden{ display:none !important; }

  /* ===== Full View Overlay ===== */
  .fullOverlay{
    position: fixed;
    inset: 0;
    z-index: 200;
    background:
      radial-gradient(900px 600px at 50% 35%, rgba(88,247,255,0.10), transparent 60%),
      radial-gradient(900px 600px at 20% 15%, rgba(199,125,255,0.08), transparent 55%),
      rgba(0,0,0,0.72);
    backdrop-filter: blur(10px);
    display: none;
  }
  .fullOverlay.show{ display:block; }

  .fullCard{
    position:absolute;
    inset: calc(10px + var(--safeTop)) 10px calc(10px + var(--safeBot));
    border-radius: 26px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(10,14,24,0.65);
    box-shadow: 0 28px 90px rgba(0,0,0,0.70);
    overflow:hidden;
  }
  .fullTopbar{
    height: 56px;
    display:flex;
    align-items:center;
    justify-content: space-between;
    padding: 10px 12px;
    border-bottom: 1px solid rgba(160,190,255,0.18);
    background: linear-gradient(180deg, rgba(10,14,24,0.86), rgba(10,14,24,0.55));
  }
  .fullTitle{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
    font-weight: 1000;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.78rem;
    color: rgba(234,242,255,0.95);
  }
  .fullBtns{ display:flex; gap: 8px; align-items:center; }
  .miniBtn{
    padding: 10px 12px;
    border-radius: 16px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(7,10,18,0.55);
    color: rgba(234,242,255,0.95);
    font-weight: 1000;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.72rem;
    cursor:pointer;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
  }
  .miniBtn.primary{
    border-color: rgba(88,247,255,0.38);
    background: rgba(88,247,255,0.10);
  }
  .fullBody{
    position:absolute;
    left:0; right:0;
    top:56px; bottom:0;
    padding: 10px;
    display:grid;
    place-items:center;
  }
  .fullBody .paperFrame{
    width: min(1280px, 100%);
    height: 100%;
    transform: rotate(-0.06deg);
  }

  /* Screenshot Mode hides UI chrome */
  body.screenshotMode .dock,
  body.screenshotMode #toast{
    display:none !important;
  }
  body.screenshotMode .hint{
    opacity: 0 !important;
  }

  /* Screenshot tip */
  .shotTip{
    position:fixed;
    inset: 0;
    z-index: 220;
    display:none;
    place-items:center;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(8px);
  }
  .shotTip.show{ display:grid; }
  .shotCard{
    width: min(760px, 92vw);
    border-radius: 22px;
    border: 1px solid rgba(160,190,255,0.22);
    background: rgba(10,14,24,0.84);
    box-shadow: 0 22px 70px rgba(0,0,0,0.65);
    padding: 16px;
  }
  .shotCard h3{
    margin: 0 0 8px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.9rem;
  }
  .shotCard p{
    margin: 0 0 12px;
    color: var(--muted);
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    line-height: 1.35rem;
    font-size: 0.95rem;
  }
  .shotBtns{ display:flex; gap:10px; flex-wrap:wrap; }
</style>
</head>

<body class="crt">
  <div class="wood"></div>

  <div id="wandTrail"></div>
  <div id="wandGlow"></div>

  <!-- Audio (paths will come from embedded catalog; safe placeholders included) -->
  <audio id="bgm" preload="auto" loop></audio>

  <!-- Splash -->
  <div class="splash" id="splash">
    <div class="sCard">
      <div class="logo">Calm Paper • STARPLACE</div>
      <div class="sSmall">
        Base game is embedded in this file.<br>
        Packs can be unlocked via <b>Careon deposit receipt</b> codes (manual for now).
      </div>
      <div class="meter"><div></div></div>
      <button class="sBtn" id="startBtn">Start</button>
      <div class="sSmall" style="margin-top:10px;">
        Audio unlocks after Start (browser rule). Screenshot mode is the default output.
      </div>
    </div>
  </div>

  <div class="toast" id="toast">OK</div>

  <!-- Paper stage -->
  <div class="paperStage">
    <div class="paperFrame layout-postit" id="paperFrame">
      <div class="paper postit hasTexture" id="paper"></div>
      <canvas id="sparkCanvas"></canvas>

      <div class="stamps">
        <div class="stamp star" id="stamp1">★ STAR</div>
        <div class="stamp heart" id="stamp2">❤ CUTE</div>
        <div class="stamp mode" id="stampMode">MODE: POST-IT</div>
        <div class="stamp pack" id="stampPack">PACK: BASE</div>
        <div class="stamp level" id="levelStamp">LEVEL UP!</div>
      </div>

      <div class="boxes" id="boxes"></div>

      <div class="hint">
        <span id="layoutHint">POST-IT • 3 BOXES</span>
        <span id="colorHint">IVORY</span>
      </div>
    </div>
  </div>

  <!-- Dock -->
  <div class="dock" id="dock">
    <div class="dockPanel" id="dockPanel" aria-hidden="true">
      <div class="panelInner">

        <!-- Paper -->
        <div class="block tabPane" data-pane="paper">
          <div class="labelTiny">paper</div>
          <select class="sel" id="paperType">
            <option value="postit">Post-it</option>
            <option value="note">Notebook</option>
            <option value="book">Book Cover</option>
            <option value="blank">Blank</option>
          </select>
        </div>

        <!-- Packs -->
        <div class="block tabPane" data-pane="packs">
          <div class="labelTiny">packs</div>
          <select class="sel" id="packSelect"></select>
          <div style="height:10px"></div>

          <div class="btnRow">
            <button class="btn primary" id="unlockBtn">Unlock (Receipt)</button>
            <button class="btn warn" id="resetUnlocksBtn">Reset Unlocks</button>
          </div>

          <div style="height:10px"></div>
          <div class="tog">
            <input id="hideStampsToggle" type="checkbox" />
            <div><small>Hide stamps (cleaner screenshots)</small></div>
          </div>
        </div>

        <!-- Music -->
        <div class="block tabPane" data-pane="music">
          <div class="labelTiny">music</div>
          <select class="sel" id="musicSelect"></select>
          <div style="height:10px"></div>
          <div class="tog">
            <input id="musicToggle" type="checkbox" checked />
            <div><small>Music on/off (per device)</small></div>
          </div>
        </div>

        <!-- Color -->
        <div class="block tabPane" data-pane="color">
          <div class="labelTiny">color</div>
          <div class="chips" aria-label="Paper colors">
            <button class="chip" data-color="--p1" aria-pressed="true"  title="Ivory"    style="background:var(--p1)"></button>
            <button class="chip" data-color="--p2" aria-pressed="false" title="Lavender" style="background:var(--p2)"></button>
            <button class="chip" data-color="--p3" aria-pressed="false" title="Mint"     style="background:var(--p3)"></button>
            <button class="chip" data-color="--p4" aria-pressed="false" title="Peach"    style="background:var(--p4)"></button>
            <button class="chip" data-color="--p5" aria-pressed="false" title="Slate"    style="background:var(--p5)"></button>
            <button class="chip" data-color="--p6" aria-pressed="false" title="Lilac"    style="background:var(--p6)"></button>
            <button class="chip" data-color="--p7" aria-pressed="false" title="Butter"   style="background:var(--p7)"></button>
            <button class="chip" data-color="--p8" aria-pressed="false" title="Sky"      style="background:var(--p8)"></button>
          </div>
        </div>

        <!-- Actions -->
        <div class="block tabPane" data-pane="actions">
          <div class="labelTiny">actions</div>

          <div class="tog">
            <input id="sfxToggle" type="checkbox" checked />
            <div><small>Calm SFX (tap • flip • stamp • sparkle)</small></div>
          </div>

          <div style="height:10px"></div>
          <div class="btnRow">
            <button class="btn good" id="randomBtn">Random</button>
            <button class="btn warn" id="clearBtn">Clear</button>
          </div>

          <div style="height:10px"></div>
          <div class="btnRow">
            <button class="btn primary" id="fullViewBtn">Full View</button>
            <button class="btn primary" id="screenshotBtn">Screenshot</button>
          </div>
        </div>

      </div>
    </div>

    <div class="tabBar" role="tablist" aria-label="Tool tabs">
      <button class="tab" role="tab" data-tab="paper" aria-selected="false">Paper</button>
      <button class="tab" role="tab" data-tab="packs" aria-selected="false">Packs</button>
      <button class="tab" role="tab" data-tab="music" aria-selected="false">Music</button>
      <button class="tab" role="tab" data-tab="color" aria-selected="false">Color</button>
      <button class="tab" role="tab" data-tab="actions" aria-selected="false">Actions</button>
    </div>
  </div>

  <!-- Full View Overlay -->
  <div class="fullOverlay" id="fullOverlay" aria-hidden="true">
    <div class="fullCard">
      <div class="fullTopbar">
        <div class="fullTitle">Full View • Screenshot Friendly</div>
        <div class="fullBtns">
          <button class="miniBtn" id="shotToggleBtn">Screenshot Mode</button>
          <button class="miniBtn primary" id="closeFullBtn">Close</button>
        </div>
      </div>
      <div class="fullBody" id="fullBody"></div>
    </div>
  </div>

  <!-- Screenshot Tip -->
  <div class="shotTip" id="shotTip" aria-hidden="true">
    <div class="shotCard">
      <h3>Screenshot Mode</h3>
      <p>
        UI is hidden for a clean capture.<br>
        On Samsung: use <b>Smart Select</b> and crop the paper.
      </p>
      <div class="shotBtns">
        <button class="miniBtn primary" id="doneShotBtn">Done</button>
        <button class="miniBtn" id="exitShotBtn">Exit Screenshot Mode</button>
      </div>
    </div>
  </div>

<script>
(() => {
  /* ============================================================
     ⭐ BASE GAME CATALOG (EMBEDDED)
     - This is where "spaces for new content" live.
     - You can later swap this to fetch catalog.v1.json from hub.
     ============================================================ */

  const EMBEDDED_CATALOG_V1 = {
    app_id: "calm_paper",
    version: 1,

    // ---- Base game defaults ----
    defaults: {
      start_pack_id: "base",
      start_paper_type: "postit",
      start_paper_color_cssvar: "--p1",
      hide_stamps_default: false,
      music_enabled_default: true
    },

    // ---- Paper textures per pack (optional placeholders) ----
    // Use CSS background-image url() strings.
    // If you add real textures, put them in:
    // assets/images/textures/<pack_id>/texture.png
    textures: {
      base: {
        none: null,
        subtle: "url('assets/images/textures/base/paper_subtle.png')"   // placeholder path
      },
      radiant: {
        none: null,
        subtle: "url('assets/images/textures/radiant/radiant_glow.png')" // placeholder path
      },
      noir: {
        none: null,
        subtle: "url('assets/images/textures/noir/noir_ink.png')"        // placeholder path
      },
      vintage: {
        none: null,
        subtle: "url('assets/images/textures/vintage/vintage_parchment.png')" // placeholder path
      }
    },

    // ---- Stamps per pack (text stamps for now; later you can swap to images) ----
    // If later you want image stamps, we’ll add <img> tags and use assets/images/stamps/<pack_id>/...
    stamps: {
      base:   { left: "★ STAR", right: "❤ CUTE" },
      radiant:{ left: "✨ RADIANT", right: "🌈 GLOW" },
      noir:   { left: "◆ NOIR", right: "✦ INK" },
      vintage:{ left: "✿ VINTAGE", right: "⌁ PARCH" }
    },

    // ---- Music tracks per pack (audio tag will try to play these files) ----
    // Put files at these paths when you’re ready.
    // This app won’t break if they 404; it will just show a toast.
    music: {
      base: [
        { id:"off",  label:"Off", src:null },
        { id:"chip", label:"Chill Chiptune", src:"assets/audio/music/base/calm_chip.mp3" },
        { id:"pad",  label:"Lo-fi Pad", src:"assets/audio/music/base/soft_pad.mp3" },
        { id:"bell", label:"Ambient Bells", src:"assets/audio/music/base/ambient_bells.mp3" }
      ],
      radiant: [
        { id:"rad1", label:"Radiant Drift", src:"assets/audio/music/packs/radiant/radiant_01.mp3" },
        { id:"rad2", label:"Sunwash",       src:"assets/audio/music/packs/radiant/radiant_02.mp3" }
      ],
      noir: [
        { id:"no1", label:"Noir Alley", src:"assets/audio/music/packs/noir/noir_01.mp3" },
        { id:"no2", label:"Midnight Ink", src:"assets/audio/music/packs/noir/noir_02.mp3" }
      ],
      vintage: [
        { id:"v1", label:"Vintage Paper", src:"assets/audio/music/packs/vintage/vintage_01.mp3" },
        { id:"v2", label:"Warm Tape", src:"assets/audio/music/packs/vintage/vintage_02.mp3" }
      ]
    },

    // ---- Products / Packs (max 3 upgrade packs + base) ----
    packs: [
      { id:"base",    name:"Base Game",      locked:false, unlock_type:"none" },

      // Upgrade packs (locked until receipt unlock)
      { id:"radiant", name:"Radiant Pages",  locked:true,  unlock_type:"careon_receipt" },
      { id:"noir",    name:"Noir Pages",     locked:true,  unlock_type:"careon_receipt" },
      { id:"vintage", name:"Vintage Pages",  locked:true,  unlock_type:"careon_receipt" }
    ],

    // ---- Receipt unlock rules (placeholder) ----
    // For now: manual entry. Later: hub can write unlocks automatically.
    // You can change these codes anytime.
    receipt_codes: {
      // Example:
      // "SLD-RAD-100": "radiant"
      "SLD-RAD-100": "radiant",
      "SLD-NOIR-100": "noir",
      "SLD-VINT-100": "vintage"
    }
  };

  /* ============================================================
     ⭐ STORAGE KEYS (per device)
     ============================================================ */
  const LS_UNLOCKS = "calm_paper_unlocks_v1";
  const LS_PREFS   = "calm_paper_prefs_v1";

  function loadJSON(key, fallback){
    try { return JSON.parse(localStorage.getItem(key) || ""); }
    catch { return fallback; }
  }
  function saveJSON(key, obj){
    try { localStorage.setItem(key, JSON.stringify(obj)); } catch {}
  }

  function getUnlocks(){
    return loadJSON(LS_UNLOCKS, {});
  }
  function setUnlocked(packId, isUnlocked=true){
    const u = getUnlocks();
    u[packId] = !!isUnlocked;
    saveJSON(LS_UNLOCKS, u);
  }
  function isUnlocked(packId){
    if (packId === "base") return true;
    const u = getUnlocks();
    return !!u[packId];
  }

  function getPrefs(){
    return loadJSON(LS_PREFS, {});
  }
  function setPref(k,v){
    const p = getPrefs();
    p[k] = v;
    saveJSON(LS_PREFS, p);
  }

  /* ============================================================
     ⭐ ELEMENTS
     ============================================================ */
  const splash = document.getElementById('splash');
  const startBtn = document.getElementById('startBtn');
  const toast = document.getElementById('toast');

  const paperFrame = document.getElementById('paperFrame');
  const paper = document.getElementById('paper');
  const boxes = document.getElementById('boxes');

  const stampMode = document.getElementById('stampMode');
  const stampPack = document.getElementById('stampPack');
  const stamp1 = document.getElementById('stamp1');
  const stamp2 = document.getElementById('stamp2');
  const levelStamp = document.getElementById('levelStamp');

  const layoutHint = document.getElementById('layoutHint');
  const colorHint = document.getElementById('colorHint');

  const wandGlow = document.getElementById('wandGlow');
  const wandTrail = document.getElementById('wandTrail');

  const sparkCanvas = document.getElementById('sparkCanvas');
  const ctx2d = sparkCanvas.getContext("2d");

  const dockPanel = document.getElementById('dockPanel');
  const tabs = Array.from(document.querySelectorAll('.tab'));
  const panes = Array.from(document.querySelectorAll('.tabPane'));

  const paperType = document.getElementById('paperType');
  const packSelect = document.getElementById('packSelect');
  const unlockBtn = document.getElementById('unlockBtn');
  const resetUnlocksBtn = document.getElementById('resetUnlocksBtn');

  const hideStampsToggle = document.getElementById('hideStampsToggle');

  const musicSelect = document.getElementById('musicSelect');
  const musicToggle = document.getElementById('musicToggle');

  const chips = Array.from(document.querySelectorAll('.chip'));

  const sfxToggle = document.getElementById('sfxToggle');
  const randomBtn = document.getElementById('randomBtn');
  const clearBtn = document.getElementById('clearBtn');
  const fullViewBtn = document.getElementById('fullViewBtn');
  const screenshotBtn = document.getElementById('screenshotBtn');

  const fullOverlay = document.getElementById('fullOverlay');
  const fullBody = document.getElementById('fullBody');
  const closeFullBtn = document.getElementById('closeFullBtn');
  const shotToggleBtn = document.getElementById('shotToggleBtn');

  const shotTip = document.getElementById('shotTip');
  const doneShotBtn = document.getElementById('doneShotBtn');
  const exitShotBtn = document.getElementById('exitShotBtn');

  const bgm = document.getElementById('bgm');

  /* ============================================================
     ⭐ WAND FOLLOWER
     ============================================================ */
  let mx = innerWidth/2, my = innerHeight/2;
  let gx = mx, gy = my, tx = mx, ty = my;
  function animWand(){
    gx += (mx - gx) * 0.22;
    gy += (my - gy) * 0.22;
    tx += (mx - tx) * 0.10;
    ty += (my - ty) * 0.10;

    wandGlow.style.left = gx + "px";
    wandGlow.style.top  = gy + "px";
    wandTrail.style.left = tx + "px";
    wandTrail.style.top  = ty + "px";
    requestAnimationFrame(animWand);
  }
  animWand();
  addEventListener("pointermove", (e)=>{ mx=e.clientX; my=e.clientY; });

  /* ============================================================
     ⭐ SPARKLES
     ============================================================ */
  let sparks = [];
  function resizeSpark(){
    const r = paperFrame.getBoundingClientRect();
    sparkCanvas.width = Math.floor(r.width * devicePixelRatio);
    sparkCanvas.height = Math.floor(r.height * devicePixelRatio);
    sparkCanvas.style.width = r.width + "px";
    sparkCanvas.style.height = r.height + "px";
    ctx2d.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  }
  resizeSpark();
  addEventListener("resize", resizeSpark);

  function burst(x, y){
    const r = paperFrame.getBoundingClientRect();
    const lx = x - r.left;
    const ly = y - r.top;
    for (let i=0;i<14;i++){
      const a = Math.random()*Math.PI*2;
      const s = 1.2 + Math.random()*2.6;
      sparks.push({
        x: lx, y: ly,
        vx: Math.cos(a)*s,
        vy: Math.sin(a)*s - 0.2,
        life: 1.0,
        rot: Math.random()*Math.PI,
        spin: (Math.random()*2-1)*0.2
      });
    }
  }
  function drawSparks(){
    const r = paperFrame.getBoundingClientRect();
    ctx2d.clearRect(0,0,r.width,r.height);

    sparks = sparks.filter(p => p.life > 0.02);
    for (const p of sparks){
      p.life *= 0.92;
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.03;
      p.rot += p.spin;

      const alpha = Math.max(0, (p.life - 0.02));
      ctx2d.save();
      ctx2d.globalAlpha = alpha;
      ctx2d.translate(p.x, p.y);
      ctx2d.rotate(p.rot);

      ctx2d.beginPath();
      ctx2d.moveTo(0, -4);
      ctx2d.lineTo(3.5, 0);
      ctx2d.lineTo(0, 4);
      ctx2d.lineTo(-3.5, 0);
      ctx2d.closePath();
      ctx2d.fillStyle = "rgba(255,255,255,0.9)";
      ctx2d.fill();

      ctx2d.globalAlpha = alpha * 0.55;
      ctx2d.beginPath();
      ctx2d.arc(0,0,7,0,Math.PI*2);
      ctx2d.fillStyle = "rgba(88,247,255,0.18)";
      ctx2d.fill();

      ctx2d.restore();
    }
    requestAnimationFrame(drawSparks);
  }
  drawSparks();

  /* ============================================================
     ⭐ SFX (WebAudio fallback)
     - This guarantees “calm sounds” even without mp3 files.
     ============================================================ */
  let audioCtx = null;
  function ensureAudio(){
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") audioCtx.resume();
  }
  function sfxOn(){ return !!sfxToggle.checked; }

  function playTap(){
    if (!sfxOn()) return;
    ensureAudio();
    const t0 = audioCtx.currentTime;

    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    osc.type = "triangle";
    osc.frequency.setValueAtTime(520, t0);
    osc.frequency.exponentialRampToValueAtTime(420, t0 + 0.06);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(0.05, t0 + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.09);
    osc.connect(g).connect(audioCtx.destination);
    osc.start(t0);
    osc.stop(t0 + 0.10);
  }

  function mkNoiseBuffer(dur=0.2){
    const size = Math.floor(audioCtx.sampleRate * dur);
    const buf = audioCtx.createBuffer(1, size, audioCtx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i=0;i<size;i++){
      const x = i/size;
      const decay = Math.exp(-10*x);
      data[i] = (Math.random()*2-1) * decay;
    }
    return buf;
  }

  function playFlip(){
    if (!sfxOn()) return;
    ensureAudio();
    const t0 = audioCtx.currentTime;

    const src = audioCtx.createBufferSource();
    src.buffer = mkNoiseBuffer(0.28);

    const bp = audioCtx.createBiquadFilter();
    bp.type = "bandpass";
    bp.frequency.setValueAtTime(900, t0);
    bp.frequency.exponentialRampToValueAtTime(2400, t0 + 0.10);
    bp.frequency.exponentialRampToValueAtTime(700, t0 + 0.26);
    bp.Q.setValueAtTime(0.8, t0);

    const g = audioCtx.createGain();
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(0.08, t0 + 0.03);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.28);

    src.connect(bp).connect(g).connect(audioCtx.destination);
    src.start(t0);
  }

  function playStamp(){
    if (!sfxOn()) return;
    ensureAudio();
    const t0 = audioCtx.currentTime;

    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    osc.type = "square";
    osc.frequency.setValueAtTime(180, t0);
    osc.frequency.exponentialRampToValueAtTime(90, t0 + 0.05);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(0.10, t0 + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.09);
    osc.connect(g).connect(audioCtx.destination);
    osc.start(t0);
    osc.stop(t0 + 0.10);
  }

  function playSparkle(){
    if (!sfxOn()) return;
    ensureAudio();
    const t0 = audioCtx.currentTime;

    const notes = [880, 1108.73, 1318.51];
    notes.forEach((f, i) => {
      const o = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(f, t0 + i*0.02);
      g.gain.setValueAtTime(0.0001, t0 + i*0.02);
      g.gain.exponentialRampToValueAtTime(0.025, t0 + i*0.02 + 0.01);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + i*0.02 + 0.12);
      o.connect(g).connect(audioCtx.destination);
      o.start(t0 + i*0.02);
      o.stop(t0 + i*0.02 + 0.14);
    });
  }

  function playSuccess(){
    if (!sfxOn()) return;
    ensureAudio();
    const t0 = audioCtx.currentTime;

    const seq = [523.25, 659.25, 783.99];
    seq.forEach((f, i) => {
      const o = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(f, t0 + i*0.07);
      g.gain.setValueAtTime(0.0001, t0 + i*0.07);
      g.gain.exponentialRampToValueAtTime(0.03, t0 + i*0.07 + 0.01);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + i*0.07 + 0.22);
      o.connect(g).connect(audioCtx.destination);
      o.start(t0 + i*0.07);
      o.stop(t0 + i*0.07 + 0.24);
    });
  }

  /* ============================================================
     ⭐ MUSIC (HTMLAudio - best for hosted assets)
     ============================================================ */
  function musicEnabled(){
    return !!musicToggle.checked;
  }

  function stopMusic(){
    bgm.pause();
    bgm.removeAttribute("src");
  }

  function setMusicTrack(src){
    if (!musicEnabled()){
      stopMusic();
      return;
    }
    if (!src){
      stopMusic();
      return;
    }
    bgm.src = src;
    bgm.volume = 0.22;
    bgm.currentTime = 0;
    bgm.play().catch(() => {
      // Some embedded viewers block audio. Start button usually fixes this.
      showToast("MUSIC BLOCKED");
    });
  }

  /* ============================================================
     ⭐ UI HELPERS
     ============================================================ */
  let toastTimer = null;
  function showToast(msg){
    toast.textContent = msg;
    toast.classList.add("show");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 1200);
  }

  let levelTimer = null;
  function levelUp(){
    levelStamp.classList.add("show");
    playStamp();
    if (levelTimer) clearTimeout(levelTimer);
    levelTimer = setTimeout(() => levelStamp.classList.remove("show"), 900);
  }

  /* ============================================================
     ⭐ TABS
     ============================================================ */
  let openTab = null;

  function showPane(name){
    panes.forEach(p => p.style.display = (p.dataset.pane === name ? "block" : "none"));
  }

  function setTab(name){
    const same = (openTab === name);

    if (same){
      const isOpen = dockPanel.classList.contains("open");
      dockPanel.classList.toggle("open", !isOpen);
      dockPanel.setAttribute("aria-hidden", String(isOpen));
      tabs.forEach(t => t.setAttribute("aria-selected", String(!isOpen && t.dataset.tab === name)));
      return;
    }

    openTab = name;
    showPane(name);
    dockPanel.classList.add("open");
    dockPanel.setAttribute("aria-hidden", "false");
    tabs.forEach(t => t.setAttribute("aria-selected", String(t.dataset.tab === name)));
  }

  tabs.forEach(t => t.addEventListener("click", () => { playTap(); setTab(t.dataset.tab); }));

  document.addEventListener("pointerdown", (e) => {
    const dock = document.getElementById("dock");
    if (!dock.contains(e.target)){
      if (dockPanel.classList.contains("open")){
        dockPanel.classList.remove("open");
        dockPanel.setAttribute("aria-hidden","true");
        tabs.forEach(t => t.setAttribute("aria-selected","false"));
        openTab = null;
      }
    }
  }, {passive:true});

  /* ============================================================
     ⭐ LAYOUT BUILDERS (templates do not change)
     ============================================================ */
  function el(tag, attrs = {}){
    const n = document.createElement(tag);
    for (const [k,v] of Object.entries(attrs)){
      if (k === "class") n.className = v;
      else n.setAttribute(k, v);
    }
    return n;
  }

  function buildPostIt(){
    boxes.innerHTML = "";
    boxes.append(
      el("textarea",{rows:"6",placeholder:"Box 1..."}),
      el("textarea",{rows:"6",placeholder:"Box 2..."}),
      el("textarea",{rows:"6",placeholder:"Box 3..."})
    );
    layoutHint.textContent = "POST-IT • 3 BOXES";
    stampMode.textContent = "MODE: POST-IT";
  }

  function buildNote(){
    boxes.innerHTML = "";
    boxes.append(
      el("input",{type:"text",placeholder:"Title..."}),
      el("textarea",{rows:"18",placeholder:"Write your note..."}),
      el("input",{type:"text",placeholder:"Signature..."})
    );
    layoutHint.textContent = "NOTEBOOK • TITLE + BODY + SIGNATURE";
    stampMode.textContent = "MODE: NOTEBOOK";
  }

  function buildBook(){
    boxes.innerHTML = "";
    boxes.append(
      el("input",{type:"text",placeholder:"BOOK TITLE..."}),
      el("input",{type:"text",placeholder:"Subtitle..."}),
      el("input",{type:"text",placeholder:"Author..."})
    );
    layoutHint.textContent = "BOOK COVER • TITLE + SUBTITLE + AUTHOR";
    stampMode.textContent = "MODE: BOOK";
  }

  function buildBlank(){
    boxes.innerHTML = "";
    boxes.append(el("textarea",{rows:"22",placeholder:"Free write..."}));
    layoutHint.textContent = "BLANK • FREE WRITE";
    stampMode.textContent = "MODE: BLANK";
  }

  function applyType(type){
    paper.classList.remove("postit","note","book","blank");
    paper.classList.add(type);

    paperFrame.classList.remove("layout-postit","layout-note","layout-book","layout-blank");
    paperFrame.classList.add("layout-" + type);

    playFlip();
    if (type === "postit") buildPostIt();
    else if (type === "note") buildNote();
    else if (type === "book") buildBook();
    else buildBlank();
    levelUp();

    setPref("paperType", type);
  }

  /* ============================================================
     ⭐ COLORS
     ============================================================ */
  const colorNames = {
    "--p1":"IVORY","--p2":"LAVENDER","--p3":"MINT","--p4":"PEACH",
    "--p5":"SLATE","--p6":"LILAC","--p7":"BUTTER","--p8":"SKY"
  };

  function applyColor(cssVar){
    const val = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim();
    document.documentElement.style.setProperty("--paperColor", val);
    colorHint.textContent = colorNames[cssVar] || "COLOR";

    chips.forEach(ch => ch.setAttribute("aria-pressed","false"));
    const active = chips.find(ch => ch.dataset.color === cssVar);
    if (active) active.setAttribute("aria-pressed","true");

    playTap();
    levelUp();

    setPref("paperColorVar", cssVar);
  }

  /* ============================================================
     ⭐ PACKS + CONTENT
     - This is the “spaces for new content” section.
     - All pack behavior is driven from EMBEDDED_CATALOG_V1.
     ============================================================ */
  let currentPackId = "base";

  function packLocked(packId){
    const pack = EMBEDDED_CATALOG_V1.packs.find(p => p.id === packId);
    if (!pack) return true;
    if (pack.locked === false) return false;
    return !isUnlocked(packId);
  }

  function getPackName(packId){
    const pack = EMBEDDED_CATALOG_V1.packs.find(p => p.id === packId);
    return pack ? pack.name : "Unknown";
  }

  function applyPack(packId){
    // If locked, refuse
    if (packLocked(packId)){
      showToast("LOCKED");
      playTap();
      packSelect.value = currentPackId;
      return;
    }

    currentPackId = packId;
    stampPack.textContent = "PACK: " + getPackName(packId).toUpperCase();
    showToast(getPackName(packId).toUpperCase());
    levelUp();

    // Apply stamp text
    const st = EMBEDDED_CATALOG_V1.stamps[packId] || EMBEDDED_CATALOG_V1.stamps.base;
    stamp1.textContent = st.left || "★";
    stamp2.textContent = st.right || "❤";

    // Apply default texture (subtle) for pack
    const tx = (EMBEDDED_CATALOG_V1.textures[packId] && EMBEDDED_CATALOG_V1.textures[packId].subtle) || null;
    if (tx){
      document.documentElement.style.setProperty("--paperTexture", tx);
    } else {
      document.documentElement.style.setProperty("--paperTexture", "none");
    }

    // Rebuild music list for pack (base + pack)
    rebuildMusicSelect();

    // If current music is not valid anymore, choose first available
    const chosen = musicSelect.value;
    if (chosen && chosen !== "off"){
      // keep selection if still exists
      const exists = Array.from(musicSelect.options).some(o => o.value === chosen);
      if (!exists){
        musicSelect.value = "off";
        stopMusic();
      }
    }

    setPref("packId", packId);
  }

  function rebuildPackSelect(){
    packSelect.innerHTML = "";

    EMBEDDED_CATALOG_V1.packs.forEach(p => {
      const opt = document.createElement("option");
      const locked = packLocked(p.id);
      opt.value = p.id;
      opt.textContent = locked ? `${p.name} (Locked)` : p.name;
      packSelect.appendChild(opt);
    });

    // keep current selection if possible
    packSelect.value = currentPackId;
  }

  function rebuildMusicSelect(){
    musicSelect.innerHTML = "";

    // Base music always available
    const baseTracks = EMBEDDED_CATALOG_V1.music.base || [];
    baseTracks.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t.src ? t.src : "off";
      opt.textContent = t.label;
      musicSelect.appendChild(opt);
    });

    // Pack tracks if not base
    if (currentPackId !== "base"){
      const tracks = EMBEDDED_CATALOG_V1.music[currentPackId] || [];
      if (tracks.length){
        const sep = document.createElement("option");
        sep.disabled = true;
        sep.textContent = "──────── PACK ────────";
        musicSelect.appendChild(sep);

        tracks.forEach(t => {
          const opt = document.createElement("option");
          opt.value = t.src ? t.src : "off";
          opt.textContent = t.label;
          musicSelect.appendChild(opt);
        });
      }
    }

    // restore last choice if possible
    const pref = getPrefs();
    if (pref.musicSrc){
      const exists = Array.from(musicSelect.options).some(o => o.value === pref.musicSrc);
      if (exists) musicSelect.value = pref.musicSrc;
      else musicSelect.value = "off";
    } else {
      musicSelect.value = "off";
    }
  }

  function tryUnlockReceipt(){
    const raw = prompt("Enter Careon deposit receipt code (example: SLD-RAD-100):");
    if (!raw) return;

    const code = raw.trim().toUpperCase();
    const map = EMBEDDED_CATALOG_V1.receipt_codes || {};
    const packId = map[code];

    if (!packId){
      showToast("INVALID");
      playTap();
      return;
    }

    setUnlocked(packId, true);
    showToast("UNLOCKED!");
    playSuccess();
    rebuildPackSelect();

    // auto-switch to newly unlocked pack
    packSelect.value = packId;
    applyPack(packId);
  }

  function resetUnlocks(){
    if (!confirm("Reset local unlocks on this device?")) return;
    saveJSON(LS_UNLOCKS, {});
    showToast("RESET");
    playTap();
    rebuildPackSelect();
    // fall back to base if current pack becomes locked
    if (packLocked(currentPackId)){
      currentPackId = "base";
      rebuildPackSelect();
      applyPack("base");
    }
  }

  /* ============================================================
     ⭐ STAMP VISIBILITY (clean screenshots)
     ============================================================ */
  function applyHideStamps(on){
    const stamps = document.querySelector(".stamps");
    if (!stamps) return;
    stamps.style.opacity = on ? "0" : "1";
    setPref("hideStamps", !!on);
    showToast(on ? "STAMPS OFF" : "STAMPS ON");
    playTap();
  }

  /* ============================================================
     ⭐ FULL VIEW + SCREENSHOT MODE
     ============================================================ */
  let fullClone = null;
  let shotOn = false;

  function cloneFrameInto(target){
    if (fullClone) fullClone.remove();
    fullClone = paperFrame.cloneNode(true);

    // remove spark canvas in clone
    const c = fullClone.querySelector("#sparkCanvas");
    if (c) c.remove();

    // copy field values
    const origFields = paperFrame.querySelectorAll("textarea, input[type='text']");
    const cloneFields = fullClone.querySelectorAll("textarea, input[type='text']");
    origFields.forEach((f, i) => { if (cloneFields[i]) cloneFields[i].value = f.value; });
    cloneFields.forEach(f => f.setAttribute("readonly","true"));

    target.innerHTML = "";
    target.appendChild(fullClone);
  }

  function openFullView(){
    cloneFrameInto(fullBody);
    fullOverlay.classList.add("show");
    fullOverlay.setAttribute("aria-hidden","false");
    playTap();
    showToast("FULL VIEW");
  }
  function closeFullView(){
    fullOverlay.classList.remove("show");
    fullOverlay.setAttribute("aria-hidden","true");
    playTap();
  }

  function enterScreenshotMode(){
    shotOn = true;
    document.body.classList.add("screenshotMode");
    shotTip.classList.add("show");
    shotTip.setAttribute("aria-hidden","false");
    showToast("SCREENSHOT");
    playTap();
  }

  function exitScreenshotMode(){
    shotOn = false;
    document.body.classList.remove("screenshotMode");
    shotTip.classList.remove("show");
    shotTip.setAttribute("aria-hidden","true");
    showToast("UI ON");
    playTap();
  }

  /* ============================================================
     ⭐ INTERACTIONS
     ============================================================ */
  paperFrame.addEventListener("pointerdown", (e) => {
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : "";
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || tag === "BUTTON") return;
    burst(e.clientX, e.clientY);
    playSparkle();
  }, {passive:true});

  boxes.addEventListener("focusin", () => playTap());

  /* ============================================================
     ⭐ ACTIONS
     ============================================================ */
  function randomize(){
    const types = ["postit","note","book","blank"];
    const colors = ["--p1","--p2","--p3","--p4","--p5","--p6","--p7","--p8"];
    const t = types[Math.floor(Math.random()*types.length)];
    const c = colors[Math.floor(Math.random()*colors.length)];

    paperType.value = t;
    applyType(t);
    applyColor(c);

    showToast("RANDOM");
  }

  function clearText(){
    const fields = boxes.querySelectorAll("textarea, input[type='text']");
    fields.forEach(f => f.value = "");
    showToast("CLEARED");
    playTap();
  }

  /* ============================================================
     ⭐ EVENT WIRING
     ============================================================ */
  paperType.addEventListener("change", () => applyType(paperType.value));
  chips.forEach(ch => ch.addEventListener("click", () => applyColor(ch.dataset.color)));

  packSelect.addEventListener("change", () => {
    playTap();
    applyPack(packSelect.value);
  });
  unlockBtn.addEventListener("click", tryUnlockReceipt);
  resetUnlocksBtn.addEventListener("click", resetUnlocks);

  hideStampsToggle.addEventListener("change", () => applyHideStamps(hideStampsToggle.checked));

  musicToggle.addEventListener("change", () => {
    setPref("musicEnabled", !!musicToggle.checked);
    if (!musicToggle.checked){
      stopMusic();
      showToast("MUSIC OFF");
      return;
    }
    showToast("MUSIC ON");
    // restart selected
    const v = musicSelect.value;
    if (v && v !== "off") setMusicTrack(v);
  });

  musicSelect.addEventListener("change", () => {
    playTap();
    const v = musicSelect.value;
    setPref("musicSrc", v);
    if (v === "off") { stopMusic(); showToast("MUSIC OFF"); return; }
    setMusicTrack(v);
    showToast("PLAY");
  });

  randomBtn.addEventListener("click", () => { playTap(); randomize(); setTab("actions"); });
  clearBtn.addEventListener("click", clearText);

  fullViewBtn.addEventListener("click", openFullView);
  closeFullBtn.addEventListener("click", closeFullView);
  fullOverlay.addEventListener("pointerdown", (e) => { if (e.target === fullOverlay) closeFullView(); });

  screenshotBtn.addEventListener("click", () => {
    openFullView();         // maximize capture area
    enterScreenshotMode();  // hide UI
    playSuccess();
  });

  shotToggleBtn.addEventListener("click", () => {
    if (!shotOn){
      enterScreenshotMode();
      shotToggleBtn.textContent = "UI On";
    } else {
      exitScreenshotMode();
      shotToggleBtn.textContent = "Screenshot Mode";
    }
  });

  doneShotBtn.addEventListener("click", () => {
    // keep screenshot mode ON, hide the tip so the capture is clean
    shotTip.classList.remove("show");
    shotTip.setAttribute("aria-hidden","true");
    showToast("CAPTURE NOW");
    playTap();
  });

  exitShotBtn.addEventListener("click", () => {
    exitScreenshotMode();
    shotToggleBtn.textContent = "Screenshot Mode";
  });

  /* ============================================================
     ⭐ INIT
     ============================================================ */
  function applyDefaults(){
    const prefs = getPrefs();
    const d = EMBEDDED_CATALOG_V1.defaults;

    // Paper type
    const pt = prefs.paperType || d.start_paper_type || "postit";
    paperType.value = pt;
    applyType(pt);

    // Color
    const cv = prefs.paperColorVar || d.start_paper_color_cssvar || "--p1";
    applyColor(cv);

    // Hide stamps
    const hs = (prefs.hideStamps !== undefined) ? !!prefs.hideStamps : !!d.hide_stamps_default;
    hideStampsToggle.checked = hs;
    applyHideStamps(hs);

    // Pack selection
    const pid = prefs.packId || d.start_pack_id || "base";
    currentPackId = pid;

    rebuildPackSelect();
    // If saved pack is now locked, fall back to base
    if (packLocked(currentPackId)) currentPackId = "base";
    packSelect.value = currentPackId;
    applyPack(currentPackId);

    // Music enabled
    const me = (prefs.musicEnabled !== undefined) ? !!prefs.musicEnabled : !!d.music_enabled_default;
    musicToggle.checked = me;

    // Music list
    rebuildMusicSelect();
    if (!me) stopMusic();
  }

  startBtn.addEventListener("click", () => {
    ensureAudio(); // unlock audio context
    playTap();
    splash.classList.add("hidden");
    applyDefaults();
    setTab("actions");
    setTimeout(() => resizeSpark(), 200);
  });

  // Make sure stage resizes well in weird host windows
  setTimeout(() => resizeSpark(), 350);
})();
</script>
</body>
</html>