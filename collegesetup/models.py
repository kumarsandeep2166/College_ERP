from django.db import models
from django.contrib.auth.models import User

class AffiliatedTo(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
class Approval(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Accredited_Body(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class BaseSetUp(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=250,blank=True)
    affiliated_body = models.ManyToManyField(AffiliatedTo,blank=True)
    email = models.EmailField(null=True, blank=True)
    date_of_esthablishment = models.DateField(null=True,blank= True)
    approval = models.ManyToManyField(Approval,blank=True)
    approved_body = models.ManyToManyField(Accredited_Body,blank=True)
    website = models.URLField(null=True,blank=True)
    principal = models.CharField(max_length=250,null=True,blank=True)
    contact_person_number = models.CharField(max_length=13, null=True,blank=True)
    contact_person_name = models.CharField(max_length=50,null=True,blank=True)
    logo = models.ImageField(null=True,blank=True)
    lattitude = models.CharField(max_length=250,null=True,blank=True)
    longitude = models.CharField(max_length=250,null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    


