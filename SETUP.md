# Ship Risk AI - Setup Guide

## Overview
Ship Risk AI is an Intelligent Shipment Risk Management & Early Warning System with:
- Python ML backend for risk prediction
- React TypeScript frontend with modern UI
- FastAPI server for API integration
- Firebase-ready authentication

## Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Sample Data & Train Model

```bash
# Run the full ML pipeline (generates data, trains model, creates alerts)
python main_pipeline.py --mode full --train-samples 5000 --live-samples 500

# This will create:
# - data/shipments_raw.csv - Training data
# - data/live_shipments.csv - Live shipment data for demo
# - outputs/alerts.csv - Generated alerts
# - outputs/recommendations.csv - AI recommendations
# - artifacts/best_model.pkl - Trained ML model
```

### 3. Start API Server

```bash
# In a new terminal (with venv activated)
python api_server.py

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 4. Install Frontend Dependencies

```bash
cd ship-risk-ai
npm install
```

### 5. Start Frontend Development Server

```bash
npm run dev

# Frontend will be available at http://localhost:5173
```

## Project Structure

```
.
├── data/                          # Generated data
│   ├── shipments_raw.csv         # Training data
│   └── live_shipments.csv        # Live shipments
├── outputs/                       # System outputs
│   ├── alerts.csv                # Risk alerts
│   └── recommendations.csv       # AI recommendations
├── artifacts/                     # ML artifacts
│   ├── best_model.pkl           # Trained model
│   ├── scaler.pkl               # Feature scaler
│   └── feature_cols.pkl         # Feature names
├── ship-risk-ai/                 # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── contexts/            # React contexts
│   │   ├── services/            # API services
│   │   ├── types/               # TypeScript types
│   │   └── utils/               # Utilities
│   └── package.json
├── data_generator.py             # Synthetic data generation
├── feature_engineering.py        # Feature processing
├── model_training.py             # ML model training
├── risk_scoring.py               # Risk scoring engine
├── recommendation_engine.py      # Recommendation system
├── main_pipeline.py              # Main orchestration
├── api_server.py                 # FastAPI server
└── requirements.txt              # Python dependencies
```

## Python Backend Components

### Data Generator (`data_generator.py`)
Generates realistic synthetic shipment data with:
- Carrier information (FedEx, DHL, UPS, Maersk, etc.)
- Routes (origin/destination pairs)
- Weather conditions and severity
- Traffic and port congestion
- Disruptions (port strikes, natural disasters, etc.)

### Feature Engineering (`feature_engineering.py`)
Processes raw data into ML-ready features:
- Cleans and validates data
- Engineers composite risk scores
- Encodes categorical variables
- Scales numerical features

### Model Training (`model_training.py`)
Trains and evaluates multiple ML models:
- Logistic Regression
- Random Forest
- Gradient Boosting
- Extra Trees

Selects the best model based on ROC-AUC score.

### Risk Scoring (`risk_scoring.py`)
Real-time risk assessment:
- Loads trained model
- Scores shipments for delay probability
- Classifies risk tiers (LOW/MEDIUM/HIGH/CRITICAL)
- Generates alerts with action recommendations

### Recommendation Engine (`recommendation_engine.py`)
AI-powered intervention suggestions:
- REROUTE - Alternative transit path
- ALT_CARRIER - Switch carrier
- MODE_SWITCH_AIR - Upgrade to air freight
- PRIORITY_HANDLING - Expedited processing
- CUSTOMER_ALERT - Proactive notification

## API Endpoints

### Shipments
- `GET /api/shipments` - List all shipments
- `GET /api/shipments/{id}` - Get shipment details

### Alerts
- `GET /api/alerts?min_tier=MEDIUM` - Get alerts (filtered by tier)

### Recommendations
- `POST /api/recommendations` - Get recommendations for shipment
  ```json
  {"shipment_id": "SHP100123"}
  ```

### Analytics
- `GET /api/analytics` - Get system-wide metrics

### Interventions
- `POST /api/interventions` - Execute intervention
  ```json
  {"shipment_id": "SHP100123", "action": "REROUTE"}
  ```

## Frontend Features

### Dashboard
- Real-time risk metrics
- Risk distribution charts
- Alert trend visualization
- Active alerts overview

### Shipments
- Complete shipment list
- Advanced filtering
- Shipment detail modal
- Risk tier color coding

### Alerts
- Filterable alert list
- Risk tier breakdown
- Time to SLA tracking
- Action recommendations

### Recommendations
- AI-powered suggestions
- Cost/benefit analysis
- Confidence scoring
- One-click execution

### Analytics
- Comprehensive metrics
- Historical trends
- Carrier performance
- Risk distribution

## Firebase Integration (Optional)

The app is Firebase-ready for authentication and real-time features.

### Setup Steps:

1. Create Firebase project at https://console.firebase.google.com/

2. Enable Authentication:
   - Go to Authentication > Get Started
   - Enable Email/Password provider

3. Get Firebase config:
   - Project Settings > Your apps
   - Copy config values

4. Create `.env.local` in `ship-risk-ai/`:
   ```env
   VITE_FIREBASE_API_KEY=your_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   ```

5. Restart frontend dev server

## Production Build

### Frontend
```bash
cd ship-risk-ai
npm run build

# Build output in ship-risk-ai/dist/
```

### Backend
The API server can be run in production with:
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### No data showing in frontend
1. Make sure you ran `python main_pipeline.py --mode full`
2. Check that `data/live_shipments.csv` exists
3. Verify API server is running on port 8000
4. Check browser console for API errors

### API connection errors
1. Verify API is running: http://localhost:8000/health
2. Check CORS settings in `api_server.py`
3. Ensure frontend is using correct API URL

### Model training errors
1. Ensure all dependencies are installed
2. Check Python version (3.8+)
3. Verify virtual environment is activated

## Development Commands

### Python Backend
```bash
# Generate new data
python data_generator.py

# Train model only
python main_pipeline.py --mode train --train-samples 6000

# Generate predictions only
python main_pipeline.py --mode predict --live-samples 500

# Run demo scenario
python main_pipeline.py --mode demo

# Full pipeline
python main_pipeline.py --mode full
```

### Frontend
```bash
cd ship-risk-ai

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Support

For issues or questions:
1. Check the API health endpoint: http://localhost:8000/health
2. Review logs in terminal
3. Check browser console for frontend errors

## License

Proprietary - Ship Risk AI
