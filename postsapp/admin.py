
# Register your models here.
from django.contrib import admin
from .models import Category, Attribute, Post, AttributeValue

admin.site.register(Category)
admin.site.register(AttributeValue)
admin.site.register(Attribute)
admin.site.register(Post)
