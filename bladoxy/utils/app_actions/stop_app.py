import os
from bladoxy.utils.kill_process import kill_possible_processes

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



def stop():
    print("正在停止进程...")
    # 定义开始和结束标记
    START_MARKER_PROXY = "######## START MY_PROXY ########"
    END_MARKER_PROXY = "######## END MY_PROXY ########"

    # 获取用户的 home 目录并拼接 .bashrc 文件路径
    home_dir = os.path.expanduser("~")
    bashrc_path = os.path.join(home_dir, ".bashrc")

    # 从 .bashrc 文件中删除代理环境变量
    remove_proxy_from_bashrc(bashrc_path, START_MARKER_PROXY, END_MARKER_PROXY)
    kill_possible_processes()
    print("成功停止进程")