import streamlit as st
import google.generativeai as genai
import PIL.Image

st.set_page_config(page_title="Meta AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {background-color: #0b0b0b;}
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}
    
    /* टॉप बार स्टाइल */
    .top-header {display: flex; justify-content: space-between; align-items: center; padding: 10px; margin-bottom: 20px;}
    .meta-logo {font-size: 22px; font-weight: bold; color: white; font-family: sans-serif;}
    .glasses-btn {background: #1c1c1e; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; border: 1px solid #333;}

    /* सजेशन बटन्स (बैंगनी आइकन के साथ) */
    div.stButton > button {
        border-radius: 25px; border: 1px solid #333; background-color: #121212; 
        color: white; padding: 10px 20px; margin-bottom: 10px; width: 80%; text-align: left;
    }

    /* प्लस और इनपुट बार का असली जुगाड़ */
    .stChatInputContainer {padding-bottom: 20px;}
    .stChatInput > div {
        border-radius: 20px !important; background-color: #1c1c1e !important; border: none !important;
    }
    
    /* साइडबार डार्क */
    [data-testid="stSidebar"] {background-color: #000000 !important;}
    </style>
    """, unsafe_allow_html=True)
# टॉप मेन्यू (Left Side)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Settings</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# Meta AI हेडर
st.markdown("""
    <div class="top-header">
        <div class="meta-logo">Meta AI</div>
        <div class="glasses-btn">🕶️ Glasses</div>
    </div>
    """, unsafe_allow_html=True)

# होम स्क्रीन बटन्स
st.button("🎬 Animate my photo")
st.button("🎨 Create an image")
st.button("📚 Learn and grow")
st.button("💡 Analyse for me")

# --- प्लस (+) बटन जो बिल्कुल इनपुट बार के पास रहेगा ---
with st.popover("➕"):
    st.write("### मीडिया")
    uploaded_file = st.file_uploader("गैलरी", type=["jpg","png","jpeg"], label_visibility="collapsed")
    cam_file = st.camera_input("कैमरा", label_visibility="collapsed")

# AI पहचान
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
model = genai.GenerativeModel('gemini-1.5-flash')
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# असली इनपुट बार
if prompt := st.chat_input("Ask Meta AI..."):
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
        except: st.error("कनेक्शन धीमा है!")
