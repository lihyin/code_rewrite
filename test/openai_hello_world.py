import os
import openai

openai.organization = "org-D9mKe7q7myjGPTh9HzWfnhnG"
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)
print(openai.Model.list())