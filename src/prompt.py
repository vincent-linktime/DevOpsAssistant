import json
from pydantic import BaseModel
from steps import Steps

BASE_PROMPT = """
I am a DevOps engineer and you are my AI assistant. You are helping me to diagnose	
system issues and find the root cause and resolve it.  The original problem I have is:
{original_problem}

Now you need to give me only one diagnose step at a time. Each diagnose step has the following format:
New Step: The action you want me to do to collect more information about this error. This action should be very concise, no more than 100 characters.
Command: The commands I need to run to complete the above action. The commands should be accurate
and complete. An example of diagnose steps are as follows, show the content line by line exactly following the format:
DevOps Engineer: I got an error message from MySQL "SQL Error 1040: Too Many Connection"
----------
AI Assistant:
Next Step: Login into Mysql and list all the processes. 
Command: 
mysql -u root -p[your-password]
show processlist
Instruction: Tell me that the results of "show processlist" command.
Result seen by DevOps Engineer after ran the above commands:
I see 200 processes running in MySQL.
-----------
AI Assistant:
Next Step: Kill all the processes in MySQL.
Command:
kill [process-id]
Instruction: After killing idle connections, tell me if the error message is gone.
Result seen by DevOps Engineer after ran the above commands:
The error message is gone.
-----------
AI Assistant:
Next Step: We solved the problem!
Command:
None
Instruction: Try to increase the max_connections in MySQL configuration file.

As shown above, after DevOps engineer gives you the result he/her got for the last step, 
you give him/her the next diagnose step until you find the root cause and resolve it. 

Previous diagnose steps you have done:
{step_history}

Based on the history of previous diagnose steps, now what is the next diagnose step?
"""

class PromptProvider(BaseModel):
    original_problem: str
    steps: Steps = Steps()

    def get_steps(self):
        return self.steps

    def get_prompt(self, input_message: str):
        # If Steps list is not empty then input_message is the result for the last command
        # Otherwise input_message is the error message we see the first time
        step_history = "None"
        step_length = self.steps.get_steps_length()
        if step_length > 0:
            self.steps.add_result_to_last_step(input_message)
            step_history = self.steps.toText()
        prompt = BASE_PROMPT.format(original_problem=self.original_problem, step_history=step_history)   
        return prompt
