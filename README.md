
# 📊 Big Data Streaming with Kafka and Spark for Retail Clustering 📊

Relevansi dataset yang digunakan : https://www.kaggle.com/datasets/ishanshrivastava28/tata-online-retail-dataset
Relevansi Online Retail Dataset dengan tugas Anda mengenai pemrosesan data streaming menggunakan Kafka dan Apache Spark sangat erat, karena dataset ini mendukung alur kerja sistem Big Data Anda. Berikut penjelasannya:
1. Simulasi Data Streaming: Dataset ini berisi transaksi yang dapat diperlakukan sebagai data aliran, yang akan dikirimkan oleh Kafka Producer ke Kafka Server secara sekuensial.
2. Batching dengan Kafka Consumer: Data transaksi bisa dikelompokkan (batching) oleh Kafka Consumer berdasarkan jumlah atau waktu. Batch ini akan diproses lebih lanjut oleh Spark.
3. Pelatihan Model Clustering dengan Spark: Data yang diterima digunakan untuk melatih model clustering (misalnya, KMeans) untuk mengelompokkan produk atau pelanggan berdasarkan pola pembelian.
4. API untuk Prediksi dan Rekomendasi: Setelah model dilatih, API dapat digunakan untuk memberikan prediksi cluster atau rekomendasi produk kepada pengguna berdasarkan data yang diberikan.


