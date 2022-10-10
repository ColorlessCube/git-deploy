## 背景

在开发项目时，涉及人员比较多，代码推送频繁。项目代码每次更新，需要在测试环境重部署项目，以便相关人员测试。有没有什么方法能让 push 代码后项目可以自动化部署呢？参考了 CI/CD 相关资料，发现 Git 的 Webhook 机制可以帮助实现这项任务。

Git 提供的 Webhook 机制，简单来说就是一种反向 API 机制，类似于触发器的一样。对于 Git 而言，push、merge 等事件就是触发器，而项目的自动化重部署就是需要触发的动作。只需要将动作封装成 API 提供给 Git，那么在 Git 触发相应事件 时，就会通过 Webhook 来回调服务。

## 安装

项目目录下：

```bash
# 安装虚拟环境及依赖
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
# 启动项目
chmod a+x deploy
chmod a+x gunicorn.config.py
bash deploy start
```

## 使用

### 配置项目

- 名称：项目名称，需要与 gitlab 中仓库的名称保持一致；
- 仓库：仓库的 url，免密拉取仓库设置 `SSH URL`，如`git@10.124.5.195:sp-dev/deploy.git`；账号密码拉取仓库设置 `HTTP URL`，如`http://10.124.5.195/sp-dev/deploy.git`；
- 分支：触发 Webhook 的分支，在 Webhook 设置页面设置；
- token：验证 Webhook 的 token，在 Webhook 设置页面设置；
- username：拉取项目时的 gitlab 账户信息，已经设置免密拉取仓库时可为空；
- password：拉取项目时的 gitlab 账户密码信息，已经设置免密拉取仓库时可为空。

### 配置 server

- 主机：server 的 IP 地址；
- username：登录 server 的账户；
- password：登录 server 的密码；
- 本地仓库目录：该项目在本 server 中的 git 本地仓库目录；
- 重部署命令：重新部署该项目的一系列 shell 命令，可能包含：文件的更新、项目的重启动；
- *检查命令：检查项目是否重部署成功，需要 git deploy 对状态信息进行校验。

## 环境

|      |           地址           |       版本        | 数据库 |
| :--: | :----------------------: | :---------------: | :----: |
| 上海 | http://10.124.5.199:3668 | V 0.1.221010_beta | SQLite |
| 北京 |  http://10.124.205.218   | V 0.1.221010_beta | SQLite |

## 版本

### V 0.1.221010_beta

#### 完成

- 完成 git deploy 的基本功能，需要继续测试；

#### 待办

- 完成项目部署完成后的状态检查，需要适配各种状态信息的检验；