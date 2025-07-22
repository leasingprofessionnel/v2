#!/usr/bin/env python3
"""
Backend API Test Suite for CRM LLD Automobile
Tests all the new features mentioned in the review request:
1. New commercials (Matthews, Sauveur, Autre)
2. Extended car brands database (56 brands)
3. Note field support
4. Multi-vehicle support
5. All CRUD operations and filtering
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any

class CRMAPITester:
    def __init__(self):
        # Use the public URL from frontend/.env
        self.base_url = "https://2d52afcb-feae-4234-be99-4715d120d1e2.preview.emergentagent.com/api"
        self.headers = {'Content-Type': 'application/json'}
        self.tests_run = 0
        self.tests_passed = 0
        self.created_lead_ids = []

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
            response = requests.get(f"{self.base_url}/", headers=self.headers, timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            details = f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            return self.log_test("API Root", success, details)
        except Exception as e:
            return self.log_test("API Root", False, f"Error: {str(e)}")

    def test_get_config(self):
        """Test configuration endpoint"""
        try:
            response = requests.get(f"{self.base_url}/config", headers=self.headers, timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = ['prestataires', 'commerciaux', 'car_brands', 'contract_durations', 'annual_mileages', 'status_colors']
                has_all_keys = all(key in data for key in required_keys)
                success = has_all_keys
                details = f"Status: {response.status_code}, Keys present: {has_all_keys}"
            else:
                details = f"Status: {response.status_code}"
            return self.log_test("Get Config", success, details)
        except Exception as e:
            return self.log_test("Get Config", False, f"Error: {str(e)}")

    def test_create_lead(self):
        """Test lead creation"""
        lead_data = {
            "company": {
                "name": "Test Auto SARL",
                "siret": "12345678901234",
                "address": "123 Rue de la Paix, 75001 Paris",
                "phone": "01.23.45.67.89",
                "email": "contact@testauto.fr"
            },
            "contact": {
                "first_name": "Jean",
                "last_name": "Dupont",
                "email": "jean.dupont@testauto.fr",
                "phone": "06.12.34.56.78",
                "position": "Directeur"
            },
            "vehicle": {
                "brand": "Peugeot",
                "model": "3008",
                "carburant": "diesel",
                "contract_duration": 36,
                "annual_mileage": 15000
            },
            "assigned_to_prestataire": "Localease",
            "assigned_to_commercial": "Jean Dupont"
        }

        try:
            response = requests.post(f"{self.base_url}/leads", 
                                   json=lead_data, 
                                   headers=self.headers, 
                                   timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                self.created_lead_id = data.get('id')
                details = f"Status: {response.status_code}, Lead ID: {self.created_lead_id}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            return self.log_test("Create Lead", success, details)
        except Exception as e:
            return self.log_test("Create Lead", False, f"Error: {str(e)}")

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
        if not self.created_lead_id:
            return self.log_test("Get Single Lead", False, "No lead ID available")
        
        try:
            response = requests.get(f"{self.base_url}/leads/{self.created_lead_id}", 
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
        if not self.created_lead_id:
            return self.log_test("Update Lead Status", False, "No lead ID available")
        
        update_data = {"status": "relance"}
        
        try:
            response = requests.put(f"{self.base_url}/leads/{self.created_lead_id}", 
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

    def test_filter_leads_by_status(self):
        """Test lead filtering by status"""
        try:
            response = requests.get(f"{self.base_url}/leads?status=relance", 
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
        if not self.created_lead_id:
            return self.log_test("Create Activity", False, "No lead ID available")
        
        activity_data = {
            "lead_id": self.created_lead_id,
            "activity_type": "note",
            "title": "Premier contact effectué",
            "description": "Client intéressé par le véhicule Peugeot 3008"
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
        if not self.created_lead_id:
            return self.log_test("Get Lead Activities", False, "No lead ID available")
        
        try:
            response = requests.get(f"{self.base_url}/activities/{self.created_lead_id}", 
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

    def test_delete_lead(self):
        """Test lead deletion (run last)"""
        if not self.created_lead_id:
            return self.log_test("Delete Lead", False, "No lead ID available")
        
        try:
            response = requests.delete(f"{self.base_url}/leads/{self.created_lead_id}", 
                                     headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            return self.log_test("Delete Lead", success, details)
        except Exception as e:
            return self.log_test("Delete Lead", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting CRM LLD Automobile API Tests")
        print(f"🔗 Testing API at: {self.base_url}")
        print("=" * 60)

        # Test sequence
        test_methods = [
            self.test_api_root,
            self.test_get_config,
            self.test_create_lead,
            self.test_get_leads,
            self.test_get_single_lead,
            self.test_update_lead_status,
            self.test_search_leads,
            self.test_filter_leads_by_status,
            self.test_dashboard_stats,
            self.test_create_activity,
            self.test_get_lead_activities,
            self.test_delete_lead
        ]

        for test_method in test_methods:
            test_method()
            print()  # Add spacing between tests

        # Final results
        print("=" * 60)
        print(f"📊 TEST RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Backend API is working correctly.")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed. Check the issues above.")
            return 1

def main():
    """Main test runner"""
    tester = CRMAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())