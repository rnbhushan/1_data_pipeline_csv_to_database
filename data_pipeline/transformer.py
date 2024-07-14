class Transformer:
    @staticmethod
    def add_age_plus_ten(df):
        df['age_plus_ten'] = df['age'] + 10
        return df
