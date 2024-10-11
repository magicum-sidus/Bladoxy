import argparse

from bladoxy.utils.app_actions.install import install
from bladoxy.utils.app_actions.uninstall import uninstall
from bladoxy.utils.app_actions.run_app import run
from bladoxy.utils.app_actions.stop_app import stop
from bladoxy.utils.nodes import modify_node

# def echo_version_info():
#     print(r"""
#   ____  _           _                 
#  | __ )| | __ _  __| | _____  ___   _ 
#  |  _ \| |/ _` |/ _` |/ _ \ \/ / | | |
#  | |_) | | (_| | (_| | (_) >  <| |_| |
#  |____/|_|\__,_|\__,_|\___/_/\_\\__, |
#                                 |___/ """)

# def install():
#     echo_version_info()
#     print("安装环境...")
#     # Add your installation logic here


# def uninstall():
#     print("正在卸载...")
#     # Add your uninstallation logic here

# def run():
#     echo_version_info()
#     print("运行SSPrivoxy...")
#     # Add your run logic here

# def modify():
#     print("修改节点...")
#     # Add your modify logic here

# def stop():
#     print("正在停止进程...")
#     # Add your stop logic here

def main():
    parser = argparse.ArgumentParser(description="Bladoxy is a linux network assistant.")
    parser.add_argument("action", help="Select the action you want to perform.",
                        choices=["install", "uninstall", "run", "modify", "stop"])
    
    args = parser.parse_args()

    action_map = {
        "install": install,
        "uninstall": uninstall,
        "run": run,
        "modify": modify_node,
        "stop": stop
    }

    action_function = action_map.get(args.action)
    if action_function:
        action_function()

if __name__ == "__main__":
    main()