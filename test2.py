from openai import OpenAI
client = OpenAI()

code = ""

completion = client.chat.completions.create(
  model="gpt-4-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to change an altaire Code."},
    {"role": "user", "content": "Change this altaircode that it zoomes in: "+code}
  ]
)

print(completion.choices[0].message)