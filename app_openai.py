import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

st.set_page_config(page_title="MAIN Hackathon App", page_icon="⚡")
st.title("⚡ MAIN Hackathon AI App")

api_key = None
try:
  if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
  pass

if not api_key:
  api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
  st.error("未检测到 OPENAI_API_KEY，请在 .env 或 Streamlit Secrets 中配置。")
  st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
  st.session_state.messages = []

for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

if prompt := st.chat_input("输入你的问题或任务..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    try:
      stream = client.responses.create(
          model="gpt-4o-mini",
          input=[
              {
                  "role": "system",
                  "content": "你是一个简洁、高效的 Hackathon AI 助手。",
              },
              *st.session_state.messages,
          ],
          stream=True,
      )

      def token_generator():
        for event in stream:
          if event.type == "response.output_text.delta":
            yield event.delta

      reply = st.write_stream(token_generator())
      st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
      st.warning(f"API 调用异常（{type(e).__name__}）：{e}")