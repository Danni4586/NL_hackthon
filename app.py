import time
import streamlit as st

st.set_page_config(page_title="MAIN Hackathon Demo", page_icon="⚡")
st.title("⚡ MAIN Hackathon AI Demo")

if "messages" not in st.session_state:
  st.session_state.messages = []

for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

if prompt := st.chat_input("输入你的测试问题或任务指令..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):

    def mock_stream():
      text = f"收到你的测试输入：「{prompt}」。当前为本地流式验证模式，Streamlit 交互与公网部署链路已就绪。"
      for ch in text:
        yield ch
        time.sleep(0.015)

    reply = st.write_stream(mock_stream())
    st.session_state.messages.append({"role": "assistant", "content": reply})