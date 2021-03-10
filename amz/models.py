from django.db import models

# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=50,null=False)
    item = models.CharField(max_length=500,null=False)
    creation_date = models.CharField(max_length=50,null=False)
    creation_price = models.IntegerField(null=False,default=00)
    trigger_price = models.IntegerField(null=False,default=00)

    def __str__(self):
        return  self.email



