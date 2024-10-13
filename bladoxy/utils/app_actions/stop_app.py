import os
import re
from bladoxy.utils.kill_process import kill_possible_processes
from bladoxy.utils.set_env import remove_proxy_from_bashrc


def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
        return False


def stop():
    bashrc_path = os.path.expanduser("~/.bashrc")
    START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
    if check_marker_in_bashrc(bashrc_path, START_MARKER_BLADOXY):
        print("正在停止进程...")
        # 定义开始和结束标记
        START_MARKER_PROXY = "######## START MY_PROXY ########"
        END_MARKER_PROXY = "######## END MY_PROXY ########"

        # 获取用户的 home 目录并拼接 .bashrc 文件路径
        home_dir = os.path.expanduser("~")
        bashrc_path = os.path.join(home_dir, ".bashrc")

        # 从 .bashrc 文件中删除代理环境变量
        remove_proxy_from_bashrc(bashrc_path, START_MARKER_PROXY, END_MARKER_PROXY)
        kill_possible_processes()
        print("成功停止进程")

    else:
        print("请先执行 bladoxy init 进行初始化！")