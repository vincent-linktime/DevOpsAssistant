from pydantic import BaseModel

class Step(BaseModel):
    suggestion: str
    commands: list[str]
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

    def add_step_from_str(self, step_str: str):
        step = self.str2step(step_str)
        self.add_step(step)

    def add_result_to_last_step(self, result: str):
        self.step_list[-1].result = result

    def get_steps(self):
        return self.step_list

    def get_steps_length(self):
        return len(self.step_list)

    def str2step(self, step_str: str):
        suggestion = ""
        commands = []
        step_str = step_str.strip()
        lines = step_str.split("\n")
        commands_start = False
        for line in lines:
            if line.startswith("Next Step:"):
                suggestion = line.replace("Next Step:", "").strip()
            elif line.startswith("Command:"):
                commands_start = True
                continue
            elif commands_start:
                commands.append(line.strip())
        return Step(suggestion=suggestion, commands=commands, result="")

    def toText(self):
        rtn_str = ""
        step_num = 0
        for step in self.step_list:
            step_num += 1
            rtn_str += "AI Assistant:\n"
            rtn_str += f"Step {step_num}: " + step.suggestion + "\n"
            rtn_str += "Command:\n"
            for command in step.commands:
                rtn_str += command + "\n"
            rtn_str += "Result seen by DevOps Engineer after ran the above commands:\n"
            rtn_str += step.result + "\n"
            rtn_str += "-----------\n"
        return rtn_str