# Create a Python script or web form to collect user input for travel date, start location, and destination.

import openai
import config

openai.api_key = config.OPEN_AI_API_KEY

# user_destination = input("Enter a city: ")
user_destination = 'Hanoi'
model_engine = "gpt-3.5-turbo"
user_search_string = f"What is the typical weather in {user_destination} in the month of January?"

completion = openai.ChatCompletion.create(
  model=model_engine,
  messages=[{"role": "user", "content": user_search_string}],
  # max_tokens=30,
  n=1,
  stop=None, 
  temperature=0.5,
)
chatgpt_response = completion.choices[0].message.content
# print("chatgpt_response >> ", chatgpt_response)

message_history = []
user_search_string = f"What is the most famous attraction in this city?"
message_history.append({"role": "user", "content": user_search_string})
# print("message_history only user >> ", message_history)

message_history.append({"role": "assistant", "content": chatgpt_response})
# print("message_history with assistant >> ", message_history)

completion = openai.ChatCompletion.create(
  model=model_engine,
  messages=message_history,
)

chatgpt_response = completion.choices[0].message.content
print("chatgpt_response 2 >> ", chatgpt_response)
