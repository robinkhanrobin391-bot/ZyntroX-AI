import streamlit as st
import google.generativeai as genai

# प्रीमियम लुक और बटन छुपाने के लिए
st.set_page_config(page_title="ZyntroX AI", layout="centered")
st.markdown("""
    <style>
    #<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #121212;}
    .stChatInput > div {border-radius: 35px !important; background-color: #252525 !important;}
    div.stButton > button {border-radius: 25px; border: 1px solid #444; background: transparent; color: white; width: 100%;}
    .stTitle {font-size: 35px !important; text-align: center;}
</style>


st.title("🤖 ZyntroX AI")
st.markdown("<p style='color: grey;'>Developed by Azam</p>", unsafe_allow_html=True)

# API सेटिंग
genai.configure(api_key="AIzaSyAL50NrdiVLuRmQQqEohJhD-Ag-kjUr0WI") 

# निर्देश और मॉडल
instruction = "तुम्हारा नाम ZyntroX है। तुम्हें Azam ने बनाया है। तुम हमेशा उन्हें 'मालिक' कहोगे।"
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash', system_instruction=instruction)


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
 
        except Exception as e:
            st.error(f"मालिक, यह एरर आ रहा है: {e}")
