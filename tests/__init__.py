import os
import sys
import argparse

try:
    import readline
except ImportError:
    import pyreadline3
from openai import OpenAI
from colorama import Fore, Style


def main():
    try:
        parser = argparse.ArgumentParser(description="Meow AI")
        parser.add_argument(
            "-b", "--base_url", dest="base_url", help="设置 Base URL", type=str
        )
        parser.add_argument(
            "-a", "--api_key", dest="api_key", help="设置 API Key", type=str
        )
        parser.add_argument(
            "-m", "--model", dest="model", help="设置启动时使用的 Model", type=str
        )
        parser.add_argument(
            "-r", "--read", dest="read", help="使用sys.stdin.read输入", action="store_true"
        )
        args = parser.parse_args()
        config = {
            "base_url": args.base_url or os.getenv("OPENAI_API_BASE"),
            "api_key": args.api_key or os.getenv("OPENAI_API_KEY"),
            "model": args.model or os.getenv("MODEL"),
        }
        print("欢迎使用 Meow AI, 按下 Ctrl + C 以退出程序")
        print()
        if config["base_url"] == None:
            print("".join([Fore.RED, "警告: 没有设置 Base URL, 开始配置", Style.RESET_ALL]))
            print()
            while True:
                try:
                    config["base_url"] = input(
                        "".join(
                            [
                                Fore.BLUE,
                                "请输入您的 Base URL, 直接回车以使用 OpenAI 官方接口 > ",
                                Style.RESET_ALL,
                            ]
                        )
                    )
                    break
                except EOFError:
                    continue
            print()
            print("".join([Fore.GREEN, "设置完成!", Style.RESET_ALL]))
            print()
        if config["api_key"] == None:
            print("".join([Fore.RED, "警告: 没有设置 API Key, 开始配置", Style.RESET_ALL]))
            print()
            while True:
                try:
                    config["api_key"] = input(
                        "".join(
                            [Fore.BLUE, "请输入您的 API Key, 若没有请直接回车 > ", Style.RESET_ALL]
                        )
                    )
                    break
                except EOFError:
                    continue
            print()
            print("".join([Fore.GREEN, "设置完成!", Style.RESET_ALL]))
            print()
        if config["model"] == None:
            print("".join([Fore.RED, "警告: 没有设置 Model, 开始配置", Style.RESET_ALL]))
            print()
            while True:
                try:
                    config["model"] = input(
                        "".join(
                            [
                                Fore.BLUE,
                                "请输入要使用的模型, 直接回车以使用 gpt-3.5-turbo > ",
                                Style.RESET_ALL,
                            ]
                        )
                    )
                    break
                except EOFError:
                    continue
            print()
            print("".join([Fore.GREEN, "设置完成!", Style.RESET_ALL]))
            print()
        if not config["base_url"]:
            config["base_url"] = "https://api.openai.com/v1"
        if not config["model"]:
            config["model"] = "gpt-3.5-turbo"
        openai = OpenAI(base_url=config["base_url"], api_key=config["api_key"])
        print(
            "".join(
                [
                    Fore.RED,
                    "警告: 即将进入交互模式. 输入 %help 以获取帮助; 若您使用了 read 参数, 请在消息输入结束后按下 Enter, 然后按下 Ctrl + D, 或不按 Enter, 按两次 Ctrl + D 即可发送消息",
                    Style.RESET_ALL,
                    "\n",
                ]
            )
        )
        messages = []
        while True:
            message: str
            print("> ", end="", flush=True)
            if args.read:
                message = sys.stdin.read().strip()
            else:
                try:
                    message = sys.stdin.readline().strip()
                except EOFError:
                    print("错误: 您没有使用 read 参数, 请按下 Enter 发送消息!")
                    print()
                    continue
            try:
                readline.add_history(message)
            except ModuleNotFoundError:
                pyreadline3.add_history(message)
            print()
            if message.startswith("%"):
                command = message[1:].strip()
                if command == "help":
                    print("MeowBot Help Menu")
                    print("%help: 获取帮助")
                    print("%reset: 重置聊天记录")
                    print("其他内容: 向 AI 提问")
                if command == "reset":
                    messages = []
                    print("".join([Fore.GREEN, "重置成功!", Style.RESET_ALL]))
            else:
                messages.append({"role": "user", "content": message})
                print("< ", end="", flush=True)
                completion = openai.chat.completions.create(
                    model=config["model"], messages=messages, stream=True
                )
                for chunk in completion:
                    print(chunk.choices[0].delta.content or "", end="", flush=True)
                print()
            print()
    except KeyboardInterrupt:
        print("再见!")
        sys.exit(0)


if __name__ == "__main__":
    main()
