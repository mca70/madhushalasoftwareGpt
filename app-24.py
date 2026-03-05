import sys
import os
import re
import threading
import webbrowser
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

KNOWLEDGE_BASE = [
    {
        "keywords": ["hi","hello","hey","helo","hii","hai","start","help me","good morning","good evening","good afternoon","namaste"],
        "label": None, "link": None,
        "reply": """Hello! Welcome to <strong>madhushalasoftwareGpt</strong> &#127863;<br><br>
How can I help you today?<br><br>
&#127760; <strong>Our Social Media &amp; Links:</strong><br>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;">
<a class="social-btn" href="https://madhushalasoftware.com/" target="_blank">&#127760; madhushalasoftware.com</a>
<a class="social-btn" href="https://abmtechno.com/" target="_blank">&#128187; abmtechno.com</a>
<a class="social-btn" href="https://www.youtube.com/results?search_query=abm+technomatrix+youtube+channel" target="_blank">&#127910; YouTube</a>
<a class="social-btn" href="https://snapkey.in/sandminingpage/" target="_blank">&#128273; Snapkey</a>
<a class="social-btn" href="https://www.facebook.com/madhushalasoftware1330/followers/" target="_blank">&#128241; Facebook</a>
</div>"""
    },
    {
        "keywords": ["support crm","support dashboard","support login","crm support"],
        "label": "Support CRM Login",
        "link": "http://13.235.37.46:8082/home/SupportDashboard",
        "reply": "Here is your <strong>Support CRM Login Link</strong>. Click below to open the Support Dashboard."
    },
    {
        "keywords": ["snapkey crm","crm snapkey","snapkey login","snapkey crm login","snapkey"],
        "label": "CRM Snapkey Login",
        "link": "https://crm.snapkey.in/login.html",
        "reply": "Here is your <strong>CRM Snapkey Login Link</strong>. Click below to open the Snapkey CRM."
    },
    {
        "keywords": ["email format","email formate","email template","client email","email all clients"],
        "label": "Email Format for All Clients",
        "link": "https://docs.google.com/document/d/1T4Uahnc3FPoXB5H-YAc_E9a46bk1hiUI_5WV5r3qLkQ/edit?usp=drive_link",
        "reply": "Here is the <strong>Email Format for All Clients</strong>. Click below to open the Google Doc."
    },
    {
        "keywords": ["madhushala setup","setup file","madhushala setup file"],
        "label": "Madhushala Setup File",
        "link": "https://drive.google.com/file/d/1_qzBKL2Ms-l4_IgYz3PC5fDjYNcHhLHF/view?usp=sharing",
        "reply": "Here is your <strong>Madhushala Setup File</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["restaurant setup","resturent setup","restaurant setup file","resturent setup file"],
        "label": "Restaurant Setup File",
        "link": "https://drive.google.com/file/d/1Pr30GKBuXccLi3G_42jji8EK2Nzj8y6s/view?usp=sharing",
        "reply": "Here is your <strong>Restaurant Setup File</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["pos setup","madhushala pos setup","pos setup file"],
        "label": "Madhushala POS Setup File",
        "link": "https://drive.google.com/file/d/13f6ZbhX37hiMGYwiDNxBH6ppmrN_5pzN/view?usp=sharing",
        "reply": "Here is your <strong>Madhushala POS Setup File</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["delhi pos","delhi pos setup","madhushala delhi pos"],
        "label": "Madhushala Delhi POS Setup File",
        "link": "https://drive.google.com/file/d/1P5A63kBNHMquOVRmyPOCLdpF1k4Z9bv2/view?usp=sharing",
        "reply": "Here is your <strong>Madhushala Delhi POS Setup File</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["madhushala downloader","downloader"],
        "label": "Madhushala Downloader",
        "link": "https://drive.google.com/file/d/1n0LYQUndkMcxhCZQwKTp3NOUS-UqTSkq/view?usp=drive_link",
        "reply": "Here is the <strong>Madhushala Downloader</strong>. Click below to access from Google Drive."
    },
    {
        "keywords": ["pos downloader","madhushala pos downloader","pos download"],
        "label": "Madhushala POS Downloader",
        "link": "https://drive.google.com/file/d/1d0H0cNj6UiueNF33dIg8NWzNemVAqGeY/view?usp=sharing",
        "reply": "Here is your <strong>Madhushala POS Downloader</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["all database query","all db query","madhushala all database","all database","all query"],
        "label": "Madhushala ALL Database Query",
        "link": "https://drive.google.com/file/d/1OAbJMOMCUuw90cvbyuV261hC4M-CgXRH/view?usp=sharing",
        "reply": "Here is the <strong>Madhushala ALL Database Query</strong> file. Click below to access it from Google Drive."
    },
    {
        "keywords": ["database delete","madhushala database delete","db delete","database delete query"],
        "label": "Madhushala Database Delete Query",
        "link": "https://drive.google.com/file/d/1MsvCNoVDbBwqff9YdNv4hA1Db8U3xDhC/view?usp=drive_link",
        "reply": "Here is the <strong>Madhushala Database Delete Query</strong>. Click below to access it."
    },
    {
        "keywords": ["pos database","pos delete","madhushala pos delete","pos db"],
        "label": "Madhushala POS Database Delete Query",
        "link": "https://drive.google.com/file/d/1dmKh_wwE0BZBs1CXV-b1yYX-nO4qwdPj/view?usp=drive_link",
        "reply": "Here is the <strong>Madhushala POS Database Delete Query</strong>. Click below to open it."
    },
    {
        "keywords": ["restro","restaurant delete","delete query restro","restro delete"],
        "label": "Madhushala Database Delete Query (Restro)",
        "link": "https://drive.google.com/file/d/1XRNv6VTNkTKmpbe5bsoDD7vwNGF3DGfx/view?usp=sharing",
        "reply": "Here is the <strong>Madhushala Database Delete Query - Restro</strong>. Click to view it."
    },
    {
        "keywords": ["manual sql","manual installation sql","sql manual","sql 2014 manual"],
        "label": None, "link": None,
        "reply": """Here are the files for <strong>Manual Installation of Microsoft SQL Server 2014</strong>:<br><br>
<a class="drive-btn" href="https://drive.google.com/file/d/1WaaYOZv6Xs58ysWIPAi3SRC8Zm_NDTig/view?usp=sharing" target="_blank">&#128190; Download SQLEXPR</a><br>
<a class="drive-btn" href="https://drive.google.com/file/d/1SO2jdt3mlnGY3UTh8oPJoyKoXaBOWbLd/view?usp=sharing" target="_blank" style="margin-top:8px;display:inline-block;">&#128190; Download SQL Management Studio</a><br>
<a class="drive-btn" href="https://drive.google.com/file/d/1gl-wYt_eQ9CWhVd2RfW8bBwF4f9pU5nF/view?usp=sharing" target="_blank" style="margin-top:8px;display:inline-block;">&#128190; SAP Crystal Reports 13.0 Runtime (32-bit)</a>"""
    },
    {
        "keywords": ["automatic sql","auto sql","sql automatic","sql 2014 automatic"],
        "label": "SQL Server 2014 Automatic Installer",
        "link": "https://drive.google.com/file/d/166QAJfrXCeoz4dPdnL81kPDqHLX9uXGW/view?usp=sharing",
        "reply": "Here is the <strong>Automatic Microsoft SQL Server 2014 Installer</strong>. Click below to download."
    },
    {
        "keywords": ["ms office","office 2010","ms office 2010"],
        "label": "MS Office 2010 (32-bit)",
        "link": "https://drive.google.com/file/d/1nmWv6DGZzwiOH7gRM40sH9teD9i68QVy/view?usp=sharing",
        "reply": "Here is <strong>MS Office 2010 (32-bit)</strong>. Click below to download from Google Drive."
    },
    {
        "keywords": ["accessdatabaseengine","access database engine","access db engine","database engine"],
        "label": None, "link": None,
        "reply": """Here are the <strong>Access Database Engine</strong> download links:<br><br>
<a class="drive-btn" href="https://drive.google.com/file/d/186_W2HsrajVWB8Y4jC-S789IjNGgL3sD/view?usp=sharing" target="_blank">&#128190; AccessDatabaseEngine 32-bit</a><br>
<a class="drive-btn" href="https://drive.google.com/file/d/11KDwuAsYIOpbSYXD5V4tonYr1A0yPFEH/view?usp=sharing" target="_blank" style="margin-top:8px;display:inline-block;">&#128190; AccessDatabaseEngine 64-bit</a>"""
    },
    {
        "keywords": ["epos qr","qr code error","epos qr code","epos dll","qr dll"],
        "label": "EPOS QR Code DLL Fix",
        "link": "https://drive.google.com/file/d/1enUcPnxlR3iMMuZEyDNmD5Y2dNDCykHi/view?usp=sharing",
        "reply": "Here is the <strong>EPOS QR Code DLL Fix</strong> file. Click below to download."
    },
    {
        "keywords": ["ledger error","ledger issue","ledger edit","invalid column","disc error","column disc","ledger problem"],
        "label": None, "link": None,
        "reply": """&#9888;&#65039; <strong>Problem Detected: Ledger Edit Issue</strong><br><br>
<div class="solution-box">
  <div class="solution-title">&#128295; How to Fix &mdash; Follow These Steps:</div>
  <div class="solution-step"><span class="step-num">1</span>Turn <strong>OFF</strong> the Madhushala application.</div>
  <div class="solution-step"><span class="step-num">2</span>Run the <strong>Madhushala Downloader</strong>.</div>
  <div class="solution-step"><span class="step-num">3</span>Open <strong>Admin Section</strong> &rarr; <strong>Parameters</strong> &rarr; <strong>Utilities Section</strong>.</div>
  <div class="solution-step"><span class="step-num">4</span>Click <strong>Update Database Structure</strong> &rarr; click <strong>Save</strong>.</div>
  <div class="solution-step"><span class="step-num">5</span>Turn the <strong>Madhushala Software ON</strong> again.</div>
</div>"""
    },
]

