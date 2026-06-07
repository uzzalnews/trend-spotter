import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
import google.generativeai as genai

# ড্যাশবোর্ডের লেআউট সেটআপ
st.set_page_config(page_title="Media Trend Spotter", layout="wide", page_icon="🔥")

st.title("🇧🇩 সোশ্যাল মিডিয়া ট্রেন্ড স্পটার")
st.markdown("### মিডিয়া হাউজের রাইটারদের জন্য লাইভ ড্যাশবোর্ড")
st.write("---")

# Gemini AI কনফিগারেশন (আপনার এপিআই কি এখানে বসাবেন)
# সুরক্ষার জন্য সরাসরি কোডে না বসিয়ে নিচে st.text_input দিয়েছি যেন আপনি ড্যাশবোর্ড থেকেই কি দিতে পারেন
st.sidebar.header("🔑 AI settings")
api_key = st.sidebar.text_input("Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# ডাটা ফেচ করার ফাঞ্চন
@st.cache_data(ttl=300)
def get_bangladesh_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='bangladesh')
        df.columns = ['আজকের ট্রেন্ডিং টপিকসমূহ']
        return df
    except Exception:
        return None

# ডাটা লোড করা
trends_df = get_bangladesh_trends()

# ব্যাকআপ ডাটা তৈরি
backup_data = pd.DataFrame([
    "বাংলাদেশ ব্রেকিং নিউজ", "আজকের আবহাওয়া ও বৃষ্টিপাত", 
    "সোশ্যাল মিডিয়া ভাইরাল টপিক", "চলতি সপ্তাহের টপ ট্রেন্ডস"
], columns=['আজকের ট্রেন্ডিং টপিকসমূহ'])

col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("📈 গুগল ট্রেন্ডস (বাংলাদেশ)")
    if trends_df is not None and not trends_df.empty:
        st.dataframe(trends_df, use_container_width=True, height=450)
    else:
        st.warning("গুগল সার্ভার সাময়িক ব্যস্ত। নিচে কিছু সম্ভাব্য লাইভ টপিক দেওয়া হলো:")
        st.dataframe(backup_data, use_container_width=True)

with col2:
    st.header("✍️ রাইটিং অ্যাসিস্ট্যান্ট")
    current_df = trends_df if (trends_df is not None and not trends_df.empty) else backup_data
    
    selected_topic = st.selectbox("কোন টপিকটি নিয়ে লিখতে চান?", current_df['আজকের ট্রেন্ডিং টপিকসমূহ'])
    st.success(f"আপনি সিলেক্ট করেছেন: **{selected_topic}**")
    
    if st.button("আইডিয়া এবং আউটলাইন তৈরি করুন"):
        if not api_key:
            st.error("দয়া করে বামপাশের সাইডবারে আপনার Gemini API Key টি দিন।")
        else:
            with st.spinner("এআই (AI) আপনার জন্য কনটেন্ট আউটলাইন তৈরি করছে..."):
                try:
                    # Gemini মডেল কল করা
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    You are an expert journalist for a Bangladeshi digital media house. 
                    Based on the trending topic '{selected_topic}', please generate the following in Bengali:
                    1. 3 Catchy and Clickable News Headlines (আকর্ষণীয় শিরোনাম).
                    2. A short Facebook post caption with relevant hashtags (সোশ্যাল মিডিয়া ক্যাপশন).
                    3. 4 Main bullet points explaining what should be covered in this article (আর্টিকেলের মূল বিষয়বস্তু).
                    Keep the tone professional yet engaging.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("### 🤖 AI Generated Content Blueprint:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"এআই রেসপন্স তৈরি করতে পারেনি। এরর: {e}")
