<div align="center">

# 🔒 Network Security System

**Phishing Website Detection using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E.svg)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.7+-0194E2.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready machine learning pipeline for detecting phishing websites using classification algorithms with MongoDB data ingestion, MLflow experiment tracking, and FastAPI deployment.

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [API](#-api-documentation) • [Deployment](#-deployment) • [Contributing](#-contributing)

</div>

---

## ✨ Features

| Module | Capabilities |
|--------|--------------|
| **Data Ingestion** | MongoDB data loading, train/test split, feature store |
| **Data Validation** | Schema validation, data drift detection using KS-test |
| **Data Transformation** | KNN imputation, missing value handling |
| **Model Training** | 5 classifiers, hyperparameter tuning, model selection |
| **Experiment Tracking** | MLflow, DagsHub integration, metrics logging |
| **Deployment** | FastAPI REST API, Docker, AWS EC2 deployment |
| **Cloud Sync** | Automatic artifact and model sync to AWS S3 |

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Ingestion │────▶│ Data Validation │────▶│ Data Transform  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  AWS S3 Sync    │◀────│ Model Training  │◀────│  Preprocessor   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Docker Image   │◀────│  FastAPI App    │◀────│ Trained Model   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 📁 Project Structure

```
Network-Security-System/
├── 📄 app.py                          # FastAPI Application
├── 📄 main.py                         # Training Pipeline Entrypoint
├── 📄 requirements.txt                # Dependencies
├── 📄 setup.py                        # Package Configuration
├── 📄 Dockerfile                      # Docker Configuration
├── 📄 README.md                       # You are here
├── 📄 .env.example                    # Environment Variables Template
├── 📄 .gitignore                      # Git Ignore Rules
│
├── 📂 .github/workflows/              # CI/CD Configuration
│   └── main.yml                       # GitHub Actions Pipeline
│
├── 📂 networksecurity/                # Main Python Package
│   ├── __init__.py
│   ├── 📂 exception/
│   │   └── exception.py               # Custom Exception Handler
│   ├── 📂 logging/
│   │   └── logger.py                  # Logging Configuration
│   ├── 📂 entity/
│   │   ├── config_entity.py           # Configuration Data Classes
│   │   └── artifact_entity.py         # Pipeline Artifacts
│   ├── 📂 constant/
│   │   └── training_pipeline/         # Pipeline Constants
│   ├── 📂 components/
│   │   ├── data_ingestion.py          # MongoDB Data Loader
│   │   ├── data_validation.py         # Schema & Drift Check
│   │   ├── data_transformation.py     # KNN Imputation
│   │   └── model_trainer.py           # Model Training & Evaluation
│   ├── 📂 pipeline/
│   │   ├── training_pipeline.py       # End-to-End Training Orchestrator
│   │   └── batch_prediction.py        # Batch Prediction Pipeline
│   ├── 📂 cloud/
│   │   └── s3_syncer.py               # AWS S3 Integration
│   └── 📂 utils/
│       ├── main_utils.py              # I/O Utilities (YAML, Pickle)
│       └── ml_utils/
│           ├── estimator.py           # Model Wrapper Class
│           └── classification_metric.py # Evaluation Metrics
│
├── 📂 Network_Data/                   # Raw Dataset
│   └── phisingData.csv                # 11,055 samples, 31 features
│
├── 📂 data_schema/
│   └── schema.yaml                    # Data Schema Definition
│
├── 📂 templates/
│   └── table.html                     # Prediction Results Template
│
└── 📂 final_model/                    # Production Models
    ├── model.pkl                      # Trained Classifier
    └── preprocessor.pkl               # Fitted Preprocessor
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- MongoDB Atlas Account (or local MongoDB)
- AWS Account (optional, for S3 sync)
- Docker (optional, for containerization)

### Step 1: Clone the Repository

```bash
git clone https://github.com/theshivammishra10/Network-Security-System.git
cd Network-Security-System
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .  # Install package in development mode
```

### Step 4: Configure Environment Variables

```bash
# Copy the template
cp .env .env.local

# Edit with your credentials
# Add MONGO_DB_URL, DAGSHUB credentials, AWS keys
```

**Required Environment Variables:**
```env
# MongoDB Connection
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority

# DagsHub (MLflow Tracking)
DAGSHUB_REPO_OWNER=your_username
DAGSHUB_REPO_NAME=Network-Security-System
MLFLOW_TRACKING_URI=https://dagshub.com/your_username/Network-Security-System.mlflow

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
AWS_REGION=us-east-1
```

### Step 5: Data Setup

```bash
# Push dataset to MongoDB
python push_data.py
```

---

## 💻 Usage

### Training the Model

Run the complete training pipeline:

```bash
python main.py
```

**Pipeline Execution Stages:**
1. ✅ **Data Ingestion**: Load data from MongoDB → 80/20 train/test split
2. ✅ **Data Validation**: Schema check + dataset drift detection
3. ✅ **Data Transformation**: KNN imputation for missing values
4. ✅ **Model Training**: Train 5 classifiers, select best performing
5. ✅ **Model Evaluation**: F1, Precision, Recall metrics
6. ✅ **Cloud Sync**: Upload artifacts and model to S3

### Start the API Server

```bash
python app.py
```

Server will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000

---

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/` | API root, redirects to documentation | - |
| `GET` | `/train` | Trigger full training pipeline | - |
| `POST` | `/predict` | Predict phishing probability | `multipart/form-data` with CSV file |

### Example Predict Request

```bash
curl -X POST -F "file=@test_data.csv" http://localhost:8000/predict
```

**Response:**
- HTML table with predictions
- Results saved to `prediction_output/output.csv`
- `predicted_column`: 1 = Phishing, 0 = Legitimate

---

## 🧪 Testing

```bash
# Run full test suite
python test_app.py

# Test prediction only
python -c "from networksecurity.utils.main_utils.utils import load_object; from networksecurity.utils.ml_utils.model.estimator import NetworkModel; pre = load_object('final_model/preprocessor.pkl'); model = load_object('final_model/model.pkl'); print('Model loaded successfully')"
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t network-security-system .
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env.local network-security-system
```

### AWS EC2 Deployment

```bash
# 1. SSH into EC2 instance
ssh ubuntu@<ec2-public-ip>

# 2. Install Docker
sudo apt-get update && sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker

# 3. Pull and run
docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 788614365622.dkr.ecr.us-east-1.amazonaws.com
docker pull 788614365622.dkr.ecr.us-east-1.amazonaws.com/networkssecurity:latest
docker run -d -p 80:8000 --env-file .env 788614365622.dkr.ecr.us-east-1.amazonaws.com/networkssecurity:latest
```

---

## 📊 MLflow Experiment Tracking

View experiments at:
```bash
# Local UI
mlflow ui

# DagsHub UI
https://dagshub.com/theshivammishra10/Network-Security-System
```

Tracked metrics:
- `train_f1`, `test_f1`
- `train_precision`, `test_precision`
- `train_recall`, `test_recall`

---

## ⚙️ Configuration

### Model Parameters

| Model | Hyperparameters |
|-------|-----------------|
| Random Forest | `n_estimators`: [16, 32, 64, 128] |
| Decision Tree | `criterion`: ['gini', 'entropy', 'log_loss'] |
| Gradient Boosting | `learning_rate`: [0.1, 0.01], `n_estimators`: [32, 64, 128] |
| AdaBoost | `learning_rate`: [0.1, 0.01], `n_estimators`: [32, 64, 128] |

### Dataset Features

31 input features including:
- URL characteristics (length, special characters)
- DNS and domain age
- Page content properties
- SSL certificate information

---

## 🔒 Security Notes

- **Never commit `.env` file** - Contains sensitive credentials
- All secrets are loaded from environment variables
- MongoDB connection uses TLS encryption
- API endpoints are CORS enabled for production use
- Model artifacts are sanitized before deployment

---

## 🛠️ Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| **MongoDB Connection Error** | Verify `MONGO_DB_URL` and IP whitelist in Atlas |
| **ModuleNotFoundError** | Run `pip install -e .` to install package |
| **AWS S3 Sync Failed** | Check AWS credentials and IAM permissions |
| **MLflow Connection Error** | Verify DagsHub token and tracking URI |

### Logs

Application logs are stored in `logs/` directory with timestamp-based filenames.

---

## 📈 Performance

Best model performance (Random Forest):
- **F1 Score**: 0.952
- **Precision**: 0.961
- **Recall**: 0.943
- **Accuracy**: 94.7%

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**Author**: Shivam Mishra  
**Contact**: theshivammishra10@gmail.com  
**Repository**: [github.com/theshivammishra10/Network-Security-System](https://github.com/theshivammishra10/Network-Security-System)

</div>