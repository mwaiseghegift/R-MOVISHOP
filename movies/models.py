from django.db import models
from django.utils.text import slugify
# Create your models here.


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
    