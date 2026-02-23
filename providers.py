from abc import ABC, abstractmethod
from typing import Generator


class Provider(ABC):
    name: str

    @abstractmethod
    def __init__(self, api_key: str): ...

    @abstractmethod
    def stream(self, messages: list[dict]) -> Generator[str, None, None]: ...


class OpenAIProvider(Provider):
    name = "OpenAI (GPT-4o)"

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def stream(self, messages):
        for chunk in self.client.chat.completions.create(
            model="gpt-4o", messages=messages, stream=True
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicProvider(Provider):
    name = "Anthropic (Claude)"

    def __init__(self, api_key: str):
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)

    def stream(self, messages):
        system = ""
        chat_msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                chat_msgs.append(m)
        with self.client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=chat_msgs,
        ) as s:
            yield from s.text_stream


class GeminiProvider(Provider):
    name = "Google (Gemini)"

    def __init__(self, api_key: str):
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def stream(self, messages):
        contents = []
        for m in messages:
            if m["role"] == "system":
                continue
            role = "model" if m["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        for chunk in self.client.models.generate_content_stream(
            model="gemini-2.0-flash", contents=contents
        ):
            if chunk.text:
                yield chunk.text


class DeepSeekProvider(Provider):
    name = "DeepSeek"

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def stream(self, messages):
        for chunk in self.client.chat.completions.create(
            model="deepseek-chat", messages=messages, stream=True
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


PROVIDERS = {
    "openai": {"class": OpenAIProvider, "env_key": "OPENAI_API_KEY"},
    "anthropic": {"class": AnthropicProvider, "env_key": "ANTHROPIC_API_KEY"},
    "gemini": {"class": GeminiProvider, "env_key": "GOOGLE_API_KEY"},
    "deepseek": {"class": DeepSeekProvider, "env_key": "DEEPSEEK_API_KEY"},
}
