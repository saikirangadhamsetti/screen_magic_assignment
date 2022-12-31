from django.db import models
class Messages(models.Model):
    Message=models.CharField(max_length=160)
    Email=models.EmailField()
    Phone=models.IntegerField()
    Country=models.CharField(max_length=20)
    Schedule_date=models.CharField(max_length=20)
    validatorlog=models.CharField(max_length=200,null=True)
    