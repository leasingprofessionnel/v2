# Instructions pour créer un dépôt GitHub

## 🚀 Étapes pour publier votre CRM sur GitHub

### 1. Créer le dépôt sur GitHub.com

1. Allez sur **github.com**
2. Cliquez **"+ New repository"**
3. Nom du repository : `crm-leasinprofessionnel`
4. Description : `CRM LEASINPROFESSIONNEL.FR - Système de gestion des leads LLD automobile`
5. Choisissez **Public** (pour accès facile depuis Replit)
6. Cochez **"Add a README file"**
7. Cliquez **"Create repository"**

### 2. URL du dépôt GitHub

Une fois créé, votre dépôt sera accessible à :
```
https://github.com/VOTRE-USERNAME/crm-leasinprofessionnel
```

### 3. Utiliser avec Replit

Sur Replit :
1. **"+ Create Repl"**
2. **"Import from GitHub"**  
3. Collez l'URL : `https://github.com/VOTRE-USERNAME/crm-leasinprofessionnel`

## 📁 Structure du projet sur GitHub

```
crm-leasinprofessionnel/
├── README.md (Description du projet)
├── REPLIT_GUIDE.md (Guide de déploiement)
├── .replit (Configuration Replit)
├── main.py (Point d'entrée)
├── backend/ (API FastAPI)
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/ (Interface React)
│   ├── src/
│   ├── package.json
│   └── .env
└── scripts/ (Scripts d'installation)
```