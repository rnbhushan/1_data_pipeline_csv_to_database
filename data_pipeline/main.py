
import sys,os
sys.path.append(os.getcwd())

from data_pipeline.config import Config
from data_pipeline.csv_reader import CSVReader
from data_pipeline.transformer import Transformer
from data_pipeline.db_loader import DBLoader

def main():
    # Read the CSV file
    reader = CSVReader(Config.CSV_FILE_PATH, encoding='latin1')  # Specify the encoding here
    df = reader.read_csv()

    # Transform the data
    transformer = Transformer()
    df = transformer.add_age_plus_ten(df)

    # Load the data into the database
    loader = DBLoader(Config.DATABASE_URL)
    loader.load_to_db(df, Config.TABLE_NAME)

    print(f"Data has been successfully loaded into the '{Config.TABLE_NAME}' table.")

if __name__ == '__main__':
    main()
