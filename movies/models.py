from django.db import models
from django.utils.text import slugify
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
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True)
    parental_guidance = models.CharField(choices=PG, max_length=50)
    date_released = models.DateTimeField()
    
class Trailer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_ddelete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TectField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    