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
import json

import bladoxy
from bladoxy.utils.get_available_port import get_available_port
from bladoxy.utils.logger import logger





def modify_bashrc_variable(bashrc_path, variable_name, new_value):
    """修改 .bashrc 文件中的指定变量的值"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        
        # 构建正则表达式，查找并替换指定变量的值
        pattern = rf'export {variable_name}="(\d+)"'
        replacement = f'export {variable_name}="{new_value}"'
        
        # 替换变量的值
        updated_content = re.sub(pattern, replacement, content)
        
        # 写回 .bashrc 文件
        with open(bashrc_path, 'w') as file:
            file.write(updated_content)

        logger.info(f"{variable_name} 已修改为 {new_value}")

    except FileNotFoundError:
        logger.warning(f"未找到文件: {bashrc_path}")
    except Exception as e:
        logger.error(f"修改 {variable_name} 时出错: {e}")




def configure_port(ss_port=1080, privoxy_port=8118,is_init = False,onlyss = False):
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    if onlyss==False:
        if is_init:
            privoxy_configure_file_install = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")

            logger.info(f"Privoxy初始检测端口为：{privoxy_port}")

            available_privoxy_port = get_available_port(privoxy_port)  # 获取可用端口

            logger.info(f"第一个Privoxy可用端口为 {available_privoxy_port}.")

            # 读取文件第794行的内容，获取当前端口号
            with open(privoxy_configure_file_install, 'r') as file:
                lines = file.readlines()


            # # TODO:可以去掉，备份的逻辑再思考一下。如果处理正确，理论上无需备份
            # backup_file = privoxy_configure_file_install + '.bak'
            # with open(backup_file, 'w') as backup:
            #     backup.writelines(lines)        

            current_privoxy_port_line = lines[793].strip()  # 获取第794行 (索引为793)
            current_privoxy_port = int(current_privoxy_port_line.split(':')[-1])  # 提取端口号

            # 仅当新端口号不等于当前端口时，才执行更新操作
            if available_privoxy_port != current_privoxy_port:
                # 更新第794行的端口号
                new_privoxy_port_line = current_privoxy_port_line.replace(str(current_privoxy_port), str(available_privoxy_port))
                lines[793] = new_privoxy_port_line + "\n"

                # 写回修改后的内容
                with open(privoxy_configure_file_install, 'w') as file:
                    file.writelines(lines)

                logger.info(f"端口已更新为：{available_privoxy_port}.")
            else:
                logger.info(f"端口已经是：{current_privoxy_port}，无需修改.")

            # 处理文件第1455行的SOCKS5代理设置
            expected_line = f"forward-socks5t / 127.0.0.1:{ss_port} ."
            actual_line = lines[1454].strip()  # 获取第1455行 (索引为1454)

            # 如果第1455行内容不符合预期，则替换该行
            if actual_line != expected_line:
                # 修改第1455行
                lines[1454] = expected_line + "\n"

                # 写回修改后的内容
                with open(privoxy_configure_file_install, 'w') as file:
                    file.writelines(lines)

                logger.info(f"已更新 privoxy 配置中对应shadowsocks端口。")
            else:
                logger.info("shadowsocks端口已正确配置，无需修改。")

            return available_privoxy_port
        else:

            
            current_privoxy_port = os.getenv('Privoxy_port')
            current_ss_port = os.getenv('Shadowsocks_port')
            if current_privoxy_port == None or current_ss_port == None:
                logger.error("未成功加载环境变量，请先执行 source ~/.bashrc ")
                exit(1)

            logger.info(f"Privoxy初始检测端口为：{current_privoxy_port}")
            available_privoxy_port = get_available_port(int(current_privoxy_port))
            if int(current_privoxy_port) == available_privoxy_port:
                logger.info(f"端口 {current_privoxy_port} 可用，无须修改端口。")
            else:
                logger.info(f"第一个privoxy可用端口为 {available_privoxy_port}.")
                privoxy_configure_file_install = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")
                with open(privoxy_configure_file_install, 'r') as file:
                    lines = file.readlines()
                current_privoxy_port_line = lines[793].strip()  # 获取第794行 (索引为793)
                current_privoxy_port_ = int(current_privoxy_port_line.split(':')[-1])  # 提取端口号
                assert current_privoxy_port_ == int(current_privoxy_port)
                # 更新第794行的端口号
                new_privoxy_port_line = current_privoxy_port_line.replace(str(current_privoxy_port), str(available_privoxy_port))
                lines[793] = new_privoxy_port_line + "\n"

                # 写回修改后的内容
                with open(privoxy_configure_file_install, 'w') as file:
                    file.writelines(lines)
                logger.info(f"配置文件端口已更新为：{available_privoxy_port}.")
                # 获取用户的 home 目录并拼接 .bashrc 文件路径
                home_dir = os.path.expanduser("~")
                bashrc_path = os.path.join(home_dir, ".bashrc")
                # 修改 .bashrc 文件中的 Privoxy_port
                modify_bashrc_variable(bashrc_path, "Privoxy_port", str(available_privoxy_port))
            
            logger.info(f"shadowsocks初始检测端口为：{current_ss_port}")
            available_ss_port = get_available_port(int(current_ss_port))
            if int(current_ss_port) == available_ss_port:
                logger.info(f"端口 {current_ss_port} 可用，无须修改端口。")
            else:
                logger.info(f"第一个shadowsocks可用端口为 {available_ss_port}.")
                privoxy_configure_file_install = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")
                with open(privoxy_configure_file_install, 'r') as file:
                    lines = file.readlines()
                # 处理文件第1455行的SOCKS5代理设置
                expected_line = f"forward-socks5t / 127.0.0.1:{available_ss_port} ."
                actual_line = lines[1454].strip()  # 获取第1455行 (索引为1454)
                current_ss_port_ = int(actual_line.split(':')[1].split(' ')[0].strip())
                assert current_ss_port_ == int(current_ss_port)
                
                # 修改第1455行
                lines[1454] = expected_line + "\n"

                # 写回修改后的内容
                with open(privoxy_configure_file_install, 'w') as file:
                    file.writelines(lines)

                logger.info(f"已更新 privoxy 配置中对应shadowsocks端口。")

                # 获取用户的 home 目录并拼接 .bashrc 文件路径
                home_dir = os.path.expanduser("~")
                bashrc_path = os.path.join(home_dir, ".bashrc")
                # 修改 .bashrc 文件中的 Shadowsocks_port
                modify_bashrc_variable(bashrc_path, "Shadowsocks_port", str(available_ss_port))

                
                # 更新all_nodes_info.json 和 shadowsocks.json
                # 读取 所有节点信息 数据
                ALL_NODES_INFO_FILE = os.path.join(WORKING_DIRECTORY, 'nodes_profiles','all_nodes_info.json')
                with open(ALL_NODES_INFO_FILE, 'r', encoding='utf-8') as json_file_1:
                    all_nodes_info = json.load(json_file_1)
                assert int(all_nodes_info['local_port']) == int(current_ss_port)
                all_nodes_info['local_port'] = available_ss_port
                with open(ALL_NODES_INFO_FILE, 'w', encoding='utf-8') as json_file_2:
                    json.dump(all_nodes_info, json_file_2, ensure_ascii=False, indent=4)

                

                SHADOWSOCKS_CONFIG_FILE = os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.json')
                with open(SHADOWSOCKS_CONFIG_FILE, 'r', encoding='utf-8') as json_file_3:
                    shadowsocks_config = json.load(json_file_3)

                shadowsocks_config['local_port'] = available_ss_port

                with open(SHADOWSOCKS_CONFIG_FILE, 'w', encoding='utf-8') as json_file_4:
                    json.dump(shadowsocks_config, json_file_4, ensure_ascii=False, indent=4)

                logger.info("Shadowsocks 配置文件已更新。")
            
            return available_privoxy_port,available_ss_port
        
    else:
        # 只修改ss端口
        current_ss_port = os.getenv('Shadowsocks_port')
        
        try:
            logger.info(f"shadowsocks初始检测端口为：{current_ss_port}")
            available_ss_port = get_available_port(int(current_ss_port))
        except TypeError as e:
            logger.error("未成功加载环境变量，请先执行 source ~/.bashrc ")
            exit(1)


        if int(current_ss_port) == available_ss_port:
                logger.info(f"端口 {current_ss_port} 可用，无须修改端口。")
        else:
            logger.info(f"第一个shadowsocks可用端口为 {available_ss_port}.")
            privoxy_configure_file_install = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")
            with open(privoxy_configure_file_install, 'r') as file:
                lines = file.readlines()
            # 处理文件第1455行的SOCKS5代理设置
            expected_line = f"forward-socks5t / 127.0.0.1:{available_ss_port} ."
            actual_line = lines[1454].strip()  # 获取第1455行 (索引为1454)
            current_ss_port_ = int(actual_line.split(':')[1].split(' ')[0].strip())
            assert current_ss_port_ == int(current_ss_port)
            
            # 修改第1455行
            lines[1454] = expected_line + "\n"

            # 写回修改后的内容
            with open(privoxy_configure_file_install, 'w') as file:
                file.writelines(lines)

            logger.info(f"已更新 privoxy 配置中对应shadowsocks端口。")

            # 获取用户的 home 目录并拼接 .bashrc 文件路径
            home_dir = os.path.expanduser("~")
            bashrc_path = os.path.join(home_dir, ".bashrc")
            # 修改 .bashrc 文件中的 Shadowsocks_port
            modify_bashrc_variable(bashrc_path, "Shadowsocks_port", str(available_ss_port))

            
            # 更新all_nodes_info.json 和 shadowsocks.json
            # 读取 所有节点信息 数据
            ALL_NODES_INFO_FILE = os.path.join(WORKING_DIRECTORY, 'nodes_profiles','all_nodes_info.json')
            with open(ALL_NODES_INFO_FILE, 'r', encoding='utf-8') as json_file_1:
                all_nodes_info = json.load(json_file_1)
            assert int(all_nodes_info['local_port']) == int(current_ss_port)
            all_nodes_info['local_port'] = available_ss_port
            with open(ALL_NODES_INFO_FILE, 'w', encoding='utf-8') as json_file_2:
                json.dump(all_nodes_info, json_file_2, ensure_ascii=False, indent=4)

            

            SHADOWSOCKS_CONFIG_FILE = os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.json')
            with open(SHADOWSOCKS_CONFIG_FILE, 'r', encoding='utf-8') as json_file_3:
                shadowsocks_config = json.load(json_file_3)

            shadowsocks_config['local_port'] = available_ss_port

            with open(SHADOWSOCKS_CONFIG_FILE, 'w', encoding='utf-8') as json_file_4:
                json.dump(shadowsocks_config, json_file_4, ensure_ascii=False, indent=4)

            logger.info("Shadowsocks 配置文件已更新。")










                    











