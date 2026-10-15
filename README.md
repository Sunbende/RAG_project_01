# 简易 RAG 智能客服系统

一个基于 LangChain + ChromaDB + Streamlit 的轻量级检索增强生成（RAG）示例项目，演示了从知识库构建、向量检索到多轮对话问答的完整流程。

## 功能特性

- **知识库管理**：通过 Web 页面上传 `.txt` 文本文件，自动切分、向量化并持久化到 ChromaDB
- **内容去重**：基于 MD5 校验，避免同一文本重复入库
- **语义检索**：使用 DashScope Embedding 模型进行相似度检索
- **多轮对话**：基于文件存储的对话历史，支持带上下文的连续问答
- **流式输出**：回答内容支持流式展示，提升交互体验

## 项目结构

```
RAG_project_01/
├── app.file.uploader.py   # 知识库上传页面（Streamlit）
├── app_qa.py              # 智能客服问答页面（Streamlit）
├── config_data.py         # 全局配置（模型、分块、检索参数等）
├── file_history_store.py  # 对话历史文件存储
├── knowledge_base.py      # 知识库服务（文本切分、向量化入库）
├── rag.py                 # RAG 核心链路（检索 + 生成 + 历史）
├── vector_stores.py       # 向量存储与检索器封装
├── data/                  # 示例知识库文本
├── chroma_db/             # ChromaDB 持久化目录（自动生成）
├── chat_history/          # 对话历史存储目录（自动生成）
└── md5.txt                # 已入库文本的 MD5 记录（自动生成）
```

## 技术栈

- Python 3.13
- LangChain（Chain 编排、Prompt、消息历史）
- ChromaDB（本地向量数据库）
- DashScope / 通义千问（`text-embedding-v4` 嵌入、`qwen-plus` 对话）
- Streamlit（Web 界面）

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境（可选）
python -m venv .venv

# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\Activate.ps1

# 安装依赖
pip install langchain langchain-chroma langchain-community chromadb streamlit dashscope
```

### 2. 配置 API Key

本项目依赖阿里云 DashScope 服务，需要设置 API Key 环境变量：

```powershell
# Windows PowerShell
$env:DASHSCOPE_API_KEY="你的API Key"

# Linux/macOS
export DASHSCOPE_API_KEY="你的API Key"
```

> 也可在代码中直接传入 `api_key` 参数，但建议通过环境变量管理。

### 3. 启动知识库上传服务

```bash
streamlit run app.file.uploader.py
```

打开浏览器访问终端提示的地址（默认 `http://localhost:8501`），上传 `.txt` 文件构建知识库。

### 4. 启动智能问答服务

```bash
streamlit run app_qa.py
```

在页面下方输入问题，系统会结合知识库内容和历史对话生成回答。

## 配置说明

所有可调参数集中在 [config_data.py](file:///d:/Profession/Python/Resource/RAG_project_01/config_data.py) 中：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `collection_name` | `"rag"` | ChromaDB 集合名称 |
| `persist_directory` | `"./chroma_db"` | 向量数据库持久化路径 |
| `chunk_size` | `1000` | 文本切分块大小 |
| `chunk_overlap` | `100` | 相邻文本块重叠长度 |
| `similarity_threshold` | `2` | 检索返回的文档数量 |
| `embedding_model` | `"text-embedding-v4"` | DashScope 嵌入模型 |
| `chat_model_name` | `"qwen-plus"` | 通义千问对话模型 |
| `session_config` | `user_001` | 默认会话 ID |

## 使用示例

项目内置了服装类示例知识库（`data/` 目录），可测试以下问题：

- "针织毛衣如何保养？"
- "我的体重140斤，尺码推荐"
- "这件衣服有哪些颜色可选？"

## 注意事项

1. 当前仅支持 `.txt` 格式文件上传
2. 知识库按文本内容 MD5 去重，内容完全相同时会拒绝重复入库
3. 对话历史按 `session_id` 分文件存储在 `chat_history/` 目录
4. 向量数据库文件存储在 `chroma_db/` 目录，删除后需重新上传知识库

## 许可证

MIT
