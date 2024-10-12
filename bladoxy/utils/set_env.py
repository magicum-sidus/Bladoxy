import bladoxy

import os


def set_environment_variables(ss_port,privoxy_port,init = False):
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    

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

