from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(blank = True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default =False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField()
    city = models.CharField(max_length=50)
        
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)



class ReviewMessage(models.Model):
    review = models.ForeignKey(Review, related_name='rev_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_reviews', on_delete=models.CASCADE)