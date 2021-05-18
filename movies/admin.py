from django.contrib import admin
from .models import TvSeries, TvEpisode, Movie, MovieReview, Category, Tag
# Register your models here.

class TvEpisodeInline(admin.TabularInline):
    model = TvEpisode

@admin.register(TvSeries)
class TvSeriesAdmin(admin.ModelAdmin):
    list_display = ('title','category','date_released')
    inlines = [TvEpisodeInline]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','category','date_released')
