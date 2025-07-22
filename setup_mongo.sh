#!/bin/bash

# Configuration MongoDB pour Replit
mkdir -p data/db
mkdir -p logs

# Démarrage MongoDB
mongod --dbpath ./data/db --logpath ./logs/mongodb.log --fork --bind_ip 127.0.0.1 --port 27017

echo "MongoDB démarré sur port 27017"