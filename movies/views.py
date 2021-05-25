from django.shortcuts import render, get_object_or_404
from .models import Movie, TvSeries
from django.utils import timezone
# Create your views here.


def IndexView(request, *args, **kwargs):
    new_movies = Movie.objects.all().order_by("-date_released")
    new_series = TvSeries.objects.all().order_by("-date_released")
    all_things = list(new_movies)+list(new_series)
    
    context = {
        'new_series':new_series[:18],
        'new_movies':new_movies[:18],
        # 'animations':Movie.objects.filter(category="animation"),
        'all_new': sorted(all_things, key=lambda x: x.date_released, reverse=True)[:10],
        'new_releases': sorted(all_things, key=lambda x: x.date_released, reverse=True)[:6]
    } 
    return render(request, 'index.html', context)

def MovieListView(request, *args, **kwargs):
    context = {
        'movies':Movie.objects.filter(date_released__lte=timezone.now())
    }
    return render(request, 'movies.html', context)

def MovieDetailView(request, slug,*args, **kwargs):
    movie = get_object_or_404(Movie, slug=slug)
    
    context = {
        'movie':movie,
    }
    return render(request, 'movie_detail.html', context)

def TvListView(request, *args, **kwargs):
    context = {
        'series':Movie.objects.filter(date_released__lte=timezone.now())
    }
    return render(request, 'series.html', context)

def TvSerieDetailView(request, slug, *args, **kwargs):
    serie = get_object_or_404(TvSeries, slug=slug)

    context = {
        'series':serie,
    }
    return render(request, 'serie_detail.html', context)
    
def catalog(request, *args, **kwargs):
    return render(request, 'catalog.html')

def pricing(request, *args, **kwargs):
    movies = Movie.objects.all()
    return render(request, 'pricing.html')

def faq(request, *args, **kwargs):
    return render(request, 'faq.html')

def about(request, *args, **kwargs):
    return render(request,'about.html')

