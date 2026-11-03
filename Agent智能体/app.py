import time

import streamlit as st
from agent.react_agent import ReactAgent

# 标题
st.title("智扫通机器人智能客服")
st.divider()

# 初始化智能体（session_state全局缓存，避免重复实例化）
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 初始化聊天历史记录
if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:

    st.chat_message(message['role']).write(message['content'])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    # 渲染用户消息
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 加载模型流式回复
    response_message = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture_output(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char
        st.chat_message("assistant").write(capture_output(res_stream,response_message))
        st.session_state["message"].append({"role": "assistant", "content": response_message[-1]})
        st.rerun()