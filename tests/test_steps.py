import os, sys, unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.steps import Step, Steps, STEP_HISTORY_LENGTH

step_str ="""
Next Step: Login into Mysql and list all the processes.
Command:
mysql -u root -p{your password}
"""

# Test the Steps class
class TestSteps(unittest.TestCase):
    def test_add_step(self):
        # Create a Steps object
        
        steps = Steps()
        
        # Create a Step object
        step = Step(suggestion="suggestion", commands=["commands"], result="result")
        
        # Add the Step object to the Steps object
        steps.add_step(step)
        
        # Check if the Steps object has the Step object
        self.assertIn(step, steps.get_steps())

        # Test add_step with more than STEP_HISTORY_LENGTH steps,
        # each step has a different suggestion so that we can check
        # if the first step is removed.
        for i in range(0, STEP_HISTORY_LENGTH + 1):
            step = Step(suggestion=str(i), commands=["commands"], result="result")
            steps.add_step(step)
            self.assertIn(step, steps.get_steps())
            if i == STEP_HISTORY_LENGTH:
                self.assertNotIn(Step(suggestion="0", commands=["commands"], result="result"),\
                     steps.get_steps())

    def test_add_step_from_str(self):
        # Create a Steps object
        steps = Steps()
            
        # Add the Step object to the Steps object
        steps.add_step_from_str(step_str)

        rtn_step = steps.get_steps()[0]
        # Check if the Steps object has the Step object
        self.assertIn(rtn_step.suggestion, "Next Step: Login into Mysql and list all the processes.")
    
    def test_add_result_to_last_step(self):
        result = "problem solved"
        steps = Steps()
        steps.add_step_from_str(step_str)
        steps.add_result_to_last_step(result)
        self.assertEqual(steps.get_steps()[0].result, result)

    def test_get_steps(self):
        # Create a Steps object
        steps = Steps()
        
        # Create a Step object
        step = Step(suggestion="suggestion", commands=["commands"], result="result")
        
        # Add the Step object to the Steps object
        steps.add_step(step)
        
        # Check if the Steps object has the Step object
        self.assertIn(step, steps.get_steps())

    def test_get_steps_length(self):
        steps = Steps()
        self.assertEqual(steps.get_steps_length(), 0)
        step = Step(suggestion="suggestion", commands=["commands"], result="result")
        steps.add_step(step)
        self.assertEqual(steps.get_steps_length(), 1)

    def test_str2step(self):
        steps = Steps()
        step = steps.str2step(step_str)
        self.assertEqual(step.suggestion, "Login into Mysql and list all the processes.")
    
    def test_toText(self):
        steps = Steps()
        steps.add_step_from_str(step_str)
        print(steps.toText())
        self.assertEqual(steps.toText(), "Step 1: Login into Mysql and list all the processes.\nCommand:\nmysql -u root -p{your password}\nResult:\n")