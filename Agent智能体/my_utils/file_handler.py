import os
import hashlib
from typing import Tuple, List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from my_utils.logger_hander import logger


def get_file_md5_hex(filepath: str) -> str | None:
    """获取文件md5的16进制字符串，用于文件去重"""
    # 判断文件是否存在
    if not os.path.exists(filepath):
        logger.error(f"文件不存在: {filepath}")
        return None
    # 判断是否为文件（修复原逻辑颠倒bug）
    if not os.path.isfile(filepath):
        logger.error(f"路径不是文件: {filepath}")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 8192  # 8KB 分块读取，适配大文件
    try:
        with open(filepath, 'rb') as f:  # 二进制读取，避免编码问题
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
        md5_hex = md5_obj.hexdigest()
        return md5_hex
    except Exception as e:
        logger.error(f"获取文件md5失败 | 文件:{filepath} | 错误:{str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]) -> tuple[str, ...]:
    """
    遍历文件夹，返回指定后缀的文件完整路径元组
    :param path: 目标文件夹路径
    :param allowed_types: 允许的文件后缀，如 (".pdf", ".txt")
    :return: 匹配文件绝对路径元组
    """
    files = []
    # 路径不是文件夹，返回空列表，而非传入的后缀元组
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type] {path} 不是有效文件夹")
        return tuple()
    for f_name in os.listdir(path):
        full_path = os.path.join(path, f_name)
        # 只匹配文件，排除子文件夹
        if os.path.isfile(full_path) and f_name.endswith(allowed_types):
            files.append(full_path)
    return tuple(files)


def pdf_loader(filepath: str, password=None) -> List[Document]:
    """加载PDF文档"""
    return PyPDFLoader(filepath, password=password).load()


def txt_loader(filepath: str) -> List[Document]:
    """加载TXT文本文档"""
    return TextLoader(filepath,encoding = 'utf-8').load()