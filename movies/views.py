from django.shortcuts import render
from .models import Movie, TvSeries
# Create your views here.


def IndexView(request, *args, **kwargs):
    new_movies = Movie.objects.all().order_by("-date_released")
    new_series = TvSeries.objects.all().order_by("-date_released")
    
    context = {
        'new_series':new_movies,
        'new_movies':new_movies,
    } 
    return render(request, 'index.html', {})

def catalog(request, *args, **kwargs):
    return render(request, 'catalog.html')

def pricing(request, *args, **kwargs):
    return render(request, 'pricing.html')

def faq(request, *args, **kwargs):
    return render(request, 'faq.html')

def about(request, *args, **kwargs):
    return render(request,'about.html')