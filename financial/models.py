from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tax(models.Models):
	name = models.CharField(max_legth=100)
	rate = models.FloatField(default=0.0)
		