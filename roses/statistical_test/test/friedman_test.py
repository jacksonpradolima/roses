import unittest
import warnings

from rpy2.rinterface import RRuntimeWarning

from roses.statistical_test.friedman import friedman

# Filter the warnings from R
warnings.filterwarnings("ignore", category=RRuntimeWarning)

class RunningFriedman(unittest.TestCase):
    def test_friedman(self):        
        # f = friedman('../../../resources/friedman.csv', 'fitness', 'algorithm', 'instance')
        f = friedman('./resources/friedman.csv', 'fitness', 'algorithm', 'instance')
        friedman_result, posthoc = f.apply()

        p_value = round(friedman_result[0], 8)
        chi_squared = round(friedman_result[1], 3)

        self.assertTrue(p_value == 4.81e-06 and chi_squared == 30.036)

if __name__ == '__main__':
    unittest.main()