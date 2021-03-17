# https://docs.python.org/3.8/library/unittest.html

import pandas as pd
import numpy as np
import unittest

from data_requests.survey_functions import calc_prop


# Create dummy data for testing purposes
data = pd.DataFrame({
    'TOID': [1, 1, 1, 1, 1, 2, 2],
    'Measure1': [1, 0, 1, 1, 0, 0,  1],
    'WEIGHT': [0.5, 1, 1, 0.25, 0.5, 1, 0.75]
})

# Expected output (group by TOID)
toid_output = pd.DataFrame({
    'TOID': [1, 2],
    'variable': ['Measure1', 'Measure1'],
    'proportion': [0.6, np.nan],
    'N': [5, 2]
})

state_output = pd.DataFrame({
    'variable': ['Measure1'],
    'proportion': [0.5],
    'N': [7]
})

class Tests(unittest.TestCase):
    
    # Define tests and expected outputs

    # Example test
    def test_function(self):
        self.assertEqual(sum([1, 2]), 3)

    # Andrew's version of function
    def test_toid_output(self):
        output = calc_prop(df=data, group_vars=['TOID'], vars=['Measure1'], weighted=False)
        
        self.assertTrue(output.equals(toid_output))

    def test_state_output(self):
        output = calc_prop(df=data, vars=['Measure1'], weighted=True)

        self.assertTrue(output.equals(state_output))


# Must remain at the bottom of this script
# Run these tests on running this python script
if __name__ == '__main__':
    unittest.main(verbosity=2)
