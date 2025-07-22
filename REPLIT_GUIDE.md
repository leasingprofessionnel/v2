# 🚀 GUIDE DE PUBLICATION SUR REPLIT

## 📋 Instructions étape par étape

### **Étape 1 : Créer un compte Replit**
1. Allez sur [replit.com](https://replit.com)
2. Créez un compte gratuit ou connectez-vous

### **Étape 2 : Créer un nouveau projet**
1. Cliquez sur **"+ Create Repl"**
2. Sélectionnez **"Import from GitHub"** OU **"Upload folder"**
3. Nommez votre projet : `crm-leasinprofessionnel`

### **Étape 3 : Importer les fichiers**
**Option A - GitHub (recommandée) :**
1. Créez un dépôt GitHub privé
2. Uploadez tous les fichiers du CRM
3. Collez l'URL GitHub dans Replit

**Option B - Upload direct :**
1. Compressez le dossier `/app` en fichier ZIP
2. Uploadez sur Replit
3. Décompressez dans le projet

### **Étape 4 : Configuration automatique**
Replit détectera automatiquement :
- ✅ Python 3.11 (backend)
- ✅ Node.js 18 (frontend)  
- ✅ MongoDB (base de données)

### **Étape 5 : Variables d'environnement**
1. Dans Replit, allez dans **"Secrets"** (🔒)
2. Ajoutez ces variables :
   ```
   MONGO_URL=mongodb://localhost:27017/crm_lld
   DB_NAME=crm_lld
   ```

### **Étape 6 : Modifier l'URL backend**
1. Ouvrez `frontend/.env`
2. Remplacez `your-repl-name.your-username.repl.co` par votre vraie URL Replit
3. Exemple : `https://crm-leasinprofessionnel.john-doe.repl.co`

### **Étape 7 : Lancement**
1. Cliquez sur le gros bouton **"Run" ▶️**
2. Patientez pendant l'installation (3-5 minutes)
3. Votre CRM sera accessible sur l'URL générée !

## 🔧 Configuration avancée

### **URLs importantes :**
- **Frontend** : `https://your-repl-name.your-username.repl.co`  
- **API Backend** : `https://your-repl-name.your-username.repl.co:3001/api`

### **Mise à jour du frontend/.env :**
```env
REACT_APP_BACKEND_URL=https://votre-nom-repl.votre-nom.repl.co
WDS_SOCKET_HOST=0.0.0.0
WDS_SOCKET_PORT=443
```

## 🎯 Points d'attention

### **✅ À faire :**
- Renommez votre Repl avec un nom unique
- Vérifiez que MongoDB démarre correctement
- Testez tous les endpoints API
- Validez la génération de PDF

### **❌ Problèmes courants :**
- **MongoDB ne démarre pas** → Vérifiez les logs dans `Console`
- **Frontend ne charge pas** → Vérifiez l'URL dans `.env`
- **API inaccessible** → Vérifiez que le backend tourne sur port 8001

## 🚀 Déploiement en production

### **Replit Deployments :**
1. Allez dans **"Deployments"**
2. Cliquez **"Create deployment"**
3. Choisissez **"Autoscale"** pour plus de performance
4. Votre CRM aura une URL permanente !

## 📞 Support
En cas de problème :
1. Vérifiez la **Console** Replit pour les erreurs
2. Testez l'API avec `curl` dans le Shell
3. Consultez les logs MongoDB

---
🎉 **Félicitations !** Votre CRM LEASINPROFESSIONNEL.FR est maintenant en ligne !