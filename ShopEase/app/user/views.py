from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from user.models import Address, User
from goods.models import GoodsSKU
from order.models import OrderGoods, OrderInfo
from itsdangerous import URLSafeSerializer
from django.conf import settings
from celery_tasks.tasks import send_email_task
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
import re

# Create your views here.
class RegisterView(View):

    def get(self,request):

        return render(request,'register.html')

    def post(self,request):

        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')

        if not all([user_name,pwd,email]):
            return render(request,'register.html',{'errmsg':'Parameter error'})
        
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱格式不正确'})

        # Check if username is duplicate
        try:
           user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request,'register.html',{'errmsg':'Username already exists'})

        user = User.objects.create_user(user_name,email,pwd)
        user.is_active = 0
        user.save()

        # Encrypt user information
        auth_s = URLSafeSerializer(settings.SECRET_KEY,'auth')
        token = auth_s.dumps(user.id)

        # Send mail asynchronously
        send_email_task.delay(user_name,email,token)

        return redirect(reverse('users:login')) # Registered successfully Jump to the login page

class ActiveView(View):

    def get(self,request,token):
        
        auth_s = URLSafeSerializer(settings.SECRET_KEY,'auth')  
        try:
            id = auth_s.loads(token)
            user = User.objects.get(id=id)
            user.is_active = 1
            user.save()
            return HttpResponse("Activation successful!")
        except User.DoesNotExist:
            return HttpResponse("Activation failed, there is no such user")
        except Exception as err:
            return HttpResponse('Error: Not Yet Activated')

class LoginView(View):

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username,password]):
            return render(request,'login.html',{'errmsg':"Parameter error"})

        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                next_url = request.GET.get('next',reverse('users:user_info')) # Obtain the address to be redirected after login, if there is next, it will jump to next, if not, it will jump to the product home page
                return redirect(next_url)
            else:
                return render(request,'login.html',{'errmsg':'This user is not active'})
        else:
            return render(request,'login.html',{'errmsg':'wrong user name or password'})

class LogoutView(View):

    def get(self,request):
        logout(request)
        return redirect(reverse('users:login'))

class UserInfoView(LoginRequiredMixin,View):

    def get(self,request):
        data = {
            "cur_page":"info"
        }
        redis_conn = get_redis_connection("default")
        user_id = request.user.id
        history_list = redis_conn.lrange('history_%d' % user_id,0,4) # Get the first 5 historical browsing records
        history_data = GoodsSKU.objects.filter(id__in=history_list)
        data.update(history_data=history_data)
        return render(request,'user_center_info.html',data)

class UserOrderView(LoginRequiredMixin,View):

    def get(self,request,page):
        # Get user order information
        user_id = request.user.id

        order_list = OrderInfo.objects.filter(user_id=user_id).order_by('-create_time')
        for order_item in order_list:
            order_goods = OrderGoods.objects.filter(order_info=order_item)
            order_item.order_goods = order_goods
            order_item.status_name = OrderInfo.ORDER_STATUS[order_item.status]

        order_page = Paginator(order_list,1) # 1 piece of data is a page number
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > order_page.num_pages:
            page = 1

        order_list = order_page.page(page)

        if order_page.num_pages < 5:
            page_range = range(1,order_page.num_pages+1)
        elif order_list.number <= 3:
            page_range = range(1,6)
        elif order_page.num_pages - order_list.number <= 3:
            page_range = range(order_page.num_pages-4,order_page.num_pages+1)
        else:
            page_range = range(order_list.number-2,order_list.number+3)
            
        data = {
            "cur_page":"order",
            "orders":order_list,
            "page_range":page_range
        }
        return render(request,'user_center_order.html',data)

class UserSiteView(LoginRequiredMixin,View):

    def get(self,request):
        data = {
            "cur_page":"site"
        }
        addr = Address.objects.getDefaultAddress(request.user)
        if addr:
            data['addr_str'] = "%s （%s 收） %s" % (addr.addr,addr.receiver,addr.phone)
        return render(request,'user_center_site.html',data)

    def post(self,request):
        data = {
            "cur_page":"site"
        }
        user = request.user
        
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver,addr,phone]):
            data["errmsg"] = "Parameter error - recipient, detailed address, phone number cannot be empty"
            return render(request,'user_center_site.html',data)
        if not re.match(r'^1[0-9]{10}$',phone):
            data['errmsg'] = "Mobile phone number is wrong"
            return render(request,'user_center_site.html',data)

        # If the user does not currently have a default address, the newly added address will be the default address
        default_addr = Address.objects.getDefaultAddress(user)
        if default_addr:
            is_default = False
        else:
            is_default = True
        
        Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone,is_default=is_default)

        return redirect(reverse('users:user_site'))

