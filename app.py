import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
import google.generativeai as genai
import urllib.request
import xml.etree.ElementTree as ET

# ড্যাশবোর্ডের লেআউট সেটআপ
st.set_page_config(page_title="Media Trend Spotter Pro", layout="wide", page_icon="🔥")

st.title("🚀 সোশ্যাল মিডিয়া ও গুগল ট্রেন্ড স্পটার (Pro Version)")
st.markdown("### মিডিয়া হাউজের জন্য রিয়েল-টাইম ভাইরাল কনটেন্ট ড্যাশবোর্ড")
st.write("---")

# Gemini AI কনফিগারেশন
st.sidebar.header("🔑 AI Settings")
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# ১. গুগল ট্রেন্ডস ডাটা ফেচ করার ফাংশন
@st.cache_data(ttl=300)
def get_google_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='bangladesh')
        df.columns = ['আজকের ট্রেন্ডিং টপিকসমূহ']
        return df
    except Exception:
        return None

# ২. ফেসবুক ও সোশ্যাল মিডিয়া ব্রেকিং নিউজ স্ক্র্যাপ করার ফাংশন (RSS & Public Data Feed)
@st.cache_data(ttl=300)
def get_social_viral_trends():
    viral_topics = []
    # বাংলাদেশের শীর্ষস্থানীয় কিছু ভাইরাল নিউজ সোর্সের আরএসএস ফিড
    feeds = [
        "https://www.prothomalo.com/feed",
        "https://bangla.bdnews24.com/?widgetName=rssfeed&widgetId=1151",
        "https://www.banglanews24.com/rss/feeds/banglanews24.xml"
    ]
    
    for url in feeds:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read()
                root = ET.fromstring(html)
                for item in root.findall('.//item')[:5]: # প্রতি সাইট থেকে টপ ৫টি করে ব্রেকিং নিউজ নিবে
                    title = item.find('title').text
                    if title and title not in viral_topics:
                        viral_topics.append(title)
        except Exception:
            continue
            
    if len(viral_topics) > 0:
        return pd.DataFrame(viral_topics[:15], columns=['সোশ্যাল মিডিয়া ও ফেসবুক ভাইরাল নিউজ'])
    else:
        # ব্যাকআপ ফেসবুক ভাইরাল ডাটা
        return pd.DataFrame([
            "ঢাকায় তীব্র জানজট ও জনগণের ভোগান্তি",
            "সোশ্যাল মিডিয়ায় নতুন ভাইরাল ইস্যু ও ট্রোল",
            "বাংলাদেশ ক্রিকেট দলের আজকের ম্যাচ আপডেট",
            "বাজারে নিত্যপ্রয়োজনীয় পণ্যের দাম বৃদ্ধি নিয়ে ক্ষোভ"
        ], columns=['সোশ্যাল মিডিয়া ও ফেসবুক ভাইরাল নিউজ'])

# ডাটা লোড করা
google_df = get_google_trends()
social_df = get_social_viral_trends()

# ব্যাকআপ গুগল ডাটা
backup_google = pd.DataFrame([
    "বাংলাদেশ ব্রেকিং নিউজ", "আজকের আবহাওয়া ও বৃষ্টিপাত", 
    "সোশ্যাল মিডিয়া ভাইরাল টপিক", "চলতি সপ্তাহের টপ ট্রেন্ডস"
], columns=['আজকের ট্রেন্ডিং টপিকসমূহ'])

# ড্যাশবোর্ড লেআউট তৈরি (৩টি কলাম: গুগল ট্রেন্ড, ফেসবুক ট্রেন্ড, রাইটিং অ্যাসিস্ট্যান্ট)
col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("📈 গুগল ট্রেন্ডস (BD)")
    if google_df is not None and not google_df.empty:
        st.dataframe(google_df, use_container_width=True, height=450)
    else:
        st.warning("গুগল সার্ভার সাময়িক ব্যস্ত।")
        st.dataframe(backup_google, use_container_width=True)

with col2:
    st.header("📱 ফেসবুক ও সোশ্যাল ট্রেন্ড")
    st.dataframe(social_df, use_container_width=True, height=450)

with col3:
    st.header("✍️ এআই রাইটিং অ্যাসিস্ট্যান্ট")
    
    # দুটি টেবিলের ডাটা একসাথে করে ড্রপডাউন তৈরি করা
    g_list = google_df['আজকের ট্রেন্ডিং টপিকসমূহ'].tolist() if (google_df is not None and not google_df.empty) else backup_google['আজকের ট্রেন্ডিং টপিকসমূহ'].tolist()
    s_list = social_df['সোশ্যাল মিডিয়া ও ফেসবুক ভাইরাল নিউজ'].tolist()
    all_topics = list(set(g_list + s_list))
    
    selected_topic = st.selectbox("কোন ভাইরাল টপিকটি নিয়ে লিখতে চান?", all_topics)
    st.success(f"সিলেক্টেড: **{selected_topic}**")
    
    if st.button("প্রফেশনাল নিউজ আউটলাইন তৈরি করুন"):
        if not api_key:
            st.error("দয়া করে বামপাশের সাইডবারে আপনার Gemini API Key টি দিন।")
        else:
            with st.spinner("সাংবাদিকতার স্ট্যান্ডার্ড অনুযায়ী কনটেন্ট তৈরি হচ্ছে..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    You are a senior professional journalist and editor for a top Bangladeshi digital media house. 
                    Based on the trending/viral topic '{selected_topic}', please generate a highly professional and engaging editorial kit in Bengali:
                    
                    1. 💡 3 Premium News Headlines (১টি ব্রেকিং নিউজ স্টাইল, ১টি সাধারণ ইনফরমেটিভ, ১টি ফেসবুকের জন্য আকর্ষণীয় ক্লিকঅ্যাবল শিরোনাম).
                    2. 📝 Professional Facebook Post Caption (সাংবাদিকতার স্ট্যান্ডার্ড মেইনটেইন করে আকর্ষণীয় ইমোজি ও ট্রেন্ডিং হ্যাশট্যাগসহ একটি রেডি-টু-পোস্ট ক্যাপশন).
                    3. 📌 Investigative Article Outline/Bullet Points (এই খবরের ভেতরে একজন রিপোর্টারের কী কী গুরুত্বপূর্ণ তথ্য তুলে ধরা উচিত, তার ৪টি সুনির্দিষ্ট এবং গভীর পয়েন্ট).
                    
                    Ensure the Bengali tone is pristine, formal yet highly engaging for digital readers (Standard Sadhu/Cholit blend used in modern journalism).
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("### 🤖 AI Editor-in-Chief Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"এআই রেসপন্স তৈরি করতে পারেনি। এরর: {e}")
