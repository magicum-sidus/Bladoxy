# Copyright 2024 Magicum Sidus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from bladoxy.utils.print_info import echo_version_info
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.set_env import set_environment_variables
from bladoxy.utils.start_process import start_sslocal,start_privoxy
from bladoxy.utils.check_availability import check_availability
from bladoxy.utils.kill_process import kill_possible_processes
import os
import re



# def get_pids_by_name(process_name):
#     """通过进程名获取进程 ID 列表"""
#     try:
#         # 使用 `pgrep` 根据进程名查找进程 ID
#         result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
#         pids = result.stdout.strip().split("\n")
#         return [pid for pid in pids if pid]
#     except Exception as e:
#         print(f"获取进程 {process_name} 的 PID 时出错: {e}")
#         return []

# def kill_processes(pids):
#     """根据 PID 列表终止进程"""
#     for pid in pids:
#         try:
#             print(f"正在终止 PID: {pid}")
#             os.kill(int(pid), 9)  # 使用信号 9 (SIGKILL) 杀掉进程
#         except Exception as e:
#             print(f"无法终止 PID {pid}: {e}")

# def kill_possible_processes():
#     # 获取并杀掉 'privoxy' 进程
#     privoxy_pids = get_pids_by_name('privoxy')
#     if privoxy_pids:
#         kill_processes(privoxy_pids)
#     else:
#         print("未找到 'privoxy' 进程。")

#     # 获取并杀掉 'sslocal' 进程
#     sslocal_pids = get_pids_by_name('sslocal')
#     if sslocal_pids:
#         kill_processes(sslocal_pids)
#     else:
#         print("未找到 'sslocal' 进程。")




def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
        return False


def run():
    # 这里需要检测是否已初始化
    echo_version_info()
    print("(重新)运行SSPrivoxy...")


    bashrc_path = os.path.expanduser("~/.bashrc")
    START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
    if check_marker_in_bashrc(bashrc_path, START_MARKER_BLADOXY):
        kill_possible_processes()
        privoxy_port,ss_port = configure_port(is_init = False,onlyss=False)
        set_environment_variables(ss_port=ss_port, privoxy_port=privoxy_port, is_init = False)
        start_sslocal()
        start_privoxy()
        check_availability()
    else:
        print("请先执行 bladoxy init 进行初始化！")



    