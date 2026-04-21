import streamlit as st
import google.generativeai as genai
import PIL.Image

# Meta AI प्रीमियम डार्क लुक
st.set_page_config(page_title="ZyntroX AI", layout="centered")

st.markdown("""
    <style>
    /* पूरा बैकग्राउंड काला */
    .stApp {background-color: #000000;}
    
    /* टॉप टाइटिल Meta AI स्टाइल */
    .main-title {
        font-size: 42px; font-weight: bold; text-align: center; 
        color: white; margin-top: 60px; font-family: sans-serif;
    }
    .sub-title {text-align: center; color: #888; margin-bottom: 40px;}

    /* इनपुट बॉक्स को गोल और सुंदर बनाना */
    .stChatInput > div {
        border-radius: 35px !important; 
        background-color: #1c1c1e !important; 
        border: 1px solid #333 !important;
    }

    /* बटन्स को Meta AI जैसा लुक देना */
    div.stButton > button {
        border-radius: 25px; border: 1px solid #333; 
        background-color: transparent; color: white; 
        width: 100%; padding: 15px; text-align: left;
    }
    
    /* फालतू की चीजें छुपाना */
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}
    </style>
    """, unsafe_allow_html=True)
# API और पहचान सेटिंग
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
instruction = "तुम्हारा नाम ZyntroX है। तुम्हें Azam ने बनाया है। तुम हमेशा उन्हें 'मालिक' कहोगे।"
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)
# मुख्य स्क्रीन का लुक
st.markdown('<div class="main-title">What can I do for you?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Developed by Azam</div>', unsafe_allow_html=True)

# सजेशन बटन्स (Meta AI की तरह)
col1, col2 = st.columns(2)
with col1:
    if st.button("🎬 Animate my photo"): st.info("मालिक, यह जल्द आएगा!")
    if st.button("📚 Learn and grow"): st.info("मालिक, क्या सीखना चाहते हैं?")
with col2:
    if st.button("🎨 Create an image"): st.info("मालिक, मैं मदद कर सकता हूँ।")
    if st.button("🔍 Analyse for me"): st.info("मालिक, फोटो अपलोड करें।")
# चैट हिस्ट्री और मैसेजिंग
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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
            st.error("मालिक, सर्वर में कुछ गड़बड़ है।")
