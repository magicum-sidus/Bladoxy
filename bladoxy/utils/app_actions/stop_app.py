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


import os
import re

from bladoxy.utils.kill_process import kill_possible_processes
from bladoxy.utils.set_env import remove_proxy_from_bashrc
from bladoxy.utils.logger import logger


def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        logger.warning(f"未找到文件: {bashrc_path}")
        return False


def stop():

    logger.info("正在停止进程...")
    # 定义开始和结束标记
    START_MARKER_PROXY = "######## START MY_PROXY ########"
    END_MARKER_PROXY = "######## END MY_PROXY ########"

    # 获取用户的 home 目录并拼接 .bashrc 文件路径
    home_dir = os.path.expanduser("~")
    bashrc_path = os.path.join(home_dir, ".bashrc")

    # 从 .bashrc 文件中删除代理环境变量
    remove_proxy_from_bashrc(bashrc_path, START_MARKER_PROXY, END_MARKER_PROXY)
    kill_possible_processes()
    logger.info("成功停止进程")




        