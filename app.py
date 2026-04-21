import streamlit as st
import google.generativeai as genai

# Meta AI जैसा प्रीमियम लुक देने के लिए CSS
st.set_page_config(page_title="ZyntroX AI", layout="centered")

st.markdown("""
    <style>
    /* बैकग्राउंड और फालतू चीजें छुपाने के लिए */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* मेन टाइटल (What can I do for you?) */
    .main-title {
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        margin-top: 60px;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* इनपुट बॉक्स को Meta AI जैसा गोल बनाने के लिए */
    .stChatInputContainer {
        padding-bottom: 30px;
    }
    .stChatInput > div {
        border-radius: 35px !important;
        background-color: #252525 !important;
        border: 1px solid #333 !important;
    }
    
    /* सजेशन बटन्स की स्टाइल (Meta AI स्टाइल) */
    div.stButton > button {
        border-radius: 25px;
        border: 1px solid #333;
        background-color: transparent;
        color: white;
        width: 100%;
        text-align: left;
        padding: 12px 20px;
        margin-bottom: 10px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #252525;
        border: 1px solid #A855F7;
    }
    </style>
    """, unsafe_allow_html=True)

# API सेटिंग (आपकी चाबी यहाँ है)
genai.configure(api_key="AIzaSyAL50NrdiVLuRnQQqeOhJhD-Ag-kjUr0WI")

# निर्देश और मॉडल सेटिंग
instruction = "तुम्हारा नाम ZyntroX है। तुम्हें Azam ने बनाया है। तुम हमेशा उन्हें 'मालिक' कहोगे।"
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash', system_instruction=instruction)

# स्वागत संदेश
st.markdown('<div class="main-title">What can I do for you?</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey; margin-bottom: 30px;'>Developed by Azam</p>", unsafe_allow_html=True)

# सजेशन बटन्स (Meta AI की तरह)
col1, col2 = st.columns(2)
with col1:
    if st.button("🎬 Animate my photo"):
        st.info("मालिक, एनीमेशन फीचर जल्द ही आएगा!")
    if st.button("📚 Learn and grow"):
        st.info("मालिक, आप क्या नया सीखना चाहते हैं?")
with col2:
    if st.button("🎨 Create an image"):
        st.info("मालिक, मैं इमेज प्रोम्प्ट लिखने में मदद कर सकता हूँ।")
    if st.button("🔍 Analyse for me"):
        st.info("मालिक, कुछ भी लिख कर भेजें, मैं उसे एनालाइज करूँगा।")

# चैट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# चैट इनपुट
if prompt := st.chat_input("Ask ZyntroX AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"मालिक, यह एरर आ रहा है: {e}")
