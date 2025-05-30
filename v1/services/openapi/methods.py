import openai

openai.api_key = "YOUR_API_KEY"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Translate to Russian: Hello world"}
    ]
)

print(response['choices'][0]['message']['content'])
