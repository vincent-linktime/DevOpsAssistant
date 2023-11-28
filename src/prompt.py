import json
from pydantic import BaseModel
from steps import Steps

BASE_PROMPT = """
I am a DevOps engineer and you are my AI assistant. You are helping me to diagnose	
system issues and find the root cause and resolve it. 
{abstract}

The system context:
{context}

Now you need to give me only one diagnose step at a time. Each diagnose step has the following format:
New Step: The action you want me to do to collect more information about this error. This action should be very concise, no more than 100 characters.
Command: The commands I need to run to complish the above action. The commands should be accurate
and complete. For example, if we need to run a Mysql command, we need to first run 'ssh x' first 
to get into the host running Mysql, then we need to run 'mysql -u root -p'  to login Mysql server.

An example of a diagnose step is as follows, show the content line by line exactly following the format:
Next Step: Login into Mysql and list all the processes. 
Command: 
mysql -u root -p[your-password]
show processlist<
Instruction: Tell me that the results of "show processlist" command.

After I show you the result I got from this action, you give me the next diagnose step until we find the root cause and resolve it. 

Previous diagnose steps we have done:
{step_history}

Based on the history of previous diagnose steps, now what is the next diagnose step?
"""

class PromptProvider(BaseModel):
    context: str
    steps: Steps = Steps()

    def set_context(self, context: str):
        self.context = context

    def get_steps(self):
        return self.steps

    def get_prompt(self, input_message: str):
        # If Steps list is not empty then input_message is the result for the last command
        # Otherwise input_message is the error message we see the first time
        step_history = "None"
        abstract = f"The error message I see is: {input_message}"
        step_length = self.steps.get_steps_length()
        if step_length > 0:
            abstract = f"After ran the last command in Step {step_length-1}, \
                 {input_message}"
            self.steps.add_result_to_last_step(input_message)
            step_history = self.steps.toText()
        prompt = BASE_PROMPT.format(abstract=abstract, \
            context=self.context, step_history=step_history)   
        return prompt
