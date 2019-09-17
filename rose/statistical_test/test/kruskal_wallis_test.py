import unittest
import warnings
import pandas as pd
from rpy2.rinterface import RRuntimeWarning
from rose.statistical_test.kruskal_wallis import kruskal_wallis

# Filter the warnings from R
warnings.filterwarnings("ignore", category=RRuntimeWarning)

class RunningKruskal(unittest.TestCase):
    def test_kruskal(self):
        # df = pd.read_csv('../../../resources/kruskal.csv', sep=";")
        df = pd.read_csv('./resources/kruskal.csv', sep=";")

        k = kruskal_wallis(df, 'fitness', 'algorithm')
        kruskal_result, posthoc = k.apply()

        pvalue = kruskal_result['p-unc'][0]

        self.assertTrue(posthoc is not None and round(pvalue,5) == 0.0)

if __name__ == '__main__':
    unittest.main()