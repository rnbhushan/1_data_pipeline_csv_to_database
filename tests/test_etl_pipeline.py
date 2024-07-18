import unittest
import pandas as pd
from etl_pipeline import ETLPipeline

class TestETLPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ETLPipeline('sample_data.csv', 'sqlite:///test.db')

    def test_transform(self):
        input_data = pd.DataFrame({'name': ['John', 'Jane']})
        expected_output = pd.DataFrame({'name': ['JOHN', 'JANE']})
        result = self.pipeline.transform(input_data)
        pd.testing.assert_frame_equal(result, expected_output)

if __name__ == '__main__':
    unittest.main()