def match_query(user_input):
    lower = user_input.lower().strip()

    # ── Greetings first ───────────────────────────────────────────
    greet_words = ["hi","hello","hey","helo","hii","hai","start","namaste",
                   "good morning","good evening","good afternoon","help me"]
    for gw in greet_words:
        if re.search(r'\b' + re.escape(gw) + r'\b', lower):
            return KNOWLEDGE_BASE[0]

    # ── Priority checks (specific before generic) ─────────────────

    # Snapkey before generic CRM
    for kw in ["snapkey crm","crm snapkey","snapkey login","snapkey crm login","snapkey"]:
        if kw in lower:
            return KNOWLEDGE_BASE[2]

    # Restaurant Setup before generic Madhushala Setup
    for kw in ["restaurant setup","resturent setup","restaurant setup file","resturent setup file"]:
        if kw in lower:
            return KNOWLEDGE_BASE[5]

    # Delhi POS before generic POS Setup
    for kw in ["delhi pos","delhi pos setup","madhushala delhi pos"]:
        if kw in lower:
            return KNOWLEDGE_BASE[7]

    # POS Setup before generic Madhushala Setup
    for kw in ["pos setup","madhushala pos setup","pos setup file"]:
        if kw in lower:
            return KNOWLEDGE_BASE[6]

    # POS Downloader before generic Downloader
    for kw in ["pos downloader","madhushala pos downloader","pos download"]:
        if kw in lower:
            return KNOWLEDGE_BASE[9]

    # ALL Database Query before specific delete queries
    for kw in ["all database query","all db query","madhushala all database","all database","all query"]:
        if kw in lower:
            return KNOWLEDGE_BASE[10]  # ALL DB Query is now index 10

    # POS Delete before generic DB Delete
    for kw in ["pos database","pos delete","madhushala pos delete","pos db"]:
        if kw in lower:
            return KNOWLEDGE_BASE[12]

    # Restro Delete before generic DB Delete
    for kw in ["restro","restaurant delete","delete query restro","restro delete"]:
        if kw in lower:
            return KNOWLEDGE_BASE[13]

    # ── General loop ──────────────────────────────────────────────
    for item in KNOWLEDGE_BASE[1:]:
        for keyword in item["keywords"]:
            if keyword in lower:
                return item
    return None

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>madhushalasoftwareGpt</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',sans-serif; height:100vh; background:#faf7f4; display:flex; flex-direction:column; overflow:hidden; }
  .topbar { display:flex; align-items:center; justify-content:space-between; padding:14px 28px; background:#fff; border-bottom:1px solid #ede8e2; box-shadow:0 1px 4px #00000010; flex-shrink:0; }
  .topbar-left { display:flex; align-items:center; gap:12px; }
  .logo-icon { width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg,#b84a00,#7c2000); display:flex; align-items:center; justify-content:center; font-size:18px; color:#ffd580; }
  .logo-text { font-size:16px; font-weight:700; color:#2d1200; }
  .logo-sub  { font-size:11px; color:#a07060; margin-top:1px; }
  .topbar-right { display:flex; gap:8px; }
  .top-btn { padding:7px 16px; border-radius:8px; font-size:13px; font-weight:500; border:1px solid #e0d0c0; background:#fff; color:#7c3000; cursor:pointer; transition:all .2s; font-family:'Inter',sans-serif; }
  .top-btn:hover { background:#fff4ee; border-color:#b84a00; }
  .top-btn.primary { background:linear-gradient(135deg,#b84a00,#7c2000); color:#fff; border:none; }
  .top-btn.primary:hover { opacity:.9; }
  .main { flex:1; display:flex; flex-direction:column; align-items:center; overflow:hidden; }
  #chatbox { flex:1; width:100%; max-width:740px; overflow-y:auto; padding:30px 20px 10px; display:flex; flex-direction:column; gap:20px; scroll-behavior:smooth; }
  #chatbox::-webkit-scrollbar { width:4px; }
  #chatbox::-webkit-scrollbar-thumb { background:#e0c8b0; border-radius:4px; }
  .welcome-center { display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; flex:1; padding:30px 20px 10px; gap:12px; }
  .welcome-icon { width:64px; height:64px; border-radius:18px; background:linear-gradient(135deg,#b84a00,#7c2000); display:flex; align-items:center; justify-content:center; font-size:30px; box-shadow:0 6px 24px #b84a0030; margin-bottom:4px; }
  .welcome-title { font-size:28px; font-weight:700; color:#2d1200; font-family:'Playfair Display',serif; }
  .welcome-sub { font-size:14.5px; color:#a07060; max-width:460px; line-height:1.6; }
  .quick-chips { display:flex; flex-wrap:wrap; justify-content:center; gap:8px; margin-top:8px; max-width:640px; }
  .qchip { background:#fff; border:1.5px solid #e8d8cc; color:#7c3000; border-radius:22px; padding:7px 16px; font-size:12.5px; font-weight:500; cursor:pointer; font-family:'Inter',sans-serif; transition:all .2s; box-shadow:0 1px 4px #00000010; }
  .qchip:hover { background:#fff4ee; border-color:#b84a00; color:#b84a00; transform:translateY(-1px); }
  .msg { display:flex; align-items:flex-end; gap:10px; }
  .msg.user { justify-content:flex-end; }
  .avatar-sm { width:30px; height:30px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:14px; }
  .avatar-sm.bot  { background:linear-gradient(135deg,#b84a00,#7c2000); }
  .avatar-sm.user { background:#7c2000; }
  .bubble { max-width:78%; padding:12px 18px; font-size:14.5px; line-height:1.75; border-radius:18px; box-shadow:0 1px 6px #00000012; }
  .bubble.bot  { background:#fff; color:#2d1200; border:1px solid #ede0d4; border-bottom-left-radius:4px; }
  .bubble.user { background:linear-gradient(135deg,#b84a00,#7c2000); color:#fff; border-bottom-right-radius:4px; }
  .drive-btn { display:inline-block; margin-top:10px; background:linear-gradient(90deg,#b84a00,#d47000); color:#fff; padding:8px 18px; border-radius:8px; text-decoration:none; font-size:13px; font-weight:600; transition:opacity 0.2s; box-shadow:0 2px 8px #b84a0040; }
  .drive-btn:hover { opacity:0.88; }
  .social-btn { display:inline-flex; align-items:center; gap:5px; background:#fff4ee; color:#7c2000; padding:5px 13px; border-radius:16px; text-decoration:none; font-size:12.5px; font-weight:600; border:1.5px solid #e8c8a0; transition:all 0.2s; }
  .social-btn:hover { background:#b84a00; color:#fff; }
  .solution-box { background:#fff8f2; border:1.5px solid #f0d8c0; border-radius:14px; padding:16px 18px; margin-top:10px; }
  .solution-title { font-weight:700; color:#b84a00; font-size:14px; margin-bottom:12px; }
  .solution-step { display:flex; align-items:flex-start; gap:10px; margin-bottom:10px; font-size:13.5px; color:#2d1200; line-height:1.6; }
  .solution-step:last-child { margin-bottom:0; }
  .step-num { background:linear-gradient(135deg,#b84a00,#7c2000); color:#fff; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0; margin-top:1px; }
  .typing { display:flex; align-items:flex-end; gap:10px; }
  .dots-wrap { background:#fff; border:1px solid #ede0d4; border-radius:18px 18px 18px 4px; padding:14px 18px; display:flex; gap:5px; }
  .dot { width:7px; height:7px; border-radius:50%; background:#d47000; animation:pulse 1s ease-in-out infinite; }
  .dot:nth-child(2){ animation-delay:.2s; } .dot:nth-child(3){ animation-delay:.4s; }
  @keyframes pulse { 0%,100%{opacity:.3;transform:scale(.8)} 50%{opacity:1;transform:scale(1.1)} }
  .bottom-area { width:100%; max-width:740px; padding:10px 20px 18px; flex-shrink:0; }
  .input-card { background:#fff; border:1.5px solid #e0d0c0; border-radius:16px; box-shadow:0 2px 12px #00000014; overflow:hidden; }
  .input-row { display:flex; align-items:center; padding:4px 8px 4px 18px; gap:6px; }
  #userInput { flex:1; border:none; outline:none; font-size:14.5px; color:#2d1200; background:transparent; font-family:'Inter',sans-serif; padding:12px 0; }
  #userInput::placeholder { color:#c0a898; }
  .action-btn { width:36px; height:36px; border-radius:9px; border:none; display:flex; align-items:center; justify-content:center; font-size:17px; cursor:pointer; transition:all .2s; flex-shrink:0; }
  #micBtn { background:#fff4ee; color:#b84a00; border:1.5px solid #e8d0b8; }
  #micBtn:hover { background:#ffe0c0; }
  #micBtn.listening { background:linear-gradient(135deg,#b84a00,#7c2000); color:#fff; border-color:#b84a00; animation:micPulse 1s ease-in-out infinite; }
  @keyframes micPulse { 0%,100%{box-shadow:0 0 0 0 #b84a0060} 50%{box-shadow:0 0 0 8px #b84a0000} }
  #sendBtn { background:linear-gradient(135deg,#b84a00,#7c2000); color:#fff; }
  #sendBtn:hover { opacity:.88; }
  #voiceStatus { display:none; align-items:center; gap:8px; padding:7px 18px; background:#fff8f2; border-top:1px solid #f0e0d0; font-size:12.5px; color:#b84a00; font-weight:500; }
  .wave { display:flex; gap:3px; align-items:center; }
  .wave span { width:3px; border-radius:3px; background:#b84a00; animation:wave 0.8s ease-in-out infinite; }
  .wave span:nth-child(1){height:8px;} .wave span:nth-child(2){height:16px;animation-delay:.1s;}
  .wave span:nth-child(3){height:12px;animation-delay:.2s;} .wave span:nth-child(4){height:20px;animation-delay:.3s;}
  .wave span:nth-child(5){height:10px;animation-delay:.4s;}
  @keyframes wave { 0%,100%{transform:scaleY(.4)} 50%{transform:scaleY(1)} }
  .input-chips { display:flex; flex-wrap:wrap; gap:6px; padding:0 14px 12px; }
  .ichip { background:#fff4ee; border:1px solid #e8d0b8; color:#a05030; border-radius:16px; padding:4px 12px; font-size:11.5px; font-weight:500; cursor:pointer; font-family:'Inter',sans-serif; transition:all .18s; white-space:nowrap; }
  .ichip:hover { background:#b84a00; color:#fff; border-color:#b84a00; }
  .modal-overlay { display:none; position:fixed; inset:0; background:#00000060; z-index:999; align-items:center; justify-content:center; }
  .modal-box { background:#fff; border-radius:20px; padding:36px 40px; max-width:400px; width:90%; box-shadow:0 20px 60px #00000030; position:relative; animation:popIn .25s ease; }
  .modal-close { position:absolute; top:14px; right:16px; background:none; border:none; font-size:22px; cursor:pointer; color:#a07060; }
  .modal-header { display:flex; align-items:center; gap:12px; margin-bottom:24px; }
  .modal-icon { width:46px; height:46px; border-radius:12px; background:linear-gradient(135deg,#b84a00,#7c2000); display:flex; align-items:center; justify-content:center; font-size:22px; }
  .contact-card { background:#fff8f2; border:1.5px solid #f0d8c0; border-radius:14px; padding:16px 18px; display:flex; align-items:center; gap:14px; margin-bottom:12px; }
  .contact-icon { width:40px; height:40px; border-radius:10px; background:#ffeedd; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0; }
  .contact-label { font-size:11px; font-weight:600; color:#a07060; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:3px; }
  .contact-number { font-size:17px; font-weight:700; color:#b84a00; text-decoration:none; }
  @keyframes popIn { from{transform:scale(.85);opacity:0} to{transform:scale(1);opacity:1} }
</style>
</head>
<body>
<div class="topbar">
  <div class="topbar-left">
    <div class="logo-icon">&#127863;</div>
    <div>
      <div class="logo-text">madhushalasoftwareGpt</div>
      <div class="logo-sub">Software Assistant</div>
    </div>
  </div>
  <div class="topbar-right">
    <button class="top-btn" onclick="window.open('https://madhushalasoftware.com/','_blank')">&#127760; Website</button>
    <button class="top-btn primary" onclick="document.getElementById('contactModal').style.display='flex'">&#128222; Contact Us</button>
  </div>
</div>

<div class="main">
  <div id="chatbox">
    <div class="welcome-center" id="welcomeBlock">
      <div class="welcome-icon">&#127863;</div>
      <div class="welcome-title">Hi, How can I help you?</div>
      <div class="welcome-sub">I'm your Madhushala Software Assistant. Ask me anything about files, queries, CRM links, or downloads.</div>
      <div class="quick-chips">
        <button class="qchip" onclick="sendChip('Hi')">&#128075; Say Hello</button>
        <button class="qchip" onclick="sendChip('Give me the Madhushala setup file')">&#128190; Madhushala Setup</button>
        <button class="qchip" onclick="sendChip('Give me the restaurant setup file')">&#128190; Restaurant Setup</button>
        <button class="qchip" onclick="sendChip('Give me the madhushala pos setup file')">&#128190; POS Setup</button>
        <button class="qchip" onclick="sendChip('Delhi POS setup file')">&#128190; Delhi POS</button>
        <button class="qchip" onclick="sendChip('Support CRM login link')">&#128187; Support CRM</button>
        <button class="qchip" onclick="sendChip('Snapkey CRM login link')">&#128187; Snapkey CRM</button>
        <button class="qchip" onclick="sendChip('Email format all clients')">&#128140; Email Format</button>
        <button class="qchip" onclick="sendChip('Madhushala database delete query')">&#128203; DB Delete</button>
        <button class="qchip" onclick="sendChip('Madhushala ALL database query')">&#128203; ALL DB Query</button>
        <button class="qchip" onclick="sendChip('POS database delete query')">&#128203; POS Delete</button>
        <button class="qchip" onclick="sendChip('Database DELETE QUERY RESTRO')">&#128203; Restro Delete</button>
        <button class="qchip" onclick="sendChip('Manual SQL installation')">&#128421; SQL Manual</button>
        <button class="qchip" onclick="sendChip('Automatic SQL installation')">&#128421; SQL Auto</button>
        <button class="qchip" onclick="sendChip('AccessDatabaseEngine')">&#128421; Access DB Engine</button>
        <button class="qchip" onclick="sendChip('MS Office 2010')">&#128196; MS Office 2010</button>
        <button class="qchip" onclick="sendChip('EPOS QR Code error')">&#128247; EPOS QR Fix</button>
        <button class="qchip" onclick="sendChip('Madhushala Downloader')">&#11015; Downloader</button>
      </div>
    </div>
  </div>

  <div class="bottom-area">
    <div class="input-card">
      <div id="voiceStatus">
        <div class="wave"><span></span><span></span><span></span><span></span><span></span></div>
        <span id="voiceText">Listening... speak now</span>
        <button onclick="stopVoice()" style="margin-left:auto;background:none;border:1px solid #e0c0a0;border-radius:8px;padding:3px 10px;font-size:11px;color:#b84a00;cursor:pointer;">Stop</button>
      </div>
      <div class="input-row">
        <input id="userInput" type="text" placeholder="Send a message to your agent..." onkeydown="if(event.key==='Enter') sendMessage()"/>
        <button class="action-btn" id="micBtn" onclick="toggleVoice()" title="Voice input">&#127908;</button>
        <button class="action-btn" id="sendBtn" onclick="sendMessage()">&#10148;</button>
      </div>
      <div class="input-chips">
        <button class="ichip" onclick="sendChip('Hi')">&#128075; Hi</button>
        <button class="ichip" onclick="sendChip('Support CRM login link')">Support CRM</button>
        <button class="ichip" onclick="sendChip('Snapkey CRM login link')">Snapkey CRM</button>
        <button class="ichip" onclick="sendChip('Email format all clients')">Email Format</button>
        <button class="ichip" onclick="sendChip('Give me the Madhushala setup file')">Madhushala Setup</button>
        <button class="ichip" onclick="sendChip('Give me the restaurant setup file')">Restaurant Setup</button>
        <button class="ichip" onclick="sendChip('Give me the madhushala pos setup file')">POS Setup</button>
        <button class="ichip" onclick="sendChip('Delhi POS setup file')">Delhi POS</button>
        <button class="ichip" onclick="sendChip('Madhushala POS downloader')">POS Downloader</button>
        <button class="ichip" onclick="sendChip('Madhushala database delete query')">DB Delete</button>
        <button class="ichip" onclick="sendChip('Madhushala ALL database query')">ALL DB Query</button>
        <button class="ichip" onclick="sendChip('POS database delete query')">POS Delete</button>
        <button class="ichip" onclick="sendChip('Database DELETE QUERY RESTRO')">Restro Delete</button>
        <button class="ichip" onclick="sendChip('Manual SQL installation')">SQL Manual</button>
        <button class="ichip" onclick="sendChip('Automatic SQL installation')">SQL Auto</button>
        <button class="ichip" onclick="sendChip('MS Office 2010')">MS Office</button>
        <button class="ichip" onclick="sendChip('AccessDatabaseEngine')">Access DB</button>
        <button class="ichip" onclick="sendChip('EPOS QR Code error')">EPOS QR Fix</button>
        <button class="ichip" onclick="sendChip('Madhushala Downloader')">Downloader</button>
      </div>
    </div>
  </div>
</div>

<div class="modal-overlay" id="contactModal">
  <div class="modal-box">
    <button class="modal-close" onclick="document.getElementById('contactModal').style.display='none'">&#10005;</button>
    <div class="modal-header">
      <div class="modal-icon">&#127863;</div>
      <div>
        <div style="font-size:17px;font-weight:700;color:#2d1200;font-family:'Playfair Display',serif;">Contact Us</div>
        <div style="font-size:12px;color:#a07060;margin-top:2px;">madhushalasoftwareGpt Support</div>
      </div>
    </div>
    <div class="contact-card">
      <div class="contact-icon">&#128222;</div>
      <div><div class="contact-label">Phone Support</div><a class="contact-number" href="tel:+918101434343">+91 81014 34343</a></div>
    </div>
    <div class="contact-card">
      <div class="contact-icon">&#128200;</div>
      <div><div class="contact-label">Sales</div><a class="contact-number" href="tel:+919836362143">+91 98363 62143</a></div>
    </div>
    <div class="contact-card" style="margin-bottom:0;">
      <div class="contact-icon">&#128172;</div>
      <div><div class="contact-label">Enquiry</div><a class="contact-number" href="tel:+919836362143">+91 98363 62143</a></div>
    </div>
    <div style="margin-top:20px;text-align:center;font-size:12px;color:#c0a898;">&#128344; Available Mon-Sat, 9:00 AM - 6:00 PM</div>
  </div>
</div>

<script>
  document.getElementById('contactModal').addEventListener('click',function(e){ if(e.target===this) this.style.display='none'; });
  const chatbox=document.getElementById('chatbox');
  const welcomeBlock=document.getElementById('welcomeBlock');
  let welcomeRemoved=false;
  function removeWelcome(){ if(!welcomeRemoved&&welcomeBlock){ welcomeBlock.style.display='none'; welcomeRemoved=true; } }
  function appendMsg(role,html){
    removeWelcome();
    const wrap=document.createElement('div'); wrap.className='msg '+role;
    if(role==='bot'){ wrap.innerHTML='<div class="avatar-sm bot">&#127863;</div><div class="bubble bot">'+html+'</div>'; }
    else { wrap.innerHTML='<div class="bubble user">'+html+'</div><div class="avatar-sm user">&#128100;</div>'; }
    chatbox.appendChild(wrap); chatbox.scrollTop=chatbox.scrollHeight;
  }
  function showTyping(){
    removeWelcome();
    const wrap=document.createElement('div'); wrap.className='typing'; wrap.id='typing';
    wrap.innerHTML='<div class="avatar-sm bot">&#127863;</div><div class="dots-wrap"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
    chatbox.appendChild(wrap); chatbox.scrollTop=chatbox.scrollHeight;
  }
  function hideTyping(){ const t=document.getElementById('typing'); if(t) t.remove(); }
  async function sendMessage(){
    const input=document.getElementById('userInput');
    const text=input.value.trim();
    if(!text) return;
    input.value='';
    appendMsg('user',text);
    showTyping();
    try{
      const res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
      const data=await res.json();
      hideTyping();
      let html=data.reply;
      if(data.link){ html+='<br><a class="drive-btn" href="'+data.link+'" target="_blank">&#128193; Open: '+data.label+'</a>'; }
      appendMsg('bot',html);
    }catch(e){ hideTyping(); appendMsg('bot','Connection error. Please try again.'); }
  }
  function sendChip(text){ document.getElementById('userInput').value=text; sendMessage(); }
  let recognition=null, isListening=false;
  function initSpeech(){
    const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!SR){ alert('Voice input requires Google Chrome browser.'); return null; }
    const r=new SR(); r.lang='en-IN'; r.continuous=false; r.interimResults=true;
    r.onstart=()=>{ isListening=true; document.getElementById('micBtn').classList.add('listening'); document.getElementById('micBtn').innerHTML='&#9632;'; document.getElementById('voiceStatus').style.display='flex'; document.getElementById('voiceText').textContent='Listening... speak now'; };
    r.onresult=(e)=>{ let interim='',final=''; for(let i=e.resultIndex;i<e.results.length;i++){ if(e.results[i].isFinal) final+=e.results[i][0].transcript; else interim+=e.results[i][0].transcript; } const d=final||interim; document.getElementById('userInput').value=d; document.getElementById('voiceText').textContent='"'+d+'"'; if(final){ stopVoice(); sendMessage(); } };
    r.onerror=(e)=>{ stopVoice(); if(e.error==='not-allowed') alert('Microphone permission denied.'); };
    r.onend=()=>{ if(isListening) stopVoice(); };
    return r;
  }
  function toggleVoice(){ if(isListening){ stopVoice(); return; } recognition=initSpeech(); if(recognition) recognition.start(); }
  function stopVoice(){ isListening=false; if(recognition){ try{recognition.stop();}catch(e){} } document.getElementById('micBtn').classList.remove('listening'); document.getElementById('micBtn').innerHTML='&#127908;'; document.getElementById('voiceStatus').style.display='none'; }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message","")
    match = match_query(user_input)
    if match:
        return jsonify({"reply":match["reply"],"link":match["link"],"label":match["label"]})
    else:
        return jsonify({
            "reply":"I'm sorry, I didn't understand that.<br>Please use the quick chips or type keywords like:<br>&#8226; Setup File &nbsp;&#8226; CRM Login &nbsp;&#8226; Delete Query<br>&#8226; SQL Install &nbsp;&#8226; MS Office &nbsp;&#8226; Downloader",
            "link":None,"label":None
        })

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=5000, use_reloader=False)
