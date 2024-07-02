from rest_framework import serializers
from .models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UpdatePaymentSerializer(serializers.Serializer):
    new_principal = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_new_principal(self, value):
        if value <= 0:
            raise serializers.ValidationError("The new principal must be greater than zero.")
        return value