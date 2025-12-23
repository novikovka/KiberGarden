# файл для аодключения к нейросети

from openai import AsyncOpenAI

AI_TOKEN='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'

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)

async def ai_generate(text: str):
  completion = await client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
      {
        "role": "user",
        "content": text
      }
    ]
  )
  print(completion)
  return completion.choices[0].message.content

