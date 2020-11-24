import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, RedirectView

from apps.staff.forms import LeaveForm
from apps.staff.models import Leave, Staff
from . import forms
from . import models


@login_required()
def dashboard(request):
    return render(request, template_name='staff/dashboard.html')


@login_required()
def complaints(request):
    my_complaints = models.Complaint.objects.filter(created_by=request.user)
    form = forms.ComplaintForm

    context = {
        'object_list': my_complaints,
        'form': form
    }

    if request.method == 'POST':
        form = forms.ComplaintForm(request.POST)
        form.instance.created_by = request.user
        form.instance.is_seen = False
        form.instance.status = 0
        form.save()

    return render(request, template_name='staff/complaints.html', context=context)


@login_required()
def cancel_complaint(request, id):
    complaint = models.Complaint.objects.get(id=id)

    if complaint.status == 0:
        complaint.status = 2
        complaint.save()

    return redirect(reverse_lazy('staff:complaints'))


class StaffLeaves(LoginRequiredMixin, ListView):
    template_name = 'staff/leaves.html'
    model = Leave

    def get_queryset(self):
        return Leave.objects.filter(created_by=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffLeaves, self).get_context_data(**kwargs)
        try:
            context['staff'] = Staff.objects.get(
                user=self.request.user,
                leave_period__end_date__year=timezone.now().year)
        except Staff.DoesNotExist:
            pass
        return context


# class NewStaffLeave(LoginRequiredMixin, RedirectView):
#     url = reverse_lazy('staff:leaves')
#
#     def post(self, request, *args, **kwargs):
#         str_start_date = request.POST.get('start_date')
#         str_end_date = request.POST.get('end_date')
#
#         start_date = datetime.datetime.strptime(str_start_date, '%Y-%m-%d')
#         end_date = datetime.datetime.strptime(str_end_date, '%Y-%m-%d')
#
#         print(start_date)
#         print(end_date)
#
#         return super(NewStaffLeave, self).post(self, request, *args, **kwargs)


class NewStaffLeave(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('staff:leaves')
    template_name = 'staff/new_leave.html'
    form_class = LeaveForm
    queryset = Leave.objects.all()

    def form_valid(self, form):
        valid = super(NewStaffLeave, self).form_valid(form)

        # current staff leave period for the user
        staff = Staff.objects.get(user=self.request.user, leave_period__end_date__year=timezone.now().year)

        # number of days to go on leave
        form.instance.number_of_days = (form.instance.end_date - form.instance.start_date).days

        # assigning staff object o leave.staff
        form.instance.staff = staff

        # setting leave status to Pending
        form.instance.status = 0

        form.instance.created_by = self.request.user

        # adding new leave record to staff object
        staff.leaves.add(form.instance)

        staff.save()

        form.save()

        return valid

    # this method allows us to pass self.request to the LeaveForm __init__() method
    def get_form_kwargs(self):
        kwargs = super(NewStaffLeave, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
