import pandas as pd
import numpy as np
import random
from faker import Faker

class UserAccessDataGenerator:
    def __init__(self):
        self.fake = Faker()
        
    def generate_departments(self):
        """Generate a list of departments."""
        departments = [
            "Engineering", "Sales", "Marketing", "Finance", 
            "Human Resources", "Customer Support", "IT", 
            "Product Management", "Legal", "Operations"
        ]
        return departments
    
    def generate_websites(self):
        """Generate a list of websites with some specifically marked for rejection."""
        websites = [
            "salesforce.com", "github.com", "atlassian.net", 
            "office365.com", "google.com", "slack.com", 
            "amazon.com", "azure.microsoft.com", "sap.com", 
            "oracle.com", "workday.com", "zendesk.com",
            # Websites with potential complete rejection
            "restricted-internal.com",
            "confidential-system.net",
            "high-security-portal.org"
        ]
        return websites
    
    def generate_synthetic_data(self, num_rows=100):
        """
        Generate synthetic user access data with varied approval statuses.
        
        Args:
            num_rows (int): Total number of rows to generate
        
        Returns:
            pd.DataFrame: Synthetic user access data
        """
        # Generate base data
        departments = self.generate_departments()
        websites = self.generate_websites()
        
        # Prepare data lists
        data = {
            'UserID': [],
            'Name': [],
            'Email': [],
            'Department': [],
            'ReportingManager': [],
            'Website': [],
            'RequestStatus': [],
            'Reason': []
        }
        
        # Track website access patterns
        website_access_counts = {site: 0 for site in websites}
        website_rejection_counts = {site: 0 for site in websites}
        
        # Websites to be completely rejected
        completely_rejected_sites = [
            "restricted-internal.com", 
            "confidential-system.net", 
            "high-security-portal.org"
        ]
        
        for _ in range(num_rows):
            # Select a department
            department = random.choice(departments)
            
            # Generate user details
            name = self.fake.name()
            email = self.fake.email()
            reporting_manager = self.fake.name()
            
            # Determine website selection strategy
            if random.random() < 0.7:  # 70% chance of existing website
                # Prioritize websites with fewer accesses
                website = min(website_access_counts, key=website_access_counts.get)
            else:
                website = random.choice(websites)
            
            # Special handling for completely rejected websites
            if website in completely_rejected_sites:
                request_status = 'Rejected'
                reason = f'Access to {website} is strictly prohibited'
                website_rejection_counts[website] += 1
            else:
                # Normal access logic
                if website_access_counts[website] > 1:
                    request_status = 'Approved'
                    reason = 'Historical access exists'
                else:
                    # Weighted selection for status
                    request_status = random.choices(
                        ['Approved', 'Rejected'], 
                        weights=[0.7, 0.3]
                    )[0]
                    reason = ('No prior access' if request_status == 'Rejected' 
                              else 'First access granted')
                
                # Update access count for non-rejected websites
                if request_status == 'Approved':
                    website_access_counts[website] += 1
            
            # Append data
            data['UserID'].append(f"USER_{_ + 1:03d}")
            data['Name'].append(name)
            data['Email'].append(email)
            data['Department'].append(department)
            data['ReportingManager'].append(reporting_manager)
            data['Website'].append(website)
            data['RequestStatus'].append(request_status)
            data['Reason'].append(reason)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Print summary of website access patterns
        print("Website Access Summary:")
        for site in websites:
            approved = len(df[(df['Website'] == site) & (df['RequestStatus'] == 'Approved')])
            rejected = len(df[(df['Website'] == site) & (df['RequestStatus'] == 'Rejected')])
            print(f"{site}: Approved = {approved}, Rejected = {rejected}")
        
        # Save to CSV
        df.to_csv('user_access_historical_data.csv', index=False)
        
        return df

# Usage example
if __name__ == "__main__":
    generator = UserAccessDataGenerator()
    historical_data = generator.generate_synthetic_data(num_rows=100)
    print("\nData Generation Complete. Check 'user_access_historical_data.csv'")