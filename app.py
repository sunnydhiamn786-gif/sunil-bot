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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        ans = response.text

    st.chat_message("assistant").write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
