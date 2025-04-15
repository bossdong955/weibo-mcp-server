# weiboresou-mcp-server

一个获取前N微博热搜的MCP服务，支持stdio和sse模式调用。

## 配置方式

### stdio模式
配置文件内容如下：
```json
{
  "mcpServers": {
    "weiboresou": {
      "disabled": false,
      "timeout": 60,
      "command": "conda",
      "args": [
        "run",
        "-n",
        "mcp",
        "--no-capture-output",
        "mcp",
        "run",
        "文件的绝对路径/resou_stdio.py"
      ],
      "transportType": "stdio"
    }
  }
}
```
在vscode中下载`cline`插件并配置`Installed`服务 ，将上面`json`粘贴到配置文件即可。

![image2](assets/image2.png)

### sse模式

首先运行`python`程序

```
python resou_sse.py
```

在vscode中下载`cline`插件并配置`Remote Servers`服务 ，ip和端口根据实际情况设置。

![image.png](assets/image.png)