from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Loan, Payment


class PaymentScheduleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.loan_data = {
            'amount': 1000,
            'loan_start_date': '2024-01-10',
            'number_of_payments': 4,
            'periodicity': '1m',
            'interest_rate': 10.0
        }

    def test_generate_schedule(self):
        response = self.client.post('/api/schedule/', self.loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), self.loan_data['number_of_payments'])

        first_payment = response.data[0]
        self.assertIn('id', first_payment)
        self.assertIn('date', first_payment)
        self.assertIn('principal', first_payment)
        self.assertIn('interest', first_payment)

    def test_invalid_data(self):
        invalid_loan_data = {
            'amount': 'invalid',
            'loan_start_date': 'invalid',
            'number_of_payments': 'invalid',
            'periodicity': 'invalid',
            'interest_rate': 'invalid'
        }
        response = self.client.post('/api/schedule/', invalid_loan_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.loan = Loan.objects.create(
            amount=1000,
            loan_start_date='2024-01-10',
            number_of_payments=4,
            periodicity='1m',
            interest_rate=10.0
        )
        self.payments = [
            Payment.objects.create(loan=self.loan, date='2024-02-10', principal=240, interest=10),
            Payment.objects.create(loan=self.loan, date='2024-03-10', principal=240, interest=8),
            Payment.objects.create(loan=self.loan, date='2024-04-10', principal=240, interest=6),
            Payment.objects.create(loan=self.loan, date='2024-05-10', principal=240, interest=4),
        ]
        self.payment_id = self.payments[1].id

    def test_update_payment(self):
        response = self.client.post(f'/api/payment/{self.payment_id}/', {'new_principal': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_payment = Payment.objects.get(id=self.payment_id)
        self.assertEqual(updated_payment.principal, 100)

        remaining_payments = Payment.objects.filter(loan=self.loan, date__gt=updated_payment.date)
        for payment in remaining_payments:
            self.assertNotEqual(payment.interest, 0)

    def test_update_invalid_payment(self):
        response = self.client.post('/api/payment/9999/', {'new_principal': 50})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_data(self):
        response = self.client.post(f'/api/payment/{self.payment_id}/', {'new_principal': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
