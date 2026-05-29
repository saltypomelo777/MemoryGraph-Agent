import streamlit as st

# 1. 页面基本配置（让它适配手机屏幕和浏览器）
st.set_page_config(page_title="MemoryGraph", page_icon="🧠", layout="centered")

st.title("🧠 MemoryGraph 第二大脑")
st.caption("全渠道碎片化知识主动型自组织 Agent 系统")

# 2. 初始化一个“聊天记录列表”（相当于C语言里的结构体数组，用来存历史对话）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "嘿，我是你的 MemoryGraph 助理。今天在 B站 或小红书刷到了什么硬核干货？直接把链接发给我吧！"}
    ]

# 3. 遍历并渲染历史聊天气泡（Streamlit 自带的高仿微信气泡组件）
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. 接收手机端/网页端的输入框
if user_input := st.chat_input("随手记点什么，或者粘贴B站/小红书链接..."):
    # 在屏幕上立刻显示用户说的话
    with st.chat_message("user"):
        st.write(user_input)
    # 把用户的话追加到历史数组里
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 模拟大模型给你的回应（我们后面会把 DeepSeek 脑子缝合到这里）
    with st.chat_message("assistant"):
        st.write(f"（系统已拦截到输入）我已收到你的碎片信息：'{user_input}'。正在后台提取语义标签并尝试与你的历史知识库连线织网...")