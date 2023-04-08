from django.db import models

# Create your models here.
    
class UserPayment(models.Model):
  userName = models.CharField(max_length=100)
  cardHolder = models.CharField(max_length=100)
  cardNumber = models.CharField(max_length=15)
  expiryDate = models.DateField()
  transactionId = models.CharField(max_length=20)
  transactionDate = models.DateTimeField()
  transactionAmt = models.IntegerField()