from typing import Optional, Any

from openai import OpenAI

import config


class RagLLM(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # 11434: Ollama本地Http进程端口
            cls._instance.client = OpenAI(base_url=config.base_url,
                             api_key=config.model_name)
        return cls._instance

    def __call__(self, prompt: str, **kwargs: Any):
        """ 模型推理 """
        completion = self.client.completions.create(model="qwen2:72b",
                                                    prompt=prompt,
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096),
                                                    stream=kwargs.get('stream', False))  # 是否支持流式输出。
        if kwargs.get('stream', False):
            return completion
        return completion.choices[0].text
