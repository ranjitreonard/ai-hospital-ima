from django.contrib import admin
from .models import *

admin.site.register(Medicine)
admin.site.register(PrescribedMedicine)
admin.site.register(Prescription)
