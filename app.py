import streamlit as st
import google.generativeai as genai
import PIL.Image

st.set_page_config(page_title="ZyntroX AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {background-color: #000000;}
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}
    
    /* नमस्ते टाइटिल स्टाइल */
    .welcome-text {font-size: 30px; font-weight: bold; color: white; margin-bottom: 5px;}
    .sub-welcome {font-size: 24px; color: white; margin-bottom: 25px;}

    /* गोल मेन्यू बटन्स */
    div.stButton > button {
        border-radius: 20px; border: 1px solid #333; background-color: #1a1a1a; 
        color: white; padding: 10px 18px; margin-bottom: 10px; font-size: 14px;
    }

    /* नीचे का प्लस और इनपुट बार साथ-साथ */
    .media-container {
        position: fixed; bottom: 85px; width: 100%; max-width: 700px;
        background: transparent; z-index: 999;
    }
    
    .stChatInputContainer {padding-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)
# टॉप लेफ्ट मेन्यू
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Settings</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# AI पहचान
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
model = genai.GenerativeModel('gemini-1.5-flash')

# होम स्क्रीन लुक (Gemini Style)
st.markdown('<div class="welcome-text">नमस्ते, Azam!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-welcome">कहाँ से शुरुआत करें?</div>', unsafe_allow_html=True)

# वो चार संगीत/इमेज वाले बटन
if st.button("🖼️ इमेज बनाएँ"): st.toast("Coming soon!")
if st.button("🎸 संगीत बनाएँ"): st.toast("Soon!")
if st.button("📚 कुछ सीखने में मदद करो"): st.toast("क्या सीखना है?")
if st.button("📄 कुछ भी लिखें"): st.toast("लिखना शुरू करें!")

# --- असली 'Gemini' वाला प्लस सेटअप ---
# इसे हम इनपुट बार के ठीक बगल में जैसा लुक देने के लिए पॉपओवर यूज़ कर रहे हैं
st.write("") 
with st.popover("➕"):
    st.write("### मीडिया जोड़ें")
    uploaded_file = st.file_uploader("📁 गैलरी", type=["jpg","png","jpeg","mp4"], label_visibility="collapsed")
    cam_file = st.camera_input("📸 कैमरा", label_visibility="collapsed")
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# चैट इनपुट बार
if prompt := st.chat_input("ZyntroX से पूछें"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                res = model.generate_content([prompt, PIL.Image.open(uploaded_file)])
            elif cam_file:
                res = model.generate_content([prompt, PIL.Image.open(cam_file)])
            else:
                res = model.generate_content(prompt)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except: st.error("कनेक्शन धीमा है, मालिक!")
