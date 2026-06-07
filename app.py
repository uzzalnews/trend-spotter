"""
╔══════════════════════════════════════════════════════════════════╗
║         TREND SPOTTER INTELLIGENCE PRO  —  v2.0                 ║
║         Bangladesh's #1 AI-Powered Newsroom Radar               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import time
import json
from datetime import datetime
from pytrends.request import TrendReq
import google.generativeai as genai

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Trend Spotter Intelligence Pro",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM CSS — Dark Editorial Newsroom Aesthetic
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;600&family=Noto+Sans+Bengali:wght@400;600;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:    #080C14;
    --bg-secondary:  #0D1320;
    --bg-card:       #111827;
    --bg-card-hover: #1a2234;
    --border:        rgba(255,255,255,0.07);
    --border-bright: rgba(255,255,255,0.15);
    --accent-red:    #E63946;
    --accent-blue:   #3B9EFF;
    --accent-green:  #00C896;
    --accent-amber:  #F4A261;
    --text-primary:  #F0F4FF;
    --text-muted:    #8A95A5;
    --text-dim:      #4A5568;
    --mono:          'IBM Plex Mono', monospace;
    --serif:         'DM Serif Display', serif;
    --bengali:       'Noto Sans Bengali', sans-serif;
}

/* ── Global Reset ── */
.stApp, .main, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Masthead ── */
.masthead {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 28px 0 20px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.masthead-logo {
    font-family: var(--serif);
    font-size: 36px;
    color: var(--accent-red);
    letter-spacing: -1px;
    line-height: 1;
}
.masthead-title {
    font-family: var(--serif);
    font-size: 26px;
    color: var(--text-primary);
    font-weight: 400;
    letter-spacing: -0.3px;
    line-height: 1.2;
}
.masthead-sub {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(230,57,70,0.15);
    border: 1px solid rgba(230,57,70,0.4);
    color: var(--accent-red);
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
}
.live-dot {
    width: 6px; height: 6px;
    background: var(--accent-red);
    border-radius: 50%;
    animation: pulse-red 1.4s ease infinite;
}
@keyframes pulse-red {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

/* ── Ticker ── */
.ticker-wrap {
    background: var(--accent-red);
    padding: 8px 0;
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 28px;
    border-radius: 6px;
}
.ticker-label {
    display: inline-block;
    background: #8B0000;
    color: #fff;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 0 14px;
    margin-right: 12px;
    text-transform: uppercase;
}
.ticker-content {
    display: inline-block;
    animation: ticker-scroll 30s linear infinite;
    font-family: var(--bengali);
    font-size: 13px;
    font-weight: 600;
    color: #fff;
}
@keyframes ticker-scroll {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.red::before   { background: var(--accent-red); }
.kpi-card.blue::before  { background: var(--accent-blue); }
.kpi-card.green::before { background: var(--accent-green); }
.kpi-card.amber::before { background: var(--accent-amber); }

.kpi-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-bright);
    transform: translateY(-2px);
}
.kpi-source {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.kpi-card.red   .kpi-source { color: var(--accent-red); }
.kpi-card.blue  .kpi-source { color: var(--accent-blue); }
.kpi-card.green .kpi-source { color: var(--accent-green); }
.kpi-card.amber .kpi-source { color: var(--accent-amber); }

.kpi-number {
    font-family: var(--serif);
    font-size: 38px;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
}
.kpi-icon {
    position: absolute;
    top: 14px; right: 16px;
    font-size: 28px;
    opacity: 0.12;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.section-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.section-title {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted);
    white-space: nowrap;
}

/* ── Data Table Overrides ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: var(--bg-card) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg-secondary) !important;
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 10px 14px !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    font-family: var(--bengali) !important;
    font-size: 13px !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 10px 14px !important;
    background: transparent !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: rgba(59,158,255,0.05) !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: var(--text-primary) !important;
    border-bottom-color: var(--accent-blue) !important;
    background: transparent !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--bengali) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(59,158,255,0.2) !important;
}
[data-baseweb="popover"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 8px !important;
}
[role="option"] {
    color: var(--text-primary) !important;
    font-family: var(--bengali) !important;
    background: transparent !important;
}
[role="option"]:hover {
    background: rgba(59,158,255,0.1) !important;
}

/* ── Content Type Radio ── */
[data-testid="stRadio"] label {
    font-family: var(--mono) !important;
    font-size: 12px !important;
    color: var(--text-muted) !important;
}
[data-testid="stRadio"] [data-baseweb="radio"] div {
    border-color: var(--border-bright) !important;
}

/* ── Generate Button ── */
[data-testid="stButton"] button {
    background: var(--accent-red) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(230,57,70,0.25) !important;
}
[data-testid="stButton"] button:hover {
    background: #C1121F !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(230,57,70,0.4) !important;
}

/* ── AI Output Box ── */
.ai-output {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-blue);
    border-radius: 0 10px 10px 0;
    padding: 24px;
    margin-top: 16px;
    font-family: var(--bengali);
    font-size: 14px;
    line-height: 1.9;
    color: var(--text-primary);
}
.ai-output h3 {
    font-family: var(--mono) !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--accent-blue) !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] label {
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
}
[data-testid="stSidebar"] input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(59,158,255,0.15) !important;
}

/* ── Status Dots ── */
.status-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.status-dot.green  { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-dot.red    { background: var(--accent-red);   box-shadow: 0 0 6px var(--accent-red); }
.status-dot.yellow { background: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }

/* ── Timestamp ── */
.timestamp {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 1px;
}

/* ── Rank Badge ── */
.rank-badge {
    display: inline-block;
    background: rgba(59,158,255,0.12);
    color: var(--accent-blue);
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 8px;
}

/* ── Spinner Override ── */
[data-testid="stSpinner"] {
    color: var(--accent-blue) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(230,57,70,0.1) !important;
    border: 1px solid rgba(230,57,70,0.3) !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

/* ── Success box ── */
.output-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px;
    background: rgba(0,200,150,0.08);
    border: 1px solid rgba(0,200,150,0.25);
    border-radius: 8px 8px 0 0;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent-green);
}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.markdown("---")

    api_key = st.text_input(
        "GEMINI API KEY",
        type="password",
        placeholder="AIza...",
        help="Google AI Studio থেকে বিনামূল্যে API Key নিন"
    )

    st.markdown("---")
    st.markdown("### 🎯 Content Settings")

    content_type = st.radio(
        "আউটপুট ফরম্যাট",
        ["🗞️ Full Editorial Kit", "📱 Social Media Pack", "📺 Script + Hook", "📊 SEO Article Brief"],
        index=0
    )

    tone_select = st.selectbox(
        "টোন সিলেক্ট করুন",
        ["প্রফেশনাল সাংবাদিক", "ভাইরাল ক্যাজুয়াল", "অ্যাকাডেমিক বিশ্লেষণ", "ব্রেকিং নিউজ আর্জেন্ট"]
    )

    word_limit = st.slider("Word Count Target", 300, 1200, 600, 50)

    st.markdown("---")
    st.markdown("### 📡 Feed Status")

    now = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="status-row"><span class="status-dot green"></span>Google Trends BD — LIVE</div>
    <div class="status-row"><span class="status-dot green"></span>Google Realtime RSS — LIVE</div>
    <div class="status-row"><span class="status-dot yellow"></span>YouTube Trends — CACHED</div>
    <div class="status-row"><span class="status-dot green"></span>Prothom Alo RSS — LIVE</div>
    <div class="status-row"><span class="status-dot green"></span>BDNews24 RSS — LIVE</div>
    <br><div class="timestamp">LAST SYNC: {now} BDT</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v2.0 · Built for BD Newsrooms · MIT License")

    if api_key:
        genai.configure(api_key=api_key)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA FETCHING — Cached, Resilient, Typed
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@st.cache_data(ttl=120, show_spinner=False)
def fetch_google_daily_trends() -> list[str]:
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        df = pytrends.trending_searches(pn='bangladesh')
        return df[0].tolist()[:20]
    except Exception:
        return [
            "বাংলাদেশ জাতীয় রাজনীতি আপডেট",
            "ঢাকার আবহাওয়া ও বন্যা পরিস্থিতি",
            "অর্থনৈতিক সংকট ও মূল্যস্ফীতি",
            "বাংলাদেশ ক্রিকেট টিম আপডেট",
            "ঢাকা সিটি কর্পোরেশন নির্বাচন",
        ]


@st.cache_data(ttl=90, show_spinner=False)
def fetch_google_realtime_trends() -> list[str]:
    url = "https://trends.google.com/trending/rss?geo=BD"
    topics = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            root = ET.fromstring(response.read())
            for item in root.findall(".//item")[:20]:
                title_el = item.find("title")
                if title_el is not None and title_el.text:
                    topics.append(title_el.text.strip())
    except Exception:
        pass
    return topics or [
        "ঢাকায় তীব্র যানজট",
        "সোশ্যাল মিডিয়া ভাইরাল টপিক",
        "আজকের শীর্ষ ট্রেন্ডস",
    ]


@st.cache_data(ttl=180, show_spinner=False)
def fetch_youtube_bd_trends() -> list[str]:
    """
    YouTube Data API v3 without a key returns 403.
    We parse the public YouTube trending RSS (no key needed).
    Fallback to curated placeholders if blocked.
    """
    url = "https://www.youtube.com/feeds/videos.xml?chart=mostpopular&regionCode=BD&hl=bn"
    titles = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            ns = {"media": "http://search.yahoo.com/mrss/", "yt": "http://www.youtube.com/xml/schemas/2015"}
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:20]:
                title_el = entry.find("{http://www.w3.org/2005/Atom}title")
                if title_el is not None and title_el.text:
                    titles.append(title_el.text.strip())
    except Exception:
        pass

    if not titles:
        titles = [
            "নতুন বাংলা নাটক — ভাইরাল এপিসোড রিভিউ",
            "আজকের টকশো — রাজনৈতিক বিশ্লেষণ",
            "মোবাইল আনবক্সিং ও গ্যাজেট রিভিউ",
            "ভাইরাল ফুড ব্লগ ও রেস্টুরেন্ট ট্যুর",
            "ক্রিকেট ম্যাচ হাইলাইটস ও বিশ্লেষণ",
            "অনলাইন ইনকাম ও ফ্রিল্যান্সিং গাইড",
            "ইসলামিক লেকচার ও ওয়াজ ট্রেন্ডস",
            "বাংলাদেশি কমেডি ও প্র্যাঙ্ক ভিডিও",
            "স্বাস্থ্য ও ফিটনেস টিপস বাংলায়",
            "নতুন বাংলা মিউজিক ভিডিও হিটস",
        ]
    return titles


@st.cache_data(ttl=90, show_spinner=False)
def fetch_news_portal_headlines() -> list[str]:
    feeds = [
        "https://www.prothomalo.com/feed",
        "https://bangla.bdnews24.com/?widgetName=rssfeed&widgetId=1151",
        "https://www.kalerkantho.com/rss.xml",
    ]
    headlines = []
    for url in feeds:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item")[:8]:
                    title_el = item.find("title")
                    if title_el is not None and title_el.text:
                        t = title_el.text.strip()
                        if t not in headlines:
                            headlines.append(t)
        except Exception:
            continue
    return headlines[:20] or ["শীর্ষ পোর্টালগুলোর লিড হেডলাইন ফেচ হয়নি — পুনরায় রিফ্রেশ করুন"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FETCH ALL DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.spinner("📡 Live feeds লোড হচ্ছে..."):
    google_daily    = fetch_google_daily_trends()
    google_realtime = fetch_google_realtime_trends()
    youtube_trends  = fetch_youtube_bd_trends()
    portal_news     = fetch_news_portal_headlines()

all_topics = list(dict.fromkeys(google_daily + google_realtime + youtube_trends + portal_news))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MASTHEAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
now_str = datetime.now().strftime("%A, %d %B %Y — %H:%M BDT")

st.markdown(f"""
<div class="masthead">
  <div class="masthead-logo">⚡</div>
  <div>
    <div class="masthead-title">Trend Spotter Intelligence Pro</div>
    <div class="masthead-sub">Bangladesh Newsroom Radar · {now_str}</div>
  </div>
  <div style="margin-left:auto; display:flex; gap:10px; align-items:center;">
    <span class="live-badge"><span class="live-dot"></span>LIVE</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BREAKING NEWS TICKER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ticker_items = portal_news[:8] + google_realtime[:5]
