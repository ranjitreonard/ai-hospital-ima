from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from apps.management.models import Patient, Revenue
from .models import *


@login_required()
def dashboard(request):
    return render(request=request, template_name='portal/dashboard.html')


class Bills(LoginRequiredMixin, ListView):
    template_name = 'portal/bills.html'
    queryset = Bill.objects.all()


# This view is to confirm patient card payment bills
class ConfirmPayment(LoginRequiredMixin, RedirectView):
    # url = reverse_lazy('portal:bills')

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('portal:patient-card', kwargs={'id': kwargs.get('patient_id')})

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')

        bill = Bill.objects.get(uuid=uuid)

        bill.status = 1

        bill.save()

        Revenue.objects.create(
            bill=bill,
            patient=bill.patient,
            amount=bill.amount,
            stream='Patient',
            description='Patient Card Payment',
            created_at=timezone.now(),
            created_by=request.user
        )

        return super(ConfirmPayment, self).get(self, request, *args, **kwargs)


class PatientCard(LoginRequiredMixin, DetailView):
    template_name = 'portal/patient_card.html'
    queryset = Patient.objects.all()
    model = Patient
    pk_url_kwarg = 'id'


# This view is for patient ward bills payment
class ConfirmDischarge(LoginRequiredMixin, RedirectView):
    # url = reverse_lazy('portal:bills')
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('portal:bill-details', kwargs={'uuid': kwargs.get('uuid')})

    def get(self, request, *args, **kwargs):
        bill_id = kwargs.get('uuid')

        bill = Bill.objects.get(uuid=bill_id)

        # bill.status = 1

        if bill.bill_type == 'WB':
            number_of_days = (timezone.now().date() - bill.patient.date_admitted).days
            bill_charge = DefaultBill.objects.get(bill_type='WB')
            amount_to_pay = (number_of_days if number_of_days > 0 else 1) * bill_charge.amount
            
            print(number_of_days)
            print(bill_charge)
            print(amount_to_pay)

            bill.amount = amount_to_pay
            bill.number_of_days = number_of_days if number_of_days > 0 else 1
            bill.patient.date_discharged = timezone.now().date()
            bill.patient.time_discharged = timezone.now().time()
            bill.patient.bed.allocate.date_discharged = timezone.now().date()
            bill.patient.bed.allocate.time_discharged = timezone.now().time()
            bill.patient.bed.status = 'Unassigned'
            bill.patient.bed.allocate.save()
            bill.patient.bed.allocate = None
            bill.patient.bed.save()
            bill.patient.bed = None
            bill.patient.save()

        bill.status = 1
        bill.save()

        Revenue.objects.create(
            bill=bill,
            patient=bill.patient,
            amount=bill.amount,
            stream='Patient',
            description='Patient Ward Bill Payment',
            created_at=timezone.now(),
            created_by=request.user
        )
        
        return super(ConfirmDischarge, self).get(self, request, *args, **kwargs)


@login_required()
def bill_details(request, uuid):
    bill = Bill.objects.get(uuid=uuid)
    bill_charge = None
    numbers_of_days = 0
    days_spent = 0
    amount_paid = 0
    amount = 0
    amount_per_day = 0

    date_to_be_discharged = timezone.now().date()
    try:
        bill_charge = DefaultBill.objects.get(bill_type=bill.bill_type)
        numbers_of_days = (timezone.now().date() - bill.patient.date_admitted).days
        amount = (numbers_of_days if numbers_of_days > 0 else 1) * bill_charge.amount
        amount_per_day = bill_charge.amount
        if bill.status == 1:
            days_spent = (bill.patient.date_discharged - bill.patient.date_admitted).days
            amount_paid = days_spent * bill_charge.amount
    except:
        pass
    context = {
        'object': bill,
        'date_to_be_discharged': date_to_be_discharged,
        'number_of_days': numbers_of_days,
        'total_amount': amount,
        'amount_per_day': amount_per_day,
        'days_spent': days_spent,
        'amount_paid': amount_paid,
    }

    return render(request, template_name='portal/bill_details.html', context=context)


# This view is to confirm patient prescription payment
class ConfirmPrescriptionBill(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('portal:bill-details', kwargs={'uuid': kwargs.get('uuid')})

    def get(self, request, *args, **kwargs):
        bill = Bill.objects.get(uuid=kwargs.get('uuid'))

        bill.prescription.is_paid = True

        bill.status = 1

        bill.prescription.save()
        bill.save()

        Revenue.objects.create(
            bill=bill,
            patient=bill.patient,
            amount=bill.amount,
            stream='Patient',
            description='Patient Prescription Payment',
            created_at=timezone.now(),
            created_by=request.user
        )

        return super(ConfirmPrescriptionBill, self).get(self, request, *args, **kwargs)
