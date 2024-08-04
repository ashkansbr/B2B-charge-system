from locust import HttpUser, TaskSet, task, between
from locust.contrib.fasthttp import FastHttpUser
import json

class TopUpTaskSet(TaskSet):
    def on_start(self):
        response = self.client.post("/", json={"username": "testuser", "password": "password"})
        if response.status_code != 200:
            print(f"Failed to login: {response.status_code} {response.text}")
        else:
            self.create_vendor_and_phone_number()

    def create_vendor_and_phone_number(self):
        user_response = self.client.get("/api/users/")
        if user_response.status_code != 200:
            print(f"Failed to get user: {user_response.status_code} {user_response.text}")
            return

        user_data = json.loads(user_response.text)
        if not user_data:
            print("No users found")
            return

        user_id = user_data[0]["id"]

        vendor_response = self.client.post("/api/vendors/", json={"user": user_id, "credit": 10000})
        if vendor_response.status_code != 201:
            print(f"Failed to create vendor: {vendor_response.status_code} {vendor_response.text}")
            return

        self.vendor_id = json.loads(vendor_response.text)["id"]

        phone_response = self.client.post("/api/users/phonenumbers/", json={"number": "1234567890", "total_amount_added": 0})
        if phone_response.status_code != 201:
            print(f"Failed to create phone number: {phone_response.status_code} {phone_response.text}")
            return

        self.phone_number_id = json.loads(phone_response.text)["id"]

    @task
    def top_up(self):
        if not hasattr(self, 'vendor_id') or not hasattr(self, 'phone_number_id'):
            print("Vendor or phone number not created")
            return

        response = self.client.post("/api/top_up/topups/", json={
            "vendor": self.vendor_id,
            "phone_number": "1234567890",
            "amount": 10
        })
        assert response.status_code == 201, "TopUp failed"


class TopUpUser(FastHttpUser):
    tasks = [TopUpTaskSet]
    wait_time = between(1, 2)
    host = "http://127.0.0.1:8000"

    def on_start(self):
        self.client.post("/api/users/users/", json={"username": "testuser", "email": "testuser@example.com", "password": "password"})
