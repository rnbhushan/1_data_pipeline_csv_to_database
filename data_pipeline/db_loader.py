from sqlalchemy import create_engine

class DBLoader:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)

    def load_to_db(self, df, table_name):
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)
