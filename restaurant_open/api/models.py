from django.db import models

class RestaurantHours(models.Model):
    name = models.CharField(max_length=100)
    sunday = models.CharField(max_length=100, default="closed")
    monday = models.CharField(max_length=100, default="closed")
    tuesday = models.CharField(max_length=100, default="closed")
    wednesday = models.CharField(max_length=100, default="closed")
    thursday = models.CharField(max_length=100, default="closed")
    friday = models.CharField(max_length=100, default="closed")
    saturday = models.CharField(max_length=100, default="closed")