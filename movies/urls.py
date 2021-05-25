from django.urls import path
from .views import (IndexView, catalog, pricing, faq, about,
                    MovieListView, TvListView,
                    MovieDetailView, TvSerieDetailView)

app_name = 'movies'

urlpatterns = [
    path("", IndexView, name='index'),
    path("catalog/", catalog, name='catalog'),
    path('pricing/', pricing, name='pricing'),
    path('faq/', faq, name="faq"),
    path('about/', about, name='about'),
    path('movies/', MovieListView, name="movies"),
    path('series/', TvListView, name="series"),
    path('movies/<slug>/<int:pk>/', MovieDetailView, name='movie-detail'),
    path('shows/<slug>/<int:pk>/', TvSerieDetailView, name='series-detail'),
]