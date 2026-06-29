from openai import AzureOpenAI

from core.config import OPENAI_API_KEY, OPENAI_API_VERSION, OPENAI_BASE_URL, OPENAI_MODEL

client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_BASE_URL,
    api_version=OPENAI_API_VERSION,
)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