📋 Daftar Isi
- [🛠 Prasyarat](#🛠-prasyarat)
- [📂 Struktur Direktori](#📂-struktur-direktori)
- [📦 Langkah-Langkah Instalasi dan Pengaturan](#📦-langkah-langkah-instalasi-dan-pengaturan)
- [🚀 Penjelasan Program](#🚀-penjelasan-program)
- [🔍 Pengujian Program](#🔍-pengujian-program)
- [🔢 Klasifikasi Data Input ke dalam cluster](#klasifikasi-data-input-ke-dalam-cluster)
- [🌐 Endpoint API untuk Prediksi Clustering](#🌐-endpoint-api-untuk-prediksi-clustering)
- [🎉 Kesimpulan](#🎉-kesimpulan)
- [🛠 Troubleshooting](#🛠-troubleshooting)



## 🛠 Prasyarat
Pastikan Anda memiliki perangkat berikut terinstal di sistem Anda:
- Python (versi 3.7 ke atas)
- Kafka (Apache Kafka, untuk streaming data)
- Apache Spark (untuk melakukan clustering)
- Flask (untuk membuat API)
- Kafka-Python library
- PySpark library

**Instalasi requirements:**
```
pip install Flask pyspark
```

**Catatan:** Anda bisa menginstal Kafka dan Spark melalui package manager atau mengikuti petunjuk di Kafka Documentation dan Spark Documentation.
    
## 📂 Struktur Direktori

    ├── batch                        # Menyimpan file batch dari Kafka Consumer. Setiap file mewakili sekumpulan data streaming
    ├── models                       # Berisi model KMeans yang dilatih menggunakan Spark
    ├── Online_Retail_Dataset.csv    # Dataset retail untuk streaming
    ├── app.py                       # Skrip utama API yang berjalan di Flask untuk melayani endpoint clustering dan rekomendasi
    ├── producer.py                  # Kafka Producer untuk mengirim data
    ├── consumer.py                  # Kafka Consumer untuk batching data
    └── kmeans_spark_training.py     # Program untuk melatih model KMeans

## 📦 Langkah-Langkah Instalasi dan Pengaturan
#### 1. Clone Proyek ini 
```
git clone https://github.com/Tiaaara/Kafka_Bigdata_2.git
cd your-repo
```

#### 2. Instal Dependensi
```
pip install kafka-python pyspark flask
```

### 3. Jalankan Kafka
- Buka terminal baru, masuk ke folder kafka, lalu jalankan Zookeeper:
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
- Di terminal lain, jalankan Kafka Server:
```
bin/kafka-server-start.sh config/server.properties
```

### 4. Siapkan Kafka Topic
- Buat Kafka topic bernama retail_stream yang akan digunakan oleh producer dan consumer.
```
    bin/kafka-topics.sh --create --topic retail_stream --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## 🚀 Penjelasan Program
1. Producer ``(producer.py)``
Producer ini bertugas membaca data dari file Online_Retail_Dataset.csv dan mengirimkannya satu per satu ke Kafka topic retail_stream. Setiap pengiriman diberi jeda acak untuk mensimulasikan aliran data real-time.<br>

**Jalankan Producer:**
```
python producer.py
```
**Note:** Pastikan dataset Online_Retail_Dataset.csv berada di direktori yang sama dengan producer.py. Producer akan menampilkan data yang dikirim ke Kafka di terminal.

2. Consumer (consumer.py)
Consumer menerima data dari Kafka, mengelompokkan data dalam batch berdasarkan ukuran batch atau waktu, lalu menyimpannya sebagai file CSV di folder batch. Setiap file CSV yang dihasilkan berisi sekumpulan data yang telah dikelompokkan dalam batch.<br>

**Jalankan Consumer:**
```
python consumer.py
```
**Notes :** Konsumer akan menampilkan pesan setiap kali batch baru disimpan. File batch akan diberi nama berdasarkan nomor batch dan timestamp.
   
3. Model Training (kmeans_spark_training.py)
Program ini memanfaatkan Spark untuk melatih model clustering KMeans berdasarkan batch data yang telah tersimpan di folder batch. Model yang telah dilatih disimpan di folder models untuk digunakan dalam prediksi.<br>

**Jalankan Model Training:**
```
python kmeans_spark_training.py
```

4. API untuk Prediksi (app.py)
API ini memungkinkan pengguna mengirim data customer, produk, atau negara untuk mendapatkan prediksi cluster. API akan mengembalikan cluster yang paling sesuai berdasarkan model yang telah dilatih.<br>

**Jalankan API:**
```
python app.py
```
**Catatan:** API akan berjalan di http://localhost:5000.


## 🔍 Pengujian Program
#### Langkah-Langkah Pengujian
1. Jalankan Kafka: Pastikan Kafka berjalan dengan perintah di bagian sebelumnya.
2. Jalankan Producer: Jalankan producer.py untuk mulai mengirim data ke Kafka.
3. Jalankan Consumer: Jalankan consumer.py untuk menerima data dan menyimpan batch di folder batch.
4. Jalankan Model Training: Setelah beberapa batch terkumpul, jalankan kmeans_spark_training.py untuk melatih model.
5. Jalankan API: Terakhir, jalankan app.py untuk mengaktifkan endpoint prediksi.


## 🔢 Klasifikasi Data Input ke dalam cluster
**1. Prediksi Customer Cluster**
**Input :**
```
{
    "model_number": "1",
    "CustomerID": 17850,
    "Quantity": 10,
    "UnitPrice": 5.0
}
```
**Output:**
```
{
    "CustomerID": 17850,
    "Quantity": 10,
    "UnitPrice": 5.0,
    "cluster": 2,
    "cluster_description": "Frequent High-Value Customers",
    "model_number": "1"
}
```

**2. Prediksi Product Cluster**
**Input :**
```
{
    "model_number": "1",
    "StockCode": "85123A",
    "Quantity": 10,
    "UnitPrice": 5.0
}
```
**Output :**
```
{
    "StockCode": "85123A",
    "Quantity": 10,
    "UnitPrice": 5.0,
    "cluster": 3,
    "cluster_description": "Popular and Frequently Purchased Products",
    "model_number": "1"
}

```

**3. Prediksi Country Cluster**
**Input :**
```
{
    "model_number": "1",
    "Country": "United Kingdom",
    "Quantity": 10,
    "UnitPrice": 5.0
}
```
**Output :**
```
{
    "Country":"United Kingdom",
    "Quantity":10,
    "UnitPrice":5.0,
    "cluster":1,
    "cluster_description":"Moderate-Spending Countries",
    "model_number":"1"}
```

## 🌐 Endpoint API untuk Prediksi Clustering
Berikut adalah contoh penggunaan endpoint dengan perintah curl:
#### 1. Prediksi Customer Cluster
```
    curl -X POST http://localhost:5000/cluster-customer \
-H "Content-Type: application/json" \
-d '{
    "model_number": "1", 
    "CustomerID": 17850, 
    "Quantity": 10, 
    "UnitPrice": 5.0
}'
```

#### 2. Prediksi Product Cluster
```
    curl -X POST http://localhost:5000/cluster-product \
-H "Content-Type: application/json" \
-d '{
    "model_number": "1", 
    "StockCode": "85123A", 
    "Quantity": 10, 
    "UnitPrice": 5.0
}'
```

#### 3. Prediksi Country Cluster
```
    curl -X POST http://localhost:5000/cluster-country \
-H "Content-Type: application/json" \
-d '{
    "model_number": "1", 
    "Country": "United Kingdom", 
    "Quantity": 10, 
    "UnitPrice": 5.0
}'
```
    
## 🎉 Kesimpulan
Proyek ini memberikan gambaran lengkap tentang Big Data Streaming menggunakan Kafka dan Spark. Dengan pipeline ini, kita dapat mengalirkan data secara terus-menerus, memproses batch data, melakukan clustering, dan menyediakan API untuk prediksi secara real-time! 🌟

## 🛠 Troubleshooting
- **Model Tidak Ditemukan**: Pastikan model Anda tersimpan di folder `models` dengan nama seperti `kmeans_model_1`, `kmeans_model_2`, dll.
- **Pengaturan Kafka**: Pastikan Kafka berjalan dan data dikirim dengan benar untuk pemrosesan batch.
- **Path File**: Sesuaikan path file jika menggunakan struktur direktori yang berbeda.
