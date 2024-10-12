import yaml
import curses

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
        title = "Clash Node Selector"
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

def main(stdscr, filepath):
    # 读取 YAML 配置文件
    data = load_yaml(filepath)
    
    # 提取节点信息
    nodes = extract_proxies(data)

    if not nodes:
        stdscr.addstr(0, 0, "No nodes found in the YAML file.")
        stdscr.refresh()
        stdscr.getch()
    else:
        # 显示节点选择界面并保存选中的节点信息
        selected_node = display_nodes(stdscr, nodes)
        stdscr.clear()

        # 保存选中的节点详细信息到变量
        selected_node_info = selected_node

        # 显示选中的节点信息
        stdscr.addstr(0, 0, f"You selected: {selected_node_info['name']}")
        stdscr.addstr(1, 0, f"Details: {selected_node_info}")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    # 替换为实际的 YAML 文件路径
    filepath = "node_info.yaml"
    curses.wrapper(main, filepath)