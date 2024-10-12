import yaml
import curses

# 从 YAML 文件中加载配置
def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

# 提取节点信息和分组信息
def extract_proxies_and_groups(data):
    groups = []
    if 'proxy-groups' in data:
        for group in data['proxy-groups']:
            if 'proxies' in group:
                # 在 groups 中，我们不仅保存节点的名称，还保存详细的节点信息
                expanded_proxies = []
                for proxy_name in group['proxies']:
                    # 从 `proxies` 中找到详细的节点信息
                    proxy = next((p for p in data['proxies'] if p['name'] == proxy_name), None)
                    if proxy:
                        expanded_proxies.append(proxy)
                groups.append({
                    'name': group['name'],
                    'proxies': expanded_proxies
                })
    return groups

# 显示节点列表，支持分组、分页和光标移动
def display_nodes(stdscr, groups):
    curses.curs_set(0)  # 隐藏光标
    k = 0  # 键盘输入
    cursor_pos = 0  # 光标位置
    page_size = curses.LINES - 4  # 每页显示的节点数
    current_page = 0  # 当前页数
    total_items = sum(len(group['proxies']) for group in groups)  # 所有代理节点数
    total_pages = (total_items + page_size - 1) // page_size  # 总页数

    # 初始化颜色对
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # 标题颜色
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 选中项颜色
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # 普通文本颜色

    while k != ord('\n'):  # 按下回车键选择节点
        stdscr.clear()

        # 获取终端宽度，避免超出显示
        max_x = curses.COLS - 2  # 预留2列用于边距
        max_y = curses.LINES - 2  # 预留行数用于显示提示信息

        # 打印标题
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 2, "Clash Node Selector", curses.A_BOLD)
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(1, 0, "-" * (max_x))

        current_node_idx = 0
        start_node_idx = current_page * page_size
        end_node_idx = start_node_idx + page_size

        line = 2  # 从第2行开始显示内容

        # 遍历分组并显示
        for group in groups:
            group_name = f"Group: {group['name']}"
            if len(group_name) > max_x:  # 确保组名不会超出屏幕宽度
                group_name = group_name[:max_x - 3] + "..."

            # 显示分组名称
            if line < max_y:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(line, 2, group_name)
                stdscr.attroff(curses.color_pair(1))
                line += 1

            # 显示分组中的节点
            for node in group['proxies']:
                if current_node_idx >= start_node_idx and current_node_idx < end_node_idx:
                    display_text = f"> {node['name']}" if current_node_idx - start_node_idx == cursor_pos else f"  {node['name']}"
                    if len(display_text) > max_x:  # 确保节点名不会超出屏幕宽度
                        display_text = display_text[:max_x - 3] + "..."

                    if line < max_y:
                        if current_node_idx - start_node_idx == cursor_pos:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(line, 4, display_text)
                            stdscr.attroff(curses.color_pair(2))
                        else:
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(line, 4, display_text)
                            stdscr.attroff(curses.color_pair(3))

                        line += 1
                current_node_idx += 1

        # 显示页码和提示信息
        if line < curses.LINES:
            stdscr.addstr(curses.LINES - 2, 2, f"Page {current_page + 1}/{total_pages}")
            stdscr.addstr(curses.LINES - 1, 2, "Use UP/DOWN to move, LEFT/RIGHT to change page, ENTER to select")

        stdscr.refresh()

        # 等待键盘输入
        k = stdscr.getch()

        # 处理键盘输入
        if k == curses.KEY_UP:
            cursor_pos -= 1
            if cursor_pos < 0:
                cursor_pos = min(page_size - 1, total_items - start_node_idx - 1)
        elif k == curses.KEY_DOWN:
            cursor_pos += 1
            if cursor_pos >= min(page_size, total_items - start_node_idx):
                cursor_pos = 0
        elif k == curses.KEY_LEFT and current_page > 0:
            current_page -= 1
            cursor_pos = 0
        elif k == curses.KEY_RIGHT and current_page < total_pages - 1:
            current_page += 1
            cursor_pos = 0

    # 返回选中的节点信息
    selected_idx = current_page * page_size + cursor_pos
    current_node_idx = 0
    for group in groups:
        for node in group['proxies']:
            if current_node_idx == selected_idx:
                return node  # 返回选中的节点的详细信息
            current_node_idx += 1

def main(stdscr, filepath):
    # 读取 YAML 配置文件
    data = load_yaml(filepath)
    
    # 提取节点和分组信息
    groups = extract_proxies_and_groups(data)

    if not groups:
        stdscr.addstr(0, 0, "No proxy groups found in the YAML file.")
        stdscr.refresh()
        stdscr.getch()
    else:
        # 显示节点选择界面并保存选中的节点信息
        selected_node = display_nodes(stdscr, groups)
        stdscr.clear()

        # 在这里，我们将选中的节点保存到一个变量中，可以在这里使用它
        selected_node_info = selected_node  # 选中的节点详细信息保存在此变量中

        # 显示选中的节点信息
        stdscr.addstr(0, 0, f"You selected: {selected_node_info['name']}")
        stdscr.addstr(1, 0, f"Details: {selected_node_info}")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    # 替换为实际的 YAML 文件路径
    filepath = "node_info.yaml"
    curses.wrapper(main, filepath)





