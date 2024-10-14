# ⚔️Bladoxy (原SSprivoxy) V1.4.3 使用说明

Author *：M.S.*

*LICENSE：Apache 2.0*

*Tips：请务必在每次执行命令后执行 source ～/.bashrc*



> #### SSPrivoxy 从 v1.3.0 已更名为：Bladoxy（⚔️Blade+Proxy）（刀锋代理）
> #### v1.2.0 最新支持功能：自动循环检测可用端口（避免多用户进程冲突）
>
> #### v1.3.0 最新支持功能：更新机制，代码全部迁移到 pypi平台，可以使用 pip 机制安装、卸载、更新
>
> #### v1.4.0最新支持功能：支持上传节点文件，并用光标可视化翻页、选择节点



### 一、准备

1. 购买一个机场账号，有可用的 SS 节点。（目前只支持SS节点，后续会支持更多节点类型）
2. 下载节点配置文件（clash yaml格式），其中一个节点一般长下面这样（下面不是真实的节点信息，只展示格式）

    ```yaml
    name: 'Canada Quebec Montreal Beauharnois 10GE0/0/27 DELLR6515 F05'
        type: ss
        server: ca05.kp.wf
        port: 19313
        cipher: aes-256-cfb
        password: MG34Sd
        udp: true
    ```
3. 一个linux普通用户账号，要求安装 Anaconda Python 环境，gcc、 g++ 以及 make 工具。

### 二、安装说明

从 SSprivoxy 升级的用户，请先卸载 SSprivoxy.

执行命令:

```bash 
ssprivoxy uninstall
```

通过 pip 安装、更新、卸载:

1）安装：

```bash
# 请选择 3.5-3.9 的 python 版本
conda create -n bladoxy python=3.9
conda activate bladoxy
pip install bladoxy
# 安装后一定要初始化 Bladoxy，必须在同一个 conda 环境
# 安装时需要输入节点文件路径，请提前准备好！
bladoxy init
# 务必刷新环境变量
source ~/.bashrc
```

2）更新：

```bash
bladoxy cleanup
pip -U install bladoxy
bladoxy init
source ~/.bashrc
```

3）卸载：

```bash
bladoxy cleanup
pip uninstall bladoxy
source ~/.bashrc
```

### 三、参数用法

下面命令选择一个执行:

```bash
bladoxy init
bladoxy cleanup
bladoxy run
bladoxy stop
bladoxy uptProf
bladoxy uptNode
```

> init ：初始化程序。
> cleanup ：清理卸载所有资源。
> run ：启动主程序。
> stop ：停止所有正在运行的进程。
> uptProf ：更新用户节点配置文件。
> uptNode ：切换节点。

切换节点时：

> 上下键（或者鼠标滚轮）切换同一页的节点，左右键翻页



> ## **重要！！！**

请在初始化、启动、更换节点、停止进程、清理以后确保执行 ```source ~/.bashrc``` 

也就是说，每次执行命令请确保正确加载 ```~/.bashrc``` 文件。

### 四、测试

初始化结束后程序自动进行网络测试，如果看到：`成功访问到外网，并且测试文件已下载到临时文件夹` ，就可以正常使用Bladoxy。

也可以随时自行测试，测试代码：

```bash
curl -I www.google.com
wget https://huggingface.co/moka-ai/m3e-base/resolve/main/README.md?download=true
```

第一条命令有返回值且第二条命令成功下载文件，即成功访问到外部网络。

### 五、Bladoxy V1 开发路线

- [x] shadowsock补丁
- [x] 支持安装、运行、更换节点（单节点）、停止、卸载操作
- [x] 环境检测
- [x] 支持本地安装（无需联网）
- [x] 数据持久化（环境变量正确写入和移除）
- [x] 自动循环检测可用端口（避免多用户进程冲突）
- [x] 支持脚本自动更新功能 -> 打包为pip包，采用pip系统更新
- [x] 支持多节点切换
- [x] 读取 yaml 多节点配置文件
- [ ] 支持多种加密算法
- [ ] 托管远程节点配置文件
- [ ] 支持配置多种路由规则，视编程环境自动切换
- [ ] 支持多种节点类型 -> 除ss节点类型之外的其他节点
- [ ] Coming soon……

### 六、致谢

Bladoxy 使用了以下开源项目：
- shadowsocks 由 [https://shadowsocks.org/](https://shadowsocks.org/)

- privoxy 由 [https://www.privoxy.org/](https://www.privoxy.org/)

  我们对这些项目对开源社区的贡献表示感谢。

> ### FAQ
>
> 1. Q：为什么程序没有按照预期行为运行？
>
>    A：重要的事情只说一遍：记得运行完成执行 ```source ~/.bashrc``` ！！！
>
> 4. Q：按照要求做了还是出现报错怎么办？
>
>    A：我们建议更新到最新版本。我们并没有测试广泛的机器和环境，如果您遇到了安装问题，请提 issue，我们很乐意让我们的作品变得更好。如果您有更好的建议和想法，也请在 issue 中详细说明。
