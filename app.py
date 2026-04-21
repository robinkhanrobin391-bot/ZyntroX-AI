import streamlit as st
import google.generativeai as genai

# प्रीमियम लुक और बटन छुपाने के लिए
st.set_page_config(page_title="ZyntroX AI", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 ZyntroX AI")
st.markdown("<p style='color: grey;'>Developed by Azam</p>", unsafe_allow_html=True)

# API सेटिंग
genai.configure(api_key="AIzaSyB1eRMb7zkS9eEWvE2F5-2pSCGzA3-dY0A")

# निर्देश और मॉडल
instruction = "तुम्हारा नाम ZyntroX है। तुम्हें Azam ने बनाया है। तुम हमेशा उन्हें 'मालिक' कहोगे।"
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("नमस्ते मालिक, कुछ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.warning("मालिक, Google की चाबी अभी एक्टिव हो रही है। 1 मिनट रुकें।")
