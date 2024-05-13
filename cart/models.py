from django.db import models

# Create your models here.

class OrderModel(models.Model):
    subtota = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    customname = models.CharField(max_length=50)
    customeemail = models.CharField(max_length=50)
    customephone = models.CharField(max_length=20)
    customeaddress = models.CharField(max_length=200)
    paytype = models.CharField(max_length=10)
    bankaccount = models.CharField(max_length=10,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.customname
    
class DetailModel(models.Model):
    #以下是代入外來主鍵，on_delete消失時會自動刪除所有細項
    dorder = models.ForeignKey('OrderModel',on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname