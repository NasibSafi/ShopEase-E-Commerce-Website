from celery import Celery
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings

# django environment configuration (celery and django run in different processes, so you need to import django configuration)
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # 从 app/wsgi.py中拷贝过来
django.setup()

# You need to register the django application before you can operate on these model classes
from goods.models import GoodsType, IndexCreatoryGoods, IndexGoodsBanner, IndexPromotion

# Connect to the 8th redis database Celery ('package name. file name') => Otherwise, run `celery -A celery_tasks.tasks worker -l info` command in the ./ShopEase/app directory and django will not be found app module in environment configurationapp_celery = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379//8')

app_celery = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379//8')

@app_celery.task
def send_email_task(user_name,email,token):
        subject = 'Fresh Everyday welcome message'
        message = '<h1>%s, Welcome to become a registered member of Fresh Everyday</h1>Please click the link below to activate your account<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (user_name, token, token)
        send_mail(subject,'',settings.EMAIL_HOST_USER,[email],html_message=message)


@app_celery.task
def generate_static_indexhtml():
        '''Generate home page static page'''
        types = GoodsType.objects.all() # Get product type information
        banners = IndexGoodsBanner.objects.all().order_by('index') # Get carousel data
        promotions = IndexPromotion.objects.all().order_by('index') # Get promotional product data

        # Obtaining the home page category product display information
        for type in types:
                image_banners = IndexCreatoryGoods.objects.filter(type=type).order_by('index')
                title_banners = IndexCreatoryGoods.objects.filter(type=type,display_mode=0).order_by('index')
                type.image_banners = image_banners
                type.title_banners = title_banners
        # Organization Template Context
        context = {
                "types":types,
                "banners":banners,
                "promotions":promotions
        }
        # use template
        # 1.Load a template file and return a template object
        temp = loader.get_template('index.html')
        # 2. render template
        static_index_html = temp.render(context)

        # Generate static files corresponding to the home page
        # save_path = os.path.join(settings.BASE_DIR,'template\static_index.html')
        save_path = 'E:\\PythonProject\\py_fresh-everyday-main\\app\\templates\static_index.html'
        with open(save_path,'w',encoding='utf-8') as f:
                f.write(static_index_html)