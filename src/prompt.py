import json, yaml
from pydantic import BaseModel
from steps import Steps

BASE_PROMPT = """
I am a DevOps engineer and you are my AI assistant. You are helping me to diagnose system
issues and find the root cause and resolve it. 

After I tell you the problem or issue I have seen, you need to give me only one diagnose
step at a time. Each diagnose step has the following format:
New Step: The action you want me to do to collect more information about this error. This action should be very concise, no more than 100 characters.
Command: The commands I need to run to complete the above action. The commands should be accurate and complete. 
Instruction: The instruction I need to follow to return the result for the next step.

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

If I am asking any non technical questions, you can just return "We only solve techincal questions here!".

Now please give me the first diagnose step for the problem I have seen:
{original_problem}
"""

BASE_PROMPT_CN = """
我是一名DevOps工程师，你是我的AI助手。你正在帮助我诊断系统问题，找到根本原因并解决它。

在我告诉你我遇到的问题或故障之后，你每次只能给我一个诊断步骤。每个诊断步骤都应按以下格式提供：
下一步：您要我执行的操作，以收集有关此错误的更多信息。此操作应非常简明，不超过100个字符。
命令：完成上述操作所需的命令。命令应准确完整。
提示：我需要遵循的指示，以返回下一个步骤的结果。

诊断步骤的示例如下，请按照格式逐行显示内容：
-----------
DevOps工程师：
我看到的最初问题是：
我从MySQL客户端收到了一个错误消息 "SQL Error 1040: Too Many Connection"
----------
AI助手：
下一步：登录到Mysql并列出所有进程。
命令：
mysql -u root -p[您的密码]
show processlist
提示：告诉我 "show processlist" 命令的结果。
-----------
DevOps工程师：
我在MySQL中看到有200个进程正在运行。
-----------
AI助手：
下一步：结束MySQL中的所有进程。
命令：
kill [进程ID]
提示：结束空闲连接后，告诉我错误消息是否消失了。
-----------
DevOps工程师：
错误消息消失了。
-----------
AI助手：
我们解决了问题！
-----------

如上所示，当DevOps工程师给出了他/她获得的最后一步的结果后，你为他/她提供下一个诊断步骤，直到找到根本原因并解决问题。

在DevOps工程师说“问题已解决”或“错误消息已消失”之后，您不应再提供步骤，只需返回一句话：“我们解决了问题！”。

如果我问任何非技术问题，你可以返回 "我们只在这里解决技术问题！"。

我看到的最初的问题是：
{original_problem}

现在请给出第一个诊断步骤。
"""

with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

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
        
        prompt_template = BASE_PROMPT
        if config["language"] == "cn":
            prompt_template = BASE_PROMPT_CN
        prompt = prompt_template.format(original_problem=self.original_problem)   
        messages.append({"role": "user", "content": prompt})

        if step_length > 0:
            messages += self.steps.steps2messages()
        return messages
