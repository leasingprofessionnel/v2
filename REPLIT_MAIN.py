#!/usr/bin/env python3
"""
CRM LEASINPROFESSIONNEL.FR - Version complète pour Replit
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, date
import uvicorn
import os
import json

# Application FastAPI
app = FastAPI(
    title="CRM LEASINPROFESSIONNEL.FR",
    version="1.0.0",
    description="Système de gestion des leads LLD automobile"
)

# CORS pour permettre les requêtes frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de données en mémoire (fichier JSON pour persistance)
LEADS_FILE = "leads.json"
leads_db = {}

# Charger les données existantes
def load_leads():
    global leads_db
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                leads_db = data
    except Exception as e:
        print(f"Erreur chargement leads: {e}")
        leads_db = {}

# Sauvegarder les données
def save_leads():
    try:
        with open(LEADS_FILE, 'w', encoding='utf-8') as f:
            # Convertir les dates en strings pour JSON
            data_to_save = {}
            for lead_id, lead in leads_db.items():
                lead_copy = dict(lead)
                if isinstance(lead_copy.get('created_at'), datetime):
                    lead_copy['created_at'] = lead_copy['created_at'].isoformat()
                if isinstance(lead_copy.get('delivery_date'), date):
                    lead_copy['delivery_date'] = lead_copy['delivery_date'].isoformat()
                data_to_save[lead_id] = lead_copy
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")

# Modèles Pydantic
class Company(BaseModel):
    name: str
    siret: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    position: Optional[str] = None

class Vehicle(BaseModel):
    brand: str
    model: str
    carburant: str = "diesel"
    contract_duration: int = 36
    annual_mileage: int = 15000
    tarif_mensuel: Optional[str] = None
    commission_agence: Optional[str] = None
    payment_status: str = "en_attente"

class Lead(BaseModel):
    id: Optional[str] = None
    company: Company
    contact: Contact
    vehicles: List[Vehicle] = []
    status: str = "premier_contact"
    note: Optional[str] = None
    delivery_date: Optional[str] = None
    assigned_to_commercial: Optional[str] = None
    assigned_to_prestataire: Optional[str] = None
    created_at: Optional[str] = None

class LeadCreate(BaseModel):
    company: Company
    contact: Contact
    vehicles: List[Vehicle] = []
    note: Optional[str] = None
    assigned_to_commercial: Optional[str] = None
    assigned_to_prestataire: Optional[str] = None

# Configuration du CRM
CAR_BRANDS = {
    "Peugeot": ["208", "308", "3008", "5008", "508", "2008"],
    "Renault": ["Clio", "Megane", "Captur", "Kadjar", "Koleos"],
    "Citroën": ["C3", "C4", "C5 Aircross", "Berlingo"],
    "BMW": ["Série 1", "Série 3", "X1", "X3", "X5"],
    "Mercedes": ["Classe A", "Classe C", "GLA", "GLC"],
    "Audi": ["A3", "A4", "Q3", "Q5"],
    "Volkswagen": ["Golf", "Polo", "Tiguan", "Passat"],
    "Toyota": ["Yaris", "Corolla", "RAV4", "Prius"],
    "Ford": ["Fiesta", "Focus", "Kuga"]
}

COMMERCIAUX = ["Matthews", "Sauveur", "Autre"]
PRESTATAIRES = ["Localease", "Leasefactory", "Ayvens", "ALD Automotive"]

# Routes API
@app.get("/")
async def root():
    return {
        "message": "🚗 CRM LEASINPROFESSIONNEL.FR",
        "version": "1.0.0",
        "status": "✅ API en ligne !",
        "total_leads": len(leads_db),
        "endpoints": ["/web", "/api/leads", "/api/dashboard", "/docs"]
    }

@app.get("/api/config")
async def get_config():
    return {
        "car_brands": CAR_BRANDS,
        "commerciaux": COMMERCIAUX,
        "prestataires": PRESTATAIRES,
        "status_colors": {
            "premier_contact": "#94a3b8",
            "relance": "#f59e0b",
            "attribue": "#06b6d4",
            "offre": "#8b5cf6",
            "accord": "#10b981",
            "livree": "#22c55e",
            "perdu": "#ef4444"
        }
    }

@app.post("/api/leads")
async def create_lead(lead_data: LeadCreate):
    lead_id = str(uuid.uuid4())[:8]
    
    lead = Lead(
        id=lead_id,
        company=lead_data.company,
        contact=lead_data.contact,
        vehicles=lead_data.vehicles,
        note=lead_data.note,
        assigned_to_commercial=lead_data.assigned_to_commercial,
        assigned_to_prestataire=lead_data.assigned_to_prestataire,
        created_at=datetime.now().isoformat()
    )
    
    leads_db[lead_id] = lead.dict()
    save_leads()
    
    return {"message": "Lead créé avec succès", "lead": lead}

@app.get("/api/leads")
async def get_leads():
    return {
        "total": len(leads_db),
        "leads": list(leads_db.values())
    }

@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    return leads_db[lead_id]

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, update_data: dict):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    
    # Mise à jour des champs
    for key, value in update_data.items():
        if key in leads_db[lead_id]:
            leads_db[lead_id][key] = value
    
    save_leads()
    return {"message": "Lead mis à jour", "lead": leads_db[lead_id]}

@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    
    del leads_db[lead_id]
    save_leads()
    return {"message": "Lead supprimé avec succès"}

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    total_leads = len(leads_db)
    status_stats = {}
    commissions_paid = 0.0
    commissions_pending = 0.0
    
    for lead in leads_db.values():
        # Compter les statuts
        status = lead.get("status", "premier_contact")
        status_stats[status] = status_stats.get(status, 0) + 1
        
        # Calculer les commissions
        for vehicle in lead.get("vehicles", []):
            commission = vehicle.get("commission_agence", "")
            if commission:
                try:
                    # Extraire le montant (ex: "120€" -> 120)
                    import re
                    numbers = re.findall(r'\d+', commission)
                    if numbers:
                        amount = float(numbers[0])
                        if vehicle.get("payment_status") == "paye":
                            commissions_paid += amount
                        else:
                            commissions_pending += amount
                except:
                    pass
    
    return {
        "total_leads": total_leads,
        "status_stats": status_stats,
        "commissions_stats": {
            "year": 2025,
            "total_paid": commissions_paid,
            "total_pending": commissions_pending,
            "total_expected": commissions_paid + commissions_pending
        }
    }

# Interface web intégrée
@app.get("/web", response_class=HTMLResponse)
async def web_interface():
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRM LEASINPROFESSIONNEL.FR</title>
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .card {{ background: white; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            .header {{ background: linear-gradient(90deg, #2563eb, #ffffff, #dc2626); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }}
            .btn {{ background: #2563eb; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; margin: 5px; transition: all 0.3s; }}
            .btn:hover {{ background: #1d4ed8; transform: translateY(-2px); }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-card {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
            .leads-list {{ max-height: 400px; overflow-y: auto; }}
            .lead-item {{ background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #2563eb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 class="header">🚗 CRM LEASINPROFESSIONNEL.FR</h1>
                <p style="text-align: center; color: #64748b; font-size: 1.2em;">Système de gestion des leads LLD automobile</p>
                
                <div class="stats">
                    <div class="stat-card">
                        <h3>📊 Total Leads</h3>
                        <p style="font-size: 2em; margin: 10px 0;">{len(leads_db)}</p>
                    </div>
                    <div class="stat-card">
                        <h3>✅ API Active</h3>
                        <p style="font-size: 1.5em;">En ligne</p>
                    </div>
                    <div class="stat-card">
                        <h3>🚀 Statut</h3>
                        <p style="font-size: 1.5em;">Opérationnel</p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <button class="btn" onclick="window.open('/docs', '_blank')">📖 Documentation API</button>
                    <button class="btn" onclick="loadLeads()">🔄 Actualiser les leads</button>
                    <button class="btn" onclick="showCreateForm()">➕ Nouveau Lead</button>
                </div>
                
                <div id="leads-container" class="leads-list">
                    <p style="text-align: center; color: #64748b;">Cliquez sur "Actualiser les leads" pour voir la liste</p>
                </div>
                
                <!-- Formulaire de création -->
                <div id="create-form" style="display: none; margin-top: 30px;">
                    <h3>➕ Nouveau Lead</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                        <div>
                            <label>Société *</label>
                            <input id="company-name" type="text" placeholder="Nom société" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                            <input id="company-siret" type="text" placeholder="SIRET" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                        </div>
                        <div>
                            <label>Contact *</label>
                            <input id="contact-name" type="text" placeholder="Prénom Nom" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                            <input id="contact-email" type="email" placeholder="Email" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                        </div>
                    </div>
                    <div>
                        <label>Véhicule</label>
                        <select id="vehicle-brand" style="width: 48%; padding: 10px; margin: 5px 1%; border: 1px solid #ddd; border-radius: 5px;">
                            <option>Peugeot</option>
                            <option>Renault</option>
                            <option>BMW</option>
                            <option>Mercedes</option>
                        </select>
                        <select id="vehicle-model" style="width: 48%; padding: 10px; margin: 5px 1%; border: 1px solid #ddd; border-radius: 5px;">
                            <option>208</option>
                            <option>308</option>
                            <option>3008</option>
                        </select>
                    </div>
                    <textarea id="note" placeholder="Notes..." style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; height: 80px;"></textarea>
                    
                    <div style="text-align: center;">
                        <button class="btn" onclick="createLead()">✅ Créer le Lead</button>
                        <button class="btn" onclick="hideCreateForm()" style="background: #6b7280;">❌ Annuler</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function loadLeads() {{
                try {{
                    const response = await fetch('/api/leads');
                    const data = await response.json();
                    
                    const container = document.getElementById('leads-container');
                    if (data.leads.length === 0) {{
                        container.innerHTML = '<p style="text-align: center; color: #64748b;">Aucun lead trouvé</p>';
                        return;
                    }}
                    
                    container.innerHTML = data.leads.map(lead => `
                        <div class="lead-item">
                            <div style="display: flex; justify-content: between; align-items: center;">
                                <div>
                                    <h4 style="margin: 0; color: #1e293b;">🏢 ${{lead.company.name}}</h4>
                                    <p style="margin: 5px 0; color: #64748b;">👤 ${{lead.contact.first_name}} ${{lead.contact.last_name || ''}}</p>
                                    <p style="margin: 5px 0; color: #64748b;">📧 ${{lead.contact.email}}</p>
                                    ${{lead.vehicles.length > 0 ? `<p style="margin: 5px 0; color: #64748b;">🚗 ${{lead.vehicles[0].brand}} ${{lead.vehicles[0].model}}</p>` : ''}}
                                </div>
                                <div>
                                    <span style="background: #22c55e; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em;">
                                        ${{lead.status.replace('_', ' ').toUpperCase()}}
                                    </span>
                                </div>
                            </div>
                        </div>
                    `).join('');
                }} catch (error) {{
                    console.error('Erreur:', error);
                    document.getElementById('leads-container').innerHTML = '<p style="color: red;">Erreur lors du chargement</p>';
                }}
            }}
            
            function showCreateForm() {{
                document.getElementById('create-form').style.display = 'block';
            }}
            
            function hideCreateForm() {{
                document.getElementById('create-form').style.display = 'none';
            }}
            
            async function createLead() {{
                const leadData = {{
                    company: {{
                        name: document.getElementById('company-name').value,
                        siret: document.getElementById('company-siret').value
                    }},
                    contact: {{
                        first_name: document.getElementById('contact-name').value.split(' ')[0] || '',
                        last_name: document.getElementById('contact-name').value.split(' ').slice(1).join(' ') || '',
                        email: document.getElementById('contact-email').value
                    }},
                    vehicles: [{{
                        brand: document.getElementById('vehicle-brand').value,
                        model: document.getElementById('vehicle-model').value,
                        carburant: 'diesel'
                    }}],
                    note: document.getElementById('note').value
                }};
                
                try {{
                    const response = await fetch('/api/leads', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(leadData)
                    }});
                    
                    if (response.ok) {{
                        alert('✅ Lead créé avec succès !');
                        hideCreateForm();
                        loadLeads();
                        // Reset form
                        document.getElementById('company-name').value = '';
                        document.getElementById('company-siret').value = '';
                        document.getElementById('contact-name').value = '';
                        document.getElementById('contact-email').value = '';
                        document.getElementById('note').value = '';
                    }}
                }} catch (error) {{
                    alert('❌ Erreur lors de la création');
                }}
            }}
        </script>
    </body>
    </html>
    """

# Charger les leads au démarrage
load_leads()

# Démarrage de l'application
if __name__ == "__main__":
    print("🚀 Démarrage CRM LEASINPROFESSIONNEL.FR...")
    print("📊 Interface web : /web")
    print("🔧 API docs : /docs")
    
    # Port pour Replit
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)