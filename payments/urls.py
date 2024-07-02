from django.urls import path
from .views import GenerateScheduleView, UpdatePaymentView

urlpatterns = [
    path('schedule/', GenerateScheduleView.as_view(), name='generate_schedule'),
    path('payment/<int:payment_id>/', UpdatePaymentView.as_view(), name='update_payment'),
]
