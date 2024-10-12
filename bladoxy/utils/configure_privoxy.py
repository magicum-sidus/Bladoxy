import bladoxy
from bladoxy.utils.get_available_port import get_available_port

import os



WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)




def configure_privoxy_port(ss_port=1080, privoxy_port=8118, init = False):
    """配置Privoxy"""

    privoxy_configure_file_install = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")

    print(f"Privoxy初始检测端口为：{privoxy_port}")

    available_privoxy_port = get_available_port(privoxy_port)  # 获取可用端口

    print(f"第一个Privoxy可用端口为 {available_privoxy_port}.")

    # 读取文件第794行的内容，获取当前端口号
    with open(privoxy_configure_file_install, 'r') as file:
        lines = file.readlines()


    if not init:
        backup_file = privoxy_configure_file_install + '.bak'
        with open(backup_file, 'w') as backup:
            backup.writelines(lines)

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

        print(f"端口已更新为：{available_privoxy_port}.")
    else:
        print(f"端口已经是：{current_privoxy_port}，无需修改.")

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

        print(f"已更新 privoxy 配置中对应shadowsocks端口。")
    else:
        print("shadowsocks端口已正确配置，无需修改。")

    return available_privoxy_port