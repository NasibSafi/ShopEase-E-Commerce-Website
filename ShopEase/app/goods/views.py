from django.shortcuts import redirect, render
from django.core.cache import cache
from django.urls import reverse
from django.views import View
from django.db.models import Q
from goods.models import Goods, GoodsSKU, GoodsType, IndexCreatoryGoods,IndexGoodsBanner, IndexPromotion
from order.models import OrderGoods
from django_redis import get_redis_connection
from django.core.paginator import Paginator
# Create your views here.

class IndexGoodView(View):

    def get(self,request):
        '''
            If the user is not logged in, return the generated static home page;
            If the user is logged in, judge whether there is cached data, if there is cached data, use the cached data, if there is no cached data, query the database and set the cache
        '''
        if not request.user.is_authenticated:
            return render(request,'static_index.html')
        index_cache = cache.get('static_index_data')
        if index_cache is None:
            # Get all product category information
            types = GoodsType.objects.all()
            # Get carousel data
            banners = IndexGoodsBanner.objects.all().order_by('index')
            # get activity data
            promotions = IndexPromotion.objects.all().order_by('index')
            # Get the home page data corresponding to the category
            for type in types:
                # Get the text information of the homepage category
                title_banner = IndexCreatoryGoods.objects.filter(type=type,display_mode=0).order_by('index')
                # Get the image information of the homepage category
                image_banner = IndexCreatoryGoods.objects.filter(type=type).order_by('index')

                type.title_banners = title_banner
                type.image_banners = image_banner
            index_cache = {"types":types,"banners":banners,"promotions":promotions}
            # set cache
            cache.set('static_index_data',index_cache,3600) # 1 hour expires

        # Get the current user's shopping cart quantity
        redis_conn = get_redis_connection('default') # connect redis
        user_id = request.user.id
        cart_len = redis_conn.hlen('cart_%d' % user_id)
        index_cache.update(cart_len=cart_len) #Add or update cart_len field to index_cache dictionary

        return render(request,'index.html',index_cache)


class GoodDetailView(View):

    def get(self,request,good_id):
        try:
            # Get information about the current product
            goods = GoodsSKU.objects.get(id=good_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index')) 

        # Get all product category information
        types = GoodsType.objects.all()
        # Obtain two pieces of data for the new product recommendation of the current category
        new_products = GoodsSKU.objects.filter(Q(type=goods.type)&~Q(id=goods.id)).order_by('-create_time')[:2]
        # Obtain other specifications and product information of the current product
        good_spu = GoodsSKU.objects.filter(goods=goods.goods).exclude(id=goods.id)

        # Get product review information
        order_goods = OrderGoods.objects.filter(goods_sku=good_id).exclude(comment='')

        data = {'goods':goods,'types':types,'new_products':new_products,"good_spu":good_spu,"order_goods":order_goods}

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('default')
            user_id = request.user.id
            cart_len = redis_conn.hlen('cart_%d' % user_id)
            data.update(cart_len=cart_len)

            # add browsing history
            redis_conn.lrem('history_%d' % user_id,0,good_id) # First remove the current product browsing records that existed before.
            redis_conn.lpush('history_%d' % user_id,good_id) # Insert the current product id record to the left

        return render(request,'detail.html',data)


class GoodListView(View):

    def get(self,request,type_id,page):
        
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            return redirect(reverse('goods:index'))
        
        # Query all commodity classification information
        types = GoodsType.objects.all()
        # Get new product recommendation data
        new_products = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]

        sort = request.GET.get('sort')
        if sort == "price":
            goods = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == "sales":
            goods = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = "default"
            goods = GoodsSKU.objects.filter(type=type).order_by('-id')

        good_page = Paginator(goods,1) # 1条数据为一个页码
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > good_page.num_pages:
            page = 1

        goods = good_page.page(page)

        """Construct page number: return 5 page number buttons, the first two page numbers, the current page number, and the last two page numbers"""
         # When the total number of pages is less than 5, return all page numbers
         # If the current page is the first 3 pages, then display pages 1-5
         # If the current page is the last 3 pages, then display the last 5 pages
         # In other cases, display the first 2 pages of the current page, the current page, and the next 2 pages of the current page
        
        if good_page.num_pages < 5:
            page_range = range(1,good_page.num_pages+1)
        elif goods.number <= 3:
            page_range = range(1,6)
        elif good_page.num_pages - goods.number <= 3:
            page_range = range(good_page.num_pages-4,good_page.num_pages+1)
        else:
            page_range = range(goods.number-2,goods.number+3)

        data = {"type":type,"types":types,"new_products":new_products,"goods":goods,"page_range":page_range,"sort":sort}

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('default')
            user_id = request.user.id
            cart_len = redis_conn.hlen('cart_%d' % user_id)
            data.update(cart_len=cart_len)

        return render(request,'list.html',data)