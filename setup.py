from setuptools import setup, find_packages
import codecs

with codecs.open('bladoxy/README.md', encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        return [line for line in lines if line.strip() and not line.strip().startswith('#')]

setup(
    name="bladoxy",
    version="1.3.0",
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description="Bladoxy is a linux network assistant.",
    author='Magicum Sidus',
    author_email='your_email@example.com',
    url='https://github.com/magicum-sidus/Bladoxy',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'bladoxy': ['README.md', 'LICENSE', 'modules/dependeencies/pcre/**/*', 'modules/privoxy/**/*'],  
    },
    # install_requires=[
    #     # Add any other dependencies your package requires
    # ],
    install_requires=parse_requirements('bladoxy/requirements.txt'),
    entry_points="""
    [console_scripts]
    bladoxy = bladoxy.cli.cli_app:main
    sslocal = bladoxy.modules.shadowsocks_module.shadowsocks.local:main
    ssserver = bladoxy.modules.shadowsocks_module.shadowsocks.server:main
    """,           # sslocal/ssserver我不希望暴露给用户
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        # Add other relevant classifiers
    ],
    python_requires='>=3.6',
    long_description=long_description,
)

# from setuptools import setup, find_packages
# import codecs
# import os
# from setuptools.command.install import install

# # 自定义安装后钩子类
# class PostInstallCommand(install):
#     """自定义安装后命令"""
#     def run(self):
#         print("Bladoxy 已成功安装！")
#         print("你可以通过命令 'bladoxy' 来启动 Bladoxy 网络助手。")
        
#         # 调用父类的安装方法，确保常规的安装流程完成
#         install.run(self)
        
#         # # 在安装后执行的自定义逻辑
#         # print("Bladoxy 已成功安装！")
#         # print("开始执行安装后的额外操作...")
        
#         # # 你可以在这里添加其他操作，如环境变量设置、文件生成等
#         # # 例如：
#         # # os.system('echo "export MY_VAR=abc" >> ~/.bashrc')
        
#         # # 提示用户如何使用
#         # print("你可以通过命令 'bladoxy' 来启动 Bladoxy 网络助手。")

# # 读取 README.md 作为长描述
# with codecs.open('README.md', encoding='utf-8') as f:
#     long_description = f.read()

# setup(
#     name="bladoxy",
#     version="1.3.0",
#     license='http://www.apache.org/licenses/LICENSE-2.0',
#     description="Bladoxy is a linux network assistant.",
#     author='Magicum Sidus',
#     author_email='your_email@example.com',
#     url='https://github.com/magicum-sidus/Bladoxy',
#     packages=find_packages(),
#     include_package_data=True,
#     # package_data={
#     #     'bladoxy': ['README.md', 'LICENSE'],  
#     # },
#     install_requires=[
#         # 在此处添加你的依赖包
#     ],
#     entry_points="""
#     [console_scripts]
#     bladoxy = bladoxy.cli.cli_app:main
#     sslocal = bladoxy.modules.shadowsocks_module.shadowsocks.local:main
#     ssserver = bladoxy.modules.shadowsocks_module.shadowsocks.server:main
#     """,  
#     # 注意：sslocal/ssserver 暂时还是会暴露给用户（你可以通过其他方式隐藏）
    
#     classifiers=[
#         'License :: OSI Approved :: Apache Software License',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: Implementation :: CPython',
#         # 在此处添加其他相关的分类器
#     ],
#     python_requires='>=3.6',
#     long_description=long_description,
    
#     cmdclass={
#         'install': PostInstallCommand,  # 使用自定义的安装钩子类
#     },
# )