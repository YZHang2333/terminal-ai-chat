import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from prompt_toolkit import prompt

from providers import PROVIDERS

console = Console()


def select_provider():
    console.print("\n[bold]选择 AI 提供商:[/bold]\n")
    keys = list(PROVIDERS.keys())
    for i, key in enumerate(keys, 1):
        console.print(f"  {i}. {PROVIDERS[key]['class'].name}")

    while True:
        try:
            idx = int(prompt("\n请输入编号> ").strip()) - 1
            if 0 <= idx < len(keys):
                break
        except (ValueError, EOFError, KeyboardInterrupt):
            pass
        console.print("[red]无效选择，请重试[/red]")

    info = PROVIDERS[keys[idx]]
    api_key = os.getenv(info["env_key"])
    if not api_key:
        console.print(f"[red]未找到环境变量 {info['env_key']}，请在 .env 文件中配置[/red]")
        sys.exit(1)

    return info["class"](api_key)


def chat(provider):
    messages = []
    console.print(f"\n[green]已连接 {provider.name}，输入 exit 退出[/green]\n")

    while True:
        try:
            user_input = prompt("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input or user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        console.print(f"\n[bold cyan]{provider.name}>[/bold cyan] ", end="")

        full = []
        try:
            for chunk in provider.stream(messages):
                console.print(chunk, end="", highlight=False)
                full.append(chunk)
        except Exception as e:
            console.print(f"\n[red]错误: {e}[/red]")
            messages.pop()
            continue

        console.print("\n")
        messages.append({"role": "assistant", "content": "".join(full)})


def main():
    load_dotenv()
    console.print("[bold blue]Terminal AI Chat[/bold blue]")
    provider = select_provider()
    chat(provider)
    console.print("[dim]再见！[/dim]")


if __name__ == "__main__":
    main()
