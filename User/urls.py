from django.urls import path
from .views import LogInView, RegisterView

app_name = 'user'

urlpatterns = [
    path('login/', LogInView, name='login'),
    path('signup/', RegisterView, name='register')
]
