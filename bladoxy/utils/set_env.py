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



import bladoxy

import os
import re



def remove_proxy_from_bashrc(bashrc_path, start_marker, end_marker):
    """从 .bashrc 中删除指定标记之间的环境变量"""
    
    try:
        # 读取 .bashrc 文件内容
        with open(bashrc_path, 'r') as file:
            content = file.read()

        # 查找 START_MARKER 和 END_MARKER 之间的内容
        pattern = re.escape(start_marker) + r'.*?' + re.escape(end_marker)
        if re.search(pattern, content, re.DOTALL):
            print("从 .bashrc 中删除环境变量")
            # 删除标记之间的内容
            updated_content = re.sub(pattern, '', content, flags=re.DOTALL)

            # 将修改后的内容写回 .bashrc 文件
            with open(bashrc_path, 'w') as file:
                file.write(updated_content)
        else:
            print("未找到 proxy 环境变量")
    
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
    except Exception as e:
        print(f"修改 .bashrc 时出错: {e}")




def add_proxy_to_bashrc(bashrc_path, start_marker, end_marker, privoxy_port):
    """向 .bashrc 添加或更新 http_proxy 和 https_proxy 环境变量"""
    
    # 构建代理地址
    http_proxy_value = f"http://127.0.0.1:{privoxy_port}"
    https_proxy_value = http_proxy_value

    # 检查 .bashrc 是否已经包含代理设置
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()

        # 如果没有找到开始标记，添加代理设置
        if not re.search(re.escape(start_marker), content):
            print("向 .bashrc 添加 http(s)_proxy 环境变量")
            with open(bashrc_path, 'a') as file:
                file.write(f"\n{start_marker}\n")
                file.write(f'export http_proxy="{http_proxy_value}"\n')
                file.write(f'export https_proxy="{https_proxy_value}"\n')
                file.write(f"{end_marker}\n")
        else:
            print("proxy 环境变量已经存在")
    
    except FileNotFoundError:
        print(f"未找到文件: {bashrc_path}")
    except Exception as e:
        print(f"修改 .bashrc 时出错: {e}")



def set_environment_variables(ss_port,privoxy_port,is_init = False):
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    if is_init:
        
        conda_env_path = os.environ.get("CONDA_PREFIX")
        if conda_env_path:
            print(f"当前 Conda 环境路径: {conda_env_path}")
        else:
            print("未检测到 Conda 环境")

        print("正在设置环境变量")

        # 变量定义
        bladoxy_version = "v1.3.0"
        START_MARKER_PROXY = "######## START MY_PROXY ########"
        END_MARKER_PROXY = "######## END MY_PROXY ########"
        START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
        END_MARKER_BLADOXY = "######## END MY_BLADOXY ########"

    
        
        # 代理变量
        http_proxy_value = f"http://127.0.0.1:{privoxy_port}"
        https_proxy_value = f"http://127.0.0.1:{privoxy_port}"



        # 路径设置
        pcre_lib_path = os.path.join(WORKING_DIRECTORY, "modules", "dependencies","pcre", "lib")
        sslocal_bin_path = os.path.join(conda_env_path, "bin")
        privoxy_bin_path = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "sbin")

        # 设置环境变量
        os.environ["http_proxy"] = http_proxy_value
        os.environ["https_proxy"] = https_proxy_value

        # 检查并修改 .bashrc 文件
        home_dir = os.path.expanduser("~")
        bashrc_path = os.path.join(home_dir, ".bashrc")

        def update_bashrc(start_marker, end_marker, content_lines):
            with open(bashrc_path, "r") as bashrc:
                bashrc_content = bashrc.read()

            if start_marker not in bashrc_content:
                print(f"向 .bashrc 添加环境变量块: {start_marker.strip('# ')}")
                with open(bashrc_path, "a") as bashrc:
                    bashrc.write(f"\n{start_marker}\n")
                    bashrc.writelines(content_lines)
                    bashrc.write(f"{end_marker}\n")
            else:
                print(f"{start_marker.strip('# ')} 环境变量已经存在")

        # 添加 Bladoxy 环境变量到 .bashrc
        bladoxy_env_content = [
            f"export bladoxy_version=\"{bladoxy_version}\"\n",
            f"export Shadowsocks_port=\"{ss_port}\"\n",
            f"export Privoxy_port=\"{privoxy_port}\"\n",
            f"export bladoxy_installation_path=\"{WORKING_DIRECTORY}\"\n",
            f"export pcre_lib_path=\"{pcre_lib_path}\"\n",
            f"export sslocal_bin_path=\"{sslocal_bin_path}\"\n",
            f"export privoxy_bin_path=\"{privoxy_bin_path}\"\n"
        ]
        update_bashrc(START_MARKER_BLADOXY, END_MARKER_BLADOXY, bladoxy_env_content)

        # 添加 http(s)_proxy 环境变量到 .bashrc
        proxy_env_content = [
            f"export http_proxy=\"{http_proxy_value}\"\n",
            f"export https_proxy=\"{https_proxy_value}\"\n"
        ]
        update_bashrc(START_MARKER_PROXY, END_MARKER_PROXY, proxy_env_content)
        os.environ['http_proxy'] = http_proxy_value
        os.environ['https_proxy'] = https_proxy_value

    else:
        # 定义开始和结束标记
        START_MARKER_PROXY = "######## START MY_PROXY ########"
        END_MARKER_PROXY = "######## END MY_PROXY ########"
        # 获取用户的 home 目录并拼接 .bashrc 文件路径
        home_dir = os.path.expanduser("~")
        bashrc_path = os.path.join(home_dir, ".bashrc")
        # 向 .bashrc 文件中添加或更新代理设置
        add_proxy_to_bashrc(bashrc_path, START_MARKER_PROXY, END_MARKER_PROXY, privoxy_port)

