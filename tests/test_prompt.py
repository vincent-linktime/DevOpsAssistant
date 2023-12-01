import os, sys, unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.prompt import PromptProvider, BASE_PROMPT
from src.steps import Steps

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

class TestPromptProvider(unittest.TestCase):
    def test_get_prompt(self):
        original_problem = "error message"
        step_history = "None"
        expected_prompt = BASE_PROMPT.format(original_problem=original_problem, \
            step_history="None")            

        prompt_provider = PromptProvider(original_problem=original_problem)
        prompt = prompt_provider.get_prompt("none")
        self.assertEqual(prompt, expected_prompt)

        # Test with a non-empty step history
        steps = prompt_provider.get_steps()
        steps.add_step_from_str(step_str)
        input_message = "none"
        expected_step_history = "Step 1: Login into Mysql and list all the processes.\n" + \
            "Command:\nmysql -u root -p{your password}\n" + \
            "Result seen by DevOps Engineer after ran the above commands:\n" + input_message
        expected_prompt = BASE_PROMPT.format(original_problem=original_problem, \
            step_history=expected_step_history)
        prompt = prompt_provider.get_prompt(input_message)
        self.assertEqual(prompt, expected_prompt)

