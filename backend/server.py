from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, date
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="CRM LLD Automobile", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class LeadStatus(str, Enum):
    PREMIER_CONTACT = "premier_contact"
    RELANCE = "relance" 
    ATTRIBUE = "attribue"
    OFFRE = "offre"
    ATTENTE_DOCUMENT = "attente_document"
    ETUDE_EN_COURS = "etude_en_cours"
    ACCORD = "accord"
    LIVREE = "livree"
    PERDU = "perdu"

class CarburantType(str, Enum):
    DIESEL = "diesel"
    ESSENCE = "essence"
    HYBRIDE = "hybride"
    ELECTRIQUE = "electrique"

# Models
class Company(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    siret: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Vehicle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    brand: str
    model: str
    carburant: CarburantType
    contract_duration: int  # en mois
    annual_mileage: int  # km/an
    tarif_mensuel: Optional[str] = None  # Nouveau champ
    commission_agence: Optional[str] = None  # Nouveau champ
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Activity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    lead_id: str
    activity_type: str  # note, task, call, email
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None

class Reminder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    lead_id: str
    title: str
    description: Optional[str] = None
    reminder_date: datetime
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None

class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: Company
    contact: Contact
    vehicles: List[Vehicle] = []  # Support multiple vehicles
    note: Optional[str] = None  # Champ note multiligne
    status: LeadStatus = LeadStatus.PREMIER_CONTACT
    assigned_to_prestataire: Optional[str] = None
    assigned_to_commercial: Optional[str] = None
    activities: List[Activity] = []
    reminders: List[Reminder] = []  # Nouveau champ pour les rappels
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Create models
class CompanyCreate(BaseModel):
    name: str
    siret: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[str] = None

class VehicleCreate(BaseModel):
    brand: str
    model: str
    carburant: CarburantType
    contract_duration: int
    annual_mileage: int
    tarif_mensuel: Optional[str] = None
    commission_agence: Optional[str] = None

class ReminderCreate(BaseModel):
    lead_id: str
    title: str
    description: Optional[str] = None
    reminder_date: datetime

class ActivityCreate(BaseModel):
    lead_id: str
    activity_type: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class LeadCreate(BaseModel):
    company: CompanyCreate
    contact: ContactCreate
    vehicles: List[VehicleCreate] = []  # Support multiple vehicles
    note: Optional[str] = None  # Champ note
    assigned_to_prestataire: Optional[str] = None
    assigned_to_commercial: Optional[str] = None

class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    assigned_to_prestataire: Optional[str] = None
    assigned_to_commercial: Optional[str] = None
    company: Optional[CompanyCreate] = None
    contact: Optional[ContactCreate] = None
    vehicles: Optional[List[VehicleCreate]] = None  # Support multiple vehicles
    note: Optional[str] = None  # Champ note

# Status colors mapping
STATUS_COLORS = {
    LeadStatus.PREMIER_CONTACT: "#94a3b8",  # slate-400
    LeadStatus.RELANCE: "#f59e0b",          # amber-500
    LeadStatus.ATTRIBUE: "#06b6d4",         # cyan-500
    LeadStatus.OFFRE: "#8b5cf6",            # violet-500
    LeadStatus.ATTENTE_DOCUMENT: "#f97316", # orange-500
    LeadStatus.ETUDE_EN_COURS: "#3b82f6",   # blue-500
    LeadStatus.ACCORD: "#10b981",           # emerald-500
    LeadStatus.LIVREE: "#22c55e",           # green-500
    LeadStatus.PERDU: "#ef4444"             # red-500
}

# Predefined lists
PRESTATAIRES = [
    "Localease", "Leasefactory", "Ayvens", "Leaseplan", "ALD Automotive", 
    "Alphabet", "Arval", "Autre"
]

COMMERCIAUX = [
    "Matthews", "Sauveur", "Autre"
]

CAR_BRANDS = {
    "Abarth": ["500", "595", "695"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "Giulietta", "159", "147", "156", "MiTo"],
    "Aston Martin": ["DB11", "DBS", "Vantage", "DBX"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q4 e-tron", "Q5", "Q7", "Q8", "e-tron", "TT", "R8", "RS3", "RS4", "RS5", "RS6", "RS7"],
    "Bentley": ["Bentayga", "Continental", "Flying Spur", "Mulsanne"],
    "BMW": ["Série 1", "Série 2", "Série 3", "Série 4", "Série 5", "Série 6", "Série 7", "Série 8", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i4", "iX", "iX3"],
    "Cadillac": ["Escalade", "XT4", "XT5", "XT6", "CT4", "CT5"],
    "Chevrolet": ["Camaro", "Corvette", "Silverado", "Tahoe", "Suburban", "Cruze", "Aveo", "Captiva"],
    "Chrysler": ["300C", "Pacifica", "Voyager"],
    "Citroën": ["C1", "C3", "C4", "C5", "C5 X", "C5 Aircross", "C3 Aircross", "Berlingo", "Jumpy", "Jumper", "SpaceTourer", "Ami"],
    "Dacia": ["Sandero", "Logan", "Duster", "Lodgy", "Dokker", "Spring", "Jogger"],
    "Dodge": ["Challenger", "Charger", "Durango", "Ram"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9"],
    "Ferrari": ["488", "F8", "SF90", "Roma", "Portofino", "812", "LaFerrari"],
    "Fiat": ["500", "500X", "500L", "Panda", "Punto", "Tipo", "Ducato", "Doblo", "Fiorino"],
    "Ford": ["Fiesta", "Focus", "Mondeo", "Mustang", "Kuga", "EcoSport", "Puma", "Explorer", "Edge", "Transit", "Ranger", "Ka+"],
    "Genesis": ["G70", "G80", "G90", "GV60", "GV70", "GV80"],
    "Honda": ["Civic", "Accord", "Jazz", "HR-V", "CR-V", "Pilot", "Ridgeline", "e"],
    "Hyundai": ["i10", "i20", "i30", "i40", "Tucson", "Santa Fe", "Kona", "Ioniq", "Ioniq 5", "Nexo"],
    "Infiniti": ["Q30", "Q50", "Q60", "Q70", "QX30", "QX50", "QX60", "QX70"],
    "Isuzu": ["D-Max", "MU-X"],
    "Jaguar": ["XE", "XF", "XJ", "F-Type", "F-Pace", "E-Pace", "I-Pace"],
    "Jeep": ["Compass", "Grand Cherokee", "Cherokee", "Wrangler", "Renegade", "Gladiator", "Avenger"],
    "Kia": ["Picanto", "Rio", "Ceed", "Stonic", "XCeed", "Sportage", "Sorento", "Niro", "EV6", "Soul"],
    "Lada": ["Niva", "Vesta", "Granta"],
    "Lamborghini": ["Huracán", "Aventador", "Urus"],
    "Lancia": ["Ypsilon", "Delta"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Sport", "Range Rover Evoque", "Range Rover Velar"],
    "Lexus": ["IS", "ES", "LS", "CT", "NX", "RX", "GX", "LX", "LC", "UX"],
    "Lincoln": ["Continental", "Navigator", "Aviator", "Corsair"],
    "Lotus": ["Elise", "Exige", "Evora", "Emira"],
    "Maserati": ["Ghibli", "Quattroporte", "Levante", "MC20"],
    "Mazda": ["2", "3", "6", "CX-3", "CX-5", "CX-30", "CX-60", "MX-5", "MX-30"],
    "McLaren": ["570S", "720S", "765LT", "Artura"],
    "Mercedes": ["Classe A", "Classe B", "Classe C", "Classe E", "Classe S", "CLA", "CLS", "GLA", "GLB", "GLC", "GLE", "GLS", "G", "SL", "SLC", "AMG GT", "EQA", "EQB", "EQC", "EQS", "EQV", "Vito", "Sprinter", "Citan"],
    "MG": ["ZS", "MG5", "Marvel R", "HS"],
    "Mini": ["Cooper", "Countryman", "Clubman", "Paceman", "Roadster"],
    "Mitsubishi": ["Space Star", "ASX", "Eclipse Cross", "Outlander", "L200"],
    "Nissan": ["Micra", "Note", "Sentra", "Altima", "Maxima", "Juke", "Qashqai", "X-Trail", "Murano", "Pathfinder", "Titan", "Leaf", "Ariya", "NV200", "Primastar"],
    "Opel": ["Corsa", "Astra", "Insignia", "Crossland", "Grandland", "Mokka", "Zafira", "Vivaro", "Movano", "Combo"],
    "Peugeot": ["108", "208", "308", "408", "508", "2008", "3008", "5008", "Partner", "Expert", "Boxer", "Rifter", "Traveller", "e-208", "e-2008"],
    "Porsche": ["911", "Boxster", "Cayman", "Panamera", "Macan", "Cayenne", "Taycan"],
    "Ram": ["1500", "2500", "3500", "ProMaster"],
    "Renault": ["Twingo", "Clio", "Mégane", "Talisman", "Captur", "Kadjar", "Koleos", "Arkana", "Austral", "Espace", "Scénic", "Kangoo", "Trafic", "Master", "ZOE", "Twizy"],
    "Rolls-Royce": ["Ghost", "Phantom", "Wraith", "Dawn", "Cullinan"],
    "Saab": ["9-3", "9-5"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona", "Tarraco", "Alhambra"],
    "Skoda": ["Fabia", "Scala", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq"],
    "Smart": ["ForTwo", "ForFour"],
    "SsangYong": ["Tivoli", "Korando", "Rexton"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "XV", "BRZ"],
    "Suzuki": ["Swift", "Baleno", "SX4", "Vitara", "S-Cross", "Jimny", "Ignis"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y"],
    "Toyota": ["Aygo", "Yaris", "Corolla", "Camry", "Avalon", "C-HR", "RAV4", "Highlander", "4Runner", "Sequoia", "Land Cruiser", "Prius", "Mirai", "Hilux", "Proace", "Supra"],
    "Volkswagen": ["up!", "Polo", "Golf", "Jetta", "Passat", "Arteon", "T-Cross", "T-Roc", "Tiguan", "Touareg", "Sharan", "Touran", "Caddy", "Transporter", "Crafter", "ID.3", "ID.4", "ID.Buzz"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "S90", "V60", "V90", "C40", "EX30"]
}

CONTRACT_DURATIONS = [24, 25, 27, 30, 35, 36, 37, 48, 60]
ANNUAL_MILEAGES = list(range(10000, 65000, 5000))

# Routes
@api_router.get("/")
async def root():
    return {"message": "CRM LLD Automobile API", "version": "1.0.0"}

@api_router.get("/config")
async def get_config():
    return {
        "prestataires": PRESTATAIRES,
        "commerciaux": COMMERCIAUX,
        "car_brands": CAR_BRANDS,
        "contract_durations": CONTRACT_DURATIONS,
        "annual_mileages": ANNUAL_MILEAGES,
        "status_colors": STATUS_COLORS
    }

# Leads routes
@api_router.post("/leads", response_model=Lead)
async def create_lead(lead_data: LeadCreate):
    company = Company(**lead_data.company.dict())
    contact = Contact(**lead_data.contact.dict())
    vehicles = [Vehicle(**vehicle.dict()) for vehicle in lead_data.vehicles]
    
    lead = Lead(
        company=company,
        contact=contact,
        vehicles=vehicles,
        note=lead_data.note,
        assigned_to_prestataire=lead_data.assigned_to_prestataire,
        assigned_to_commercial=lead_data.assigned_to_commercial
    )
    
    await db.leads.insert_one(lead.dict())
    return lead

@api_router.get("/leads", response_model=List[Lead])
async def get_leads(
    status: Optional[str] = Query(None),
    prestataire: Optional[str] = Query(None),
    commercial: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    query = {}
    
    if status:
        query["status"] = status
    if prestataire:
        query["assigned_to_prestataire"] = prestataire
    if commercial:
        query["assigned_to_commercial"] = commercial
    if search:
        query["$or"] = [
            {"company.name": {"$regex": search, "$options": "i"}},
            {"contact.first_name": {"$regex": search, "$options": "i"}},
            {"contact.last_name": {"$regex": search, "$options": "i"}},
            {"vehicles.brand": {"$regex": search, "$options": "i"}},
            {"vehicles.model": {"$regex": search, "$options": "i"}},
            {"note": {"$regex": search, "$options": "i"}}
        ]
    
    leads = await db.leads.find(query).skip(skip).limit(limit).to_list(limit)
    return [Lead(**lead) for lead in leads]

@api_router.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str):
    lead = await db.leads.find_one({"id": lead_id})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return Lead(**lead)

@api_router.put("/leads/{lead_id}", response_model=Lead)
async def update_lead(lead_id: str, lead_update: LeadUpdate):
    existing_lead = await db.leads.find_one({"id": lead_id})
    if not existing_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = lead_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.leads.update_one({"id": lead_id}, {"$set": update_data})
    
    updated_lead = await db.leads.find_one({"id": lead_id})
    return Lead(**updated_lead)

@api_router.delete("/leads/{lead_id}")
async def delete_lead(lead_id: str):
    result = await db.leads.delete_one({"id": lead_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted successfully"}

# Activities routes
@api_router.post("/activities", response_model=Activity)
async def create_activity(activity_data: ActivityCreate):
    activity = Activity(**activity_data.dict())
    await db.activities.insert_one(activity.dict())
    return activity

@api_router.get("/activities/{lead_id}", response_model=List[Activity])
async def get_lead_activities(lead_id: str):
    activities = await db.activities.find({"lead_id": lead_id}).to_list(1000)
    return [Activity(**activity) for activity in activities]

@api_router.put("/activities/{activity_id}", response_model=Activity)
async def update_activity(activity_id: str, completed: bool):
    await db.activities.update_one(
        {"id": activity_id}, 
        {"$set": {"completed": completed, "updated_at": datetime.utcnow()}}
    )
    updated_activity = await db.activities.find_one({"id": activity_id})
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return Activity(**updated_activity)

# Dashboard stats
@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    total_leads = await db.leads.count_documents({})
    
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_counts = await db.leads.aggregate(pipeline).to_list(None)
    
    status_stats = {}
    for item in status_counts:
        status_stats[item["_id"]] = item["count"]
    
    # Recent activities
    recent_activities = await db.activities.find().sort("created_at", -1).limit(5).to_list(5)
    
    return {
        "total_leads": total_leads,
        "status_stats": status_stats,
        "recent_activities": [Activity(**activity) for activity in recent_activities]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()