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
import yaml
import json
import shutil
import curses

import bladoxy
from bladoxy.utils.get_available_port import get_available_port
from bladoxy.utils.logger import logger





    

def ssconfig_handler():
    logger.info("处理ss配置...")
    
    # 1. Prompt the user to input the configuration file path
    config_path = input("请输入配置文件的路径:")

    # 2. Check if the configuration file exists
    if not os.path.isfile(config_path):
        logger.warning("配置文件不存在")
        exit(1)

    # 3. Check if the configuration file is valid (Clash YAML configuration file)
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
            proxies = config_data.get('proxies', [])
    except:
        logger.error("配置文件不是合法的 YAML 文件！")
        exit(1)

    # Check if 'proxies' field has nodes and is valid
    if not proxies:
        logger.error("配置文件不包含 proxy 节点！")
        exit(1)

    valid = True
    for proxy in proxies:
        if proxy.get('type') != 'ss' or not all(k in proxy for k in ['server', 'port', 'cipher', 'password']):
            valid = False
            break

    if not valid:
        logger.error("配置文件不包含合法 SS 节点！")
        exit(1)

    # 4. Copy the configuration file to the profiles directory
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    profiles_dir = os.path.join(WORKING_DIRECTORY, 'nodes_profiles')
    os.makedirs(profiles_dir, exist_ok=True)
    shutil.copy(config_path, os.path.join(profiles_dir, 'nodes_profile.yaml'))
    logger.info(f"配置文件已经保存到 {profiles_dir}")


    logger.info(f"shadowsocks初始检测端口为：1080")
    ss_local_port = get_available_port(start_port=1080)
    logger.info(f"第一个shadowsocks可用端口为 {ss_local_port}.")




    all_node_info = {
        "servers": [],
        "local_port": ss_local_port,
        "timeout": 300,  # Default timeout, can be adjusted as needed
    }

    for proxy in proxies:
        all_node_info["servers"].append({
            'server': proxy.get('server'),
            'server_port': proxy.get('port'),
            'method': proxy.get('cipher'),
            'password': proxy.get('password'),
        })

    ALL_NODES_INFO_FILE = os.path.join(profiles_dir, 'all_nodes_info.json')

    with open(ALL_NODES_INFO_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(all_node_info, json_file, ensure_ascii=False, indent=4)
    
    # print("Configuration file has been converted and saved as all_nodes_info.json.")

    # 7. Save node names and their index to a separate file (name_index_mapping.json)
    node_name_index = {}

    for index, proxy in enumerate(proxies):
        node_name = proxy.get('name', f'Node-{index}')  # Use 'name' field if present, otherwise default to 'Node-{index}'
        node_name_index[node_name] = index

    NODE_NAME_INDEX_FILE = os.path.join(profiles_dir, 'name_index_mapping.json')

    with open(NODE_NAME_INDEX_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(node_name_index, json_file, ensure_ascii=False, indent=4)

    # print(f"Node names and their indices have been saved to {NODE_NAME_INDEX_FILE}.")

    return ss_local_port






# 从 YAML 文件中加载配置
def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

# 提取所有节点信息
def extract_proxies(data):
    return data.get('proxies', [])

# 显示节点列表，支持分页和光标移动
def display_nodes(stdscr, nodes):
    curses.curs_set(0)  # 隐藏光标
    k = 0  # 键盘输入
    cursor_pos = 0  # 光标位置
    page_size = curses.LINES - 6  # 每页显示的节点数 (预留顶部和底部用于信息显示)
    current_page = 0  # 当前页数
    total_items = len(nodes)  # 节点总数
    total_pages = (total_items + page_size - 1) // page_size  # 总页数

    # 初始化颜色对
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # 标题颜色
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 选中项颜色
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 普通文本颜色

    while k != ord('\n'):  # 按下回车键选择节点
        stdscr.clear()

        # 获取终端宽度和高度
        max_x = curses.COLS
        max_y = curses.LINES

        # 打印标题
        title = "Bladoxy Node Selector"
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, (max_x - len(title)) // 2, title, curses.A_BOLD)
        stdscr.attroff(curses.color_pair(1))

        # 显示帮助信息
        help_text = "Use UP/DOWN to move, ENTER to select"
        stdscr.addstr(1, (max_x - len(help_text)) // 2, help_text)

        stdscr.addstr(2, 0, "-" * max_x)

        current_node_idx = 0
        start_node_idx = current_page * page_size
        end_node_idx = min(start_node_idx + page_size, total_items)

        line = 3  # 从第3行开始显示内容

        # 遍历并显示节点
        for idx in range(start_node_idx, end_node_idx):
            node = nodes[idx]
            node_display = f"  {node['name']}"  # 节点名称
            if idx == start_node_idx + cursor_pos:
                node_display = f"> {node['name']}"  # 高亮显示当前选中的节点
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(line, (max_x - len(node_display)) // 2, node_display)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(line, (max_x - len(node_display)) // 2, node_display)
                stdscr.attroff(curses.color_pair(3))

            line += 1

        stdscr.addstr(max_y - 3, 0, "-" * max_x)

        # 显示页码
        page_info = f"Page {current_page + 1}/{total_pages}"
        stdscr.addstr(max_y - 2, (max_x - len(page_info)) // 2, page_info)

        stdscr.refresh()

        # 等待键盘输入
        k = stdscr.getch()

        # 处理键盘输入
        if k == curses.KEY_UP:
            cursor_pos -= 1
            if cursor_pos < 0:
                cursor_pos = min(page_size - 1, end_node_idx - start_node_idx - 1)
        elif k == curses.KEY_DOWN:
            cursor_pos += 1
            if cursor_pos >= end_node_idx - start_node_idx:
                cursor_pos = 0
        elif k == curses.KEY_LEFT and current_page > 0:
            current_page -= 1
            cursor_pos = 0
        elif k == curses.KEY_RIGHT and current_page < total_pages - 1:
            current_page += 1
            cursor_pos = 0

    # 返回选中的节点信息
    return nodes[start_node_idx + cursor_pos]

def node_selector(stdscr, filepath):
    # 读取 YAML 配置文件
    data = load_yaml(filepath)
    
    # 提取节点信息
    nodes = extract_proxies(data)

    if not nodes:
        stdscr.addstr(0, 0, "No nodes found in the YAML file.")
        stdscr.refresh()
        stdscr.getch()
        return None  # 如果没有节点，返回 None
    else:
        # 显示节点选择界面并保存选中的节点信息
        selected_node = display_nodes(stdscr, nodes)
        stdscr.clear()

        # 保存选中的节点详细信息到变量
        selected_node_info = selected_node

        # 显示选中的节点信息
        stdscr.addstr(0, 0, f"你选择了: {selected_node_info['name']}")
        stdscr.addstr(1, 0, f"节点信息: {selected_node_info}")
        stdscr.addstr(6, 0, "请按回车继续……")
        stdscr.refresh()
        stdscr.getch()

        # 返回选中的节点信息
        return selected_node_info









def update_ss_config(node_name):
    logger.info("更新ss配置...")
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    NODE_NAME_INDEX_FILE = os.path.join(WORKING_DIRECTORY, 'nodes_profiles','name_index_mapping.json')

    # 读取 节点和索引映射 数据
    with open(NODE_NAME_INDEX_FILE, 'r', encoding='utf-8') as json_file:
        node_name_index = json.load(json_file)

  

    selected_node_index = node_name_index.get(node_name)



    ALL_NODES_INFO_FILE = os.path.join(WORKING_DIRECTORY, 'nodes_profiles','all_nodes_info.json')

    # 读取 所有节点信息 数据
    with open(ALL_NODES_INFO_FILE, 'r', encoding='utf-8') as json_file_2:
        all_nodes_info = json.load(json_file_2)
    
    servers_list = all_nodes_info.get('servers', [])
    ss_local_port = all_nodes_info.get('local_port', 1080)
    timeout = all_nodes_info.get('timeout', 300)
    select_node_info = servers_list[selected_node_index]


    # 更新 shadowsocks.json 文件

    SHADOWSOCKS_CONFIG_FILE = os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.json')

    shadowsocks_config = {
        "server": select_node_info['server'],
        "server_port": select_node_info['server_port'],
        "local_port": ss_local_port,
        "password": select_node_info['password'],
        "method": select_node_info['method'],
        "timeout": timeout
    }

    with open(SHADOWSOCKS_CONFIG_FILE, 'w', encoding='utf-8') as json_file_3:
        json.dump(shadowsocks_config, json_file_3, ensure_ascii=False, indent=4)

    logger.info("Shadowsocks 配置文件已更新。")




def change_node():
    logger.info("修改节点...")
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    nodes_profile_file = os.path.join(WORKING_DIRECTORY, 'nodes_profiles', 'nodes_profile.yaml')

    if not os.path.isfile(nodes_profile_file):
        logger.error("节点配置文件不存在！")
        logger.error("请重新上传节点配置文件!")
        exit(1)

    # 使用 curses.wrapper 调用 node_selector 并返回选中的节点
    selected_node = curses.wrapper(node_selector, nodes_profile_file)

    if selected_node:
        logger.info(f"已选择节点: {selected_node['name']}")
        # 进一步处理选中的节点，更新配置文件
        update_ss_config(selected_node['name'])


    else:
        logger.warning("没有选择任何节点！")





if __name__ == '__main__':
    # ss_port = ssconfig_handler()
    # print(ss_port)
    change_node()