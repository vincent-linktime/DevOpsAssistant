from prompt import PromptProvider
from utils import openai_completion
from pydantic import BaseModel

CONTEXT = "Mysql server is running on host 192.168.7.11"

class QaEngine(BaseModel):
    prompt_provider: PromptProvider = PromptProvider(context=CONTEXT)

    def get_answer(self, question: str) -> str:
        messages = []
        prompt = self.prompt_provider.get_prompt(question)
        messages.append({"role": "user", "content": prompt})
        rtn_items = openai_completion(messages, 1)
        steps = self.prompt_provider.get_steps()
        rtn_text = rtn_items[0]
        steps.add_step_from_str(rtn_text)
        return rtn_text
