
from django.db import models
from usersapp.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        on_delete=models.CASCADE, related_name="child_category")

    def __str__(self):
        return self.name
    # making it dynamic


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='attributes', on_delete=models.CASCADE)
    data_type = models.CharField(max_length=50)  # String, Integer, Boolean, etc.

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hide_phone_number = models.BooleanField(default=False)
    phone_number = models.TextField(max_length=14, blank=True, null=True)


class AttributeValue(models.Model):
    post = models.ForeignKey(Post, related_name='attribute_values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('post', 'attribute')  # Ensuring a post has only one value for each attribute


class Chat(models.Model):
    post = models.ForeignKey(Post, related_name='chats', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.timestamp}'


