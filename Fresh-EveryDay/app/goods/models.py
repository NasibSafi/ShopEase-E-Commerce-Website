from django.db import models
from db.base_model import BaseModel
from simditor.fields import RichTextField


# Create your models here.

class GoodsType(BaseModel):

    name = models.CharField(max_length=50,verbose_name='Type Name')
    logo = models.CharField(max_length=20,verbose_name='Logo')
    image = models.ImageField(upload_to='type',verbose_name='Goods Type image')

    class Meta:
        db_table = 'f_goods_type'
        verbose_name = 'Goods Type Table'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Goods(BaseModel):
    
    name = models.CharField(max_length=50,verbose_name='Goods SPU Name')
    detail = RichTextField()

    class Meta:
        db_table = 'f_goods_spu'
        verbose_name = 'Goods SPU'
        verbose_name_plural = verbose_name

class GoodsSKU(BaseModel):

    status_choices = (
        (0,'Remove from the shelves'),
        (1,'On the shelf')
    )

    type = models.ForeignKey('GoodsType',on_delete=models.CASCADE,verbose_name='Associated Goods types')
    goods = models.ForeignKey('Goods',on_delete=models.CASCADE,verbose_name='Goods SPU')
    name = models.CharField(max_length=50,verbose_name='Goods Name')
    desc = models.CharField(max_length=256,verbose_name='Goods Desc')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Goods Price')
    unite = models.CharField(max_length=20,verbose_name='Unite')
    image = models.ImageField(upload_to='goods',verbose_name='Goods Image')
    stock = models.IntegerField(default=1,verbose_name='Stock')
    sales = models.IntegerField(default=0,verbose_name='Sales')
    state = models.SmallIntegerField(default=1,choices=status_choices,verbose_name='Goods State')

    class Meta:
        db_table = 'f_goods_sku'
        verbose_name = 'Goods SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):

    good = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE,verbose_name='Goods sku associated id')
    path = models.ImageField(upload_to='goods',verbose_name='Image path')

    class Meta:
        db_table = 'f_goods_image'
        verbose_name = 'Goods Images'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):

    good = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE,verbose_name='Goods id')
    image = models.ImageField(upload_to='index',verbose_name='Rotation picture')
    index = models.SmallIntegerField(default=0,verbose_name='Display order') # 0 1 2 3 ...

    class Meta:
        db_table = 'f_index_banner'
        verbose_name = 'Index Banner Table'
        verbose_name_plural = verbose_name


class IndexPromotion(BaseModel):

    name = models.CharField(max_length=50,verbose_name='Event Name')
    url = models.CharField(max_length=256,verbose_name='Event Url')
    image = models.ImageField(upload_to='index',verbose_name='Event image')
    index = models.SmallIntegerField(default=0,verbose_name='Display order')

    class Meta:
        db_table = 'f_index_promotion'
        verbose_name = 'Index Event Table'
        verbose_name_plural = verbose_name


class IndexCreatoryGoods(BaseModel):

    DISPLAY_TYPE_CHOICES = (
        (0,'Title'),
        (1,'Image')
    )

    good = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE,verbose_name='Goods id')
    type = models.ForeignKey('GoodsType',on_delete=models.CASCADE,verbose_name='Goods Type id')
    display_mode = models.SmallIntegerField(default=1,choices=DISPLAY_TYPE_CHOICES,verbose_name='Display Mode')
    index = models.SmallIntegerField(default=0,verbose_name='Display order')

    class Meta:
        db_table = 'f_index_creatory'
        verbose_name = 'Index Category Goods Table'
        verbose_name_plural = verbose_name


