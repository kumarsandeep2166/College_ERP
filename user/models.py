from django.db import models
from django.contrib.auth.models import User

class Usertype(models.Model):
    user_choice=(
        ('employee', 'employee'),
        ('student','student'),
    )
    usertype=models.CharField(max_length=50, choices=user_choice, default='employee')
    userprofile = models.OneToOneField(User, on_delete=models.CASCADE)       



