import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *

from apps.pharmacy.models import Medicine
from apps.portal.models import DefaultBill
from apps.staff.models import *
from .models import *
from apps.management.forms import UserForm, LeavePeriodForm, RevenueForm
from apps.user.models import User


@login_required()
def dashboard(request):
    wards = Ward.objects.count()
    beds = Bed.objects.count()

    staffs = User.objects.count()

    current_year = 2020
    years = [(current_year + year, current_year + year) for year in range(51)]

    # for year in range(51):
    #     years.append((current_year + year, current_year + year))

    active_staffs = User.objects.filter(status='Active').count()
    inactive_staffs = User.objects.exclude(status='Active').count()

    year = int(request.GET.get('year')) if request.GET.get('year')else current_year

    exps = Expenditure.objects.filter(created_at__year=year)
    total_exp = 0

    for exp in exps.all():
        total_exp += exp.cost

    revs = Revenue.objects.filter(created_at__year=year)

    total_rev = 0

    for rev in revs.all():
        total_rev += rev.amount

    jan_rev = Revenue.objects.filter(created_at__year=year, created_at__month=1)
    jan_rev_amount = 0
    for rev in jan_rev.all():
        jan_rev_amount += rev.amount

    feb_rev = Revenue.objects.filter(created_at__year=year, created_at__month=2)
    feb_rev_amount = 0
    for rev in feb_rev.all():
        feb_rev_amount += rev.amount

    mar_rev = Revenue.objects.filter(created_at__year=year, created_at__month=3)
    mar_rev_amount = 0
    for rev in mar_rev.all():
        mar_rev_amount += rev.amount

    apr_rev = Revenue.objects.filter(created_at__year=year, created_at__month=4)
    apr_rev_amount = 0
    for rev in apr_rev.all():
        apr_rev_amount += rev.amount

    may_rev = Revenue.objects.filter(created_at__year=year, created_at__month=5)
    may_rev_amount = 0
    for rev in may_rev.all():
        may_rev_amount += rev.amount

    june_rev = Revenue.objects.filter(created_at__year=year, created_at__month=6)
    june_rev_amount = 0
    for rev in june_rev.all():
        june_rev_amount += rev.amount

    july_rev = Revenue.objects.filter(created_at__year=year, created_at__month=7)
    july_rev_amount = 0
    for rev in july_rev.all():
        july_rev_amount += rev.amount

    aug_rev = Revenue.objects.filter(created_at__year=year, created_at__month=8)
    aug_rev_amount = 0
    for rev in aug_rev.all():
        aug_rev_amount += rev.amount

    sept_rev = Revenue.objects.filter(created_at__year=year, created_at__month=9)
    sept_rev_amount = 0
    for rev in sept_rev.all():
        sept_rev_amount += rev.amount

    oct_rev = Revenue.objects.filter(created_at__year=year, created_at__month=10)
    oct_rev_amount = 0
    for rev in oct_rev.all():
        oct_rev_amount += rev.amount

    nov_rev = Revenue.objects.filter(created_at__year=year, created_at__month=11)
    nov_rev_amount = 0
    for rev in nov_rev.all():
        nov_rev_amount += rev.amount

    dec_rev = Revenue.objects.filter(created_at__year=year, created_at__month=12)
    dec_rev_amount = 0
    for rev in dec_rev.all():
        dec_rev_amount += rev.amount

    revenue = {
        'jan': jan_rev_amount,
        'feb': feb_rev_amount,
        'mar': mar_rev_amount,
        'apr': apr_rev_amount,
        'may': mar_rev_amount,
        'june': june_rev_amount,
        'july': july_rev_amount,
        'aug': aug_rev_amount,
        'sept': sept_rev_amount,
        'oct': oct_rev_amount,
        'nov': nov_rev_amount,
        'dec': dec_rev_amount,
    }

    jan_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=1)
    jan_exp_amount = 0
    for rev in jan_exp.all():
        jan_exp_amount += rev.cost

    feb_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=2)
    feb_exp_amount = 0
    for exp in feb_exp.all():
        feb_exp_amount += exp.cost

    mar_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=3)
    mar_exp_amount = 0
    for exp in mar_exp.all():
        mar_exp_amount += exp.cost

    apr_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=4)
    apr_exp_amount = 0
    for exp in apr_exp.all():
        apr_exp_amount += exp.cost

    may_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=5)
    may_exp_amount = 0
    for exp in may_exp.all():
        may_exp_amount += exp.cost

    june_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=6)
    june_exp_amount = 0
    for exp in june_exp.all():
        june_exp_amount += exp.cost

    july_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=7)
    july_exp_amount = 0
    for exp in july_exp.all():
        july_exp_amount += exp.cost

    aug_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=8)
    aug_exp_amount = 0
    for exp in aug_exp.all():
        aug_exp_amount += exp.cost

    sept_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=9)
    sept_exp_amount = 0
    for exp in sept_exp.all():
        sept_exp_amount += exp.cost

    oct_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=10)
    oct_exp_amount = 0
    for exp in oct_exp.all():
        oct_exp_amount += exp.cost

    nov_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=11)
    nov_exp_amount = 0
    for exp in nov_exp.all():
        nov_exp_amount += exp.cost

    dec_exp = Expenditure.objects.filter(created_at__year=year, created_at__month=12)
    dec_exp_amount = 0
    for exp in dec_exp.all():
        dec_exp_amount += exp.cost

    expenditure = {
        'jan': jan_exp_amount,
        'feb': feb_exp_amount,
        'mar': mar_exp_amount,
        'apr': apr_exp_amount,
        'may': mar_exp_amount,
        'june': june_exp_amount,
        'july': july_exp_amount,
        'aug': aug_exp_amount,
        'sept': sept_exp_amount,
        'oct': oct_exp_amount,
        'nov': nov_exp_amount,
        'dec': dec_exp_amount,
    }

    patients = {
        'jan':Patient.objects.filter(created_at__year=year, created_at__month=1).count(),
        'feb': Patient.objects.filter(created_at__year=year, created_at__month=2).count(),
        'mar': Patient.objects.filter(created_at__year=year, created_at__month=3).count(),
        'apr': Patient.objects.filter(created_at__year=year, created_at__month=4).count(),
        'may': Patient.objects.filter(created_at__year=year, created_at__month=5).count(),
        'june': Patient.objects.filter(created_at__year=year, created_at__month=6).count(),
        'july': Patient.objects.filter(created_at__year=year, created_at__month=7).count(),
        'aug': Patient.objects.filter(created_at__year=year, created_at__month=8).count(),
        'sept': Patient.objects.filter(created_at__year=year, created_at__month=9).count(),
        'oct': Patient.objects.filter(created_at__year=year, created_at__month=10).count(),
        'nov': Patient.objects.filter(created_at__year=year, created_at__month=11).count(),
        'dec': Patient.objects.filter(created_at__year=year, created_at__month=12).count(),


    }

    context = {
        'wards': wards,
        'beds': beds,
        'expenditure': total_exp,
        'revenue': total_rev,
        'staff': staffs,
        'active': active_staffs,
        'inactive': inactive_staffs,
        'years': years,
        'current_year': year,
        'rev_line': revenue,
        'exp_line': expenditure,
        'patient_line': patients,
        'revs_for_year' : revs,
        'exps_for_year': exps,
    }
    return render(request=request, template_name='management/dashboard.html', context=context)


