from django.db import models

# Create your models here.


class Vocabulary(models.Model):
    word = models.CharField(max_length=50, null=True)
    frequency = models.IntegerField(null=True)
