import streamlit as st
import google.generativeai as genai
import PIL.Image

st.set_page_config(page_title="ZyntroX AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {background-color: #000000;}
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}
    
    /* ऊपर का मेन्यू बटन और टाइटिल */
    .top-bar {display: flex; align-items: center; padding: 10px; color: white;}
    .main-title {font-size: 32px; font-weight: bold; color: white; margin-top: 20px; font-family: sans-serif;}

    /* जेमिनी स्टाइल गोल बटन */
    div.stButton > button {
        border-radius: 20px; border: 1px solid #333; background-color: #1a1a1a; 
        color: white; width: fit-content; padding: 10px 20px; margin-bottom: 10px;
    }

    /* नीचे का चैट बार (Gemini स्टाइल) */
    .stChatInputContainer {padding-bottom: 20px;}
    .stChatInput > div {
        border-radius: 30px !important; background-color: #1e1e1e !important; border: none !important;
    }
    
    /* साइडबार (History Menu) */
    [data-testid="stSidebar"] {background-color: #121212 !important; border-right: 1px solid #333;}
    </style>
    """, unsafe_allow_html=True)
# लेफ्ट साइड ऊपर कोर्नर में मेन्यू (History/Settings)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>ZyntroX Menu</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.markdown("<p style='color:gray;'>History & Settings</p>", unsafe_allow_html=True)

# AI पहचान
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
model = genai.GenerativeModel('gemini-1.5-flash')

# होम स्क्रीन का लुक (बिल्कुल जेमिनी जैसा)
st.markdown(f'<div class="main-title">नमस्ते, Azam!</div>', unsafe_allow_html=True)
st.markdown("<h2 style='color:white; font-size:28px;'>कहाँ से शुरुआत करें?</h2>", unsafe_allow_html=True)

# वो 4 बटन जो आपको चाहिए थे
if st.button("🖼️ इमेज बनाएँ"): st.toast("Coming soon!")
if st.button("🎸 संगीत बनाएँ"): st.toast("Music mode coming soon!")
if st.button("📚 कुछ सीखने में मेरी मदद करो"): st.toast("मालिक, क्या सीखना है?")
if st.button("📄 कुछ भी लिखें"): st.toast("लिखना शुरू कीजिये!")
# प्लस बटन के अंदर कैमरा और गैलरी
with st.expander("➕ Plus Menu (Camera, Gallery, Video)"):
    c1, c2 = st.columns(2)
    with c1: uploaded_file = st.file_uploader("📁 गैलरी", type=["jpg","png","jpeg"])
    with c2: cam_file = st.camera_input("📸 कैमरा")

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# चैट इनपुट
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
        except: st.error("कनेक्शन धीमा है, मालिक।")
