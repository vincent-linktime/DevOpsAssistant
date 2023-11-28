import json

BASE_PROMPT = """
I am a DevOps engineer and you are my AI assistant. You are helping me to diagnose	
system issues and find the root cause and resolve it. The error message I have seen is:
'''{error_message}'''

The system context:
{context}

Now you need to give me only one diagnose step at a time. Each diagnose step has the following format:
New Step: The action you want me to do to collect more information about this error. This action should be very concise, no more than 100 characters.
Command: The commands I need to run to complish the above action. The commands should be accurate
and complete. For example, if we need to run a Mysql command, we need to first run 'ssh x' first 
to get into the host running Mysql, then we need to run 'mysql -u root -p'  to login Mysql server.

An example of a diagnose step is:
Next Step: Login into Mysql and list all the processes. 
Command: 
mysql -u root -p{your password}
show processlist

After I show you the result I got from this action, you give me the next diagnose step until we find the root cause and resolve it. 

Previous diagnose steps we have done:
{step_history}

Based on the history of previous diagnose steps, now what is the next diagnose step?
"""