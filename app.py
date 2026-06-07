"""
╔══════════════════════════════════════════════════════════════════════╗
║  NewsIQ Pro — Bangladesh AI Newsroom Intelligence Platform  v3.0    ║
║  Powered by Google News RSS + Gemini 2.5 Flash                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import time
import re
from datetime import datetime
from collections import Counter
import google.generativeai as genai
from pytrends.request import TrendReq

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="NewsIQ Pro · Bangladesh",
    layout="wide",
    page_icon="◈",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
#  ULTRA-PREMIUM CSS — Cinematic Command Center Aesthetic
# ══════════════════════════════════════════════════════
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── VARIABLES ── */
:root {
  --ink:        #05080F;
  --ink2:       #0A0F1E;
  --ink3:       #111827;
  --ink4:       #1C2537;
  --wire:       rgba(255,255,255,0.06);
  --wire2:      rgba(255,255,255,0.12);
  --wire3:      rgba(255,255,255,0.20);
  --signal:     #FF3B3B;
  --signal2:    #FF6B35;
  --ice:        #00D4FF;
  --lime:       #39FF14;
  --gold:       #FFD700;
  --paper:      #EEF2FF;
  --mist:       #8892A4;
  --ghost:      #3D4A5C;
  --display:    'Bebas Neue', sans-serif;
  --body:       'Outfit', sans-serif;
  --bengali:    'Noto Sans Bengali', sans-serif;
  --code:       'JetBrains Mono', monospace;
}

/* ── GLOBAL ── */
*, *::before, *::after { box-sizing: border-box; }
.stApp, .main, [data-testid="stAppViewContainer"] {
  background: var(--ink) !important;
  color: var(--paper) !important;
}
[data-testid="stSidebar"] {
  background: var(--ink2) !important;
  border-right: 1px solid var(--wire2) !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; display:none !important; }

/* ── NOISE OVERLAY ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
  opacity: 0.4;
}

/* ── MASTHEAD ── */
.masthead {
  position: relative;
  padding: 32px 0 24px;
  margin-bottom: 0;
  border-bottom: 1px solid var(--wire2);
  overflow: hidden;
}
.masthead::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 280px; height: 2px;
  background: linear-gradient(90deg, var(--signal), transparent);
}
.wordmark {
  font-family: var(--display);
  font-size: 52px;
  letter-spacing: 4px;
  line-height: 1;
  background: linear-gradient(135deg, #ffffff 0%, #8892A4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.wordmark span {
  background: linear-gradient(135deg, var(--signal) 0%, var(--signal2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.tagline {
  font-family: var(--code);
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--mist);
  margin-top: 6px;
}
.masthead-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}
.live-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(255,59,59,0.12);
  border: 1px solid rgba(255,59,59,0.35);
  border-radius: 100px;
  padding: 5px 14px 5px 10px;
  font-family: var(--code);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: var(--signal);
  text-transform: uppercase;
}
.live-dot {
  width: 7px; height: 7px;
  background: var(--signal);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--signal);
  animation: throb 1.2s ease-in-out infinite;
}
@keyframes throb {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.65); opacity: 0.4; }
}
.clock-display {
  font-family: var(--code);
  font-size: 13px;
  font-weight: 700;
  color: var(--ice);
  letter-spacing: 1px;
}

/* ── TICKER ── */
.ticker-outer {
  background: linear-gradient(90deg, var(--signal) 0%, #CC1A1A 100%);
  height: 36px;
  display: flex;
  align-items: center;
  overflow: hidden;
  margin-bottom: 28px;
  position: relative;
}
.ticker-flag {
  background: rgba(0,0,0,0.3);
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 18px;
  font-family: var(--display);
  font-size: 14px;
  letter-spacing: 3px;
  color: #fff;
  white-space: nowrap;
  flex-shrink: 0;
  border-right: 1px solid rgba(255,255,255,0.2);
  gap: 8px;
}
.ticker-track {
  display: flex;
  align-items: center;
  gap: 0;
  overflow: hidden;
  flex: 1;
}
.ticker-animate {
  display: inline-flex;
  align-items: center;
  gap: 0;
  white-space: nowrap;
  animation: crawl 60s linear infinite;
  font-family: var(--bengali);
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  padding-left: 32px;
}
@keyframes crawl {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.ticker-sep {
  display: inline-block;
  margin: 0 24px;
  color: rgba(255,255,255,0.5);
  font-size: 10px;
}

/* ── KPI STRIP ── */
.kpi-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}
.kpi-block {
  background: var(--ink3);
  border: 1px solid var(--wire);
  border-radius: 12px;
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
  cursor: default;
}
.kpi-block:hover {
  border-color: var(--wire3);
  transform: translateY(-2px);
}
.kpi-block::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.kpi-block.s { --c: var(--signal); }
.kpi-block.b { --c: var(--ice); }
.kpi-block.g { --c: var(--lime); }
.kpi-block.o { --c: var(--signal2); }
.kpi-block.y { --c: var(--gold); }
.kpi-block::before { background: var(--c); box-shadow: 0 0 12px var(--c); }

.kpi-label {
  font-family: var(--code);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--c);
  margin-bottom: 8px;
}
.kpi-val {
  font-family: var(--display);
  font-size: 36px;
  line-height: 1;
  color: #fff;
  letter-spacing: 1px;
}
.kpi-sub {
  font-family: var(--code);
  font-size: 10px;
  color: var(--ghost);
  margin-top: 4px;
}
.kpi-icon {
  position: absolute;
  bottom: 10px; right: 14px;
  font-size: 26px;
  opacity: 0.08;
}

/* ── SECTION LABEL ── */
.sec-label {
  font-family: var(--code);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--ghost);
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}
.sec-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--wire);
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 0 !important;
  border-bottom: 1px solid var(--wire2) !important;
  padding: 0 !important;
}
[data-baseweb="tab"] {
  background: transparent !important;
  color: var(--ghost) !important;
  font-family: var(--code) !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  padding: 10px 18px !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  transition: all 0.2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  color: #fff !important;
  border-bottom-color: var(--ice) !important;
  background: rgba(0,212,255,0.04) !important;
}

/* ── DATA TABLE ── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--wire) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
  background: var(--ink2) !important;
  color: var(--ghost) !important;
  font-family: var(--code) !important;
  font-size: 10px !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid var(--wire2) !important;
  padding: 10px 14px !important;
}
[data-testid="stDataFrame"] td {
  color: var(--paper) !important;
  font-family: var(--bengali) !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
  border-bottom: 1px solid var(--wire) !important;
  padding: 10px 14px !important;
}
[data-testid="stDataFrame"] tr:hover td { background: rgba(0,212,255,0.03) !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
  background: var(--ink3) !important;
  border: 1px solid var(--wire2) !important;
  border-radius: 8px !important;
  color: var(--paper) !important;
  font-family: var(--bengali) !important;
}
[data-baseweb="select"] > div:focus-within {
  border-color: var(--ice) !important;
  box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
[data-baseweb="popover"] {
  background: var(--ink4) !important;
  border: 1px solid var(--wire2) !important;
  border-radius: 8px !important;
}
[role="option"] { color: var(--paper) !important; font-family: var(--bengali) !important; }
[role="option"]:hover { background: rgba(0,212,255,0.08) !important; }

/* ── BUTTONS ── */
[data-testid="stButton"] button {
  background: linear-gradient(135deg, var(--signal) 0%, var(--signal2) 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: var(--display) !important;
  font-size: 15px !important;
  letter-spacing: 3px !important;
  text-transform: uppercase !important;
  padding: 14px 28px !important;
  width: 100% !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 24px rgba(255,59,59,0.3) !important;
}
[data-testid="stButton"] button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(255,59,59,0.5) !important;
}

/* ── RADIO ── */
[data-testid="stRadio"] label {
  font-family: var(--code) !important;
  font-size: 11px !important;
  color: var(--mist) !important;
}
[data-testid="stRadio"] [data-baseweb="radio"] div {
  border-color: var(--ghost) !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--ice) !important;
  border-color: var(--ice) !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
  font-family: var(--code) !important;
  font-size: 11px !important;
  color: var(--mist) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: var(--display) !important;
  font-size: 16px !important;
  letter-spacing: 3px !important;
  color: var(--paper) !important;
}
[data-testid="stSidebar"] input {
  background: var(--ink3) !important;
  border: 1px solid var(--wire2) !important;
  border-radius: 6px !important;
  color: var(--paper) !important;
  font-family: var(--code) !important;
  font-size: 12px !important;
}
[data-testid="stSidebar"] input:focus {
  border-color: var(--ice) !important;
  box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}

/* ── AI OUTPUT ── */
.ai-frame {
  background: var(--ink3);
  border: 1px solid var(--wire2);
  border-top: 2px solid var(--ice);
  border-radius: 10px;
  overflow: hidden;
  margin-top: 16px;
}
.ai-header {
  background: rgba(0,212,255,0.06);
  border-bottom: 1px solid var(--wire2);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--code);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--ice);
}
.ai-body {
  padding: 22px 24px;
  font-family: var(--bengali);
  font-size: 14px;
  line-height: 2;
  color: var(--paper);
}
.ai-body h3 {
  font-family: var(--code) !important;
  font-size: 11px !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  color: var(--ice) !important;
  margin: 22px 0 10px !important;
  padding-bottom: 6px !important;
  border-bottom: 1px solid var(--wire) !important;
}

/* ── TOPIC CARD ── */
.topic-card {
  background: var(--ink3);
  border: 1px solid var(--wire);
  border-left: 3px solid var(--ice);
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 10px;
  font-family: var(--bengali);
  font-size: 13px;
  color: var(--paper);
  line-height: 1.5;
  transition: all 0.2s;
  cursor: pointer;
}
.topic-card:hover {
  border-left-color: var(--signal);
  background: var(--ink4);
}
.topic-rank {
  font-family: var(--code);
  font-size: 10px;
  font-weight: 700;
  color: var(--ghost);
  margin-bottom: 4px;
  letter-spacing: 1px;
}

/* ── FEED STATUS INDICATORS ── */
.feed-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px solid var(--wire);
  font-family: var(--code);
  font-size: 10px;
  color: var(--mist);
  letter-spacing: 0.5px;
}
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot.live  { background: var(--lime);  box-shadow: 0 0 8px var(--lime); }
.dot.cache { background: var(--gold);  box-shadow: 0 0 8px var(--gold); }
.dot.off   { background: var(--ghost); }
.feed-label { flex: 1; }
.feed-count {
  font-weight: 700;
  color: var(--paper);
}

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
  background: var(--ink4) !important;
  border: 1px solid var(--wire2) !important;
  color: var(--ice) !important;
  font-family: var(--code) !important;
  font-size: 11px !important;
  letter-spacing: 2px !important;
  padding: 10px !important;
  box-shadow: none !important;
}
[data-testid="stDownloadButton"] button:hover {
  border-color: var(--ice) !important;
  box-shadow: 0 0 12px rgba(0,212,255,0.2) !important;
  transform: none !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
  background: rgba(255,59,59,0.08) !important;
  border: 1px solid rgba(255,59,59,0.25) !important;
  border-radius: 8px !important;
  font-family: var(--code) !important;
  font-size: 11px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--ghost); border-radius: 4px; }

/* ── TREND HEAT BADGE ── */
.heat {
  display: inline-block;
  font-family: var(--code);
  font-size: 9px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-right: 8px;
}
.heat.h { background: rgba(255,59,59,0.2);  color: var(--signal); }
.heat.m { background: rgba(255,215,0,0.15); color: var(--gold); }
.heat.l { background: rgba(57,255,20,0.12); color: var(--lime); }

/* ── CATEGORY PILL ── */
.cat-pill {
  display: inline-block;
  background: rgba(0,212,255,0.1);
  border: 1px solid rgba(0,212,255,0.2);
  color: var(--ice);
  font-family: var(--code);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1.5px;
  padding: 3px 9px;
  border-radius: 100px;
  text-transform: uppercase;
  margin-right: 6px;
  margin-bottom: 4px;
}

/* ── PROGRESS BAR OVERRIDE ── */
[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, var(--ice), var(--signal)) !important;
}

/* ── METRIC ── */
[data-testid="stMetricValue"] {
  font-family: var(--display) !important;
  font-size: 28px !important;
  color: var(--paper) !important;
}
[data-testid="stMetricLabel"] {
  font-family: var(--code) !important;
  font-size: 10px !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  color: var(--ghost) !important;
}
[data-testid="stMetricDelta"] {
  font-family: var(--code) !important;
  font-size: 11px !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SIDEBAR — Control Panel
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ◈ NEWSIQ PRO")
    st.markdown("---")

    api_key = st.text_input(
        "GEMINI API KEY",
        type="password",
        placeholder="AIza••••••••••••••••••",
        help="aistudio.google.com থেকে বিনামূল্যে নিন"
    )
    if api_key:
        genai.configure(api_key=api_key)

    st.markdown("---")
    st.markdown("### ⚙ CONTENT ENGINE")

    content_mode = st.radio("OUTPUT MODE", [
        "🗞 Full Editorial Kit",
        "📱 Social Media Blitz",
        "🎙 Video Script Pack",
        "📊 SEO Intelligence Brief",
        "🔎 Investigative Angle Finder",
    ])

    tone_mode = st.selectbox("JOURNALIST TONE", [
        "এলিট সাংবাদিক — প্রথম আলো স্টাইল",
        "ব্রেকিং — আর্জেন্ট ও পাঞ্চি",
        "ভাইরাল — সোশ্যাল মিডিয়া মাস্টার",
        "গভীর বিশ্লেষণ — একাডেমিক",
        "ফিচার রাইটিং — ম্যাগাজিন স্টাইল",
    ])

    target_audience = st.selectbox("TARGET AUDIENCE", [
        "সাধারণ পাঠক", "শিক্ষিত মধ্যবিত্ত",
        "তরুণ ও ছাত্র", "ব্যবসায়িক পাঠক", "রাজনীতি সচেতন"
    ])

    word_limit = st.slider("WORD TARGET", 300, 1500, 700, 50)

    st.markdown("---")
    st.markdown("### 📡 FEED STATUS")

    now_str = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="feed-row"><span class="dot live"></span><span class="feed-label">Google News BD</span><span class="feed-count">LIVE</span></div>
    <div class="feed-row"><span class="dot live"></span><span class="feed-label">Google Trends Daily</span><span class="feed-count">LIVE</span></div>
    <div class="feed-row"><span class="dot live"></span><span class="feed-label">Google Realtime RSS</span><span class="feed-count">LIVE</span></div>
    <div class="feed-row"><span class="dot cache"></span><span class="feed-label">YouTube BD Trends</span><span class="feed-count">2m CACHE</span></div>
    <br><div style="font-family:var(--code);font-size:9px;color:var(--ghost);letter-spacing:1px;">SYNC: {now_str} BDT</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("NewsIQ Pro v3.0 · MIT License · BD Newsrooms")


# ══════════════════════════════════════════════════════
#  DATA FETCHING — Google News as PRIMARY source
# ══════════════════════════════════════════════════════

@st.cache_data(ttl=90, show_spinner=False)
def fetch_google_news_bd(topic: str = "বাংলাদেশ", max_items: int = 25) -> list[dict]:
    """
    Fetch from Google News RSS — the ONLY news source.
    Returns list of {title, link, pubDate, source} dicts.
    """
    encoded = urllib.parse.quote(topic) if hasattr(urllib, 'parse') else topic.replace(" ", "+")
    urls = [
        f"https://news.google.com/rss/search?q={encoded}&hl=bn&gl=BD&ceid=BD:bn",
        f"https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFZxYUdjU0FtSm5LQUFQAzoo?hl=bn&gl=BD&ceid=BD:bn",
        "https://news.google.com/rss?hl=bn&gl=BD&ceid=BD:bn",
    ]
    items = []
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item")[:max_items]:
                    title_el   = item.find("title")
                    link_el    = item.find("link")
                    date_el    = item.find("pubDate")
                    source_el  = item.find("source")
                    if title_el is not None and title_el.text:
                        # Clean Google News title (remove source suffix)
                        raw_title = title_el.text.strip()
                        # "Title - Source Name" → keep full
                        items.append({
                            "title":   raw_title,
                            "link":    link_el.text.strip() if link_el is not None and link_el.text else "",
                            "date":    date_el.text.strip() if date_el is not None and date_el.text else "",
                            "source":  source_el.text.strip() if source_el is not None and source_el.text else "Google News",
                        })
            if items:
                break
        except Exception:
            continue
    return items[:max_items]


@st.cache_data(ttl=90, show_spinner=False)
def fetch_google_news_by_category() -> dict[str, list[dict]]:
    """Fetch Google News for multiple BD-relevant categories."""
    import urllib.parse
    categories = {
        "🔴 টপ হেডলাইন":     "বাংলাদেশ",
        "⚡ রাজনীতি":         "বাংলাদেশ রাজনীতি",
        "💰 অর্থনীতি":        "বাংলাদেশ অর্থনীতি বাজার",
        "🏏 খেলাধুলা":        "বাংলাদেশ ক্রিকেট ফুটবল",
        "💻 প্রযুক্তি":       "বাংলাদেশ প্রযুক্তি",
    }
    result = {}
    for label, query in categories.items():
        result[label] = fetch_google_news_bd(topic=query, max_items=15)
    return result


@st.cache_data(ttl=120, show_spinner=False)
def fetch_google_trends_daily() -> list[str]:
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        df = pytrends.trending_searches(pn='bangladesh')
        return df[0].tolist()[:20]
    except Exception:
        return ["বাংলাদেশ রাজনীতি", "ক্রিকেট আপডেট", "মূল্যস্ফীতি", "ঢাকার আবহাওয়া"]


@st.cache_data(ttl=90, show_spinner=False)
def fetch_google_realtime_trends() -> list[str]:
    try:
        req = urllib.request.Request(
            "https://trends.google.com/trending/rss?geo=BD",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            topics = []
            for item in root.findall(".//item")[:20]:
                t = item.find("title")
                if t is not None and t.text:
                    topics.append(t.text.strip())
            return topics
    except Exception:
        return ["ভাইরাল ট্রেন্ড লোড হয়নি — রিফ্রেশ করুন"]


@st.cache_data(ttl=180, show_spinner=False)
def fetch_youtube_trends() -> list[str]:
    try:
        url = "https://www.youtube.com/feeds/videos.xml?chart=mostpopular&regionCode=BD&hl=bn"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            titles = []
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:15]:
                t = entry.find("{http://www.w3.org/2005/Atom}title")
                if t is not None and t.text:
                    titles.append(t.text.strip())
            return titles
    except Exception:
        return [
            "বাংলা ভাইরাল ভিডিও", "নতুন নাটক রিভিউ",
            "ক্রিকেট হাইলাইটস", "টকশো লাইভ", "ইসলামিক লেকচার"
        ]


def extract_keywords(texts: list[str], top_n: int = 12) -> list[tuple[str, int]]:
    """Extract trending keywords from news titles."""
    stop = {"এবং", "বা", "যে", "কি", "এই", "সে", "তার", "আর", "না", "হয়", "করে",
            "the", "a", "an", "in", "of", "to", "is", "for", "on", "at", "by", "with"}
    words = []
    for text in texts:
        for w in re.findall(r'[\u0980-\u09FF]{3,}|[a-zA-Z]{4,}', text):
            if w.lower() not in stop:
                words.append(w)
    return Counter(words).most_common(top_n)


# ══════════════════════════════════════════════════════
#  LOAD ALL DATA
# ══════════════════════════════════════════════════════
with st.spinner("◈ NewsIQ নেটওয়ার্ক সিঙ্ক হচ্ছে..."):
    news_by_cat   = fetch_google_news_by_category()
    trends_daily  = fetch_google_trends_daily()
    trends_rt     = fetch_google_realtime_trends()
    youtube_data  = fetch_youtube_trends()

# Flatten all Google News titles
all_news_items  = [item for cat in news_by_cat.values() for item in cat]
all_news_titles = [item["title"] for item in all_news_items]
all_topics      = list(dict.fromkeys(all_news_titles + trends_daily + trends_rt))
top_keywords    = extract_keywords(all_news_titles, top_n=10)


# ══════════════════════════════════════════════════════
#  MASTHEAD
# ══════════════════════════════════════════════════════
now_display = datetime.now().strftime("%A, %d %B %Y  ·  %H:%M BDT")

col_m1, col_m2 = st.columns([2, 1])
with col_m1:
    st.markdown(f"""
    <div class="masthead">
      <div class="wordmark">News<span>IQ</span> Pro</div>
      <div class="tagline">Bangladesh AI Newsroom Intelligence Platform · {now_display}</div>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
    <div style="text-align:right; padding-top:32px;">
      <div class="live-pill"><span class="live-dot"></span>ALL FEEDS LIVE</div>
      <div class="clock-display" style="margin-top:10px;">{datetime.now().strftime("%H:%M:%S")}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  BREAKING NEWS TICKER — Slow readable speed
