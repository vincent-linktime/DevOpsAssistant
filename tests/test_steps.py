import os, sys, unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.steps import Step, Steps, STEP_HISTORY_LENGTH

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

expected_str = "\nNext Step: Login into Mysql and list all the processes.\n" + \
    "Command:\nmysql -u root -p{your password}\n"


# Test the Steps class
class TestSteps(unittest.TestCase):
    def test_add_step(self):
        # Create a Steps object
        
        steps = Steps()
        
        # Create a Step object
        step = Step(suggestion="suggestion", result="result")
        
        # Add the Step object to the Steps object
        steps.add_step(step)
        
        # Check if the Steps object has the Step object
        self.assertIn(step, steps.get_steps())

        # Test add_step with more than STEP_HISTORY_LENGTH steps,
        # each step has a different suggestion so that we can check
        # if the first step is removed.
        for i in range(0, STEP_HISTORY_LENGTH + 1):
            step = Step(suggestion=str(i), result="result")
            steps.add_step(step)
            self.assertIn(step, steps.get_steps())
            if i == STEP_HISTORY_LENGTH:
                self.assertNotIn(Step(suggestion="0", result="result"),\
                     steps.get_steps())

    def test_add_step_from_str(self):
        # Create a Steps object
        steps = Steps()
            
        # Add the Step object to the Steps object
        steps.add_step_from_str(step_str)

        rtn_step = steps.get_steps()[0]
        # Check if the Steps object has the Step object
        self.assertIn(rtn_step.suggestion, expected_str)
    
    def test_add_result_to_last_step(self):
        result = "problem solved"
        steps = Steps()
        steps.add_step_from_str(step_str)
        steps.add_result_to_last_step(result)
        self.assertEqual(steps.get_steps()[0].result, result)

    def test_clean_steps(self):
        steps = Steps()
        self.assertEqual(steps.get_steps_length(), 0)
        step = Step(suggestion="suggestion", result="result")
        steps.add_step(step)
        self.assertEqual(steps.get_steps_length(), 1)
        steps.clean_steps()
        self.assertEqual(steps.get_steps_length(), 0)

    def test_get_steps(self):
        # Create a Steps object
        steps = Steps()
        
        # Create a Step object
        step = Step(suggestion="suggestion", result="result")
        
        # Add the Step object to the Steps object
        steps.add_step(step)
        
        # Check if the Steps object has the Step object
        self.assertIn(step, steps.get_steps())

    def test_get_steps_length(self):
        steps = Steps()
        self.assertEqual(steps.get_steps_length(), 0)
        step = Step(suggestion="suggestion", result="result")
        steps.add_step(step)
        self.assertEqual(steps.get_steps_length(), 1)
    
    def test_lastStep2Str(self):
        steps = Steps()
        self.assertEqual(steps.lastStep2Str(), "")
        steps.add_step_from_str(step_str)
        self.assertEqual(steps.lastStep2Str(), expected_str)

    def test_steps2messages(self):
        steps = Steps()
        steps.add_step_from_str(step_str)
        messages = steps.steps2messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["content"], expected_str) 
        self.assertEqual(messages[0]["role"], "assistant")