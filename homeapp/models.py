import datetime

from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.

class PasswordStore(models.Model):
    user_id = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    app_type = models.CharField(max_length=20)
    app_or_web = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=100, null=True)
    app_pass = models.CharField(max_length=100)
    other_detail = models.CharField(max_length=500)
    updated_on = models.DateField(datetime.date.today())

    def __str__(self) -> str:
        return self.app_or_web


