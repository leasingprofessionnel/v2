#!/bin/bash

echo "🚀 Démarrage de CRM LEASINPROFESSIONNEL.FR"

# Installer les dépendances Python
echo "📦 Installation des dépendances backend..."
cd backend
pip install -r requirements.txt

# Démarrer MongoDB en arrière-plan
echo "🍃 Démarrage de MongoDB..."
mongod --dbpath ./data --fork --logpath ./mongodb.log

# Démarrer le backend en arrière-plan
echo "🔧 Démarrage de l'API backend..."
cd ../
python backend/server.py &

# Installer les dépendances frontend
echo "📦 Installation des dépendances frontend..."
cd frontend
npm install

# Démarrer le frontend
echo "🌐 Démarrage de l'interface utilisateur..."
npm start