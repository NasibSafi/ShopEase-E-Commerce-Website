from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotion, Goods, IndexCreatoryGoods



# Register your models here.

class BaseModelAdmin(admin.ModelAdmin):
    '''Called when adding or updating data in the table'''
    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change) 
        # Issue tasks to let celery regenerate static pages
        from celery_tasks.tasks import generate_static_indexhtml
        generate_static_indexhtml.delay()
        # Delete home page cache data
        cache.delete('static_index_data')

    '''删除表中的数据时调用'''
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        from celery_tasks.tasks import generate_static_indexhtml
        # Issue tasks to let celery regenerate static pages
        generate_static_indexhtml.delay()
        # Delete home page cache data
        cache.delete('static_index_data')


class GoodsTypeModelAdmin(BaseModelAdmin):
    pass
class GoodsSKUModelAdmin(BaseModelAdmin):
    pass
class IndexGoodsBannerModelAdmin(BaseModelAdmin):
    pass
class IndexPromotionModelAdmin(BaseModelAdmin):
    pass
class IndexCreatoryGoodsAdmin(BaseModelAdmin):
    pass

admin.site.register(GoodsType,GoodsTypeModelAdmin)
admin.site.register(IndexCreatoryGoods, IndexCreatoryGoodsAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerModelAdmin)
admin.site.register(IndexPromotion,IndexPromotionModelAdmin)
admin.site.register(Goods)
admin.site.register(GoodsSKU,GoodsSKUModelAdmin)
