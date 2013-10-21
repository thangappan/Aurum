from django.db import models

# Create your models here.

class Count(models.Model):

	count = models.IntegerField(max_length=10)

