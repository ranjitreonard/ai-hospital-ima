from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Ward)
admin.site.register(Bed)
admin.site.register(BedAllocate)
admin.site.register(Patient)
admin.site.register(MedicalDiagnosis)
admin.site.register(Treatment)
# admin.site.register(Announcement)
admin.site.register(Request)
admin.site.register(LeavePeriod)
admin.site.register(Revenue)
admin.site.register(VitalSign)
