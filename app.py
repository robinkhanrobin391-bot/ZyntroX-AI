import streamlit as st
import google.generativeai as genai
import PIL.Image

# Meta AI लुक की सेटिंग
st.set_page_config(page_title="ZyntroX AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {background-color: #000000;}
    footer, header, .stDeployButton {visibility: hidden; display: none !important;}
    .main-title {font-size: 38px; font-weight: bold; text-align: center; color: white; margin-top: 50px; font-family: sans-serif;}
    .sub-title {text-align: center; color: #888; font-size: 14px; margin-bottom: 30px;}
    
    /* इनपुट बॉक्स और साइड के बटन */
    .stChatInput {padding-bottom: 20px;}
    .stChatInput > div {border-radius: 35px !important; background-color: #1c1c1e !important; border: 1px solid #333 !important;}
    
    /* बटन स्टाइल */
    div.stButton > button {border-radius: 25px; border: 1px solid #333; background: transparent; color: white; width: 100%; text-align: left; padding: 12px 20px;}
    
    /* साइडबार डार्क थीम */
    [data-testid="stSidebar"] {background-color: #121212 !important; border-right: 1px solid #333;}
    </style>
    """, unsafe_allow_html=True)

# सेटिंग मेन्यू (लेफ्ट साइड में)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Settings</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.markdown("<p style='color: #888;'>ZyntroX v2.0</p>", unsafe_allow_html=True)
# AI सेटअप
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
model = genai.GenerativeModel('gemini-1.5-flash')

# मुख्य स्क्रीन
st.markdown('<div class="main-title">What can I do for you?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Developed by Azam</div>', unsafe_allow_html=True)

# मीडिया अपलोड (कैमरा और फोटो के लिए)
col_media, col_cam = st.columns(2)
with col_media:
    uploaded_file = st.file_uploader("➕ फोटो/वीडियो जोड़ें", type=["jpg", "png", "jpeg", "mp4"])
with col_cam:
    cam_file = st.camera_input("📸 कैमरा खोलें")

# सजेशन बटन्स
c1, c2 = st.columns(2)
with c1:
    st.button("🎬 Animate my photo")
    st.button("📚 Learn and grow")
with c2:
    st.button("🎨 Create an image")
    st.button("🔍 Analyse for me")
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask ZyntroX AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # अगर कैमरा या फोटो इस्तेमाल हुई है
            final_input = prompt
            if uploaded_file:
                final_input = [prompt, PIL.Image.open(uploaded_file)]
            elif cam_file:
                final_input = [prompt, PIL.Image.open(cam_file)]
                
            response = model.generate_content(final_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("मालिक, फाइल पढ़ने में दिक्कत आ रही है।")
