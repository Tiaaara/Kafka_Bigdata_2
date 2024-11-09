
# 📊 Retail KMeans API 🛒

Selamat datang di **Retail KMeans API**! API ini menggunakan kekuatan **KMeans Clustering** untuk menganalisis data retail, memberikan rekomendasi produk, dan banyak lagi. Dapatkan wawasan tentang pola pembelian pelanggan, klasifikasi cluster, dan ringkasan model – semuanya lewat API sederhana. 🚀

## 📂 Struktur Proyek

- **`batch`**: Menyimpan file batch dari Kafka Consumer. Setiap file mewakili sekumpulan data streaming 🗂️.
- **`models`**: Berisi model KMeans yang dilatih menggunakan Spark 🎓.
- **`app.py`**: Skrip utama API yang berjalan di Flask untuk melayani endpoint clustering dan rekomendasi 🌐.

## 🔧 Persyaratan

Pastikan Anda sudah menginstal:
- **Python 3.7+** 🐍
- **Flask** untuk server API 🌐
- **PySpark** untuk memuat model KMeans 🔥

Instalasi requirements:
```bash
pip install Flask pyspark
```

## 🚀 Cara Kerja

1. **Kafka Producer** mengalirkan data baris demi baris ke Kafka. 📈
2. **Kafka Consumer** membaca dan membagi data menjadi batch, lalu menyimpannya sebagai file CSV di folder `batch`. 📥
3. **Training Spark KMeans** menggunakan file batch ini untuk melatih dan menyimpan model KMeans di folder `models`. 🤖
4. **API Flask** memuat model-model ini dan menyediakan lima endpoint untuk clustering, rekomendasi, dan ringkasan model. 🎉

## 🌈 Endpoint API

### 1. `/cluster` 📍
Klasifikasikan data input ke dalam cluster!

**Request**:
```json
{
    "model_number": "1",
    "Quantity": 10,
    "UnitPrice": 5.0
}
```

**Response**:
```json
{
    "model_number": "1",
    "Quantity": 10,
    "UnitPrice": 5.0,
    "cluster": 2
}
```

---

### 2. `/recommend` 🎁
Dapatkan rekomendasi produk berdasarkan cluster! (Cocok untuk aplikasi e-commerce) 🛍️

**Request**:
```json
{
    "model_number": "1",
    "Quantity": 10,
    "UnitPrice": 5.0
}
```

**Response**:
```json
{
    "model_number": "1",
    "Quantity": 10,
    "UnitPrice": 5.0,
    "cluster": 2,
    "recommendations": ["Product E", "Product F"]
}
```

---

### 3. `/cluster-info` 🧩
Dapatkan informasi tentang setiap cluster dalam model! Berguna untuk menganalisis karakteristik cluster. 🕵️‍♂️

**Request**:
```json
{
    "model_number": "1"
}
```

**Response**:
```json
{
    "model_number": "1",
    "cluster_info": [
        {
            "cluster": 0,
            "center": [12.5, 7.8]
        },
        {
            "cluster": 1,
            "center": [10.2, 3.4]
        }
    ]
}
```

---

### 4. `/all-models` 📑
Melihat daftar semua model yang dimuat! Cepat untuk referensi model. 🧾

**Request**: Tidak perlu input apa pun.

**Response**:
```json
{
    "models": [
        {"model_number": "1"},
        {"model_number": "2"},
        {"model_number": "3"}
    ]
}
```

---

### 5. `/model-summary` 📝
Dapatkan ringkasan dari model tertentu, termasuk pusat cluster! 📊

**Request**:
```json
{
    "model_number": "1"
}
```

**Response**:
```json
{
    "model_number": "1",
    "summary": [
        {"cluster": 0, "center": [12.5, 7.8]},
        {"cluster": 1, "center": [10.2, 3.4]}
    ]
}
```

## 🎬 Cara Menjalankan


### 1. Menyalakan Zookeeper dan Kafka Server

1. **Mulai Zookeeper** (buka terminal baru):
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

2. **Mulai Kafka Server** (buka terminal baru):
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

3. **Buat Kafka Topic** untuk mengalirkan data (jalankan ini di terminal yang sudah terhubung ke Kafka):
   ```bash
   bin/kafka-topics.sh --create --topic retail_stream --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
   ```

### 2. Menjalankan Kafka Producer

Kafka Producer akan mengalirkan data dari dataset baris demi baris ke topic `retail_stream` di Kafka.

**Jalankan Producer**: 
   ```bash
   python kafka_producer.py
   ```

### 3. Menjalankan Kafka Consumer untuk Membuat Batch

Kafka Consumer ini akan membaca data dari Kafka topic `retail_stream`, membentuk batch, dan menyimpannya ke folder `batch`.

**Jalankan Consumer**: 
   ```bash
   python kafka_consumer.py
   ```

### 4. Melatih Model KMeans dengan Spark
File spark ini akan membaca file batch dari folder batch, melatih model KMeans, dan menyimpannya ke folder models.

**Jalankan Training**: 
   ```bash
   spark-submit spark_kmeans_training.py
   ```

### 5. Menjalankan API Flask

API ini memuat model dari folder `models` dan menyediakan 5 endpoint untuk clustering, rekomendasi, dan lainnya.

**Menjalankan API**:
   ```bash
   python app.py
   ```

API akan berjalan di `http://localhost:5000`.

### 6. Uji Endpoint
Gunakan `curl` atau aplikasi API (seperti Postman) untuk menguji endpoint. 

### Contoh Permintaan `curl`

#### Klasifikasi Data dengan `/cluster`
```bash
curl -X POST http://localhost:5000/cluster -H "Content-Type: application/json" -d '{"model_number": "1", "Quantity": 10, "UnitPrice": 5.0}'
```

#### Mendapatkan Rekomendasi dengan `/recommend`
```bash
curl -X POST http://localhost:5000/recommend -H "Content-Type: application/json" -d '{"model_number": "1", "Quantity": 10, "UnitPrice": 5.0}'
```

---

## 🛠 Troubleshooting

- **Model Tidak Ditemukan**: Pastikan model Anda tersimpan di folder `models` dengan nama seperti `kmeans_model_1`, `kmeans_model_2`, dll.
- **Pengaturan Kafka**: Pastikan Kafka berjalan dan data dikirim dengan benar untuk pemrosesan batch.
- **Path File**: Sesuaikan path file jika menggunakan struktur direktori yang berbeda.




