# AI Pharmacy Management System - FastAPI Backend

Professional backend API for AI-powered pharmacy management with drug shortage prediction.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token

### Medicine Endpoints
- `GET /api/medicines` - Get all medicines
- `GET /api/medicines/low-stock` - Get low stock medicines
- `GET /api/medicines/out-of-stock` - Get out of stock medicines
- `GET /api/medicines/{id}` - Get specific medicine
- `POST /api/medicines` - Create medicine (Admin)
- `PUT /api/medicines/{id}` - Update medicine (Admin)
- `DELETE /api/medicines/{id}` - Delete medicine (Admin)

### Sales Endpoints
- `GET /api/sales` - Get all sales
- `GET /api/sales/statistics/today` - Today's sales stats
- `GET /api/sales/statistics/monthly` - Monthly sales stats
- `GET /api/sales/{id}` - Get specific sale
- `POST /api/sales` - Create new sale

### Prediction Endpoints
- `GET /api/predictions` - Get all predictions
- `GET /api/predictions/shortages` - Get shortage predictions
- `GET /api/predictions/{id}` - Get specific prediction
- `POST /api/predictions` - Create prediction

### Dashboard Endpoints
- `GET /api/dashboard/stats` - Get dashboard statistics

## 🔐 Authentication

All endpoints (except `/api/auth/register` and `/api/auth/login`) require authentication using Bearer token.

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8000/api/medicines
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

## 📦 Database

The system uses SQLite by default. To use PostgreSQL:

1. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/pharmacy_db
   ```

2. Install PostgreSQL:
   ```bash
   pip install psycopg2-binary
   ```

## 🚢 Deployment

### Using Docker

```bash
docker build -t pharmacy-api .
docker run -p 8000:8000 pharmacy-api
```

### Using Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Using Render

1. Connect GitHub repository
2. Set environment variables
3. Deploy

## 📝 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── security.py             # Authentication
│   └── routes/
│       ├── __init__.py
│       ├── auth.py             # Auth endpoints
│       ├── medicines.py        # Medicine endpoints
│       ├── sales.py            # Sales endpoints
│       ├── predictions.py      # Prediction endpoints
│       └── dashboard.py        # Dashboard endpoints
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## 👥 Team

- Angel Beulah K
- Sinchana A P
- Vennela G
- Neha Hegde

## 📄 License

© 2026 AI Pharmacy Management System. All rights reserved.
