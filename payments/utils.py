import datetime
from decimal import Decimal
from typing import List, Dict

from dateutil.relativedelta import relativedelta
from typing import TYPE_CHECKING
from .models import Payment

if TYPE_CHECKING:
    from .models import Loan


def generate_payment_schedule(
    amount: Decimal,
    loan_start_date: datetime.date,
    number_of_payments: int,
    periodicity: str,
    interest_rate: Decimal
) -> List[Dict[str, Decimal]]:
    schedule: List = []
    period_delta = get_period_delta(periodicity)

    r: Decimal = interest_rate / 100
    l: float = get_period_length(periodicity)
    i: Decimal = r * Decimal(l)
    emi: Decimal = (i * amount) / (1 - (1 + i) ** -number_of_payments)

    balance: Decimal = amount
    for i in range(number_of_payments):
        interest: Decimal = balance * i
        principal: Decimal = emi - interest
        balance -= principal
        date = loan_start_date + period_delta * i
        schedule.append({
            'date': date,
            'principal': round(principal, 2),
            'interest': round(interest, 2)
        })

    return schedule


def get_period_delta(periodicity: str) -> datetime.timedelta | relativedelta:
    unit: str = periodicity[-1]
    quantity: int = int(periodicity[:-1])

    if unit == 'd':
        return datetime.timedelta(days=quantity)
    elif unit == 'w':
        return datetime.timedelta(weeks=quantity)
    elif unit == 'm':
        return relativedelta(months=quantity)


def get_period_length(periodicity: str) -> float:
    unit = periodicity[-1]
    quantity = int(periodicity[:-1])

    if unit == 'd':
        return quantity / 365
    elif unit == 'w':
        return quantity * 7 / 365
    elif unit == 'm':
        return quantity / 12


def recalculate_schedule(payments: List[Payment], new_principal: Decimal):
    loan: Loan = payments[0].loan
    r: Decimal = loan.interest_rate / 100
    l: float = get_period_length(loan.periodicity)
    i: Decimal = r * Decimal(l)
    emi: Decimal = (i * loan.amount) / (1 - (1 + i) ** -loan.number_of_payments)

    balance: Decimal = loan.amount - new_principal

    for payment in payments:
        interest: Decimal = balance * i
        principal: Decimal = emi - interest
        balance -= principal
        payment.principal = round(principal, 2)
        payment.interest = round(interest, 2)
        payment.save()
