# Network Security System - Phishing Detection

A machine learning-based network security system for detecting phishing websites using classification algorithms. The project implements a complete ML pipeline with data ingestion from MongoDB, validation, transformation, model training, and prediction via a FastAPI web interface.

## Project Overview

This project is designed to:
- Detect phishing websites based on various URL and website features
- Use machine learning classification models (Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost)
- Provide a REST API for predictions via FastAPI
- Track experiments using MLflow and DagsHub
- Deploy on AWS with Docker

## Project Structure

```
Network Security System/
├── app.py                          # FastAPI application (main entry point)
├── main.py                        # Training pipeline script
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup file
├── Dockerfile                     # Docker configuration
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
├── .github/workflows/
│   └── main.yml                   # GitHub Actions CI/CD
│
├── networksecurity/                # Main package
│   ├── __init__.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── exception.py           # Custom exception handling
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logger.py              # Logging configuration
│   ├── entity/
│   │   ├── __init__.py
│   │   ├── config_entity.py       # Configuration classes
│   │   └── artifact_entity.py    # Artifact data classes
│   ├── constant/
│   │   ├── __init__.py
│   │   └── training_pipeline/
│   │       └── __init__.py        # Pipeline constants
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py      # MongoDB data loading
│   │   ├── data_validation.py   # Schema & drift validation
│   │   ├── data_transformation.py # KNN imputation & transformation
│   │   └── model_trainer.py      # Model training & evaluation
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── training_pipeline.py  # Full training orchestration
│   │   └── batch_prediction.py   # Batch prediction
│   ├── cloud/
│   │   ├── __init__.py
│   │   └── s3_syncer.py          # AWS S3 sync utility
│   └── utils/
│       ├── __init__.py
│       ├── main_utils/
│       │   ├── __init__.py
│       │   └── utils.py          # YAML, pickle, numpy utilities
│       └── ml_utils/
│           ├── __init__.py
│           ├── model/
│           │   ├── __init__.py
│           │   └── estimator.py   # NetworkModel wrapper
│           └── metric/
│               ├── __init__.py
│               └── classification_metric.py # F1, precision, recall
│
├── networksecurity/               # (duplicate for package reference)
│
├── Network_Data/
│   └── phisingData.csv            # Original dataset
│
├── data_schema/
│   └── schema.yaml                # Data schema definition
│
├── final_model/
│   ├── model.pkl                  # Trained model
│   └── preprocessor.pkl           # Fitted preprocessor
│
├── templates/
│   └── table.html                 # HTML template for predictions
│
├── prediction_output/
│   └── output.csv                 # Prediction results
│
├── valid_data/
│   └── test.csv                  # Test data
│
├── logs/                          # Application logs
│
└── mlflow.db                      # MLflow tracking database
```

## Features

1. **Data Ingestion**: Loads data from MongoDB database
2. **Data Validation**: Validates schema and detects data drift
3. **Data Transformation**: KNN imputation for missing values
4. **Model Training**: Multiple classifiers with hyperparameter tuning
5. **MLflow Tracking**: Experiment tracking on DagsHub
6. **FastAPI Web Service**: REST API for real-time predictions
7. **AWS S3 Sync**: Upload artifacts and models to S3

## Prerequisites

- Python 3.10 or higher
- MongoDB (local or Atlas)
- AWS Account (for S3 storage)
- Docker (optional for containerization)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/theshivammishra10/Network-Security-System.git
cd Network-Security-System
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package:

```bash
pip install -e .
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# MongoDB Connection
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority

# AWS Credentials (for S3 sync)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# MLflow Tracking
MLFLOW_TRACKING_URI=https://dagshub.com/your_username/Network-Security-System.mlflow
```

### Getting MongoDB URL

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster and get your connection string
3. Replace `<username>` and `<password>` with your credentials

## Data Setup

### Option 1: Push CSV to MongoDB

```bash
python push_data.py
```

This script:
- Reads `Network_Data/phisingData.csv`
- Converts to JSON format
- Inserts into MongoDB database `SHIVAMAI`, collection `networksecurity`

### Option 2: Use Existing Data

The project is pre-configured to use:
- Database: `SHIVAMAI`
- Collection: `networksecurity`
- Ensure your MongoDB has the data before running

## Running the Project

### Training the Model

Run the full training pipeline:

```bash
# Method 1: Using main.py
python main.py

# Method 2: Using training pipeline
python -c "from networksecurity.pipeline.training_pipeline import TrainingPipeline; tp = TrainingPipeline(); tp.run_pipeline()"

# Method 3: Via API endpoint
# Start the server and visit http://localhost:8000/train
```

The training pipeline performs:
1. Data Ingestion (MongoDB → train/test split)
2. Data Validation (schema check + drift detection)
3. Data Transformation (KNN imputation)
4. Model Training (5 classifiers, best selected)
5. S3 sync (artifacts + model)

### Starting the Web Server

```bash
python app.py
```

Or with uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirect to Swagger docs |
| GET | `/train` | Trigger model training |
| POST | `/predict` | Upload CSV for prediction |

### Making Predictions

```bash
# Using curl
curl -X POST -F "file=@your_data.csv" http://localhost:8000/predict

# Or use Swagger UI at http://localhost:8000/docs
```

## Testing

```bash
# Test prediction
python test_app.py

# Or test individual components
python -c "from networksecurity.components.data_ingestion import DataIngestion; print('DataIngestion imported successfully')"
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t network-security-app .
```

### Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env network-security-app
```

### AWS EC2 Deployment

1. **Setup Docker on EC2**:
```bash
sudo apt-get update -y
sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

2. **Pull and Run**:
```bash
docker pull 788614365622.dkr.ecr.us-east-1.amazonaws.com/networkssecurity:latest
docker run -p 8000:8000 -e MONGO_DB_URL=your_mongo_url networksecurity
```

## GitHub Secrets (for CI/CD)

Configure these secrets in your GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region (e.g., us-east-1) |
| `AWS_ECR_LOGIN_URI` | ECR login URI |
| `ECR_REPOSITORY_NAME` | ECR repository name |

## MLflow & DagsHub

- MLflow UI: `mlflow ui` (local)
- DagsHub: https://dagshub.com/theshivammishra10/Network-Security-System

## Output Files

| File | Description |
|------|-------------|
| `final_model/model.pkl` | Trained classifier |
| `final_model/preprocessor.pkl` | Fitted KNN imputer |
| `prediction_output/output.csv` | Prediction results |
| `logs/*.log` | Application logs |

## Troubleshooting

### MongoDB Connection Error
- Check your `.env` file has correct `MONGO_DB_URL`
- Ensure MongoDB IP whitelist includes your IP

### Module Not Found Error
- Ensure you've installed the package: `pip install -e .`
- Or add project root to PYTHONPATH

### AWS S3 Sync Error
- Verify AWS credentials in `.env`
- Check IAM permissions for S3 operations

## License

MIT License

## Author

Shivam Mishra - theshivammishra10@gmail.com