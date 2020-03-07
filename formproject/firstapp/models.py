from django.db import models
from django.utils import timezone
# Create your models here.
class user_data(models.Model):
    name=models.CharField(max_length=264)
    email =models.EmailField(max_length=264,unique=True)
    phone =models.CharField(max_length=264,unique=True)
    gender=models.CharField(max_length=20)
    # password =models.CharField(max_length=264)

    def __str__(self):
        return self.name

class searched_history(models.Model):
    email =models.EmailField(max_length=264,unique=False,blank=True,null=True)
    monument_name=models.CharField(max_length=264,unique=False,blank=True,null=True)
    date = models.DateField(default=timezone.now())
    def __str__(self):
        return self.email+" "+self.monument_name

class monument_reviews(models.Model):
    email =models.EmailField(max_length=264,unique=False)
    monument_name=models.CharField(max_length=264,unique=False)
    rating1 =models.IntegerField(unique=False)
    rating2 =models.IntegerField(unique=False)
    rating3 =models.IntegerField(unique=False)
    rating4 =models.IntegerField(unique=False)
    rating5 =models.IntegerField(unique=False)

    total_avg =models.IntegerField(unique=False)
    date = models.DateField(default=timezone.now())

class information(models.Model):
    email =models.EmailField(max_length=264,unique=False)
    monument_name=models.CharField(max_length=264,unique=False)
    information=models.CharField(max_length=264,unique=False)
    flag =models.BooleanField()
