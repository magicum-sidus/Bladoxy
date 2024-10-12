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