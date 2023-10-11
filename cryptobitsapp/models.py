from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



# Create your models here.
class UserMessages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=5000)
    subject = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return "sender:" + str(self.sender) +"body:"+ str (self.message)

class UserExtraInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=500)
    moblie_number = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    alternate_email = models.EmailField(max_length=70)
    date_of_birth = models.CharField(max_length=50)
    balance = models.DecimalField(decimal_places=2, max_digits=35)
    amount_available = models.DecimalField(decimal_places=2, max_digits=35)
    amount_withdrawable = models.DecimalField(decimal_places=2, max_digits=35)
    gold = models.BooleanField(default=False)
    def __str__(self):
         return str(self.user)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=5000)
    subject = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return "name:" + str(self.name) +"body:"+ str (self.message)

class subscriber(models.Model):
   
    email = models.EmailField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return "name:" + str(self.email) 