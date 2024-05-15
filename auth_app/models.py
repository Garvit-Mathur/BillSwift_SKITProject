from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Billswift(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.ImageField(upload_to="media/Billswift")
    date_time = models.DateTimeField(auto_now = True,blank = True,null = True)
class BillData(models.Model):
    date_of_upload = models.CharField(max_length=255)
    email = models.EmailField()
    date_on_bill = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    view_bill = models.ImageField(upload_to="media/Billswift")