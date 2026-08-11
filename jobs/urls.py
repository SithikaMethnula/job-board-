from django.urls import path
from .views import job_list_create, job_detail

urlpatterns = [
    path('', job_list_create, name='job_list_create'),
    path('<int:pk>/', job_detail, name='job_detail'),
]