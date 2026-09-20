# 1Password 7 Chrome 扩展 · 社区优化版

**通过 Manifest V3 扩展，继续配合现有的 1Password 7 桌面版使用。**

[English](README.md) · [更新记录](CHANGELOG.md) · [下载 ZIP](https://github.com/PM100Fun/1password7-chrome-extension/archive/refs/heads/master.zip)

这是基于 [ferreirafabio/1password7-chrome-extension](https://github.com/ferreirafabio/1password7-chrome-extension) 维护的非官方分支，重点是把 macOS 上可用的配置方法整理成可复现的流程，并修复实际代码问题。

## 我们更新了什么？

核对发现，本机原有扩展代码与上游一致；实际使用的通信 host 与上游 README 的说明不一致。此次版本 `4.7.5.91` 做了这些改进：

1. **修正安装文档中的 host 名称。** 按当前代码真实请求的 `2bua8c4s2c.com.agilebits.1password` 配置，避免改了另一个白名单却仍无法连接。
2. **新增配置检查与修复工具。** 默认只读；只有加上 `--apply` 才修改。修改前备份，保留已有白名单与其他字段，并检查 helper 文件是否存在。
3. **修复隐藏/禁用输入框的图标遗漏。** 原来过早标记“已处理”，显示后也不会补图标；现在保留重试资格，在用户聚焦时再次尝试。
4. **修复行内点击的成功状态。** 工具栏处理函数不可用时不再返回成功。
5. **补充中英文 README、更新记录和回归测试。** 保留原扩展公钥与 ID，不新增扩展权限。

Manifest V3 迁移、行内图标、原有两步登录与填充逻辑来自上游，不作为本分支新发明的功能。未来浏览器兼容性不能保证“永久可用”。

## 安装：macOS + Google Chrome

前提：已安装并合法使用 1Password 7 桌面版，且桌面版具备浏览器集成功能。配置工具需要 Python 3，扩展本身无需构建。

1. 下载 ZIP 并解压，放入不会随意移动/删除的目录。或运行：

   ```sh
   git clone https://github.com/PM100Fun/1password7-chrome-extension.git
   cd 1password7-chrome-extension
   ```

2. 打开 `chrome://extensions`，开启“开发者模式”，点击“加载已解压的扩展程序”，选择含 `manifest.json` 的目录。
3. 核对扩展 ID：`aomjjhallfgjeglblehebfpbcfeobpgk`。它由 manifest 的公开 `key` 决定，不是密码或私钥。若界面显示不同 ID，以实际 ID 为准。
4. 在解压/克隆的项目目录运行检查：

   ```sh
   python3 scripts/configure_native_host.py
   ```

   `OK` 表示无需修改；`MISSING` 表示需要添加白名单，可执行：

   ```sh
   python3 scripts/configure_native_host.py --apply
   ```

   工具会先在原 JSON 同目录生成带时间戳的备份，然后只补充扩展来源。不会读取密码库，不会创建缺失的 host。如果 host 或 helper 不存在，应先修复桌面版安装与浏览器集成。

5. 彻底退出并重新打开 Chrome，打开并解锁 1Password 7，在普通 HTTPS 登录页测试工具栏按钮。

### 手动配置与回滚

当前 `global.min.js` 请求的 host 是：

```text
2bua8c4s2c.com.agilebits.1password
```

macOS Chrome 对应文件：

```text
~/Library/Application Support/Google/Chrome/NativeMessagingHosts/2bua8c4s2c.com.agilebits.1password.json
```

先备份文件，再在现有 `allowed_origins` 数组加入：

```text
chrome-extension://aomjjhallfgjeglblehebfpbcfeobpgk/
```

保留原有来源和桌面版生成的 `path`。只修改 `com.1password.1password7.json` 无法配置本版本实际请求的 host，也不要随意替换成猜测的 SLS helper 路径。

自定义现有文件位置或扩展 ID：

```sh
python3 scripts/configure_native_host.py --host-file '/完整路径/2bua8c4s2c.com.agilebits.1password.json' --extension-id 实际扩展ID
```

检查后需要写入时再加 `--apply`。撤回配置修改时，将工具提示的备份恢复至原文件，再彻底重启 Chrome。退出码：`0` 已正常/已更新，`1` 缺少白名单，`2` 配置缺失或无效。

## 常见问题

| 现象 | 处理方式 |
| --- | --- |
| 找不到 native messaging host | 检查上面的准确文件名，以及 JSON 中 `path` 指向的 helper 是否存在。 |
| 访问 host 被禁止 | 在正确 host 的白名单中加入实际扩展 ID，并彻底重启 Chrome。 |
| 点击图标无响应 | 检查桌面版运行/解锁状态、浏览器集成与扩展 service worker 错误。 |
| 隐藏表单显示后没有图标 | 聚焦对应输入框，本版本会重试创建图标。 |
| 在浏览器内部页面无法使用 | 改用普通 HTTP/HTTPS 页面测试。 |
| 两步登录没有继续填充 | 在密码步骤再次点击工具栏；上游自动弹窗/填充行为保留，效果依网站而异。 |

## 验证范围

维护者反馈原 macOS 安装可用；本次核对了原代码与上游的一致性、本地 host 名称、白名单和 helper 文件存在性。配置工具及 JavaScript 改动有自动化测试，详见[验证记录](docs/VALIDATION.md)。

**本次更新后的真实密码填充尚未重新端到端验收。Windows、Linux、其他 Chromium 浏览器均未验证。** 配置脚本默认针对 macOS Chrome；传入其他路径不代表已支持其他平台。

扩展会从桌面版接收用于填充的凭据，并继承上游的 HTTP/HTTPS 页面访问权限。本分支没有增加遥测或外部服务。请勿在问题反馈中提供真实密码、密码库导出或未脱敏的凭据。

## 开发与反馈

使用 Python 3 和 Node.js 18+ 执行：

```sh
python3 -m unittest discover -s tests -v
node --test tests/extension.test.cjs
node --check background.js
node --check inline-icon.js
```

欢迎提交问题和改进，反馈时附上系统、Chrome、1Password 版本、复现步骤及脱敏错误。如果这个项目帮你继续使用现有环境，欢迎点一个 Star，让有同样需求的人更容易找到它。

## 来源与许可

原始扩展、资源和商标属于 AgileBits / 1Password；Manifest V3 迁移、行内图标及原有兼容工作来自上游作者 **ferreirafabio**。本分支的配置工具、修复和中英文文档由 **PM100Fun** 维护。

社区原创代码及修改保留 [GPL-3.0](LICENSE) 许可。按上游说明，`global.min.js`、`injected.min.js`、语言包及资源保留 AgileBits 原始权属，本分支不对这些内容重新授权；`ext/sjcl.js` 等第三方声明原样保留。本项目非官方，与 1Password 无隶属或背书关系。
