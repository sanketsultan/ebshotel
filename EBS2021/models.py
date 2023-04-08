from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class UserSignup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    address = models.CharField(max_length=300,null=True,default=None)
    regdate = models.DateTimeField(auto_now_add=True,blank=True)
    def _str_(self):
      return self.user.username

class Event(models.Model):
    eventname=models.CharField(max_length=100,null=True)
    image = models.FileField(null=True)
    category=models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=300,null=True)
    startdate=models.DateField(null=True)
    enddate=models.DateField(null=True)
    venue=models.CharField(max_length=300,null=True)
    entryprice=models.CharField(max_length=100,null=True)
    creationdate = models.DateTimeField(default=datetime.now, blank=True)
    def _str_(self):
      return self.eventname

class SponsorTbl(models.Model):
    event =models.ForeignKey(Event,on_delete=models.CASCADE)
    sponsorimage = models.FileField(null=True)
    creationdate = models.DateTimeField(default=datetime.now, blank=True)
    def _str_(self):
      return self.event.eventname

class Category(models.Model):
    categoryname=models.CharField(max_length=100,null=True)
    creationdate = models.DateTimeField(default=datetime.now, blank=True)
    def _str_(self):
      return self.categoryname

class Booking(models.Model):
    userinfo =models.ForeignKey(UserSignup,on_delete=models.CASCADE)
    eventinfo = models.ForeignKey(Event, on_delete=models.CASCADE)
    person=models.CharField(max_length=100,null=True)
    total=models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=20,null=True)
    bookingdate = models.DateField(null=True)
    cardno = models.CharField(max_length=20,null=True)
    cvv = models.CharField(max_length=10,null=True)
    expirydate = models.CharField(max_length=50,null=True)
    def _str_(self):
      return self.id
    
    
    
class UserPayment(models.Model):
  userName = models.CharField(max_length=100)
  cardHolder = models.CharField(max_length=100)
  cardNumber = models.CharField(max_length=15)
  expiryDate = models.DateField()
  transactionId = models.CharField(max_length=20)
  transactionDate = models.DateTimeField()
  transactionAmt = models.IntegerField()
  


class Mail(models.Model):
  url = models.CharField(max_length=100)
  request = models.CharField(max_length=150)
  response =models.CharField(max_length=150)
  responsecode = models.CharField(max_length=5)
  transactionDate = models.DateTimeField()
  uuid = models.CharField(max_length=10,null=False)