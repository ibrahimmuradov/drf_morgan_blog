from django.urls import path
from . import views

app_name = 'contact-api'

urlpatterns = [
    path('contact/', views.ContactCreateView.as_view(), name="contact")
]