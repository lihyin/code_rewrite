# Introduction
This repository implements the code short description API by using OpenAI API (with its open accessible GPT-3 models), AWS Lambda, AWS API Gateway, and Python. The API could be improved by switching to use OpenAI Codex model once the Codex model access is approved.

# How to use the API
* API Endpoint: https://r4ph71epe1.execute-api.us-east-1.amazonaws.com/dev
* Send the following JSON content with escaped code via POST HTTP request:
```json
{'code': 'print(\"hello world!\"'}
```
* Example: run the command
```bash
curl -X POST https://r4ph71epe1.execute-api.us-east-1.amazonaws.com/dev -H 'Content-Type: application/json' -d '{"code": "class Log:\n    def __init__(self, path):\n        dirname = os.path.dirname(path)\n        os.makedirs(dirname, exist_ok=True)\n        f = open(path, \"a+\")\n\n        # Check that the file is newline-terminated\n        size = os.path.getsize(path)\n        if size > 0:\n            f.seek(size - 1)\n            end = f.read(1)\n            if end != \"\\n\":\n                f.write(\"\\n\")\n        self.f = f\n        self.path = path\n\n    def log(self, event):\n        event[\"_event_id\"] = str(uuid.uuid4())\n        json.dump(event, self.f)\n        self.f.write(\"\\n\")\n\n    def state(self):\n        state = {\"complete\": set(), \"last\": None}\n        for line in open(self.path):\n            event = json.loads(line)\n            if event[\"type\"] == \"submit\" and event[\"success\"]:\n                state[\"complete\"].add(event[\"id\"])\n                state[\"last\"] = event\n        return state\n\n\"\"\"\n"}'
```
response:
```json
{"statusCode": 200, "body": {"id": "cmpl-5t90WRVFzzhhR8lmzDbuZaS8j7b2K", "object": "text_completion", "created": 1663824348, "model": "davinci", "choices": [{"text": "\nThe Log class is a simple wrapper around a file object. It has a log() method that takes an event and writes it to the file. It also has a state() method that returns a dictionary of the last event ID and the set of events that have been completed.\n\nThe Log class is initialized with", "index": 0, "logprobs": null, "finish_reason": "length"}], "usage": {"prompt_tokens": 463, "completion_tokens": 64, "total_tokens": 527}}}
```

# How to set up the dev environment and deploy
1. [Install OpenAI API](https://beta.openai.com/docs/api-reference/introduction)
2. [Setup AWS Lambda with Python packages by using a virtual environment](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
3. [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
4. [Setup REST API via AWS API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html)
5. [Get OPENAI_API_KEY](https://beta.openai.com/account/api-keys) and set up the environment variable OPENAI_API_KEY in AW Lambda 
6. [Test REST API](https://stackoverflow.com/questions/39655048/missing-authentication-token-while-accessing-api-gateway)

# Troubleshoot 
## Couldn't run numpy in Lambda (due to incompatible numpy version)
1. In Lambda Function, Add Layer `AWSDataWrangler-Python39` 
2. When packaging Python zip, first delete numpy folder in .venv/lib/python3.9/site-packages

# TODO
* Replace the OpenAI API with the Codex model afer getting the access approval (the Codex API access is currently pending for approval)
* Truncate the returned description to just use the first sentance as needed.
* Wrap the API and document with AWS API Gateway, Swagger API, etc