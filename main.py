from data_generator import UserAccessDataGenerator
from access_manager import UserAccessManager

from data_generator import UserAccessDataGenerator
from access_manager import UserAccessManager
def main():
    # Step 1: Generate Synthetic Data
    print("Generating synthetic user access data...")
    generator = UserAccessDataGenerator()
    historical_data = generator.generate_synthetic_data(num_rows=100)
    
    # Step 2: Launch Access Request GUI
    print("Launching User Access Request System...")
    access_manager = UserAccessManager('user_access_historical_data.csv')
    access_manager.create_gui()

if __name__ == "__main__":
    main()