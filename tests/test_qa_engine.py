import os, sys, unittest, openai

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.qa_engine import QaEngine
from unittest.mock import patch, MagicMock

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": step_str,
        "role": "assistant"
      }
    }
  ]
}

class TestQaEngine(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_get_answer(self, mock_openai_chatcompletion):
        mock_openai_chatcompletion.return_value = response
        qa_engine = QaEngine()
        steps = qa_engine.prompt_provider.get_steps()
        self.assertEqual(steps.get_steps_length(), 0)
        rtn_text = qa_engine.get_answer("error message")
        self.assertEqual(rtn_text, step_str)
        self.assertEqual(steps.get_steps_length(), 1)
        

