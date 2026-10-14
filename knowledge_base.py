"""知识库"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    """检查传入的md5字符串是否已经被处理过了
        Return False if md5_str does not match
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()   # 处理字符串前后的空格和回车
            if line == md5_str:
                return True # 匹配成功
        return False





def save_md5(md5_str: str):
    """保存传入的md5字符串"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""
    return hashlib.md5(input_str.encode(encoding)).hexdigest()


class KnowledgeBaseService(object):

    def __init__(self):
        # 初始化向量数据库
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,  # 数据库本地存储文件夹
        )  # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,  # 连续文本段之间的字符重叠数量
            separators=config.separators,  # 自然段落划分的符号
            length_function=len,  # 使用Python自带的len函数做长度统计的依据
        )  # 文本分割器的对象

    def upload_by_str(self, data: str, filename):
        """根据传入的字符串，进行向量化，存入向量数据库中"""
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[ERROR],the str has been uploaded!" # 已经处理过了，直接返回

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks: list[str] = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "Sunbende",
        }

        self.chroma.add_texts(
            # iterable -> list \ tuple
            texts=knowledge_chunks, # 文本段列表
            metadatas = [metadata for _ in knowledge_chunks] # 每个文本段的元数据
        )

        save_md5(md5_hex)
        return "[SUCCESS],the str has been uploaded!"

if __name__ == '__main__':


    service = KnowledgeBaseService()
    print(service.upload_by_str("周杰伦","testfile"))
