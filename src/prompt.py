import json
from pydantic import BaseModel
from steps import Steps

BASE_PROMPT = """
I am a DevOps engineer and you are my AI assistant. You are helping me to diagnose system issues and find the root cause and resolve it. 
The original problem I have seen is:
{original_problem}

Now you need to give me only one diagnose step at a time. Each diagnose step has the following format:
New Step: The action you want me to do to collect more information about this error. This action should be very concise, no more than 100 characters.
Command: The commands I need to run to complete the above action. The commands should be accurate and complete. 

An example of diagnose steps are as follows, please show the content line by line exactly following the format:
-----------
DevOps Engineer: 
The original problem I have seen is:
I got an error message from MySQL client "SQL Error 1040: Too Many Connection"
----------
AI Assistant:
Next Step: Login into Mysql and list all the processes. 
Command: 
mysql -u root -p[your-password]
show processlist
Instruction: Tell me that the results of "show processlist" command.
-----------
DevOps Engineer:
I see 200 processes running in MySQL.
-----------
AI Assistant:
Next Step: Kill all the processes in MySQL.
Command:
kill [process-id]
Instruction: After killing idle connections, tell me if the error message is gone.
-----------
DevOps Engineer:
The error message is gone.
-----------
AI Assistant:
We solved the problem!
-----------

As shown above, after DevOps engineer gives you the result he/her got for the last step, 
you give him/her the next diagnose step until you find the root cause and resolve it. 

After DevOps engineer said "the problem is solved" or "the error message is gone", 
you should give no more steps and return only one sentence "We solved the problem!".
"""

class PromptProvider(BaseModel):
    original_problem: str
    steps: Steps = Steps()

    def add_step_from_str(self, suggestion: str):
        self.steps.add_step_from_str(suggestion)

    def clean_steps(self):
        self.steps.clean_steps()

    def lastStep2Str(self):
        return self.steps.lastStep2Str()

    def get_messages(self, input_message: str):
        # If Steps list is not empty then input_message is the result for the last command
        # Otherwise input_message is the error message we see the first time
        step_length = self.steps.get_steps_length()
        messages = []
        if step_length > 0:
            self.steps.add_result_to_last_step(input_message)
        else:
            self.original_problem = input_message
        prompt = BASE_PROMPT.format(original_problem=self.original_problem)   
        messages.append({"role": "user", "content": prompt})
        messages += self.steps.steps2messages()
        return messages
