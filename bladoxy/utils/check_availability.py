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
import tempfile
import urllib.request
import shutil

# 检查能否访问 www.google.com
def check_google_access():
    try:
        response = urllib.request.urlopen("http://www.google.com", timeout=5)
        return response.status == 200
    except:
        return False

# 下载文件
def download_file(url, output_file):
    try:
        urllib.request.urlretrieve(url, output_file)
        return True
    except:
        return False

def check_availability():
    print("执行测试……")

    # 检查是否可以访问 www.google.com
    if check_google_access():
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"创建临时文件夹: {temp_dir}")
            
            # 下载文件到临时文件夹
            download_url = "https://huggingface.co/moka-ai/m3e-base/resolve/main/README.md?download=true"
            temp_file_path = os.path.join(temp_dir, "README.md")
            
            if download_file(download_url, temp_file_path):
                print(f"成功访问到外网，并且测试文件已下载到临时文件夹: {temp_file_path}")
                print("请执行 source ~/.bashrc 刷新环境变量.")
                
                
            else:
                print("无法下载文件，但可以访问 www.google.com。")
    else:
        print("无法访问 www.google.com。")

if __name__ == "__main__":
    check_availability()