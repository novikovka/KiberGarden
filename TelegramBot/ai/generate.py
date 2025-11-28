from openai import AsyncOpenAI
#from config import AI_TOKEN

# AI_TOKEN='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'
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

