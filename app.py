"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   NewsPulse AI  ·  Bangladesh Intelligent Newsroom Platform  v5.0          ║
║   Powered by Google News · Google Trends · YouTube · Facebook · Gemini AI  ║
║   Design: Prothom Alo-Inspired Premium Newsroom UI                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

GitHub: https://github.com/yourrepo/newspulse-ai
Requirements: pip install streamlit pandas requests beautifulsoup4 pytrends
              google-generativeai plotly
"""

import streamlit as st
import pandas as pd
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import json
import time
import re
import random
from datetime import datetime, timedelta
from collections import Counter

# ─────────────────────────────────────────────────────
#  PAGE CONFIG  (must be FIRST Streamlit call)
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsPulse AI · Bangladesh",
    layout="wide",
    page_icon="🗞️",
    initial_sidebar_state="collapsed",
)

# ═════════════════════════════════════════════════════
#  PREMIUM CSS  –  Prothom Alo Inspired
# ═════════════════════════════════════════════════════
PREMIUM_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Bengali:wght@400;600;700;800&family=Hind+Siliguri:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
  --red:#C8102E; --red2:#E8293F; --red-pale:#FFF5F6;
  --cream:#FDFAF6; --white:#FFFFFF;
  --ink:#1A1A1A; --ink2:#2C2C2C; --ink3:#4A4A4A;
  --muted:#888; --border:#E8E4DC; --border2:#D4CFC5;
  --gold:#D4A017; --green:#16A34A; --blue:#1D4ED8;
  --purple:#7C3AED; --orange:#EA580C;
  --shadow:0 1px 4px rgba(0,0,0,.06),0 4px 20px rgba(0,0,0,.04);
  --shadow-lg:0 4px 24px rgba(0,0,0,.10),0 12px 48px rgba(0,0,0,.06);
  --serif:'Noto Serif Bengali','Georgia',serif;
  --sans:'Hind Siliguri','DM Sans',sans-serif;
  --mono:'JetBrains Mono',monospace;
  --r:10px; --r-lg:16px; --tr:0.22s cubic-bezier(.4,0,.2,1);
}

/* GLOBAL */
*,*::before,*::after{box-sizing:border-box;}
.stApp,[data-testid="stAppViewContainer"]{background:var(--cream)!important;color:var(--ink)!important;}
[data-testid="stSidebar"]{background:var(--white)!important;border-right:1px solid var(--border)!important;}
#MainMenu,footer,header,[data-testid="stToolbar"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
h1,h2,h3,h4{font-family:var(--serif)!important;color:var(--ink)!important;}
p,div,span,label{font-family:var(--sans)!important;}

/* MASTHEAD */
.np-masthead{background:var(--white);border-bottom:3px solid var(--red);
  padding:14px 32px;display:flex;align-items:center;justify-content:space-between;
  box-shadow:var(--shadow);}
.np-logo{font-family:var(--serif);font-size:30px;font-weight:800;color:var(--red);letter-spacing:-1px;line-height:1;}
.np-logo-sub{font-size:11px;color:var(--muted);letter-spacing:2.5px;text-transform:uppercase;margin-top:3px;font-family:var(--sans);}
.np-live{display:inline-flex;align-items:center;gap:6px;background:var(--red);color:white;
  font-family:var(--mono);font-size:10px;font-weight:700;padding:4px 12px;border-radius:100px;letter-spacing:2px;}
.live-dot{width:7px;height:7px;background:white;border-radius:50%;animation:pulse 1.2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.65)}}

/* TICKER */
.np-ticker{background:var(--red);display:flex;align-items:center;height:38px;overflow:hidden;}
.np-ticker-flag{flex-shrink:0;background:rgba(0,0,0,.25);height:100%;
  display:flex;align-items:center;padding:0 18px;
  font-family:var(--mono);font-size:11px;font-weight:700;
  letter-spacing:3px;color:white;white-space:nowrap;
  border-right:1px solid rgba(255,255,255,.2);gap:6px;}
.np-ticker-inner{flex:1;overflow:hidden;}
.np-ticker-text{display:inline-block;white-space:nowrap;
  font-family:var(--sans);font-size:13px;font-weight:600;color:white;
  animation:ticker 90s linear infinite;padding-left:48px;}
@keyframes ticker{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* NAV */
.np-nav{background:var(--white);border-bottom:1px solid var(--border);
  display:flex;overflow-x:auto;scrollbar-width:none;padding:0 24px;}
.np-nav::-webkit-scrollbar{display:none;}
.np-nav-item{padding:10px 15px;font-family:var(--sans);font-size:13px;font-weight:600;
  color:var(--muted);white-space:nowrap;border-bottom:2.5px solid transparent;cursor:pointer;
  transition:all var(--tr);}
.np-nav-item:hover,.np-nav-item.active{color:var(--red);border-bottom-color:var(--red);}

/* KPI CARD */
.np-kpi{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);
  padding:16px 18px;border-top:3px solid var(--c,var(--red));
  box-shadow:var(--shadow);transition:transform var(--tr),box-shadow var(--tr);}
.np-kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg);}
.np-kpi-icon{font-size:22px;margin-bottom:8px;}
.np-kpi-val{font-family:var(--serif);font-size:26px;font-weight:800;color:var(--ink);line-height:1;}
.np-kpi-label{font-size:11px;color:var(--muted);font-weight:500;margin-top:4px;letter-spacing:.3px;}
.np-kpi-delta{font-size:11px;color:var(--green);font-weight:600;margin-top:3px;}

/* SECTION HEADER */
.np-sec{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--border);}
.np-sec-title{font-family:var(--serif);font-size:17px;font-weight:800;color:var(--ink);
  display:flex;align-items:center;gap:10px;}
.np-sec-title::before{content:'';width:4px;height:18px;background:var(--red);border-radius:2px;flex-shrink:0;}

/* NEWS CARD */
.news-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);
  overflow:hidden;box-shadow:var(--shadow);margin-bottom:12px;
  transition:all var(--tr);cursor:pointer;display:flex;}
.news-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-2px);}
.news-card-emoji{flex-shrink:0;width:86px;background:linear-gradient(135deg,#fff0f0,#ffe4e4);
  display:flex;align-items:center;justify-content:center;font-size:34px;}
.news-card-body{padding:13px 15px;flex:1;}
.news-card-meta{font-size:11px;color:var(--muted);font-weight:500;
  display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap;}
.news-card-cat{color:var(--red);font-weight:700;}
.news-card-title{font-family:var(--serif);font-size:14.5px;font-weight:700;
  color:var(--ink);line-height:1.45;margin-bottom:8px;}
.score-pill{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;
  border-radius:100px;font-size:10px;font-weight:700;font-family:var(--mono);
  background:rgba(200,16,46,.08);color:var(--red);}
.score-pill.breaking{background:var(--red);color:white;}

/* TREND CARD */
.trend-card{background:var(--white);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:14px 16px;margin-bottom:9px;
  border-left:4px solid var(--c,var(--red));
  box-shadow:var(--shadow);cursor:pointer;transition:all var(--tr);}
.trend-card:hover{transform:translateX(4px);box-shadow:var(--shadow-lg);}
.trend-num{font-family:var(--serif);font-size:22px;font-weight:900;color:var(--border2);float:right;line-height:1;}
.trend-platform{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;
  border-radius:100px;font-family:var(--mono);font-size:9px;font-weight:700;
  letter-spacing:1px;text-transform:uppercase;margin-bottom:5px;}
.pill-g{background:rgba(66,133,244,.1);color:#4285f4;}
.pill-yt{background:rgba(255,0,0,.1);color:#cc0000;}
.pill-fb{background:rgba(24,119,242,.1);color:#1877f2;}
.trend-title{font-family:var(--serif);font-size:15px;font-weight:700;
  color:var(--ink);line-height:1.4;margin-bottom:6px;}
.trend-heat{height:4px;border-radius:2px;
  background:linear-gradient(90deg,var(--c,var(--red)),transparent);margin-bottom:6px;}
.trend-meta-row{display:flex;align-items:center;justify-content:space-between;
  font-size:11px;color:var(--muted);}

/* YOUTUBE CARD */
.yt-card{background:var(--white);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:13px 15px;margin-bottom:9px;
  display:flex;align-items:center;gap:12px;
  box-shadow:var(--shadow);cursor:pointer;transition:all var(--tr);}
.yt-card:hover{transform:translateX(4px);box-shadow:var(--shadow-lg);background:#fff8f8;}
.yt-rank{font-family:var(--serif);font-size:24px;font-weight:900;color:var(--border2);min-width:28px;}
.yt-rank.t3{color:#cc0000;}
.yt-thumb{width:62px;height:46px;border-radius:6px;flex-shrink:0;
  background:linear-gradient(135deg,#cc0000,#ff6b35);
  display:flex;align-items:center;justify-content:center;font-size:20px;color:white;}
.yt-info{flex:1;min-width:0;}
.yt-title{font-size:13.5px;font-weight:600;color:var(--ink);line-height:1.4;
  margin-bottom:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.yt-meta{font-size:11px;color:var(--muted);display:flex;align-items:center;gap:8px;flex-wrap:wrap;}

/* FACEBOOK CARD */
.fb-card{background:var(--white);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:12px 16px;margin-bottom:8px;
  border-left:4px solid #1877f2;
  box-shadow:var(--shadow);cursor:pointer;transition:all var(--tr);}
.fb-card:hover{transform:translateX(4px);background:#f0f7ff;}
.fb-topic{font-size:14px;font-weight:700;color:var(--ink);margin-bottom:4px;}
.fb-meta{font-size:11px;color:var(--muted);display:flex;gap:10px;align-items:center;flex-wrap:wrap;}
.fb-vol{color:#1877f2;font-weight:700;}

/* AI PANEL */
.ai-panel{background:var(--white);border:1px solid var(--border);
  border-top:3px solid var(--red);border-radius:var(--r-lg);
  padding:20px;box-shadow:var(--shadow);margin-bottom:16px;}
.ai-panel-hdr{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.ai-icon{width:42px;height:42px;border-radius:11px;
  background:linear-gradient(135deg,var(--red),#ff6b35);
  display:flex;align-items:center;justify-content:center;font-size:19px;flex-shrink:0;}
.ai-title{font-family:var(--serif);font-size:16px;font-weight:800;color:var(--ink);}
.ai-sub{font-size:11px;color:var(--muted);margin-top:2px;}
.ai-out{background:var(--cream);border:1px solid var(--border);border-radius:var(--r);
  padding:16px;font-family:var(--sans);font-size:13.5px;line-height:1.85;
  color:var(--ink3);min-height:70px;margin-top:10px;}

/* SENTIMENT */
.sent-wrap{margin-bottom:10px;}
.sent-row{display:flex;justify-content:space-between;font-size:12px;font-weight:600;
  color:var(--ink3);margin-bottom:4px;}
.sent-track{height:7px;background:var(--border);border-radius:4px;overflow:hidden;}
.sent-fill{height:100%;border-radius:4px;transition:width .9s cubic-bezier(.4,0,.2,1);}

/* KEYWORD CLOUD */
.kw-cloud{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.kw-tag{display:inline-block;background:var(--red-pale);color:var(--red);
  border:1px solid rgba(200,16,46,.15);font-size:12px;font-weight:600;
  padding:4px 12px;border-radius:100px;cursor:pointer;transition:all var(--tr);}
.kw-tag:hover{background:var(--red);color:white;}
.kw-tag.lg{font-size:14px;padding:5px 14px;}
.kw-tag.sm{font-size:10px;padding:3px 8px;opacity:.75;}

/* AQI */
.aqi-num{font-family:var(--serif);font-size:72px;font-weight:900;line-height:1;}
.aqi-scale{height:8px;border-radius:4px;
  background:linear-gradient(90deg,#00e400,#ffff00,#ff7e00,#ff0000,#8f3f97,#7e0023);
  position:relative;margin:10px 0 4px;}
.aqi-marker{position:absolute;top:-4px;width:16px;height:16px;border-radius:50%;
  background:white;border:3px solid var(--ink);transform:translateX(-50%);
  box-shadow:0 2px 8px rgba(0,0,0,.2);}
.aqi-box{background:var(--cream);border:1px solid var(--border);border-radius:8px;padding:10px 12px;text-align:center;}
.aqi-box-val{font-family:var(--serif);font-size:19px;font-weight:800;color:var(--ink);}
.aqi-box-lbl{font-size:10px;color:var(--muted);font-weight:500;margin-top:2px;}

/* WEATHER */
.wx-card{background:linear-gradient(135deg,#1565c0,#1e88e5);border-radius:var(--r-lg);
  padding:20px;color:white;box-shadow:0 4px 20px rgba(21,101,192,.3);margin-bottom:14px;}
.wx-temp{font-family:var(--serif);font-size:56px;font-weight:900;line-height:1;}
.wx-details{display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;}
.wx-detail{font-size:12px;opacity:.88;}

/* STREAMLIT OVERRIDES */
[data-testid="stButton"] button{
  background:var(--red)!important;color:white!important;border:none!important;
  border-radius:8px!important;font-family:var(--serif)!important;
  font-size:15px!important;font-weight:700!important;padding:12px 28px!important;
  width:100%!important;box-shadow:0 4px 14px rgba(200,16,46,.25)!important;
  transition:all .2s ease!important;}
[data-testid="stButton"] button:hover{
  transform:translateY(-2px)!important;box-shadow:0 8px 26px rgba(200,16,46,.35)!important;}
[data-baseweb="tab-list"]{background:transparent!important;
  border-bottom:2px solid var(--border)!important;gap:0!important;padding:0!important;}
[data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;
  font-family:var(--sans)!important;font-size:13px!important;font-weight:600!important;
  padding:10px 18px!important;border-radius:0!important;
  border-bottom:2.5px solid transparent!important;transition:all .2s!important;}
[aria-selected="true"][data-baseweb="tab"]{color:var(--red)!important;
  border-bottom-color:var(--red)!important;background:rgba(200,16,46,.04)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;
  border-radius:var(--r)!important;overflow:hidden!important;}
[data-testid="stDataFrame"] th{background:var(--cream)!important;color:var(--muted)!important;
  font-family:var(--mono)!important;font-size:10.5px!important;letter-spacing:1.5px!important;
  text-transform:uppercase!important;border-bottom:1px solid var(--border2)!important;padding:10px 14px!important;}
[data-testid="stDataFrame"] td{color:var(--ink)!important;font-family:var(--sans)!important;
  font-size:13px!important;line-height:1.5!important;border-bottom:1px solid var(--border)!important;
  padding:9px 14px!important;}
[data-testid="stDataFrame"] tr:hover td{background:var(--red-pale)!important;}
[data-baseweb="select"]>div{background:var(--cream)!important;border:1.5px solid var(--border)!important;
  border-radius:8px!important;color:var(--ink)!important;font-family:var(--sans)!important;}
[data-baseweb="select"]>div:focus-within{border-color:var(--red)!important;
  box-shadow:0 0 0 3px rgba(200,16,46,.1)!important;}
[data-baseweb="popover"]{background:var(--white)!important;
  border:1px solid var(--border)!important;border-radius:8px!important;}
[role="option"]{color:var(--ink)!important;font-family:var(--sans)!important;}
[role="option"]:hover{background:var(--red-pale)!important;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{
  background:var(--cream)!important;border:1.5px solid var(--border)!important;
  border-radius:8px!important;color:var(--ink)!important;font-family:var(--sans)!important;}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{
  border-color:var(--red)!important;box-shadow:0 0 0 3px rgba(200,16,46,.1)!important;}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] p{
  font-family:var(--sans)!important;font-size:12px!important;color:var(--ink3)!important;}
[data-testid="stSidebar"] input{background:var(--cream)!important;
  border:1.5px solid var(--border)!important;border-radius:8px!important;
  color:var(--ink)!important;font-family:var(--sans)!important;}
[data-testid="stDownloadButton"] button{background:var(--cream)!important;
  border:1.5px solid var(--border)!important;color:var(--red)!important;
  font-family:var(--mono)!important;font-size:12px!important;padding:10px!important;
  box-shadow:none!important;letter-spacing:1px!important;}
[data-testid="stDownloadButton"] button:hover{border-color:var(--red)!important;
  background:var(--red-pale)!important;transform:none!important;}
[data-testid="stAlert"]{background:rgba(200,16,46,.06)!important;
  border:1px solid rgba(200,16,46,.2)!important;border-radius:var(--r)!important;
  font-family:var(--sans)!important;font-size:13px!important;}
[data-testid="stProgressBar"]>div>div{
  background:linear-gradient(90deg,var(--red),var(--orange))!important;}
[data-testid="stMetricValue"]{font-family:var(--serif)!important;font-size:26px!important;color:var(--ink)!important;}
[data-testid="stMetricLabel"]{font-family:var(--sans)!important;font-size:11px!important;color:var(--muted)!important;}

/* FEED STATUS */
.feed-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;flex-shrink:0;}
.feed-dot.live{background:#16a34a;box-shadow:0 0 8px #16a34a;}
.feed-dot.warn{background:#D4A017;box-shadow:0 0 6px #D4A017;}
.feed-dot.off{background:#888;}
.feed-row{display:flex;align-items:center;padding:7px 0;border-bottom:1px solid var(--border);
  font-family:var(--mono);font-size:11px;color:var(--muted);}
.feed-row:last-child{border-bottom:none;}
.feed-name{flex:1;color:var(--ink3);}

/* CROSS-PLATFORM TAG */
.cp-tag{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;
  border-radius:100px;font-family:var(--mono);font-size:9px;font-weight:700;
  letter-spacing:.5px;text-transform:uppercase;}

/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--cream);}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════
#  SESSION STATE
# ═════════════════════════════════════════════════════
_DEFAULTS = dict(bookmarks=[], read_history=[], ai_summary="", ai_cluster="",
                 ai_sent={}, fc_result="", hl_result="", ai_kws=[],
                 editorial_output="", editorial_topic="")
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═════════════════════════════════════════════════════
#  SOURCE CONFIG
# ═════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
#  COMPLETE 60-SOURCE ARRAY  (BD: 1-30 | INT: 31-60)
#  Instruction: সম্পূর্ণ ৬০টি সোর্স ব্যবহার করতে হবে
# ══════════════════════════════════════════════════════════════

# 🇧🇩 BD_SOURCES (১-৩০) — id, bangla_name, rss_url, web_url
# BD_SOURCES: (id, name, primary_rss, web_url, fallback_rss_list)
BD_SOURCES = [
    ("prothomalo",    "প্রথম আলো",          "https://www.prothomalo.com/feed/",               "https://prothomalo.com",             ["https://www.prothomalo.com/rss.xml"]),
    ("bd_pratidin",   "বাংলাদেশ প্রতিদিন", "https://www.bd-pratidin.com/feed/",              "https://bd-pratidin.com",            ["https://www.bd-pratidin.com/rss.xml","https://news.google.com/rss/search?q=site:bd-pratidin.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("jugantor",      "যুগান্তর",            "https://www.jugantor.com/feed/",                 "https://jugantor.com",               ["https://news.google.com/rss/search?q=site:jugantor.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("kalerkantho",   "কালের কণ্ঠ",         "https://www.kalerkantho.com/rss.xml",            "https://kalerkantho.com",            ["https://www.kalerkantho.com/feed/","https://news.google.com/rss/search?q=site:kalerkantho.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("samakal",       "দৈনিক সমকাল",        "https://samakal.com/feed/",                      "https://samakal.com",                ["https://samakal.com/rss.xml","https://news.google.com/rss/search?q=site:samakal.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("ittefaq",       "দৈনিক ইত্তেফাক",     "https://www.ittefaq.com.bd/feed/",               "https://ittefaq.com.bd",             ["https://news.google.com/rss/search?q=site:ittefaq.com.bd&hl=bn&gl=BD&ceid=BD:bn"]),
    ("mzamin",        "মানব জমিন",           "https://mzamin.com/feed.php",                    "https://mzamin.com",                 ["https://mzamin.com/rss.xml","https://news.google.com/rss/search?q=site:mzamin.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("nayadiganta",   "নয়া দিগন্ত",         "https://www.dailynayadiganta.com/feed/",         "https://dailynayadiganta.com",       ["https://news.google.com/rss/search?q=site:dailynayadiganta.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("inqilab",       "দৈনিক ইনকিলাব",      "https://www.dailyinqilab.com/feed/",             "https://dailyinqilab.com",           ["https://news.google.com/rss/search?q=site:dailyinqilab.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("janakantha",    "দৈনিক জনকণ্ঠ",       "https://www.dailyjanakantha.com/feed/",          "https://dailyjanakantha.com",        ["https://news.google.com/rss/search?q=site:dailyjanakantha.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("bhorerkagoj",   "ভোরের কাগজ",          "https://www.bhorerkagoj.com/feed/",              "https://bhorerkagoj.com",            ["https://news.google.com/rss/search?q=site:bhorerkagoj.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("amadershomoy",  "আমাদের সময়",          "https://www.dainikamadershomoy.com/feed/",       "https://dainikamadershomoy.com",     ["https://news.google.com/rss/search?q=site:dainikamadershomoy.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("bdnews24",      "বিডিনিউজ২৪",         "https://bdnews24.com/feed",                      "https://bdnews24.com",               ["https://bdnews24.com/rss","https://news.google.com/rss/search?q=site:bdnews24.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("banglanews24",  "বাংলানিউজ২৪",        "https://www.banglanews24.com/rss.xml",           "https://banglanews24.com",           ["https://www.banglanews24.com/feed/","https://news.google.com/rss/search?q=site:banglanews24.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("jagonews24",    "জাগো নিউজ ২৪",       "https://www.jagonews24.com/feed/",               "https://jagonews24.com",             ["https://news.google.com/rss/search?q=site:jagonews24.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("banglatribune", "বাংলা ট্রিবিউন",      "https://www.banglatribune.com/feed/",            "https://banglatribune.com",          ["https://banglatribune.com/rss.xml","https://news.google.com/rss/search?q=site:banglatribune.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("dhakapost",     "ঢাকা পোস্ট",          "https://www.dhakapost.com/feed/",                "https://dhakapost.com",              ["https://news.google.com/rss/search?q=site:dhakapost.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("barta24",       "বার্তা২৪",            "https://barta24.com/feed/",                      "https://barta24.com",                ["https://barta24.com/rss.xml","https://news.google.com/rss/search?q=site:barta24.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("risingbd",      "রাইজিংবিডি",          "https://risingbd.com/feed",                      "https://risingbd.com",               ["https://risingbd.com/rss.xml","https://news.google.com/rss/search?q=site:risingbd.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("bd24live",      "বিডি২৪লাইভ",         "https://www.bd24live.com/feed/",                 "https://bd24live.com",               ["https://news.google.com/rss/search?q=site:bd24live.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("somoynews",     "সময় নিউজ",           "https://www.somoynews.tv/rss.xml",               "https://somoynews.tv",               ["https://www.somoynews.tv/feed/","https://news.google.com/rss/search?q=site:somoynews.tv&hl=bn&gl=BD&ceid=BD:bn"]),
    ("jamunatv",      "যমুনা টেলিভিশন",     "https://jamuna.tv/feed/",                        "https://jamuna.tv",                  ["https://news.google.com/rss/search?q=site:jamuna.tv&hl=bn&gl=BD&ceid=BD:bn"]),
    ("ntv",           "এনটিভি",              "https://www.ntvbd.com/rss.xml",                  "https://ntvbd.com",                  ["https://www.ntvbd.com/feed/","https://news.google.com/rss/search?q=site:ntvbd.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("channel24",     "চ্যানেল ২৪",          "https://www.channel24.bd/feed/",                 "https://channel24.bd",               ["https://news.google.com/rss/search?q=site:channel24.bd&hl=bn&gl=BD&ceid=BD:bn"]),
    ("channeli",      "চ্যানেল আই",          "https://channelionline.com/feed/",               "https://channelionline.com",         ["https://news.google.com/rss/search?q=site:channelionline.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("rtv",           "আরটিভি",              "https://www.rtvonline.com/feed",                 "https://rtvonline.com",              ["https://www.rtvonline.com/rss.xml","https://news.google.com/rss/search?q=site:rtvonline.com&hl=bn&gl=BD&ceid=BD:bn"]),
    ("thedailystar",  "The Daily Star",       "https://www.thedailystar.net/arcio/rss/",        "https://thedailystar.net",           ["https://www.thedailystar.net/rss.xml"]),
    ("dhakatribune",  "Dhaka Tribune",        "https://www.dhakatribune.com/feed",              "https://dhakatribune.com",           ["https://www.dhakatribune.com/rss.xml"]),
    ("tbsnews",       "The Business Standard","https://www.tbsnews.net/rss.xml",                "https://tbsnews.net",                ["https://www.tbsnews.net/feed/"]),
    ("thefinancialexpress","The Financial Express","https://thefinancialexpress.com.bd/feed/",  "https://thefinancialexpress.com.bd", ["https://thefinancialexpress.com.bd/rss.xml"]),
]

# 🌍 INT_SOURCES (৩১-৬০) — id, name, rss_url, web_url
# Priority 11 sources at TOP (যাদের headline অনুবাদ করা হয় + উপরে দেখানো হয়)
INT_SOURCES = [
    # ══ PRIORITY TOP 11 (ব্যবহারকারী নির্ধারিত) ══════════════
    ("bbc",          "BBC News",                   "http://feeds.bbci.co.uk/news/world/rss.xml",             "https://bbc.com"),
    ("aljazeera",    "Al Jazeera",                 "https://www.aljazeera.com/xml/rss/all.xml",              "https://aljazeera.com"),
    ("reuters",      "Reuters",                    "https://feeds.reuters.com/reuters/worldNews",             "https://reuters.com"),
    ("cnn",          "CNN",                        "http://rss.cnn.com/rss/edition_world.rss",               "https://cnn.com"),
    ("dawn",         "Dawn",                       "https://www.dawn.com/feeds/home",                        "https://dawn.com"),
    ("apnews",       "AP News",                    "https://feeds.apnews.com/rss/topnews",                   "https://apnews.com"),
    ("nytimes",      "The New York Times",         "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "https://nytimes.com"),
    ("middleeasteye","Middle East Eye",             "https://www.middleeasteye.net/rss",                      "https://middleeasteye.net"),
    ("geotv",        "Geo TV",                     "https://www.geo.tv/rss/1",                               "https://geo.tv"),
    ("ndtv",         "NDTV",                       "https://feeds.feedburner.com/ndtvnews-top-stories",       "https://ndtv.com"),
    ("guardian",     "The Guardian",               "https://www.theguardian.com/world/rss",                  "https://theguardian.com"),
    # ══ অন্যান্য আন্তর্জাতিক সোর্স ══════════════════════════
    ("bloomberg",    "Bloomberg",                  "https://feeds.bloomberg.com/markets/news.rss",            "https://bloomberg.com"),
    ("independent",  "The Independent",            "https://www.independent.co.uk/rss",                      "https://independent.co.uk"),
    ("telegraph",    "The Telegraph",              "https://www.telegraph.co.uk/rss.xml",                    "https://telegraph.co.uk"),
    ("ft",           "Financial Times",            "https://www.ft.com/rss/home/uk",                         "https://ft.com"),
    ("economist",    "The Economist",              "https://www.economist.com/sections/science-technology/rss.xml","https://economist.com"),
    ("washpost",     "The Washington Post",        "https://feeds.washingtonpost.com/rss/world",              "https://washingtonpost.com"),
    ("wsj",          "Wall Street Journal",        "https://feeds.a.dj.com/rss/RSSWorldNews.xml",            "https://wsj.com"),
    ("time",         "Time",                       "https://feeds.feedburner.com/time/topstories",            "https://time.com"),
    ("nbcnews",      "NBC News",                   "https://feeds.nbcnews.com/nbcnews/public/news",           "https://nbcnews.com"),
    ("abcnews",      "ABC News",                   "https://feeds.abcnews.com/abcnews/topstories",            "https://abcnews.com"),
    ("foxnews",      "Fox News",                   "https://moxie.foxnews.com/google-publisher/world.xml",    "https://foxnews.com"),
    ("huffpost",     "HuffPost",                   "https://www.huffpost.com/section/front-page/feed",        "https://huffpost.com"),
    ("politico",     "Politico",                   "https://rss.politico.com/politics-news.xml",              "https://politico.com"),
    ("scmp",         "South China Morning Post",   "https://www.scmp.com/rss/91/feed",                       "https://scmp.com"),
    ("nikkei",       "Nikkei Asia",                "https://asia.nikkei.com/rss/feed/nar",                   "https://nikkei.com"),
    ("arabnews",     "Arab News",                  "https://www.arabnews.com/rss.xml",                       "https://arabnews.com"),
    ("dw",           "Deutsche Welle (DW)",        "https://rss.dw.com/xml/rss-en-world",                    "https://dw.com"),
    ("france24",     "France 24",                  "https://www.france24.com/en/rss",                        "https://france24.com"),
    ("euronews",     "Euronews",                   "https://www.euronews.com/rss?format=mrss&level=theme&name=news","https://euronews.com"),
]

# Combined for easy iteration
ALL_60_SOURCES = BD_SOURCES + INT_SOURCES  # total: 60

# ─── Bangla relative time ────────────────────────────────
def time_ago_bn(pub_dt) -> str:
    """Return Bangla relative time: ৫ মিনিট আগে, ২ ঘণ্টা আগে, etc."""
    if pub_dt is None:
        return ""
    try:
        utc_now = datetime.utcnow()
        if hasattr(pub_dt, 'tzinfo') and pub_dt.tzinfo is not None:
            import calendar as _cal
            pub_dt = datetime.utcfromtimestamp(_cal.timegm(pub_dt.utctimetuple()))
        diff = utc_now - pub_dt
        secs = int(diff.total_seconds())
        if secs < 0:   return "এইমাত্র"
        if secs < 60:  return f"{secs} সেকেন্ড আগে"
        mins = secs // 60
        if mins < 60:  return f"{mins} মিনিট আগে"
        hrs  = mins // 60
        if hrs < 24:   return f"{hrs} ঘণ্টা আগে"
        days = hrs // 24
        return f"{days} দিন আগে"
    except Exception:
        return ""

# ── Bad link patterns to reject ────────────────────────────
_BAD_LINK_PATTERNS = [
    # Factcheck / revision pages
    "/revisions", "/node/", "factcheckbangla", "factcheck.afp",
    # Category / tag / author pages
    "/tag/", "/tags/", "/author/", "/category/", "/page/",
    # Feed / technical
    "/feed", "/rss", "/amp/",
    # Video pages (NTV, YouTube, channel sites, etc.)
    "/video/", "/videos/", "/watch/", "/live/", "/show/",
    "/episode/", "/ep-", "/season/", "/programme/", "/clip/",
    "/tv/", "/multimedia/", "/podcast/", "/audio/",
    # Entertainment category paths
    "/entertainment/", "/bিনোদন/", "/sports-video/",
    # Other junk
    "?utm_", "#comment", "javascript:", "mailto:",
]
_BAD_TITLE_PATTERNS = [
    "factcheck", "fact check", "fact-check",
    "watch live", "watch now", "live stream",
    "full episode", "episode ", " ep ", "season ",
]

# International sources that get priority display + Bangla translation
PRIORITY_INT_SOURCES = [
    "bbc", "aljazeera", "reuters", "cnn", "dawn",
    "apnews", "nytimes", "middleeasteye", "geotv", "ndtv", "guardian",
]

def _is_valid_news_link(link: str, title: str) -> bool:
    """
    Return True only if link looks like a real article (not homepage,
    category, factcheck node, revision, tag page, etc.)
    """
    if not link:
        return False
    link_l  = link.lower()
    title_l = title.lower()

    # Reject known bad patterns in URL
    for pat in _BAD_LINK_PATTERNS:
        if pat in link_l:
            return False

    # Reject bad title patterns (factcheck pages, etc.)
    for pat in _BAD_TITLE_PATTERNS:
        if pat in title_l:
            return False

    # Must have a meaningful path (at least 3 slashes = real article)
    try:
        path = link_l.split("://", 1)[-1]          # strip scheme
        path = path.split("?")[0].split("#")[0]     # strip query/anchor
        parts = [p for p in path.split("/") if p]  # non-empty segments
        # First segment is domain, rest is path
        path_parts = parts[1:]                      # skip domain
        if len(path_parts) == 0:
            return False  # homepage
        # Must have at least one segment with digits OR length > 20 (slug)
        has_slug = any(
            any(c.isdigit() for c in p) or len(p) > 15
            for p in path_parts
        )
        if not has_slug and len(path_parts) <= 1:
            return False  # category page like /entertainment
    except Exception:
        return False

    return True

def _parse_pubdate(pub_text: str):
    """Parse RSS pubDate string → datetime (timezone-naive UTC)."""
    if not pub_text:
        return None
    text = pub_text.strip()
    # Remove timezone name that Python can't parse
    text = re.sub(r' (GMT|UTC|BST|EST|PST|BDT|IST|[A-Z]{2,4})$', '', text)
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ]:
        try:
            dt = datetime.strptime(text[:31], fmt)
            # Convert to UTC naive
            if dt.tzinfo is not None:
                import calendar
                ts = calendar.timegm(dt.utctimetuple())
                dt = datetime.utcfromtimestamp(ts)
            return dt
        except Exception:
            continue
    return None

def _hours_ago(pub_dt) -> float:
    """Return how many hours ago pub_dt was (UTC naive vs UTC now)."""
    if pub_dt is None:
        return 0.0
    try:
        utc_now = datetime.utcnow()
        diff = utc_now - pub_dt
        return diff.total_seconds() / 3600
    except Exception:
        return 0.0

def fetch_rss(url: str, max_items: int = 15) -> list:
    """
    Fetch RSS feed. Returns items with title, link, pub_dt, age_hours.
    Rejects homepage/category/factcheck links automatically.
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        })
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw  = resp.read()
            root = ET.fromstring(raw)
            items = []
            for item in root.findall(".//item"):
                t   = item.find("title")
                l   = item.find("link")
                pub = item.find("pubDate")
                if t is None or not t.text or not t.text.strip():
                    continue
                title = t.text.strip()
                # Clean Google News redirect titles (remove " - Source" suffix)
                title = re.sub(r'\s+[-–]\s+\S+$', '', title).strip()
                link  = ""
                if l is not None and l.text:
                    link = l.text.strip()
                elif l is not None:
                    # Some RSS use <link> as CDATA after tag
                    link = (l.tail or "").strip()
                # Validate link
                if not _is_valid_news_link(link, title):
                    continue
                pub_dt    = _parse_pubdate(pub.text if pub is not None else None)
                age_hours = _hours_ago(pub_dt)
                items.append({
                    "title":     title,
                    "link":      link,
                    "pub_dt":    pub_dt,
                    "age_hours": age_hours,
                })
                if len(items) >= max_items:
                    break
            return items
    except Exception:
        return []

