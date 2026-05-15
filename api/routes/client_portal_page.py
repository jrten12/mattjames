def render_client_portal_html() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Matt James — AI Intake Portal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,400..800&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #f7f4ef;
      --bg-deep: #efe9e0;
      --surface: #fffcfa;
      --surface-glass: rgba(255,252,250,0.78);
      --surface-soft: #faf6f0;
      --border: rgba(28, 32, 44, 0.06);
      --border-strong: rgba(28, 32, 44, 0.1);
      --ink: #141a24;
      --text: #1a2230;
      --text-2: #3d4556;
      --text-muted: #6b7287;
      --accent: #2f4d8c;
      --accent-mid: #3d62b8;
      --accent-bright: #5a7fd4;
      --accent-teal: #0d9488;
      --accent-soft: #e8eef9;
      --accent-glow: rgba(45, 77, 140, 0.14);
      --gold: #b8956a;
      --gold-soft: rgba(184, 149, 106, 0.12);
      --success: #0f766e;
      --success-bg: #ecfdf9;
      --success-border: #99f6e4;
      --warning: #9a3412;
      --warning-bg: #fff7ed;
      --warning-border: #fed7aa;
      --shadow: 0 1px 0 rgba(255,255,255,.85) inset, 0 4px 20px rgba(20, 26, 36, 0.06), 0 1px 3px rgba(20, 26, 36, 0.04);
      --shadow-lg: 0 1px 0 rgba(255,255,255,.9) inset, 0 16px 48px rgba(20, 26, 36, 0.09), 0 4px 12px rgba(20, 26, 36, 0.05);
      --shadow-xl: 0 1px 0 rgba(255,255,255,.95) inset, 0 28px 64px rgba(20, 26, 36, 0.11), 0 8px 24px rgba(20, 26, 36, 0.06);
      --radius-sm: 10px;
      --radius: 16px;
      --radius-lg: 20px;
      --radius-xl: 26px;
      --radius-pill: 999px;
    }
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    html{scroll-behavior:smooth}
    body{
      font-family:"Plus Jakarta Sans","Segoe UI",system-ui,sans-serif;
      background:linear-gradient(180deg, var(--bg) 0%, var(--bg-deep) 55%, #ebe4d9 100%);
      color:var(--text);
      line-height:1.58;
      min-height:100vh;
      overflow-x:hidden;
      -webkit-font-smoothing:antialiased;
    }

    /* Ambient */
    .ambient{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
    .ambient::after{
      content:"";position:absolute;inset:0;
      background:radial-gradient(ellipse 90% 50% at 50% -10%, rgba(255,252,248,.9), transparent 55%);
    }
    .orb{position:absolute;border-radius:50%;filter:blur(88px);opacity:.28;animation:orbFloat 14s ease-in-out infinite alternate}
    .orb-1{width:620px;height:620px;background:radial-gradient(circle, rgba(61,98,184,.35) 0%, transparent 68%);top:-180px;right:-80px}
    .orb-2{width:480px;height:480px;background:radial-gradient(circle, rgba(13,148,136,.22) 0%, transparent 70%);bottom:-40px;left:-120px;animation-delay:-5s;opacity:.2}
    .orb-3{width:340px;height:340px;background:radial-gradient(circle, rgba(184,149,106,.18) 0%, transparent 72%);top:38%;left:42%;opacity:.14;animation-delay:-9s}
    @keyframes orbFloat{from{transform:translate(0,0) scale(1)}to{transform:translate(18px,12px) scale(1.03)}}

    .shell{position:relative;z-index:1}

    /* Nav */
    .nav{position:sticky;top:0;z-index:50;padding:14px 20px 10px}
    .nav-inner{
      max-width:1280px;margin:0 auto;
      display:flex;align-items:center;justify-content:space-between;gap:14px;
      background:linear-gradient(135deg, rgba(255,252,250,.94), rgba(247,244,239,.88));
      backdrop-filter:blur(22px) saturate(160%);
      -webkit-backdrop-filter:blur(22px) saturate(160%);
      border:1px solid var(--border-strong);
      border-radius:var(--radius-pill);
      padding:10px 18px 10px 14px;
      box-shadow:var(--shadow-lg);
    }
    .nav-brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
    .nav-mark{
      width:38px;height:38px;border-radius:12px;
      background:linear-gradient(145deg, #1e3a5f 0%, #2f4d8c 45%, #0d9488 100%);
      display:grid;place-items:center;
      flex-shrink:0;
      box-shadow:0 4px 16px rgba(30,58,95,.35), 0 0 0 1px rgba(255,255,255,.2) inset;
    }
    .nav-mark svg{width:22px;height:22px;display:block}
    .nav-word{display:flex;flex-direction:column;gap:1px;line-height:1.05}
    .nav-brand-name{font-size:15px;font-weight:800;letter-spacing:-.35px;color:var(--ink)}
    .nav-brand-tag{font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted)}
    .nav-links{display:flex;align-items:center;gap:2px;flex-wrap:wrap}
    .nav-link{
      border:none;background:none;color:var(--text-muted);
      font:inherit;font-size:13px;font-weight:600;
      padding:8px 14px;border-radius:var(--radius-pill);cursor:pointer;
      transition:color .18s,background .18s;
    }
    .nav-link:hover{color:var(--text);background:rgba(20,26,36,.05)}
    .nav-cta{
      background:linear-gradient(135deg, #2a4578, #3d62b8);
      color:#fff;
      border:none;border-radius:var(--radius-pill);
      padding:9px 18px;font:inherit;font-size:13px;font-weight:700;
      cursor:pointer;
      box-shadow:0 4px 18px rgba(42,69,120,.35), 0 0 0 1px rgba(255,255,255,.12) inset;
      transition:transform .18s, box-shadow .18s, filter .18s;
    }
    .nav-cta:hover{transform:translateY(-1px);box-shadow:0 8px 28px rgba(42,69,120,.4), 0 0 0 1px rgba(255,255,255,.15) inset;filter:brightness(1.03)}

    /* Container */
    .container{max-width:1280px;margin:0 auto;padding:0 24px 72px}

    /* Hero */
    .hero{
      padding:56px 0 52px;
      display:grid;grid-template-columns:1fr 1fr;gap:40px 56px;align-items:center;
    }
    .hero-left{max-width:580px}
    .eyebrow{
      display:inline-flex;align-items:center;gap:8px;
      background:linear-gradient(135deg, var(--accent-soft), #f5f0e8);
      border:1px solid rgba(47,77,140,.15);
      color:var(--accent);font-size:11px;font-weight:700;
      letter-spacing:.04em;
      padding:6px 14px;border-radius:var(--radius-pill);margin-bottom:22px;
    }
    .eyebrow-dot{width:6px;height:6px;border-radius:50%;background:var(--accent-teal);animation:blink 2.4s ease-in-out infinite}
    @keyframes blink{0%,100%{opacity:1}50%{opacity:.35}}
    .hero h1{
      font-size:clamp(32px,3.9vw,52px);font-weight:800;
      line-height:1.04;letter-spacing:-.045em;margin-bottom:20px;color:var(--ink);
    }
    .hero h1 span{
      background:linear-gradient(115deg, #1e3a5f 0%, #3d62b8 38%, #0d9488 72%, #b8956a 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    }
    .hero-sub{font-size:16.5px;color:var(--text-2);line-height:1.62;max-width:500px;margin-bottom:34px;font-weight:450}
    .hero-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
    .btn-hero{
      display:inline-flex;align-items:center;gap:8px;
      background:linear-gradient(135deg, #2a4578, #3d62b8);
      color:#fff;
      border:none;border-radius:var(--radius-pill);
      padding:14px 26px;font:inherit;font-size:15px;font-weight:700;
      cursor:pointer;
      box-shadow:0 8px 28px rgba(42,69,120,.38), 0 0 0 1px rgba(255,255,255,.1) inset;
      transition:transform .2s, box-shadow .2s, filter .2s;
    }
    .btn-hero:hover{transform:translateY(-2px);box-shadow:0 14px 36px rgba(42,69,120,.45), 0 0 0 1px rgba(255,255,255,.14) inset;filter:brightness(1.04)}
    .btn-ghost-hero{
      display:inline-flex;align-items:center;gap:8px;
      background:var(--surface);color:var(--text-2);
      border:1px solid var(--border-strong);border-radius:var(--radius-pill);
      padding:14px 22px;font:inherit;font-size:15px;font-weight:600;
      cursor:pointer;transition:border-color .18s,color .18s,transform .18s,box-shadow .18s;
      box-shadow:var(--shadow);
    }
    .btn-ghost-hero:hover{border-color:rgba(47,77,140,.25);color:var(--accent);transform:translateY(-1px);box-shadow:var(--shadow-lg)}

    /* Hero visual — art-directed stack */
    .hero-visual{position:relative;height:400px;max-width:540px;margin-left:auto}
    .float-card{
      position:absolute;
      background:linear-gradient(165deg, rgba(255,252,250,.95), rgba(250,246,240,.88));
      backdrop-filter:blur(24px) saturate(165%);
      -webkit-backdrop-filter:blur(24px) saturate(165%);
      border:1px solid rgba(255,255,255,.65);
      border-radius:var(--radius-lg);
      box-shadow:var(--shadow-lg);
      padding:17px 18px;
      animation:floatUp 7s ease-in-out infinite alternate;
    }
    .float-card:nth-child(1){width:min(100%,302px);top:12px;right:0;z-index:3;animation-delay:0s}
    .float-card:nth-child(2){width:min(100%,232px);top:168px;right:228px;z-index:2;animation-delay:-2.8s}
    .float-card:nth-child(3){width:min(100%,198px);bottom:20px;right:44px;z-index:4;animation-delay:-5.5s}
    @keyframes floatUp{from{transform:translateY(0)}to{transform:translateY(-8px)}}
    .fc-header{display:flex;align-items:center;gap:8px;margin-bottom:11px}
    .fc-dot{width:7px;height:7px;border-radius:50%}
    .fc-title{font-size:11px;font-weight:700;color:var(--text-muted);letter-spacing:.04em}
    .fc-bar-row{display:flex;align-items:center;gap:8px;margin-bottom:7px}
    .fc-bar-label{font-size:10px;color:var(--text-muted);min-width:56px;font-weight:500}
    .fc-bar{flex:1;height:6px;border-radius:4px;background:rgba(47,77,140,.08);overflow:hidden}
    .fc-bar-fill{height:100%;border-radius:4px;background:linear-gradient(90deg, #2f4d8c, #0d9488)}
    .mini-chip{
      display:inline-flex;align-items:center;gap:4px;
      font-size:10px;font-weight:700;padding:5px 10px;border-radius:var(--radius-pill);border:1px solid;
    }
    .chip-accent{border-color:rgba(47,77,140,.22);color:var(--accent);background:var(--accent-soft)}
    .chip-purple{border-color:rgba(47,77,140,.22);color:var(--accent);background:var(--accent-soft)}
    .chip-teal{border-color:rgba(13,148,136,.22);color:var(--accent-teal);background:rgba(13,148,136,.08)}
    .chip-gold{border-color:rgba(184,149,106,.28);color:#8a6d3e;background:var(--gold-soft)}

    /* Workspace */
    .workspace{display:grid;grid-template-columns:1.6fr 1fr;gap:20px;align-items:start}

    /* Card */
    .card{
      background:var(--surface);border:1px solid var(--border);
      border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:22px;
      transition:box-shadow .2s;
    }
    .card:hover{box-shadow:var(--shadow-lg)}

    /* AI Assistant */
    .assistant-head{
      display:flex;align-items:center;gap:12px;
      padding-bottom:16px;border-bottom:1px solid var(--border);margin-bottom:16px;
    }
    .ai-avatar{
      width:40px;height:40px;border-radius:14px;
      background:linear-gradient(135deg,#5b47e0,#9333ea);
      display:grid;place-items:center;
      animation:avatarPulse 3s ease-in-out infinite;
      flex-shrink:0;
    }
    .ai-avatar svg{width:20px;height:20px}
    @keyframes avatarPulse{
      0%,100%{box-shadow:0 0 0 0 rgba(91,71,224,.4)}
      50%{box-shadow:0 0 0 8px rgba(91,71,224,0)}
    }
    .ai-meta{flex:1}
    .ai-name{font-size:14px;font-weight:800;letter-spacing:-.2px}
    .ai-online{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:var(--success);font-weight:600}
    .status-dot{width:6px;height:6px;border-radius:50%;background:var(--success);animation:blink 2s infinite}
    .step-tags{display:flex;gap:5px;flex-wrap:wrap}
    .step-tag{
      font-size:11px;font-weight:700;padding:4px 9px;border-radius:var(--radius-pill);
      border:1px solid;transition:all .2s;
    }

    /* Progress */
    .prog-wrap{margin-bottom:16px}
    .prog-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:7px}
    .prog-label{font-size:12px;font-weight:700;color:var(--text-2)}
    .prog-pct{font-size:12px;font-weight:800;color:var(--accent)}
    .prog-rail{width:100%;height:6px;border-radius:3px;background:#ede9fe;overflow:hidden}
    .prog-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,#5b47e0,#9333ea);transition:width .4s ease}
    .step-dots{display:flex;gap:5px;margin-top:10px;justify-content:center}
    .step-dot{height:6px;border-radius:3px;background:#e5e0fb;transition:background .3s,width .3s;width:22px}
    .step-dot.active{background:linear-gradient(90deg,#5b47e0,#9333ea);width:38px}
    .step-dot.done{background:#a78bfa;width:22px}

    /* Message bubble */
    .msg-bubble{
      background:linear-gradient(135deg,#f5f3ff,#faf8ff);
      border:1px solid rgba(167,139,250,.3);
      border-radius:4px 16px 16px 16px;
      padding:13px 15px;font-size:14px;color:var(--text-2);
      line-height:1.6;margin-bottom:16px;
    }

    /* Thinking */
    .thinking{
      display:none;align-items:center;gap:5px;
      padding:9px 13px;background:#f5f3ff;
      border:1px solid rgba(167,139,250,.3);
      border-radius:4px 14px 14px 14px;width:fit-content;margin-bottom:12px;
    }
    .thinking.on{display:flex}
    .tdot{width:6px;height:6px;border-radius:50%;background:var(--accent);animation:tdotBounce 1.2s ease-in-out infinite}
    .tdot:nth-child(2){animation-delay:.2s}
    .tdot:nth-child(3){animation-delay:.4s}
    @keyframes tdotBounce{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-6px);opacity:1}}

    /* Current question */
    .cq{margin-bottom:14px}
    .cq-label{
      font-size:10px;font-weight:800;text-transform:uppercase;
      letter-spacing:.8px;color:var(--accent);margin-bottom:6px;
      display:flex;align-items:center;gap:5px;
    }
    .cq-text{font-size:17px;font-weight:700;letter-spacing:-.3px;line-height:1.3;color:var(--text)}
    .helper{font-size:12px;color:var(--text-muted);margin-top:4px;font-style:italic}

    /* Fields */
    .frow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
    .fcol{display:grid;gap:12px}
    .full{grid-column:1/-1}
    .flabel{display:block;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;color:var(--text-muted);margin-bottom:6px}
    textarea,input,select{
      width:100%;border:1.5px solid var(--border-strong);border-radius:var(--radius-sm);
      padding:10px 12px;font:inherit;font-size:14px;color:var(--text);background:var(--surface);
      transition:border-color .15s,box-shadow .15s;
    }
    textarea{resize:vertical;min-height:90px;line-height:1.6}
    textarea::placeholder,input::placeholder{color:#b0a898}
    textarea:focus,input:focus,select:focus{
      outline:none;border-color:var(--accent);
      box-shadow:0 0 0 4px rgba(91,71,224,.1);
    }
    select{appearance:none;cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%237d7670' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:32px}

    /* Chips */
    .chips-label{font-size:11px;font-weight:700;color:var(--text-muted);margin-bottom:8px;margin-top:14px}
    .chips-row{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:14px}
    .chip{
      border:1px solid var(--border-strong);background:var(--surface);color:var(--text-2);
      border-radius:var(--radius-pill);padding:7px 13px;
      font:inherit;font-size:12px;font-weight:600;cursor:pointer;
      transition:border-color .15s,color .15s,background .15s,transform .1s;
    }
    .chip:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-soft);transform:translateY(-1px)}

    /* Controls */
    .ctrl-row{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:14px}
    .ctrl-left{display:flex;gap:8px}

    /* Buttons */
    .btn{
      display:inline-flex;align-items:center;gap:6px;
      border:none;border-radius:var(--radius-pill);
      padding:10px 18px;font:inherit;font-size:13px;font-weight:700;
      cursor:pointer;transition:filter .15s,transform .15s,box-shadow .15s;
      text-decoration:none;
    }
    .btn-primary{
      background:linear-gradient(135deg,#5b47e0,#7c5ce4);color:#fff;
      box-shadow:0 6px 16px rgba(91,71,224,.3);
    }
    .btn-primary:hover{filter:brightness(1.06);transform:translateY(-1px);box-shadow:0 10px 24px rgba(91,71,224,.4)}
    .btn-secondary{background:var(--surface);color:var(--text-2);border:1px solid var(--border-strong)}
    .btn-secondary:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px)}
    .btn-ghost{background:transparent;color:var(--text-muted);border:1px solid var(--border)}
    .btn-ghost:hover{color:var(--text);border-color:var(--border-strong)}
    button[disabled]{opacity:.4;cursor:not-allowed;transform:none!important;filter:none!important}

    /* Status */
    .status-msg{
      margin-top:12px;border-radius:var(--radius-sm);
      padding:11px 14px;font-size:13px;min-height:44px;
      border:1px solid var(--border);background:var(--surface-soft);color:var(--text-2);
    }
    .status-msg.success{background:var(--success-bg);border-color:var(--success-border);color:var(--success)}
    .status-msg.warning{background:var(--warning-bg);border-color:var(--warning-border);color:var(--warning)}

    /* Live Brief */
    .brief-head{
      display:flex;align-items:center;justify-content:space-between;
      padding-bottom:14px;border-bottom:1px solid var(--border);margin-bottom:14px;
    }
    .brief-label{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px}
    .brief-title{font-size:16px;font-weight:800;letter-spacing:-.3px}
    .orb-wrap{position:relative;width:52px;height:52px;flex-shrink:0}
    .orb-wrap svg{width:52px;height:52px;transform:rotate(-90deg)}
    .orb-bg{fill:none;stroke:#ede9fe;stroke-width:4}
    .orb-fg{fill:none;stroke:url(#og);stroke-width:4;stroke-linecap:round;stroke-dasharray:132;stroke-dashoffset:132;transition:stroke-dashoffset .6s ease}
    .orb-label{
      position:absolute;inset:0;display:grid;place-items:center;
      font-size:11px;font-weight:800;color:var(--accent);
    }
    .brief-item{
      margin-bottom:9px;padding:10px 12px;
      border:1px solid var(--border);border-radius:var(--radius-sm);
      background:#fdfaf7;transition:border-color .2s;
    }
    .brief-item:hover{border-color:var(--border-strong)}
    .brief-item-top{display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:3px}
    .brief-item-key{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.5px;color:var(--text-muted)}
    .badge{display:inline-flex;align-items:center;font-size:10px;font-weight:700;padding:2px 7px;border-radius:var(--radius-pill)}
    .badge-ready{background:#dcfce7;color:#15803d;border:1px solid #86efac}
    .badge-needs{background:#fffbeb;color:#b45309;border:1px solid #fde68a}
    .badge-empty{background:#f1f5f9;color:#64748b;border:1px solid #e2e8f0}
    .brief-item-val{font-size:13px;color:var(--text-2);line-height:1.5}
    .brief-item-placeholder{font-size:13px;color:#c4b8a8;font-style:italic}
    .followup-box{
      background:linear-gradient(135deg,#faf5ff,#f5f3ff);
      border:1px solid rgba(167,139,250,.25);border-radius:var(--radius-sm);
      padding:12px;margin-top:10px;
    }
    .followup-title{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;color:var(--accent);margin-bottom:8px}
    .followup-item{
      display:flex;align-items:flex-start;gap:7px;
      font-size:12px;color:var(--text-2);padding:5px 0;
      border-bottom:1px solid rgba(167,139,250,.15);line-height:1.5;
    }
    .followup-item:last-child{border-bottom:none}
    .followup-arrow{color:var(--accent);margin-top:2px;flex-shrink:0}

    /* Section bar */
    .section-bar{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
    .section-eyebrow{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px}
    .section-title{font-size:24px;font-weight:800;letter-spacing:-.5px}
    .section-sub{font-size:14px;color:var(--text-muted);margin-top:2px}

    /* SOW */
    .sow-wrap{margin-top:20px}
    .sow-card{
      background:#fff;border:1px solid var(--border);
      border-radius:var(--radius-xl);box-shadow:var(--shadow-xl);overflow:hidden;
    }
    .sow-bar{
      background:linear-gradient(135deg,#5b47e0,#7c5ce4);
      padding:18px 24px;
      display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
    }
    .sow-bar-left{display:flex;align-items:center;gap:12px}
    .sow-icon{
      width:38px;height:38px;background:rgba(255,255,255,.18);border-radius:11px;
      display:grid;place-items:center;font-size:18px;
    }
    .sow-bar-title{color:#fff;font-weight:800;font-size:15px}
    .sow-bar-sub{color:rgba(255,255,255,.7);font-size:12px;margin-top:1px}
    .sow-badge-el{
      display:inline-flex;align-items:center;gap:5px;
      background:rgba(255,255,255,.18);color:#fff;
      border:1px solid rgba(255,255,255,.3);border-radius:var(--radius-pill);
      padding:5px 12px;font-size:11px;font-weight:700;
    }
    .sow-body{padding:28px}
    .sow-empty{text-align:center;padding:36px}
    .sow-empty-icon{font-size:44px;margin-bottom:12px}
    .sow-empty-title{font-size:18px;font-weight:800;color:var(--text-2);margin-bottom:6px}
    .sow-empty-sub{font-size:14px;color:var(--text-muted);max-width:380px;margin:0 auto 20px}
    .sow-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    .sow-field{display:grid;gap:5px}
    .sow-field.full{grid-column:1/-1}
    .sow-field-label{
      font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.7px;color:var(--text-muted);
      display:flex;align-items:center;gap:8px;
    }
    .sow-field-label::after{content:'';flex:1;height:1px;background:var(--border)}
    .sow-textarea{
      border:1px solid var(--border);border-radius:var(--radius-sm);
      padding:10px 12px;font:inherit;font-size:13px;
      color:var(--text-2);background:#fdfaf7;resize:vertical;min-height:80px;
      transition:border-color .15s,box-shadow .15s;
    }
    .sow-textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(91,71,224,.08);background:#fff}
    .sow-actions-bar{
      padding:16px 28px 24px;border-top:1px solid var(--border);
      display:flex;align-items:center;gap:10px;flex-wrap:wrap;
    }

    /* Shimmer */
    .shimmer{
      background:linear-gradient(90deg,#f0ebff 25%,#e8e2fb 50%,#f0ebff 75%);
      background-size:200% 100%;animation:shim 1.5s infinite;
      border-radius:6px;height:12px;margin-bottom:8px;
    }
    @keyframes shim{0%{background-position:-200% 0}100%{background-position:200% 0}}

    /* Requests */
    .reqs-section{margin-top:20px}
    .reqs-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
    .req-card{
      background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
      padding:16px;display:grid;gap:10px;
      transition:box-shadow .2s,transform .2s,border-color .2s;
    }
    .req-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-2px);border-color:var(--border-strong)}
    .req-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
    .req-title{font-size:14px;font-weight:700;color:var(--text);line-height:1.3}
    .req-type{font-size:11px;color:var(--text-muted);margin-top:2px}
    .req-meta{font-size:11px;color:var(--text-muted)}
    .req-footer{display:flex;align-items:center;justify-content:space-between;gap:8px}
    .req-badge{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:4px 10px;border-radius:var(--radius-pill)}
    .rb-draft{background:#f1f5f9;color:#475569;border:1px solid #e2e8f0}
    .rb-submitted{background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe}
    .rb-review{background:var(--accent-soft);color:var(--accent);border:1px solid rgba(91,71,224,.2)}
    .rb-approved{background:var(--success-bg);color:var(--success);border:1px solid var(--success-border)}
    .rb-changes{background:var(--warning-bg);color:var(--warning);border:1px solid var(--warning-border)}
    .req-action{
      background:var(--accent-soft);color:var(--accent);
      border:1px solid rgba(91,71,224,.2);border-radius:var(--radius-pill);
      padding:6px 13px;font:inherit;font-size:12px;font-weight:700;cursor:pointer;
      transition:background .15s,transform .1s;
    }
    .req-action:hover{background:#e0d9fb;transform:translateY(-1px)}

    /* Empty state */
    .empty-state{
      text-align:center;padding:52px 24px;
      border:1.5px dashed var(--border-strong);border-radius:var(--radius-lg);
    }
    .empty-icon{font-size:48px;margin-bottom:14px}
    .empty-title{font-size:18px;font-weight:800;color:var(--text-2);margin-bottom:6px}
    .empty-sub{font-size:14px;color:var(--text-muted);max-width:360px;margin:0 auto 22px;line-height:1.6}

    /* Review section */
    .review-section{margin-top:20px}

    /* Drawer */
    .overlay{position:fixed;inset:0;background:rgba(10,8,6,.42);z-index:80;backdrop-filter:blur(4px);display:none}
    .overlay.open{display:block}
    .drawer{
      position:fixed;top:0;right:0;width:min(440px,100vw);height:100vh;
      background:var(--surface);border-left:1px solid var(--border);
      box-shadow:-24px 0 48px rgba(0,0,0,.14);z-index:90;
      transform:translateX(110%);transition:transform 280ms cubic-bezier(.4,0,.2,1);
      display:flex;flex-direction:column;
    }
    .drawer.open{transform:translateX(0)}
    .drawer-head{padding:20px 22px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
    .drawer-head-title{font-size:16px;font-weight:800}
    .drawer-head-sub{font-size:12px;color:var(--text-muted);margin-top:2px}
    .drawer-body{flex:1;overflow-y:auto;padding:22px;display:grid;gap:14px;align-content:start}
    .drawer-field label{display:block;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;color:var(--text-muted);margin-bottom:6px}
    .drawer-field input{border:1px solid var(--border-strong)}

    .hidden{display:none!important}

    @media(max-width:1100px){.workspace{grid-template-columns:1fr}.hero{grid-template-columns:1fr}.hero-visual{display:none}}
    @media(max-width:760px){.frow,.sow-grid{grid-template-columns:1fr}.hero h1{font-size:30px}.container{padding:0 16px 48px}.nav-inner{padding:8px 12px}}
  </style>
</head>
<body>

<div class="ambient" aria-hidden="true">
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
</div>

<div class="shell">
  <nav class="nav">
    <div class="nav-inner">
      <a class="nav-brand" href="#">
        <div class="nav-mark">MJ</div>
        <span class="nav-brand-name">Matt James</span>
      </a>
      <div class="nav-links">
        <button class="nav-link" id="navIntakeBtn">Intake</button>
        <button class="nav-link" id="navRequestsBtn">My Requests</button>
        <button class="nav-link" id="navSowBtn">SOW</button>
        <button class="nav-link" id="navHelpBtn">Help</button>
        <button class="nav-link" id="openSettingsBtn" title="Admin settings">&#9881;</button>
      </div>
      <button class="nav-cta" id="navStartBtn">Start AI intake &#8594;</button>
    </div>
  </nav>

  <div class="container">

    <!-- Hero -->
    <section class="hero">
      <div class="hero-left">
        <div class="eyebrow">
          <span class="eyebrow-dot"></span>
          AI-Powered Intake Assistant
        </div>
        <h1>Turn your app idea into a <span>build-ready scope.</span></h1>
        <p class="hero-sub">Our AI intake assistant asks the right questions, organises your requirements, and drafts a professional Statement of Work — ready for our team to scope and build.</p>
        <div class="hero-actions">
          <button class="btn-hero" id="heroStartBtn">&#10022; Start your AI intake</button>
          <button class="btn-ghost-hero" id="heroRequestsBtn">View existing requests</button>
        </div>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="float-card">
          <div class="fc-header">
            <div class="fc-dot" style="background:#5b47e0"></div>
            <span class="fc-title">SOW Readiness</span>
          </div>
          <div class="fc-bar-row"><span class="fc-bar-label">Goal</span><div class="fc-bar"><div class="fc-bar-fill" style="width:90%"></div></div></div>
          <div class="fc-bar-row"><span class="fc-bar-label">Users</span><div class="fc-bar"><div class="fc-bar-fill" style="width:72%"></div></div></div>
          <div class="fc-bar-row"><span class="fc-bar-label">Features</span><div class="fc-bar"><div class="fc-bar-fill" style="width:58%"></div></div></div>
          <div class="fc-bar-row"><span class="fc-bar-label">Timeline</span><div class="fc-bar"><div class="fc-bar-fill" style="width:38%"></div></div></div>
          <div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap">
            <span class="mini-chip chip-purple">42% complete</span>
            <span class="mini-chip chip-teal">3 questions left</span>
          </div>
        </div>
        <div class="float-card">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
            <div style="width:24px;height:24px;border-radius:8px;background:linear-gradient(135deg,#5b47e0,#9333ea);display:grid;place-items:center;color:#fff;font-size:10px;font-weight:800">AI</div>
            <span style="font-size:11px;font-weight:700;color:#4a4640">Scope Assistant</span>
          </div>
          <div style="font-size:12px;color:#4a4640;line-height:1.5">"What problem should this app solve first?"</div>
          <div style="display:flex;gap:4px;margin-top:8px">
            <div style="width:5px;height:5px;border-radius:50%;background:#5b47e0;animation:tdotBounce 1.2s ease-in-out infinite"></div>
            <div style="width:5px;height:5px;border-radius:50%;background:#5b47e0;animation:tdotBounce 1.2s ease-in-out infinite;animation-delay:.2s"></div>
            <div style="width:5px;height:5px;border-radius:50%;background:#5b47e0;animation:tdotBounce 1.2s ease-in-out infinite;animation-delay:.4s"></div>
          </div>
        </div>
        <div class="float-card">
          <div style="font-size:10px;font-weight:700;color:#7d7670;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px">Statement of Work</div>
          <div style="font-size:13px;font-weight:800;color:#1a1916;margin-bottom:8px">Client Portal Project</div>
          <span class="mini-chip chip-purple">SOW ready for review</span>
        </div>
      </div>
    </section>

    <!-- Workspace -->
    <div class="workspace">
      <!-- AI Intake Assistant -->
      <div class="card">
        <div class="assistant-head">
          <div class="ai-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div class="ai-meta">
            <div class="ai-name">Scope Assistant</div>
            <div class="ai-online"><span class="status-dot"></span>Ready to help</div>
          </div>
          <div class="step-tags" id="stepTags"></div>
        </div>

        <div class="prog-wrap">
          <div class="prog-top">
            <span class="prog-label" id="progressLabel">Step 1 of 6</span>
            <span class="prog-pct" id="progressPct">17%</span>
          </div>
          <div class="prog-rail"><div class="prog-fill" id="progressFill" style="width:17%"></div></div>
          <div class="step-dots" id="stepDots"></div>
        </div>

        <div class="msg-bubble">
          <strong>Tell me what you want to build.</strong> You can be rough &mdash; I'll ask follow-up questions and turn your answers into a clear project scope and Statement of Work.
        </div>

        <div class="thinking" id="thinkingEl">
          <div class="tdot"></div><div class="tdot"></div><div class="tdot"></div>
        </div>

        <div class="cq">
          <div class="cq-label"><span>&#10022;</span> Current question</div>
          <div class="cq-text" id="aiQuestion">What is the app, workflow, or tool you want us to help you build?</div>
          <div class="helper" id="helperText">This helps us define scope and understand the core purpose of your project.</div>
        </div>

        <!-- Step 0 -->
        <div id="step-0">
          <div class="frow">
            <div>
              <label class="flabel" for="title">Project title</label>
              <input id="title" placeholder="e.g. Sales onboarding automation" />
            </div>
            <div>
              <label class="flabel" for="request_type">Type of project</label>
              <select id="request_type">
                <option value="new_app">New app</option>
                <option value="workflow_automation">Workflow automation</option>
                <option value="dashboard_report">Dashboard / report</option>
                <option value="ai_assistant">AI assistant</option>
                <option value="integration">Integration</option>
                <option value="website_portal">Website / client portal</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
          <div>
            <label class="flabel" for="goal">What are you trying to achieve?</label>
            <textarea id="goal" placeholder="Describe the business problem in plain language. What outcome matters most?"></textarea>
          </div>
        </div>

        <!-- Step 1 -->
        <div id="step-1" class="hidden">
          <div class="fcol">
            <div>
              <label class="flabel" for="primary_users">Who are the primary users?</label>
              <textarea id="primary_users" placeholder="Who will use this? Teams, roles, or customer groups." style="min-height:80px"></textarea>
            </div>
            <div>
              <label class="flabel" for="user_actions">What do they need to do?</label>
              <textarea id="user_actions" placeholder="e.g. Submit requests, review approvals, track deliverables." style="min-height:80px"></textarea>
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div id="step-2" class="hidden">
          <div class="fcol">
            <div>
              <label class="flabel" for="current_process">What does the current process look like?</label>
              <textarea id="current_process" placeholder="Walk us through what happens today and where it breaks down." style="min-height:80px"></textarea>
            </div>
            <div>
              <label class="flabel" for="features">What features do you need?</label>
              <textarea id="features" placeholder="List must-haves first, then nice-to-haves." style="min-height:80px"></textarea>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div id="step-3" class="hidden">
          <div class="fcol">
            <div>
              <label class="flabel" for="systems">What systems should this connect to?</label>
              <textarea id="systems" placeholder="e.g. Salesforce, QuickBooks, Google Sheets, internal database." style="min-height:80px"></textarea>
            </div>
            <div>
              <label class="flabel" for="security">Any compliance or approval requirements?</label>
              <textarea id="security" placeholder="e.g. SOC 2, HIPAA, role-based access, legal sign-off." style="min-height:68px"></textarea>
            </div>
            <div>
              <label class="flabel" for="assets">References or examples</label>
              <textarea id="assets" placeholder="Links, docs, screenshots, or process notes." style="min-height:60px"></textarea>
            </div>
          </div>
        </div>

        <!-- Step 4 -->
        <div id="step-4" class="hidden">
          <div class="frow">
            <div>
              <label class="flabel" for="timeline">Timeline target</label>
              <input id="timeline" placeholder="e.g. Pilot in 6 weeks" />
            </div>
            <div>
              <label class="flabel" for="budget">Budget range</label>
              <input id="budget" placeholder="e.g. $25k&ndash;$40k" />
            </div>
          </div>
          <div style="margin-top:12px">
            <label class="flabel" for="success">Definition of success</label>
            <textarea id="success" placeholder="How will you know this was successful six months after launch?"></textarea>
          </div>
        </div>

        <!-- Step 5 -->
        <div id="step-5" class="hidden">
          <div class="status-msg success">Your intake is complete. Review the live brief on the right, then generate or refine your Statement of Work below.</div>
          <div style="margin-top:12px">
            <label class="flabel" for="project_brief_review">Final notes before submission</label>
            <textarea id="project_brief_review" placeholder="Any last details, priorities, or context for our team." style="min-height:80px"></textarea>
          </div>
        </div>

        <div class="chips-label" id="chipsLabel">Quick answers &mdash; click to add:</div>
        <div class="chips-row" id="quickChips"></div>

        <div class="ctrl-row">
          <div class="ctrl-left">
            <button class="btn btn-ghost" id="backBtn" disabled>&#8592; Back</button>
            <button class="btn btn-primary" id="nextBtn">Continue &#8594;</button>
          </div>
          <button class="btn btn-secondary" id="saveDraftBtn">Save draft</button>
        </div>
        <div class="status-msg hidden" id="statusMsg"></div>
      </div>

      <!-- Live Project Brief -->
      <aside>
        <div class="card">
          <div class="brief-head">
            <div>
              <div class="brief-label">Live Project Brief</div>
              <div class="brief-title">Your scope, as you answer</div>
            </div>
            <div class="orb-wrap">
              <svg viewBox="0 0 52 52">
                <defs>
                  <linearGradient id="og" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#5b47e0"/>
                    <stop offset="100%" stop-color="#9333ea"/>
                  </linearGradient>
                </defs>
                <circle class="orb-bg" cx="26" cy="26" r="21"/>
                <circle class="orb-fg" id="orbFg" cx="26" cy="26" r="21"/>
              </svg>
              <div class="orb-label" id="orbPct">0%</div>
            </div>
          </div>

          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Goal</span><span class="badge badge-empty" id="badgeGoal">Empty</span></div>
            <div class="brief-item-placeholder" id="briefGoal">What problem should this solve?</div>
          </div>
          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Users</span><span class="badge badge-empty" id="badgeUsers">Empty</span></div>
            <div class="brief-item-placeholder" id="briefUsers">Who will use this?</div>
          </div>
          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Core features</span><span class="badge badge-empty" id="badgeFeatures">Empty</span></div>
            <div class="brief-item-placeholder" id="briefFeatures">Must-have capabilities</div>
          </div>
          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Integrations</span><span class="badge badge-empty" id="badgeIntegrations">Empty</span></div>
            <div class="brief-item-placeholder" id="briefIntegrations">Systems to connect</div>
          </div>
          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Timeline</span><span class="badge badge-empty" id="badgeTimeline">Empty</span></div>
            <div class="brief-item-placeholder" id="briefTimeline">When do you need this?</div>
          </div>
          <div class="brief-item">
            <div class="brief-item-top"><span class="brief-item-key">Risks / assumptions</span></div>
            <div class="brief-item-placeholder" id="briefRisks" style="color:#7d7670">Will surface as you answer.</div>
          </div>

          <div class="followup-box">
            <div class="followup-title">&#10022; AI refining questions</div>
            <div id="followUpList"></div>
          </div>
        </div>
      </aside>
    </div>

    <!-- SOW Preview -->
    <section class="sow-wrap" id="sowSection">
      <div class="section-bar">
        <div>
          <div class="section-eyebrow">Generated Deliverable</div>
          <div class="section-title">Statement of Work Preview</div>
          <div class="section-sub">Review and edit before sharing with our team.</div>
        </div>
        <button class="btn btn-primary" id="generateSowBtn">&#10022; Generate SOW from intake</button>
      </div>
      <div class="sow-card">
        <div class="sow-bar">
          <div class="sow-bar-left">
            <div class="sow-icon">&#128196;</div>
            <div>
              <div class="sow-bar-title">Statement of Work</div>
              <div class="sow-bar-sub">Matt James Technology &mdash; Client Intake</div>
            </div>
          </div>
          <span class="sow-badge-el" id="sowBadge">&#9675; Draft</span>
        </div>
        <div class="sow-body" id="sowBody">
          <div class="sow-empty" id="sowEmptyState">
            <div class="sow-empty-icon">&#10022;</div>
            <div class="sow-empty-title">Your SOW will appear here</div>
            <div class="sow-empty-sub">Complete the intake and click Generate SOW to create a professional Statement of Work from your answers.</div>
            <button class="btn btn-primary" id="sowEmptyGenBtn">&#10022; Generate SOW from intake</button>
          </div>
          <div class="hidden" id="sowContent">
            <div class="sow-grid" id="sowGrid"></div>
          </div>
          <div class="hidden" id="sowShimmer">
            <div class="shimmer" style="width:55%;height:18px;margin-bottom:18px"></div>
            <div class="shimmer" style="width:100%"></div>
            <div class="shimmer" style="width:88%"></div>
            <div class="shimmer" style="width:95%;margin-top:18px;margin-bottom:8px"></div>
            <div class="shimmer" style="width:80%"></div>
            <div class="shimmer" style="width:90%"></div>
          </div>
        </div>
        <div class="sow-actions-bar">
          <button class="btn btn-primary" id="submitRequestBtn">Review and submit</button>
          <button class="btn btn-secondary" id="approveSowBtn">Approve SOW</button>
          <button class="btn btn-ghost" id="requestChangesBtn">Request changes</button>
        </div>
        <div class="status-msg hidden" id="sowStatusMsg" style="margin:0 28px 20px"></div>
      </div>
    </section>

    <!-- My Requests -->
    <section class="reqs-section" id="requestsSection">
      <div class="section-bar">
        <div>
          <div class="section-eyebrow">Project History</div>
          <div class="section-title">My Requests</div>
          <div class="section-sub">Continue drafts, review SOW progress, and track your projects.</div>
        </div>
        <button class="btn btn-secondary" id="refreshBtn">Refresh</button>
      </div>
      <div id="requestsGrid" class="reqs-grid"></div>
      <div id="requestsEmpty" class="empty-state">
        <div class="empty-icon">&#10022;</div>
        <div class="empty-title">No requests yet</div>
        <div class="empty-sub">Start your first AI intake and we'll help turn your idea into a build-ready project scope.</div>
        <button class="btn btn-primary" id="emptyStartBtn">Start AI intake &#8594;</button>
      </div>
    </section>

    <!-- SOW Review actions -->
    <section class="review-section card" id="reviewSection">
      <div class="section-bar" style="margin-bottom:16px">
        <div>
          <div class="section-eyebrow">Review Actions</div>
          <div class="section-title" style="font-size:20px">SOW Review</div>
          <div class="section-sub">Use this once a preview is ready from our team.</div>
        </div>
      </div>
      <div class="frow">
        <div>
          <label class="flabel" for="preview_request_select">Select request</label>
          <select id="preview_request_select"><option value="">Select a request...</option></select>
        </div>
        <div>
          <label class="flabel" for="preview_decision">Your decision</label>
          <select id="preview_decision">
            <option value="approve">Approve SOW</option>
            <option value="request_changes">Request changes</option>
            <option value="reject">Decline</option>
          </select>
        </div>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;align-items:center">
        <button class="btn btn-secondary" id="loadPreviewBtn">Load preview details</button>
        <a id="openPreviewLink" href="#" target="_blank" style="display:none" class="btn btn-ghost">Open preview &#8594;</a>
      </div>
      <div style="margin-top:14px">
        <label class="flabel" for="preview_feedback">Feedback for our team</label>
        <textarea id="preview_feedback" placeholder="Share what you want changed, clarified, or what you're approving." style="min-height:80px"></textarea>
      </div>
      <div style="margin-top:12px">
        <button class="btn btn-primary" id="submitDecisionBtn">Submit SOW decision</button>
      </div>
      <div class="status-msg hidden" id="previewMeta" style="margin-top:12px"></div>
    </section>

  </div>
</div>

<!-- Admin drawer -->
<div class="overlay" id="drawerOverlay"></div>
<aside class="drawer" id="settingsDrawer">
  <div class="drawer-head">
    <div>
      <div class="drawer-head-title">Admin / Developer Settings</div>
      <div class="drawer-head-sub">Internal configuration &mdash; not visible to clients</div>
    </div>
    <button class="btn btn-ghost" id="closeSettingsBtn" style="padding:8px 12px">&#10005;</button>
  </div>
  <div class="drawer-body">
    <div class="drawer-field">
      <label for="base_url">API Base URL</label>
      <input id="base_url" value="http://127.0.0.1:8000" />
    </div>
    <div class="drawer-field">
      <label for="api_key">API Key</label>
      <input id="api_key" type="password" placeholder="Internal API key" />
    </div>
    <div class="drawer-field">
      <label for="organization_id">Organization ID</label>
      <input id="organization_id" placeholder="Internal organization identifier" />
    </div>
    <div class="drawer-field">
      <label for="project_id">Project ID (optional)</label>
      <input id="project_id" placeholder="Optional internal project identifier" />
    </div>
  </div>
</aside>

<script>
  const STEPS = [0,1,2,3,4,5];
  const QUESTIONS = [
    "What is the app, workflow, or tool you want us to help you build?",
    "Who are the primary users, and what do they need to accomplish?",
    "What does your current process look like, and what needs to change first?",
    "What systems should this connect to, and what constraints matter?",
    "What timeline, budget, and success criteria guide this project?",
    "Ready to generate your Statement of Work?"
  ];
  const HELPERS = [
    "This helps us define scope and understand the core purpose of your project.",
    "Understanding users helps us design the right flows and interfaces.",
    "Knowing the current process reveals where to create the most value first.",
    "Integrations and compliance requirements shape the build plan.",
    "Timeline and success criteria anchor the scope and delivery milestones.",
    "Review your live project brief, then generate or edit your SOW."
  ];
  const STEP_LABELS = ["Basics","Users","Workflow","Systems","Delivery","Review"];
  const CHIPS = [
    ["Replace a manual process","Automate approvals","Create a client portal","Build an internal AI assistant","Connect existing systems","Generate reports"],
    ["Sales and ops teams","Customer success managers","Executive visibility","Clients need self-service","All internal staff"],
    ["Currently all email","Too many handoffs","No single source of truth","Approval takes too long","Data stuck in spreadsheets"],
    ["Salesforce","HubSpot","QuickBooks","Google Sheets","Slack","Internal database"],
    ["Pilot in 6 weeks","Launch this quarter","$10k-$25k","$25k-$50k","Success = faster turnaround"],
    ["Generate SOW now","Add final notes","Submit for review"]
  ];
  const CHIP_TARGETS = ["goal","primary_users","current_process","systems","success","project_brief_review"];

  let stepIndex = 0;
  let cachedRequests = [];
  let selectedPreviewBuild = null;
  let latestRequestId = null;
  let sowGenerated = false;

  const $ = id => document.getElementById(id);
  const val = id => { const el=$(id); return el && el.value ? el.value.trim() : ""; };

  function form() {
    return {
      title: val("title"), request_type: val("request_type"), goal: val("goal"),
      primary_users: val("primary_users"), user_actions: val("user_actions"),
      current_process: val("current_process"), features: val("features"),
      systems: val("systems"), assets: val("assets"), security: val("security"),
      timeline: val("timeline"), budget: val("budget"), success: val("success"),
      project_brief_review: val("project_brief_review")
    };
  }

  function requestPayload() {
    const f = form();
    const parts = [];
    if (f.primary_users) parts.push("Primary users:\\n" + f.primary_users);
    if (f.user_actions) parts.push("User actions:\\n" + f.user_actions);
    if (f.current_process) parts.push("Current process:\\n" + f.current_process);
    if (f.features) parts.push("Desired features:\\n" + f.features);
    if (f.systems) parts.push("Systems:\\n" + f.systems);
    if (f.assets) parts.push("References:\\n" + f.assets);
    if (f.security) parts.push("Security / compliance:\\n" + f.security);
    if (f.timeline) parts.push("Timeline:\\n" + f.timeline);
    if (f.budget) parts.push("Budget:\\n" + f.budget);
    if (f.success) parts.push("Definition of success:\\n" + f.success);
    if (f.project_brief_review) parts.push("Client notes:\\n" + f.project_brief_review);
    const payload = {
      organization_id: val("organization_id"),
      request_type: f.request_type || "new_app",
      title: f.title, goal: f.goal,
      details: parts.join("\\n\\n") || null
    };
    const pid = val("project_id");
    if (pid) payload.project_id = pid;
    return payload;
  }

  function completionPct() {
    const f = form();
    const fields = [f.title,f.goal,f.primary_users,f.user_actions,f.current_process,f.features,f.systems,f.security,f.timeline,f.success];
    return Math.round(fields.filter(Boolean).length / fields.length * 100);
  }

  function humanType(v) {
    return ({new_app:"New app",workflow_automation:"Workflow automation",dashboard_report:"Dashboard / report",ai_assistant:"AI assistant",integration:"Integration",website_portal:"Website / portal",update:"Update",bugfix:"Bug fix",enhancement:"Enhancement",other:"Other"})[v] || v || "Unspecified";
  }

  function humanStatus(s) {
    return ({draft:"Draft",submitted:"Submitted",triaged:"Needs detail",building:"In review",preview_ready:"SOW ready for review",client_review:"SOW ready for review",changes_requested:"Changes requested",approved:"Approved",rejected:"Changes requested"})[s] || String(s||"draft").replace(/_/g," ");
  }

  function statusClass(s) {
    const h = humanStatus(s).toLowerCase();
    if (h.includes("draft")) return "rb-draft";
    if (h.includes("approved")) return "rb-approved";
    if (h.includes("changes")) return "rb-changes";
    if (h.includes("review")||h.includes("sow")) return "rb-review";
    return "rb-submitted";
  }

  function actionLabel(s) {
    const h = humanStatus(s).toLowerCase();
    if (h.includes("draft")||h.includes("detail")) return "Continue";
    if (h.includes("sow")||h.includes("review")) return "Review SOW";
    return "View details";
  }

  function decisionToStatus(d) {
    if (d==="approve") return "approved";
    if (d==="request_changes") return "changes_requested";
    return "rejected";
  }

  function showStatus(elId, text, type) {
    const el = $(elId);
    if (!el) return;
    el.classList.remove("hidden","success","warning");
    if (type) el.classList.add(type);
    el.textContent = text;
  }

  function buildFollowUps() {
    const f = form();
    const q = [];
    if (!f.primary_users) q.push("Who are the primary users we should prioritise?");
    if (!f.current_process) q.push("What does your current workflow look like today?");
    if (!f.systems) q.push("What systems does this need to connect with?");
    if (!f.success) q.push("What would make this successful after launch?");
    if (!f.security) q.push("Any compliance, privacy, or approval requirements?");
    if (!f.timeline) q.push("When do you need an initial version in users' hands?");
    if (!q.length) q.push("Great detail! Do you want a pilot-first or full launch plan?");
    return q.slice(0,4);
  }

  function updateBrief() {
    const f = form();
    const pct = completionPct();
    const circ = 2 * Math.PI * 21;
    const offset = circ - (pct / 100) * circ;
    const fg = $("orbFg");
    if (fg) { fg.style.strokeDasharray = circ; fg.style.strokeDashoffset = offset; }
    if ($("orbPct")) $("orbPct").textContent = pct + "%";

    function setItem(valId, badgeId, value, placeholder) {
      const el = $(valId), badge = $(badgeId);
      if (!el) return;
      if (value) {
        el.textContent = value;
        el.className = "brief-item-val";
        if (badge) { badge.textContent = "Ready"; badge.className = "badge badge-ready"; }
      } else {
        el.textContent = placeholder;
        el.className = "brief-item-placeholder";
        if (badge) { badge.textContent = "Empty"; badge.className = "badge badge-empty"; }
      }
    }

    setItem("briefGoal","badgeGoal",f.goal,"What problem should this solve?");
    setItem("briefUsers","badgeUsers",f.primary_users,"Who will use this?");
    setItem("briefFeatures","badgeFeatures",f.features,"Must-have capabilities");
    setItem("briefIntegrations","badgeIntegrations",f.systems,"Systems to connect");
    setItem("briefTimeline","badgeTimeline",f.timeline,"When do you need this?");

    const risks = [];
    if (!f.security) risks.push("Security / compliance requirements still needed.");
    if (!f.timeline) risks.push("Timeline not yet defined.");
    if (!f.budget) risks.push("Budget not yet clarified.");
    const re = $("briefRisks");
    if (re) {
      re.textContent = risks.length ? risks.join(" ") : "Key constraints are documented.";
      re.style.fontStyle = risks.length ? "italic" : "normal";
      re.style.color = risks.length ? "#7d7670" : "#4a4640";
    }

    const list = $("followUpList");
    if (list) {
      list.innerHTML = buildFollowUps().map(q =>
        '<div class="followup-item"><span class="followup-arrow">&#8594;</span><span>' + q + '</span></div>'
      ).join("");
    }
  }

  function buildStepDots() {
    const wrap = $("stepDots");
    if (!wrap) return;
    wrap.innerHTML = STEPS.map(i =>
      '<div class="step-dot' + (i < stepIndex ? " done" : i === stepIndex ? " active" : "") + '"></div>'
    ).join("");
  }

  function buildStepTags() {
    const wrap = $("stepTags");
    if (!wrap) return;
    wrap.innerHTML = STEP_LABELS.map((label, i) => {
      let style = "";
      if (i === stepIndex) style = "border-color:rgba(91,71,224,.4);color:#5b47e0;background:#f0edfb";
      else if (i < stepIndex) style = "border-color:#86efac;color:#15803d;background:#f0fdf4";
      else style = "border-color:#e6dfd5;color:#7d7670;background:#fdfaf7";
      return '<span class="step-tag" style="' + style + '">' + label + '</span>';
    }).join("");
  }

  function buildQuickChips() {
    const wrap = $("quickChips");
    const label = $("chipsLabel");
    if (!wrap) return;
    const suggestions = CHIPS[stepIndex] || [];
    if (!suggestions.length) { wrap.innerHTML = ""; if (label) label.style.display = "none"; return; }
    if (label) label.style.display = "block";
    wrap.innerHTML = suggestions.map(text =>
      '<button class="chip" data-text="' + text.replace(/"/g,"&quot;") + '">' + text + '</button>'
    ).join("");
    wrap.querySelectorAll(".chip").forEach(btn => {
      btn.addEventListener("click", () => {
        const target = CHIP_TARGETS[stepIndex];
        const field = $(target);
        if (!field) return;
        const t = btn.getAttribute("data-text");
        field.value = field.value ? field.value + "\\n- " + t : t;
        field.dispatchEvent(new Event("input"));
        btn.style.borderColor = "var(--accent)";
        btn.style.color = "var(--accent)";
        btn.style.background = "var(--accent-soft)";
      });
    });
  }

  function showThinking(on) {
    const el = $("thinkingEl");
    if (el) el.classList.toggle("on", on);
  }

  function updateStepUi() {
    STEPS.forEach(i => {
      const el = $("step-" + i);
      if (el) el.classList.toggle("hidden", i !== stepIndex);
    });
    if ($("backBtn")) $("backBtn").disabled = stepIndex === 0;
    if ($("nextBtn")) $("nextBtn").textContent = stepIndex === 5 ? "&#10022; Generate SOW" : "Continue &#8594;";
    if ($("aiQuestion")) $("aiQuestion").textContent = QUESTIONS[stepIndex];
    if ($("helperText")) $("helperText").textContent = HELPERS[stepIndex];
    if ($("progressLabel")) $("progressLabel").textContent = "Step " + (stepIndex + 1) + " of 6";
    if ($("progressPct")) $("progressPct").textContent = Math.round((stepIndex + 1) / STEPS.length * 100) + "%";
    if ($("progressFill")) $("progressFill").style.width = ((stepIndex + 1) / STEPS.length * 100) + "%";
    buildStepDots();
    buildStepTags();
    buildQuickChips();
    updateBrief();
    if (stepIndex === 5 && !sowGenerated) {
      showThinking(true);
      setTimeout(() => { showThinking(false); generateSowPreview(); }, 1100);
    }
  }

  function generateSowPreview() {
    const f = form();
    const followUps = buildFollowUps();
    if ($("sowEmptyState")) $("sowEmptyState").classList.add("hidden");
    if ($("sowContent")) $("sowContent").classList.add("hidden");
    if ($("sowShimmer")) $("sowShimmer").classList.remove("hidden");

    setTimeout(() => {
      if ($("sowShimmer")) $("sowShimmer").classList.add("hidden");
      if ($("sowContent")) $("sowContent").classList.remove("hidden");

      const fields = [
        ["full","Executive Summary","sowExecutive",
          (f.title || "Requested project") + " is a " + humanType(f.request_type).toLowerCase() + " initiative. " +
          (f.goal || "The goal is to solve the stated business challenge.") +
          " This document outlines the agreed scope, deliverables, and timeline required to bring this project to completion."],
        ["","Project Objectives","sowObjectives",
          "1. Define and document all business requirements for launch readiness.\\n2. Design user-friendly workflows for " + (f.primary_users || "target users") + ".\\n3. Prioritise quick wins while building a scalable foundation."],
        ["","Scope of Work","sowScope",
          "- Discovery and requirement refinement\\n- UX workflow and intake-to-delivery blueprint\\n- Build and configure priority feature set\\n- Stakeholder review and revision cycle"],
        ["","Key Features","sowFeatures", f.features || "Feature list to be finalised from intake."],
        ["","User Roles","sowRoles", f.primary_users || "User roles to be confirmed."],
        ["","Integrations","sowIntegrations", f.systems || "Integration details to be confirmed."],
        ["","Deliverables","sowDeliverables",
          "- Approved project brief\\n- Statement of Work\\n- Interactive build plan\\n- Delivery roadmap and milestones"],
        ["","Timeline / Milestones","sowTimeline", f.timeline || "Timeline to be finalised after scoping workshop."],
        ["","Assumptions","sowAssumptions",
          f.security ? "Assumes requirements include: " + f.security : "Assumes standard security and access controls unless otherwise specified."],
        ["","Out of Scope","sowOutOfScope",
          "Long-term support, third-party licensing fees, and non-approved integrations."],
        ["","Acceptance Criteria","sowAcceptance", f.success || "Acceptance criteria to be finalised during scope review."],
        ["","Client Responsibilities","sowResponsibilities",
          "Client provides timely feedback, stakeholder approvals, and required system access."],
        ["","Open Questions","sowOpenQuestions", followUps.join("\\n")],
        ["","Pricing","sowPricing", "To be estimated after full scope review."]
      ];

      const grid = $("sowGrid");
      if (!grid) return;
      grid.innerHTML = fields.map(([cls, label, id, v]) =>
        '<div class="sow-field' + (cls === "full" ? " full" : "") + '">' +
        '<div class="sow-field-label">' + label + '</div>' +
        '<textarea class="sow-textarea" id="' + id + '">' + v + '</textarea>' +
        '</div>'
      ).join("");

      sowGenerated = true;
      if ($("sowBadge")) $("sowBadge").innerHTML = '<span style="color:#86efac">&#9679;</span> Generated draft';
    }, 900);
  }

  async function submitRequest() {
    const payload = requestPayload();
    const base = val("base_url"), key = val("api_key");
    if (!payload.organization_id || !payload.title || !payload.goal) {
      showStatus("sowStatusMsg","Please complete project title, goal, and open admin settings to set your organisation before submitting.","warning");
      $("sowStatusMsg") && $("sowStatusMsg").classList.remove("hidden");
      return;
    }
    showStatus("sowStatusMsg","Submitting your request...","");
    $("sowStatusMsg") && $("sowStatusMsg").classList.remove("hidden");
    if (!window.confirm("Submit this project brief for review now?")) {
      showStatus("sowStatusMsg","Submission cancelled. Your draft is still here.","warning");
      return;
    }
    try {
      const res = await fetch(base + "/v1/intake-requests", {
        method:"POST",
        headers:{"Content-Type":"application/json","X-API-Key":key,"Idempotency-Key":"client-req-" + Date.now()},
        body: JSON.stringify(payload)
      });
      const body = await res.json();
      if (res.ok) {
        latestRequestId = body && body.id ? body.id : null;
        showStatus("sowStatusMsg","Request submitted. Our team will review and return with next steps.","success");
        stepIndex = 0;
        updateStepUi();
        await refreshRequests();
      } else {
        showStatus("sowStatusMsg","Submission failed: " + (body?.error?.message || "Please try again."),"warning");
      }
    } catch (_) {
      showStatus("sowStatusMsg","Submission failed due to a network error. Please try again.","warning");
    }
  }

  async function refreshRequests() {
    const base = val("base_url"), key = val("api_key"), orgId = val("organization_id");
    const grid = $("requestsGrid"), empty = $("requestsEmpty"), sel = $("preview_request_select");
    if (!orgId) {
      if (grid) grid.innerHTML = "";
      if (empty) empty.classList.remove("hidden");
      if (sel) sel.innerHTML = '<option value="">Select a request...</option>';
      cachedRequests = [];
      return;
    }
    try {
      const res = await fetch(base + "/v1/intake-requests?organization_id=" + encodeURIComponent(orgId), {headers:{"X-API-Key":key}});
      const body = await res.json();
      if (!res.ok || !Array.isArray(body) || !body.length) {
        if (grid) grid.innerHTML = "";
        if (empty) empty.classList.remove("hidden");
        if (sel) sel.innerHTML = '<option value="">Select a request...</option>';
        cachedRequests = [];
        return;
      }
      cachedRequests = body;
      if (empty) empty.classList.add("hidden");
      if (sel) sel.innerHTML = '<option value="">Select a request...</option>' +
        body.map(r => '<option value="' + r.id + '">' + r.title + " (" + humanStatus(r.status) + ")</option>").join("");
      if (grid) {
        grid.innerHTML = body.map(r =>
          '<div class="req-card">' +
          '<div class="req-top">' +
          '<div><div class="req-title">' + r.title + '</div><div class="req-type">' + humanType(r.request_type) + "</div></div>" +
          '<span class="req-badge ' + statusClass(r.status) + '">' + humanStatus(r.status) + "</span>" +
          "</div>" +
          '<div class="req-meta">Updated ' + r.updated_at + "</div>" +
          '<div class="req-footer">' +
          '<button class="req-action request-action" data-id="' + r.id + '">' + actionLabel(r.status) + "</button>" +
          "</div></div>"
        ).join("");
        grid.querySelectorAll(".request-action").forEach(btn => {
          btn.addEventListener("click", () => {
            if ($("preview_request_select")) $("preview_request_select").value = btn.getAttribute("data-id");
            $("reviewSection") && $("reviewSection").scrollIntoView({behavior:"smooth",block:"start"});
          });
        });
      }
    } catch (_) {
      if (grid) grid.innerHTML = "";
      if (empty) empty.classList.remove("hidden");
      if (sel) sel.innerHTML = '<option value="">Select a request...</option>';
      cachedRequests = [];
    }
  }

  async function loadPreview() {
    const base = val("base_url"), key = val("api_key");
    const intakeId = val("preview_request_select");
    const link = $("openPreviewLink");
    selectedPreviewBuild = null;
    if (link) link.style.display = "none";
    if (!intakeId) {
      showStatus("previewMeta","Select a request first.","warning");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
      return;
    }
    try {
      const res = await fetch(base + "/v1/preview-builds?intake_request_id=" + encodeURIComponent(intakeId), {headers:{"X-API-Key":key}});
      const body = await res.json();
      if (!res.ok || !Array.isArray(body) || !body.length) {
        showStatus("previewMeta","No preview available yet for this request.","warning");
        $("previewMeta") && $("previewMeta").classList.remove("hidden");
        return;
      }
      selectedPreviewBuild = body[0];
      if (link) { link.href = selectedPreviewBuild.preview_url; link.style.display = "inline-flex"; }
      showStatus("previewMeta","Preview ready: version " + selectedPreviewBuild.build_version + ". Open the preview link to review.","success");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
    } catch (_) {
      showStatus("previewMeta","Could not load preview. Please try again.","warning");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
    }
  }

  async function submitDecision() {
    const base = val("base_url"), key = val("api_key");
    const intakeId = val("preview_request_select") || latestRequestId;
    const decision = val("preview_decision"), feedback = val("preview_feedback");
    if (!intakeId) {
      showStatus("previewMeta","Select a request first.","warning");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
      return;
    }
    if (decision !== "approve" && !window.confirm("This decision may require additional revisions. Continue?")) {
      showStatus("previewMeta","Decision cancelled.","warning");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
      return;
    }
    try {
      const res = await fetch(base + "/v1/intake-requests/" + intakeId + "/status", {
        method:"POST",
        headers:{"Content-Type":"application/json","X-API-Key":key,"Idempotency-Key":"decision-" + intakeId + "-" + Date.now()},
        body: JSON.stringify({status: decisionToStatus(decision), feedback: feedback || null})
      });
      const body = await res.json();
      if (res.ok) {
        const msgs = {approve:"Approved. Our team will continue to the next stage.",request_changes:"Changes requested. Your feedback has been shared.",reject:"Declined. Your team has been notified."};
        showStatus("previewMeta", msgs[decision] || "Decision submitted.","success");
        if ($("sowStatusMsg")) {
          showStatus("sowStatusMsg", decision === "approve" ? "SOW approved — our team will reach out with next steps." : "Feedback submitted to our team.", decision === "approve" ? "success" : "warning");
          $("sowStatusMsg").classList.remove("hidden");
        }
        $("previewMeta") && $("previewMeta").classList.remove("hidden");
        await refreshRequests();
      } else {
        showStatus("previewMeta","Decision failed: " + (body?.error?.message || "Please try again."),"warning");
        $("previewMeta") && $("previewMeta").classList.remove("hidden");
      }
    } catch (_) {
      showStatus("previewMeta","Decision failed due to a network error.","warning");
      $("previewMeta") && $("previewMeta").classList.remove("hidden");
    }
  }

  function openSettings() { $("settingsDrawer").classList.add("open"); $("drawerOverlay").classList.add("open"); }
  function closeSettings() { $("settingsDrawer").classList.remove("open"); $("drawerOverlay").classList.remove("open"); }
  function scrollToIntake() { window.scrollTo({top:0,behavior:"smooth"}); $("title") && $("title").focus(); }

  function bindFields() {
    ["title","request_type","goal","primary_users","user_actions","current_process","features","systems","assets","security","timeline","budget","success","project_brief_review"].forEach(id => {
      const el = $(id);
      if (el) el.addEventListener("input", updateBrief);
    });
  }

  $("backBtn").addEventListener("click", () => { if (stepIndex > 0) { stepIndex--; updateStepUi(); } });
  $("nextBtn").addEventListener("click", () => {
    if (stepIndex < 5) { stepIndex++; updateStepUi(); return; }
    generateSowPreview();
    $("sowSection") && $("sowSection").scrollIntoView({behavior:"smooth",block:"start"});
  });
  $("saveDraftBtn").addEventListener("click", () => {
    showStatus("statusMsg","Draft saved. Continue whenever you're ready.","success");
    $("statusMsg") && $("statusMsg").classList.remove("hidden");
  });
  $("generateSowBtn").addEventListener("click", generateSowPreview);
  $("sowEmptyGenBtn") && $("sowEmptyGenBtn").addEventListener("click", generateSowPreview);
  $("submitRequestBtn").addEventListener("click", submitRequest);
  $("approveSowBtn").addEventListener("click", () => { if ($("preview_decision")) $("preview_decision").value = "approve"; submitDecision(); });
  $("requestChangesBtn").addEventListener("click", () => { if ($("preview_decision")) $("preview_decision").value = "request_changes"; submitDecision(); });
  $("refreshBtn").addEventListener("click", refreshRequests);
  $("loadPreviewBtn").addEventListener("click", loadPreview);
  $("submitDecisionBtn").addEventListener("click", submitDecision);
  $("openSettingsBtn").addEventListener("click", openSettings);
  $("closeSettingsBtn").addEventListener("click", closeSettings);
  $("drawerOverlay").addEventListener("click", closeSettings);
  $("heroStartBtn").addEventListener("click", scrollToIntake);
  $("navStartBtn").addEventListener("click", scrollToIntake);
  $("emptyStartBtn") && $("emptyStartBtn").addEventListener("click", scrollToIntake);
  $("heroRequestsBtn").addEventListener("click", () => $("requestsSection") && $("requestsSection").scrollIntoView({behavior:"smooth",block:"start"}));
  $("navRequestsBtn").addEventListener("click", () => $("requestsSection") && $("requestsSection").scrollIntoView({behavior:"smooth",block:"start"}));
  $("navSowBtn").addEventListener("click", () => $("sowSection") && $("sowSection").scrollIntoView({behavior:"smooth",block:"start"}));
  $("navHelpBtn").addEventListener("click", () => { showStatus("statusMsg","Start with your business goal and our assistant will guide the rest.","success"); $("statusMsg") && $("statusMsg").classList.remove("hidden"); });

  bindFields();
  updateStepUi();
  refreshRequests();
</script>
</body>
</html>
"""
