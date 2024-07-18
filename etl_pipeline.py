# etl_pipeline.py
import pandas as pd
from sqlalchemy import create_engine
import logging
import os

class ETLPipeline:
    def __init__(self, input_file, db_connection_string):
        self.input_file = input_file
        self.db_connection_string = db_connection_string
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def extract(self):
        try:
            df = pd.read_csv(self.input_file)
            self.logger.info(f"Data extracted from {self.input_file}")
            return df
        except Exception as e:
            self.logger.error(f"Error extracting data: {str(e)}")
            raise

    def transform(self, df):
        try:
            # Example transformation: capitalize the 'name' column
            df['name'] = df['name'].str.upper()
            self.logger.info("Data transformation completed")
            return df
        except Exception as e:
            self.logger.error(f"Error transforming data: {str(e)}")
            raise

    def load(self, df, table_name):
        try:
            engine = create_engine(self.db_connection_string)
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            self.logger.info(f"Data loaded to table {table_name}")
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    def run(self, table_name):
        try:
            data = self.extract()
            transformed_data = self.transform(data)
            self.load(transformed_data, table_name)
            self.logger.info("ETL job completed successfully")
        except Exception as e:
            self.logger.error(f"ETL job failed: {str(e)}")
            raise

if __name__ == "__main__":
    input_file = os.environ.get('INPUT_FILE', 'data.csv')
    db_connection_string = os.environ.get('DB_CONNECTION_STRING', 'sqlite:///output.db')
    table_name = os.environ.get('TABLE_NAME', 'output_table')

    pipeline = ETLPipeline(input_file, db_connection_string)
    pipeline.run(table_name)