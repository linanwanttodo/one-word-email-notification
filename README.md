# 随机一言

使用接口盒子 API 获取随机句子的工具，支持 GitHub Actions 每天自动发送。

## 功能特性

- 从接口盒子 API 获取随机句子
- 支持 Server酱 微信推送
- 支持邮件通知（HTML 模板）
- 可选择多种通知方式
- GitHub Actions 自动运行

## 项目结构

```
suijiyiyan/
├── main.py                      # 主程序
├── api.py                       # 一言 API 接口
├── serverchan.py                # Server酱 通知
├── email_sender.py              # 邮件通知
├── email_template.html          # 邮件 HTML 模板
├── requirements.txt             # Python 依赖
├── .env                         # 环境变量配置
├── .env.example                 # 环境变量示例
├── README.md                    # 项目文档
├── .gitignore                   # Git 忽略
└── .github/workflows/
    └── daily.yml               # GitHub Actions 配置
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写配置：

```bash
cp .env.example .env
```

**必填配置：**
- `NOTIFY_TYPE` - 通知方式（serverchan 和/或 email，多个用逗号分隔）
- `YIYAN_API_ID` - 随机一言 API ID（从 https://www.apihz.cn/ 获取）
- `YIYAN_API_KEY` - 随机一言 API KEY（从 https://www.apihz.cn/ 获取）
- `SERVERCHAN_KEY` - Server酱 SendKey（至少配置一个通知方式）
- `SMTP_*` - 邮件配置（可选）

**随机一言 API 申请：**
1. 访问 https://www.apihz.cn/
2. 注册并登录账户
3. 在个人资料中获取开发者 ID 和 KEY
4. 填写到 `.env` 文件中的 `YIYAN_API_ID` 和 `YIYAN_API_KEY`

### 3. 运行程序

```bash
python main.py
```

### 4. 配置说明

**通知方式：**
```bash
# 只使用 Server酱
NOTIFY_TYPE=serverchan

# 只使用邮件
NOTIFY_TYPE=email

# 同时使用两种方式
NOTIFY_TYPE=serverchan,email
```

**Server酱：**
- 访问 https://sct.ftqq.com/ 获取 SendKey

**邮件：**
- `SMTP_HOST` - SMTP 服务器地址（如 smtp.qq.com）
- `SMTP_PORT` - SMTP 端口（587 或 465）
- `SMTP_USERNAME` - SMTP 用户名
- `SMTP_PASSWORD` - SMTP 密码或授权码
- `EMAIL_FROM` - 发件人邮箱
- `EMAIL_TO` - 收件人邮箱

## GitHub Actions

### 1. Fork 仓库

Fork 本项目到你的 GitHub 账户。

### 2. 添加 Repository Secrets

打开 Fork 后的仓库，进入 **Settings → Secrets and variables → Actions**。

点击 **Repository secrets** 分区下的 **New repository secret** 按钮，添加以下变量：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `NOTIFY_TYPE` | 通知方式（serverchan 和/或 email，多个用逗号分隔） | `email` 或 `serverchan,email` |
| `YIYAN_API_ID` | 随机一言 API ID（接口盒子） | `1158549` |
| `YIYAN_API_KEY` | 随机一言 API KEY（接口盒子） | `fjfjewi24897rguhfw` |
| `SERVERCHAN_KEY` | Server酱 SendKey（可选，仅当使用 serverchan 时） | 从 https://sct.ftqq.com/ 获取 |
| `SMTP_HOST` | SMTP 服务器地址（可选，仅当使用 email 时） | `smtp.qq.com` |
| `SMTP_PORT` | SMTP 端口（可选，仅当使用 email 时） | `587` |
| `SMTP_USERNAME` | SMTP 用户名（可选，仅当使用 email 时） | `example@qq.com` |
| `SMTP_PASSWORD` | SMTP 密码或授权码（可选，仅当使用 email 时） | SMTP 授权码 |
| `EMAIL_FROM` | 发件人邮箱（可选，仅当使用 email 时） | `example@qq.com` |
| `EMAIL_TO` | 收件人邮箱（可选，仅当使用 email 时） | `recipient@qq.com` |

**添加步骤示例：**
1. 点击 "New repository secret" 按钮
2. 在 "Name" 字段输入变量名称（如 `NOTIFY_TYPE`）
3. 在 "Secret" 字段输入对应的值
4. 点击 "Add secret" 保存

### 3. 启用 GitHub Actions

**启用 Actions 功能：**

打开 Fork 后的仓库，进入 **Actions** 选项卡。如果看到黄色的提示条提示需要启用 Workflows，点击 **"I understand my workflows, go ahead and enable them"** 按钮启用 Actions。

**重要：设置 Workflow 权限**

1. 进入仓库的 **Settings → Actions → General** 页面
2. 在 **"Workflow permissions"** 部分，选择 **"Read and write permissions"**
3. 点击 **"Save"** 按钮保存


### 4. 手动测试运行

1. 进入 **Actions** 选项卡
2. 点击左侧的工作流名称（"Daily Yiyan"）
3. 点击右侧的 **"Run workflow"** 按钮
4. 再次点击绿色 **"Run workflow"** 按钮，手动触发任务以验证配置是否成功
5. 你可以点击运行中的工作流查看其执行日志和状态

### 5. 自动运行配置

工作流已配置完成，脚本将按预设时间自动运行。

**运行时间说明：**
- 默认设置在**北京时间上午 8 点**运行
- 由于 GitHub Actions 的计划任务调度机制，实际运行时间可能会有几分钟到几十分钟的延迟，这是正常现象
- 随机延迟的加入也会影响确切的启动时间

**执行逻辑：**
- 脚本会先检查当天是否已成功执行过
- 如果已执行，则跳过后续操作
- 如果未执行，则按照配置的通知方式发送一言

### GitHub Actions 工作流文件

工作流文件位置：`.github/workflows/daily.yml`

你可以根据需要修改运行时间。修改 `cron` 表达式来改变执行时间：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 时间 0:00（对应北京时间 8:00）
```

Cron 表达式格式：`分 小时 日 月 周`
- 第一个 `0` = 0 分
- 第二个 `0` = 0 点（UTC）

北京时间 = UTC 时间 + 8 小时

## 开发说明

### 添加新的通知方式

1. 创建新的通知模块文件（如 `wechat.py`）
2. 实现通知函数，返回 `True`/`False`
3. 在 `main.py` 中导入并集成
4. 更新 `.env.example` 和 `README.md`

### 邮件模板

邮件模板文件：`email_template.html`

可以修改模板样式，但需要保留以下变量：
- `{content}` - 一言内容
- `{date}` - 发送日期

## 常见问题

### 1. Server酱 怎么获取 SendKey？

访问 https://sct.ftqq.com/ ，微信扫码登录后创建推送即可获得。

### 2. QQ 邮箱 SMTP 如何配置？

- 服务器：smtp.qq.com
- 端口：587
- 密码：邮箱设置中的授权码，不是登录密码

### 3. 可以只使用一种通知方式吗？

可以，在 `.env` 文件中设置 `NOTIFY_TYPE=serverchan` 或 `NOTIFY_TYPE=email`。

## 许可证和开源协议

本项目采用 **MIT License** 开源协议。你可以自由使用、修改和分发本项目，但需要保留原始许可证声明。

如果你基于本项目进行二次开发或有任何建议，欢迎联系作者：[Linanwanttodo@outlook.com](mailto:Linanwanttodo@outlook.com)

## 许可证

MIT License
