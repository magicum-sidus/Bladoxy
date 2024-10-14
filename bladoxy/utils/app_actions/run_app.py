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

from bladoxy.utils.print_info import echo_version_info
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.set_env import set_environment_variables
from bladoxy.utils.start_process import start_sslocal,start_privoxy
from bladoxy.utils.check_availability import check_availability
from bladoxy.utils.kill_process import kill_possible_processes
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


def run():
    # 这里需要检测是否已初始化
    echo_version_info()
    logger.info("(重新)运行 Bladoxy...")


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
        logger.error("请先执行 bladoxy init 进行初始化！")



    