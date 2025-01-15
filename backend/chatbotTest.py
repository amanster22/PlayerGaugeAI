# import openai

# # Set up the OpenAI API key
# openai.api_key = "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"

# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "developer", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )

# print(completion.choices[0].message)