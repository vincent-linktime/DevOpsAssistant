import os, sys, unittest, openai, shutil, yaml

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

full_cn_str ="""
DevOps工程师：
这里不应该返回任何东西。
下一步: 登录到Mysql并列出所有进程。
命令:
mysql -u root -p{your password}
"""

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

step_cn_str ="""
下一步: 登录到Mysql并列出所有进程。
命令:
mysql -u root -p{your password}
"""


with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)


FINAL_STR = ""
STEP_STR = ""
FULL_STR = ""
if config["language"] == "en":
    FINAL_STR = config["en_labels"]["final_str"]
    STEP_STR = step_str
    FULL_STR = full_str
else:
    FINAL_STR = config["cn_labels"]["final_str"]
    STEP_STR = step_cn_str
    FULL_STR = full_cn_str

response = {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": STEP_STR,
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
        "content": FINAL_STR,
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
        rtn_text = qa_engine.parse_return_from_openai(FULL_STR)
        self.assertEqual(rtn_text.strip(), STEP_STR.strip())

        rtn_text = qa_engine.parse_return_from_openai(FINAL_STR)
        self.assertEqual(rtn_text.strip(), FINAL_STR)

        rtn_text = qa_engine.parse_return_from_openai("something else")
        self.assertEqual(rtn_text, "")

    @patch("openai.ChatCompletion.create")
    def test_get_answer(self, mock_openai_chatcompletion):
        mock_openai_chatcompletion.return_value = response
        qa_engine = QaEngine()
        rtn_text = qa_engine.get_answer("error message", "")
        replaced_str = STEP_STR.replace("\n", "<p>")
        self.assertEqual(rtn_text.strip("<p>"), replaced_str.strip("<p>"))
        prompt_provider = qa_engine.get_prompt_provider()
        self.assertEqual(prompt_provider.lastStep2Str().strip(), STEP_STR.strip())

        mock_openai_chatcompletion.return_value = final_response
        rtn_text = qa_engine.get_answer("error message", "")
        self.assertEqual(rtn_text.strip("<p>"), FINAL_STR)
        self.assertEqual(prompt_provider.lastStep2Str(), "")

