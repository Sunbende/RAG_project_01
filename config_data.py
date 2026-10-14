md5_path = "./md5.txt"

# ChromaDB 配置
collection_name = "rag"
persist_directory = "./chroma_db"


# splitter文本分割器配置
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000 # 文本分割阈值
