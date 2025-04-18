for executing run -over-streamlit- app\application.py<br>

src/structure.py --> All the States and Graph functions
src/share.py --> State variables and Structured output

- Problems <br>
(In consistant Issue)
-- File "D:\krish\llm_app\.venv\Lib\site-packages\groq\_base_client.py", line 1020, in _request
    raise self._make_status_error_from_response(err.response) from None
groq.BadRequestError: Error code: 400 - {'error': {'message': "Failed to call a function. Please adjust your prompt. See 'failed_generation' for more details.", 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '<tool-use>\n{\n  "tool_calls": [\n    {\n      "id": "pending",\n      "type": "function",\n      "function": {\n        "name": "Code_Format",\n        "parameters": {\n          "code": "Code for bird-flapping game",\n          "file_name": "main.py"\n        }\n      }\n    }\n  ]\n}\n</tool-use>'}}
During task with name 'Generate Code' and id 'ee335b11-c8f5-3201-497d-88fd6ba8e9f4'<br>

![flow](https://github.com/user-attachments/assets/581cbe1d-1bd7-4038-b1bb-492a50b783b2)

![image](https://github.com/user-attachments/assets/4b922e8f-2828-48b0-b746-7c93315688a6)

