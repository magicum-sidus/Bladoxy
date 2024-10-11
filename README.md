# SSPrivoxy V1.2.0 一键安装使用说明

Author *：M.S.*

*Tips：安装脚本文件位于发行版（ Releases ）中。*

***技术路线：Shadowsocks（作为客户端连接购买 Airport 的 SS 节点）+ privoxy（将 http 和 https 请求转为 socks 请求）+ 设置 proxy 系统环境变量***

> #### SSPrivoxy 即将更名为：Bladoxy（Blade+Proxy）
> #### v1.2.0 最新支持功能：自动循环检测可用端口（避免多用户进程冲突）

### 一、准备

1. 购买一个机场账号，有可用的 SS 节点。
2. 下载节点配置文件，其中一个节点一般长下面这样（下面不是真实的节点信息，只展示格式），后面要使用这些信息：

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

### 二、安装脚本说明

安装脚本有两个：

1）联网安装脚本：`SSPrivoxy-nolocal.sh`​

2）联网/本地安装脚本：`SSPrivoxy-install.sh`​

联网/本地安装脚本无需连接网络、无需下载即可安装，安装便捷快速，但是占用空间较大，可根据实际情况选用。

### 三、用法

执行之前需要给shell脚本增加执行权限，下面以 ```SSPrivoxy-install.sh``` 为例。

**下面命令二选一：**

```bash
chmod +x ./SSPrivoxy-install.sh
source ./SSPrivoxy-install.sh <install|install-local|uninstall|run|modify|stop>
```

```bash
chmod +x ./SSPrivoxy-install.sh
./SSPrivoxy-install.sh <install|install-local|uninstall|run|modify|stop>
source ~/.bashrc
```
> ## **重要！！！**

请在安装、运行、更换节点、停止、卸载以后确保执行 ```source ~/.bashrc``` 或者使用 ```source``` 执行脚本。

也就是说，每次执行脚本后请确保正确加载 ```~/.bashrc``` 文件。

**一般的操作步骤是：**

安装（install or install-local）一次以后无需再次安装，第一次安装自动运行所有进程。进程一直在后台运行，每次登录账号无需额外操作都可直接访问外部网络。可按需关闭（stop）进程，需要时再运行（run）进程，无用时可卸载（uninstall）。支持修改 SS 节点（modify）。

### 四、参数选项

##### A. `install (联网安装)`​

所有需要编译的源代码都通过网络下载，进行编译安装。运行中途需要粘贴 SS 节点信息（如第一节准备中所示）（整个粘贴到命令行即可，只粘贴一个节点的信息），然后按 `Ctrl+D`​ 结束输入（按2次，观察到程序继续运行即可）。

##### B. `install-local (离线本地安装)`​

所有需要编译的源代码都已本地打包，无需下载即可编译安装。粘贴 SS 节点操作同上。

##### C. `uninstall (卸载)`​

卸载所有安装文件，删除所有环境变量，卸载 Python 环境。

##### D. `run (运行SSPrivoxy)`​

运行 `Shadowsocks`​ 和 `Privoxy`​ 进程，添加 `Proxy`​ 环境变量。

##### E. `modify (修改 SS 节点)`​

修改节点操作同安装过程中输入 SS 节点信息的操作。修改节点后自动运行新进程，可直接使用切换后的节点。

##### F. `stop (停止进程)`​

停止 `Shadowsocks`​ 和 `Privoxy`​ 进程，删除 `Proxy`​ 环境变量。

### 五、测试

每次安装、运行之后脚本自动进行网络测试，如果看到：`成功访问到外网，并且测试文件已下载。`​ ，就可以正常使用SSPrivoxy。

也可以随时自行测试，测试代码：

```bash
curl -I www.google.com
wget https://huggingface.co/moka-ai/m3e-base/resolve/main/README.md?download=true
```

第一条命令有返回值且第二条命令成功下载文件，即成功访问到外部网络。

### 六、SSPrivoxy V1 开发路线

- [x] shadowsock补丁
- [x] 支持安装、运行、更换节点（单节点）、停止、卸载操作
- [x] 环境检测
- [x] 支持本地安装（无需联网）
- [x] 数据持久化（环境变量正确写入和移除）
- [x] 自动循环检测可用端口（避免多用户进程冲突）
- [ ] 支持脚本自动更新功能 -> 打包为pip包，采用pip系统更新
- [ ] 支持多种加密算法
- [ ] 支持多节点切换
- [ ] 读取 yaml 多节点配置文件，托管远程节点配置文件
- [ ] 自动刷新环境变量
- [ ] 支持配置多种路由规则，视编程环境自动切换
- [ ] 支持多种节点类型 -> 除ss节点类型之外的其他节点
- [ ] Coming soon……

### 七、致谢

SSPrivoxy 使用了以下开源项目：
- shadowsocks 由 [https://shadowsocks.org/](https://shadowsocks.org/)

- privoxy 由 [https://www.privoxy.org/](https://www.privoxy.org/)

  我们对这些项目对开源社区的贡献表示感谢。

> ### FAQ
>
> 1. Q：为什么程序没有按照预期行为运行？
>
>    A：重要的事情只说一遍：记得运行完成执行 ```source ~/.bashrc``` ！！！
>
> 2. Q：为什么报 "jq 命令找不到" 错误？
>
>    A：请更新conda到最新版本（最新版conda自带 jq 命令），并在base环境下执行安装脚本。
>
> 3. Q：我应该选择哪个安装脚本？
>
>    A：SSPrivoxy-install.sh 支持离线安装，也就是说无需下载编译所需文件，建议选择这个同时使用 install-local 参数安装。
>
>    SSPrivoxy-nolocal.sh 仅支持下载安装，速度较慢，优点是占用空间小，方便移植。
>
> 4. Q：按照要求做了还是出现报错怎么办？
>
>    A：我们建议更新到最新版本。我们并没有测试广泛的机器和环境，如果您遇到了安装问题，请提 issue，我们很乐意让我们的作品变得更好。如果您有更好的建议和想法，也请在 issue 中详细说明。
