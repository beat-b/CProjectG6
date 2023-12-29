import csv
from faker import Faker
import random
from typing import List, Union

fake = Faker()

def generate_fake_data(num_records: int = 10) -> List[List[Union[str, int]]]:
    """
    Generate fake customer data.

    --------------------------
    Parameters:
     - num_records (int): Number of records to generate. Default is 10.
    --------------------------
    Returns:
     - List[List[Union[str, int]]]: List of lists representing customer data.
        Each row contains:
         - Username (str)
         - Email (str)
         - Password (str)
         - Age (int)
         - Planned Trips (int)
         - Disabilities (str)
    """
    data = [["Username", "Email", "Password", "Age", "Planned Trips", "Disabilities"]]

    for _ in range(num_records):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        age = random.randint(18, 80)
        planned_trips = random.randint(0, 10)
        # Assign weights to choices for disabilities
        disabilities_choices = ["None", "Visual", "Mobility", "Cognitive"]
        disabilities_weights = [0.7, 0.1, 0.1, 0.1]
        disabilities = random.choices(disabilities_choices, weights=disabilities_weights)[0]

        data.append([username, email, password, age, planned_trips, disabilities])

    return data

def export_to_csv(data: List[List[Union[str, int]]], filename: str = "./data/customer_data.csv") -> None:
    """
    Export customer data to a CSV file.
    --------------------------
    Parameters:
     - data (List[List[Union[str, int]]]): List of lists representing customer data.
     - filename (str): Name of the CSV file. Default is "customer_data.csv".
    --------------------------
    Returns:
     - None
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    num_records = 1000
    customer_data = generate_fake_data(num_records)
    export_to_csv(customer_data)

    print(f"CSV file '{customer_data[0][0]}' created successfully.")
