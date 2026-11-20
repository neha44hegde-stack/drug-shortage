# AI Drug Shortage Prediction System

An AI-powered pharmacy management system designed to predict potential medicine shortages using machine learning and support better inventory management.

## Project Overview

The AI Drug Shortage Prediction System helps pharmacies monitor medicine inventory, analyze demand patterns, identify potential shortages and make informed stock management decisions.

The project combines machine learning, a pharmacy management application and a web-based interface.

## Key Features

- **Drug Shortage Prediction:** Uses an XGBoost classification model to predict shortage status.
- **Medicine Management:** Manage medicine records and inventory.
- **Inventory Monitoring:** Track available stock and low-stock medicines.
- **Sales Management:** Maintain and analyze sales information.
- **Demand Forecasting:** Analyze medicine demand.
- **Prediction History:** Maintain prediction records.
- **Alerts and Reports:** Support inventory monitoring and reporting.
- **Weather Trends:** Includes weather-related information for analysis.
- **Multi-Branch Optimization:** Supports pharmacy branch management features.

## Technologies Used

| Component | Technologies |
|---|---|
| Programming Languages | Python, TypeScript, JavaScript |
| Machine Learning | XGBoost, Scikit-learn, Pandas |
| Frontend | React.js, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| Application Interface | Streamlit |
| Model Storage | Joblib, Pickle |

## Machine Learning Model

The project uses an XGBoost Classifier to predict medicine shortage status.

**Input Features:**
- Drug Name
- Demand Quantity
- Available Stock
- Temperature
- Humidity
- Rainfall
- Age Group
- Severity Level

**Target Variable:** Shortage Status

The dataset is processed using Label Encoding for categorical features and divided into training and testing sets using an 80:20 split.

## Project Structure

```text
AI_Drug_Shortage_Prediction/
│
├── app/
│   ├── dataset/
│   ├── templates/
│   ├── static/
│   ├── train_model.py
│   └── app.py
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
└── model/
    └── drug_shortage_model.pkl
```

## Installation

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables using `.env.example` and run:

```bash
uvicorn app.main:app --reload
```

API documentation:

`http://localhost:8000/api/docs`

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

### Streamlit Application

The project also contains a Streamlit application in the `app` directory. Refer to its Python dependencies before running it.

## Machine Learning Training

Navigate to the application directory and run:

```bash
python train_model.py
```

The trained model is saved as `drug_shortage_model.pkl` in the model directory.

## Project Purpose

The objective is to explore how machine learning and software development can support pharmacy inventory monitoring and help identify potential medicine shortages.

## Contributors
 Neha Hegde

## License

This project is developed for academic purposes.
