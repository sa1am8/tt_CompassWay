from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import LoanSerializer, PaymentSerializer, UpdatePaymentSerializer
from .utils import generate_payment_schedule, recalculate_schedule


class GenerateScheduleView(APIView):
    def post(self, request):
        loan_serializer = LoanSerializer(data=request.data)
        if loan_serializer.is_valid():
            loan = loan_serializer.save()
            schedule = generate_payment_schedule(
                loan.amount,
                loan.loan_start_date,
                loan.number_of_payments,
                loan.periodicity,
                loan.interest_rate
            )
            for payment_data in schedule:
                Payment.objects.create(loan=loan, **payment_data)

            payment_serializer = PaymentSerializer(loan.payments.all(), many=True)
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePaymentView(APIView):
    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            new_principal = Decimal(serializer.validated_data['new_principal'])

            payment.principal = new_principal
            payment.save()

            remaining_payments = Payment.objects.filter(loan=payment.loan, date__gt=payment.date)
            recalculate_schedule(remaining_payments, new_principal)

            payment_serializer = PaymentSerializer(payment.loan.payments.all(), many=True)
            return Response(payment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)