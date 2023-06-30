from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    # User dashboard
    path('edit/', views.edit, name='edit')
]
