import unittest
import pandas as pd
from rose.effect_size.vargha_delaney import VD_A, VD_A_DF, reduce

class RunningEffectSize(unittest.TestCase):
    def test_VD_A_negligible(self):
        # negligible
        array1 = [0.8236111111111111, 0.7966666666666666, 0.923611111111111, 0.8197222222222222, 0.7108333333333333]
        array2 = [0.8052777777777779, 0.8172222222222221, 0.8322222222222223, 0.783611111111111, 0.8141666666666666]

        result = VD_A(array1, array2)
        self.assertTrue(result[0] == 0.56 and result[1] == 'negligible')

    def test_VD_A_small(self):
        # small
        array1 = [0.478515625, 0.4638671875, 0.4638671875, 0.4697265625, 0.4638671875, 0.474609375, 0.4814453125,
             0.4814453125,
             0.4697265625, 0.4814453125, 0.474609375, 0.4833984375, 0.484375, 0.44921875, 0.474609375, 0.484375,
             0.4814453125, 0.4638671875, 0.484375, 0.478515625, 0.478515625, 0.45703125, 0.484375, 0.419921875,
             0.4833984375, 0.478515625, 0.4697265625, 0.484375, 0.478515625, 0.4638671875]
        array2 = [0.4814453125, 0.478515625, 0.44921875, 0.4814453125, 0.4638671875, 0.478515625, 0.474609375, 0.4638671875,
             0.474609375, 0.44921875, 0.474609375, 0.478515625, 0.478515625, 0.474609375, 0.4697265625, 0.474609375,
             0.45703125, 0.4697265625, 0.478515625, 0.4697265625, 0.4697265625, 0.484375, 0.45703125, 0.474609375,
             0.474609375, 0.4638671875, 0.45703125, 0.474609375, 0.4638671875, 0.4306640625]

        result = VD_A(array1, array2)
        self.assertTrue(result[0] == 0.6405555555555555 and result[1] == 'small')

    def test_VD_A_medium(self):
        # medium
        array1 = [0.9108333333333334, 0.8755555555555556, 0.900277777777778, 0.9274999999999999, 0.8777777777777779]
        array2 = [0.8663888888888888, 0.8802777777777777, 0.7816666666666667, 0.8377777777777776, 0.9305555555555556]

        result = VD_A(array1, array2)
        self.assertTrue(result[0] == 0.72 and result[1] == 'medium')

    def test_VD_A_large(self):
        # Large
        array1 = [0.9108333333333334, 0.8755555555555556, 0.900277777777778, 0.9274999999999999, 0.8777777777777779]
        array2 = [0.7202777777777778, 0.77, 0.8544444444444445, 0.7947222222222222, 0.7577777777777778]

        result = VD_A(array1, array2)
        self.assertTrue(result[0] == 1.0 and result[1] == 'large')

    def test_VD_A_DF(self):
        # df = pd.read_csv('../../../resources/kruskal.csv', sep=";")
        df = pd.read_csv('./resources/kruskal.csv', sep=";")

        reduced = reduce(VD_A_DF(df, 'fitness', 'algorithm'), 'AlgorithmA')

        first_row = reduced.iloc[0]

        self.assertTrue(first_row['base'] == 'AlgorithmA'
                        and first_row['compared_with'] == 'AlgorithmB'
                        and first_row['estimate'] == '1.0'
                        and first_row['magnitude'] == 'large'
                        and first_row['effect_size_symbol'] == '$\\blacktriangle$')

if __name__ == '__main__':
    unittest.main()