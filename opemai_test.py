import openai


openai.api_key = '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'

# try:
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt="Translate the following English text to French: 'Hello, how are you?'",
#         temperature=0.4,
#         max_tokens=60
#     )
#     print(response.choices[0].text.strip())
# except Exception as e:
#     print(f"An error occurred: {e.args}")
