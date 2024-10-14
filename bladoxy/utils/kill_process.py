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


import subprocess
import os


def get_pids_by_name(process_name):
    """通过进程名获取进程 ID 列表"""
    try:
        # 使用 `pgrep` 根据进程名查找进程 ID
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")
        return [pid for pid in pids if pid]
    except Exception as e:
        print(f"获取进程 {process_name} 的 PID 时出错: {e}")
        return []

def kill_processes(pids):
    """根据 PID 列表终止进程"""
    for pid in pids:
        try:
            print(f"正在终止 PID: {pid}")
            os.kill(int(pid), 9)  # 使用信号 9 (SIGKILL) 杀掉进程
        except Exception as e:
            print(f"无法终止 PID {pid}: {e}")

def kill_possible_processes():
    # 获取并杀掉 'privoxy' 进程
    privoxy_pids = get_pids_by_name('privoxy')
    if privoxy_pids:
        kill_processes(privoxy_pids)
    else:
        print("未找到 'privoxy' 进程。")

    # 获取并杀掉 'sslocal' 进程
    sslocal_pids = get_pids_by_name('sslocal')
    if sslocal_pids:
        kill_processes(sslocal_pids)
    else:
        print("未找到 'sslocal' 进程。")


def kill_possible_sslocal_processes():
    # 获取并杀掉 'sslocal' 进程
    sslocal_pids = get_pids_by_name('sslocal')
    if sslocal_pids:
        kill_processes(sslocal_pids)
    else:
        print("未找到 'sslocal' 进程。")