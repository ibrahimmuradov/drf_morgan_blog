from django.urls import path
from . import views

app_name = 'account-api'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('activate/<slug>/', views.ActivationView.as_view(), name="activate"),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_complete/<slug>/', views.ResetPasswordCompleteView.as_view(), name='reset_password_complete')
]