import datetime
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import *

from apps.department.models import Note
from apps.portal.models import Bill, DefaultBill
from . import forms

# Create your views here.
from apps.management.models import Patient, MedicalDiagnosis, Treatment, Ward, Bed, BedAllocate, VitalSign


@login_required()
def dashboard(request):
    return render(request=request, template_name='department/dashboard.html')


class NewPatient(LoginRequiredMixin, CreateView):
    template_name = 'department/new_patient.html'
    form_class = forms.NewPatientForm
    queryset = Patient.objects.all()
    success_url = reverse_lazy('department:patients')

    def form_valid(self, form):
        valid = super(NewPatient, self).form_valid(form)

        form.instance.created_by = self.request.user
        # try:
        card_charge = DefaultBill.objects.get(bill_type='CB')
        # except DefaultBill.DoesNotExist:
        #     raise ValidationError(
        #         message='There is no card bills in the system'
        #     )

        Bill.objects.create(
            patient=form.instance,
            bill_type='CB',
            amount=card_charge.amount,
            status=0,
            created_by=self.request.user
        )

        form.save()

        return valid


class Patients(LoginRequiredMixin, ListView):
    template_name = 'department/patients.html'
    queryset = Patient.objects.all()
    model = Patient


class PatientDetails(LoginRequiredMixin, DetailView):
    template_name = 'department/patient_details.html'
    model = Patient
    queryset = Patient.objects.all()
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(PatientDetails, self).get_context_data(**kwargs)
        context['age'] = round((timezone.now().date() - self.object.date_of_birth).days / 365)
        return context


@login_required()
def vital_signs(request, id):
    patient = Patient.objects.get(id=id)
    weight = request.POST.get('weight')
    sys = request.POST.get('sys')
    dias = request.POST.get('dias')
    respiration = request.POST.get('respiration')
    temperature = request.POST.get('temperature')
    pulse = request.POST.get('pulse')

    bp = sys + ' / ' + dias
    if request.method == 'POST':
        nvs = VitalSign.objects.create(
            patient=patient,
            diastolic=dias,
            systolic=sys,
            weight=weight,
            respiration=respiration,
            pulse=pulse,
            temperature=temperature,
            created_by=request.user,
        )

        patient.vital_signs.add(nvs)
        patient.weight = weight + ' kg'
        patient.bp = bp + ' mmHg'
        patient.respiration = respiration + ' cpm'
        patient.temperature = temperature + ' °C'
        patient.patient_type = 'OPD'

        patient.save()

    return HttpResponseRedirect(reverse_lazy('department:patient-details', kwargs={'id': patient.id}))


class VitalSigns(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs.get('id'))
        weight = request.POST.get('weight')
        sys = request.POST.get('sys')
        dias = request.POST.get('dias')
        respiration = request.POST.get('respiration')
        temperature = request.POST.get('temperature')

        bp = sys + ' / ' + dias

        patient.weight = weight + ' kg'
        patient.bp = bp + ' mmHg'
        patient.respiration = respiration + ' cpm'
        patient.temperature = temperature + ' °C'
        patient.patient_type = 'OPD'

        patient.save()

        return super(VitalSigns, self).post(self, request, *args, **kwargs)


