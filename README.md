# Introduction
This repository implements the NLP API by using OpenAI API (with its open accessible GPT-3 models), AWS Lambda, AWS API Gateway, and Python. The API could be improved by switching to use OpenAI Codex model once the Codex model access is approved. Currently, support:
- Generate code:
  - from docstring document
- Rewrite code:
  - from iterative to recursive

# How to use the API
## API Endpoint: https://xrhv8qvx7h.execute-api.us-east-1.amazonaws.com/dev/generate
  ### Method: POST
  ### Content Example:
```json
{
    "type":"docstring",
    "input":"    \"\"\"Takes in two numbers, returns their product.\"\"\"\n"
}
```
  ### CURL Example:
```bash
curl -X POST https://xrhv8qvx7h.execute-api.us-east-1.amazonaws.com/dev/generate -H 'Content-Type: application/json' -d '{
    "type":"docstring",
    "input":"    \"\"\"Takes in two numbers, returns their product.\"\"\"\n"
}'
```

  ### Response:
```json
def multiply(a, b):
    """Takes in two numbers, returns their product."""
    return a*b
```

## API Endpoint: https://xrhv8qvx7h.execute-api.us-east-1.amazonaws.com/dev/rewrite
  ### Method: POST
  ### Content Example:
```json
{
    "type":"iterative2recursive",
    "input":" def Reverse_iter(s):\n   rev = ''\n   for k in s:\n     rev = k + rev\n   return rev\n\n Reverse_iter('Welcome!')"
}
```
  ### CURL Example:
```bash
curl -X POST https://xrhv8qvx7h.execute-api.us-east-1.amazonaws.com/dev/rewrite -H 'Content-Type: application/json' -d '{
    "type":"iterative2recursive",
    "input":" def Reverse_iter(s):\n   rev = ''\n   for k in s:\n     rev = k + rev\n   return rev\n\n Reverse_iter('Welcome!')"
}'
```

  ### Response:
```json
def Reverse_recur(s):
   # base case
   if len(s) == 1:
     return s
   # general case
   else:
     return s[-1] + Reverse_recur(s[:-1])

 Reverse_recur(Welcome!)
```

# How to set up the dev environment and deploy
1. [Install OpenAI API](https://beta.openai.com/docs/api-reference/introduction)
2. [Setup AWS Lambda with Python packages by using a virtual environment](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
3. [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
4. [Setup REST API via AWS API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html)
5. [Get OPENAI_API_KEY](https://beta.openai.com/account/api-keys) and set up the environment variable OPENAI_API_KEY in AWS Lambda 
6. [Test REST API](https://stackoverflow.com/questions/39655048/missing-authentication-token-while-accessing-api-gateway)
7. Deploy the AWS Gateway REST API with path: [Part 1](https://youtu.be/9eHh946qTIk?t=687), [Part 2](https://youtu.be/9eHh946qTIk?t=1213) (make sure to "Use Lambda Proxy integration")

# Troubleshoot 
## Couldn't run numpy in Lambda (due to incompatible numpy version)
1. In Lambda Function, Add Layer `AWSDataWrangler-Python39` 
2. When packaging Python zip, first delete numpy folder in .venv/lib/python3.9/site-packages


# OpenAI Prompt Engineering: generate code from docstring

## OpenAI Playground
Play the following code rewrite prompt engineering text in [OpenAI Playground](https://beta.openai.com/playground) for [iterative to recursive example](https://analyticsindiamag.com/ultimate-guide-to-recursion-and-iteration-in-python/)

```
converts a text instruction in Natural Language to Python Code with a suitable docstring in numpy style:
[Docstring]
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
[Generated Code with Docstring]
def add_binary(a, b):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    binary_sum = bin(a+b)[2:]
    return binary_sum

converts a text instruction in Natural Language to Python Code with a suitable docstring in numpy style:
[Docstring]
    """Takes in two numbers, returns their product."""
[Generated Code with Docstring]
```

## OpenAI Python Code:
Use the following Python code to implement the code generation:
```python
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="text-davinci-002",
  prompt="converts a text instruction in Natural Language to Python Code with a suitable docstring in numpy style:\n[Docstring]\n    '''\n    Returns the sum of two decimal numbers in binary digits.\n\n            Parameters:\n                    a (int): A decimal integer\n                    b (int): Another decimal integer\n\n            Returns:\n                    binary_sum (str): Binary string of the sum of a and b\n    '''\n[Generated Code with Docstring]\ndef add_binary(a, b):\n    '''\n    Returns the sum of two decimal numbers in binary digits.\n\n            Parameters:\n                    a (int): A decimal integer\n                    b (int): Another decimal integer\n\n            Returns:\n                    binary_sum (str): Binary string of the sum of a and b\n    '''\n    binary_sum = bin(a+b)[2:]\n    return binary_sum\n\nconverts a text instruction in Natural Language to Python Code with a suitable docstring in numpy style:\n[Docstring]\n    \"\"\"Takes in two numbers, returns their product.\"\"\"\n[Generated Code with Docstring]",
  temperature=0,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
```
# OpenAI Prompt Engineering: code rewrite

## OpenAI Playground
Play the following code rewrite prompt engineering text in [OpenAI Playground](https://beta.openai.com/playground) for [iterative to recursive example](https://analyticsindiamag.com/ultimate-guide-to-recursion-and-iteration-in-python/)

```
creating a recursive approach from an iterative approach in python:
[iterative]
 n = 10
 result = 1
 i = 1
 while i <= n:
   result *= i
   i += 1
 print(result) 

[recursive]
 def Factorial(n):
   # declare a base case (a limiting criteria)
   if n == 1:
     return 1
   # continue with general case
   else:
     return n * Factorial(n-1)
 
 print(Factorial(10))

creating a recursive approach from an iterative approach in python:
[iterative]
 def Reverse_iter(s):
   rev = ''
   for k in s:
     rev = k + rev
   return rev

 Reverse_iter('Welcome!')

[recursive]
```

## OpenAI Python Code:
Use the following Python code to implement the code rewrite
```python
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="text-davinci-002",
  prompt="creating a recursive approach from an iterative approach in python:\n[iterative]\n n = 10\n result = 1\n i = 1\n while i <= n:\n   result *= i\n   i += 1\n print(result) \n\n[recursive]\n def Factorial(n):\n   # declare a base case (a limiting criteria)\n   if n == 1:\n     return 1\n   # continue with general case\n   else:\n     return n * Factorial(n-1)\n \n print(Factorial(10))\n\ncreating a recursive approach from an iterative approach in python:\n[iterative]\n def Reverse_iter(s):\n   rev = ''\n   for k in s:\n     rev = k + rev\n   return rev\n\n Reverse_iter('Welcome!')\n\n[recursive]\n",
  temperature=0,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
```
