#!/bin/bash

echo "🚀 Installation de CRM LEASINPROFESSIONNEL.FR pour Replit"
echo "=================================================="

# Création des dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p data/db
mkdir -p logs
mkdir -p temp

# Installation des dépendances Python
echo "🐍 Installation des dépendances Python..."
cd backend
pip install -r requirements.txt
cd ..

# Installation des dépendances Node.js
echo "📦 Installation des dépendances Node.js..."
cd frontend
npm install
cd ..

echo "✅ Installation terminée !"
echo ""
echo "🎯 Prochaines étapes :"
echo "1. Modifiez frontend/.env avec votre URL Replit"
echo "2. Cliquez sur 'Run' pour démarrer l'application"
echo "3. Votre CRM sera accessible sur votre URL Replit !"
echo ""
echo "📚 Consultez REPLIT_GUIDE.md pour plus de détails"