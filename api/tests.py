from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import InvestmentFund
from datetime import date

class InvestmentFundAPITest(TestCase):
    """Test suite for the investment fund API."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = APIClient()
        self.fund_data = {
            "fund_id": 1,  # Using fund_id instead of id
            "fund_manager": "John Doe",
            "fund_name": "Test Fund",
            "fund_description": "This is a test fund.",
            "fund_nav": 100.5,
            "fund_creation_date": date(2023, 1, 1),
            "fund_performance": 5.2
        }
        self.fund = InvestmentFund.objects.create(**self.fund_data)

    # ✅ Test Retrieve All Funds
    def test_retrieve_all_funds(self):
        response = self.client.get("/api/list-funds/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_funds", response.data)
        self.assertIn("funds", response.data)

    # # ✅ Test Retrieve Specific Fund
    def test_retrieve_specific_fund(self):
        response = self.client.get(f"/api/get-funds/{self.fund.fund_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["fund_id"], self.fund.fund_id)

    # ✅ Test Create Fund
    def test_create_fund(self):
        new_fund_data = {
            "fund_manager": "Jane Doe",
            "fund_name": "New Test Fund",
            "fund_description": "This is another test fund.",
            "fund_nav": 150.75,
            "fund_creation_date": "2024-01-01",
            "fund_performance": 7.8
        }
        response = self.client.post("/api/create-funds/", new_fund_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["fund"]["fund_name"], "New Test Fund")

    # # ✅ Test Update Fund Performance
    def test_update_fund_performance(self):
        update_data = {"fund_performance": 10.5}
        response = self.client.post(f"/api/update-performance/{self.fund.fund_id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["fund"]["fund_performance"], 10.5)

    # ✅ Test Delete Fund
    def test_delete_fund(self):
        response = self.client.post(f"/api/delete-fund/{self.fund.fund_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Investment fund deleted successfully!")

        # Ensure fund is actually deleted
        response = self.client.get(f"/api/get-funds/{self.fund.fund_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
