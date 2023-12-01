import os, sys, unittest, openai, shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.qa_engine import QaEngine
from src.logger import DevOpsAILogger
from unittest.mock import patch, MagicMock

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

FINAL_RTN = "We solved the problem!"

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

final_response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": FINAL_RTN,
        "role": "assistant"
      }
    }
  ]
}

class TestQaEngine(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        if os.path.exists("logs"):
          shutil.rmtree("logs")

    @patch("openai.ChatCompletion.create")
    def test_get_answer(self, mock_openai_chatcompletion):
        mock_openai_chatcompletion.return_value = response
        qa_engine = QaEngine()
        rtn_text = qa_engine.get_answer("error message", "")
        self.assertEqual(rtn_text, step_str.replace("\n", "<p>"))
        prompt_provider = qa_engine.get_prompt_provider()
        self.assertEqual(prompt_provider.lastStep2Str(), step_str)

        mock_openai_chatcompletion.return_value = final_response
        rtn_text = qa_engine.get_answer("error message", "")
        self.assertEqual(rtn_text, FINAL_RTN)
        self.assertEqual(prompt_provider.lastStep2Str(), "")

