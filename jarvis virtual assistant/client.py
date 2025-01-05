from openai import OpenAI
#client = OpenAI()
client = OpenAI(
    api_key = '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',
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant jarvis skilled in general tasks like alexa and google cloud."},
        {
        "role": "user",
        "content": "what is coding."
        }
    ]
)
print(completion.choices[0].message)

