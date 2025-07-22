# 🚂 RAILWAY.APP - Déploiement en 1 clic

## ✨ Pourquoi Railway ?
- **1 clic** pour déployer
- Interface **très jolie**
- **Auto-détection** Python/Node.js
- Base de données gratuite incluse
- URL personnalisée gratuite

## 📋 Instructions ultra-rapides

### ÉTAPE 1 : Aller sur Railway
1. **railway.app**
2. **"Start a New Project"**
3. Connexion avec **GitHub**

### ÉTAPE 2 : Déployer
1. **"Deploy from GitHub repo"**
2. Ou **"Empty Project"** → Upload ZIP
3. Railway détecte automatiquement Python !

### ÉTAPE 3 : Configuration
- **Nom** : `crm-leasinprofessionnel`
- **Auto-deployment** : ✅ Activé
- **Domain** : `crm-leasinprofessionnel.up.railway.app`

### 🎯 Résultat en 2 minutes !
```
https://crm-leasinprofessionnel.up.railway.app
```

## 💾 Base de données gratuite
Railway offre PostgreSQL gratuit :
1. **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Variables automatiquement configurées !

## 📦 Package.json pour Railway
```json
{
  "name": "crm-leasinprofessionnel",
  "scripts": {
    "start": "python main.py"
  },
  "engines": {
    "python": "3.11"
  }
}
```