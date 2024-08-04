import pytest
from users.models import Vendor, CustomUser
from credit_management.models import CreditRequest, TransactionLog

@pytest.mark.django_db
class TestCreditRequest:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = CustomUser.objects.create_user(username='vendor1', email='vendor1@example.com', password='password')
        self.vendor = Vendor.objects.create(user=self.user, credit=500)

    def test_credit_request_approval(self):
        credit_request = CreditRequest.objects.create(vendor=self.vendor, amount=500)

        credit_request.approve()

        self.vendor.refresh_from_db()
        credit_request.refresh_from_db()

        assert credit_request.is_approved
        assert credit_request.approved_at is not None
        assert self.vendor.credit == 1000