@login_required()
def vital_sign_chart(request, id):

    patient = Patient.objects.get(id=id)

    today = datetime.datetime.strptime(request.GET.get('today'), '%d-%m-%Y') if request.GET.get('today') else timezone.now().date()

    ndate = today + timedelta(days=1)

    pdate = today - timedelta(days=1)

    ndate = datetime.datetime.strftime(ndate, '%d-%m-%Y')

    pdate = datetime.datetime.strftime(pdate, '%d-%m-%Y')

    day = today.day
    month = today.month
    year = today.year

    patient_vs_today = patient.vital_signs.filter(created_at__day=day, created_at__month=month, created_at__year=year).order_by('time')

    labels = [str(x.time.strftime('%H:%M')) for x in patient_vs_today.all()]

    temp_data = [str(x.temperature) for x in patient_vs_today.all()]

    res_data = [str(x.respiration) for x in patient_vs_today.all()]

    pulse_data = []
    for x in patient_vs_today.all():
        pulse_data.append(str(x.pulse))

    dias_data = [str(x.diastolic) for x in patient_vs_today.all()]

    sys_data = [str(x.systolic) for x in patient_vs_today.all()]

    print(json.dumps(temp_data))

    context = {
        'object': patient,
        'pdate': pdate,
        'ndate': ndate,
        'vital_signs': patient_vs_today,
        'labels': json.dumps(labels),
        'dias': json.dumps(dias_data),
        'sys': json.dumps(sys_data),
        'temp': json.dumps(temp_data),
        'res': json.dumps(res_data),
        'pulse': json.dumps(pulse_data),
        'today': today,
    }

    return render(request, template_name='department/vital_signs.html', context=context)


class OPDPatients(LoginRequiredMixin, ListView):
    template_name = 'department/opd.html'
    queryset = Patient.objects.filter(patient_type='OPD')
    model = Patient


class PatientDiagnosis(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs.get('id'))
        complaints = request.POST.get('complaints')
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        is_admitted = request.POST.get('is_admitted')
        onset = request.POST.get('onset')
        treatment = request.POST.get('treatment')
        prescription = request.POST.get('prescription')

        if is_admitted == "True":
            admitted = True
        else:
            admitted = False

        md = MedicalDiagnosis.objects.create(
            patient=patient,
            complaints=complaints,
            symptoms=symptoms,
            diagnosis=diagnosis,
            is_admitted=admitted,
            onset=onset,
            created_by=self.request.user
        )

        tmt = Treatment.objects.create(
            diagnosis=md,
            treatment=treatment,
            status='Pending',
            created_by=self.request.user,
            prescription=prescription
        )

        md.treatments.add(tmt)

        if admitted:
            patient.patient_type = 'Ward'

        patient.diagnoses.add(md)

        md.save()
        patient.save()

        return super(PatientDiagnosis, self).post(self, request, *args, **kwargs)


@login_required()
def notes(request, id):
    patient = Patient.objects.get(id=id)

    note = request.POST.get('note')

    if request.method == 'POST':
        my_note = Note.objects.create(
            note=note,
            patient=patient,
            created_by=request.user
        )

        patient.notes.add(my_note)

        patient.save()

    return HttpResponseRedirect(reverse_lazy('department:patient-details', kwargs={'id': id}))


@login_required()
def add_treatment(request, diagnosis_id, patient_id):
    diagnosis = MedicalDiagnosis.objects.get(id=diagnosis_id)
    patient = Patient.objects.get(id=patient_id)
    treatment = request.POST.get('treatment')
    prescription = request.POST.get('prescription')

    my_treatment = Treatment.objects.create(
        diagnosis=diagnosis,
        treatment=treatment,
        prescription=prescription,
        status='Pending',
        created_by=request.user
    )

    diagnosis.treatments.add(my_treatment)

    diagnosis.save()

    return redirect(reverse_lazy('department:patient-details', kwargs={'id': patient.id}))


@login_required()
def complete_treatment(request, treatment_id, patient_id):
    treatment = Treatment.objects.get(id=treatment_id)
    patient = Patient.objects.get(id=patient_id)
    time_completed = request.POST.get('time_completed')
    date_completed = request.POST.get('date_completed')

    treatment.time_treated = time_completed
    treatment.date_treated = date_completed
    treatment.status = 'Completed'

    treatment.save()

    return redirect(reverse_lazy('department:patient-details', kwargs={'id': patient.id}))


class CancelTreatment(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('patient_id')})
    
    def get(self, request, *args, **kwargs):
        treatment = Treatment.objects.get(id=kwargs.get('treatment_id'))
        
        if treatment.status == 'Pending':
            treatment.status = 'Canceled'
            
        treatment.save()
        
        return super(CancelTreatment, self).get(self, request, *args, **kwargs)


