[FIRST DRAFT](https://www.youtube.com/watch?v=53AwBWctePM) Video <br>

for executing run -over-streamlit- app\application.py<br>

src/structure.py --> All the States and Graph functions
src/share.py --> State variables and Structured output

- Problems <br>
(In consistant Issue)
-- File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1020, in _request
    raise self._make_status_error_from_response(err.response) from None
groq.BadRequestError: Error code: 400 - {'error': {'message': "Failed to call a function. Please adjust your prompt. See 'failed_generation' for more details.", 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '<tool-use>\n{\n  "tool_calls": [\n    {\n      "id": "pending",\n      "type": "function",\n      "function": {\n        "name": "Code_Format",\n        "parameters": {\n          "code": "Code for bird-flapping game",\n          "file_name": "main.py"\n        }\n      }\n    }\n  ]\n}\n</tool-use>'}}
During task with name 'Generate Code' and id 'ee335b11-c8f5-3201-497d-88fd6ba8e9f4'<br>
![image](https://github.com/user-attachments/assets/ce354a31-0af6-4f38-b8ae-82c82a4b5b96)

----

## Help me debug
#### Current observation, issues lies in this part of the code <br>
![image](https://github.com/user-attachments/assets/1c03fb59-a084-405d-a9bd-b963afd85215)

![image](https://github.com/user-attachments/assets/e9c91de2-5021-4bca-9b2a-3a38d46a6c48)
```
BadRequestError('Error code: 400 - {\'error\': {\'message\': "Failed to call a function. Please adjust your prompt. See \'failed_generation\' for more details.", \'type\': \'invalid_request_error\', \'code\': \'tool_use_failed\', \'failed_generation\': \'<tool-use>\\n{\\n    "tool_calls": [\\n        {\\n            "id": "pending",\\n            "type": "function",\\n            "function": {\\n                "name": "Code_Format"\\n            },\\n            "parameters": {\\n                "code": "import streamlit as st\\\\nst.title(\\\'Bird Game\\\')\\\\n\\\\n\\\\n# Game Code\\\\n\\\\n\\\\n"\\n            }\\n        }\\n    ]\\n}\\n</tool-use>\'}}')Traceback (most recent call last):


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\runnables\base.py", line 3023, in invoke
    input = context.run(step.invoke, input, config, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\runnables\base.py", line 5358, in invoke
    return self.bound.invoke(
           ^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\language_models\chat_models.py", line 307, in invoke
    self.generate_prompt(


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\language_models\chat_models.py", line 843, in generate_prompt
    return self.generate(prompt_messages, stop=stop, callbacks=callbacks, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\language_models\chat_models.py", line 683, in generate
    self._generate_with_cache(


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_core\language_models\chat_models.py", line 908, in _generate_with_cache
    result = self._generate(
             ^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\langchain_groq\chat_models.py", line 498, in _generate
    response = self.client.create(messages=message_dicts, **params)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\resources\chat\completions.py", line 322, in create
    return self._post(
           ^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1225, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 917, in request
    return self._request(
           ^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1005, in _request
    return self._retry_request(
           ^^^^^^^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1054, in _retry_request
    return self._request(
           ^^^^^^^^^^^^^^


  File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1020, in _request
    raise self._make_status_error_from_response(err.response) from None


groq.BadRequestError: Error code: 400 - {'error': {'message': "Failed to call a function. Please adjust your prompt. See 'failed_generation' for more details.", 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '<tool-use>\n{\n    "tool_calls": [\n        {\n            "id": "pending",\n            "type": "function",\n            "function": {\n                "name": "Code_Format"\n            },\n            "parameters": {\n                "code": "import streamlit as st\\nst.title(\'Bird Game\')\\n\\n\\n# Game Code\\n\\n\\n"\n            }\n        }\n    ]\n}\n</tool-use>'}}
```


![flow](https://github.com/user-attachments/assets/581cbe1d-1bd7-4038-b1bb-492a50b783b2)

![image](https://github.com/user-attachments/assets/4b922e8f-2828-48b0-b746-7c93315688a6)

----
## Update
![image](https://github.com/user-attachments/assets/e60d8faa-34b7-4702-82f9-39198cb5d2d1)
![image](https://github.com/user-attachments/assets/661b28b6-9f71-4661-91c5-c94b320613e2)
![image](https://github.com/user-attachments/assets/6616fb3d-cd97-4c4a-b147-4a73ebe45279)
![image](https://github.com/user-attachments/assets/a938435b-7744-48d4-8718-8a724e03a40f)


