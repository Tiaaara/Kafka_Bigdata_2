from flask import Flask, request, jsonify
from pyspark.ml.clustering import KMeansModel
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType
from pyspark.ml.linalg import Vectors
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RetailKMeansAPI") \
    .getOrCreate()

# Load KMeans models from the models directory
model_dir = "./models"
models = {}
for model_file in os.listdir(model_dir):
    if model_file.startswith("kmeans_model_"):
        model_number = model_file.split("_")[-1]
        model_path = os.path.join(model_dir, model_file)
        models[model_number] = KMeansModel.load(model_path)
        print(f"Loaded {model_file} as Model {model_number}")

# 1. /cluster: Classify input data into a cluster
@app.route('/cluster', methods=['POST'])
def cluster():
    data = request.get_json()
    model_number = data.get("model_number")
    quantity = data.get("Quantity")
    unit_price = data.get("UnitPrice")

    if model_number not in models:
        return jsonify({"error": "Model not found"}), 404

    input_data = [(Vectors.dense([quantity, unit_price]),)]
    df = spark.createDataFrame(input_data, ["features"])

    model = models[model_number]
    prediction = model.transform(df).select("prediction").collect()[0][0]

    return jsonify({
        "model_number": model_number,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "cluster": int(prediction)
    })

# 2. /recommend: Provide product recommendations based on cluster
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    model_number = data.get("model_number")
    quantity = data.get("Quantity")
    unit_price = data.get("UnitPrice")

    if model_number not in models:
        return jsonify({"error": "Model not found"}), 404

    input_data = [(Vectors.dense([quantity, unit_price]),)]
    df = spark.createDataFrame(input_data, ["features"])

    model = models[model_number]
    cluster = model.transform(df).select("prediction").collect()[0][0]

    recommendations = {
        0: ["Product A", "Product B"],
        1: ["Product C", "Product D"],
        2: ["Product E", "Product F"]
    }
    recommended_products = recommendations.get(cluster, [])

    return jsonify({
        "model_number": model_number,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "cluster": int(cluster),
        "recommendations": recommended_products
    })

# 3. /cluster-info: Get information about each cluster
@app.route('/cluster-info', methods=['POST'])
def cluster_info():
    data = request.get_json()
    model_number = data.get("model_number")

    if model_number not in models:
        return jsonify({"error": "Model not found"}), 404

    model = models[model_number]
    centers = model.clusterCenters()
    cluster_info = [{"cluster": i, "center": center.tolist()} for i, center in enumerate(centers)]

    return jsonify({
        "model_number": model_number,
        "cluster_info": cluster_info
    })

# 4. /all-models: List all loaded models
@app.route('/all-models', methods=['GET'])
def all_models():
    model_list = [{"model_number": model_number} for model_number in models.keys()]
    return jsonify({
        "models": model_list
    })

# 5. /model-summary: Get summary of a specific model (e.g., cluster centers)
@app.route('/model-summary', methods=['POST'])
def model_summary():
    data = request.get_json()
    model_number = data.get("model_number")

    if model_number not in models:
        return jsonify({"error": "Model not found"}), 404

    model = models[model_number]
    centers = model.clusterCenters()
    summary = [{"cluster": i, "center": center.tolist()} for i, center in enumerate(centers)]

    return jsonify({
        "model_number": model_number,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