class Wards(LoginRequiredMixin, ListView):
    template_name = 'department/wards.html'
    queryset = Ward.objects.all()
    model = Ward


class WardDetails(LoginRequiredMixin, DetailView):
    template_name = 'department/ward_details.html'
    queryset = Ward.objects.all()
    model = Ward
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(WardDetails, self).get_context_data(**kwargs)

        context['patients'] = Patient.objects.filter(patient_type='Ward')

        return context



@login_required()
def ward_details(request, id):
    object = Ward.objects.get(id=id)
    patients = Patient.objects.filter(patient_type='Ward')
    error = ''

    context = {
        'object': object,
        'patients': patients,
        'error': error
    }

    if request.method == 'POST':
        bed = Bed.objects.get(id=request.POST.get('bed_id'))
        patient = Patient.objects.get(id=request.POST.get('patient_id'))
        admitted_at = request.POST.get('admitted_at')
        time_admitted = request.POST.get('time_admitted')

        if patient.bed:
            context['error'] = patient.full_name() + ' has already been allocated to bed number ' + patient.bed.number + ' in ' + patient.bed.ward.label
            return render(request, template_name='department/ward_details.html', context=context)

        if bed.status == 'Assigned':
            context['error'] = 'Bed has already been assigned to ' + bed.allocate.patient.full_name()
            return render(request, 'department/ward_details.html', context=context)
        else:
            bed.status = 'Assigned'

        allocate = BedAllocate.objects.create(
            bed=bed,
            patient=patient,
            created_by=request.user,
            date_admitted=admitted_at,
            time_admitted=time_admitted,
        )

        bed.allocate = allocate
        bed.bed_allocates.add(allocate)
        patient.date_admitted = admitted_at
        patient.time_admitted = time_admitted
        patient.bed = bed
        bed.save()
        patient.save()

        return redirect(reverse_lazy('department:ward-details', kwargs={'id': id}))

    return render(request, 'department/ward_details.html', context=context)



@login_required()
def allocate_bed(request, bed_id):
    bed = Bed.objects.get(id=bed_id)
    patient = Patient.objects.get(id=request.POST.get('patient_id'))
    admitted_at = request.POST.get('admitted_at')
    time_admitted = request.POST.get('time_admitted')

    if patient.bed:
        context = {'error': patient.full_name() + ' has already been allocated to bed number ' + patient.bed.number}
        return render(request, template_name='department/ward_details.html', context=context)

    if bed.status == 'Assigned':
        context = {
            'error': 'Bed has already been assigned to ' + bed.allocate.patient.full_name()
        }
        return render(request, 'department/ward_details.html', context=context)
    else:
        bed.status = 'Assigned'

    allocate = BedAllocate.objects.create(
        bed=bed,
        patient=patient,
        created_by=request.user,
        date_admitted=admitted_at,
        time_admitted=time_admitted,
    )

    bed.allocate = allocate
    bed.bed_allocates.add(allocate)
    patient.date_admitted = admitted_at
    patient.time_admitted = time_admitted
    patient.bed = bed
    bed.save()
    patient.save()

    return redirect(reverse_lazy('department:ward-details', kwargs={'id': bed.ward.id}))


class DischargePatient(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('id')})

    def get(self, request, *args, **kwargs):
        patient_id = kwargs.get('id')
        patient = Patient.objects.get(id=patient_id)


        bill_charge = DefaultBill.objects.get(bill_type='CnB')
        Bill.objects.create(
            patient=patient,
            bill_type='WB' if patient.patient_type == 'Ward' else 'CnB',
            amount=bill_charge.amount if patient.patient_type == 'OPD' else None,
            status=0,
            created_by=self.request.user
        )
        patient.patient_type = 'Discharged'
        patient.save()

        return super(DischargePatient, self).get(self, request, *args, **kwargs)