from bladoxy.utils.kill_process import kill_possible_sslocal_processes
from bladoxy.utils.nodes import ssconfig_handler
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.start_process import start_sslocal
from bladoxy.utils.check_availability import check_availability
from bladoxy.utils.nodes import change_node
import re
import os


def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
        return False

def update_profile():
    bashrc_path = os.path.expanduser("~/.bashrc")
    START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
    if check_marker_in_bashrc(bashrc_path, START_MARKER_BLADOXY):
        print("更新配置...")
        # 停止 sslocal 进程
        kill_possible_sslocal_processes()
        ssconfig_handler()
        configure_port(is_init=False, onlyss=True)
        
        change_node()
        start_sslocal()
        check_availability()
        print("成功更新配置。")
    else:
        print("请先执行 bladoxy init 进行初始化！")


