from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RetailKMeansTraining") \
    .getOrCreate()

# Define the columns for each clustering model
customer_columns = ["CustomerID", "Quantity", "UnitPrice"]
product_columns = ["StockCode", "Quantity", "UnitPrice"]
country_columns = ["Country", "Quantity", "UnitPrice"]

# Function to load and preprocess data
def load_and_preprocess_data(file_path, columns):
    # Load CSV as DataFrame
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Select relevant columns for clustering
    df = df.select(columns)

    # Handle missing values (optional)
    df = df.na.drop()

    # Assemble features for KMeans
    assembler = VectorAssembler(inputCols=columns[1:], outputCol="features")  # Exclude the first column (ID/Code/Country)
    data = assembler.transform(df).select("features")

    return data

# Function to train and save KMeans model
def train_and_save_kmeans_model(data, model_number, model_type, k=3):
    # Initialize KMeans model
    kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")

    # Train the model
    model = kmeans.fit(data)

    # Save the model
    model_path = f"models/{model_type}model{model_number}"
    model.save(model_path)
    print(f"Saved {model_type} model {model_number} to {model_path}")

# Path to the directory containing batch files
batch_dir = "./batch"  # Adjust this path if needed
batch_files = sorted([os.path.join(batch_dir, f) for f in os.listdir(batch_dir) if f.endswith('.csv')])

# Define number of clusters for each model (optional)
k = 3  # Number of clusters for KMeans

# Train models for each batch file
for i, batch_file in enumerate(batch_files, start=1):
    print(f"Processing {batch_file} for Customer Clustering")
    customer_data = load_and_preprocess_data(batch_file, customer_columns)
    train_and_save_kmeans_model(customer_data, i, "customer", k)

    print(f"Processing {batch_file} for Product Clustering")
    product_data = load_and_preprocess_data(batch_file, product_columns)
    train_and_save_kmeans_model(product_data, i, "product", k)

    print(f"Processing {batch_file} for Country Clustering")
    country_data = load_and_preprocess_data(batch_file, country_columns)
    train_and_save_kmeans_model(country_data, i, "country", k)

# Stop Spark session
spark.stop()
