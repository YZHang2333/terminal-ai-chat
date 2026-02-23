# Terminal AI Chat

一个简洁的终端 AI 聊天工具，支持多种主流 AI 提供商，在终端中即可与 AI 对话。

## 功能特点

- 支持多种 AI 提供商，启动时自由选择
- 流式输出，实时显示 AI 回复
- 完整的上下文对话，支持多轮聊天
- 简洁的终端界面，彩色输出

## 支持的提供商

| 提供商 | 模型 | 环境变量 |
|--------|------|----------|
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| Anthropic | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` |
| Google Gemini | gemini-2.0-flash | `GOOGLE_API_KEY` |
| DeepSeek | deepseek-chat | `DEEPSEEK_API_KEY` |

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/terminal-ai-chat.git
cd terminal-ai-chat
```

### 2. 创建环境并安装依赖

```bash
conda create -n terminal-ai-chat python=3.12 -y
conda activate terminal-ai-chat
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你要使用的提供商的 API Key（只需填写你想用的那个即可）。

### 4. 运行

```bash
python main.py
```

## 使用示例

```
Terminal AI Chat

选择 AI 提供商:

  1. OpenAI (GPT-4o)
  2. Anthropic (Claude)
  3. Google (Gemini)
  4. DeepSeek

请输入编号> 1

已连接 OpenAI (GPT-4o)，输入 exit 退出

You> 你好，请介绍一下你自己

OpenAI (GPT-4o)> 你好！我是 GPT-4o，由 OpenAI 开发的 AI 助手...

You> exit
再见！
```

## 添加新的提供商

1. 在 `providers.py` 中创建新类，继承 `Provider` 并实现 `stream()` 方法
2. 将新类添加到 `PROVIDERS` 字典中

```python
class MyProvider(Provider):
    name = "My Provider"

    def __init__(self, api_key: str):
        # 初始化客户端
        ...

    def stream(self, messages):
        # 流式返回文本片段
        yield "Hello"
```

## 项目结构

```
├── main.py           # 入口：提供商选择菜单 + 聊天循环
├── providers.py      # Provider 基类 + 4 个提供商实现
├── requirements.txt  # Python 依赖
├── .env.example      # API Key 配置模板
└── .gitignore
```

## License

MIT
