import streamlit as st
from chatbot import EcoGenieBot


@st.cache_resource
def load_chatbot():
    return EcoGenieBot()


st.set_page_config(page_title="EcoGenieBot", page_icon="🌱")
st.title("EcoGenieBot")
st.caption("A small intent-based chatbot for sustainability and green technology topics.")

chatbot = load_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me about sustainability or green technology."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about sustainability"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = chatbot.respond(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
