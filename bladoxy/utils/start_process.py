import subprocess
import bladoxy
import os



def start_sslocal():
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)
    shadowsocks_config_directory = os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config')
    config_file = os.path.join(shadowsocks_config_directory,'shadowsocks.json')
    pid_file = os.path.join(shadowsocks_config_directory,'shadowsocks.pid')
    log_file = os.path.join(shadowsocks_config_directory,'shadowsocks.log')
    
    command = [
        "sslocal",
        "-c", config_file,
        "--pid-file", pid_file,
        "--log-file", log_file,
        "-d", "start"
    ]
    
    try:
        # 调用命令行工具
        subprocess.run(command, check=True)
        print("sslocal started successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start sslocal: {e}")



def start_privoxy():
    # 打印启动消息
    print("正在启动privoxy……")

    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)

    
    # 设置 LD_LIBRARY_PATH 环境变量
    pcre_lib_path = os.path.join(WORKING_DIRECTORY, "modules", "dependencies", "pcre", "lib")
    os.environ["LD_LIBRARY_PATH"] = f"{pcre_lib_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"

    # 拼接 privoxy 可执行文件的路径
    privoxy_executable_path = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "sbin", "privoxy")

    # 构建 privoxy 配置文件的路径
    privoxy_config_path = os.path.join(WORKING_DIRECTORY, "modules", "privoxy", "etc", "config")

    # 启动 privoxy
    try:
        subprocess.run([privoxy_executable_path, privoxy_config_path], check=True)
        print("privoxy已经启动")
    except subprocess.CalledProcessError as e:
        print(f"启动 privoxy 时出错: {e}")