@login_required()
def staff_list(request):
    staff = User.objects.all()

    context = {
        'object_list': staff
    }

    return render(request=request, template_name='management/staff_list.html', context=context)


class AddStaff(LoginRequiredMixin, CreateView):
    template_name = 'management/staff_new.html'
    form_class = UserForm
    success_url = reverse_lazy('management:staff')
    queryset = User.objects.all()

    def form_valid(self, form):
        valid = super(AddStaff, self).form_valid(form)

        form.instance.set_password(form.instance.password)

        form.save()

        return valid


class StaffDetails(LoginRequiredMixin, DetailView):
    template_name = 'management/staff_details.html'
    model = User
    queryset = User.objects.all()
    pk_url_kwarg = 'id'


class ManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'management/wards.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerView, self).get_context_data(**kwargs)
        context['wards'] = Ward.objects.all()
        context['beds'] = Bed.objects.all().order_by('-ward__label', 'number')
        context['patients'] = Patient.objects.all()
        context['bills'] = DefaultBill.objects.all()
        context['requests'] = Request.objects.all()
        return context


class AddWard(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        label = request.POST.get('label')

        Ward.objects.create(
            label=label,
            created_by=self.request.user
        )

        return super(AddWard, self).post(self, request, *args, **kwargs)


@login_required()
def ward_details(request, id):
    ward = Ward.objects.get(id=id)
    bed_number = request.POST.get('bed')

    errors = ''

    context = {
        'object': ward,
        'errors': errors
    }

    if request.method == 'POST':
        try:
            Bed.objects.get(number__iexact=bed_number, ward=ward)
            errors = 'Bed has already been added'
            context = {
                'object': ward,
                'errors': errors
            }
            return render(request=request, template_name='management/ward_details.html', context=context)
        except Bed.DoesNotExist:
            new_bed = Bed.objects.create(
                number=bed_number,
                ward=ward,
                status='Unassigned',
                created_by=request.user
            )
            ward.beds.add(new_bed)

            ward.save()
            return HttpResponseRedirect(reverse_lazy('management:ward-details', kwargs={'id': ward.id}))

    return render(request=request, template_name='management/ward_details.html', context=context)


class AddBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_type = request.POST.get('bill_type')
        service = request.POST.get('service')
        amount = request.POST.get('amount')

        new_default_bill = DefaultBill.objects.create(
            bill_type=bill_type,
            service=service if service else '',
            amount=amount,
            created_by=self.request.user
        )

        return super(AddBill, self).post(self, request, *args, **kwargs)


class DeleteBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_id = kwargs.get('bill_id')

        bill = DefaultBill.objects.get(id=bill_id)

        bill.delete()

        return super(DeleteBill, self).post(self, request, *args, **kwargs)


class UpdateBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_id = kwargs.get('bill_id')
        amount = request.POST.get('amount')
        service = request.POST.get('service')
        bill_type = request.POST.get('bill_type')

        bill = DefaultBill.objects.get(id=bill_id)

        bill.amount = amount
        bill.service = service
        bill.bill_type = bill_type

        bill.save()

        return super(UpdateBill, self).post(self, request, *args, **kwargs)


@login_required()
def hr(request):
    all_complaint = Complaint.objects.all().exclude(status=2)
    leave_periods = LeavePeriod.objects.all()

    context = {
        'complaints': all_complaint,
        'leave_periods': leave_periods
    }

    return render(request, template_name='management/hr.html', context=context)


class LeavePeriodDetails(LoginRequiredMixin, DetailView):
    template_name = 'management/leave_period_details.html'
    queryset = LeavePeriod.objects.all()
    model = LeavePeriod
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(LeavePeriodDetails, self).get_context_data(**kwargs)
        context['leaves'] = Leave.objects.all()
        return context


@login_required()
def complaint_details(request, id):
    complaint = Complaint.objects.get(id=id)

    if not complaint.is_seen:
        complaint.is_seen = True
        complaint.seen_at = timezone.now()
        complaint.seen_by = request.user
        complaint.save()

    context = {
        'object': complaint,
    }

    if request.method == 'POST':
        review = request.POST.get('review')
        complaint.review = review
        complaint.review_by = request.user
        complaint.review_at = timezone.now()
        complaint.status = 1
        complaint.save()

    return render(request, template_name='management/complaint_details.html', context=context)


class MakeRequest(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        department = request.POST.get('department')
        description = request.POST.get('description')

        Request.objects.create(
            department=department,
            description=description,
            status=0,
            created_by=self.request.user
        )

        return super(MakeRequest, self).post(self, request, *args, **kwargs)


class Requests(LoginRequiredMixin, ListView):
    template_name = 'management/requests.html'
    queryset = Request.objects.all()
    model = Request


class ChangeRequestStatus(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:requests')

    def get(self, request, *args, **kwargs):
        # status_type = kwargs.get('type')
        request_id = kwargs.get('request_id')

        my_request = Request.objects.get(id=request_id)

        if my_request.status == 0:
            my_request.status = 1
            my_request.save()

        return super(ChangeRequestStatus, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        comment = request.POST.get('comment')

        my_request = Request.objects.get(id=request_id)

        if my_request.status == 0:
            my_request.comment = comment
            my_request.status = 2
            my_request.save()

        return super(ChangeRequestStatus, self).post(self, request, *args, **kwargs)


class Expenditures(LoginRequiredMixin, ListView):
    template_name = 'management/expenditure.html'
    queryset = Expenditure.objects.all()
    model = Expenditure


class AddMedicine(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:expenditures')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        medicine_type = request.POST.get('medicine_type')
        boxes_bought = request.POST.get('boxes_bought')
        no_in_box = request.POST.get('no_in_box')
        manufacturer = request.POST.get('manufacturer')
        manufacture_date = request.POST.get('manufacture_date')
        expiry_date = request.POST.get('expiry_date')
        selling_price_per_unit = request.POST.get('selling_price_per_unit')
        cost_price_per_box = request.POST.get('cost_price_per_box')

        try:
            medicine = Medicine.objects.get(name__iexact=name)
            medicine.boxes_bought = boxes_bought
            medicine.accumulated_boxes_bought += int(boxes_bought)
            medicine.boxes_left += int(boxes_bought)
            medicine.no_in_box += int(no_in_box)
            medicine.total_no_units_accumulated += int(no_in_box) * int(boxes_bought)
            medicine.units_left += int(no_in_box) * int(boxes_bought)
            medicine.total_cost = int(cost_price_per_box) * int(boxes_bought)
            medicine.accumulated_total_cost += int(cost_price_per_box) * int(boxes_bought)
            # medicine.pieces_per_box += pieces_per_box
            # medicine.pieces += pieces_per_box * boxes_bought
            # medicine.pieces_left += pieces_per_box * boxes_bought
            medicine.save()
        except Medicine.DoesNotExist:
            new_medicine = Medicine.objects.create(
                name=name,
                medicine_type=medicine_type,
                boxes_bought=boxes_bought,
                accumulated_boxes_bought=boxes_bought,
                boxes_left=boxes_bought,
                no_in_box=no_in_box,
                total_no_units_accumulated=int(no_in_box) * int(boxes_bought),
                units_left=int(no_in_box) * int(boxes_bought),
                selling_price_per_unit=selling_price_per_unit,
                cost_price_per_box=cost_price_per_box,
                cost_price_per_unit=int(cost_price_per_box) / int(no_in_box),
                selling_price_per_box=int(selling_price_per_unit) * int(no_in_box),
                accumulated_total_cost=int(cost_price_per_box) * int(boxes_bought),
                total_cost=int(cost_price_per_box) * int(boxes_bought),
                # pieces_per_box=pieces_per_box,
                # pieces=pieces_per_box * boxes_bought,
                # pieces_left=pieces_per_box * boxes_bought,
                # piece_selling_price=piece_selling_price,
                manufacturer=manufacturer,
                manufacture_date=manufacture_date,
                expiry_date=expiry_date,
                created_by=self.request.user,
            )

        new_exp = Expenditure.objects.create(
            category='Medicine',
            item=name,
            cost=int(cost_price_per_box) * int(boxes_bought),
            created_by=self.request.user,
        )

        return super(AddMedicine, self).post(self, request, *args, **kwargs)


# class base view
class NewLeavePeriod(LoginRequiredMixin, CreateView):
    template_name = 'management/leave_period_new.html'
    success_url = reverse_lazy('management:hr')
    form_class = LeavePeriodForm
    queryset = LeavePeriod.objects.all()

    def form_valid(self, form):
        valid = super(NewLeavePeriod, self).form_valid(form)

        # get number of days
        nod = (form.instance.end_date - form.instance.start_date).days
        form.instance.number_of_days = nod

        # get all user objects
        users = User.objects.all()
        # convert end_date to a datetime type without the time data
        # Import datetime at the top
        # date1 = datetime.datetime.strptime(form.instance.end_date, "%Y-%m-%d")

        # leave_period = LeavePeriod.objects.get(end_date__year=date1.year)
        # looping through all the users
        for user in users:
            # initiate leave days left
            days_left = 0
            try:
                # try to get the latest staff object by excluding this new leave period
                # Add get_latest_by to the class Meta of the Staff model
                latest = Staff.objects.filter(user=user).exclude(leave_period=form.instance).latest()
                # use the latest to get the remaining days of the staff
                days_left = latest.number_of_days_left
            except Staff.DoesNotExist:
                pass
            # create the staff with the user iterator
            staff = Staff.objects.create(
                user=user,
                leave_period=form.instance,
                created_by=self.request.user,
                total_number_of_days=days_left + int(form.instance.days_allowed),
                number_of_days_left=days_left + int(form.instance.days_allowed),
            )

            # staff.save()
            # add the staff instance to the leave period staffs m2m field
            form.instance.staffs.add(staff)
        form.instance.created_by = self.request.user
        form.save()

        return valid


# function base view
@login_required()
def new_leave_period(request):
    form = LeavePeriodForm

    context = {
        'form': form
    }

    if request.method == 'POST':
        form = LeavePeriodForm(request.POST)

        if form.is_valid():
            nod = (form.instance.end_date - form.instance.start_date).days
            form.instance.number_of_days = nod

            # get all user objects
            users = User.objects.all()
            # convert end_date to a datetime type without the time data
            # Import datetime at the top
            date1 = datetime.datetime.strptime(form.instance.end_date, "%Y-%m-%d")

            # leave_period = LeavePeriod.objects.get(end_date__year=date1.year)
            # looping through all the users
            for user in users:
                # initiate leave days left
                days_left = 0
                try:
                    # try to get the latest staff object by excluding this new leave period
                    # Add get_latest_by to the class Meta of the Staff model
                    latest = Staff.objects.filter(user=user).exclude(leave_period=form.instance).latest()
                    # use the latest to get the remaining days of the staff
                    days_left = latest.number_of_days_left
                except Staff.DoesNotExist:
                    pass
                # create the staff with the user iterator
                staff = Staff.objects.create(
                    user=user,
                    leave_period=form.instance,
                    created_by=request.user,
                    total_number_of_days=days_left + int(form.instance.days_allowed),
                    number_of_days_left=days_left + int(form.instance.days_allowed),
                )

                # staff.save()
                # add the staff instance to the leave period staffs m2m field
                form.instance.staffs.add(staff)
            form.instance.created_by = request.user
            form.save()
            # if no errors route to the HR page
            return redirect(reverse_lazy('management:hr'))

    return render(request, template_name='management/leave_period_new.html', context=context)


class LeaveRequestStatus(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('management:leave-period-details', kwargs={'id': kwargs.get('lpid')})

    def get(self, request, *args, **kwargs):
        status = int(kwargs.get('status'))
        leave_id = kwargs.get('lid')

        # leave = None
        try:
            leave = Leave.objects.get(id=leave_id, status=0)
        except Leave.DoesNotExist:
            return super(LeaveRequestStatus, self).get(request, *args, **kwargs)

        if status == 1:
            staff = leave.staff
            staff.number_of_days_left -= leave.number_of_days
            staff.number_of_days_used += leave.number_of_days
            leave.status = 1
            staff.save()
        else:
            leave.status = 2

        leave.save()

        return super(LeaveRequestStatus, self).get(request, *args, **kwargs)


class Revenues(LoginRequiredMixin, CreateView):
    template_name = 'management/revenue.html'
    form_class = RevenueForm
    success_url = reverse_lazy('management:revenues')
    queryset = Revenue.objects.all()

    def form_valid(self, form):
        valid = super(Revenues, self).form_valid(form)

        form.instance.created_by = self.request.user

        form.save()

        return valid

    def get_context_data(self, **kwargs):
        context = super(Revenues, self).get_context_data(**kwargs)

        context['object_list'] = Revenue.objects.all()

        return context