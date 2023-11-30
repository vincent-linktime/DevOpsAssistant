from prompt import PromptProvider
from utils import openai_completion
from logger import DevOpsAILogger
import yaml

CONTEXT = "Mysql server is running on host 192.168.7.11"

with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

class QaEngine:
    prompt_provider: PromptProvider = PromptProvider(context=CONTEXT)
    logger : DevOpsAILogger
    def __init__(self):
        self.logger = DevOpsAILogger.get_instance(name='qaengine', config=config)
        super().__init__()

    def get_answer(self, question: str, history: str) -> str:
        messages = []
        prompt = self.prompt_provider.get_prompt(question)
        self.logger.info(f"prompt: {prompt}")
        messages.append({"role": "user", "content": prompt})
        rtn_items = openai_completion(messages, 1)
        steps = self.prompt_provider.get_steps()
        rtn_text = rtn_items[0]
        steps.add_step_from_str(rtn_text)
        rtn_text = rtn_text.replace("\n", "<p>")
        return rtn_text
