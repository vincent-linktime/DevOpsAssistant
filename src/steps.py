from pydantic import BaseModel
import yaml

with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

FEEDBACK_STR = ""
if config["language"] == "en":
    FEEDBACK_STR = config["en_labels"]["feedback_str"]
else:
    FEEDBACK_STR = config["cn_labels"]["feedback_str"]

class Step(BaseModel):
    suggestion: str
    result: str
    
STEP_HISTORY_LENGTH = 10

class Steps(BaseModel):
    step_list: list[Step] = []
    
    # Add a step into the steps list,
    # if the length of the list is greater than 
    # STEP_HISTORY_LENGTH then remove the first element
    def add_step(self, step: Step):
        self.step_list.append(step)
        if len(self.step_list) > STEP_HISTORY_LENGTH:
            self.step_list.pop(0)

    def add_step_from_str(self, suggestion: str):
        step = Step(suggestion=suggestion, result="")
        self.add_step(step)

    def add_result_to_last_step(self, result: str):
        self.step_list[-1].result = result

    def clean_steps(self):
        self.step_list = []

    def get_steps(self):
        return self.step_list

    def get_steps_length(self):
        return len(self.step_list)

    def lastStep2Str(self):
        if len(self.step_list) == 0:
            return ""
        suggestion = self.step_list[-1].suggestion
        result = self.step_list[-1].result
        rtn_str = suggestion
        if result != "":
            rtn_str = f"{suggestion}{FEEDBACK_STR}:{result}"
        return rtn_str

    def steps2messages(self):
        messages = []
        for step in self.step_list:
            messages.append({"role": "assistant", "content": step.suggestion})
            if step.result != "":
                messages.append({"role": "user", "content": step.result})
        return messages
