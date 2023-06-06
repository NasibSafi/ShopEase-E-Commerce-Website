from django.db import models
from db.base_model import BaseModel
# Create your models here.

class OrderInfo(BaseModel):

    PAY_METHOD = {       
        "1": "Cash on delivery",
        "2": "WeChat pay",
        "3": "Alipay",
        "4": "UnionPay"
    }

    ORDER_STATUS = {          
        1: 'To be paid',
        2: 'To be shipped',
        3: 'To be received',
        4: 'To be evaluated',
        5: 'Completed'
    }

    PAY_METHODS_CHOICES = (
        (1, 'Cash on delivery'),
        (2, 'WeChat pay'),
        (3, 'Alipay'),
        (4, 'UnionPay')
    )

    ORDER_STATUS_CHOICES = (          
        (1, 'To be paid'),
        (2, 'To be shipped'),
        (3, 'To be received'),
        (4, 'To be evaluated'),
        (5, 'Completed')
    )
    
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name='Order id')
    addr = models.ForeignKey('user.Address',on_delete=models.CASCADE,verbose_name='Addr id')
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,verbose_name='User id')
    pay_methods = models.SmallIntegerField(choices=PAY_METHODS_CHOICES,default=3,verbose_name='Payment Methods')
    total_count = models.IntegerField(default=1,verbose_name='Total number of Goods')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Total price of goods')
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Order shipping cost')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1,verbose_name='Order Status')
    trade_no = models.CharField(max_length=128,default='',verbose_name='Trade no.')

    class Meta:
        db_table = 'f_order_info'
        verbose_name = 'Order Info Table'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):

    order_info = models.ForeignKey('OrderInfo',on_delete=models.CASCADE,verbose_name='Order id')
    goods_sku = models.ForeignKey('goods.GoodsSKU',on_delete=models.CASCADE,verbose_name='Goods id')
    count = models.IntegerField(default=1,verbose_name='Number of Goods')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Price of goods')
    comment = models.CharField(max_length=256,verbose_name='Comment')

    class Meta:
        db_table = 'f_order_goods'
        verbose_name = 'Order Goods Table'
        verbose_name_plural = verbose_name

