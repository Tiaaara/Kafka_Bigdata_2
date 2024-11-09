from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RetailKMeansTraining") \
    .getOrCreate()

def load_and_preprocess_data(file_path):
    """
    Load and preprocess each batch CSV file.
    Selects relevant columns, handles missing values, and assembles features.
    """
    # Load CSV as DataFrame
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    # Select relevant columns for clustering (e.g., Quantity and UnitPrice)
    df = df.select("Quantity", "UnitPrice")

    # Handle missing values (optional)
    df = df.na.drop()
    
    # Assemble features for KMeans
    assembler = VectorAssembler(inputCols=["Quantity", "UnitPrice"], outputCol="features")
    data = assembler.transform(df).select("features")
    
    return data

def train_and_save_kmeans_model(data, model_number, k=3):
    """
    Train and save the KMeans model with a specified number of clusters (k).
    """
    # Initialize KMeans model
    kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")
    
    # Train the model
    model = kmeans.fit(data)
    
    # Save the model
    model_path = f"models/kmeans_model_{model_number}"
    model.save(model_path)
    print(f"Model {model_number} saved to {model_path}")

# Path to the directory containing batch files
batch_dir = "./batch"  # Adjust this path if needed
batch_files = sorted([os.path.join(batch_dir, f) for f in os.listdir(batch_dir) if f.endswith('.csv')])

# Define number of clusters and batch limit (optional)
k = 3  # Number of clusters for KMeans
batch_limit = 3  # Number of batches to process for model generation

# Train models for each batch file
for i, batch_file in enumerate(batch_files[:batch_limit], start=1):
    print(f"Processing {batch_file} for Model {i}")
    
    # Load and preprocess the batch data
    data = load_and_preprocess_data(batch_file)
    
    # Train and save the KMeans model
    train_and_save_kmeans_model(data, model_number=i, k=k)

# Stop Spark session
spark.stop()
