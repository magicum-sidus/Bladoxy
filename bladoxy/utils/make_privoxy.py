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
import subprocess
import tarfile
import shutil
from termcolor import colored



import bladoxy
from bladoxy.utils.logger import logger




def run_command(command):
    """Helper function to run a shell command and print its output."""
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    print(colored(result.stdout,'green'))
    return result

def extract_tar_gz(tar_path, extract_to):
    """Extracts a .tar.gz file to a specified directory."""
    logger.info(f"解压缩 {tar_path} 到 {extract_to}")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_to)




def get_first_folder_in_tar(tar_path):
    """Mimic the behavior of 'tar -tf ... | head -n 1 | awk -F "/" '{print $1}''."""
    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()
        if not members:
            return None  # Return None if the tar file is empty
        first_member = members[0]
        # Ensure the path is not empty and contains at least one '/'
        if '/' in first_member.name:
            return first_member.name.split('/')[0]
        else:
            return first_member.name  # If it's a flat file, return the file name directly
            

def clear_directory(directory):
    if os.path.exists(directory):
        logger.info(f"清空路径: {directory}")
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)  # Recreate the directory


def compile_and_install(source_dir, prefix):
    """Runs the standard ./configure, make, make install commands."""
    logger.info(f"从 {source_dir} 编译安装")
    os.chdir(source_dir)
    run_command(f"./configure --prefix={prefix}")
    run_command("make")
    run_command("make install")


def modify_privoxy_compile_config(privoxy_source_dir,pcre_install_dir,zlib_install_dir):
    logger.info("修改编译配置文件")

    # 配置文件路径
    PRIVOXY_CONFIGURE_FILE = os.path.join(privoxy_source_dir,"configure.in")

    # 期望的第874行内容
    EXPECTED_LINE_3 = 'AC_CHECK_LIB(pcre, pcre_compile, ['

    # 读取配置文件的所有行
    with open(PRIVOXY_CONFIGURE_FILE, 'r') as file:
        lines = file.readlines()
        ACTUAL_LINE_3 = lines[873].strip()  # 注意：第874行的索引为873

    # 如果第874行与期望不符，进行修改
    if ACTUAL_LINE_3 != EXPECTED_LINE_3:

        # 需要插入的文本
        TEXT_TO_ADD = [
            f'CPPFLAGS="$CPPFLAGS -I{pcre_install_dir}/include"\n',
            f'LDFLAGS="$LDFLAGS -L{pcre_install_dir}/lib"\n'
        ]

        # 备份原文件
        backup_file = PRIVOXY_CONFIGURE_FILE + '.bak'
        shutil.copy(PRIVOXY_CONFIGURE_FILE, backup_file)

        try:
            # 在第871行后插入两行文本
            lines[871:871] = TEXT_TO_ADD  # 在第871行后插入

            # 写回插入后的修改内容
            with open(PRIVOXY_CONFIGURE_FILE, 'w') as file:
                file.writelines(lines)

            logger.info(f"成功将pcre路径添加到 {PRIVOXY_CONFIGURE_FILE} 中")
        except Exception as e:
            logger.error(f"未能将pcre路径添加到 {PRIVOXY_CONFIGURE_FILE} 中: {e}")

        # 重新读取文件内容（确保包括刚刚插入的两行）
        with open(PRIVOXY_CONFIGURE_FILE, 'r') as file:
            modified_lines = file.readlines()

        # 修改第1071行的内容（索引为1070）
        try:
            new_line_1071 = f'AC_CHECK_LIB(z, zlibVersion, [have_zlib="yes"], [have_zlib="no"], [-L{zlib_install_dir}/lib])\n'

            # 更新第1071行
            modified_lines[1070] = new_line_1071

            # 写回文件
            with open(PRIVOXY_CONFIGURE_FILE, 'w') as file:
                file.writelines(modified_lines)

            logger.info(f"成功将zlib路径添加到 {PRIVOXY_CONFIGURE_FILE} 中")
        except Exception as e:
            logger.error(f"未能将zlib路径添加到 {PRIVOXY_CONFIGURE_FILE} 中: {e}")


# def compile_and_install_privoxy(privoxy_source_dir,privoxy_install_dir,zlib_install_dir):
#     logger.info("正在编译安装privoxy")
#     os.chdir(privoxy_source_dir)
#     # 运行 autoheader 和 autoconf
#     try:
#         subprocess.run(['autoheader'], check=True)
#         subprocess.run(['autoconf'], check=True)
#     except subprocess.CalledProcessError as e:
#         logger.error(f"运行 autoheader 或 autoconf 失败: {e}")
#         return

#     # 设置 CPPFLAGS 和 LDFLAGS 环境变量
#     env = os.environ.copy()
#     env['CPPFLAGS'] = f'{env.get("CPPFLAGS", "")} -I{zlib_install_dir}/include'
#     env['LDFLAGS'] = f'{env.get("LDFLAGS", "")} -L{zlib_install_dir}/lib'

#     # 运行 ./configure, make 和 make install
#     try:
#         # 配置 Privoxy
#         subprocess.run(
#             ['./configure', f'--prefix={privoxy_install_dir}'],
#             check=True,
#             env=env
#         )

#         # 编译
#         subprocess.run(['make'], check=True)

#         # 安装
#         subprocess.run(['make', 'install'], check=True)

#         logger.info("Privoxy 编译安装成功")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"编译或安装 Privoxy 失败: {e}")


