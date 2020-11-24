from django.urls import path
from .views import *

app_name = 'pharmacy'


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('medicines/', Medicines.as_view(), name='medicines'),
    path('treatments/', Treatments.as_view(), name='treatments'),
    path('treatment/<id>/', treatment_details, name='treatment-details'),
    path('medicine/<id>/', MedicineDetails.as_view(), name='medicine-details'),
    path('prescription/open/<treatment_id>/<patient_id>/', OpenPrescription.as_view(), name='prescription-open'),
    path('prescribed/medicine/remove/<treatment_id>/<pres_id>/<pm_id>/', RemovePrescribedMedicine.as_view(),
         name='prescribed-medicine-remove'),
    path('prescription/confirm/<treatment_id>/<pres_id>/', ConfirmPrescription.as_view(), name='prescription-confirm'),
]
