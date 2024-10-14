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
from bladoxy.utils.logger import logger
from bladoxy.utils.nodes import ssconfig_handler
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.nodes import change_node
from bladoxy.utils.set_env import set_environment_variables
from bladoxy.utils.check_availability import check_availability
from bladoxy.utils.start_process import start_sslocal,start_privoxy

from bladoxy.utils.app_actions.cleanup import finalizeToinit

from bladoxy.utils.make_privoxy import make_privoxy

from termcolor import colored

import os
import bladoxy
import re



def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
        return False




def initialize():
    
    logger.info("Version Info")
    echo_version_info()



    bashrc_path = os.path.expanduser("~/.bashrc")
    START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
    if check_marker_in_bashrc(bashrc_path, START_MARKER_BLADOXY):
        # 获取用户确认
        reply = input("检测到您已安装 Bladoxy ，要清理重装吗? (y/n) ").strip().lower()
        if reply == 'y':
            finalizeToinit()
        else:
            print("重装已取消")
            print("正在退出初始化安装程序……")
            exit(1)
    else:
        print("未检测到已安装的 SSPrivoxy")





    logger.info("Initializing the environment...")
    # 嵌入的许可证文本
    LICENSE = colored("""
Software License (English version):

MIT License

Copyright (c) [2024] [Magicum Sidus]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Acknowledgements:
The Bladoxy makes use of the following open source projects:
- shadowsocks by https://shadowsocks.org/
- privoxy by https://www.privoxy.org/

We extend our gratitude to these projects for their contributions to the open source community.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Welcome to provide better suggestions for Bladoxy!

软件许可（中文版本）：

MIT 许可证

版权所有 (c) [2024] [Magicum Sidus]

特此免费授予任何人获得本软件和相关文档文件（“软件”）副本的权利，无限制地处理本软件，包括但不限于使用、复制、修改、合并、出版、发行、授权、和/或出售本软件的副本，并允许向其提供本软件的人这样做，但须符合以下条件：

上述版权声明和本许可声明应包含在本软件的所有副本或实质性部分中。

致谢：
Bladoxy项目使用了以下开源项目：
- shadowsocks 由 https://shadowsocks.org/
- privoxy 由 https://www.privoxy.org/

我们对这些项目对开源社区的贡献表示感谢。

本软件按“原样”提供，不提供任何形式的保证，明示或暗示，包括但不限于适销性、适用于特定目的和不侵权的保证。在任何情况下，作者或版权持有人均不对任何索赔、损害或其他责任承担责任，无论是在合同诉讼、侵权行为或其他与本软件或本软件的使用或其他交易有关的诉讼中。

欢迎对 Bladoxy 提供更好的建议！
    """, 'cyan')

    # 显示许可证文本
    print(LICENSE)

    # 提示用户接受许可证
    while True:
        yn = input(colored("Do you accept the license terms? [yes/no] ",'green')).strip().lower()
        if yn in ('yes', 'y'):
            break
        elif yn in ('no', 'n'):
            logger.error("You need to accept the license to continue.")
            exit()
        else:
            logger.warning("Please answer yes(y) or no(n).")

    # 继续安装...
    logger.info("Initialization will now continue...")


    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)

    
    
    shadowsocks_config_directory = os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config')


    if not os.path.isdir(shadowsocks_config_directory):
        os.makedirs(shadowsocks_config_directory, exist_ok=True)
        logger.info(f"Created dir {shadowsocks_config_directory}")


    ss_config_files = [
        os.path.join(shadowsocks_config_directory,'shadowsocks.json'),
        os.path.join(shadowsocks_config_directory,'shadowsocks.log'),
        os.path.join(shadowsocks_config_directory,'shadowsocks.pid'),
    ]

 
    for file in ss_config_files:
        if not os.path.isfile(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)
            open(file, 'w').close()
            logger.info(f"Created file: {file}")


    # 1.提示用户输入配置文件所在路径
    # 2.检查配置文件是否存在
    # 3.检查配置文件是否合法（clash得yaml配置文件）
    # 4.复制配置文件到profiles目录
    # 5.读取配置文件
    # 6.将配置文件内容写入到总节点信息列表文件
    # 7.启动shadowsocks服务时选取其中一个节点，配置文件只写一个节点。按照索引来选取


    ss_port = ssconfig_handler()

    # 在这里插入编译安装privoxy的逻辑
    make_privoxy()


    # configure privoxy
    privoxy_port = configure_port(ss_port=ss_port, privoxy_port=8118, is_init=True,onlyss=False)

    # select node
    change_node()

    # start shadowsocks service
    start_sslocal()

    # start privoxy service
    start_privoxy()

    set_environment_variables(ss_port=ss_port, privoxy_port=privoxy_port, is_init = True)
    
    check_availability()





if __name__ == "__main__":
    initialize()

