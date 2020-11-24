from django.conf import settings
from django.db import models
from django.utils import timezone

STATUS = {
    (0, 'Pending'),
    (1, 'Reviewed'),
    (2, 'Cancel')
}


class Complaint(models.Model):
    complaint = models.CharField(max_length=3000, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, blank=True, null=True)
    review = models.CharField(max_length=3000, blank=True, null=True)
    is_seen = models.BooleanField(blank=True, null=True)
    seen_at = models.DateTimeField(blank=True, null=True)
    seen_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='complaint_seen_by')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='complaints')
    created_at = models.DateTimeField(default=timezone.now)
    review_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  blank=True, null=True, related_name='complaint_review_by')
    review_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.complaint)

    class Meta:
        db_table = 'complaint'
        ordering = ('-created_at',)


class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             related_name='staff_user', blank=True, null=True)
    total_number_of_days = models.IntegerField(blank=True, null=True, default=0)
    number_of_days_used = models.IntegerField(blank=True, null=True, default=0)
    number_of_days_left = models.IntegerField(blank=True, null=True, default=0)
    leaves = models.ManyToManyField('Leave', related_name='staff_leaves', blank=True)
    leave_period = models.ForeignKey('management.LeavePeriod', on_delete=models.SET_NULL,
                                     related_name='staff_leave_period', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   related_name='staffs', blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name()} - {self.number_of_days_left}"

    class Meta:
        db_table = 'staff'
        get_latest_by = 'created_at'


LEAVE_STATUS = {
    (0, 'Pending'),
    (1, 'Approved'),
    (2, 'Rejected')
}


class Leave(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL,
                              related_name='leave_staff', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_days = models.IntegerField(blank=True, null=True, default=0)
    status = models.IntegerField(choices=LEAVE_STATUS, blank=True, null=True)
    purpose = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   related_name='leaves', blank=True, null=True)

    def __str__(self):
        return f"{self.number_of_days}"

    class Meta:
        db_table = 'leave'