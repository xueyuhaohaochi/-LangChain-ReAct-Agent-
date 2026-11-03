import sys
from pathlib import Path
# ========== 新增路径代码，解决 ModuleNotFoundError ==========
# 获取当前文件所在上级目录（Agent智能体），加入Python检索路径
current_file = Path(__file__)
parent_dir = current_file.parent.parent
sys.path.insert(0, str(parent_dir))
# ==========================================================

import logging
import os
from my_utils.path_tool import get_abs_path
from datetime import datetime

#日志保存的根目录
LOG_ROOT = get_abs_path('log')
#确保日志文件夹存在
os.makedirs(LOG_ROOT, exist_ok=True)
#日志格式
DEFAULT_LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


def get_logger(
        name='agent',
        console_level=logging.INFO,
        file_level=logging.DEBUG,
        log_file=None,
) -> logging.Logger:
    #创建日志管理器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    #如果日志管理器已经存在 handlers，则直接返回，避免重复添加
    if logger.handlers:
        return logger

    #控制台输出handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    #文件输出handler（修复原代码缩进bug，原代码缩进导致文件不会生成）
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f'{name}_{datetime.now().strftime("%Y-%m-%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

#快捷全局日志对象
logger = get_logger()

if __name__ == '__main__':
    test_logger = get_logger()
    test_logger.info('信息日志')
    test_logger.debug('调试日志')
    test_logger.warning('警告日志')
    test_logger.error('错误日志')
    test_logger.critical('严重错误日志')