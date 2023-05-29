"""
URL configuration for phoneradar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views as main_views
from PhoneReview import views as phonereview_views


urlpatterns = [
    path('login/', phonereview_views.login),
    path('logout/', phonereview_views.logout),

    path('overview/instru/', phonereview_views.overview),
    path('overview/attendance/', phonereview_views.attendance),
    path('overview/add/', phonereview_views.overview_add),
    path('overview/modif/', phonereview_views.overview_modif),
    path('overview/delete/', phonereview_views.overview_delete),


    path('overview/parent/', phonereview_views.overview_parent),

    path('model/', phonereview_views.model),
    path('model/add/', phonereview_views.model_add),

    path('brandapi/', phonereview_views.BrandApiView.as_view()),
    path('brandapi/<int:pk>/', phonereview_views.BrandDetailApiView.as_view()),

    path('review/', phonereview_views.review),
    path('review/add/', phonereview_views.review_add),


    path('index/', main_views.index),
    path('admin/', admin.site.urls),
]
