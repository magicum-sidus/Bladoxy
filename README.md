# SSPrivoxy V1.1.0 一键安装使用说明

Author *：M.S.*

*Tips：安装脚本文件位于发行版（ Releases ）中。*

***技术路线：Shadowsocks（作为客户端连接购买 Airport 的 SS 节点）+ privoxy（将 http 和 https 请求转为 socks 请求）+ 设置 proxy 系统环境变量***

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
3. 一个linux普通用户账号，要求安装 Anaconda Python 环境，gcc 以及 make 工具。

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
请在安装、运行、停止、卸载以后确保执行 ```source ~/.bashrc``` 或者使用 ```source``` 执行脚本

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
