# 随机一言

每天定时获取一句随机一言，通过 Server酱（微信）和/或 邮件 推送，使用 GitHub Actions 自动运行。

## 支持的句子接口

| 来源 | `YIYAN_SOURCE` 值 | 是否需要密钥 | 说明 |
|------|-------------------|-------------|------|
| 接口盒子（默认） | `apihz` | 需要 | 12 万不重复语录库，需到 https://www.apihz.cn/ 注册获取 ID/KEY |
| 一言 hitokoto | `hitokoto` | 不需要 | 文学/诗词/影视句子，附出处，免注册直接调用 |

**切换方式：** 设置环境变量 `YIYAN_SOURCE=hitokoto` 即切换到一言源（无需任何密钥）；不设置默认走接口盒子。

## 本地运行

```bash
pip install -r requirements.txt
cp .env.example .env   # 编辑 .env 填写配置
python main.py
```

环境变量说明见 `.env.example` 内注释。

## GitHub Actions

1. Fork 仓库后，进入 **Settings → Secrets and variables → Actions** 添加 secrets：

| Secret | 必填 | 说明 |
|--------|------|------|
| `NOTIFY_TYPE` | 是 | 通知方式：`serverchan` / `email`，多个逗号分隔 |
| `YIYAN_SOURCE` | 否 | 句子接口：`apihz`（默认）/ `hitokoto` |
| `YIYAN_API_ID` / `YIYAN_API_KEY` | 仅 apihz | 接口盒子开发者 ID/KEY |
| `SERVERCHAN_KEY` | 用 serverchan 时 | 从 https://sct.ftqq.com/ 获取 |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USERNAME` / `SMTP_PASSWORD` / `EMAIL_FROM` / `EMAIL_TO` | 用 email 时 | SMTP 邮件配置 |

2. 在 Actions 选项卡启用 workflow，手动 **Run workflow** 测试一次。

定时任务默认北京时间早 8 点运行（GitHub 调度可能有延迟），可修改 `.github/workflows/daily.yml` 中的 `cron` 表达式调整时间。

> 注意：`EMAIL_TO` 支持逗号分隔的多收件人。

## 项目结构

```
├── main.py                    # 入口
├── app/
│   ├── api.py                 # 一言接口（多源适配，见 SOURCES 注册表）
│   └── notifiers/
│       ├── serverchan.py      # Server酱 推送
│       └── email_sender.py    # 邮件推送
├── templates/
│   └── email_template.html    # 邮件模板（保留 {content} {date} 变量）
└── .github/workflows/
    └── daily.yml              # 定时任务
```

**添加新的句子接口：** 在 `app/api.py` 中实现一个 `_get_xxx()` 函数（返回 `{'text', 'tips'}` 或 `None`），登记到 `SOURCES` 注册表，并在 `.env.example` 和本文件补充说明。

## 许可证

MIT License
