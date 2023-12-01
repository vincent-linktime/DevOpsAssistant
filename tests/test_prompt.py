import os, sys, unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.prompt import PromptProvider, BASE_PROMPT
from src.steps import Steps

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

expected_str = "\nNext Step: Login into Mysql and list all the processes.\n" + \
    "Command:\nmysql -u root -p{your password}\n"

class TestPromptProvider(unittest.TestCase):
    def test_get_messages(self):
        original_problem = "error message"
        expected_prompt = BASE_PROMPT.format(original_problem=original_problem)            

        prompt_provider = PromptProvider(original_problem="")
        messages = prompt_provider.get_messages(original_problem)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")

        # Test with a non-empty step history
        input_message = "none"
        prompt_provider.add_step_from_str(input_message)
        messages = prompt_provider.get_messages(input_message)
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]['role'], "assistant")   
        self.assertEqual(messages[1]['content'], input_message)
        self.assertEqual(messages[2]['role'], "user")
        self.assertEqual(messages[2]['content'], input_message)
