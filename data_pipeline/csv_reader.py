import pandas as pd

class CSVReader:
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def read_csv(self):
        return pd.read_csv(self.file_path, encoding=self.encoding)
