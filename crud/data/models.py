from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Data(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, default=True, null=True, related_name="userData"
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.firstname
