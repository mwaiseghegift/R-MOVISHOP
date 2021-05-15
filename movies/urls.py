from django.urls import path
from .views import (IndexView, catalog)

app_name = 'movies'

urlpatterns = [
    path("", IndexView, name='index'),
    path("catalog/", catalog, name='catalog'),
]