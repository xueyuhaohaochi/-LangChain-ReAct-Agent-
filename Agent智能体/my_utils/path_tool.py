#为整个工程提供统一的绝对路径
import os
#获取根目录
def get_project_root() -> str:
    current_file = os.path.abspath(__file__)
    #获取工程的根目录，获取当前文件的绝对路径
    current_dir = os.path.dirname(current_file)
    #获取根目录本目录
    project_root = os.path.dirname(current_dir)
    return project_root


def get_abs_path(relative_path: str) -> str:
    ''''
    提供相对路径，返回绝对路径
    relative_path: 相对路径
    return: 绝对路径
    '''
    project_root = get_project_root()
    return os.path.join(project_root,relative_path)
#路径工具中两个常用函数开发完成
