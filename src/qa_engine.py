from prompt import PromptProvider
from utils import openai_completion
from logger import DevOpsAILogger
import yaml

CONTEXT = "Mysql server is running on host 192.168.7.11"

with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

FINAL_RTN = "We solved the problem!"

class QaEngine:
    prompt_provider: PromptProvider = PromptProvider(original_problem="")
    logger : DevOpsAILogger
    def __init__(self):
        self.logger = DevOpsAILogger.get_instance(name='qaengine', config=config)
        super().__init__()

    def get_prompt_provider(self):
        return self.prompt_provider
        
    def get_answer(self, question: str, history: str) -> str:
        messages = self.prompt_provider.get_messages(question)        
        rtn_items = openai_completion(messages, 1)
    
        rtn_text = rtn_items[0]
        if rtn_text == FINAL_RTN:
            self.prompt_provider.clean_steps()
        else:
            self.prompt_provider.add_step_from_str(rtn_text)
        self.logger.info(f"last step: \n {self.prompt_provider.lastStep2Str()}")
        rtn_text = rtn_text.replace("\n", "<p>")
        return rtn_text