# ══════════════════════════════════════════════════════
ticker_headlines = all_news_titles[:12]
ticker_text = "  ◆  ".join(ticker_headlines)
# Duplicate for seamless loop
ticker_full = ticker_text + "  ◆  " + ticker_text

st.markdown(f"""
<div class="ticker-outer">
  <div class="ticker-flag">⚡ BREAKING</div>
  <div class="ticker-track">
    <div class="ticker-animate">{ticker_full}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  KPI STRIP — 5 cards
# ══════════════════════════════════════════════════════
total_news = len(all_news_items)
unique_src  = len(set(i.get("source","") for i in all_news_items))

st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-block s">
    <div class="kpi-icon">📰</div>
    <div class="kpi-label">Google News</div>
    <div class="kpi-val">{total_news}</div>
    <div class="kpi-sub">Live Articles</div>
  </div>
  <div class="kpi-block b">
    <div class="kpi-icon">📡</div>
    <div class="kpi-label">Realtime Trends</div>
    <div class="kpi-val">{len(trends_rt)}</div>
    <div class="kpi-sub">Viral Topics</div>
  </div>
  <div class="kpi-block g">
    <div class="kpi-icon">🔍</div>
    <div class="kpi-label">Daily Searches</div>
    <div class="kpi-val">{len(trends_daily)}</div>
    <div class="kpi-sub">Search Trends</div>
  </div>
  <div class="kpi-block o">
    <div class="kpi-icon">🎬</div>
    <div class="kpi-label">YouTube BD</div>
    <div class="kpi-val">{len(youtube_data)}</div>
    <div class="kpi-sub">Trending Videos</div>
  </div>
  <div class="kpi-block y">
    <div class="kpi-icon">🏷️</div>
    <div class="kpi-label">News Sources</div>
    <div class="kpi-val">{unique_src}</div>
    <div class="kpi-sub">Media Outlets</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  MAIN LAYOUT
# ══════════════════════════════════════════════════════
left_col, right_col = st.columns([1.1, 1.3], gap="large")


# ─── LEFT PANEL ─────────────────────────────────────
with left_col:

    # ── Tab 1: Google News by Category
    st.markdown('<div class="sec-label">◈ GOOGLE NEWS INTELLIGENCE</div>', unsafe_allow_html=True)

    cat_tabs = st.tabs(list(news_by_cat.keys()) + ["📈 Trends", "🎬 YouTube"])

    cat_keys = list(news_by_cat.keys())
    for i, key in enumerate(cat_keys):
        with cat_tabs[i]:
            items = news_by_cat[key]
            if items:
                df = pd.DataFrame([
                    {"#": f"{j+1:02d}", "শিরোনাম": item["title"], "সূত্র": item.get("source","—")}
                    for j, item in enumerate(items)
                ])
                st.dataframe(df, use_container_width=True, height=380, hide_index=True)
            else:
                st.info("ডেটা লোড হয়নি")

    with cat_tabs[-2]:  # Trends
        df_trends = pd.DataFrame([
            {"#": f"{i+1:02d}", "Google Daily Trends": t}
            for i, t in enumerate(trends_daily)
        ] + [
            {"#": f"R{i+1:02d}", "Google Daily Trends": t}
            for i, t in enumerate(trends_rt[:10])
        ])
        st.dataframe(df_trends, use_container_width=True, height=380, hide_index=True)

    with cat_tabs[-1]:  # YouTube
        df_yt = pd.DataFrame([
            {"#": f"{i+1:02d}", "YouTube BD ট্রেন্ডিং": t}
            for i, t in enumerate(youtube_data)
        ])
        st.dataframe(df_yt, use_container_width=True, height=380, hide_index=True)

    # ── Trending Keywords Heatmap
    st.write("")
    st.markdown('<div class="sec-label">◈ KEYWORD FREQUENCY ANALYSIS</div>', unsafe_allow_html=True)

    if top_keywords:
        max_count = top_keywords[0][1] if top_keywords else 1
        for word, count in top_keywords:
            pct = int((count / max_count) * 100)
            st.progress(pct / 100, text=f"`{word}` — {count} mentions")


# ─── RIGHT PANEL ────────────────────────────────────
with right_col:
    st.markdown('<div class="sec-label">◈ AI CONTENT ENGINE — GEMINI 2.5 FLASH</div>', unsafe_allow_html=True)

    # Topic selector
    selected = st.selectbox(
        "টপিক সিলেক্ট করুন",
        all_topics,
        help="Google News ও Google Trends থেকে একত্রিত সব ট্রেন্ডিং টপিক"
    )

    # Category filter
    cat_filter = st.multiselect(
        "অতিরিক্ত কনটেক্সট (ঐচ্ছিক)",
        ["রাজনীতি", "অর্থনীতি", "খেলাধুলা", "প্রযুক্তি", "আন্তর্জাতিক", "সমাজ", "বিনোদন"],
        default=[]
    )

    context_hint = f" [Context: {', '.join(cat_filter)}]" if cat_filter else ""

    st.write("")

    # ── Prompt Builder
    def build_prompt(topic: str, mode: str, tone: str, audience: str, words: int) -> str:
        tone_map = {
            "এলিট সাংবাদিক — প্রথম আলো স্টাইল": "elite, authoritative Bengali journalism like Prothom Alo",
            "ব্রেকিং — আর্জেন্ট ও পাঞ্চি":       "urgent, punchy breaking news with short powerful sentences",
            "ভাইরাল — সোশ্যাল মিডিয়া মাস্টার":   "viral social media style, conversational, emotionally charged",
            "গভীর বিশ্লেষণ — একাডেমিক":           "deep analytical, academic, evidence-based structured arguments",
            "ফিচার রাইটিং — ম্যাগাজিন স্টাইল":    "magazine feature writing, narrative-driven, vivid and immersive",
        }
        tone_desc = tone_map.get(tone, "professional Bengali journalism")

        sys = f"""You are the Editor-in-Chief of Bangladesh's most prestigious digital media network.
Topic: «{topic}»
Tone: {tone_desc}
Target Audience: {audience}
Bengali word target: ~{words} words
Context tags: {', '.join(cat_filter) if cat_filter else 'general'}

Rules:
- Write ONLY in natural, elite, non-robotic Bengali
- Zero AI clichés or filler phrases
- Clean markdown formatting, use relevant emojis
- Every section must be substantive and usable directly
"""

        if "Full Editorial" in mode:
            return sys + """
---
### 📱 ফেসবুক প্রিমিয়াম পোস্ট
**💥 হুক:** (এক লাইনে পাঠককে আটকে ফেলুন)
**📝 মূল বডি:** (৩-৪টি গভীর প্যারা)
**🔑 মূল পয়েন্টস:** (৩টি বুলেট)
**💬 এনগেজমেন্ট প্রশ্ন:**
**🏷️ হ্যাশট্যাগ:**

---
### 📰 ওয়েব আর্টিকেল প্যাকেজ
**ব্রেকিং হেডলাইন:**
**বিশ্লেষণমূলক হেডলাইন:**
**ভাইরাল হেডলাইন:**
**লিড প্যারাগ্রাফ:** (১৫০ শব্দ)
**রিপোর্টিং আউটলাইন:** (৫টি গভীর পয়েন্ট)

---
### 🔔 পুশ নোটিফিকেশন
(৮০ ক্যারেক্টারের মধ্যে আর্জেন্ট কপি)

---
### 📊 SEO Package
**Primary Keyword:** | **Meta Description (160 char):**
**Secondary Keywords (৫টি):**
"""

        elif "Social Media" in mode:
            return sys + """
---
### 📱 Facebook (Premium Post)
(হুক + বডি + CTA + হ্যাশট্যাগ)

---
### 🐦 Twitter/X Thread
**Tweet 1 (Hook):** | **Tweet 2:** | **Tweet 3:** | **Tweet 4:** | **Tweet 5 (CTA):**

---
### 📸 Instagram Caption
(ক্যাপশন + ৮-১০ হ্যাশট্যাগ)

---
### 💬 WhatsApp Broadcast
(ফরোয়ার্ডযোগ্য সংক্ষিপ্ত মেসেজ)

---
### 📺 YouTube Community Post
"""

        elif "Video Script" in mode:
            return sys + """
---
### 🎬 Hook (০-৫ সেকেন্ড)
(দর্শককে থামানোর একটি লাইন)

---
### 🎙 ফুল ভিডিও স্ক্রিপ্ট
- **ইন্ট্রো (০:০০-০:৩০):**
- **সেকশন ১ (০:৩০-১:৩০):**
- **সেকশন ২ (১:৩০-৩:০০):**
- **আউট্রো + CTA (৩:০০-৩:৩০):**

---
### 🖼 Thumbnail Text Ideas (৩টি অপশন)
### 🏷️ YouTube Tags (১৫টি)
### 📝 Video Description (SEO-optimized)
"""

        elif "SEO" in mode:
            return sys + """
---
### 🎯 SEO Intelligence Report
**Primary Keyword:** | **Search Intent:**
**Secondary Keywords (৮টি):**
**LSI Keywords (৫টি):**

---
### 📑 Article Structure
(H1 → H2 → H3 hierarchy with word count per section)

---
### 🔗 Link Strategy
**Internal Links (৩টি):** | **External Authority Links (৩টি):**

---
### 📊 SERP Feature Opportunities
(Featured Snippet, People Also Ask, Knowledge Panel)

---
### 📈 Content Gaps & Angles
(প্রতিযোগীরা মিস করছে কী?)
"""

        else:  # Investigative Angle Finder
            return sys + """
---
### 🔎 Investigative Angles (৫টি)
(প্রতিটি অ্যাঙ্গেলে: প্রশ্ন + কেন গুরুত্বপূর্ণ + কোথায় তথ্য পাবেন)

---
### 📂 Source Map
(বিশেষজ্ঞ + সরকারি ডেটা + স্থানীয় সোর্স)

---
### ⚠️ Story Risks & Ethics
(কী সতর্কতা নিতে হবে)

---
### 📊 Data Points to Find
(রিপোর্টারের জন্য ৬টি নির্দিষ্ট ডেটা টার্গেট)

---
### 🗣️ Expert Quote Angles
(কোন বিশেষজ্ঞকে কোন প্রশ্ন করবেন)
"""

    # Generate button
    if st.button("◈ GENERATE INTELLIGENCE REPORT", use_container_width=True):
        if not api_key:
            st.error("⚠ সাইডবারে Gemini API Key দিন — aistudio.google.com এ বিনামূল্যে পাওয়া যায়।")
        else:
            prompt = build_prompt(
                selected + context_hint,
                content_mode, tone_mode,
                target_audience, word_limit
            )
            with st.spinner("◈ Gemini 2.5 Flash রিপোর্ট তৈরি করছে..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    resp  = model.generate_content(prompt)
                    output = resp.text

                    word_count = len(output.split())
                    char_count = len(output)

                    st.markdown(f"""
                    <div class="ai-frame">
                      <div class="ai-header">
                        ◈ &nbsp; AI OUTPUT · {word_count} WORDS · {content_mode[:18].upper()}
                      </div>
                      <div class="ai-body">
                    """, unsafe_allow_html=True)

                    st.markdown(output)

                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # Download
                    fname = f"newsiq_{selected[:20].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                    st.download_button(
                        "⬇ DOWNLOAD REPORT (.TXT)",
                        data=output,
                        file_name=fname,
                        mime="text/plain",
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"Gemini Error: {e}")

    # ── Quick Keyword Cloud (from all_topics)
    st.write("")
    st.markdown('<div class="sec-label">◈ TRENDING TOPIC CLOUD</div>', unsafe_allow_html=True)

    kw_html = ""
    for word, count in top_keywords:
        heat_cls = "h" if count >= 3 else ("m" if count >= 2 else "l")
        kw_html += f'<span class="cat-pill">{word} <b>{count}</b></span>'
    st.markdown(f'<div style="line-height:2.4;">{kw_html}</div>', unsafe_allow_html=True)

    # ── Live source breakdown
    st.write("")
    st.markdown('<div class="sec-label">◈ SOURCE BREAKDOWN</div>', unsafe_allow_html=True)

    src_counter = Counter(i.get("source","Unknown") for i in all_news_items)
    top_sources = src_counter.most_common(8)
    if top_sources:
        max_s = top_sources[0][1]
        for src, cnt in top_sources:
            st.progress(cnt / max_s, text=f"`{src}` — {cnt} articles")


# ══════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════
st.write("")
st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,0.06); padding-top:18px; margin-top:12px;
  display:flex; justify-content:space-between; align-items:center;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#3D4A5C; letter-spacing:2px;">
    ◈ NEWSIQ PRO v3.0 · BUILT FOR BANGLADESH NEWSROOMS · MIT LICENSE
  </div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#3D4A5C; letter-spacing:1px;">
    DATA: GOOGLE NEWS RSS · GOOGLE TRENDS · YOUTUBE BD
  </div>
</div>
""", unsafe_allow_html=True)
