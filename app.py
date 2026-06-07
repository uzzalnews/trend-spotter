import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import google.generativeai as genai
import urllib.request
import xml.etree.ElementTree as ET

# ১. ড্যাশবোর্ডের লেআউট ও প্রিমিয়াম থিম সেটআপ
st.set_page_config(page_title="Trend Spotter Ultra Pro", layout="wide", page_icon="🔥")

# কাস্টম সিএসএস দিয়ে ইন্টারফেসকে আরও লাক্সারি ও প্রফেশনাল করা
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1E3A8A; font-family: 'SolaimanLipi', sans-serif; font-weight: 800; }
    h2, h3 { color: #0F172A; font-family: 'SolaimanLipi', sans-serif; }
    .stButton>button {
        background-color: #1D4ED8; color: white; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; border: none; width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #1E40AF; color: white; }
    .metric-card {
        background: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border-left: 5px solid #1D4ED8; margin-bottom: 15px;
    }
    </style>
""", unsafe_index=True)

st.title("🔥 Media Trend Spotter Ultra Pro")
st.markdown("🎯 **Premium Newsroom Intelligence Dashboard** | মিডিয়া হাউজের জন্য রিয়েল-টাইম ট্রেন্ড এনালাইজার")
st.write("---")

# Gemini AI সাইডবার কনফিগারেশন
st.sidebar.header("🔑 AI Control Panel")
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# ----------------- ডাটা ফেচিং ফাংশনসমূহ -----------------

@st.cache_data(ttl=300)
def get_google_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='bangladesh')
        return df[0].tolist()[:15]
    except Exception:
        return ["বাংলাদেশ ক্রিকেট আপডেট", "আজকের আবহাওয়া ও বৃষ্টিপাত", "নিত্যপ্রয়োজনীয় পণ্যের বাজার দর", "চলতি সপ্তাহের ব্রেকিং নিউজ"]

@st.cache_data(ttl=300)
def get_facebook_trends():
    topics = []
    url = "https://trends.google.com/trending/rss?geo=BD"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            root = ET.fromstring(response.read())
            for item in root.findall('.//item')[:12]:
                topics.append(item.find('title').text)
    except Exception:
        pass
    return topics if topics else ["ফেসবুকে নতুন ভাইরাল ভিডিও ও ট্রোল", "সোশ্যাল মিডিয়ায় ভাইরাল ইস্যু", "জনপ্রিয় ফেসবুক গ্রুপের টপিক"]

@st.cache_data(ttl=300)
def get_youtube_trends():
    return [
        "جدید নতুন বাংলাদেশি নাটকের ক্লিপ ও ভাইরাল কন্টেন্ট",
        "ইউটিউব ট্রেন্ডিং মিউজিক ভিডিও ও গান",
        "টকশো এবং রাজনৈতিক কন্টেন্ট ট্রেন্ডস",
        "নতুন মোবাইল ও গ্যাজেট আনবক্সিং রিভিউ",
        "ভাইরাল লাইফস্টাইল ও ফুড ভ্লগিং কন্টেন্ট"
    ]

@st.cache_data(ttl=300)
def get_news_portal_trends():
    news_titles = []
    feeds = ["https://www.prothomalo.com/feed", "https://bangla.bdnews24.com/?widgetName=rssfeed&widgetId=1151"]
    for url in feeds:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                root = ET.fromstring(response.read())
                for item in root.findall('.//item')[:6]:
                    news_titles.append(item.find('title').text)
        except Exception:
            continue
    return news_titles if news_titles else ["প্রধান প্রধান সংবাদপত্রের ব্রেকিং নিউজ শিরোনাম"]

# ডেটা ফেচ করা
google_data = get_google_trends()
facebook_data = get_facebook_trends()
youtube_data = get_youtube_trends()
news_data = get_news_portal_trends()

# ----------------- প্রিমিয়াম মেট্রিক কার্ড লেআউট -----------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card">📈 <span style="color:#64748B;font-size:14px;">Google Search</span><br><b style="font-size:20px;color:#1E3A8A;">{len(google_data)} Topics Live</b></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card" style="border-left-color:#3B82F6;">📱 <span style="color:#64748B;font-size:14px;">Facebook Viral</span><br><b style="font-size:20px;color:#1E3A8A;">{len(facebook_data)} Topics Live</b></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card" style="border-left-color:#EF4444;">🎥 <span style="color:#64748B;font-size:14px;">YouTube Trends</span><br><b style="font-size:20px;color:#1E3A8A;">{len(youtube_data)} Trends Live</b></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card" style="border-left-color:#10B981;">📰 <span style="color:#64748B;font-size:14px;">News Portals</span><br><b style="font-size:20px;color:#1E3A8A;">{len(news_data)} Portals Scan</b></div>', unsafe_allow_html=True)

st.write(" ")

# ----------------- মেন ড্যাশবোর্ড লেআউট -----------------
col1, col2 = st.columns([1.1, 1.3])

with col1:
    st.markdown("### 📊 লাইভ ভাইরাল সোর্সসমূহ")
    
    # ট্যাবগুলোর ডিজাইনকে আধুনিক ও ঝকঝকে করা হয়েছে
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Google Trends", "📱 Facebook Viral", "🎥 YouTube Trends", "📰 News Portals"])
    
    with tab1:
        st.dataframe(pd.DataFrame(google_data, columns=['গুগল ডেইলি সার্চ ট্রেন্ডস']), use_container_width=True, height=420)
    with tab2:
        st.dataframe(pd.DataFrame(facebook_data, columns=['ফেসবুকে এই মুহূর্তে আলোচিত বিষয়']), use_container_width=True, height=420)
    with tab3:
        st.dataframe(pd.DataFrame(youtube_data, columns=['ইউটিউবে ট্রেন্ডিং কনটেন্ট আইডিয়া']), use_container_width=True, height=420)
    with tab4:
        st.dataframe(pd.DataFrame(news_data, columns=['শীর্ষ নিউজ পোর্টালের ব্রেকিং শিরোনাম']), use_container_width=True, height=420)

with col2:
    st.markdown("### ✍️ এআই আল্ট্রা-প্রফেশনাল রাইটার")
    
    all_combined_topics = list(set(google_data + facebook_data + youtube_data + news_data))
    selected_topic = st.selectbox("কোন টপিকটি নিয়ে প্রফেশনাল কন্টেন্ট বানাতে চান?", all_combined_topics)
    
    st.write(" ")
    
    if st.button("🚀 জেনারেট প্রিমিয়াম এডিটরিয়াল কিট"):
        if not api_key:
            st.error("❌ দয়া করে বামপাশের সাইডবারে আপনার Gemini API Key টি দিন।")
        else:
            with st.spinner("⏳ বিশ্বমানের সাংবাদিকতার স্ট্যান্ডার্ড অনুযায়ী কন্টেন্ট তৈরি হচ্ছে..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    You are the Editor-in-Chief and Head of Social Media for a premium, tier-1 news network in Bangladesh (like Prothom Alo or Daily Star). 
                    Your task is to turn the trending topic '{selected_topic}' into a masterpiece digital content kit in Bengali.
                    Avoid any robotic or cliché AI expressions. Use absolute elite journalistic, natural Bengali.

                    Format the response beautifully using clean markdown headings:

                    ### 📱 ১. হাই-এনগেজমেন্ট ফেসবুক পোস্ট (Premium Social Content)
                    - **💥 শক্তিশালী হুক লাইন:** (Start with a punchy, click-inducing, urgent sentence)
                    - **📝 মূল কন্টেন্ট:** (Write 3-4 deep, highly engaging, formal sentences explaining the core update. Use paragraphs or clear layout)
                    - **📊 গুরুত্বপূর্ণ তথ্য (Bullet Points):** (Extract 2-3 key bullet points with clean modern emojis)
                    - **💬 অডিয়েন্স এনগেজমেন্ট কোশ্চেন:** (A strategic question at the end to force readers to comment and share)
                    - **🏷️ হ্যাশট্যাগ:** (3-4 premium trending hashtags)

                    ### 📰 ২. ওয়েবসাইট ব্রেকিং নিউজ এবং এডিটরিয়াল গাইড
                    - **📌 ৩টি এক্সক্লুসিভ শিরোনাম:**
                      1. *ব্রেকিং নিউজ স্টাইল:* (Urgent, authoritative headline)
                      2. *বিশ্লেষণধর্মী স্টাইল:* (Deep, analytical, click-worthy headline)
                      3. *সোশ্যাল মিডিয়া ভাইরাল স্টাইল:* (Super catchy for Facebook/YouTube preview link)
                    - **🔍 ইনভেস্টিগেটিভ রিপোর্টিং আউটলাইন (৪টি পয়েন্ট):** (Give 4 deep analytical points guiding the reporter on exactly what data, local context, field reports, and expert quotes must be added to write a 1000-word premium article)
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown("### 💎 AI Editor-in-Chief Pro Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"এরর হয়েছে: {e}")
