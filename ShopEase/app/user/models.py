from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Address Model Manager Class
class AddressManager(models.Manager):
    # Encapsulation Query the user's default address
    def getDefaultAddress(self,user):
        try:
            addr = self.get(user=user,is_default=True)
        except self.model.DoesNotExist:
            addr = None
        return addr
 
# Create your models here.
class User(AbstractUser,BaseModel):

    class Meta:
        db_table = 'f_user'
        verbose_name = 'usertable'
        verbose_name_plural = verbose_name


class Address(BaseModel):

    user = models.ForeignKey('User',verbose_name="user",on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name="recipient")
    addr = models.CharField(max_length=256,verbose_name="address")
    zip_code = models.CharField(max_length=6,null=True,verbose_name="postcode")
    phone = models.CharField(max_length=11,verbose_name="contact")
    is_default = models.BooleanField(default=False,verbose_name="isdefault")
    objects = AddressManager()

    class Meta:
        db_table = 'f_address'
        verbose_name = 't_address'
        verbose_name_plural = verbose_name