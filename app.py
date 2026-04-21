import streamlit as st
import google.generativeai as genai
import PIL.Image
from gtts import gTTS
import base64
import os

st.set_page_config(page_title="ZyntroX AI", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    footer, header, .stDeployButton {visibility: hidden; display: none !important;}
    .stApp {background-color: #000000;}
    section[data-testid="stSidebar"] {background-color: #121212 !important; border-right: 1px solid #333;}
    .main-title {font-size: 38px; font-weight: bold; text-align: center; color: white; margin-top: 30px;}
    .stChatInput > div {border-radius: 35px !important; background-color: #1c1e21 !important; border: 1px solid #333 !important;}
    div.stButton > button {border-radius: 25px; border: 1px solid #333; background: transparent; color: white; width: 100%; text-align: left;}
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
instruction = "तुम ZyntroX AI हो जिसे Azam ने बनाया है। तुम उन्हें मालिक कहोगे।"
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>ZyntroX Menu</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    uploaded_file = st.file_uploader("➕ Upload Photo", type=["jpg", "png", "jpeg"])
    st.markdown("<p style='color: #888;'>Developed by Azam</p>", unsafe_allow_html=True)

st.markdown('<div class="main-title">What can I do for you?</div>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])
def speak(text):
    tts = gTTS(text=text[:500], lang='hi')
    tts.save("v.mp3")
    with open("v.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask ZyntroX AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            content = [prompt, PIL.Image.open(uploaded_file)] if uploaded_file else prompt
            response = model.generate_content(content)
            st.markdown(response.text)
            if st.button("🔊 Listen"): speak(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e: st.error("मालिक, कनेक्शन एरर है।")
