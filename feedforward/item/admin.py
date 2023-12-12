from django.contrib import admin

from .models import Category, Item, Review, ReviewMessage

admin.site.register(Category)

admin.site.register(Item)


admin.site.register(ReviewMessage)

admin.site.register(Review)