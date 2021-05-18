from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


User = settings.AUTH_USER_MODEL
# Create your models here.
PG = [
    ('General','4+'),
    ('PG','13+'),
    ('Teen','16+'),
    ('Adult','18+')
]
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return self.category_name
 
class Tag(models.Model):
     name = models.CharField(max_length=255)
     slug = models.SlugField(blank=True)
     
     def __str__(self):
         return self.name
     
     def get_tag_movies(self):
         return Movie.objects.filter(tags__icontains=self)
     
class Movie(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    plot = models.TextField()
    cover_image = models.ImageField(upload_to="images/movies/covers")
    cover_thumbnail = ImageSpecField(source='cover_image',
                                   processors = [ResizeToFill(270,400)],
                                   format='JPEG',
                                   options = {'quality':100})
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True)
    trailer = models.URLField()
    parental_guidance = models.CharField(choices=PG, max_length=50)
    is_hd = models.BooleanField(default=True)
    date_released = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
class TvSeries(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    plot = models.TextField()
    cover_image = models.ImageField(upload_to="images/series/covers")
    cover_thumbnail = ImageSpecField(source='cover_image',
                                   processors = [ResizeToFill(270,400)],
                                   format='JPEG',
                                   options = {'quality':100})
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True)
    trailer = models.URLField()
    parental_guidance = models.CharField(choices=PG, max_length=50)
    is_hd = models.BooleanField(default=True)
    date_released = models.DateTimeField()
    
    def __str__(self):
        return self.title

class TvEpisode(models.Model):
    name = models.CharField(max_length=255)
    series = models.ForeignKey(TvSeries, on_delete=models.CASCADE)
    plot = models.TextField()
    date_released = models.DateTimeField()
    
    def __str__(self):
        return f"{self.tvSeries.title} - {self.name}"
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    