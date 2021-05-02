from django.urls import path
from .views import IndexView

app_name = 'movies'

urlpatterns = [
    path("", IndexView, name='index')
]