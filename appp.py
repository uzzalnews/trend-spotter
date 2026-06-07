import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# ড্যাশবোর্ডের লেআউট সেটআপ
st.set_page_config(page_title="Media Trend Spotter", layout="wide", page_icon="🔥")

st.title("🇧🇩 সোশ্যাল মিডিয়া ট্রেন্ড স্পটার")
st.markdown("### মিডিয়া হাউজের রাইটারদের জন্য লাইভ ড্যাশবোর্ড")
st.write("---")

# ৫ মিনিট পর পর ডাটা অটো রিফ্রেশ করার জন্য ক্যাশ (Cache) মেমোরি ব্যবহার
@st.cache_data(ttl=300)
def get_bangladesh_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        df = pytrends.trending_searches(pn='bangladesh')
        df.columns = ['আজকের ট্রেন্ডিং টপিকসমূহ']
        return df
    except Exception as e:
        return None

# ডাটা লোড করা
trends_df = get_bangladesh_trends()

# স্ক্রিনটিকে দুটি ভাগে ভাগ করা (বাম পাশ এবং ডান পাশ)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("📈 গুগল ট্রেন্ডস (বাংলাদেশ)")
    if trends_df is not None:
        st.dataframe(trends_df, use_container_width=True, height=400)
    else:
        st.error("গুগল থেকে ডাটা আনতে সমস্যা হচ্ছে। একটু পর আবার চেষ্টা করুন।")

with col2:
    st.header("✍️ রাইটিং অ্যাসিস্ট্যান্ট")
    if trends_df is not None:
        selected_topic = st.selectbox("কোন টপিকটি নিয়ে লিখতে চান?", trends_df['আজকের ট্রেন্ডিং টপিকসমূহ'])
        st.success(f"আপনি সিলেক্ট করেছেন: **{selected_topic}**")
        
        if st.button("আইডিয়া এবং আউটলাইন তৈরি করুন"):
            st.info(f"'{selected_topic}' নিয়ে দ্রুত লেখার জন্য একটি খসড়া তৈরি হচ্ছে...")
