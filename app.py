from flask import Flask, request, jsonify
from pyspark.ml.clustering import KMeansModel
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pyspark.sql.types import StructType, StructField, FloatType
import os

# Initialize Flask app
app = Flask(_name_)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RetailKMeansAPI") \
    .getOrCreate()

# Load KMeans models from the models directory
model_dir = "./models"
models = {}
for model_file in os.listdir(model_dir):
    if model_file.startswith("customer_model_"):
        model_number = model_file.split("_")[-1]
        model_path = os.path.join(model_dir, model_file)
        models[f"customer_{model_number}"] = KMeansModel.load(model_path)
        print(f"Loaded customer model {model_number}")

    if model_file.startswith("product_model_"):
        model_number = model_file.split("_")[-1]
        model_path = os.path.join(model_dir, model_file)
        models[f"product_{model_number}"] = KMeansModel.load(model_path)
        print(f"Loaded product model {model_number}")

    if model_file.startswith("country_model_"):
        model_number = model_file.split("_")[-1]
        model_path = os.path.join(model_dir, model_file)
        models[f"country_{model_number}"] = KMeansModel.load(model_path)
        print(f"Loaded country model {model_number}")

# Define cluster descriptions
customer_cluster_descriptions = {
    0: "Low-Quantity Buyers",
    1: "Medium-Quantity Buyers",
    2: "High-Quantity Buyers"
}

product_cluster_descriptions = {
    0: "Low-Demand Products",
    1: "Moderate-Demand Products",
    2: "High-Demand Products"
}

country_cluster_descriptions = {
    0: "Low-Spending Countries",
    1: "Moderate-Spending Countries",
    2: "High-Spending Countries"
}

# Endpoint for clustering customers
@app.route('/cluster-customer', methods=['POST'])
def cluster_customer():
    data = request.get_json()
    model_number = data.get("model_number")
    customer_id = data.get("CustomerID")
    quantity = data.get("Quantity")
    unit_price = data.get("UnitPrice")

    model_key = f"customer_{model_number}"
    if model_key not in models:
        return jsonify({"error": "Model not found"}), 404

    # Prepare data for prediction
    input_data = [(Vectors.dense([quantity, unit_price]),)]
    df = spark.createDataFrame(input_data, ["features"])

    model = models[model_key]
    prediction = model.transform(df).select("prediction").collect()[0][0]

    return jsonify({
        "model_number": model_number,
        "CustomerID": customer_id,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "cluster": int(prediction),
        "cluster_description": customer_cluster_descriptions.get(int(prediction), "Unknown Cluster")
    })

# Endpoint for clustering products
@app.route('/cluster-product', methods=['POST'])
def cluster_product():
    data = request.get_json()
    model_number = data.get("model_number")
    stock_code = data.get("StockCode")
    quantity = data.get("Quantity")
    unit_price = data.get("UnitPrice")

    model_key = f"product_{model_number}"
    if model_key not in models:
        return jsonify({"error": "Model not found"}), 404

    # Prepare data for prediction
    input_data = [(Vectors.dense([quantity, unit_price]),)]
    df = spark.createDataFrame(input_data, ["features"])

    model = models[model_key]
    prediction = model.transform(df).select("prediction").collect()[0][0]

    return jsonify({
        "model_number": model_number,
        "StockCode": stock_code,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "cluster": int(prediction),
        "cluster_description": product_cluster_descriptions.get(int(prediction), "Unknown Cluster")
    })

# Endpoint for clustering countries
@app.route('/cluster-country', methods=['POST'])
def cluster_country():
    data = request.get_json()
    model_number = data.get("model_number")
    country = data.get("Country")
    quantity = data.get("Quantity")
    unit_price = data.get("UnitPrice")

    model_key = f"country_{model_number}"
    if model_key not in models:
        return jsonify({"error": "Model not found"}), 404

    # Prepare data for prediction
    input_data = [(Vectors.dense([quantity, unit_price]),)]
    df = spark.createDataFrame(input_data, ["features"])

    model = models[model_key]
    prediction = model.transform(df).select("prediction").collect()[0][0]

    return jsonify({
        "model_number": model_number,
        "Country": country,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "cluster": int(prediction),
        "cluster_description": country_cluster_descriptions.get(int(prediction), "Unknown Cluster")
    })

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
