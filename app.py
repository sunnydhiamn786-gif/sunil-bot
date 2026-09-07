import streamlit as st
from google import genai

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Sunil's Bot")
st.title("🤖 Sunil's Data Analyst Bot")
st.write("Mujhe Data Analyst banne ka roadmap pucho!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Kuch bhi pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Soch raha hu..."):
        try:
            # Pehle naya model try karega, fail hua to purana
            models_to_try = ["gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash"]
            ans = None
            for m in models_to_try:
                try:
                    response = client.models.generate_content(model=m, contents=prompt)
                    ans = response.text
                    break
                except:
                    continue
            
            if not ans:
                ans = "Google ka server busy hai, 1 min baad fir try karo."
        except Exception as e:
            ans = f"Error: {e}"

    st.chat_message("assistant").write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
