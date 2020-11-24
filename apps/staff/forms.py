from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.staff.models import Staff, Leave
from . import models


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = ('complaint',)
        widgets = {
            'complaint': forms.Textarea(attrs={'required': True, 'rows': 1, 'class': 'form-control border-0', 'placeholder': 'Type complaints here', 'autofocus': True})
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = models.Leave
        fields = ('start_date', 'end_date', 'purpose')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'required': True, 'min': f'{timezone.now().date()}'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'required': True, 'min': f'{timezone.now().date()}'})
        }

    # using __init__() method to get self.request from NewStaffLeave cbv
    def __init__(self, request=None, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.request=request

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        # getting number of days from end date and start date
        no_of_days = (end_date - start_date).days

        # getting staff object of the current leave period for the user
        staff = Staff.objects.get(user=self.request.user, leave_period__end_date__year=timezone.now().year)

        # checking to ensure end date is not less than start date
        if end_date < start_date:
            raise ValidationError('End Date is less than Start Date selected')

        # checking to ensure end date is not the same as start date
        if end_date == start_date:
            raise ValidationError('End Date should not be the same as Start Date')

        # checking to ensure number of days requested is not more than number of days left for the staff
        if staff.number_of_days_left < no_of_days:
            raise ValidationError('The number of days selected are more than your number of leave days remaining')

        # get staff current period leave requests
        leaves = Leave.objects.filter(staff=staff)

        # check if the dates selected are not between previous leave periods
        for leave in leaves.all():
            if leave.start_date > start_date:
                raise ValidationError('Invalid start date selected')

            if leave.start_date <= start_date and leave.end_date >= end_date:
                raise ValidationError('You already have a leave request between the dates selected')

        return self.cleaned_data
