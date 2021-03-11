import pandas as pd
import numpy as np
import unittest
from data_requests import functions # Andrew's code TODO: Rename python file name

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

class Tests(unittest.TestCase):
    # Define tests and expected outputs
    def test_function():
        assert sum([1, 2]) == 3, 'message on error'

    # Andrew's version of function
    def test_calc_prop():
        output = functions.calc_prop(df=data, group_vars=['TOID'], vars=['Measure1'], weighted=False)
        assert output.equals(toid_output), 'calc_prop did not provide the right output'

# def test_supressions():

# def test_weighting():


# Speed tests?

# Run these tests on running this python script
if __name__ == '__main__':
    unittest.main()
