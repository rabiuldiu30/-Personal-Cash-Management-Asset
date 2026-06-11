from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import AddCash, Expense


class ManageCashTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'alex',
            'email': 'alex@example.com',
            'password': 'strong-pass-123',
            'confirm_password': 'strong-pass-123',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='alex').exists())

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_user_can_add_cash_and_expense(self):
        user = User.objects.create_user('sam', 'sam@example.com', 'pass12345')
        self.client.force_login(user)

        self.client.post(reverse('add_cash'), {
            'source': 'Salary',
            'amount': '5000.00',
            'datetime': '2026-06-10T10:00',
            'description': 'Monthly salary',
        })
        self.client.post(reverse('add_expense'), {
            'description': 'Rent',
            'amount': '1200.00',
            'datetime': '2026-06-10T11:00',
        })

        self.assertEqual(AddCash.objects.filter(user=user).count(), 1)
        self.assertEqual(Expense.objects.filter(user=user).count(), 1)
