import openai
import config

openai.api_key = config.OPEN_AI_API_KEY
model_engine = "gpt-3.5-turbo"

# # CREDIT to Sentdex
def get_typical_weather(destination, month):
  user_search_string = f"What is a brief description of the typical weather in {destination} in the month of {month}?"

  completion = openai.ChatCompletion.create(
    model=model_engine,
    messages=[{"role": "user", "content": user_search_string}],
    max_tokens=150,
    n=1,
    stop=None, 
    temperature=0.5,
  )
  chatgpt_response = completion.choices[0].message.content
  return chatgpt_response