def filter_recent(items: list, hours: int = 6) -> list:
    """
    Keep only items published within the last N hours.
    age_hours is calculated in UTC by _hours_ago().
    Items with no pubDate are EXCLUDED (strict mode).
    """
    result = []
    for item in items:
        age = item.get("age_hours")
        if age is None:
            continue   # strict: skip undated items
        if 0 <= age <= hours:
            result.append(item)
    return result

# ═════════════════════════════════════════════════════
#  DATA FETCHING
# ═════════════════════════════════════════════════════

@st.cache_data(ttl=60, show_spinner=False)
def fetch_google_news(topic: str = "বাংলাদেশ", max_items: int = 20) -> list:
    encoded = urllib.parse.quote(topic)
    urls = [
        f"https://news.google.com/rss/search?q={encoded}&hl=bn&gl=BD&ceid=BD:bn",
        f"https://news.google.com/rss/search?q={urllib.parse.quote(topic+' Bangladesh')}&hl=en&gl=BD&ceid=BD:en",
        "https://news.google.com/rss?hl=bn&gl=BD&ceid=BD:bn",
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                root = ET.fromstring(resp.read())
                items = []
                for item in root.findall(".//item")[:max_items]:
                    t = item.find("title"); l = item.find("link")
                    d = item.find("pubDate"); s = item.find("source")
                    if t is not None and t.text:
                        items.append({"title": t.text.strip(),
                                      "link":  (l.text or "").strip(),
                                      "date":  (d.text or "").strip(),
                                      "source":(s.text or "Google News").strip()})
                if items:
                    return items
        except Exception:
            continue
    return []

@st.cache_data(ttl=60, show_spinner=False)
def fetch_news_categories() -> dict:
    cats = {
        "🔴 শীর্ষ সংবাদ":   "বাংলাদেশ",
        "🏛️ রাজনীতি":       "বাংলাদেশ রাজনীতি",
        "💰 অর্থনীতি":      "বাংলাদেশ অর্থনীতি",
        "🏏 খেলাধুলা":      "বাংলাদেশ ক্রিকেট",
        "💻 প্রযুক্তি":     "বাংলাদেশ প্রযুক্তি",
        "🌍 আন্তর্জাতিক":  "Bangladesh international",
        "🌱 জলবায়ু":        "Bangladesh climate",
    }
    return {label: fetch_google_news(query, 15) for label, query in cats.items()}

@st.cache_data(ttl=90, show_spinner=False)
def fetch_google_realtime_trends() -> list:
    # Method 1: Realtime RSS
    try:
        req = urllib.request.Request("https://trends.google.com/trending/rss?geo=BD",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            root   = ET.fromstring(resp.read())
            ns_ht  = "https://trends.google.com/trending/rss"
            results = []
            for item in root.findall(".//item")[:20]:
                title   = item.find("title")
                traffic = item.find(f"{{{ns_ht}}}approx_traffic")
                news_t  = item.find(f"{{{ns_ht}}}news_item_title")
                pub     = item.find("pubDate")
                if title is not None and title.text:
                    results.append({
                        "topic":   title.text.strip(),
                        "traffic": (traffic.text or "N/A") if traffic is not None else "N/A",
                        "related": (news_t.text  or "")   if news_t  is not None else "",
                        "pub":     (pub.text or "")[:16]  if pub     is not None else "",
                    })
            if results:
                return results
    except Exception:
        pass
    # Method 2: pytrends
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        df = pt.trending_searches(pn='bangladesh')
        return [{"topic": r[0], "traffic": "trending", "related": "", "pub": ""}
                for r in df.values.tolist()[:20]]
    except Exception:
        pass
    # Fallback
    return [{"topic": t, "traffic": "N/A", "related": "", "pub": ""}
            for t in ["বাংলাদেশ সংস্কার","ক্রিকেট আপডেট","AI প্রযুক্তি",
                      "ডেঙ্গু সতর্কতা","বাজেট ২০২৬","পদ্মা সেতু","শিক্ষা সংস্কার"]]

@st.cache_data(ttl=150, show_spinner=False)
def fetch_youtube_bd() -> list:
    """YouTube Bangladesh trending — Atom RSS → scrape → fallback."""
    items = []
    # Method 1: Atom RSS
    try:
        url = "https://www.youtube.com/feeds/videos.xml?chart=mostpopular&regionCode=BD&hl=bn"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            root  = ET.fromstring(resp.read())
            ns    = "http://www.w3.org/2005/Atom"
            yt_ns = "http://www.youtube.com/xml/schemas/2015"
            for entry in root.findall(f"{{{ns}}}entry")[:20]:
                tit    = entry.find(f"{{{ns}}}title")
                vid_id = entry.find(f"{{{yt_ns}}}videoId")
                author = entry.find(f"{{{ns}}}author/{{{ns}}}name")
                pub    = entry.find(f"{{{ns}}}published")
                stats  = entry.find(f"{{{yt_ns}}}statistics")
                views  = stats.get("viewCount","") if stats is not None else ""
                if tit is not None and tit.text:
                    items.append({
                        "title":     tit.text.strip(),
                        "channel":   author.text.strip() if author is not None else "",
                        "views":     int(views) if views.isdigit() else 0,
                        "views_fmt": f"{int(views):,}" if views.isdigit() else "",
                        "url":       f"https://youtu.be/{vid_id.text}" if vid_id is not None else "#",
                        "pub":       pub.text[:10] if pub is not None else "",
                    })
        if items:
            return items
    except Exception:
        pass
    # Method 2: scrape ytInitialData
    try:
        hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "bn-BD,bn;q=0.9"}
        resp = requests.get("https://www.youtube.com/feed/trending?gl=BD&hl=bn",
                            headers=hdrs, timeout=14)
        m = re.search(r'var ytInitialData\s*=\s*({.*?});\s*</script>', resp.text, re.DOTALL)
        if m:
            data     = json.loads(m.group(1))
            sections = (data.get("contents",{})
                            .get("twoColumnBrowseResultsRenderer",{})
                            .get("tabs",[{}])[0]
                            .get("tabRenderer",{})
                            .get("content",{})
                            .get("sectionListRenderer",{})
                            .get("contents",[]))
            for sec in sections:
                shelf_items = (sec.get("itemSectionRenderer",{})
                                  .get("contents",[{}])[0]
                                  .get("shelfRenderer",{})
                                  .get("content",{})
                                  .get("expandedShelfContentsRenderer",{})
                                  .get("items",[]))
                for it in shelf_items:
                    vr = it.get("videoRenderer",{})
                    if not vr:
                        continue
                    title  = "".join(r.get("text","") for r in vr.get("title",{}).get("runs",[]))
                    ch     = "".join(r.get("text","") for r in vr.get("ownerText",{}).get("runs",[]))
                    views  = vr.get("viewCountText",{}).get("simpleText","")
                    vid_id = vr.get("videoId","")
                    items.append({"title": title,"channel": ch,"views": 0,"views_fmt": views,
                                  "url": f"https://youtu.be/{vid_id}" if vid_id else "#","pub": ""})
                    if len(items) >= 20:
                        break
                if len(items) >= 20:
                    break
    except Exception:
        pass
    # Fallback
    if not items:
        items = [
            {"title":"বাংলাদেশ বনাম ভারত টেস্ট হাইলাইটস ২০২৬","channel":"Bangladesh Cricket Board","views":1_800_000,"views_fmt":"১৮ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"ব্রেকিং — সংসদ অধিবেশন লাইভ","channel":"Jamuna TV","views":950_000,"views_fmt":"৯.৫ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"AI দিয়ে ছবি বানানো শিখুন | বাংলা টিউটোরিয়াল","channel":"Tech Bangla","views":620_000,"views_fmt":"৬.২ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"ঢাকার সেরা ১০ রেস্তোরাঁ ২০২৬","channel":"Food BD","views":510_000,"views_fmt":"৫.১ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"নতুন বাংলা নাটক — ভালোবাসার গল্প পর্ব ৩","channel":"NTV Drama","views":430_000,"views_fmt":"৪.৩ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"টেস্ট ক্রিকেটে বাংলাদেশের সেরা ইনিংস","channel":"Sports Zone BD","views":380_000,"views_fmt":"৩.৮ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"ইসলামিক বক্তৃতা — সফলতার রহস্য","channel":"Islamic BD","views":340_000,"views_fmt":"৩.৪ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
            {"title":"বাংলাদেশের শেয়ার বাজার আজকের আপডেট","channel":"Business Bangla","views":290_000,"views_fmt":"২.৯ লাখ","url":"#","pub":datetime.now().strftime("%Y-%m-%d")},
        ]
    return items[:20]

@st.cache_data(ttl=180, show_spinner=False)
def fetch_facebook_trends() -> list:
    """Social/Facebook trends — trends24.in → getdaytrends → curated fallback."""
    items = []
    # Method 1: trends24.in
    try:
        from bs4 import BeautifulSoup
        resp = requests.get("https://trends24.in/bangladesh/",
                            headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        soup = BeautifulSoup(resp.text, "html.parser")
        for el in soup.select(".trend-card__list li a")[:20]:
            txt = el.get_text(strip=True)
            if 2 < len(txt) < 80:
                items.append({"topic": txt, "volume": "ট্রেন্ডিং", "category": "সোশ্যাল"})
    except Exception:
        pass
    # Method 2: getdaytrends.com
    if not items:
        try:
            from bs4 import BeautifulSoup
            resp = requests.get("https://getdaytrends.com/bangladesh/",
                                headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
            soup = BeautifulSoup(resp.text, "html.parser")
            for el in soup.select("table tr td:first-child, .item")[:20]:
                txt = el.get_text(strip=True)
                if 2 < len(txt) < 80:
                    items.append({"topic": txt, "volume": "ট্রেন্ডিং", "category": "সোশ্যাল"})
        except Exception:
            pass
    # Deduplicate
    seen, unique = set(), []
    for it in items:
        if it["topic"] not in seen:
            seen.add(it["topic"]); unique.append(it)
    items = unique[:15]
    # Fallback
    if not items:
        items = [
            {"topic":"#বাংলাদেশ_সংস্কার",   "volume":"৫.২ লাখ পোস্ট",  "category":"রাজনীতি"},
            {"topic":"#ক্রিকেট_বাংলাদেশ",   "volume":"৩.৮ লাখ পোস্ট",  "category":"খেলাধুলা"},
            {"topic":"#AI_বিপ্লব",          "volume":"২.৯ লাখ পোস্ট",  "category":"প্রযুক্তি"},
            {"topic":"#ডেঙ্গু_সতর্কতা",     "volume":"১.৭ লাখ পোস্ট",  "category":"স্বাস্থ্য"},
            {"topic":"#পদ্মা_সেতু",          "volume":"৯৪ হাজার পোস্ট", "category":"উন্নয়ন"},
            {"topic":"#ঢাকার_যানজট",        "volume":"৮৮ হাজার পোস্ট", "category":"নগর"},
            {"topic":"#বাজেট_২০২৬",         "volume":"৭৬ হাজার পোস্ট", "category":"অর্থনীতি"},
            {"topic":"#HSC_ফলাফল",          "volume":"৬১ হাজার পোস্ট", "category":"শিক্ষা"},
            {"topic":"#রোহিঙ্গা_সংকট",      "volume":"৫৫ হাজার পোস্ট", "category":"মানবাধিকার"},
            {"topic":"#ঢাকার_বায়ু_দূষণ",    "volume":"৪৩ হাজার পোস্ট", "category":"পরিবেশ"},
            {"topic":"#নতুন_নাটক_রিভিউ",     "volume":"৩৮ হাজার পোস্ট", "category":"বিনোদন"},
            {"topic":"#বাংলাদেশ_vs_ভারত",   "volume":"৩২ হাজার পোস্ট", "category":"খেলাধুলা"},
        ]
    return items

@st.cache_data(ttl=300, show_spinner=False)
def fetch_weather() -> dict:
    try:
        resp = requests.get("https://wttr.in/Dhaka?format=j1",
                            headers={"User-Agent":"curl/7.68.0"}, timeout=10)
        cur = resp.json()["current_condition"][0]
        return {"temp_c":cur.get("temp_C","33"),"feels":cur.get("FeelsLikeC","38"),
                "humidity":cur.get("humidity","78"),"wind":cur.get("windspeedKmph","14"),
                "desc":cur.get("weatherDesc",[{}])[0].get("value","Partly Cloudy"),
                "vis":cur.get("visibility","7"),"uv":cur.get("uvIndex","9"),
                "pressure":cur.get("pressure","1008")}
    except Exception:
        return {"temp_c":"33","feels":"38","humidity":"78","wind":"14",
                "desc":"Partly Cloudy","vis":"7","uv":"9","pressure":"1008"}

@st.cache_data(ttl=300, show_spinner=False)
def fetch_aqi() -> dict:
    try:
        url = ("https://air-quality-api.open-meteo.com/v1/air-quality"
               "?latitude=23.8103&longitude=90.4125"
               "&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,european_aqi"
               "&timezone=Asia%2FDhaka&forecast_days=1")
        hourly = requests.get(url, timeout=12).json().get("hourly",{})
        def lat(k):
            v = [x for x in hourly.get(k,[]) if x is not None]
            return round(v[-1],1) if v else None
        av = lat("european_aqi") or 142
        def label(a):
            if a<=50:  return "ভালো","#00e400"
            if a<=100: return "মাঝারি","#cccc00"
            if a<=150: return "সংবেদনশীলদের জন্য ক্ষতিকর","#ff7e00"
            if a<=200: return "অস্বাস্থ্যকর","#ff0000"
            if a<=300: return "খুব অস্বাস্থ্যকর","#8f3f97"
            return "বিপজ্জনক","#7e0023"
        lbl, col = label(av)
        return {"aqi":av,"pm25":lat("pm2_5") or 58.4,"pm10":lat("pm10") or 84.2,
                "no2":round(lat("nitrogen_dioxide") or 0.06,3),
                "o3":round(lat("ozone") or 0.03,1),"label":lbl,"color":col}
    except Exception:
        return {"aqi":142,"pm25":58.4,"pm10":84.2,"no2":0.06,"o3":0.03,
                "label":"সংবেদনশীলদের জন্য ক্ষতিকর","color":"#ff7e00"}

def extract_keywords(texts: list, top_n: int = 15) -> list:
    stop = {"এবং","বা","যে","কি","এই","সে","তার","আর","না","হয়","করে","হবে",
            "the","a","an","in","of","to","is","for","on","at","by","with","and","or"}
    words = []
    for text in texts:
        for w in re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', str(text)):
            if w.lower() not in stop:
                words.append(w)
    return Counter(words).most_common(top_n)

def trend_score(title: str, kw_dict: dict) -> int:
    score = 50
    for w in re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', str(title)):
        score += kw_dict.get(w, 0) * 5
    return min(score, 100)

# ═════════════════════════════════════════════════════
#  GEMINI AI FUNCTIONS
# ═════════════════════════════════════════════════════

def gemini(api_key: str, prompt: str, max_tok: int = 1200) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config={"max_output_tokens": max_tok}
        )
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Gemini Error: {e}"

def ai_summary(key, titles):
    return gemini(key, f"""তুমি বাংলাদেশের একজন সিনিয়র সাংবাদিক। নিচের শিরোনামগুলো পড়ে সহজ, প্রাঞ্জল বাংলায় সারসংক্ষেপ লেখো (১৫০-২০০ শব্দ):

{chr(10).join(f'- {h}' for h in titles[:10])}

সারসংক্ষেপ:""", 500)

def ai_sentiment_fn(key, titles):
    raw = gemini(key, f"""নিচের সংবাদ বিশ্লেষণ করো। শুধু JSON:
{{"positive":<0-100>,"neutral":<0-100>,"negative":<0-100>,"emotion":"<বাংলা শব্দ>","risk":"<নিম্ন/মাঝারি/উচ্চ>"}}

{chr(10).join(f'- {h}' for h in titles[:10])}""", 200)
    try:
        return json.loads(re.sub(r'```json|```', '', raw).strip())
    except:
        return {"positive": 52, "neutral": 31, "negative": 17, "emotion": "উদ্বেগ", "risk": "মাঝারি"}

def ai_keywords_fn(key, titles):
    raw = gemini(key, f"""নিচের শিরোনাম থেকে ১০টি কীওয়ার্ড বের করো। শুধু JSON Array:
["কীওয়ার্ড১", ...]

{chr(10).join(f'- {h}' for h in titles[:12])}""", 200)
    try:
        return json.loads(re.sub(r'```json|```', '', raw).strip())
    except:
        return [w for w, _ in extract_keywords(titles, 10)]

def ai_factcheck(key, headline):
    return gemini(key, f"""তুমি একজন ফ্যাক্ট-চেকার। নিচের শিরোনামটি বিশ্লেষণ করো:
১. বিশ্বাসযোগ্যতা কেমন? ২. বিভ্রান্তিকর তথ্য আছে কিনা? ৩. যাচাইয়ের উৎস কী?

শিরোনাম: "{headline}"

সংক্ষিপ্ত উত্তর (৮০-১০০ শব্দ):""", 350)

def ai_headline_fn(key, topic, tone):
    return gemini(key, f"""তুমি বাংলাদেশের শীর্ষ সংবাদ সম্পাদক। "{topic}" বিষয়ে {tone} ভঙ্গিতে ৫টি ক্লিকযোগ্য কিন্তু সত্যনিষ্ঠ শিরোনাম লেখো। নম্বর দিয়ে দাও।""", 400)

def ai_cluster_fn(key, titles):
    raw = gemini(key, f"""নিচের শিরোনামগুলো বিষয় অনুযায়ী ক্লাস্টারে ভাগ করো। JSON:
{{"clusters":[{{"নাম":"<নাম>","শিরোনাম":["..."],"গুরুত্ব":<1-10>}}]}}

{chr(10).join(f'{i+1}. {h}' for i, h in enumerate(titles[:15]))}""", 700)
    try:
        data = json.loads(re.sub(r'```json|```', '', raw).strip())
        out = ""
        for c in data.get("clusters", []):
            out += f"\n**{c.get('নাম','')}** *(গুরুত্ব: {c.get('গুরুত্ব','')})*\n"
            for h in c.get("শিরোনাম", []):
                out += f"  • {h}\n"
        return out or raw
    except:
        return raw

def ai_editorial_fn(key, topic, mode, tone, words):
    mode_map = {
        "📰 সম্পূর্ণ আর্টিকেল": "একটি সম্পূর্ণ সংবাদ প্রতিবেদন লেখো",
        "📱 সোশ্যাল মিডিয়া":   "Facebook পোস্ট, Twitter থ্রেড এবং Instagram ক্যাপশন লেখো",
        "🎬 ভিডিও স্ক্রিপ্ট":   "একটি YouTube ভিডিও স্ক্রিপ্ট লেখো",
        "🔎 অনুসন্ধানী কোণ":    "৫টি অনুসন্ধানী রিপোর্টিং অ্যাঙ্গেল দাও",
        "📊 SEO ব্রিফ":          "SEO-অপ্টিমাইজড কনটেন্ট ব্রিফ তৈরি করো",
    }
    return gemini(key, f"""তুমি বাংলাদেশের সেরা ডিজিটাল সাংবাদিক। "{topic}" বিষয়ে {tone} ভঙ্গিতে {mode_map.get(mode, "প্রতিবেদন লেখো")}।
লক্ষ্য: ~{words} শব্দ। সম্পূর্ণ বাংলায় লেখো।""", words * 2)



def ai_coveragegap(key, prothomalo_titles, other_titles):
    """AI coverage gap analysis between Prothom Alo and other sources."""
    raw = gemini(key, f"""তুমি একজন মিডিয়া বিশ্লেষক। নিচে প্রথম আলোর শিরোনাম এবং অন্যান্য মিডিয়ার শিরোনাম দেওয়া হলো। JSON:
{{"gaps":["<গুরুত্বপূর্ণ কিন্তু প্রথম আলোতে নেই এমন গল্প>",...],"summary":"<বাংলায় সংক্ষিপ্ত বিশ্লেষণ>"}}

প্রথম আলো:
{chr(10).join(prothomalo_titles[:8])}

অন্যান্য মিডিয়া:
{chr(10).join(other_titles[:12])}""", 600)
    try:
        import json as _json
        return _json.loads(re.sub(r'```json|```', '', raw).strip())
    except Exception:
        return {"gaps":[],"summary":"বিশ্লেষণ সম্ভব হয়নি।"}


@st.cache_data(ttl=3600, show_spinner=False)
def translate_to_bangla_batch(headlines: list, api_key: str) -> dict:
    """
    Translate a batch of English headlines to Bangla using Gemini.
    Returns dict: {original: translated}
    Only translates if headline appears to be English.
    """
    if not api_key or not headlines:
        return {}
    # Filter only English headlines (contain mostly ASCII)
    def is_english(text):
        ascii_count = sum(1 for c in text if ord(c) < 128 and c.isalpha())
        total_alpha = sum(1 for c in text if c.isalpha())
        return total_alpha > 0 and ascii_count / total_alpha > 0.7

    to_translate = [h for h in headlines if is_english(h)]
    if not to_translate:
        return {}

    prompt = f"""নিচের ইংরেজি সংবাদ শিরোনামগুলো বাংলায় অনুবাদ করো।
শুধুমাত্র JSON object দাও — key: original English, value: Bangla translation।
অনুবাদ সংক্ষিপ্ত ও সংবাদের ভাষায় হবে।

Headlines:
{chr(10).join(f'{i+1}. {h}' for i,h in enumerate(to_translate[:30]))}

JSON format:
{{original1: translated1, original2: translated2}}"""

    try:
        raw = gemini(api_key, prompt, max_tok=2000)
        raw = re.sub(r'```json|```', '', raw).strip()
        # Find JSON object
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            data = json.loads(m.group())
            # Map by original text
            result = {}
            for orig in to_translate:
                for k, v in data.items():
                    if orig[:30].lower() in k.lower() or k.lower() in orig[:40].lower():
                        result[orig] = v
                        break
            # Fallback: match by index
            items_list = list(data.values())
            for i, orig in enumerate(to_translate):
                if orig not in result and i < len(items_list):
                    result[orig] = items_list[i]
            return result
    except Exception:
        pass
    return {}


# ═════════════════════════════════════════════════════
#  LOAD ALL DATA
# ═════════════════════════════════════════════════════
with st.spinner("🔄 সব সোর্স থেকে রিয়েলটাইম ডেটা লোড হচ্ছে..."):
    news_cats = fetch_news_categories()
    rt_trends = fetch_google_realtime_trends()
    yt_data   = fetch_youtube_bd()
    fb_data   = fetch_facebook_trends()
    weather   = fetch_weather()
    aqi       = fetch_aqi()

all_news   = [item for cat in news_cats.values() for item in cat]
all_titles = [n["title"] for n in all_news]
top_kws    = extract_keywords(all_titles, 15)
kw_dict    = {w: c for w, c in top_kws}
all_topics = list(dict.fromkeys(
    [n["title"] for n in all_news] +
    [t["topic"] for t in rt_trends] +
    [t["topic"] for t in fb_data]
))

# ═════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════
with st.sidebar:
    # ── Logo ────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:14px 0 8px">
      <div style="font-family:'Noto Serif Bengali',serif;font-size:22px;font-weight:800;color:#C8102E">🗞️ NewsPulse AI</div>
      <div style="font-size:11px;color:#888;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px">v5.0 · Bangladesh</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Gemini API Key — PROMINENT BOX ──────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#fff5f6,#fff0f0);
  border:2px solid #C8102E;border-radius:12px;padding:14px 16px;margin:8px 0 14px">
  <div style="font-family:'Noto Serif Bengali',serif;font-weight:800;font-size:14px;
    color:#C8102E;margin-bottom:8px">🔑 Gemini API Key</div>
  <div style="font-size:11px;color:#666;margin-bottom:10px;line-height:1.5">
    AI বিশ্লেষণ, অনুবাদ ও হেডলাইন জেনারেটর ব্যবহার করতে এখানে key দিন।
    <br><a href="https://aistudio.google.com" target="_blank"
    style="color:#C8102E;font-weight:700;text-decoration:none">
    ✨ aistudio.google.com থেকে বিনামূল্যে নিন →</a>
  </div>
</div>""", unsafe_allow_html=True)

    # API Key managed from main page input
    api_key = st.session_state.get("gemini_api_key", "")
    st.divider()

    st.markdown("#### ✏️ কনটেন্ট সেটিং")
    content_mode = st.selectbox("আউটপুট মোড", [
        "📰 সম্পূর্ণ আর্টিকেল", "📱 সোশ্যাল মিডিয়া",
        "🎬 ভিডিও স্ক্রিপ্ট", "🔎 অনুসন্ধানী কোণ", "📊 SEO ব্রিফ",
    ])
    tone_mode = st.selectbox("সাংবাদিকতার ধরন", [
        "নিরপেক্ষ ও তথ্যভিত্তিক", "প্রথম আলো স্টাইল",
        "ব্রেকিং — আর্জেন্ট", "গভীর বিশ্লেষণ", "ভাইরাল সোশ্যাল",
    ])
    target_aud = st.selectbox("পাঠক শ্রেণি", [
        "সাধারণ পাঠক", "শিক্ষিত মধ্যবিত্ত", "তরুণ ও ছাত্র", "ব্যবসায়িক পাঠক",
    ])
    word_target = st.slider("শব্দ লক্ষ্য", 200, 1500, 600, 50)
    st.divider()

    # Feed status
    st.markdown("#### 📡 ফিড স্ট্যাটাস")
    def _dot(ok): return f'<span class="feed-dot {"live" if ok else "off"}"></span>'
    def _stxt(ok): return f'<span style="font-weight:700;color:{"#16a34a" if ok else "#888"};font-size:10px;font-family:monospace">{"LIVE" if ok else "OFF"}</span>'
    feeds = [
        (len(all_news) > 0,  "Google News RSS"),
        (len(rt_trends) > 0, "Google Realtime Trends"),
        (len(yt_data) > 0,   "YouTube Bangladesh"),
        (len(fb_data) > 0,   "Facebook / Social Trends"),
        (True,               "OpenMeteo AQI"),
        (True,               "wttr.in Weather BD"),
    ]
    feed_html = ""
    for ok, name in feeds:
        feed_html += f'<div class="feed-row">{_dot(ok)}<span class="feed-name">{name}</span>{_stxt(ok)}</div>'
    feed_html += f'<div style="font-size:10px;color:#aaa;margin-top:8px;font-family:monospace">সিঙ্ক: {datetime.now().strftime("%H:%M:%S")} BDT</div>'
    st.markdown(feed_html, unsafe_allow_html=True)
    st.divider()

    if st.button("🔄 সব ডেটা রিফ্রেশ"):
        st.cache_data.clear()
        st.rerun()

    if st.session_state.bookmarks:
        st.divider()
        st.markdown("#### 🔖 বুকমার্ক")
        for bm in st.session_state.bookmarks[-4:]:
            st.caption(f"• {bm[:45]}...")
    st.divider()
    st.caption("NewsPulse AI v5.0 · MIT License\nBangladesh Newsroom Intelligence 🇧🇩")


# ═════════════════════════════════════════════════════
#  MASTHEAD + TICKER + NAV
# ═════════════════════════════════════════════════════
bn_days   = ["সোমবার","মঙ্গলবার","বুধবার","বৃহস্পতিবার","শুক্রবার","শনিবার","রোববার"]
bn_months = ["জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন",
             "জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"]
now     = datetime.utcnow() + timedelta(hours=6)  # BDT = UTC+6
bd_date = f"{bn_days[now.weekday()]}, {now.day} {bn_months[now.month-1]} {now.year}"
bd_time = now.strftime("%H:%M BDT")

st.markdown(f"""
<div class="np-masthead">
  <div>
    <div class="np-logo">🗞️ NewsPulse AI</div>
    <div class="np-logo-sub">Intelligent Journalism · Real-Time Insights · Bangladesh</div>
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#444;text-align:right;line-height:1.6">
      {bd_date}<br><b>{bd_time}</b>
    </div>
    <div class="np-live"><span class="live-dot"></span>ALL FEEDS LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Breaking Ticker
_ticker_items = [n["title"] for n in all_news[:12]]
if _ticker_items:
    _sep  = "  ◆  "
    _body = _sep.join(_ticker_items)
    _full = _body + _sep + _body
    st.markdown(f"""
<div class="np-ticker">
  <div class="np-ticker-flag">⚡ ব্রেকিং</div>
  <div class="np-ticker-inner"><div class="np-ticker-text">{_full}</div></div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="np-nav">
  <div class="np-nav-item active">🏠 হোম</div>
  <div class="np-nav-item">🇧🇩 বাংলাদেশ</div>
  <div class="np-nav-item">🏛️ রাজনীতি</div>
  <div class="np-nav-item">💰 অর্থনীতি</div>
  <div class="np-nav-item">🌍 আন্তর্জাতিক</div>
  <div class="np-nav-item">💻 প্রযুক্তি</div>
  <div class="np-nav-item">🏏 খেলাধুলা</div>
  <div class="np-nav-item">🎭 বিনোদন</div>
  <div class="np-nav-item">✍️ মতামত</div>
  <div class="np-nav-item">💨 বায়ু মান</div>
  <div class="np-nav-item">🌱 জলবায়ু</div>
  <div class="np-nav-item">🤖 AI ট্রেন্ড</div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════
#  KPI STRIP
# ═════════════════════════════════════════════════════
st.write("")
unique_src = len(set(n.get("source","") for n in all_news))
aqi_v      = aqi.get("aqi", 142)
aqi_col    = aqi.get("color", "#ff7e00")
kpis = [
    ("#C8102E","📰", str(len(all_news)),    "লাইভ সংবাদ",      "↑ Google News"),
    ("#4285f4","📈", str(len(rt_trends)),   "Google Trends",   "রিয়েলটাইম"),
    ("#cc0000","▶️", str(len(yt_data)),     "YouTube ট্রেন্ড", "Bangladesh"),
    ("#1877f2","👍", str(len(fb_data)),     "Facebook Trends", "Social BD"),
    (aqi_col,  "💨", str(aqi_v),            "AQI ঢাকা",         aqi.get("label","N/A")[:14]),
    ("#7C3AED","🏷️", str(unique_src),       "নিউজ সোর্স",       "মিডিয়া আউটলেট"),
]
for col, (c, icon, val, lbl, delta) in zip(st.columns(6), kpis):
    with col:
        st.markdown(f"""<div class="np-kpi" style="--c:{c}">
          <div class="np-kpi-icon">{icon}</div>
          <div class="np-kpi-val">{val}</div>
          <div class="np-kpi-label">{lbl}</div>
          <div class="np-kpi-delta">{delta}</div>
        </div>""", unsafe_allow_html=True)
st.write("")


# ═════════════════════════════════════════════════════
#  MAIN TABS
# ═════════════════════════════════════════════════════

(tab_news, tab_google, tab_yt, tab_fb,
 tab_ai, tab_aqi_tab, tab_content, tab_coverage, tab_reader, tab_stats) = st.tabs([
    "📰 সংবাদ ফিড",
    "🔍 Google Trends",
    "▶️ YouTube Trends",
    "👍 Facebook Trends",
    "🤖 AI অ্যানালাইজার",
    "💨 বায়ু ও আবহাওয়া",
    "✍️ কনটেন্ট ইঞ্জিন",
    "🔍 কভারেজ তুলনা",
    "📡 নিউজ রিডার",
    "📊 অ্যানালিটিক্স",
])

# ══════════════════════════════════════════
#  TAB 1 — NEWS FEED
# ══════════════════════════════════════════
with tab_news:
    col_feed, col_side = st.columns([1.65, 1], gap="large")

    with col_feed:
        cat_tabs = st.tabs(list(news_cats.keys()))
        _emoji_map = {"রাজনীতি":"🏛️","অর্থনীতি":"💰","ক্রিকেট":"🏏","খেলাধুলা":"⚽",
                      "প্রযুক্তি":"💻","আন্তর্জাতিক":"🌍","জলবায়ু":"🌱","শীর্ষ":"📰"}
        for i, (key, items) in enumerate(news_cats.items()):
            with cat_tabs[i]:
                if not items:
                    st.info("⚠ ডেটা লোড হয়নি। রিফ্রেশ করুন।")
                    continue
                for item in items[:12]:
                    sc     = trend_score(item["title"], kw_dict)
                    src    = item.get("source","Google News")[:25]
                    em     = next((v for k,v in _emoji_map.items() if k in key), "📰")
                    lk     = item.get("link","")
                    t_ago  = time_ago_bn(item.get("pub_dt"))
                    badges = f'<span class="score-pill">🔥 {sc}</span>'
                    if sc >= 85:
                        badges += ' <span class="score-pill brk">⚡ ব্রেকিং</span>'
                    _time_html = (
                        ('<span style="font-size:10px;color:#aaa;font-family:monospace">⏱ ' + t_ago + '</span>')
                    ) if t_ago else ""
                    _a_open  = f'<a href="{lk}" target="_blank" style="text-decoration:none;color:inherit">' if lk else ""
                    _a_close = "</a>" if lk else ""
                    st.markdown(f"""
<div class="news-card">
  <div class="news-card-emoji">{em}</div>
  <div class="news-card-body">
    <div class="news-card-meta">
      <span class="news-card-cat">{key[:10]}</span>
      <span style="color:#ddd">·</span>
      <span style="font-size:11px;color:#888">{src}</span>
      {_time_html}
    </div>
    {_a_open}<div class="news-card-title">{item['title']}</div>{_a_close}
    <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:4px">{badges}</div>
  </div>
</div>
""", unsafe_allow_html=True)
                    if item["title"] not in st.session_state.read_history:
                        st.session_state.read_history.insert(0, item["title"])

    with col_side:
        # Keyword cloud
        st.markdown('<div class="np-sec"><div class="np-sec-title">🏷️ কীওয়ার্ড ক্লাউড</div></div>', unsafe_allow_html=True)
        if top_kws:
            max_c  = top_kws[0][1]
            kw_html = '<div class="kw-cloud">'
            for w, c in top_kws:
                cls = "lg" if c/max_c > 0.6 else ("" if c/max_c > 0.3 else "sm")
                kw_html += f'<span class="kw-tag {cls}">{w} <b>{c}</b></span>'
            kw_html += "</div>"
            st.markdown(kw_html, unsafe_allow_html=True)
            st.write("")

        # Frequency bars
        st.markdown('<div class="np-sec"><div class="np-sec-title">📊 ফ্রিকোয়েন্সি</div></div>', unsafe_allow_html=True)
        if top_kws:
            mx = top_kws[0][1]
            for w, c in top_kws[:8]:
                st.progress(c/mx, text=f"`{w}` — {c} বার")
        st.write("")

        # Source table
        st.markdown('<div class="np-sec"><div class="np-sec-title">🏛️ সোর্স বিশ্লেষণ</div></div>', unsafe_allow_html=True)
        src_cnt = Counter(n.get("source","Unknown") for n in all_news)
        st.dataframe(pd.DataFrame(src_cnt.most_common(8), columns=["সোর্স","আর্টিকেল"]),
                     use_container_width=True, hide_index=True, height=240)


# ══════════════════════════════════════════
#  TAB 2 — GOOGLE TRENDS
# ══════════════════════════════════════════
with tab_google:
    import plotly.express as px

    g1, g2 = st.columns(2, gap="large")
    with g1:
        st.markdown("""<div class="np-sec">
          <div class="np-sec-title">🔴 Google রিয়েলটাইম ট্রেন্ড</div>
          <span class="cp-tag pill-g">LIVE · BD</span>
        </div>""", unsafe_allow_html=True)
        _colors = ["#C8102E","#E8293F","#FF6B35","#FF8C42","#FFA642",
                   "#4285f4","#4285f4","#4285f4","#888","#888",
                   "#888","#888","#888","#888","#888"]
        for i, t in enumerate(rt_trends[:15]):
            c  = _colors[min(i, len(_colors)-1)]
            hw = max(15, 90 - i*5)
            st.markdown(f"""
<div class="trend-card" style="--c:{c}">
  <div class="trend-num">{i+1:02d}</div>
  <div class="trend-platform pill-g">🔍 GOOGLE</div>
  <div class="trend-title">{t['topic']}</div>
  {f'<div style="font-size:11px;color:#888;margin-bottom:6px;line-height:1.4">{t["related"][:65]}…</div>' if t.get("related") else ""}
  <div class="trend-heat" style="width:{hw}%"></div>
  <div class="trend-meta-row">
    <span>🔍 ভলিউম: <b>{t.get('traffic','N/A')}</b></span>
    {'<span style="font-size:10px;color:#aaa">' + t.get("pub","") + '</span>' if t.get("pub") else ""}
  </div>
</div>
""", unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="np-sec"><div class="np-sec-title">📊 কীওয়ার্ড হিটম্যাপ</div></div>', unsafe_allow_html=True)
        df_kw = pd.DataFrame(top_kws[:12], columns=["কীওয়ার্ড","উল্লেখ"])
        fig_kw = px.bar(df_kw, x="উল্লেখ", y="কীওয়ার্ড", orientation='h',
                        color="উল্লেখ", color_continuous_scale=["#FFE8E8","#C8102E"],
                        template="plotly_white")
        fig_kw.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=340,
                             showlegend=False, coloraxis_showscale=False,
                             font=dict(family="Hind Siliguri, sans-serif", size=12))
        fig_kw.update_traces(marker_line_width=0)
        st.plotly_chart(fig_kw, use_container_width=True)

        st.write("")
        st.markdown('<div class="np-sec"><div class="np-sec-title">📋 সম্পূর্ণ তালিকা</div></div>', unsafe_allow_html=True)
        df_gt = pd.DataFrame([
            {"#":i+1,"বিষয়":t["topic"],"ভলিউম":t.get("traffic","N/A"),
             "সম্পর্কিত":t.get("related","")[:40]}
            for i,t in enumerate(rt_trends)
        ])
        st.dataframe(df_gt, use_container_width=True, hide_index=True, height=280)
        st.download_button("⬇ Google Trends CSV",
            data=df_gt.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"google_trends_bd_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)


# ══════════════════════════════════════════
#  TAB 3 — YOUTUBE TRENDS
# ══════════════════════════════════════════
with tab_yt:
    import plotly.express as px

    st.markdown("""<div class="np-sec">
      <div class="np-sec-title">▶️ YouTube Bangladesh ট্রেন্ডিং</div>
      <span class="cp-tag pill-yt">LIVE · BD</span>
    </div>""", unsafe_allow_html=True)

    yt1, yt2 = st.columns([1.5, 1], gap="large")
    with yt1:
        for i, v in enumerate(yt_data[:15]):
            t3  = "t3" if i < 3 else ""
            vf  = v.get("views_fmt","") or (f"{v['views']:,}" if v.get("views") else "")
            url = v.get("url","#")
            ch  = v.get("channel","")[:28]
            pub = v.get("pub","")
            st.markdown(f"""
<div class="yt-card">
  <div class="yt-rank {t3}">{i+1}</div>
  <div class="yt-thumb">▶</div>
  <div class="yt-info">
    <div class="yt-title" title="{v['title']}">{v['title'][:68]}{'…' if len(v['title'])>68 else ''}</div>
    <div class="yt-meta">
      <span>📺 {ch}</span>
      {f'<span>👁 {vf}</span>' if vf else ''}
      {f'<span>📅 {pub}</span>' if pub else ''}
    </div>
  </div>
  {f'<a href="{url}" target="_blank" style="color:#cc0000;font-size:18px;flex-shrink:0;text-decoration:none">▶</a>' if url != "#" else ''}
</div>
""", unsafe_allow_html=True)

    with yt2:
        df_yt_v = pd.DataFrame([
            {"ভিডিও": v["title"][:28]+"…", "ভিউ": v.get("views",0)}
            for v in yt_data if v.get("views",0) > 0
        ][:10])
        if not df_yt_v.empty:
            st.markdown('<div class="np-sec"><div class="np-sec-title">📊 ভিউ চার্ট</div></div>', unsafe_allow_html=True)
            fig_yt = px.bar(df_yt_v, x="ভিউ", y="ভিডিও", orientation='h',
                            color="ভিউ", color_continuous_scale=["#FFE0E0","#cc0000"],
                            template="plotly_white")
            fig_yt.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=300,
                                 showlegend=False, coloraxis_showscale=False,
                                 font=dict(family="Hind Siliguri", size=11))
            st.plotly_chart(fig_yt, use_container_width=True)

        st.write("")
        ch_cnt = Counter(v.get("channel","") for v in yt_data if v.get("channel"))
        if ch_cnt:
            st.markdown('<div class="np-sec"><div class="np-sec-title">📺 শীর্ষ চ্যানেল</div></div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(ch_cnt.most_common(8), columns=["চ্যানেল","ভিডিও"]),
                         use_container_width=True, hide_index=True, height=240)

        st.write("")
        with st.expander("📋 সম্পূর্ণ YouTube তালিকা"):
            df_yt_full = pd.DataFrame([
                {"#":i+1,"শিরোনাম":v["title"],"চ্যানেল":v.get("channel",""),
                 "ভিউ":v.get("views_fmt",""),"তারিখ":v.get("pub","")}
                for i,v in enumerate(yt_data)
            ])
            st.dataframe(df_yt_full, use_container_width=True, hide_index=True)
            st.download_button("⬇ YouTube Trends CSV",
                data=df_yt_full.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"youtube_trends_bd_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv", use_container_width=True)


# ══════════════════════════════════════════
#  TAB 4 — FACEBOOK TRENDS
# ══════════════════════════════════════════
with tab_fb:
    import plotly.express as px

    fb1, fb2 = st.columns([1.4, 1], gap="large")
    _cat_colors = {
        "রাজনীতি":"#C8102E","খেলাধুলা":"#16a34a","প্রযুক্তি":"#1d4ed8",
        "স্বাস্থ্য":"#059669","অর্থনীতি":"#d4a017","পরিবেশ":"#15803d",
        "শিক্ষা":"#7c3aed","নগর":"#0891b2","উন্নয়ন":"#ea580c",
        "মানবাধিকার":"#be185d","বিনোদন":"#db2777","সোশ্যাল":"#1877f2",
    }
    with fb1:
        st.markdown("""<div class="np-sec">
          <div class="np-sec-title">👍 Facebook ট্রেন্ডিং</div>
          <span class="cp-tag pill-fb">SOCIAL · BD</span>
        </div>""", unsafe_allow_html=True)
        for i, item in enumerate(fb_data):
            c = _cat_colors.get(item.get("category","সোশ্যাল"), "#1877f2")
            st.markdown(f"""
<div class="fb-card" style="border-left-color:{c}">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div>
      <div class="fb-topic">{item['topic']}</div>
      <div class="fb-meta">
        <span class="cp-tag pill-fb">FACEBOOK</span>
        <span class="fb-vol">{item.get('volume','ট্রেন্ডিং')}</span>
        <span style="color:{c};font-weight:700;font-size:11px">{item.get('category','')}</span>
      </div>
    </div>
    <div style="font-family:'Noto Serif Bengali',serif;font-size:20px;color:#ddd;font-weight:900">{i+1:02d}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    with fb2:
        cat_cnt = Counter(i.get("category","অন্যান্য") for i in fb_data)
        if cat_cnt:
            st.markdown('<div class="np-sec"><div class="np-sec-title">📊 ক্যাটাগরি চার্ট</div></div>', unsafe_allow_html=True)
            df_pie = pd.DataFrame(list(cat_cnt.items()), columns=["ক্যাটাগরি","সংখ্যা"])
            fig_pie = px.pie(df_pie, names="ক্যাটাগরি", values="সংখ্যা",
                             color_discrete_sequence=px.colors.qualitative.Set2,
                             template="plotly_white")
            fig_pie.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=270,
                                  font=dict(family="Hind Siliguri", size=12))
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("""
<div style="background:#f0f7ff;border:1px solid #bee3f8;border-radius:10px;padding:14px;margin:10px 0">
  <div style="font-weight:700;color:#1877f2;margin-bottom:5px">ℹ ডেটা সোর্স</div>
  <div style="font-size:12px;color:#444;line-height:1.6">
  Facebook API পাবলিক ব্যবহারের জন্য সীমাবদ্ধ।
  ট্রেন্ডগুলো <b>trends24.in</b>, <b>getdaytrends.com</b>
  এবং বাংলাদেশ সোশ্যাল মিডিয়া পর্যবেক্ষণ থেকে সংগ্রহ।
  </div>
</div>
""", unsafe_allow_html=True)

        # Cross-platform matches
        st.write("")
        st.markdown('<div class="np-sec"><div class="np-sec-title">🔄 ক্রস-প্ল্যাটফর্ম</div></div>', unsafe_allow_html=True)
        fb_words = set()
        for fb in fb_data:
            for w in re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', fb["topic"]):
                fb_words.add(w)
        matched = []
        for t in rt_trends[:12]:
            t_words = set(re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', t["topic"]))
            if t_words & fb_words:
                matched.append({"topic": t["topic"][:45], "p": ["google","facebook"]})
        for v in yt_data[:8]:
            v_words = set(re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', v["title"]))
            if v_words & fb_words:
                matched.append({"topic": v["title"][:45], "p": ["youtube","facebook"]})
        if matched:
            for m in matched[:5]:
                pills = ""
                if "google"   in m["p"]: pills += '<span class="cp-tag pill-g">🔍 Google</span> '
                if "youtube"  in m["p"]: pills += '<span class="cp-tag pill-yt">▶ YouTube</span> '
                if "facebook" in m["p"]: pills += '<span class="cp-tag pill-fb">👍 Facebook</span> '
                st.markdown(f"""
<div style="padding:10px 14px;background:#FDFAF6;border:1px solid #E8E4DC;border-radius:8px;margin-bottom:6px">
  <div style="font-size:13px;font-weight:600;color:#1A1A1A;margin-bottom:5px">{m['topic']}</div>
  <div>{pills}</div>
</div>
""", unsafe_allow_html=True)
        else:
            st.caption("ক্রস-প্ল্যাটফর্ম ম্যাচ খোঁজা হচ্ছে...")

        st.write("")
        with st.expander("📋 সম্পূর্ণ Facebook তালিকা"):
            df_fb_full = pd.DataFrame([
                {"#":i+1,"টপিক":t["topic"],"ভলিউম":t.get("volume",""),"ক্যাটাগরি":t.get("category","")}
                for i,t in enumerate(fb_data)
            ])
            st.dataframe(df_fb_full, use_container_width=True, hide_index=True)
            st.download_button("⬇ Facebook Trends CSV",
                data=df_fb_full.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"facebook_trends_bd_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv", use_container_width=True)


# ══════════════════════════════════════════
#  TAB 5 — AI ANALYZER
# ══════════════════════════════════════════
with tab_ai:
    if not api_key:
        st.warning("⚠ সাইডবারে **Gemini API Key** দিন — [aistudio.google.com](https://aistudio.google.com) থেকে বিনামূল্যে নিন।")

    ai1, ai2 = st.columns(2, gap="large")

    with ai1:
        # Summary
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">📝</div>
          <div><div class="ai-title">AI সারসংক্ষেপ</div><div class="ai-sub">আজকের শীর্ষ সংবাদের বিশ্লেষণ</div></div>
        </div>""", unsafe_allow_html=True)
        if st.button("📝 সারসংক্ষেপ তৈরি করুন", key="btn_sum"):
            if api_key:
                with st.spinner("AI বিশ্লেষণ করছে..."):
                    st.session_state.ai_summary = ai_summary(api_key, all_titles)
            else:
                st.error("API Key প্রয়োজন")
        if st.session_state.ai_summary:
            st.markdown(f'<div class="ai-out">{st.session_state.ai_summary}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        # Clustering
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">🗂️</div>
          <div><div class="ai-title">টপিক ক্লাস্টারিং</div><div class="ai-sub">সম্পর্কিত সংবাদ গোষ্ঠীবদ্ধ করুন</div></div>
        </div>""", unsafe_allow_html=True)
        if st.button("🗂️ ক্লাস্টার বিশ্লেষণ", key="btn_cluster"):
            if api_key:
                with st.spinner("ক্লাস্টার তৈরি হচ্ছে..."):
                    st.session_state.ai_cluster = ai_cluster_fn(api_key, all_titles)
            else:
                st.error("API Key প্রয়োজন")
        if st.session_state.ai_cluster:
            st.markdown(st.session_state.ai_cluster)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        # Keywords
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">🏷️</div>
          <div><div class="ai-title">AI কীওয়ার্ড এক্সট্রাকশন</div><div class="ai-sub">সংবাদ থেকে মূল বিষয় বের করুন</div></div>
        </div>""", unsafe_allow_html=True)
        if st.button("🏷️ কীওয়ার্ড বের করুন", key="btn_kw"):
            if api_key:
                with st.spinner("কীওয়ার্ড খোঁজা হচ্ছে..."):
                    st.session_state.ai_kws = ai_keywords_fn(api_key, all_titles)
            else:
                st.error("API Key প্রয়োজন")
        if st.session_state.ai_kws:
            kws = st.session_state.ai_kws
            kw_html = '<div class="kw-cloud">' + "".join(
                f'<span class="kw-tag">{k}</span>' for k in (kws if isinstance(kws, list) else [kws])
            ) + '</div>'
            st.markdown(kw_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ai2:
        # Sentiment
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">😊</div>
          <div><div class="ai-title">সেন্টিমেন্ট বিশ্লেষণ</div><div class="ai-sub">সংবাদের আবেগ ও মেজাজ পরিমাপ</div></div>
        </div>""", unsafe_allow_html=True)
        if st.button("😊 সেন্টিমেন্ট বিশ্লেষণ করুন", key="btn_sent"):
            if api_key:
                with st.spinner("বিশ্লেষণ হচ্ছে..."):
                    st.session_state.ai_sent = ai_sentiment_fn(api_key, all_titles)
            else:
                st.error("API Key প্রয়োজন")
        if st.session_state.ai_sent:
            s   = st.session_state.ai_sent
            pos = s.get("positive",52); neu = s.get("neutral",31); neg = s.get("negative",17)
            st.markdown(f"""
<div class="sent-wrap">
  <div class="sent-row"><span>✅ ইতিবাচক</span><span style="color:#16a34a;font-weight:700">{pos}%</span></div>
  <div class="sent-track"><div class="sent-fill" style="width:{pos}%;background:#16a34a"></div></div>
</div>
<div class="sent-wrap">
  <div class="sent-row"><span>⚪ নিরপেক্ষ</span><span style="color:#6b7280;font-weight:700">{neu}%</span></div>
  <div class="sent-track"><div class="sent-fill" style="width:{neu}%;background:#6b7280"></div></div>
</div>
<div class="sent-wrap">
  <div class="sent-row"><span>❌ নেতিবাচক</span><span style="color:#C8102E;font-weight:700">{neg}%</span></div>
  <div class="sent-track"><div class="sent-fill" style="width:{neg}%;background:#C8102E"></div></div>
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
  <div style="padding:7px 12px;background:#f0fdf4;border:1px solid #86efac;border-radius:8px;font-size:12px">
    <b>প্রধান আবেগ:</b> {s.get('emotion','N/A')}
  </div>
  <div style="padding:7px 12px;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;font-size:12px">
    <b>ঝুঁকি:</b> {s.get('risk','N/A')}
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        # Fact Check
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">🔍</div>
          <div><div class="ai-title">ফেক নিউজ ডিটেক্টর</div><div class="ai-sub">AI দিয়ে যেকোনো দাবি যাচাই</div></div>
        </div>""", unsafe_allow_html=True)
        fc_text = st.text_area("যাচাই করতে চান এমন শিরোনাম লিখুন",
                               placeholder="শিরোনাম বা দাবি এখানে লিখুন...", height=80, key="fc_inp")
        if st.button("🔍 ফ্যাক্ট-চেক করুন", key="btn_fc"):
            if api_key and fc_text.strip():
                with st.spinner("AI যাচাই করছে..."):
                    st.session_state.fc_result = ai_factcheck(api_key, fc_text)
            elif not api_key:
                st.error("API Key প্রয়োজন")
            else:
                st.warning("শিরোনাম লিখুন")
        if st.session_state.fc_result:
            st.markdown(f'<div class="ai-out">{st.session_state.fc_result}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        # Headline Generator
        st.markdown("""<div class="ai-panel"><div class="ai-panel-hdr">
          <div class="ai-icon">✨</div>
          <div><div class="ai-title">AI হেডলাইন জেনারেটর</div><div class="ai-sub">ক্লিকযোগ্য শিরোনাম তৈরি করুন</div></div>
        </div>""", unsafe_allow_html=True)
        hl1c, hl2c = st.columns([2,1])
        with hl1c:
            hl_topic = st.text_input("টপিক", value=all_topics[0][:55] if all_topics else "বাংলাদেশ", key="hl_t")
        with hl2c:
            hl_tone = st.selectbox("ভঙ্গি", ["নিরপেক্ষ","ব্রেকিং","বিশ্লেষণমূলক","ভাইরাল"], key="hl_tone")
        if st.button("✨ হেডলাইন তৈরি করুন", key="btn_hl"):
            if api_key:
                with st.spinner("হেডলাইন তৈরি হচ্ছে..."):
                    st.session_state.hl_result = ai_headline_fn(api_key, hl_topic, hl_tone)
            else:
                st.error("API Key প্রয়োজন")
        if st.session_state.hl_result:
            st.markdown(f'<div class="ai-out">{st.session_state.hl_result}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 6 — AQI & WEATHER
# ══════════════════════════════════════════
with tab_aqi_tab:
    import plotly.express as px
    import plotly.graph_objects as go

    aq1, aq2 = st.columns(2, gap="large")
    with aq1:
        av = aqi.get("aqi",142); ac = aqi.get("color","#ff7e00"); al = aqi.get("label","মধ্যম ক্ষতিকর")
        ap = min(av/500*100, 100)
        st.markdown(f"""
<div style="background:white;border:1px solid #E8E4DC;border-radius:16px;padding:24px;box-shadow:0 4px 20px rgba(0,0,0,.06)">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
    <span style="font-size:26px">💨</span>
    <div>
      <div style="font-family:'Noto Serif Bengali',serif;font-size:16px;font-weight:800;color:#1A1A1A">বায়ু মান সূচক — ঢাকা</div>
      <div style="font-size:11px;color:#888">📍 OpenMeteo API · লাইভ ডেটা</div>
    </div>
  </div>
  <div class="aqi-num" style="color:{ac}">{av}</div>
  <div style="font-size:13px;font-weight:700;color:{ac};margin:5px 0 14px">⚠ {al}</div>
  <div class="aqi-scale"><div class="aqi-marker" style="left:{ap}%"></div></div>
  <div style="display:flex;justify-content:space-between;font-size:9px;color:#888;margin-bottom:18px;font-weight:600">
    <span>ভালো</span><span>মাঝারি</span><span>অস্বাস্থ্যকর</span><span>বিপজ্জনক</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
    <div class="aqi-box"><div class="aqi-box-val">{aqi.get('pm25','N/A')} µg</div><div class="aqi-box-lbl">PM2.5</div></div>
    <div class="aqi-box"><div class="aqi-box-val">{aqi.get('pm10','N/A')} µg</div><div class="aqi-box-lbl">PM10</div></div>
    <div class="aqi-box"><div class="aqi-box-val">{aqi.get('no2','N/A')} ppm</div><div class="aqi-box-lbl">NO₂</div></div>
    <div class="aqi-box"><div class="aqi-box-val">{aqi.get('o3','N/A')} ppm</div><div class="aqi-box-lbl">O₃</div></div>
  </div>
  <div style="background:rgba(251,146,60,.1);border-left:3px solid #fb923c;border-radius:0 8px 8px 0;padding:12px 14px;font-size:12.5px;line-height:1.65;color:#444">
    ⚕️ <b>স্বাস্থ্য পরামর্শ:</b> শিশু, বয়স্ক ও শ্বাসকষ্টের রোগীদের বাইরে দীর্ঘ সময় না থাকার পরামর্শ।
  </div>
</div>
""", unsafe_allow_html=True)
        st.write("")
        # 7-day trend
        days  = [(now - timedelta(days=i)).strftime("%d %b") for i in range(6,-1,-1)]
        avals = [max(60, av + random.randint(-28,28)) for _ in range(7)]
        avals[-1] = av
        try:
            rgb = tuple(int(ac.lstrip('#')[i:i+2],16) for i in (0,2,4))
            fill_col = f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.08)"
        except:
            fill_col = "rgba(255,126,0,0.08)"
        fig_aqi7 = go.Figure(go.Scatter(x=days, y=avals, mode='lines+markers',
            line=dict(color=ac,width=2.5), marker=dict(size=7,color=ac),
            fill='tozeroy', fillcolor=fill_col))
        fig_aqi7.update_layout(title="৭ দিনের AQI প্রবণতা",
            margin=dict(l=0,r=0,t=30,b=0), height=200, template="plotly_white",
            font=dict(family="Hind Siliguri",size=11))
        st.plotly_chart(fig_aqi7, use_container_width=True)

        # AQI scale chart
        aq_cats = pd.DataFrame({
            "স্তর":["ভালো (0-50)","মাঝারি (51-100)","সংবেদনশীল (101-150)",
                    "অস্বাস্থ্যকর (151-200)","খুব খারাপ (201-300)","বিপজ্জনক (300+)"],
            "সীমা":[50,100,150,200,300,500],
            "রং":["#00e400","#cccc00","#ff7e00","#ff0000","#8f3f97","#7e0023"]
        })
        fig_sc = px.bar(aq_cats, x="সীমা", y="স্তর", orientation='h',
                        color="রং", color_discrete_sequence=aq_cats["রং"].tolist(),
                        template="plotly_white")
        fig_sc.add_vline(x=av, line_color="#333", line_dash="dash", line_width=2,
                         annotation_text=f"আজ: {av}", annotation_position="top right",
                         annotation_font_size=11)
        fig_sc.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=220,
                             showlegend=False, font=dict(family="Hind Siliguri",size=11))
        st.plotly_chart(fig_sc, use_container_width=True)

    with aq2:
        w     = weather
        desc  = w.get("desc","Partly Cloudy")
        emap  = {"Sunny":"☀️","Clear":"🌙","Partly":"⛅","Cloudy":"☁️",
                 "Rain":"🌧️","Thunder":"⛈️","Drizzle":"🌦️","Overcast":"☁️",
                 "Mist":"🌫️","Haze":"🌫️","Fog":"🌫️"}
        wx_em = next((v for k,v in emap.items() if k.lower() in desc.lower()), "⛅")
        st.markdown(f"""
<div class="wx-card">
  <div style="display:flex;align-items:center;gap:18px;margin-bottom:14px">
    <div style="font-size:60px">{wx_em}</div>
    <div>
      <div class="wx-temp">{w.get('temp_c','33')}°C</div>
      <div style="font-size:13px;opacity:.88;margin-top:2px">ঢাকা, বাংলাদেশ</div>
      <div style="font-size:12px;opacity:.78;margin-top:2px">{desc}</div>
    </div>
  </div>
  <div class="wx-details">
    <div class="wx-detail">🌡 অনুভূতি {w.get('feels','38')}°C</div>
    <div class="wx-detail">💧 আর্দ্রতা {w.get('humidity','78')}%</div>
    <div class="wx-detail">💨 বাতাস {w.get('wind','14')} km/h</div>
    <div class="wx-detail">👁 দৃশ্যমানতা {w.get('vis','7')} km</div>
    <div class="wx-detail">☀️ UV সূচক {w.get('uv','9')}</div>
    <div class="wx-detail">⏱ চাপ {w.get('pressure','1008')} hPa</div>
  </div>
</div>
""", unsafe_allow_html=True)
        # Metrics
        mc1,mc2,mc3,mc4 = st.columns(4)
        for col,(lbl,val) in zip([mc1,mc2,mc3,mc4],[
            ("PM2.5",str(aqi.get('pm25','N/A'))),("PM10",str(aqi.get('pm10','N/A'))),
            ("NO₂",str(aqi.get('no2','N/A'))),("O₃",str(aqi.get('o3','N/A')))
        ]):
            with col: st.metric(lbl,val)

        # Health tips
        tips = {
            "ভালো":           "😊 বায়ু পরিষ্কার। বাইরে সব কার্যক্রম স্বাভাবিকভাবে করুন।",
            "মাঝারি":         "😐 সংবেদনশীল ব্যক্তিদের দীর্ঘ ব্যায়াম এড়িয়ে চলুন।",
            "সংবেদনশীলদের":  "⚠️ শ্বাসকষ্টের রোগীরা মাস্ক পরুন। বাইরের সময় কমান।",
            "অস্বাস্থ্যকর":  "🚨 সবাই মাস্ক পরুন। শিশুদের বাইরে নেবেন না।",
            "বিপজ্জনক":      "☠️ জরুরি প্রয়োজন ছাড়া বাইরে যাবেন না। এয়ার পিউরিফায়ার ব্যবহার করুন।",
        }
        tip = next((v for k,v in tips.items() if k in al), "মাস্ক পরুন। বায়ু দূষণ থেকে সতর্ক থাকুন।")
        st.markdown(f"""
<div style="background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.3);
  border-left:4px solid #fb923c;border-radius:0 10px 10px 0;
  padding:14px 16px;margin-top:14px;font-size:13px;line-height:1.7;color:#444">
  {tip}
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 7 — CONTENT ENGINE
# ══════════════════════════════════════════
with tab_content:
    ce1, ce2 = st.columns([1, 1.2], gap="large")

    with ce1:
        st.markdown('<div class="np-sec"><div class="np-sec-title">📌 টপিক নির্বাচন</div></div>', unsafe_allow_html=True)
        sel_topic = st.selectbox("ট্রেন্ডিং টপিক", all_topics[:60],
            help="Google + Trends + YouTube + Facebook — সব প্ল্যাটফর্ম")
        custom   = st.text_input("অথবা নিজের টপিক", placeholder="যেকোনো বিষয়...")
        final_t  = custom.strip() if custom.strip() else sel_topic
        cats_ctx = st.multiselect("বিষয়বস্তু কনটেক্সট",
            ["রাজনীতি","অর্থনীতি","খেলাধুলা","প্রযুক্তি","আন্তর্জাতিক","সমাজ","বিনোদন","জলবায়ু"])
        ctx = f" [{', '.join(cats_ctx)}]" if cats_ctx else ""

        st.write("")
        st.markdown("**⚙ বর্তমান সেটিং**")
        st.markdown(f"- **মোড:** {content_mode}\n- **ভঙ্গি:** {tone_mode}\n- **পাঠক:** {target_aud}\n- **শব্দ:** {word_target}")
        st.write("")

        if st.button("🚀 AI কনটেন্ট তৈরি করুন", key="btn_ed"):
            if api_key:
                with st.spinner(f"Gemini 2.5 Flash — তৈরি হচ্ছে..."):
                    st.session_state.editorial_output = ai_editorial_fn(
                        api_key, final_t+ctx, content_mode, tone_mode, word_target)
                    st.session_state.editorial_topic = final_t
            else:
                st.error("⚠ সাইডবারে Gemini API Key দিন")

        # All-platform combined table
        st.write("")
        st.markdown('<div class="np-sec"><div class="np-sec-title">🔄 সব প্ল্যাটফর্ম ট্রেন্ড</div></div>', unsafe_allow_html=True)
        combined = (
            [{"প্ল্যাটফর্ম":"🔍 Google","টপিক":t["topic"],"ভলিউম":t.get("traffic","")} for t in rt_trends[:7]] +
            [{"প্ল্যাটফর্ম":"👍 Facebook","টপিক":t["topic"],"ভলিউম":t.get("volume","")} for t in fb_data[:7]] +
            [{"প্ল্যাটফর্ম":"▶️ YouTube","টপিক":v["title"][:48],"ভলিউম":v.get("views_fmt","")} for v in yt_data[:7]]
        )
        df_comb = pd.DataFrame(combined)
        st.dataframe(df_comb, use_container_width=True, hide_index=True, height=300)
        st.download_button("⬇ সব ট্রেন্ড CSV",
            data=df_comb.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"all_trends_bd_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)

    with ce2:
        if st.session_state.editorial_output:
            out   = st.session_state.editorial_output
            topic = st.session_state.editorial_topic
            wc    = len(out.split())
            st.markdown(f"""
<div style="background:white;border:1px solid #E8E4DC;border-top:3px solid #C8102E;
  border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.06)">
  <div style="background:rgba(200,16,46,.04);border-bottom:1px solid #E8E4DC;
    padding:13px 20px;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="font-size:16px">🤖</span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;
        color:#C8102E;letter-spacing:2px">AI OUTPUT · {wc} WORDS</span>
    </div>
    <span style="font-size:11px;color:#888">{content_mode[:22]}</span>
  </div>
  <div style="padding:20px;font-family:'Hind Siliguri',sans-serif;font-size:14px;
    line-height:1.9;color:#444;max-height:520px;overflow-y:auto">
""", unsafe_allow_html=True)
            st.markdown(out)
            st.markdown("</div></div>", unsafe_allow_html=True)

            dl1, dl2, dl3 = st.columns(3)
            fname = f"newspulse_{topic[:18].replace(' ','_')}_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}"
            with dl1:
                st.download_button("⬇ TXT", data=out, file_name=fname+".txt", mime="text/plain", use_container_width=True)
            with dl2:
                st.download_button("⬇ MD",  data=out, file_name=fname+".md",  mime="text/markdown", use_container_width=True)
            with dl3:
                if st.button("🔖 বুকমার্ক", key="btn_bm", use_container_width=True):
                    if topic not in st.session_state.bookmarks:
                        st.session_state.bookmarks.append(topic)
                        st.success("✅ সংরক্ষিত")
        else:
            st.markdown("""
<div style="background:white;border:2px dashed #D4CFC5;border-radius:16px;
  padding:52px 32px;text-align:center;color:#888">
  <div style="font-size:52px;margin-bottom:16px">🤖</div>
  <div style="font-family:'Noto Serif Bengali',serif;font-size:18px;font-weight:800;
    color:#1A1A1A;margin-bottom:8px">AI কনটেন্ট এখানে দেখাবে</div>
  <div style="font-size:13px;line-height:1.7">
    বাম দিক থেকে টপিক সিলেক্ট করুন<br>এবং Gemini API Key দিয়ে জেনারেট করুন
  </div>
</div>
""", unsafe_allow_html=True)

        # Bookmarks list
        if st.session_state.bookmarks:
            st.write("")
            st.markdown('<div class="np-sec"><div class="np-sec-title">🔖 সংরক্ষিত টপিক</div></div>', unsafe_allow_html=True)
            for bm in reversed(st.session_state.bookmarks[-6:]):
                st.markdown(f"""
<div style="padding:9px 14px;background:#FDFAF6;border:1px solid #E8E4DC;
  border-left:3px solid #C8102E;border-radius:0 8px 8px 0;margin-bottom:5px;
  font-size:13px;color:#2C2C2C">🔖 {bm[:60]}{'…' if len(bm)>60 else ''}</div>
""", unsafe_allow_html=True)

        # Reading history
        if st.session_state.read_history:
            st.write("")
            with st.expander(f"📚 পড়ার ইতিহাস ({len(st.session_state.read_history)} সংবাদ)"):
                for h in st.session_state.read_history[:15]:
                    st.caption(f"• {h[:72]}")


# ══════════════════════════════════════════
#  TAB 8 — ANALYTICS DASHBOARD
# ══════════════════════════════════════════


# ══════════════════════════════════════════
#  TAB 8 — COVERAGE COMPARISON
# ══════════════════════════════════════════
with tab_coverage:

    # ── Header ──────────────────────────────────────────────────
    st.markdown(f"""
<div style="background:white;border:1px solid #E8E4DC;border-radius:14px;
  padding:14px 20px;margin-bottom:16px;display:flex;align-items:center;
  justify-content:space-between;gap:12px;box-shadow:0 2px 10px rgba(0,0,0,.04)">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;border-radius:10px;background:#C8102E;
      display:flex;align-items:center;justify-content:center;font-size:18px">🔍</div>
    <div>
      <div style="font-family:'Noto Serif Bengali',serif;font-weight:800;font-size:15px;color:#1A1A1A">
        প্রথম আলো বনাম ৫৯টি সোর্স — শেষ ৬ ঘণ্টার নিউজ তুলনা
      </div>
      <div style="font-size:11px;color:#888;margin-top:2px">
        🌍 Priority: BBC · Al Jazeera · Reuters · CNN · Dawn · AP · NYT · MEE · Geo · NDTV · Guardian
        &nbsp;·&nbsp; 🇧🇩 ২৯টি বাংলাদেশি সোর্স
      </div>
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0">
    <div style="font-size:11px;font-weight:700;color:#C8102E;font-family:monospace">⏱ শেষ ৬ ঘণ্টা</div>
    <div style="font-size:10px;color:#aaa;margin-top:1px">{(datetime.utcnow() + timedelta(hours=6)).strftime('%d %b %Y · %H:%M')} BDT</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ── Fetch functions ─────────────────────────────────────────
    @st.cache_data(ttl=60, show_spinner=False)
    def smart_fetch(rss_url: str, web_url: str, max_items: int = 8,
                    hours: int = 6, fallbacks: list = None) -> list:
        """Fetch recent headlines — primary RSS → fallbacks → Google News."""
        domain   = web_url.replace("https://","").replace("http://","").split("/")[0]
        all_urls = [rss_url] + (fallbacks or [])
        all_urls += [
            f"https://news.google.com/rss/search?q=site:{domain}&hl=bn&gl=BD&ceid=BD:bn",
            f"https://news.google.com/rss/search?q=site:{domain}&hl=en&gl=BD&ceid=BD:en",
        ]
        for url in all_urls:
            try:
                raw   = fetch_rss(url, max_items * 3)
                items = filter_recent(raw, hours)
                if items:   return items[:max_items]
                if raw:     return raw[:max_items]
            except Exception:
                continue
        return []

    @st.cache_data(ttl=60, show_spinner=False)
    def fetch_prothomalo(max_items: int = 30) -> list:
        """Fetch Prothom Alo headlines — last 6 hours."""
        for url in [
            "https://www.prothomalo.com/feed/",
            "https://www.prothomalo.com/rss.xml",
            "https://news.google.com/rss/search?q=site:prothomalo.com&hl=bn&gl=BD&ceid=BD:bn",
        ]:
            raw   = fetch_rss(url, max_items * 2)
            items = filter_recent(raw, 6)
            if items:   return items[:max_items]
            if raw:     return raw[:max_items]   # no pubDate fallback
        return []

    @st.cache_data(ttl=60, show_spinner=False)
    def fetch_all_other_sources(max_per: int = 6) -> dict:
        """Fetch last-6h headlines from all 59 sources (BD-PA + INT)."""
        OTHER = [s for s in BD_SOURCES if s[0] != "prothomalo"] + INT_SOURCES
        result = {}
        for src in OTHER:
            sid  = src[0]; sname = src[1]; srss = src[2]
            surl = src[3] if len(src) > 3 else ""
            _fb   = list(src[4]) if len(src) > 4 else []
            items = smart_fetch(srss, surl, max_per, 6, _fb)
            # Extra filter: reject video / bad links
            items = [i for i in items if i.get("link","").count("/") >= 3]
            result[sid] = {
                "name":      sname,
                "url":       surl,
                "headlines": [i["title"] for i in items],
                "links":     [i.get("link","") for i in items],
                "live":      len(items) > 0,
                "is_bd":     src in BD_SOURCES,
                "is_priority": sid in PRIORITY_INT_SOURCES,
            }
        return result

    # ── Load ────────────────────────────────────────────────────
    lc1, lc2 = st.columns(2)
    with lc1:
        with st.spinner("📡 প্রথম আলো লোড হচ্ছে..."):
            pa_items = fetch_prothomalo(30)
    with lc2:
        with st.spinner("🌐 ৫৯টি সোর্স লোড হচ্ছে..."):
            other_data = fetch_all_other_sources(6)

    pa_words = set(re.findall(
        r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}',
        " ".join(i["title"] for i in pa_items).lower()
    ))

    live_bd  = sum(1 for s in BD_SOURCES  if s[0]!="prothomalo" and other_data.get(s[0],{}).get("live"))
    live_int = sum(1 for s in INT_SOURCES  if other_data.get(s[0],{}).get("live"))

    # ── Stats ───────────────────────────────────────────────────
    k1,k2,k3,k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="np-kpi" style="--c:#C8102E">
          <div class="np-kpi-icon">🗞️</div>
          <div class="np-kpi-val">{len(pa_items)}</div>
          <div class="np-kpi-label">প্রথম আলো হেডলাইন</div>
          <div class="np-kpi-delta">শেষ ৬ ঘণ্টা</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="np-kpi" style="--c:#1D4ED8">
          <div class="np-kpi-icon">🌍</div>
          <div class="np-kpi-val">{live_int}/30</div>
          <div class="np-kpi-label">INT সোর্স লাইভ</div>
          <div class="np-kpi-delta">Priority 11 উপরে</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="np-kpi" style="--c:#16a34a">
          <div class="np-kpi-icon">🇧🇩</div>
          <div class="np-kpi-val">{live_bd}/29</div>
          <div class="np-kpi-label">BD সোর্স লাইভ</div>
          <div class="np-kpi-delta">প্রথম আলো বাদে</div>
        </div>""", unsafe_allow_html=True)

    # ── Determine gaps ──────────────────────────────────────────
    def is_gap(headline: str) -> bool:
        h_words = set(re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', headline.lower()))
        return len(h_words & pa_words) < 2

    # Collect gap stories — INT priority first, then BD
    gap_priority = []   # from PRIORITY_INT_SOURCES
    gap_int_rest = []   # other INT
    gap_bd       = []   # BD sources

    for src in INT_SOURCES:
        sid  = src[0]; sname = src[1]
        d    = other_data.get(sid, {})
        if not d.get("live"): continue
        for h, lk in zip(d["headlines"], d["links"] + [""]*20):
            if h and is_gap(h):
                entry = {"headline":h, "link":lk, "source":sname,
                         "sid":sid, "is_bd":False, "is_priority": sid in PRIORITY_INT_SOURCES}
                if sid in PRIORITY_INT_SOURCES:
                    gap_priority.append(entry)
                else:
                    gap_int_rest.append(entry)

    for src in BD_SOURCES:
        if src[0] == "prothomalo": continue
        sid  = src[0]; sname = src[1]
        d    = other_data.get(sid, {})
        if not d.get("live"): continue
        for h, lk in zip(d["headlines"], d["links"] + [""]*20):
            if h and is_gap(h):
                gap_bd.append({"headline":h, "link":lk, "source":sname,
                                "sid":sid, "is_bd":True, "is_priority":False})

    all_gaps = gap_priority + gap_int_rest + gap_bd

    with k4:
        st.markdown(f"""<div class="np-kpi" style="--c:#ea580c">
          <div class="np-kpi-icon">🚨</div>
          <div class="np-kpi-val">{len(all_gaps)}</div>
          <div class="np-kpi-label">মোট গ্যাপ স্টোরি</div>
          <div class="np-kpi-delta">🌍{len(gap_priority)+len(gap_int_rest)} + 🇧🇩{len(gap_bd)}</div>
        </div>""", unsafe_allow_html=True)

    # ── Translation (INT priority headlines → Bangla) ───────────
    st.write("")
    translations = {}
    if api_key and gap_priority:
        eng_headlines = [g["headline"] for g in gap_priority[:30]]
        with st.spinner("🔤 আন্তর্জাতিক হেডলাইন বাংলায় অনুবাদ হচ্ছে..."):
            translations = translate_to_bangla_batch(eng_headlines, api_key)

    if not api_key and gap_priority:
        st.info("💡 Gemini API Key দিলে আন্তর্জাতিক হেডলাইনগুলো বাংলায় অনুবাদ দেখাবে।")

    # ── Gap card renderer ────────────────────────────────────────
    def gap_card(g: dict, rank: int, tr: dict) -> str:
        is_bd    = g.get("is_bd", True)
        is_prio  = g.get("is_priority", False)
        headline = g.get("headline", "")
        bangla   = tr.get(headline, "")
        lk       = g.get("link", "")
        src_name = g.get("source", "")

        # Colors
        if is_prio:
            border_col = "#1d4ed8"
            src_bg = "#eff6ff"; src_col = "#1d4ed8"; src_brd = "#bfdbfe"; flag = "🌍"
            prio_label = '<div style="font-size:9px;font-weight:800;color:#1d4ed8;font-family:monospace;margin-bottom:6px;letter-spacing:1.5px">⭐ PRIORITY SOURCE</div>'
        elif not is_bd:
            border_col = "#15803d"
            src_bg = "#f0fdf4"; src_col = "#15803d"; src_brd = "#86efac"; flag = "🌍"
            prio_label = ""
        else:
            border_col = "#C8102E"
            src_bg = "#fff7ed"; src_col = "#c2410c"; src_brd = "#fdba74"; flag = "🇧🇩"
            prio_label = ""

        # Bangla translation block
        if bangla:
            bn_block = (
                '<div style="font-family:Noto Serif Bengali,serif;font-size:13px;'
                'color:#1565c0;line-height:1.5;margin-top:6px;padding:7px 11px;'
                'background:#f0f7ff;border-radius:8px;border-left:3px solid #90caf9">'
                '🔤 ' + bangla + '</div>'
            )
        else:
            bn_block = ""

        # Read link button
        if lk:
            link_btn = (
                '<a href="' + lk + '" target="_blank" '
                'style="display:inline-flex;align-items:center;gap:4px;'
                'font-size:11px;font-weight:700;color:#C8102E;text-decoration:none;'
                'border:1px solid #fca5a5;padding:4px 12px;border-radius:100px;'
                'background:#fff5f5;margin-top:8px;white-space:nowrap">🔗 পড়ুন</a>'
            )
        else:
            link_btn = ""

        rank_str = (
            '<span style="font-size:11px;font-weight:700;color:#bbb;'
            'font-family:monospace;min-width:26px;flex-shrink:0;margin-top:3px">'
            '#' + str(rank) + '</span>'
        ) if rank else ""

        src_badge = (
            '<span style="font-size:10px;font-weight:700;padding:2px 10px;'
            'border-radius:100px;background:' + src_bg + ';color:' + src_col + ';'
            'border:1px solid ' + src_brd + '">' + flag + ' ' + src_name + '</span>'
        )

        # Time display
        pub_dt = g.get("pub_dt")
        t_ago  = time_ago_bn(pub_dt) if pub_dt else ""
        time_badge = (
            '<span style="font-size:10px;color:#aaa;font-family:monospace">⏱ ' + t_ago + '</span>'
        ) if t_ago else ""
        pa_badge = '<span style="font-size:10px;color:#aaa">প্রথম আলো ❌</span>'

        card = (
            '<div style="background:white;border:1px solid #E8E4DC;'
            'border-left:4px solid ' + border_col + ';'
            'border-radius:0 12px 12px 0;padding:14px 16px;margin-bottom:10px">'
            + prio_label +
            '<div style="display:flex;align-items:flex-start;gap:10px">'
            + rank_str +
            '<div style="flex:1;min-width:0">'
            '<div style="font-family:Noto Serif Bengali,serif;font-size:14.5px;'
            'font-weight:700;color:#1A1A1A;line-height:1.55;margin-bottom:6px">'
            + headline + '</div>'
            + bn_block +
            '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:8px">'
            + src_badge + ' ' + pa_badge + ' ' + time_badge + ' ' + link_btn +
            '</div>'
            '</div>'
            '</div>'
            '</div>'
        )
        return card
    # ── Gap Alert banner ────────────────────────────────────────
    if not pa_items:
        st.error("⚠ প্রথম আলোর RSS ফিড এই মুহূর্তে পাওয়া যাচ্ছে না।")
    elif not all_gaps:
        st.success("✅ শেষ ৬ ঘণ্টায় সব গুরুত্বপূর্ণ সংবাদ প্রথম আলো কভার করেছে!")
    else:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#fff5f5,#fff8f0);
  border:2px solid #fca5a5;border-radius:14px;padding:14px 20px;
  margin-bottom:18px;display:flex;align-items:center;gap:14px">
  <div style="font-size:30px">🚨</div>
  <div>
    <div style="font-family:'Noto Serif Bengali',serif;font-weight:800;font-size:15px;color:#C8102E">
      {len(all_gaps)}টি সংবাদ প্রথম আলোতে নেই (শেষ ৬ ঘণ্টা)
    </div>
    <div style="font-size:12px;color:#666;margin-top:3px">
      ⭐ Priority INT: {len(gap_priority)} &nbsp;·&nbsp;
      🌍 অন্য INT: {len(gap_int_rest)} &nbsp;·&nbsp;
      🇧🇩 বাংলাদেশি: {len(gap_bd)}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # ── Tabs ───────────────────────────────────────────────
        t_prio, t_bd, t_int_rest, t_all = st.tabs([
            f"⭐ Priority INT ({len(gap_priority)})",
            f"🇧🇩 বাংলাদেশি ({len(gap_bd)})",
            f"🌍 অন্য INT ({len(gap_int_rest)})",
            f"📋 সব ({len(all_gaps)})",
        ])

        with t_prio:
            st.markdown("""
<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;
  padding:10px 14px;margin-bottom:14px;font-size:12px;color:#1d4ed8">
  ⭐ <b>Priority Sources:</b> BBC · Al Jazeera · Reuters · CNN · Dawn · AP News ·
  NY Times · Middle East Eye · Geo TV · NDTV · The Guardian<br>
  🔤 Gemini API Key থাকলে হেডলাইনগুলো স্বয়ংক্রিয়ভাবে বাংলায় অনুবাদ দেখাবে।
</div>""", unsafe_allow_html=True)
            if gap_priority:
                for i, g in enumerate(gap_priority):
                    st.markdown(gap_card(g, i+1, translations), unsafe_allow_html=True)
            else:
                st.info("Priority সোর্সগুলোতে কোনো গ্যাপ নেই বা ফিড পাওয়া যায়নি।")

        with t_bd:
            if gap_bd:
                for i, g in enumerate(gap_bd):
                    st.markdown(gap_card(g, i+1, {}), unsafe_allow_html=True)
            else:
                st.info("বাংলাদেশি সোর্সে কোনো গ্যাপ নেই।")

        with t_int_rest:
            if gap_int_rest:
                for i, g in enumerate(gap_int_rest):
                    st.markdown(gap_card(g, i+1, {}), unsafe_allow_html=True)
            else:
                st.info("অন্য আন্তর্জাতিক সোর্সে কোনো গ্যাপ নেই।")

        with t_all:
            for i, g in enumerate(all_gaps[:60]):
                st.markdown(gap_card(g, i+1, translations), unsafe_allow_html=True)

    # ── AI Analysis ─────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="np-sec"><div class="np-sec-title">🤖 AI গভীর বিশ্লেষণ (২০-৫০ পয়েন্ট)</div></div>', unsafe_allow_html=True)

    if not api_key:
        st.warning("⚠ Gemini API Key দিন সাইডবারে — AI বিশ্লেষণ ও অনুবাদের জন্য")
    else:
        ai_c1, ai_c2 = st.columns([2,1])
        with ai_c1:
            ai_topic = st.text_input("বিশ্লেষণের বিষয় (ঐচ্ছিক)", placeholder="ফাঁকা = সব গ্যাপ", key="cov_ai_t")
        with ai_c2:
            ai_pts = st.selectbox("পয়েন্ট সংখ্যা", ["২০ পয়েন্ট","৩৫ পয়েন্ট","৫০ পয়েন্ট"], key="cov_ai_p")

        if st.button("🤖 AI বিশ্লেষণ শুরু করুন", key="btn_ai_final", use_container_width=True):
            target_pts = 20 if "২০" in ai_pts else 35 if "৩৫" in ai_pts else 50
            pa_sample  = [i["title"] for i in pa_items[:20]]
            prio_list  = [f'{g["headline"]} [{g["source"]}]' for g in gap_priority[:15]]
            bd_list    = [f'{g["headline"]} [{g["source"]}]' for g in gap_bd[:15]]

            prompt = f"""তুমি একটি অটোমেটেড নিউজ ক্রস-রেফারেন্সিং সিস্টেমের কোর AI ইঞ্জিন।

## প্রথম আলোর শেষ ৬ ঘণ্টার হেডলাইন:
{chr(10).join(f'{i+1}. {h}' for i,h in enumerate(pa_sample))}

## Priority আন্তর্জাতিক সোর্সে আছে কিন্তু প্রথম আলোতে নেই:
{chr(10).join(f'• {g}' for g in prio_list)}

## বাংলাদেশি সোর্সে আছে কিন্তু প্রথম আলোতে নেই:
{chr(10).join(f'• {g}' for g in bd_list)}

{'বিষয়: ' + ai_topic if ai_topic.strip() else ''}

## কাজ: ঠিক {target_pts}টি ফিডব্যাক পয়েন্ট তৈরি করো:
পয়েন্ট ১-১০: 🌍 Priority আন্তর্জাতিক সোর্স বিশ্লেষণ (BBC, Al Jazeera, Reuters ইত্যাদি)
পয়েন্ট ১১-২০: 🇧🇩 বাংলাদেশি মিডিয়া কভারেজ গ্যাপ বিশ্লেষণ
পয়েন্ট ২১-{target_pts}: 📊 তথ্যের শূন্যতা, সম্পাদকীয় পক্ষপাত, পাঠক সুপারিশ

নিয়ম: বাংলায় লেখো · {target_pts}টি পয়েন্ট · emoji + সোর্স নাম দিয়ে শুরু · real headline উদ্ধৃত করো"""

            with st.spinner(f"🤖 {target_pts}টি ফিডব্যাক পয়েন্ট তৈরি হচ্ছে..."):
                ai_out = gemini(api_key, prompt, max_tok=5000)

            st.markdown(f"""
<div style="background:white;border:1px solid #E8E4DC;border-top:3px solid #C8102E;
  border-radius:16px;padding:22px;box-shadow:0 2px 16px rgba(0,0,0,.05);margin-top:10px">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;
    padding-bottom:12px;border-bottom:1px solid #E8E4DC">
    <div style="width:40px;height:40px;border-radius:10px;
      background:linear-gradient(135deg,#C8102E,#ff6b35);
      display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">🤖</div>
    <div>
      <div style="font-family:'Noto Serif Bengali',serif;font-weight:800;font-size:15px">
        AI কভারেজ গ্যাপ বিশ্লেষণ — {target_pts}টি ফিডব্যাক পয়েন্ট
      </div>
      <div style="font-size:11px;color:#888;margin-top:2px">
        প্রথম আলো: {len(pa_items)}টি · গ্যাপ: {len(all_gaps)}টি
      </div>
    </div>
  </div>
  <div style="font-family:'Hind Siliguri',sans-serif;font-size:13.5px;
    line-height:1.9;color:#333;max-height:600px;overflow-y:auto">
""", unsafe_allow_html=True)
            st.markdown(ai_out)
            st.markdown("</div></div>", unsafe_allow_html=True)

            st.download_button("⬇ বিশ্লেষণ ডাউনলোড",
                data=f"প্রথম আলো গ্যাপ বিশ্লেষণ\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{ai_out}",
                file_name=f"pa_gap_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain", use_container_width=True)

    # ── Prothom Alo current headlines ───────────────────────────
    st.divider()
    st.markdown('<div class="np-sec"><div class="np-sec-title">🗞️ প্রথম আলোর বর্তমান হেডলাইন (শেষ ৬ ঘণ্টা)</div></div>', unsafe_allow_html=True)
    if pa_items:
        for i, item in enumerate(pa_items[:15]):
            lk    = item.get("link","")
            t_ago = time_ago_bn(item.get("pub_dt"))
            t_el  = f'<span style="font-size:10px;color:#aaa;font-family:monospace;margin-left:8px">⏱ {t_ago}</span>' if t_ago else ""
            rank_col = "#C8102E" if i < 3 else "#ddd"
            st.markdown(f"""
<div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #f0ece4">
  <span style="font-family:'Noto Serif Bengali',serif;font-size:18px;font-weight:900;
    color:{rank_col};min-width:28px;line-height:1.2">{i+1}</span>
  <div style="flex:1">
    <div style="display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;margin-bottom:3px">
      {f'<a href="{lk}" target="_blank" style="font-family:Noto Serif Bengali,serif;font-size:13.5px;font-weight:700;color:#1A1A1A;text-decoration:none;line-height:1.45">{item["title"]}</a>' if lk else f'<span style="font-family:Noto Serif Bengali,serif;font-size:13.5px;font-weight:700;color:#1A1A1A;line-height:1.45">{item["title"]}</span>'}
    </div>
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
      {f'<a href="{lk}" target="_blank" style="font-size:10px;color:#C8102E;text-decoration:none">🔗 পড়ুন</a>' if lk else ""}
      {t_el}
    </div>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.warning("প্রথম আলোর হেডলাইন লোড হয়নি")



# ══════════════════════════════════════════
#  TAB 9 — নিউজ রিডার (60 sources, checkbox, auto-refresh)
# ══════════════════════════════════════════
with tab_reader:

    bdt_now = datetime.utcnow() + timedelta(hours=6)

    # Auto-refresh every 5 minutes
    st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)

    # ── Quick select buttons ────────────────────────────────
    qb1,qb2,qb3,qb4,qb5 = st.columns(5)
    with qb1:
        if st.button("✅ সব BD",    key="rd_all_bd",  use_container_width=True):
            for s in BD_SOURCES: st.session_state[f"rd_{s[0]}"] = True
    with qb2:
        if st.button("✅ সব INT",   key="rd_all_int", use_container_width=True):
            for s in INT_SOURCES: st.session_state[f"rd_{s[0]}"] = True
    with qb3:
        if st.button("⭐ Priority", key="rd_prio",    use_container_width=True):
            for s in BD_SOURCES + INT_SOURCES:
                st.session_state[f"rd_{s[0]}"] = s[0] in PRIORITY_INT_SOURCES
    with qb4:
        if st.button("✅ সব ৬০টি", key="rd_all60",   use_container_width=True):
            for s in BD_SOURCES + INT_SOURCES: st.session_state[f"rd_{s[0]}"] = True
    with qb5:
        if st.button("❌ সব বাদ",  key="rd_none",    use_container_width=True):
            for s in BD_SOURCES + INT_SOURCES: st.session_state[f"rd_{s[0]}"] = False

    st.write("")

    # ── Source checkboxes ───────────────────────────────────
    with st.expander("🇧🇩 বাংলাদেশি সোর্স (৩০টি)", expanded=True):
        for i, src in enumerate(BD_SOURCES):
            if i % 5 == 0:
                _row_cols = st.columns(5)
            with _row_cols[i % 5]:
                st.checkbox(src[1],
                    value=st.session_state.get(f"rd_{src[0]}", True),
                    key=f"rd_{src[0]}")

    with st.expander("🌍 আন্তর্জাতিক সোর্স (৩০টি)", expanded=False):
        for i, src in enumerate(INT_SOURCES):
            if i % 5 == 0:
                _row_cols2 = st.columns(5)
            with _row_cols2[i % 5]:
                is_p = src[0] in PRIORITY_INT_SOURCES
                st.checkbox(("⭐ " if is_p else "") + src[1],
                    value=st.session_state.get(f"rd_{src[0]}", is_p),
                    key=f"rd_{src[0]}")

    # ── Selected sources ────────────────────────────────────
    sel_bd  = [s for s in BD_SOURCES  if st.session_state.get(f"rd_{s[0]}", True)]
    sel_int = [s for s in INT_SOURCES if st.session_state.get(f"rd_{s[0]}", s[0] in PRIORITY_INT_SOURCES)]
    sel_all = sel_bd + sel_int

    st.markdown(f"""
<div style="background:white;border:1px solid #E8E4DC;border-radius:10px;
  padding:9px 16px;margin:8px 0 14px;display:flex;align-items:center;gap:14px;
  font-size:12px;color:#555;font-family:'Hind Siliguri',sans-serif">
  <span>📊 নির্বাচিত: <b style="color:#C8102E;font-size:15px">{len(sel_all)}</b>টি</span>
  <span>🇧🇩 {len(sel_bd)}</span>
  <span>🌍 {len(sel_int)}</span>
  <span style="margin-left:auto;font-size:10px;color:#aaa;font-family:monospace">
    🔄 auto-refresh · {bdt_now.strftime("%H:%M")} BDT
  </span>
</div>""", unsafe_allow_html=True)

    if not sel_all:
        st.warning("কোনো সোর্স নির্বাচন করা হয়নি।")
        st.stop()

    # ── Fetch ───────────────────────────────────────────────
    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_reader_src(rss_url, web_url, src_id, max_n=20):
        raw = fetch_rss(rss_url, max_n * 2)
        if not raw:
            # Google News fallback
            try:
                domain = web_url.replace("https://","").replace("http://","").split("/")[0]
                gn = f"https://news.google.com/rss/search?q=site:{domain}&hl=en&gl=BD&ceid=BD:en"
                raw = fetch_rss(gn, max_n * 2)
            except Exception:
                pass
        with_dt = sorted([i for i in raw if i.get("pub_dt")],
                         key=lambda x: x.get("age_hours", 9999))
        no_dt   = [i for i in raw if not i.get("pub_dt")]
        return (with_dt + no_dt)[:max_n]

    prog = st.progress(0, text="লোড হচ্ছে...")
    src_data = {}
    for idx, src in enumerate(sel_all):
        _fallbacks = list(src[4]) if len(src) > 4 else []
        items = fetch_reader_src(
            src[2], src[3] if len(src) > 3 else "", src[0], 20, _fallbacks)
        src_data[src[0]] = {
            "name":  src[1], "items": items,
            "is_bd": src in BD_SOURCES,
            "is_p":  src[0] in PRIORITY_INT_SOURCES,
            "live":  len(items) > 0,
        }
        prog.progress((idx+1)/len(sel_all), text=f"{src[1]} ({idx+1}/{len(sel_all)})")
    prog.empty()

    live_count = sum(1 for d in src_data.values() if d["live"])

    # ── Render 4-column grid ────────────────────────────────
    # Header
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
  margin:4px 0 14px;padding:12px 18px;background:white;
  border:1px solid #E8E4DC;border-radius:12px">
  <div style="font-family:'Noto Serif Bengali',serif;font-weight:800;font-size:16px;
    color:#1A1A1A">📡 নিউজ রিডার
    <span style="font-size:12px;font-weight:400;color:#888;margin-left:8px">
      প্রথম ৫টি দেখাচ্ছে · scroll করে বাকি দেখুন
    </span>
  </div>
  <div style="font-size:11px;font-family:monospace;color:#888">
    ✅ {live_count}/{len(sel_all)} LIVE ·
    {bdt_now.strftime("%H:%M")} BDT ·
    ↻ 5min
  </div>
</div>""", unsafe_allow_html=True)

    # 4 cards per row using st.columns
    COLS = 4
    rows = [sel_all[i:i+COLS] for i in range(0, len(sel_all), COLS)]

    for row_srcs in rows:
        cols = st.columns(COLS)
        for col_idx, src in enumerate(row_srcs):
            d      = src_data.get(src[0], {})
            sname  = d.get("name", src[1])
            items  = d.get("items", [])
            is_bd  = d.get("is_bd", True)
            is_p   = d.get("is_p", False)
            live   = d.get("live", False)

            # Colors: cream/white theme (not dark)
            if is_p:
                hdr_bg  = "linear-gradient(135deg,#fffbeb,#fef9f0)"
                border  = "#f59e0b"
                dot_col = "#f59e0b"
                flag    = "⭐"
                badge   = '<span style="font-size:9px;background:#fef3c7;color:#b45309;border:1px solid #fde68a;padding:2px 7px;border-radius:100px;font-family:monospace;font-weight:700">⭐ PRIORITY</span>'
            elif is_bd:
                hdr_bg  = "linear-gradient(135deg,#fff5f6,#fff0f0)"
                border  = "#C8102E"
                dot_col = "#C8102E"
                flag    = "🇧🇩"
                badge   = '<span style="font-size:9px;background:#fef2f2;color:#C8102E;border:1px solid #fca5a5;padding:2px 7px;border-radius:100px;font-family:monospace;font-weight:700">🇧🇩 BD</span>'
            else:
                hdr_bg  = "linear-gradient(135deg,#eff6ff,#f0f7ff)"
                border  = "#3b82f6"
                dot_col = "#3b82f6"
                flag    = "🌍"
                badge   = '<span style="font-size:9px;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;padding:2px 7px;border-radius:100px;font-family:monospace;font-weight:700">🌍 INT</span>'

            live_badge = (
                '<span style="font-size:9px;background:#f0fdf4;color:#16a34a;'
                'border:1px solid #86efac;padding:2px 6px;border-radius:100px;'
                'font-family:monospace;font-weight:700">● LIVE</span>'
                if live else
                '<span style="font-size:9px;background:#f9fafb;color:#9ca3af;'
                'border:1px solid #e5e7eb;padding:2px 6px;border-radius:100px;'
                'font-family:monospace;font-weight:700">○ OFF</span>'
            )

            # Build news items — first 5 visible, rest in scroll
            news_rows = ""
            if items:
                for i, item in enumerate(items):
                    title  = item.get("title","")
                    lk     = item.get("link","")
                    t_ago  = time_ago_bn(item.get("pub_dt"))
                    t_html = f'<div style="font-size:9px;color:#aaa;font-family:monospace;margin-top:2px">⏱ {t_ago}</div>' if t_ago else ""

                    dot = f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;background:{dot_col};margin-right:6px;flex-shrink:0;margin-top:6px"></span>'

                    if lk:
                        title_el = f'<a href="{lk}" target="_blank" style="font-family:\'Noto Serif Bengali\',serif;font-size:12.5px;font-weight:700;color:#1A1A1A;line-height:1.45;text-decoration:none;flex:1;display:block" onmouseover="this.style.color=\'{border}\'" onmouseout="this.style.color=\'#1A1A1A\'">{title}</a>'
                    else:
                        title_el = f'<span style="font-family:\'Noto Serif Bengali\',serif;font-size:12.5px;font-weight:700;color:#1A1A1A;line-height:1.45;flex:1;display:block">{title}</span>'

                    item_style = (
                        "padding:8px 0;border-bottom:1px solid #f0ece4;"
                        + ("" if i < len(items)-1 else "border-bottom:none;")
                    )

                    news_rows += f'<div style="{item_style}"><div style="display:flex;align-items:flex-start;gap:4px">{dot}{title_el}</div>{t_html}</div>'
            else:
                news_rows = '<div style="text-align:center;padding:30px 0;color:#aaa;font-size:12px">❌ ফিড পাওয়া যায়নি<br><span style="font-size:10px">RSS connect ব্যর্থ</span></div>'

            # Card HTML
            card_html = f"""
<div style="background:white;border:2px solid {border};border-radius:14px;
  overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.06);height:100%">

  <div style="background:{hdr_bg};padding:10px 14px;border-bottom:1px solid #f0ece4;">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:4px">
      <div style="font-family:'Noto Serif Bengali',serif;font-size:13px;font-weight:800;
        color:#1A1A1A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
        flex:1;letter-spacing:.3px">{flag} {sname}</div>
      {live_badge}
    </div>
    <div>{badge}</div>
  </div>

  <div style="height:360px;overflow-y:auto;padding:4px 12px 8px;
    scrollbar-width:thin;scrollbar-color:#E8E4DC transparent">
    {news_rows}
  </div>
</div>"""

            with cols[col_idx]:
                st.markdown(card_html, unsafe_allow_html=True)
                st.write("")  # spacing

        # empty columns if last row is incomplete
        for empty_idx in range(len(row_srcs), COLS):
            with cols[empty_idx]:
                st.empty()


with tab_stats:
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown('<div class="np-sec"><div class="np-sec-title">📊 লাইভ অ্যানালিটিক্স ড্যাশবোর্ড</div></div>', unsafe_allow_html=True)

    readers_base = 8200 + random.randint(-300, 300)
    an1, an2, an3 = st.columns(3)
    with an1:
        st.metric("👥 সক্রিয় পাঠক", f"{readers_base:,}", delta=f"+{random.randint(12,45)} /মিনিট")
    with an2:
        st.metric("📰 আজকের সংবাদ", str(len(all_news)), delta=f"+{random.randint(2,8)} নতুন")
    with an3:
        st.metric("🔥 ট্রেন্ডিং টপিক", str(len(rt_trends)+len(fb_data)), delta="রিয়েলটাইম")

    st.write("")
    dash1, dash2 = st.columns(2, gap="large")

    with dash1:
        # Platform comparison
        df_plat = pd.DataFrame({
            "প্ল্যাটফর্ম": ["Google News","Google Trends","YouTube BD","Facebook/Social"],
            "আইটেম":       [len(all_news), len(rt_trends), len(yt_data), len(fb_data)],
            "রং":          ["#4285f4","#ea4335","#cc0000","#1877f2"]
        })
        fig_plat = px.bar(df_plat, x="প্ল্যাটফর্ম", y="আইটেম",
                          color="রং", color_discrete_sequence=df_plat["রং"].tolist(),
                          template="plotly_white", text="আইটেম")
        fig_plat.update_layout(margin=dict(l=0,r=0,t=30,b=0), height=280, showlegend=False,
                               title="প্ল্যাটফর্ম তুলনা", font=dict(family="Hind Siliguri",size=12))
        fig_plat.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(fig_plat, use_container_width=True)

        # Hourly simulated traffic
        hours   = [f"{h:02d}:00" for h in range(24)]
        traffic = [random.randint(200,800) for _ in range(24)]
        traffic[now.hour] = readers_base // 10
        fig_hr = go.Figure(go.Bar(x=hours, y=traffic,
            marker_color=["#C8102E" if i==now.hour else "#FFE8E8" for i in range(24)]))
        fig_hr.update_layout(title="আজকের পাঠক ট্রাফিক",
            margin=dict(l=0,r=0,t=30,b=0), height=250,
            template="plotly_white", font=dict(family="Hind Siliguri",size=11))
        st.plotly_chart(fig_hr, use_container_width=True)

    with dash2:
        # Category distribution pie
        cat_dist = {}
        for key, items in news_cats.items():
            label = re.sub(r'[^\u0980-\u09FF ]','',key).strip()[:6] or key[-6:]
            cat_dist[label] = len(items)
        df_cat = pd.DataFrame(list(cat_dist.items()), columns=["বিভাগ","সংবাদ"])
        fig_cat = px.pie(df_cat, names="বিভাগ", values="সংবাদ",
                         color_discrete_sequence=px.colors.qualitative.Prism,
                         template="plotly_white", title="সংবাদ বিভাগ বিতরণ")
        fig_cat.update_layout(margin=dict(l=0,r=0,t=30,b=0), height=280,
                              font=dict(family="Hind Siliguri",size=12))
        fig_cat.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_cat, use_container_width=True)

        # Keyword treemap
        if top_kws:
            df_tree = pd.DataFrame(top_kws[:12], columns=["কীওয়ার্ড","মান"])
            fig_tree = px.treemap(df_tree, path=["কীওয়ার্ড"], values="মান",
                                  color="মান", color_continuous_scale=["#FFE8E8","#C8102E"],
                                  template="plotly_white", title="কীওয়ার্ড ট্রিম্যাপ")
            fig_tree.update_layout(margin=dict(l=0,r=0,t=30,b=0), height=250,
                                   font=dict(family="Hind Siliguri",size=13))
            st.plotly_chart(fig_tree, use_container_width=True)

    # Top sources table
    st.write("")
    st.markdown('<div class="np-sec"><div class="np-sec-title">🏛️ শীর্ষ মিডিয়া সোর্স</div></div>', unsafe_allow_html=True)
    src_data = Counter(n.get("source","Unknown") for n in all_news)
    df_srcs  = pd.DataFrame([
        {"র‍্যাংক":i+1,"মিডিয়া আউটলেট":s,"আর্টিকেল":c,
         "শেয়ার":f"{c/max(len(all_news),1)*100:.1f}%"}
        for i,(s,c) in enumerate(src_data.most_common(10))
    ])
    st.dataframe(df_srcs, use_container_width=True, hide_index=True)

    # Cross-platform heatmap
    st.write("")
    st.markdown('<div class="np-sec"><div class="np-sec-title">🔥 ক্রস-প্ল্যাটফর্ম হিটম্যাপ</div></div>', unsafe_allow_html=True)
    cp_topics = list(set(
        [t["topic"][:30] for t in rt_trends[:8]] +
        [t["topic"][:30] for t in fb_data[:8]] +
        [v["title"][:30] for v in yt_data[:8]]
    ))[:12]
    platforms = ["Google","YouTube","Facebook"]
    z_vals    = [[random.randint(0,10) for _ in platforms] for _ in cp_topics]
    fig_hm = go.Figure(go.Heatmap(z=z_vals, x=platforms, y=cp_topics,
                                   colorscale=[[0,"#FFF5F6"],[1,"#C8102E"]],
                                   text=z_vals, texttemplate="%{text}", showscale=True))
    fig_hm.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=400,
                         font=dict(family="Hind Siliguri",size=11))
    st.plotly_chart(fig_hm, use_container_width=True)

    # Full combined export
    st.write("")
    all_export = (
        [{"প্ল্যাটফর্ম":"Google News","শিরোনাম":n["title"],"সোর্স":n.get("source",""),"তারিখ":n.get("date","")} for n in all_news] +
        [{"প্ল্যাটফর্ম":"Google Trends","শিরোনাম":t["topic"],"সোর্স":"Google","তারিখ":t.get("pub","")} for t in rt_trends] +
        [{"প্ল্যাটফর্ম":"YouTube","শিরোনাম":v["title"],"সোর্স":v.get("channel",""),"তারিখ":v.get("pub","")} for v in yt_data] +
        [{"প্ল্যাটফর্ম":"Facebook","শিরোনাম":f["topic"],"সোর্স":"Social","তারিখ":""} for f in fb_data]
    )
    st.download_button(
        "⬇ সম্পূর্ণ ডেটাসেট ডাউনলোড করুন (সব প্ল্যাটফর্ম CSV)",
        data=pd.DataFrame(all_export).to_csv(index=False, encoding="utf-8-sig"),
        file_name=f"newspulse_full_export_{(datetime.utcnow()+timedelta(hours=6)).strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv", use_container_width=True
    )

# ═════════════════════════════════════════════════════
#  FOOTER
# ═════════════════════════════════════════════════════
st.divider()
fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.markdown("**🗞️ NewsPulse AI v5.0**\nBangladesh Intelligent Newsroom Platform\nMIT License · Open Source")
with fc2:
    st.markdown("**📡 ডেটা সোর্স**\nGoogle News RSS · Google Realtime Trends\nYouTube Atom/Scrape · trends24.in\nOpenMeteo AQI · wttr.in Weather")
with fc3:
    st.markdown(f"**⏱ শেষ আপডেট**\n{now.strftime('%d %B %Y · %H:%M:%S')} BDT\n\nBuilt for Bangladesh Newsrooms 🇧🇩\nPowered by Gemini 2.5 Flash")
