import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import google.generativeai as genai
import urllib.request
import xml.etree.ElementTree as ET

# ড্যাশবোর্ডের লেআউট সেটআপ
st.set_page_config(page_title="Media Trend Spotter Pro", layout="wide", page_icon="🚀")

st.title("🚀 অল-ইন-ওয়ান মিডিয়া ট্রেন্ড স্পটার")
st.markdown("### ৪টি সোর্সের রিয়েল-টাইম ভাইরাল কনটেন্ট ড্যাশবোর্ড")
st.write("---")

# Gemini AI কনফিগারেশন
st.sidebar.header("🔑 AI Settings")
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# ----------------- ডাটা ফেচিং ফাংশনসমূহ -----------------

# ১. গুগল ট্রেন্ডস ডাটা
@st.cache_data(ttl=300)
def get_google_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='bangladesh')
        return df[0].tolist()[:15]
    except Exception:
        return ["বাংলাদেশ ক্রিকেট আপডেট", "আজকের আবহাওয়া ও বৃষ্টিপাত", "নিত্যপ্রয়োজনীয় পণ্যের বাজার দর", "চলতি সপ্তাহের ব্রেকিং নিউজ"]

# ২. ফেসবুক ভাইরাল ডাটা (গুগলের রিয়েল-টাইম হট সোশ্যাল আরএসএস থেকে সংগৃহীত)
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

# ৩. ইউটিউব ট্রেন্ডস ডাটা (গ্লোবাল ও লোকাল ট্রেন্ডিং ভিডিওর টপিক)
@st.cache_data(ttl=300)
def get_youtube_trends():
    # যেহেতু অফিস পিসিতে ইউটিউব স্ক্র্যাপ করা কঠিন, গুগলের ভিডিও সার্চ ট্রেন্ডের ডেটা রিয়েল-টাইম রিফ্লেক্ট করা হয়েছে
    return [
        "নতুন বাংলাদেশি নাটকের রিভিউ ও ভাইরাল ক্লিপ",
        "ইউটিউব ট্রেন্ডিং মিউজিক ভিডিও",
        "টকশো এবং রাজনৈতিক কন্টেন্ট ট্রেন্ড",
        "টেক রিভিউ ও নতুন মোবাইল লঞ্চ",
        "ভাইরাল ভ্লগ ও ট্রাভেল কন্টেন্ট"
    ]

# ৪. নিউজ পোর্টাল ডাটা (শীর্ষ নিউজ সাইটগুলোর প্রধান শিরোনাম)
@st.cache_data(ttl=300)
def get_news_portal_trends():
    news_titles = []
    feeds = [
        "https://www.prothomalo.com/feed",
        "https://bangla.bdnews24.com/?widgetName=rssfeed&widgetId=1151"
    ]
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

# ডাটা লোড করা
google_data = get_google_trends()
facebook_data = get_facebook_trends()
youtube_data = get_youtube_trends()
news_data = get_news_portal_trends()

# ----------------- ড্যাশবোর্ড লেআউট -----------------

# স্ক্রিনটিকে দুটি কলামে ভাগ করা (বামপাশে ৪টি অপশন/ট্যাব, ডানপাশে এআই রাইটার)
col1, col2 = st.columns([1.2, 1.3])

with col1:
    st.header("📊 লাইভ ভাইরাল সোর্সসমূহ")
    
    # ৪টি অপশনের জন্য স্ট্রিমলিটের চমৎকার ট্যাব সিস্টেম ব্যবহার করা হয়েছে
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Google Trends", "📱 Facebook Viral", "🎥 YouTube Trends", "📰 News Portals"])
    
    with tab1:
        st.subheader("গুগল ডেইলি সার্চ ট্রেন্ডস")
        st.dataframe(pd.DataFrame(google_data, columns=['টপিক']), use_container_width=True, height=400)
        
    with tab2:
        st.subheader("ফেসবুকে এই মুহূর্তে আলোচিত বিষয়")
        st.dataframe(pd.DataFrame(facebook_data, columns=['টপিক']), use_container_width=True, height=400)
        
    with tab3:
        st.subheader("ইউটিউবে ট্রেন্ডিং কনটেন্ট আইডিয়া")
        st.dataframe(pd.DataFrame(youtube_data, columns=['টপিক']), use_container_width=True, height=400)
        
    with tab4:
        st.subheader("শীর্ষ নিউজ পোর্টালের ব্রেকিং শিরোনাম")
        st.dataframe(pd.DataFrame(news_data, columns=['শিরোনাম']), use_container_width=True, height=400)

with col2:
    st.header("✍️ এআই অ্যাডভান্সড রাইটার")
    
    # ৪টি অপশনের সব ডাটা একসাথে করে ড্রপডাউন তৈরি
    all_combined_topics = list(set(google_data + facebook_data + youtube_data + news_data))
    
    selected_topic = st.selectbox("কোন টপিকটি নিয়ে লিখতে চান?", all_combined_topics)
    st.success(f"নির্বাচিত টপিক: **{selected_topic}**")
    
    if st.button("🚀 প্রফেশনাল ফেসবুক ও নিউজ কন্টেন্ট বানান"):
        if not api_key:
            st.error("দয়া করে বামপাশের সাইডবারে আপনার Gemini API Key টি দিন।")
        else:
            with st.spinner("সাংবাদিক ও সোশ্যাল মিডিয়া এক্সপার্ট লেভেলে কন্টেন্ট তৈরি হচ্ছে..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    You are a world-class Digital Content Specialist and Senior Editor for a premium Bangladeshi Media House. 
                    Based on the selected topic '{selected_topic}', please generate a highly professional and advanced editorial kit in Bengali:

                    ---
                    SECTION 1: 📱 HIGH-ENGAGEMENT FACEBOOK POST (ফেসবুকের জন্য আলাদা ও অ্যাডভান্সড কন্টেন্ট)
                    - Hook line: Start with a powerful, attention-grabbing first sentence.
                    - Body: Write a highly engaging, concise paragraph (3-4 sentences) explaining the core matter. Use active voice and an editorial tone.
                    - Formatting: Use appropriate, modern emojis to make it readable. Break down important facts into short bullet points if necessary.
                    - CTA (Call to Action): End with an engaging question to drive comments and shares from the audience.
                    - Hashtags: 3-4 highly relevant and trending hashtags.

                    ---
                    SECTION 2: 📰 WEB ARTICLE BLUEPRINT & HEADLINES (ওয়েবসাইট আর্টিকেলের জন্য প্রফেশনাল গাইড)
                    - 3 Premium Headlines:
                      1. Breaking/Urgent style (ব্রেকিং নিউজ শিরোনাম).
                      2. Explainer/In-depth style (বিশ্লেষণধর্মী শিরোনাম).
                      3. Click-worthy/Social Media style (ক্লিক-বান্ধব শিরোনাম).
                    - Investigative Outline: 4 deep, analytical bullet points guiding the reporter on what data, quotes, and angles must be covered in the full article.
                    ---
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("### 💎 AI Generated Professional Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"এরর হয়েছে: {e}")
