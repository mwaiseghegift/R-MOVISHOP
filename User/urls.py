from django.urls import path
from .views import (LogInView, RegisterView, LogOutView, VerificationView,
                    RequestResetEmail, ResetPasswordView)

app_name = 'user'

urlpatterns = [
    path('login/', LogInView, name='login'),
    path('signup/', RegisterView, name='register'),
    path('logout', LogOutView, name='logout'),
    path('activate/<uidb64>/<token>/', VerificationView, name='activate'),
    path('request-reset-email/', RequestResetEmail, name="request-reset-email"),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView, name='reset-password'),
]
