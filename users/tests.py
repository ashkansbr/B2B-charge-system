import pytest
from django.contrib.auth import get_user_model
from users.models import Vendor

User = get_user_model()

@pytest.mark.django_db
class TestVendorCredit:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user1 = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='password')
        self.user2 = User.objects.create_user(username='vendor2', email='vendor2@example.com', password='password')

        self.vendor1 = Vendor.objects.create(user=self.user1, credit=0)
        self.vendor2 = Vendor.objects.create(user=self.user2, credit=0)

    def test_credit_increase_and_sales(self):

        for _ in range(10):
            self.vendor1.adjust_credit(100)
            self.vendor2.adjust_credit(100)

        for _ in range(10):
            self.vendor1.adjust_credit(-50)
            self.vendor2.adjust_credit(-50)

        self.vendor1.refresh_from_db()
        self.vendor2.refresh_from_db()

        assert self.vendor1.credit == 500
        assert self.vendor2.credit == 500

    def test_credit_after_transactions(self):

        self.vendor1.adjust_credit(500)
        self.vendor2.adjust_credit(1000)

        self.vendor1.adjust_credit(-200)
        self.vendor2.adjust_credit(-500)

        self.vendor1.refresh_from_db()
        self.vendor2.refresh_from_db()

        assert self.vendor1.credit == 300
        assert self.vendor2.credit == 500
