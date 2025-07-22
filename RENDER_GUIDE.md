# 🚀 DÉPLOIEMENT SUR RENDER.COM

## ⭐ RENDER - La meilleure alternative gratuite

### ✅ Avantages vs Replit :
- Plus rapide et stable
- URL permanente
- Déploiement automatique
- Interface plus simple
- Support technique meilleur

### 📋 Instructions étape par étape

#### ÉTAPE 1 : Créer compte Render
1. Allez sur **render.com**
2. **"Get Started for Free"**
3. Connectez-vous avec **Google** ou **GitHub**

#### ÉTAPE 2 : Nouveau service Web
1. Cliquez **"New +"**
2. **"Web Service"**
3. **"Build and deploy from a Git repository"**
4. Cliquez **"Next"**

#### ÉTAPE 3 : Configuration automatique
- **Name** : `crm-leasinprofessionnel`
- **Runtime** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python main.py`
- **Plan** : `Free` (0$/mois)

#### ÉTAPE 4 : Variables d'environnement
Dans **Environment** :
```
MONGO_URL=mongodb://localhost:27017/crm
DB_NAME=crm_lld
PORT=10000
```

#### ÉTAPE 5 : Déployer
1. Cliquez **"Create Web Service"**
2. Patientez 3-5 minutes
3. ✅ **Votre CRM est en ligne !**

### 🌐 Résultat
URL de votre CRM : `https://crm-leasinprofessionnel.onrender.com`

## 🎯 Fichiers nécessaires pour Render

### requirements.txt
```
fastapi==0.110.1
uvicorn[standard]==0.25.0
pydantic>=2.6.4
python-multipart>=0.0.9
```

### main.py (version Render)
```python
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="CRM LEASINPROFESSIONNEL.FR")

@app.get("/")
def root():
    return {"message": "🚗 CRM LEASINPROFESSIONNEL.FR", "status": "✅ En ligne sur Render !"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```