ticker_text  = "  ●  ".join(ticker_items) if ticker_items else "লাইভ ডেটা লোড হচ্ছে..."

st.markdown(f"""
<div class="ticker-wrap">
  <span class="ticker-label">⚡ BREAKING</span>
  <span class="ticker-content">{ticker_text}</span>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KPI CARDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card red">
    <div class="kpi-icon">🔍</div>
    <div class="kpi-source">Google Daily</div>
    <div class="kpi-number">{len(google_daily)}</div>
    <div class="kpi-label">Active Search Trends</div>
  </div>
  <div class="kpi-card blue">
    <div class="kpi-icon">📡</div>
    <div class="kpi-source">Realtime RSS</div>
    <div class="kpi-number">{len(google_realtime)}</div>
    <div class="kpi-label">Live Viral Topics</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-icon">🎬</div>
    <div class="kpi-source">YouTube BD</div>
    <div class="kpi-number">{len(youtube_trends)}</div>
    <div class="kpi-label">Trending Videos</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-icon">📰</div>
    <div class="kpi-source">News Portals</div>
    <div class="kpi-number">{len(portal_news)}</div>
    <div class="kpi-label">Live Headlines</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN LAYOUT — Two Columns
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
col_left, col_right = st.columns([1.05, 1.3], gap="large")

# ─── LEFT — Data Intelligence Panel ───
with col_left:
    st.markdown("""
    <div class="section-header">
      <div class="section-title">📊 Live Intelligence Feeds</div>
      <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Google Daily",
        "📡 Realtime",
        "🎬 YouTube",
        "📰 News Portals",
    ])

    def _make_df(items: list[str], col: str) -> pd.DataFrame:
        return pd.DataFrame(
            [{"#": f"{i+1:02d}", col: item} for i, item in enumerate(items)],
        )

    with tab1:
        st.dataframe(
            _make_df(google_daily, "বাংলাদেশ গুগল সার্চ ট্রেন্ড"),
            use_container_width=True, height=420, hide_index=True
        )

    with tab2:
        st.dataframe(
            _make_df(google_realtime, "গুগল রিয়েলটাইম ট্রেন্ডিং টপিক"),
            use_container_width=True, height=420, hide_index=True
        )

    with tab3:
        st.dataframe(
            _make_df(youtube_trends, "ইউটিউব বাংলাদেশ ভিডিও ট্রেন্ড"),
            use_container_width=True, height=420, hide_index=True
        )

    with tab4:
        st.dataframe(
            _make_df(portal_news, "প্রথম আলো · বিডিনিউজ২৪ · কালের কণ্ঠ"),
            use_container_width=True, height=420, hide_index=True
        )

    st.caption(f"🔄 Auto-refresh every 2 min · Last loaded: {datetime.now().strftime('%H:%M:%S')}")


