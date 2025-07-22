#!/usr/bin/env python3
"""
Backend API Test Suite for CRM LEASINPROFESSIONNEL.FR
Tests all the restored features mentioned in the review request:
1. PDF Export Functionality - GET /api/leads/{lead_id}/pdf
2. Reminder System Backend - POST /api/reminders, GET /api/reminders, GET /api/calendar/reminders
3. Car Brands and Models Configuration - GET /api/config (90+ car brands)
4. Commercial and Prestataire Lists - GET /api/config
5. Configuration API Endpoint - Complete configuration
"""

import requests
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any

class CRMAPITester:
    def __init__(self):
        # Use the public URL from frontend/.env
        self.base_url = "https://9abe3c42-2426-4b4a-a2e0-1b6d026d6b24.preview.emergentagent.com/api"
        self.headers = {'Content-Type': 'application/json'}
        self.tests_run = 0
        self.tests_passed = 0
        self.created_lead_ids = []
        self.created_reminder_ids = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def test_api_root(self):
        """Test API root endpoint"""
        try:
            # The root endpoint is at the base URL without /api prefix
            root_url = self.base_url.replace('/api', '')
            response = requests.get(f"{root_url}/", headers=self.headers, timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            details = f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            return self.log_test("API Root", success, details)
        except Exception as e:
            return self.log_test("API Root", False, f"Error: {str(e)}")

    def test_get_config(self):
        """Test configuration endpoint with all restored features"""
        try:
            response = requests.get(f"{self.base_url}/config", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = ['prestataires', 'commerciaux', 'car_brands', 'contract_durations', 'annual_mileages', 'status_colors']
                has_all_keys = all(key in data for key in required_keys)
                
                # Test commerciaux (should include Matthews, Sauveur, Autre)
                commerciaux = data.get('commerciaux', [])
                expected_commerciaux = ["Matthews", "Sauveur", "Autre"]
                commerciaux_ok = all(c in commerciaux for c in expected_commerciaux)
                
                # Test prestataires (should include major leasing companies)
                prestataires = data.get('prestataires', [])
                expected_prestataires = ["Localease", "Leasefactory", "Ayvens", "ALD Automotive", "Arval"]
                prestataires_ok = all(p in prestataires for p in expected_prestataires)
                
                # Test car brands (should have 90+ brands)
                car_brands = data.get('car_brands', {})
                brand_count = len(car_brands)
                brands_90_plus = brand_count >= 90
                
                # Test specific premium brands and their models
                premium_brands_models = {
                    "BMW": ["Série 1", "Série 3", "X1", "X3"],
                    "Mercedes": ["Classe A", "Classe C", "GLA", "GLC"],
                    "Audi": ["A1", "A3", "Q2", "Q3"],
                    "Porsche": ["911", "Boxster", "Macan", "Cayenne"],
                    "Ferrari": ["488", "F8", "SF90", "Roma"]
                }
                
                premium_ok = True
                for brand, models in premium_brands_models.items():
                    if brand not in car_brands:
                        premium_ok = False
                        break
                    brand_models = car_brands[brand]
                    if not any(model in brand_models for model in models):
                        premium_ok = False
                        break
                
                # Test French brands
                french_brands = ["Peugeot", "Renault", "Citroën", "DS"]
                french_ok = all(brand in car_brands for brand in french_brands)
                
                # Test contract durations and annual mileages
                contract_durations = data.get('contract_durations', [])
                annual_mileages = data.get('annual_mileages', [])
                durations_ok = len(contract_durations) >= 5 and 36 in contract_durations
                mileages_ok = len(annual_mileages) >= 5 and 15000 in annual_mileages
                
                # Test status colors
                status_colors = data.get('status_colors', {})
                status_colors_ok = len(status_colors) >= 5
                
                success = (has_all_keys and commerciaux_ok and prestataires_ok and 
                          brands_90_plus and premium_ok and french_ok and 
                          durations_ok and mileages_ok and status_colors_ok)
                
                details = (f"Status: {response.status_code}, Keys: {has_all_keys}, "
                          f"Commerciaux: {commerciaux_ok} ({len(commerciaux)}), "
                          f"Prestataires: {prestataires_ok} ({len(prestataires)}), "
                          f"Brands: {brand_count} (90+: {brands_90_plus}), "
                          f"Premium: {premium_ok}, French: {french_ok}, "
                          f"Durations: {durations_ok}, Mileages: {mileages_ok}, "
                          f"StatusColors: {status_colors_ok}")
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Config (All Restored Features)", success, details)
        except Exception as e:
            return self.log_test("Get Config (All Restored Features)", False, f"Error: {str(e)}")

    def test_create_lead_single_vehicle(self):
        """Test creating a lead with single vehicle and note"""
        lead_data = {
            "company": {
                "name": "Entreprise Test SARL",
                "siret": "12345678901234",
                "address": "123 Rue de la Paix, 75001 Paris",
                "phone": "01.23.45.67.89",
                "email": "contact@entreprise-test.fr"
            },
            "contact": {
                "first_name": "Jean",
                "last_name": "Dupont",
                "email": "jean.dupont@entreprise-test.fr",
                "phone": "06.12.34.56.78",
                "position": "Directeur Général"
            },
            "vehicles": [{
                "brand": "BMW",
                "model": "Série 3",
                "carburant": "diesel",
                "contract_duration": 36,
                "annual_mileage": 20000
            }],
            "note": "Client intéressé par une flotte de véhicules. Budget prévu: 50k€. Timing: Q2 2025. Préfère les véhicules allemands.",
            "assigned_to_prestataire": "Leaseplan",
            "assigned_to_commercial": "Matthews"
        }

        try:
            response = requests.post(f"{self.base_url}/leads", 
                                   json=lead_data, 
                                   headers=self.headers, 
                                   timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                lead_id = data.get('lead', {}).get('id')
                if lead_id:
                    self.created_lead_ids.append(lead_id)
                
                # Verify new features
                lead_data_obj = data.get('lead', {})
                note_ok = lead_data_obj.get('note') == lead_data['note']
                commercial_ok = lead_data_obj.get('assigned_to_commercial') == 'Matthews'
                vehicle_ok = (lead_data_obj.get('vehicles', [{}])[0].get('brand') == 'BMW' and
                            lead_data_obj.get('vehicles', [{}])[0].get('model') == 'Série 3')
                
                details = f"Status: {response.status_code}, Lead ID: {lead_id}, Note: {note_ok}, Commercial: {commercial_ok}, Vehicle: {vehicle_ok}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            return self.log_test("Create Lead (Single Vehicle + Note)", success, details)
        except Exception as e:
            return self.log_test("Create Lead (Single Vehicle + Note)", False, f"Error: {str(e)}")

    def test_create_lead_multi_vehicle(self):
        """Test creating a lead with multiple vehicles"""
        lead_data = {
            "company": {
                "name": "Multi-Fleet Corp",
                "siret": "98765432109876",
                "address": "456 Avenue des Champs, 75008 Paris",
                "phone": "01.98.76.54.32",
                "email": "fleet@multifleet.fr"
            },
            "contact": {
                "first_name": "Marie",
                "last_name": "Martin",
                "email": "marie.martin@multifleet.fr",
                "phone": "06.98.76.54.32",
                "position": "Responsable Flotte"
            },
            "vehicles": [
                {
                    "brand": "BMW",
                    "model": "Série 3",
                    "carburant": "diesel",
                    "contract_duration": 36,
                    "annual_mileage": 25000
                },
                {
                    "brand": "Mercedes",
                    "model": "Classe C",
                    "carburant": "hybride",
                    "contract_duration": 48,
                    "annual_mileage": 20000
                },
                {
                    "brand": "Audi",
                    "model": "A4",
                    "carburant": "essence",
                    "contract_duration": 36,
                    "annual_mileage": 15000
                }
            ],
            "note": "Commande groupée pour renouvellement de flotte. Négociation en cours sur les tarifs. Livraison souhaitée avant fin Q1.",
            "assigned_to_prestataire": "ALD Automotive",
            "assigned_to_commercial": "Sauveur"
        }

        try:
            response = requests.post(f"{self.base_url}/leads", 
                                   json=lead_data, 
                                   headers=self.headers, 
                                   timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                lead_id = data.get('lead', {}).get('id')
                if lead_id:
                    self.created_lead_ids.append(lead_id)
                
                lead_data_obj = data.get('lead', {})
                vehicles = lead_data_obj.get('vehicles', [])
                vehicle_count_ok = len(vehicles) == 3
                brands_ok = [v.get('brand') for v in vehicles] == ['BMW', 'Mercedes', 'Audi']
                commercial_ok = lead_data_obj.get('assigned_to_commercial') == 'Sauveur'
                
                details = f"Status: {response.status_code}, Lead ID: {lead_id}, Vehicles: {len(vehicles)}/3, Brands: {brands_ok}, Commercial: {commercial_ok}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            return self.log_test("Create Lead (Multi Vehicle)", success, details)
        except Exception as e:
            return self.log_test("Create Lead (Multi Vehicle)", False, f"Error: {str(e)}")

    def test_search_in_notes(self):
        """Test search functionality in notes"""
        try:
            response = requests.get(f"{self.base_url}/leads?search=flotte", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                results_count = len(data) if isinstance(data, list) else 0
                # Should find leads with "flotte" in notes
                details = f"Status: {response.status_code}, Search 'flotte' results: {results_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Search in Notes", success, details)
        except Exception as e:
            return self.log_test("Search in Notes", False, f"Error: {str(e)}")

    def test_specific_car_brands(self):
        """Test specific car brands mentioned in requirements"""
        try:
            response = requests.get(f"{self.base_url}/config", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                car_brands = data.get('car_brands', {})
                
                # Test specific brands and models mentioned in requirements
                test_cases = [
                    ("BMW", "Série 3"),
                    ("Mercedes", "Classe C"),
                    ("Audi", "A4"),
                    ("Porsche", "911"),
                    ("Ferrari", "488"),
                    ("Peugeot", "308"),
                    ("Renault", "Clio"),
                    ("Citroën", "C4")
                ]
                
                results = []
                for brand, model in test_cases:
                    brand_exists = brand in car_brands
                    model_exists = model in car_brands.get(brand, []) if brand_exists else False
                    results.append((brand, model, brand_exists and model_exists))
                
                success_count = sum(1 for _, _, ok in results if ok)
                total_tests = len(test_cases)
                
                details = f"Status: {response.status_code}, Brand/Model tests: {success_count}/{total_tests} passed"
                success = success_count == total_tests
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Specific Car Brands", success, details)
        except Exception as e:
            return self.log_test("Specific Car Brands", False, f"Error: {str(e)}")

    def test_get_leads(self):
        """Test getting all leads"""
        try:
            response = requests.get(f"{self.base_url}/leads", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                leads_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Leads count: {leads_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Leads", success, details)
        except Exception as e:
            return self.log_test("Get Leads", False, f"Error: {str(e)}")

    def test_get_single_lead(self):
        """Test getting a single lead by ID"""
        if not self.created_lead_ids:
            return self.log_test("Get Single Lead", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        try:
            response = requests.get(f"{self.base_url}/leads/{lead_id}", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, Company: {data.get('company', {}).get('name', 'N/A')}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Single Lead", success, details)
        except Exception as e:
            return self.log_test("Get Single Lead", False, f"Error: {str(e)}")

    def test_update_lead_status(self):
        """Test updating lead status"""
        if not self.created_lead_ids:
            return self.log_test("Update Lead Status", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        update_data = {"status": "offre"}
        
        try:
            response = requests.put(f"{self.base_url}/leads/{lead_id}", 
                                  json=update_data, 
                                  headers=self.headers, 
                                  timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                new_status = data.get('status')
                details = f"Status: {response.status_code}, New status: {new_status}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Update Lead Status", success, details)
        except Exception as e:
            return self.log_test("Update Lead Status", False, f"Error: {str(e)}")

    def test_update_lead_note(self):
        """Test updating lead note"""
        if not self.created_lead_ids:
            return self.log_test("Update Lead Note", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        update_data = {
            "note": "Note mise à jour: Offre envoyée le " + datetime.now().strftime("%d/%m/%Y") + ". En attente de retour client."
        }
        
        try:
            response = requests.put(f"{self.base_url}/leads/{lead_id}", 
                                  json=update_data, 
                                  headers=self.headers, 
                                  timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                updated_note = data.get('note', '')
                note_updated = 'mise à jour' in updated_note
                details = f"Status: {response.status_code}, Note updated: {note_updated}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Update Lead Note", success, details)
        except Exception as e:
            return self.log_test("Update Lead Note", False, f"Error: {str(e)}")

    def test_search_leads(self):
        """Test lead search functionality"""
        try:
            response = requests.get(f"{self.base_url}/leads?search=Test", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                results_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Search results: {results_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Search Leads", success, details)
        except Exception as e:
            return self.log_test("Search Leads", False, f"Error: {str(e)}")

    def test_filter_leads_by_commercial(self):
        """Test lead filtering by commercial (new feature)"""
        try:
            response = requests.get(f"{self.base_url}/leads?commercial=Matthews", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                results_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Matthews leads: {results_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Filter Leads by Commercial", success, details)
        except Exception as e:
            return self.log_test("Filter Leads by Commercial", False, f"Error: {str(e)}")

    def test_filter_leads_by_status(self):
        """Test lead filtering by status"""
        try:
            response = requests.get(f"{self.base_url}/leads?status=offre", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                results_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Filtered results: {results_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Filter Leads by Status", success, details)
        except Exception as e:
            return self.log_test("Filter Leads by Status", False, f"Error: {str(e)}")

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/dashboard/stats", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                total_leads = data.get('total_leads', 0)
                status_stats = data.get('status_stats', {})
                details = f"Status: {response.status_code}, Total leads: {total_leads}, Status types: {len(status_stats)}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Dashboard Stats", success, details)
        except Exception as e:
            return self.log_test("Dashboard Stats", False, f"Error: {str(e)}")

    def test_create_activity(self):
        """Test activity creation"""
        if not self.created_lead_ids:
            return self.log_test("Create Activity", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        activity_data = {
            "lead_id": lead_id,
            "activity_type": "note",
            "title": "Premier contact effectué",
            "description": "Client intéressé par le véhicule BMW Série 3"
        }

        try:
            response = requests.post(f"{self.base_url}/activities", 
                                   json=activity_data, 
                                   headers=self.headers, 
                                   timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                activity_id = data.get('id')
                details = f"Status: {response.status_code}, Activity ID: {activity_id}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Create Activity", success, details)
        except Exception as e:
            return self.log_test("Create Activity", False, f"Error: {str(e)}")

    def test_get_lead_activities(self):
        """Test getting activities for a lead"""
        if not self.created_lead_ids:
            return self.log_test("Get Lead Activities", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        try:
            response = requests.get(f"{self.base_url}/activities/{lead_id}", 
                                  headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                activities_count = len(data) if isinstance(data, list) else 0
                details = f"Status: {response.status_code}, Activities count: {activities_count}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Lead Activities", success, details)
        except Exception as e:
            return self.log_test("Get Lead Activities", False, f"Error: {str(e)}")

    def test_pdf_export(self):
        """Test PDF export functionality for leads"""
        if not self.created_lead_ids:
            return self.log_test("PDF Export", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        try:
            response = requests.get(f"{self.base_url}/leads/{lead_id}/pdf", 
                                  headers={'Accept': 'application/pdf'}, timeout=30)
            success = response.status_code == 200
            if success:
                content_type = response.headers.get('content-type', '')
                is_pdf = 'application/pdf' in content_type
                content_length = len(response.content)
                has_content = content_length > 1000  # PDF should be at least 1KB
                
                success = is_pdf and has_content
                details = f"Status: {response.status_code}, Content-Type: {content_type}, Size: {content_length} bytes, Valid PDF: {is_pdf and has_content}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            return self.log_test("PDF Export", success, details)
        except Exception as e:
            return self.log_test("PDF Export", False, f"Error: {str(e)}")

    def test_create_reminder(self):
        """Test creating reminders"""
        if not self.created_lead_ids:
            return self.log_test("Create Reminder", False, "No lead ID available")
        
        lead_id = self.created_lead_ids[0]
        reminder_date = (datetime.now() + timedelta(days=7)).isoformat()
        
        reminder_data = {
            "lead_id": lead_id,
            "title": "Relance client BMW Série 3",
            "description": "Appeler le client pour faire le point sur l'offre BMW Série 3. Vérifier si des ajustements sont nécessaires.",
            "reminder_date": reminder_date
        }

        try:
            response = requests.post(f"{self.base_url}/reminders", 
                                   json=reminder_data, 
                                   headers=self.headers, 
                                   timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                reminder_id = data.get('reminder', {}).get('id')
                if reminder_id:
                    self.created_reminder_ids.append(reminder_id)
                
                title_ok = data.get('reminder', {}).get('title') == reminder_data['title']
                lead_id_ok = data.get('reminder', {}).get('lead_id') == lead_id
                
                details = f"Status: {response.status_code}, Reminder ID: {reminder_id}, Title: {title_ok}, Lead ID: {lead_id_ok}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            return self.log_test("Create Reminder", success, details)
        except Exception as e:
            return self.log_test("Create Reminder", False, f"Error: {str(e)}")

    def test_get_reminders(self):
        """Test getting all reminders"""
        try:
            response = requests.get(f"{self.base_url}/reminders", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                reminders_count = len(data) if isinstance(data, list) else 0
                has_created_reminder = any(r.get('id') in self.created_reminder_ids for r in data) if self.created_reminder_ids else True
                
                details = f"Status: {response.status_code}, Reminders count: {reminders_count}, Has created: {has_created_reminder}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Reminders", success, details)
        except Exception as e:
            return self.log_test("Get Reminders", False, f"Error: {str(e)}")

    def test_calendar_reminders(self):
        """Test calendar reminders with date filtering"""
        try:
            # Test default (30 days)
            response = requests.get(f"{self.base_url}/calendar/reminders", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                reminders_count = len(data) if isinstance(data, list) else 0
                
                # Test with custom days parameter
                response2 = requests.get(f"{self.base_url}/calendar/reminders?days=7", headers=self.headers, timeout=10)
                success2 = response2.status_code == 200
                if success2:
                    data2 = response2.json()
                    reminders_7days = len(data2) if isinstance(data2, list) else 0
                    
                    # 7-day filter should return same or fewer results than 30-day
                    filter_works = reminders_7days <= reminders_count
                    
                    details = f"Status: {response.status_code}, 30-day: {reminders_count}, 7-day: {reminders_7days}, Filter works: {filter_works}"
                    success = success and success2 and filter_works
                else:
                    details = f"Status: {response.status_code}, 7-day test failed: {response2.status_code}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Calendar Reminders", success, details)
        except Exception as e:
            return self.log_test("Calendar Reminders", False, f"Error: {str(e)}")

    def test_comprehensive_car_brands(self):
        """Test comprehensive car brands database (90+ brands)"""
        try:
            response = requests.get(f"{self.base_url}/config", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                car_brands = data.get('car_brands', {})
                
                # Test for 90+ brands
                brand_count = len(car_brands)
                has_90_plus = brand_count >= 90
                
                # Test specific brands mentioned in the requirements
                test_brands = [
                    "Abarth", "BMW", "Mercedes", "Audi", "Porsche", "Ferrari", 
                    "Peugeot", "Renault", "Citroën", "DS", "Volkswagen", "Toyota",
                    "Tesla", "Lamborghini", "Maserati", "Jaguar", "Land Rover",
                    "Volvo", "Lexus", "Infiniti", "Genesis", "McLaren", "Bentley",
                    "Rolls-Royce", "Bugatti", "Alpine", "Lotus", "Morgan"
                ]
                
                brands_found = sum(1 for brand in test_brands if brand in car_brands)
                brands_coverage = brands_found / len(test_brands)
                
                # Test models for key brands
                key_models_test = [
                    ("BMW", ["Série 1", "Série 3", "X1", "X3", "M3"]),
                    ("Mercedes", ["Classe A", "Classe C", "GLA", "GLC", "AMG GT"]),
                    ("Audi", ["A1", "A3", "Q2", "Q3", "RS3"]),
                    ("Peugeot", ["108", "208", "308", "2008", "3008"]),
                    ("Tesla", ["Model S", "Model 3", "Model X", "Model Y"])
                ]
                
                models_ok = True
                for brand, expected_models in key_models_test:
                    if brand in car_brands:
                        brand_models = car_brands[brand]
                        if not any(model in brand_models for model in expected_models):
                            models_ok = False
                            break
                
                success = has_90_plus and brands_coverage >= 0.8 and models_ok
                details = (f"Status: {response.status_code}, Brands: {brand_count} (90+: {has_90_plus}), "
                          f"Coverage: {brands_coverage:.1%} ({brands_found}/{len(test_brands)}), "
                          f"Models: {models_ok}")
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Comprehensive Car Brands (90+)", success, details)
        except Exception as e:
            return self.log_test("Comprehensive Car Brands (90+)", False, f"Error: {str(e)}")

    def cleanup_test_data(self):
        """Clean up created test data"""
        cleaned = 0
        for lead_id in self.created_lead_ids:
            try:
                response = requests.delete(f"{self.base_url}/leads/{lead_id}", 
                                         headers=self.headers, timeout=10)
                if response.status_code == 200:
                    cleaned += 1
            except:
                pass
        
        details = f"Cleaned {cleaned}/{len(self.created_lead_ids)} test leads"
        return self.log_test("Cleanup Test Data", cleaned == len(self.created_lead_ids), details)

    def run_all_tests(self):
        """Run all API tests in sequence - focusing on restored CRM features"""
        print("🚀 Starting CRM LEASINPROFESSIONNEL.FR API Tests (Restored Features)")
        print(f"🔗 Testing API at: {self.base_url}")
        print("=" * 70)

        # Test sequence focusing on restored features (priority order)
        test_methods = [
            # Core API
            self.test_api_root,
            
            # Priority 1: Configuration with 90+ car brands, commerciaux, prestataires
            self.test_get_config,
            self.test_comprehensive_car_brands,
            
            # Priority 2: Lead creation for PDF and reminder testing
            self.test_create_lead_single_vehicle,
            self.test_create_lead_multi_vehicle,
            self.test_get_leads,
            self.test_get_single_lead,
            
            # Priority 3: PDF Export Functionality
            self.test_pdf_export,
            
            # Priority 4: Reminder System Backend
            self.test_create_reminder,
            self.test_get_reminders,
            self.test_calendar_reminders,
            
            # Additional functionality tests
            self.test_update_lead_status,
            self.test_update_lead_note,
            self.test_search_leads,
            self.test_search_in_notes,
            self.test_filter_leads_by_commercial,
            self.test_filter_leads_by_status,
            self.test_dashboard_stats,
            self.test_specific_car_brands,
            
            # Activity tests (if endpoints exist)
            self.test_create_activity,
            self.test_get_lead_activities,
            
            # Cleanup
            self.cleanup_test_data
        ]

        for test_method in test_methods:
            test_method()
            print()  # Add spacing between tests

        # Final results
        print("=" * 70)
        print(f"📊 TEST RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! CRM LEASINPROFESSIONNEL.FR Backend is working correctly.")
            print("✅ Restored features verified:")
            print("   - PDF Export Functionality (/api/leads/{id}/pdf)")
            print("   - Reminder System (POST/GET /api/reminders, GET /api/calendar/reminders)")
            print("   - 90+ Car Brands and Models Configuration")
            print("   - Commercial and Prestataire Lists")
            print("   - Complete Configuration API Endpoint")
            return 0
        else:
            failed_count = self.tests_run - self.tests_passed
            print(f"⚠️  {failed_count} tests failed. Check the issues above.")
            
            # Identify critical failures
            critical_failures = []
            if self.tests_run > 0:
                print("\n🔍 CRITICAL ISSUES TO ADDRESS:")
                print("   - Check server logs for detailed error information")
                print("   - Verify all endpoints are properly implemented")
                print("   - Ensure PDF generation libraries are installed")
                print("   - Confirm reminder system database operations")
            
            return 1

def main():
    """Main test runner"""
    tester = CRMAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())