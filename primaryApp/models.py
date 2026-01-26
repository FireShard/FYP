from django.db import models

# Create your models here.
class RamDetails(models.Model):
    ramid = models.AutoField(primary_key=True)
    shopeeListing = models.CharField(max_length=255)
    ramLink = models.URLField(max_length=300)

#tak pakai
class LaptopDetails(models.Model):
    laptopid = models.AutoField(primary_key=True)
    manufacturer = models.CharField(max_length=255)
    ramSize = models.IntegerField()
    architecture = models.IntegerField()
    CPUbrand = models.CharField(max_length=255)
    CPUName = models.CharField(max_length=255)
    CPUGen = models.CharField(max_length=255)
    ramType = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.brand} {self.productLine}"

class UserLaptop(models.Model):
    userid = models.AutoField(primary_key=True)
    manufacturer = models.CharField(max_length=255)
    ramSize = models.IntegerField()
    architecture = models.CharField(max_length=255)
    CPUbrand = models.CharField(max_length=255)
    CPUName = models.CharField(max_length=255)
    CPUGen = models.CharField(max_length=255)
    ramType = models.CharField(max_length=255)
    ramid = models.ForeignKey(RamDetails, on_delete=models.CASCADE)
    