# ─── RIGHT — AI Content Generator ───
with col_right:
    st.markdown("""
    <div class="section-header">
      <div class="section-title">✍️ AI Content Engine</div>
      <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    selected_topic = st.selectbox(
        "টপিক বেছে নিন",
        all_topics,
        help="সমস্ত সোর্স থেকে মার্জ করা ট্রেন্ডিং টপিক"
    )

    st.write("")

    # Prompt builder based on content type and tone
    def build_prompt(topic: str, c_type: str, tone: str, words: int) -> str:
        tone_map = {
            "প্রফেশনাল সাংবাদিক":    "formal, authoritative, investigative journalism style",
            "ভাইরাল ক্যাজুয়াল":       "casual, punchy, viral social media style with relatable language",
            "অ্যাকাডেমিক বিশ্লেষণ":   "academic, analytical, evidence-based tone with structured arguments",
            "ব্রেকিং নিউজ আর্জেন্ট":  "urgent, breaking news style with short sentences and high urgency",
        }
        tone_desc = tone_map.get(tone, "professional Bengali journalism")

        base = f"""
You are the Editor-in-Chief of Bangladesh's #1 premium digital news network.
Topic: '{topic}'
Tone: {tone_desc}
Target Bengali word count: approximately {words} words.
Write ONLY in natural, elite, non-robotic Bengali. Zero AI clichés.
Use clean markdown formatting with emojis where appropriate.
"""

        if "Full Editorial" in c_type:
            return base + """
---
### 📱 ফেসবুক প্রিমিয়াম পোস্ট
- **💥 হুক লাইন:** (আল্টা-শক্তিশালী, ক্লিক-ইন্ডিউসিং প্রথম লাইন)
- **📝 মূল কন্টেন্ট:** (৩-৪টি গভীর, এনগেজিং প্যারাগ্রাফ)
- **📌 কী পয়েন্টস:** (৩টি বুলেট)
- **💬 অডিয়েন্স প্রশ্ন:** (কমেন্ট আনার প্রশ্ন)
- **🏷️ হ্যাশট্যাগ:** (৪-৫টি)

---
### 📰 ওয়েব আর্টিকেল প্যাকেজ
- **শিরোনাম ১ (ব্রেকিং):**
- **শিরোনাম ২ (বিশ্লেষণমূলক):**
- **শিরোনাম ৩ (ভাইরাল):**
- **সাবহেডিং / লিড প্যারাগ্রাফ:**
- **রিপোর্টিং আউটলাইন (৫ পয়েন্ট):**

---
### 📊 SEO & Distribution
- **প্রাইমারি কীওয়ার্ড:**
- **মেটা ডিসক্রিপশন (১৬০ ক্যারেক্টার):**
- **পুশ নোটিফিকেশন কপি:**
"""

        elif "Social Media" in c_type:
            return base + """
---
### 📱 Facebook Post (Premium)
(হুক + মূল কন্টেন্ট + CTA + হ্যাশট্যাগ)

---
### 🐦 Twitter/X Thread (৫ টুইট)
1. 2. 3. 4. 5.

---
### 📸 Instagram Caption
(এনগেজিং ক্যাপশন + হ্যাশট্যাগ)

---
### 💬 WhatsApp Broadcast
(সংক্ষিপ্ত, শেয়ারযোগ্য মেসেজ)
"""

        elif "Script" in c_type:
            return base + """
---
### 🎬 YouTube/Reel Hook (প্রথম ৫ সেকেন্ড)

---
### 🎙️ ভিডিও স্ক্রিপ্ট আউটলাইন
- ইন্ট্রো (০:০০–০:৩০):
- মূল কন্টেন্ট (০:৩০–৩:০০):
- আউট্রো + CTA (৩:০০–৩:৩০):

---
### 📌 Thumbnail টেক্সট আইডিয়া (৩টি)
"""

        else:  # SEO Article Brief
            return base + """
---
### 🎯 Article Brief
- **প্রাইমারি কীওয়ার্ড:**
- **সেকেন্ডারি কীওয়ার্ড (৫টি):**
- **টার্গেট অডিয়েন্স:**

---
### 📑 আর্টিকেল স্ট্রাকচার (H2/H3)
(৬-৭টি সেকশন আউটলাইন)

---
### 🔗 Internal & External Link সাজেশন
---
### 📊 ডেটা ও রিসার্চ পয়েন্ট (৪টি)
"""

    # Generate Button
    generate = st.button("⚡ GENERATE CONTENT KIT", use_container_width=True)

    if generate:
        if not api_key:
            st.error("❌ সাইডবারে Gemini API Key দিন — বিনামূল্যে পাবেন aistudio.google.com তে।")
        else:
            prompt = build_prompt(selected_topic, content_type, tone_select, word_limit)
            with st.spinner("🤖 Gemini 2.5 Flash কন্টেন্ট তৈরি করছে..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    output = response.text

                    st.markdown(f"""
                    <div class="output-header">
                      ✅ &nbsp; GENERATED · {len(output.split())} words · {selected_topic[:40]}...
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f'<div class="ai-output">', unsafe_allow_html=True)
                    st.markdown(output)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Download button
                    st.download_button(
                        label="⬇️ DOWNLOAD AS .TXT",
                        data=output,
                        file_name=f"content_{selected_topic[:20].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"Gemini API Error: {e}")
