import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import Vendor, PhoneNumber
from top_up.models import TopUp

User = get_user_model()

@pytest.mark.django_db
def test_top_up():
    client = APIClient()

    # Create User and Vendor
    user = User.objects.create_user(username='testuser3', password='testpassword123')
    vendor = Vendor.objects.create(user=user, credit=1000.00)
    phone_number = PhoneNumber.objects.create(number='1234567890')

    client.force_authenticate(user=user)

    # TopUp
    top_up_data = {
        'vendor': vendor.id,
        'phone_number': phone_number.number,
        'amount': '200.00'
    }
    response = client.post('/api/top_up/topups/', top_up_data)
    assert response.status_code == 201

    # Check Credit and Phone Number Total Amount Added
    vendor.refresh_from_db()
    assert vendor.credit == 800.00
    phone_number.refresh_from_db()
    assert phone_number.total_amount_added == 200.00
