import os, sys, unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.prompt import PromptProvider, BASE_PROMPT
from src.steps import Steps

class TestPromptProvider(unittest.TestCase):
    def test_get_prompt(self):
        input_message = "error message"
        context = "context"
        step_history = "None"
        abstract = f"The error message I see is: {input_message}"
        expected_prompt = BASE_PROMPT.format(abstract=abstract, \
            context=context, step_history="None")            

        prompt_provider = PromptProvider(context=context)
        prompt = prompt_provider.get_prompt(input_message)
        self.assertEqual(prompt, expected_prompt)