import bladoxy
import os


def remove_files():
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)

    files_to_remove = [
        os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.json'),
        os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.log'),
        os.path.join(WORKING_DIRECTORY, 'modules','shadowsocks_config','shadowsocks.pid'),
        os.path.join(WORKING_DIRECTORY, 'nodes_profiles','all_nodes_info.json'),
        os.path.join(WORKING_DIRECTORY, 'nodes_profiles','name_index_mapping.json'),
        os.path.join(WORKING_DIRECTORY, 'nodes_profiles','nodes_profile.yaml')
    ]

    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed {file_path}")
            else:
                print(f"File {file_path} does not exist")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")



def finalize():
    print("正在卸载...")
    # 删除文件
    remove_files()