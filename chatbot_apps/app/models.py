from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name