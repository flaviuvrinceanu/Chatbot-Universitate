import requests
from django.conf import settings

def call_llm(messages, temperature=0.0, max_tokens=256, extra=None):
    """
    messages: list[{"role": "user"|"system"|"assistant", "content": str}]
    """
    payload = {
        "model": settings.MODEL_ID,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if extra:
        payload.update(extra)

    r = requests.post(settings.VLLM_URL, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # compat OpenAI
    return {
        "content": data["choices"][0]["message"]["content"],
        "usage": data.get("usage"),
        "raw": data,  # opțional, util pentru debug
    }
