#!/usr/bin/env python3
"""
CRM LEASINPROFESSIONNEL.FR - Point d'entrée principal pour Replit
"""

import subprocess
import sys
import os
import time
import threading

def run_mongodb():
    """Démarre MongoDB"""
    print("🍃 Démarrage de MongoDB...")
    try:
        subprocess.run(["./setup_mongo.sh"], check=True, shell=True)
        print("✅ MongoDB démarré avec succès")
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du démarrage de MongoDB")

def run_backend():
    """Démarre le backend FastAPI"""
    print("🔧 Démarrage du backend...")
    os.chdir("backend")
    subprocess.run([sys.executable, "server.py"])

def run_frontend():
    """Démarre le frontend React"""
    print("🌐 Démarrage du frontend...")
    time.sleep(5)  # Attendre que le backend soit prêt
    os.chdir("../frontend")
    subprocess.run(["npm", "start"])

def main():
    print("🚀 CRM LEASINPROFESSIONNEL.FR - Démarrage...")
    print("=" * 50)
    
    # Créer les dossiers nécessaires
    os.makedirs("data/db", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Démarrer MongoDB
    run_mongodb()
    
    # Démarrer le backend dans un thread séparé
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Démarrer le frontend (process principal)
    run_frontend()

if __name__ == "__main__":
    main()