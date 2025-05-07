from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    official_name = models.CharField(max_length=100, unique=True, blank=True)
    cca2 = models.CharField(max_length=10, unique=True)  # e.g., "US", "DE", etc.
    languages = models.JSONField(default=list)
    capital = models.CharField(max_length=100)
    population = models.BigIntegerField()
    area = models.FloatField(blank=True, null=True)
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100, blank=True)
    timezones = models.JSONField(default=list)
    currencies = models.JSONField(default=list, blank=True)
    flags = models.JSONField(default=dict, blank=True)
    coat_of_arms = models.JSONField(default=dict, blank=True)
    flag = models.CharField(max_length=2)