#!/usr/bin/env python3
"""
CRM LEASINPROFESSIONNEL.FR - Version simplifiée pour Replit
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import uvicorn

# Application FastAPI
app = FastAPI(title="CRM LEASINPROFESSIONNEL.FR", version="1.0.0")

# Base de données en mémoire (pour simplifier)
leads_db = {}

# Modèles simplifiés
class Company(BaseModel):
    name: str
    siret: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

class Vehicle(BaseModel):
    brand: str
    model: str
    carburant: str = "diesel"
    tarif_mensuel: Optional[str] = None

class Lead(BaseModel):
    id: Optional[str] = None
    company: Company
    contact: Contact
    vehicle: Vehicle
    status: str = "premier_contact"
    note: Optional[str] = None
    created_at: Optional[datetime] = None

class LeadCreate(BaseModel):
    company: Company
    contact: Contact
    vehicle: Vehicle
    note: Optional[str] = None

# Routes API
@app.get("/")
async def root():
    return {
        "message": "🚗 CRM LEASINPROFESSIONNEL.FR",
        "version": "1.0.0",
        "status": "✅ API en ligne !",
        "endpoints": ["/leads", "/leads/{id}", "/dashboard"]
    }

@app.post("/leads")
async def create_lead(lead_data: LeadCreate):
    lead_id = str(uuid.uuid4())[:8]
    lead = Lead(
        id=lead_id,
        **lead_data.dict(),
        created_at=datetime.now()
    )
    leads_db[lead_id] = lead
    return {"message": "Lead créé avec succès", "lead": lead}

@app.get("/leads")
async def get_leads():
    return {
        "total": len(leads_db),
        "leads": list(leads_db.values())
    }

@app.get("/leads/{lead_id}")
async def get_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    return leads_db[lead_id]

@app.get("/dashboard")
async def dashboard():
    total_leads = len(leads_db)
    statuts = {}
    
    for lead in leads_db.values():
        status = lead.status
        statuts[status] = statuts.get(status, 0) + 1
    
    return {
        "total_leads": total_leads,
        "status_stats": statuts,
        "message": "🎯 Dashboard CRM LEASINPROFESSIONNEL.FR"
    }

# Interface web simple
@app.get("/web", response_class=HTMLResponse)
async def web_interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CRM LEASINPROFESSIONNEL.FR</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f8ff; }
            .header { color: #2563eb; text-align: center; margin-bottom: 30px; }
            .card { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .btn:hover { background: #1d4ed8; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚗 CRM LEASINPROFESSIONNEL.FR</h1>
            <p>Système de gestion des leads LLD automobile</p>
        </div>
        
        <div class="card">
            <h2>🎯 API disponible</h2>
            <p><strong>✅ Backend en ligne !</strong></p>
            <p>API accessible sur : <code>/leads</code></p>
            <button class="btn" onclick="window.open('/docs', '_blank')">📖 Documentation API</button>
        </div>
        
        <div class="card">
            <h2>📊 Fonctionnalités</h2>
            <ul>
                <li>✅ Gestion des leads</li>
                <li>✅ Dashboard statistiques</li>
                <li>✅ API complète</li>
            </ul>
        </div>
    </body>
    </html>
    """

# Démarrage automatique pour Replit
if __name__ == "__main__":
    print("🚀 Démarrage CRM LEASINPROFESSIONNEL.FR...")
    uvicorn.run(app, host="0.0.0.0", port=8000)