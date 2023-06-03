from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin

from goods.models import GoodsSKU
# Create your views here.

class CartView(LoginRequiredMixin,View):

    def get(self,request):

        user_id = request.user.id
        redis_conn = get_redis_connection("default")

        cart_dict = redis_conn.hgetall('cart_%d' % user_id) # {"Product id":"Product Quantity"}
        total_price = 0
        total_count = 0
        goods = []
        for good_id,count in cart_dict.items():
            # Get product information based on product id
            good = GoodsSKU.objects.get(id=good_id)
            # Calculate subtotals for items
            amount = good.price * int(count)
            # Save item subtotal and quantity
            good.amount = amount
            good.count = int(count) 
            goods.append(good)
            # Add up to calculate the total number of items and the total price
            total_count += int(count)
            total_price += amount
        
        cart_len = redis_conn.hlen('cart_%d' % user_id)

        context = {"goods":goods,"total_count":total_count,"total_price":total_price,"cart_len":cart_len}

        return render(request,'cart.html',context)

class CartAddView(View):
    """
    Accumulate the data that need to be passed to calculate the total number of items and the total price: item id, item quantity, csrf defense
    """
    def post(self,request):
        
        good_id = request.POST.get('good_id')
        good_count = request.POST.get('good_count')

        if not request.user.is_authenticated:
            return JsonResponse({"res":0,"msg":"not logged in"})

        if not all([good_id,good_count]):
            return JsonResponse({"res":0,"msg":"Parameter error"})

        try:
            count = int(good_count)
        except:
            return JsonResponse({"res":0,"msg":"The cart quantity is not an integer"})
        try:
           good = GoodsSKU.objects.get(id=good_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"res":0,"msg":"Without this product, please do not operate maliciously"})

        if good.stock < count:
            return JsonResponse({"res":0,"msg":"Inventory shortage"})

        user_id = request.user.id
        redis_conn = get_redis_connection("default")
        # Query whether the current product has been added to the shopping cart, if it has been added, it needs to be accumulated
        cur_good_count = redis_conn.hget('cart_%d' % user_id,good_id)
        if cur_good_count:
            count += int(cur_good_count)
        redis_conn.hset('cart_%d' % user_id,good_id,count)

        cart_len = redis_conn.hlen('cart_%d' % user_id)

        return JsonResponse({"res":1,"msg":"Add to Cart successful","cart_len":cart_len})
        
class CartUpdateView(View):

    def post(self,request):

        good_id = request.POST.get('good_id')
        good_count = request.POST.get('good_count')

        if not request.user.is_authenticated:
            return JsonResponse({"res":0,"msg":"not logged in"})

        if not all([good_id,good_count]):
            return JsonResponse({"res":0,"msg":"Parameter error"})

        try:
            count = int(good_count)
        except:
            return JsonResponse({"res":0,"msg":"The cart quantity is not an integer"})
        try:
           good = GoodsSKU.objects.get(id=good_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"res":0,"msg":"Without this product, please do not operate maliciously"})

        if good.stock < count:
            return JsonResponse({"res":0,"msg":"Inventory shortage"})

        user_id = request.user.id
        redis_conn = get_redis_connection("default")
        # Set new cart addition quantity
        redis_conn.hset('cart_%d' % user_id,good_id,count)

        # Calculate the total number of items in the shopping cart
        cart_total = 0
        cart_list = redis_conn.hvals('cart_%d' % user_id)
        for item in cart_list:
            cart_total += int(item)
        
        return JsonResponse({"res":1,"msg":"Update the shopping cart quantity successfully","cart_total":cart_total})

class CartDelView(View):
    
    def post(self,request):
        good_id = request.POST.get('good_id')
        if not request.user.is_authenticated:
            return JsonResponse({"res":0,"msg":"not logged in"})
        if not good_id:
            return JsonResponse({"res":0,"msg":"Parameter error"})
        try:
            GoodsSKU.objects.get(id=good_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"res":0,"msg":"Without this product, please do not operate maliciously"})

        user_id = request.user.id
        redis_conn = get_redis_connection("default")
        redis_conn.hdel('cart_%d' % user_id,good_id) # Delete the current product shopping cart data
        cart_len = redis_conn.hlen('cart_%d' % user_id)
        cart_total = 0
        cart_list = redis_conn.hvals('cart_%d' % user_id)
        for item in cart_list:
            cart_total += int(item)
        
        return JsonResponse({"res":1,"msg":"successfully deleted","cart_len":cart_len,"cart_total":cart_total})
