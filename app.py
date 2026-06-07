import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time

# ড্যাশবোর্ডের লেআউট সেটআপ
st.set_page_config(page_title="Media Trend Spotter", layout="wide", page_icon="🔥")

st.title("🇧🇩 সোশ্যাল মিডিয়া ট্রেন্ড স্পটার")
st.markdown("### মিডিয়া হাউজের রাইটারদের জন্য লাইভ ড্যাশবোর্ড")
st.write("---")

# ডাটা ফেচ করার ফাংশন (Retry Mechanism সহ)
@st.cache_data(ttl=300)
def get_bangladesh_trends():
    # প্রথম চেষ্টা: অফিশিয়াল মেথড
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        df = pytrends.trending_searches(pn='bangladesh')
        df.columns = ['আজকের ট্রেন্ডিং টপিকসমূহ']
        return df
    except Exception:
        # দ্বিতীয় চেষ্টা: যদি গুগল ব্লক করে, তবে একটু ভিন্নভাবে চেষ্টা করবে
        try:
            time.sleep(2)
            pytrends = TrendReq(hl='bn-BD', tz=360, timeout=(10,25))
            df = pytrends.realtime_trending_searches(pn='BD')
            # ডাটা ফরম্যাট ঠিক করা
            topics = []
            for index, row in df.iterrows():
                topics.extend(row['title'].split(','))
            clean_df = pd.DataFrame(list(set(topics))[:20], columns=['আজকের ট্রেন্ডিং টপিকসমূহ'])
            return clean_df
        except Exception:
            return None

# ডাটা লোড করা
trends_df = get_bangladesh_trends()

# স্ক্রিনটিকে দুটি ভাগে ভাগ করা
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("📈 গুগল ট্রেন্ডস (বাংলাদেশ)")
    if trends_df is not None and not trends_df.empty:
        st.dataframe(trends_df, use_container_width=True, height=450)
    else:
        # যদি কোনোভাবেই ডাটা না আসে, রাইটারদের সাময়িক আইডিয়া দেওয়ার জন্য কিছু ব্যাকআপ ট্রেন্ড
        st.warning("গুগল সার্ভার সাময়িক ব্যস্ত। নিচে কিছু সম্ভাব্য লাইভ টপিক দেওয়া হলো:")
        backup_data = pd.DataFrame([
            "বাংলাদেশ ব্রেকিং নিউজ", "আজকের আবহাওয়া ও বৃষ্টিপাত", 
            "সোশ্যাল মিডিয়া ভাইরাল টপিক", "চলতি সপ্তাহের টপ ট্রেন্ডস"
        ], columns=['আজকের ট্রেন্ডিং টপিকসমূহ'])
        st.dataframe(backup_data, use_container_width=True)

with col2:
    st.header("✍️ রাইটিং অ্যাসিস্ট্যান্ট")
    
    # ডাটা সোর্স সিলেক্ট করা
    current_df = trends_df if (trends_df is not None and not trends_df.empty) else backup_data
    
    selected_topic = st.selectbox("কোন টপিকটি নিয়ে লিখতে চান?", current_df['আজকের ট্রেন্ডিং টপিকসমূহ'])
    st.success(f"আপনি সিলেক্ট করেছেন: **{selected_topic}**")
    
    if st.button("আইডিয়া এবংアウトলাইন তৈরি করুন"):
        st.info(f"'{selected_topic}' নিয়ে দ্রুত লেখার জন্য একটি খসড়া তৈরি হচ্ছে...")
