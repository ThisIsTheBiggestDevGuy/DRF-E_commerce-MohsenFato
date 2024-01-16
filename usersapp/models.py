from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from rest_framework.authtoken.models import Token
# Create your models here.


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    seller_groups = models.ManyToManyField(Group, related_name='seller_users', blank=True, verbose_name='Seller Groups')
    seller_permissions = models.ManyToManyField(Permission, related_name='seller_users_permissions', blank=True,
                                                verbose_name='Seller Permissions')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    contact_info = models.TextField(null=True, blank=True)
    seller_groups = models.ManyToManyField(Group, related_name='seller_profile', blank=True)
    seller_user_permissions = models.ManyToManyField(Permission, related_name='seller_profile_permissions', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    # fields related to reviews and ratings
    total_reviews = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username


class SellerReview(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} | {self.se}"