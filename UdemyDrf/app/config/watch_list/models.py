from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
    

class StreamingPlatform(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=60)
    platform = models.ForeignKey(StreamingPlatform,on_delete=models.CASCADE,related_name='watchlist')
    storyline = models.CharField(max_length=100)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    review_author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rating = models.PositiveIntegerField(default=1,choices=RATING_CHOICES)
    description = models.CharField(max_length=200,null=True,blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    
    def __str__(self):
        return (f"{self.rating} - {self.movie.title}")