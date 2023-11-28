import os, sys, unittest, openai

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.utils import openai_completion
from unittest.mock import patch, MagicMock

response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
        "role": "assistant"
      }
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}

class TestUtils(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_openai_completion(self, mock_openai_chatcompletion):
        mock_openai_chatcompletion.return_value = response
        rtn_item = openai_completion(input, 1)
        self.assertEqual(rtn_item, ["The 2020 World Series was played in Texas at Globe Life Field in Arlington."])
        

