from django.db import models

# Create your models here.
class UserAccount(models.Model):
    userName = models.CharField(max_length=16)
    password = models.CharField(max_length=16)

class student(models.Model):
    studentId = models.CharField(max_length=16)
    studentName = models.CharField(max_length=16)


class Brand(models.Model):
    name = models.CharField(max_length=16)
    origin = models.CharField(max_length=16)
    manufacturingSince = models.IntegerField()
    def __str__(self):
        return self.name


class Model(models.Model):
    modelName = models.CharField(max_length=16)
    launchDate = models.IntegerField()
    platform_choice = ((1,'Android'),(2,'iOS'),(3,'windowsPhone'),(4,'Harmony'),)
    platform = models.SmallIntegerField(verbose_name="", choices= platform_choice)
    brand = models.ForeignKey(verbose_name="", to="Brand", to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return self.modelName



class Review(models.Model):
    title = models.CharField(verbose_name="Title", max_length=16)
    dataPublish = models.CharField(verbose_name="Data Publish",max_length=16)
    relatedModle = models.ForeignKey(verbose_name="Related Modle", to="Model", to_field="id", on_delete=models.CASCADE)
    relatedbrand = models.ForeignKey(verbose_name="Related Brand", to="Brand", to_field="id", on_delete=models.CASCADE, null=True)
    link = models.CharField(verbose_name="link", max_length=16)