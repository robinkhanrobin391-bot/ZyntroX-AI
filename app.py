import streamlit as st
import google.generativeai as genai
import PIL.Image

# 1. पेज सेटअप और ZyntroX ब्रैंडिंग
st.set_page_config(page_title="ZyntroX AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {background-color: #0b0b0b;}
    header, footer, .stDeployButton {visibility: hidden; display: none !important;}
    
    /* टॉप हेडर जहाँ आपका नाम रहेगा */
    .top-header {display: flex; justify-content: space-between; align-items: center; padding: 10px; margin-bottom: 20px;}
    .zyntrox-logo {font-size: 24px; font-weight: bold; color: white; font-family: sans-serif; letter-spacing: 1px;}
    .glasses-btn {background: #1c1c1e; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; border: 1px solid #333;}

    /* सजेशन बटन्स स्टाइल */
    div.stButton > button {
        border-radius: 25px; border: 1px solid #333; background-color: #121212; 
        color: white; padding: 12px 20px; margin-bottom: 10px; width: 85%; text-align: left;
    }

    /* प्लस आइकन को चैट बार के पास सेट करना */
    div[data-testid="stVerticalBlock"] > div:has(div.stPopover) {
        position: fixed; bottom: 95px; left: 15px; z-index: 1000;
    }
    
    /* चैट इनपुट को प्लस के लिए खिसकाना */
    .stChatInput > div {
        margin-left: 55px !important; border-radius: 25px !important; background-color: #1c1c1e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. साइडबार मेन्यू (सेटिंग्स के लिए)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>ZyntroX Menu</h2>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# 3. ZyntroX हेडर (Glasses बटन के साथ)
st.markdown("""
    <div class="top-header">
        <div class="zyntrox-logo">ZyntroX AI</div>
        <div class="glasses-btn">🕶️ Glasses</div>
    </div>
    """, unsafe_allow_html=True)

# होम स्क्रीन के फीचर्स
st.button("🎬 Animate my photo")
st.button("🎨 Create an image")
st.button("📚 Learn and grow")
st.button("💡 Analyse for me")

# 4. प्लस (+) बटन (कैमरा और गैलरी के लिए)
with st.popover("➕"):
    st.write("### Media Selection")
    uploaded_file = st.file_uploader("Gallery", type=["jpg","png","jpeg","mp4"], label_visibility="collapsed")
    cam_file = st.camera_input("Camera", label_visibility="collapsed")

# 5. AI सेटअप और चैट लॉजिक
genai.configure(api_key="AIzaSyB2E2HL2Ky6RUddNzJ_vuO-hpw9BG-d8DA")
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask ZyntroX AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # फोटो या टेक्स्ट इनपुट संभालना
            input_content = [prompt, PIL.Image.open(uploaded_file if uploaded_file else cam_file)] if (uploaded_file or cam_file) else prompt
            res = model.generate_content(input_content)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except: st.error("मालिक, कनेक्शन में दिक्कत आ रही है।")
