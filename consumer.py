import json
import time
from kafka import KafkaConsumer
import csv
from datetime import datetime
import os

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'retail_stream',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Batching Parameters
batch_size = 1000  # Number of records per batch
time_window = 300  # Time window in seconds for each batch (e.g., 5 minutes)

# Initialize variables for batching
batch = []
start_time = time.time()
batch_number = 1

# Define the output directory
output_dir = "./batch"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

def save_batch(batch, batch_number):
    # File naming convention with timestamp and batch number
    filename = os.path.join(output_dir, f"batch_{batch_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    
    # Save batch to CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=batch[0].keys())
        writer.writeheader()
        writer.writerows(batch)
    
    print(f"Batch {batch_number} saved as {filename}")

# Consume and batch messages
for message in consumer:
    batch.append(message.value)
    current_time = time.time()

    # Check if batch meets the size or time window criteria
    if len(batch) >= batch_size or (current_time - start_time) >= time_window:
        save_batch(batch, batch_number)
        batch = []  # Reset batch
        batch_number += 1
        start_time = time.time()  # Reset time for the next batch

consumer.close()
