from django.shortcuts import render, get_object_or_404
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


def MovieDetailView(request, slug,*args, **kwargs):
    movie = get_object_or_404(Movie, slug=slug)
    
    context = {
        'movie':movie,
    }
    return render(request, 'movie_detail.html', context)


def TvSerieDetailView(request, slug, *args, **kwargs):
    serie = get_object_or_404(TvSeries, slug=slug)

    context = {
        'series':serie,
    }
    return render(request, 'serie_detail.html', context)
    
def catalog(request, *args, **kwargs):
    return render(request, 'catalog.html')

def pricing(request, *args, **kwargs):
    return render(request, 'pricing.html')

def faq(request, *args, **kwargs):
    return render(request, 'faq.html')

def about(request, *args, **kwargs):
    return render(request,'about.html')