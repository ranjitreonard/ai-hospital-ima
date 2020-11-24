from django.urls import *
from .views import *


app_name = 'staff'


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('complaints/', complaints, name='complaints'),
    path('complaint/cancel/<id>/', cancel_complaint, name='complaint-cancel'),
    path('leaves/', StaffLeaves.as_view(), name='leaves'),
    path('leave/add/', NewStaffLeave.as_view(), name='leave-add'),
]
