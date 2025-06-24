import streamlit as st
from agents import GaurdAgent, DetailsAgent

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gaurd_agent" not in st.session_state:
    st.session_state.gaurd_agent = GaurdAgent()
if "details_agent" not in st.session_state:
    st.session_state.details_agent = DetailsAgent()
if "show_sources" not in st.session_state:
    st.session_state.show_sources = True

st.set_page_config(page_title="Agent Chat", layout="centered")
st.title("🛡️ Guarded Agent Chat")

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages.clear()
        st.rerun()

with col2:
    st.session_state.show_sources = st.checkbox("Show Source Knowledge", value=st.session_state.show_sources)

# Display previous messages
st.markdown("### Conversation")
for msg in st.session_state.messages:
    if isinstance(msg, dict):
        role = msg.get("role", "agent").capitalize()
        content = msg.get("content", "")
        st.markdown(f"**{role}:** {content}")
        if st.session_state.show_sources and msg.get("source_knowledge"):
            st.markdown(f"<div style='font-size: 0.9em; color: gray;'>🔍 **Source:** {msg['source_knowledge']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"**User:** {msg}")

# Input box
user_input = st.text_input("Type your message", key="user_input")

if st.button("Send") and user_input.strip():
    st.session_state.messages.append(user_input)

    gaurd_response = st.session_state.gaurd_agent.get_response(st.session_state.messages)

    if gaurd_response["memory"]["gaurd_decision"] == "not allowed":
        st.session_state.messages.append({
            "role": "guard_agent",
            "content": gaurd_response.get("content", "Your message was blocked by the guard.")
        })
    else:
        response_dict, source_knowledge = st.session_state.details_agent.get_response(st.session_state.messages)
        st.session_state.messages.append({
            "role": response_dict.get("role", "assistant"),
            "content": response_dict.get("content", ""),
            "source_knowledge": source_knowledge
        })

    st.rerun()
