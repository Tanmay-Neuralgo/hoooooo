from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

app = FastAPI(title="Ship Risk AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "/home/claude/shipment_ews/data"
OUTPUT_DIR = "/home/claude/shipment_ews/outputs"
ARTIFACTS_DIR = "/home/claude/shipment_ews/artifacts"

class InterventionRequest(BaseModel):
    shipment_id: str
    action: str

class RecommendationRequest(BaseModel):
    shipment_id: str

@app.get("/")
def read_root():
    return {
        "message": "Ship Risk AI API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/shipments")
def get_shipments(limit: int = 100, offset: int = 0):
    try:
        live_data_path = os.path.join(DATA_DIR, "live_shipments.csv")
        if not os.path.exists(live_data_path):
            raw_data_path = os.path.join(DATA_DIR, "shipments_raw.csv")
            if os.path.exists(raw_data_path):
                df = pd.read_csv(raw_data_path)
            else:
                return []
        else:
            df = pd.read_csv(live_data_path)

        df = df.iloc[offset:offset + limit]

        df = df.replace({np.nan: None})

        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading shipments: {str(e)}")

@app.get("/api/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    try:
        live_data_path = os.path.join(DATA_DIR, "live_shipments.csv")
        if os.path.exists(live_data_path):
            df = pd.read_csv(live_data_path)
        else:
            raw_data_path = os.path.join(DATA_DIR, "shipments_raw.csv")
            df = pd.read_csv(raw_data_path)

        shipment = df[df['shipment_id'] == shipment_id]
        if shipment.empty:
            raise HTTPException(status_code=404, detail="Shipment not found")

        shipment = shipment.replace({np.nan: None})
        return shipment.to_dict('records')[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading shipment: {str(e)}")

@app.get("/api/alerts")
def get_alerts(min_tier: str = "LOW"):
    try:
        alerts_path = os.path.join(OUTPUT_DIR, "alerts.csv")
        if not os.path.exists(alerts_path):
            return []

        df = pd.read_csv(alerts_path)

        tier_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        min_tier_value = tier_order.get(min_tier.upper(), 0)

        df['tier_value'] = df['risk_tier'].map(tier_order)
        df = df[df['tier_value'] >= min_tier_value]
        df = df.drop('tier_value', axis=1)

        df = df.replace({np.nan: None})

        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading alerts: {str(e)}")

@app.post("/api/recommendations")
def get_recommendations(request: RecommendationRequest):
    try:
        recommendations_path = os.path.join(OUTPUT_DIR, "recommendations.csv")
        if not os.path.exists(recommendations_path):
            return []

        df = pd.read_csv(recommendations_path)

        recs = df[df['shipment_id'] == request.shipment_id]

        if recs.empty:
            return []

        recs = recs.replace({np.nan: None})

        def parse_reasoning(reasoning_str):
            if pd.isna(reasoning_str) or reasoning_str is None:
                return []
            try:
                return json.loads(reasoning_str.replace("'", '"'))
            except:
                return [str(reasoning_str)]

        result = recs.to_dict('records')
        for rec in result:
            if 'reasoning' in rec:
                rec['reasoning'] = parse_reasoning(rec['reasoning'])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading recommendations: {str(e)}")

@app.get("/api/analytics")
def get_analytics():
    try:
        live_data_path = os.path.join(DATA_DIR, "live_shipments.csv")
        alerts_path = os.path.join(OUTPUT_DIR, "alerts.csv")

        shipments_df = None
        if os.path.exists(live_data_path):
            shipments_df = pd.read_csv(live_data_path)
        elif os.path.exists(os.path.join(DATA_DIR, "shipments_raw.csv")):
            shipments_df = pd.read_csv(os.path.join(DATA_DIR, "shipments_raw.csv"))

        alerts_df = None
        if os.path.exists(alerts_path):
            alerts_df = pd.read_csv(alerts_path)

        total_shipments = len(shipments_df) if shipments_df is not None else 0

        if alerts_df is not None and not alerts_df.empty:
            critical_alerts = len(alerts_df[alerts_df['risk_tier'] == 'CRITICAL'])
            high_alerts = len(alerts_df[alerts_df['risk_tier'] == 'HIGH'])
            medium_alerts = len(alerts_df[alerts_df['risk_tier'] == 'MEDIUM'])
            low_alerts = len(alerts_df[alerts_df['risk_tier'] == 'LOW'])
        else:
            critical_alerts = high_alerts = medium_alerts = low_alerts = 0

        if shipments_df is not None and not shipments_df.empty:
            average_risk_score = float(shipments_df['delay_probability'].mean())
            shipments_at_risk = len(shipments_df[shipments_df['delay_probability'] >= 0.5])
        else:
            average_risk_score = 0.0
            shipments_at_risk = 0

        return {
            "total_shipments": total_shipments,
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "medium_alerts": medium_alerts,
            "low_alerts": low_alerts,
            "average_risk_score": average_risk_score,
            "shipments_at_risk": shipments_at_risk,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing analytics: {str(e)}")

@app.post("/api/interventions")
def execute_intervention(request: InterventionRequest):
    try:
        return {
            "success": True,
            "message": f"Intervention '{request.action}' scheduled for {request.shipment_id}",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing intervention: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "data_available": {
            "shipments": os.path.exists(os.path.join(DATA_DIR, "live_shipments.csv")) or
                        os.path.exists(os.path.join(DATA_DIR, "shipments_raw.csv")),
            "alerts": os.path.exists(os.path.join(OUTPUT_DIR, "alerts.csv")),
            "recommendations": os.path.exists(os.path.join(OUTPUT_DIR, "recommendations.csv"))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
