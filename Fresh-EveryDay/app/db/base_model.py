from django.db import models

# 定义一个抽象模型类
class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True,verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True,verbose_name="Update Time")
    is_del = models.BooleanField(default=False,verbose_name="Delete Marker")

    class Meta:
        abstract = True # 说明是一个抽象模型类