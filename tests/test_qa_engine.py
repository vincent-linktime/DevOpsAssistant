import os, sys, unittest, openai, shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.qa_engine import QaEngine
from src.logger import DevOpsAILogger
from unittest.mock import patch, MagicMock

full_str ="""
DevOps Engineer:
Something should not be returned here.
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

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

    def test_parse_return_from_openai(self):
        qa_engine = QaEngine()
        rtn_text = qa_engine.parse_return_from_openai(full_str)
        self.assertEqual(rtn_text.strip(), step_str.strip())

        rtn_text = qa_engine.parse_return_from_openai(FINAL_RTN)
        self.assertEqual(rtn_text.strip(), FINAL_RTN)

        rtn_text = qa_engine.parse_return_from_openai("something else")
        self.assertEqual(rtn_text, "")

    @patch("openai.ChatCompletion.create")
    def test_get_answer(self, mock_openai_chatcompletion):
        mock_openai_chatcompletion.return_value = response
        qa_engine = QaEngine()
        rtn_text = qa_engine.get_answer("error message", "")
        replaced_str = step_str.replace("\n", "<p>")
        self.assertEqual(rtn_text.strip("<p>"), replaced_str.strip("<p>"))
        prompt_provider = qa_engine.get_prompt_provider()
        self.assertEqual(prompt_provider.lastStep2Str().strip(), step_str.strip())

        mock_openai_chatcompletion.return_value = final_response
        rtn_text = qa_engine.get_answer("error message", "")
        self.assertEqual(rtn_text.strip("<p>"), FINAL_RTN)
        self.assertEqual(prompt_provider.lastStep2Str(), "")

