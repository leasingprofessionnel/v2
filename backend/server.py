from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, date
import uvicorn
import os
import json
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# Chemin des fichiers de sauvegarde
BACKUP_DIR = "/app/backup"
LEADS_BACKUP_FILE = f"{BACKUP_DIR}/leads_backup.json"
REMINDERS_BACKUP_FILE = f"{BACKUP_DIR}/reminders_backup.json"

# Créer le répertoire de sauvegarde s'il n'existe pas
os.makedirs(BACKUP_DIR, exist_ok=True)

# Application FastAPI
app = FastAPI(
    title="CRM LEASINPROFESSIONNEL.FR",
    version="1.0.0",
    description="Système de gestion des leads LLD automobile"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de données en mémoire
leads_db = {}
reminders_db = {}

# Fonctions de sauvegarde et restauration
def save_leads_to_file():
    """Sauvegarde automatique des leads dans un fichier JSON"""
    try:
        # Convertir les objets Pydantic en dictionnaires pour JSON
        leads_data = {}
        for lead_id, lead in leads_db.items():
            leads_data[lead_id] = lead.dict() if hasattr(lead, 'dict') else lead.__dict__
        
        with open(LEADS_BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(leads_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Sauvegarde automatique : {len(leads_data)} leads sauvegardés")
    except Exception as e:
        print(f"❌ Erreur sauvegarde leads : {str(e)}")

def save_reminders_to_file():
    """Sauvegarde automatique des rappels dans un fichier JSON"""
    try:
        reminders_data = {}
        for reminder_id, reminder in reminders_db.items():
            reminders_data[reminder_id] = reminder.dict() if hasattr(reminder, 'dict') else reminder.__dict__
        
        with open(REMINDERS_BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(reminders_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Sauvegarde automatique : {len(reminders_data)} rappels sauvegardés")
    except Exception as e:
        print(f"❌ Erreur sauvegarde rappels : {str(e)}")

def load_leads_from_file():
    """Restauration automatique des leads depuis le fichier JSON"""
    global leads_db
    try:
        if os.path.exists(LEADS_BACKUP_FILE):
            with open(LEADS_BACKUP_FILE, 'r', encoding='utf-8') as f:
                leads_data = json.load(f)
            
            # Convertir les dictionnaires JSON en objets Lead
            for lead_id, lead_dict in leads_data.items():
                # Reconstruire les objets Lead avec tous les champs
                lead = Lead(
                    id=lead_dict.get('id'),
                    company=Company(**lead_dict['company']),
                    contact=Contact(**lead_dict['contact']),
                    vehicles=[Vehicle(**v) for v in lead_dict.get('vehicles', [])],
                    status=lead_dict.get('status', 'premier_contact'),
                    note=lead_dict.get('note'),
                    delivery_date=lead_dict.get('delivery_date'),
                    assigned_to_commercial=lead_dict.get('assigned_to_commercial'),
                    assigned_to_prestataire=lead_dict.get('assigned_to_prestataire'),
                    reminders=[Reminder(**r) for r in lead_dict.get('reminders', [])],
                    created_at=lead_dict.get('created_at')
                )
                leads_db[lead_id] = lead
            
            print(f"🔄 Restauration automatique : {len(leads_data)} leads chargés depuis la sauvegarde")
        else:
            print("📂 Aucun fichier de sauvegarde leads trouvé")
    except Exception as e:
        print(f"❌ Erreur restauration leads : {str(e)}")

def load_reminders_from_file():
    """Restauration automatique des rappels depuis le fichier JSON"""
    global reminders_db
    try:
        if os.path.exists(REMINDERS_BACKUP_FILE):
            with open(REMINDERS_BACKUP_FILE, 'r', encoding='utf-8') as f:
                reminders_data = json.load(f)
            
            # Convertir les dictionnaires JSON en objets Reminder
            for reminder_id, reminder_dict in reminders_data.items():
                reminder = Reminder(**reminder_dict)
                reminders_db[reminder_id] = reminder
            
            print(f"🔄 Restauration automatique : {len(reminders_data)} rappels chargés depuis la sauvegarde")
        else:
            print("📂 Aucun fichier de sauvegarde rappels trouvé")
    except Exception as e:
        print(f"❌ Erreur restauration rappels : {str(e)}")

# Charger les données au démarrage
load_leads_from_file()
load_reminders_from_file()

# Modèles
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
    contract_duration: int = 36
    annual_mileage: int = 15000
    tarif_mensuel: Optional[str] = None
    commission_agence: Optional[str] = None
    payment_status: str = "en_attente"

class Reminder(BaseModel):
    id: Optional[str] = None
    lead_id: str
    title: str
    description: Optional[str] = None
    reminder_date: str
    completed: bool = False
    created_at: Optional[str] = None

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
    reminders: List[Reminder] = []
    created_at: Optional[str] = None

class LeadCreate(BaseModel):
    company: Company
    contact: Contact
    vehicles: List[Vehicle] = []
    note: Optional[str] = None
    assigned_to_commercial: Optional[str] = None
    assigned_to_prestataire: Optional[str] = None

class ReminderCreate(BaseModel):
    lead_id: str
    title: str
    description: Optional[str] = None
    reminder_date: str

# Configuration complète
CAR_BRANDS = {
    "Abarth": ["500", "595", "695"],
    "AC": ["Cobra", "Ace"],
    "Acura": ["MDX", "RDX", "TLX", "NSX"],
    "Aixam": ["City", "Crossline", "Coupe"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "Giulietta", "159", "147", "156", "MiTo", "4C", "Spider", "Brera", "GT"],
    "Alpine": ["A110", "A310"],
    "Aston Martin": ["DB11", "DBS", "Vantage", "DBX", "DB9", "V8", "Rapide"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q4 e-tron", "Q5", "Q7", "Q8", "e-tron", "TT", "R8", "RS3", "RS4", "RS5", "RS6", "RS7", "S3", "S4", "S5", "S6", "S8", "SQ5", "SQ7"],
    "Austin": ["Mini Cooper", "Healey"],
    "Bentley": ["Bentayga", "Continental", "Flying Spur", "Mulsanne"],
    "BMW": ["Série 1", "Série 2", "Série 3", "Série 4", "Série 5", "Série 6", "Série 7", "Série 8", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i4", "iX", "iX3", "M2", "M3", "M4", "M5", "M8", "X3 M", "X4 M", "X5 M", "X6 M"],
    "Bugatti": ["Chiron", "Veyron"],
    "Cadillac": ["Escalade", "XT4", "XT5", "XT6", "CT4", "CT5"],
    "Caterham": ["Seven", "620R"],
    "Chevrolet": ["Camaro", "Corvette", "Silverado", "Tahoe", "Suburban", "Cruze", "Aveo", "Captiva", "Spark", "Trax"],
    "Chrysler": ["300C", "Pacifica", "Voyager", "Grand Voyager"],
    "Citroën": ["C1", "C3", "C4", "C5", "C5 X", "C5 Aircross", "C3 Aircross", "Berlingo", "Jumpy", "Jumper", "SpaceTourer", "Ami", "C8", "C6", "C4 Picasso", "C4 Spacetourer", "Nemo", "C15"],
    "Cupra": ["Formentor", "Leon", "Ateca", "Born"],
    "Dacia": ["Sandero", "Logan", "Duster", "Lodgy", "Dokker", "Spring", "Jogger"],
    "Daewoo": ["Matiz", "Kalos", "Lacetti", "Nubira"],
    "Daihatsu": ["Terios", "Sirion", "Cuore", "Copen"],
    "Dodge": ["Challenger", "Charger", "Durango", "Ram", "Journey", "Nitro"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9"],
    "Ferrari": ["488", "F8", "SF90", "Roma", "Portofino", "812", "LaFerrari", "California", "458", "F12", "FF", "GTC4", "296"],
    "Fiat": ["500", "500X", "500L", "500C", "Panda", "Punto", "Tipo", "Ducato", "Doblo", "Fiorino", "Qubo", "Bravo", "Croma", "Marea", "Stilo", "Ulysse"],
    "Ford": ["Fiesta", "Focus", "Mondeo", "Mustang", "Kuga", "EcoSport", "Puma", "Explorer", "Edge", "Transit", "Ranger", "Ka+", "Galaxy", "S-Max", "C-Max", "B-Max", "Tourneo", "Escort", "Sierra"],
    "Genesis": ["G70", "G80", "G90", "GV60", "GV70", "GV80"],
    "Honda": ["Civic", "Accord", "Jazz", "HR-V", "CR-V", "Pilot", "Ridgeline", "e", "Insight", "S2000", "NSX", "Legend", "Prelude"],
    "Hummer": ["H2", "H3"],
    "Hyundai": ["i10", "i20", "i30", "i40", "Tucson", "Santa Fe", "Kona", "Ioniq", "Ioniq 5", "Nexo", "ix35", "ix55", "Veloster", "Genesis", "Coupe"],
    "Infiniti": ["Q30", "Q50", "Q60", "Q70", "QX30", "QX50", "QX60", "QX70"],
    "Isuzu": ["D-Max", "MU-X", "Trooper"],
    "Iveco": ["Daily", "Massif"],
    "Jaguar": ["XE", "XF", "XJ", "F-Type", "F-Pace", "E-Pace", "I-Pace", "XK", "S-Type", "X-Type"],
    "Jeep": ["Compass", "Grand Cherokee", "Cherokee", "Wrangler", "Renegade", "Gladiator", "Avenger", "Commander", "Patriot"],
    "Kia": ["Picanto", "Rio", "Ceed", "Stonic", "XCeed", "Sportage", "Sorento", "Niro", "EV6", "Soul", "Venga", "Carens", "Carnival", "Optima", "Stinger"],
    "Lada": ["Niva", "Vesta", "Granta", "Largus", "Kalina"],
    "Lamborghini": ["Huracán", "Aventador", "Urus", "Gallardo", "Murcielago"],
    "Lancia": ["Ypsilon", "Delta", "Musa", "Phedra", "Thesis"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Sport", "Range Rover Evoque", "Range Rover Velar", "Freelander"],
    "Lexus": ["IS", "ES", "LS", "CT", "NX", "RX", "GX", "LX", "LC", "UX", "GS"],
    "Lincoln": ["Continental", "Navigator", "Aviator", "Corsair"],
    "Lotus": ["Elise", "Exige", "Evora", "Emira", "Esprit"],
    "Maserati": ["Ghibli", "Quattroporte", "Levante", "MC20", "GranTurismo", "GranCabrio"],
    "Maybach": ["S-Class", "GLS"],
    "Mazda": ["2", "3", "6", "CX-3", "CX-5", "CX-30", "CX-60", "MX-5", "MX-30", "RX-8", "CX-7", "CX-9", "5"],
    "McLaren": ["570S", "720S", "765LT", "Artura", "540C", "650S", "P1"],
    "Mercedes": ["Classe A", "Classe B", "Classe C", "Classe E", "Classe S", "CLA", "CLS", "GLA", "GLB", "GLC", "GLE", "GLS", "G", "SL", "SLC", "AMG GT", "EQA", "EQB", "EQC", "EQS", "EQV", "Vito", "Sprinter", "Citan", "Classe R", "ML", "GLK", "SLK", "CLK", "SLR"],
    "MG": ["ZS", "MG5", "Marvel R", "HS", "MG6", "TF", "ZR", "ZT"],
    "Mini": ["Cooper", "Countryman", "Clubman", "Paceman", "Roadster", "Cabrio"],
    "Mitsubishi": ["Space Star", "ASX", "Eclipse Cross", "Outlander", "L200", "Pajero", "Lancer", "Colt", "Carisma"],
    "Morgan": ["4/4", "Plus 4", "Roadster", "3 Wheeler"],
    "Nissan": ["Micra", "Note", "Sentra", "Altima", "Maxima", "Juke", "Qashqai", "X-Trail", "Murano", "Pathfinder", "Titan", "Leaf", "Ariya", "NV200", "Primastar", "350Z", "370Z", "GT-R", "Primera", "Almera", "Terrano"],
    "Opel": ["Corsa", "Astra", "Insignia", "Crossland", "Grandland", "Mokka", "Zafira", "Vivaro", "Movano", "Combo", "Meriva", "Antara", "Vectra", "Omega", "Tigra", "Agila"],
    "Peugeot": ["108", "208", "308", "408", "508", "2008", "3008", "5008", "Partner", "Expert", "Boxer", "Rifter", "Traveller", "e-208", "e-2008", "206", "207", "307", "407", "607", "807", "1007", "4007", "4008", "RCZ"],
    "Pontiac": ["Firebird", "Trans Am", "GTO"],
    "Porsche": ["911", "Boxster", "Cayman", "Panamera", "Macan", "Cayenne", "Taycan", "928", "944", "968"],
    "Ram": ["1500", "2500", "3500", "ProMaster"],
    "Renault": ["Twingo", "Clio", "Mégane", "Talisman", "Captur", "Kadjar", "Koleos", "Arkana", "Austral", "Espace", "Scénic", "Kangoo", "Trafic", "Master", "ZOE", "Twizy", "Laguna", "Vel Satis", "Avantime", "Wind", "Fluence", "Latitude"],
    "Rolls-Royce": ["Ghost", "Phantom", "Wraith", "Dawn", "Cullinan"],
    "Rover": ["25", "45", "75", "Mini", "Streetwise"],
    "Saab": ["9-3", "9-5", "900", "9000"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona", "Tarraco", "Alhambra", "Toledo", "Cordoba", "Altea", "Exeo"],
    "Skoda": ["Fabia", "Scala", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq", "Roomster", "Yeti", "Citigo", "Rapid"],
    "Smart": ["ForTwo", "ForFour", "Roadster", "Crossblade"],
    "SsangYong": ["Tivoli", "Korando", "Rexton", "Kyron", "Actyon", "Rodius"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "XV", "BRZ", "WRX", "Tribeca"],
    "Suzuki": ["Swift", "Baleno", "SX4", "Vitara", "S-Cross", "Jimny", "Ignis", "Alto", "Splash", "Kizashi", "Grand Vitara"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Roadster", "Cybertruck"],
    "Toyota": ["Aygo", "Yaris", "Corolla", "Camry", "Avalon", "C-HR", "RAV4", "Highlander", "4Runner", "Sequoia", "Land Cruiser", "Prius", "Mirai", "Hilux", "Proace", "Supra", "Avensis", "Verso", "Auris", "iQ", "Urban Cruiser"],
    "Volkswagen": ["up!", "Polo", "Golf", "Jetta", "Passat", "Arteon", "T-Cross", "T-Roc", "Tiguan", "Touareg", "Sharan", "Touran", "Caddy", "Transporter", "Crafter", "ID.3", "ID.4", "ID.Buzz", "Beetle", "Eos", "CC", "Phaeton", "Lupo", "Fox"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "S90", "V60", "V90", "C40", "EX30", "S40", "S80", "V40", "V50", "V70", "XC70", "C30", "C70"],
    "Wartburg": ["353", "Tourist"],
    "Wiesmann": ["GT", "Roadster"]
}

COMMERCIAUX = ["Matthews", "Sauveur", "Autre"]
PRESTATAIRES = ["Localease", "Leasefactory", "Ayvens", "ALD Automotive", "Arval", "Alphabet", "Leaseplan", "BNP Paribas Leasing", "Crédit Agricole Leasing", "Société Générale Equipment Finance", "Autre"]

# Configuration des durées de contrat et kilométrages
CONTRACT_DURATIONS = [12, 24, 36, 48, 60]
ANNUAL_MILEAGES = [10000, 15000, 20000, 25000, 30000, 35000, 40000, 50000]

# Génération PDF
def generate_lead_pdf(lead: Lead) -> str:
    import tempfile
    import os
    
    # Créer un nom de fichier temporaire avec extension .pdf garantie
    temp_dir = tempfile.gettempdir()
    filename = f"lead_{lead.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    temp_path = os.path.join(temp_dir, filename)
    
    doc = SimpleDocTemplate(temp_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2563eb')
    )
    
    story.append(Paragraph("CRM LEASINPROFESSIONNEL.FR - Fiche Lead", title_style))
    story.append(Spacer(1, 20))
    
    # Informations lead
    lead_info = f"""
    <para align="center">
    <b>Lead ID:</b> {lead.id}<br/>
    <b>Créé le:</b> {lead.created_at}<br/>
    <b>Statut:</b> <b>{lead.status.replace('_', ' ').title()}</b>
    </para>
    """
    story.append(Paragraph(lead_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Société
    company_data = [
        ['Société', lead.company.name],
        ['SIRET', lead.company.siret or 'Non renseigné'],
        ['Email', lead.company.email or 'Non renseigné'],
        ['Téléphone', lead.company.phone or 'Non renseigné']
    ]
    
    company_table = Table(company_data, colWidths=[2.5*inch, 4*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eff6ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
    ]))
    story.append(company_table)
    story.append(Spacer(1, 15))
    
    # Contact
    contact_data = [
        ['Contact', f"{lead.contact.first_name} {lead.contact.last_name}"],
        ['Email', lead.contact.email],
        ['Téléphone', lead.contact.phone or 'Non renseigné']
    ]
    
    contact_table = Table(contact_data, colWidths=[2.5*inch, 4*inch])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 15))
    
    # Véhicules
    if lead.vehicles:
        for i, vehicle in enumerate(lead.vehicles):
            vehicle_data = [
                ['Véhicule', f"{vehicle.brand} {vehicle.model}"],
                ['Carburant', vehicle.carburant],
                ['Tarif mensuel', vehicle.tarif_mensuel or 'Non renseigné'],
                ['Commission', vehicle.commission_agence or 'Non renseigné'],
                ['Statut paiement', 'Payé' if vehicle.payment_status == 'paye' else 'En attente']
            ]
            
            vehicle_table = Table(vehicle_data, colWidths=[2.5*inch, 4*inch])
            vehicle_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
            ]))
            story.append(vehicle_table)
            story.append(Spacer(1, 10))
    
    # Note
    if lead.note:
        story.append(Paragraph(f"<b>Notes:</b> {lead.note}", styles['Normal']))
    
    doc.build(story)
    return temp_path

# Routes API
@app.get("/")
async def root():
    return {
        "message": "🚗 CRM LEASINPROFESSIONNEL.FR",
        "version": "1.0.0",
        "status": "✅ API en ligne !",
        "total_leads": len(leads_db)
    }

@app.get("/api/config")
async def get_config():
    return {
        "car_brands": CAR_BRANDS,
        "commerciaux": COMMERCIAUX,
        "prestataires": PRESTATAIRES,
        "contract_durations": CONTRACT_DURATIONS,
        "annual_mileages": ANNUAL_MILEAGES,
        "status_colors": {
            "premier_contact": "#94a3b8",
            "relance": "#f59e0b",
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
    
    leads_db[lead_id] = lead
    
    # 💾 SAUVEGARDE AUTOMATIQUE
    save_leads_to_file()
    
    return {"message": "Lead créé avec succès", "lead": lead}

@app.get("/api/leads")
async def get_leads():
    return list(leads_db.values())

@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    return leads_db[lead_id]

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, update_data: dict):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    
    lead = leads_db[lead_id]
    for key, value in update_data.items():
        if hasattr(lead, key):
            setattr(lead, key, value)
    
    # 💾 SAUVEGARDE AUTOMATIQUE
    save_leads_to_file()
    
    return {"message": "Lead mis à jour", "lead": lead}

@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    
    del leads_db[lead_id]
    return {"message": "Lead supprimé"}

@app.get("/api/leads/{lead_id}/pdf")
async def download_lead_pdf(lead_id: str):
    if lead_id not in leads_db:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    
    lead = leads_db[lead_id]
    pdf_path = generate_lead_pdf(lead)
    
    # S'assurer que le nom de fichier a l'extension .pdf
    safe_company_name = lead.company.name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    filename = f"Lead_{safe_company_name}_{lead_id}.pdf"
    
    return FileResponse(
        path=pdf_path,
        filename=filename,
        media_type='application/pdf',
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }
    )

@app.get("/api/reminders")
async def get_reminders():
    return list(reminders_db.values())

@app.get("/api/calendar/reminders")
async def get_calendar_reminders(days: int = 30):
    """Get upcoming reminders for the next N days"""
    from datetime import datetime, timedelta
    
    now = datetime.now()
    future_date = now + timedelta(days=days)
    
    upcoming = []
    for reminder in reminders_db.values():
        try:
            reminder_date = datetime.fromisoformat(reminder.reminder_date.replace('Z', '+00:00'))
            if now <= reminder_date <= future_date and not reminder.completed:
                upcoming.append(reminder)
        except:
            pass  # Skip invalid dates
    
    # Sort by date
    upcoming.sort(key=lambda x: x.reminder_date)
    return upcoming

@app.post("/api/reminders")
async def create_reminder(reminder_data: ReminderCreate):
    reminder_id = str(uuid.uuid4())[:8]
    
    reminder = Reminder(
        id=reminder_id,
        lead_id=reminder_data.lead_id,
        title=reminder_data.title,
        description=reminder_data.description,
        reminder_date=reminder_data.reminder_date,
        created_at=datetime.now().isoformat()
    )
    
    reminders_db[reminder_id] = reminder
    
    # Ajouter au lead
    if reminder_data.lead_id in leads_db:
        leads_db[reminder_data.lead_id].reminders.append(reminder)
    
    return {"message": "Rappel créé avec succès", "reminder": reminder}

@app.get("/api/dashboard/stats")
async def get_stats():
    total_leads = len(leads_db)
    status_stats = {}
    commissions_paid = 0.0
    commissions_pending = 0.0
    
    for lead in leads_db.values():
        status = lead.status
        status_stats[status] = status_stats.get(status, 0) + 1
        
        for vehicle in lead.vehicles:
            commission = vehicle.commission_agence or ""
            if commission:
                try:
                    import re
                    numbers = re.findall(r'\d+', commission)
                    if numbers:
                        amount = float(numbers[0])
                        if vehicle.payment_status == "paye":
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
            "total_paid": round(commissions_paid, 2),
            "total_pending": round(commissions_pending, 2),
            "total_expected": round(commissions_paid + commissions_pending, 2)
        }
    }

if __name__ == "__main__":
    print("🚀 Démarrage CRM LEASINPROFESSIONNEL.FR...")
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)