def compile_and_install_privoxy(privoxy_source_dir, privoxy_install_dir, zlib_install_dir):
    logger.info("正在编译安装privoxy")
    os.chdir(privoxy_source_dir)

    def run_command(command, env=None):
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, env=env)
            print(colored(result.stdout, 'green'))
        except subprocess.CalledProcessError as e:
            print(colored(e.stderr, 'red'))
            logger.error(f"运行 {command} 失败: {e}")
            return False
        return True

    # Run autoheader and autoconf
    if not run_command(['autoheader']):
        return
    if not run_command(['autoconf']):
        return

    # Set CPPFLAGS and LDFLAGS environment variables
    env = os.environ.copy()
    env['CPPFLAGS'] = f'{env.get("CPPFLAGS", "")} -I{zlib_install_dir}/include'
    env['LDFLAGS'] = f'{env.get("LDFLAGS", "")} -L{zlib_install_dir}/lib'

    # Run ./configure, make, and make install
    if not run_command(['./configure', f'--prefix={privoxy_install_dir}'], env=env):
        return
    if not run_command(['make']):
        return
    if not run_command(['make', 'install']):
        return

    logger.info("Privoxy 编译安装成功")



def make_privoxy():
    WORKING_DIRECTORY = os.path.dirname(bladoxy.__file__)

    # M4
    logger.info("解压m4源代码")
    m4_tar_path = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','m4-latest.tar.gz')
    EXTRACT_TARGET_PATH = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','extract_targets')
    if not os.path.isdir(EXTRACT_TARGET_PATH):
        os.makedirs(EXTRACT_TARGET_PATH, exist_ok=True)


    clear_directory(EXTRACT_TARGET_PATH)

    extract_tar_gz(m4_tar_path, EXTRACT_TARGET_PATH)
    
    m4_folder_name = get_first_folder_in_tar(m4_tar_path)
    m4_source_dir = os.path.join(EXTRACT_TARGET_PATH,m4_folder_name)

    DEPENDENCIES_DIR = os.path.join(WORKING_DIRECTORY,'modules','dependencies')
    if not os.path.isdir(DEPENDENCIES_DIR):
        os.makedirs(DEPENDENCIES_DIR, exist_ok=True)


    clear_directory(DEPENDENCIES_DIR)
    
    logger.info("正在编译安装m4")
    m4_install_dir = os.path.join(DEPENDENCIES_DIR,'m4')
    compile_and_install(m4_source_dir, m4_install_dir)
    
    os.environ["PATH"] += f":{m4_install_dir}/bin"

    # Autoconf
    logger.info("解压autoconf源代码")
    
    autoconf_tar_path = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','autoconf-latest.tar.gz')
    extract_tar_gz(autoconf_tar_path, EXTRACT_TARGET_PATH)
    
    autoconf_folder_name = get_first_folder_in_tar(autoconf_tar_path)
    autoconf_source_dir = os.path.join(EXTRACT_TARGET_PATH,autoconf_folder_name)
    
    logger.info("正在编译安装autoconf")
    autoconf_install_dir = os.path.join(DEPENDENCIES_DIR,'autoconf')
    compile_and_install(autoconf_source_dir, autoconf_install_dir)
    
    os.environ["PATH"] += f":{autoconf_install_dir}/bin"

    # PCRE
    logger.info("解压pcre源代码")
    
    pcre_tar_path = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','pcre-8.44.tar.gz')
    extract_tar_gz(pcre_tar_path, EXTRACT_TARGET_PATH)
    
    pcre_folder_name = get_first_folder_in_tar(pcre_tar_path)
    pcre_source_dir = os.path.join(EXTRACT_TARGET_PATH,pcre_folder_name)
    
    logger.info("正在编译安装pcre")
    pcre_install_dir = os.path.join(DEPENDENCIES_DIR,'pcre')
    compile_and_install(pcre_source_dir, pcre_install_dir)

    # Zlib
    logger.info("解压zlib源代码")
    
    zlib_tar_path = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','zlib-1.3.1.tar.gz')
    extract_tar_gz(zlib_tar_path, EXTRACT_TARGET_PATH)
    
    zlib_folder_name = get_first_folder_in_tar(zlib_tar_path)
    zlib_source_dir = os.path.join(EXTRACT_TARGET_PATH,zlib_folder_name)
    
    logger.info("正在编译安装zlib")
    zlib_install_dir = os.path.join(DEPENDENCIES_DIR,'zlib')
    compile_and_install(zlib_source_dir, zlib_install_dir)

    # Privoxy
    logger.info("解压privoxy源代码")
    
    privoxy_tar_path = os.path.join(WORKING_DIRECTORY,'modules','dependencies_src','privoxy-3.0.34-stable-src.tar.gz')
    extract_tar_gz(privoxy_tar_path, EXTRACT_TARGET_PATH)
    
    privoxy_folder_name = get_first_folder_in_tar(privoxy_tar_path)
    privoxy_source_dir = os.path.join(EXTRACT_TARGET_PATH,privoxy_folder_name)
    
    modify_privoxy_compile_config(privoxy_source_dir,pcre_install_dir,zlib_install_dir)

    privoxy_install_dir = os.path.join(WORKING_DIRECTORY,'modules','privoxy')
    if not os.path.isdir(privoxy_install_dir):
        os.makedirs(privoxy_install_dir, exist_ok=True)

    clear_directory(privoxy_install_dir)
    compile_and_install_privoxy(privoxy_source_dir,privoxy_install_dir,zlib_install_dir)



if __name__ == "__main__":
    make_privoxy()
