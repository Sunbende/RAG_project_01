"""
基于Streamlit的文件上传应用
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService


# 网页标题
st.title("知识库更新服务")

# file_uploader
uploaded_file = st.file_uploader(
    "请上传您的文件",
    type=["txt"],
    accept_multiple_files=False,
)

# 通过session_state来存储上传的文件
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploaded_file is not None:
    # 提取文件的信息
    file_name = uploaded_file.name
    file_size = uploaded_file.size / 1024       # KB
    file_type = uploaded_file.type

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # 读取文件内容
    text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("上传中..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)
