import csv
import time
import random
from kafka import KafkaProducer
import json

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Path to your dataset (adjust if needed)
dataset_path = 'Online_Retail_Dataset.csv'

def send_data():
    # Open the dataset and start sending rows
    with open(dataset_path, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Convert row data to JSON and send to Kafka topic
            producer.send('retail_stream', value=row)
            print(f"Sent: {row}")
            
            # Introduce a random delay to simulate streaming
            time.sleep(random.uniform(0.5, 2))  # Random delay between 0.5 to 2 seconds
    
    producer.flush()
    print("All data sent successfully.")

if __name__ == "__main__":
    send_data()
