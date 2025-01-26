from faker import Faker
import csv
from datetime import datetime
import random
from google.cloud import storage
import os

# Initialize Faker
fake = Faker()

# Number of employees to generate
NUM_EMPLOYEES = 400

# Define departments and job titles
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations']
JOB_TITLES = {
    'IT': ['Software Engineer', 'System Administrator', 'Data Analyst', 'IT Manager'],
    'HR': ['HR Manager', 'Recruiter', 'HR Coordinator', 'Benefits Specialist'],
    'Finance': ['Accountant', 'Financial Analyst', 'Controller', 'Finance Manager'],
    'Marketing': ['Marketing Manager', 'Content Writer', 'Digital Marketing Specialist', 'Brand Manager'],
    'Sales': ['Sales Representative', 'Sales Manager', 'Account Executive', 'Sales Director'],
    'Operations': ['Operations Manager', 'Project Manager', 'Business Analyst', 'Operations Coordinator']
}

# Add salary ranges for job titles
SALARY_RANGES = {
    'Software Engineer': (80000, 150000),
    'System Administrator': (70000, 120000),
    'Data Analyst': (65000, 110000),
    'IT Manager': (100000, 180000),
    'HR Manager': (90000, 140000),
    'Recruiter': (50000, 85000),
    'HR Coordinator': (45000, 70000),
    'Benefits Specialist': (55000, 85000),
    'Accountant': (60000, 100000),
    'Financial Analyst': (70000, 120000),
    'Controller': (100000, 160000),
    'Finance Manager': (100000, 170000),
    'Marketing Manager': (90000, 150000),
    'Content Writer': (45000, 80000),
    'Digital Marketing Specialist': (50000, 90000),
    'Brand Manager': (80000, 140000),
    'Sales Representative': (40000, 90000),
    'Sales Manager': (80000, 150000),
    'Account Executive': (60000, 120000),
    'Sales Director': (120000, 200000),
    'Operations Manager': (80000, 140000),
    'Project Manager': (75000, 130000),
    'Business Analyst': (65000, 110000),
    'Operations Coordinator': (45000, 75000)
}

def generate_employee_data():
    # Generate employee data
    employees = []
    
    for _ in range(NUM_EMPLOYEES):
        department = random.choice(DEPARTMENTS)
        job_title = random.choice(JOB_TITLES[department])
        
        # Generate salary based on job title
        min_salary, max_salary = SALARY_RANGES[job_title]
        salary = random.randint(min_salary, max_salary)
        
        # Generate a complex password
        password = fake.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
        
        employee = {
            'employee_id': fake.unique.random_number(digits=6),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.company_email(),
            'password': password,  # New field
            'phone_number': fake.phone_number(),
            'ssn': fake.ssn(),  # PII field
            'date_of_birth': fake.date_of_birth(minimum_age=22, maximum_age=65).strftime('%Y-%m-%d'),  # PII field
            'hire_date': fake.date_between(start_date='-10y', end_date=datetime.now()).strftime('%Y-%m-%d'),
            'department': department,
            'job_title': job_title,
            'salary': salary,  # Updated to use job-specific salary range
            'address': fake.street_address(),  # PII field
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'emergency_contact_name': fake.name(),
            'emergency_contact_phone': fake.phone_number(),
            'bank_account_number': fake.bban(),  # PII field
            'routing_number': fake.aba(),  # PII field
        }
        employees.append(employee)
    
    return employees

def save_to_csv(employees, filename='employee_data.csv'):
    # Save employee data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        if employees:
            fieldnames = employees[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(employees)

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage bucket."""
    try:
        # Initialize the GCS client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the file
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}")
    except Exception as e:
        print(f"Error uploading to GCS: {str(e)}")

if __name__ == '__main__':
    # Generate employee data
    employee_data = generate_employee_data()
    
    # Get current directory and set filename
    current_dir = os.getcwd()
    local_filename = 'employee_data.csv'
    file_path = os.path.join(current_dir, local_filename)
    
    # Save to CSV locally
    save_to_csv(employee_data, local_filename)
    print(f"Generated {NUM_EMPLOYEES} employee records")
    print(f"File saved locally at: {file_path}")
    
    # Upload to GCS
    bucket_name = "mybkt-employee-data"  # Replace with your bucket name
    destination_blob_name = f"employee_data/{datetime.now().strftime('%Y%m%d_%H%M%S')}_employee_data.csv"
    upload_to_gcs(bucket_name, local_filename, destination_blob_name)


