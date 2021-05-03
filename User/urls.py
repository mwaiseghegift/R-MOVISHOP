from django.urls import path
from .views import LogInView
app_name = 'user'

urlpatterns = [
    path('login/', LogInView, name='login')
]
