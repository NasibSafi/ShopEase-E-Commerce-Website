from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from PhoneReview import models
from django import forms
from rest_framework import generics
from .Serializers import BrandSerializer
from .models import Brand


# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    user = request.POST.get("username")
    pwd = request.POST.get("pwd")
    user_object = models.UserAccount.objects.filter(userName=user, password=pwd).first()

    if user_object:
        request.session['user_info'] = {"id": user_object.id, 'userName': user_object.userName}
        return redirect('/overview')
    else:
        return render(request, 'login.html', {'error': "wrong user name or password"})


def logout(request):
    request.session.clear()
    return render(request, 'login.html')


def overview(request):
    queryset = models.Brand.objects.all().order_by("id")
    return render(request, 'overview.html', {"queryset": queryset})

def overview_parent(request):
    queryset = models.Brand.objects.all().order_by("id")
    return render(request, 'overview_parent.html', {"queryset": queryset})

def attendance(request):
    queryset = models.student.objects.all().order_by("id")
    return render(request, 'overview_parent.html', {"queryset": queryset})


def overview_add(request):
    if request.method == "GET":
        return render(request, 'overview_add.html')
    else:
        name = request.POST.get("name")
        origin = request.POST.get("origin")
        manufacturingSince = request.POST.get("manufacturingSince")
        models.Brand.objects.create(name=name, origin=origin, manufacturingSince=manufacturingSince)
        return redirect('/overview/')


def overview_delete(request):
    id = request.GET.get("id")
    models.Brand.objects.filter(id=id).delete()
    return redirect('/overview/')


def overview_modif(request):
    if request.method == "GET":
        id = request.GET.get("id")
        modify_object = models.Brand.objects.filter(id=id).first()
        return render(request, 'overview_modif.html',
                      {"id": modify_object.id, "name": modify_object.name, "origin": modify_object.origin,
                       "manufacturingSince": modify_object.manufacturingSince})
    else:
        id = request.GET.get('id')
        name = request.POST.get('name')
        origin = request.POST.get('origin')
        manufacturingSince = request.POST.get('manufacturingSince')
        models.Brand.objects.filter(id=id).update(name=name, origin=origin, manufacturingSince=manufacturingSince)
        return redirect('/overview/')


def model(request):
    queryset = models.Model.objects.all().order_by("id")
    for obj in queryset:
        (obj.id, obj.modelName, obj.launchDate, obj.platform, obj.brand_id)
    return render(request, 'model.html', {"queryset": queryset})


def model_add(request):
    platform_list = models.Model.platform_choice
    brand_list = models.Brand.objects.all()

    return render(request, 'model_add.html', {'platform_list': platform_list, 'brand_list': brand_list})


def review(request):
    queryset = models.Review.objects.all().order_by("id")
    return render(request, 'review.html', {"queryset": queryset})


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
                field.widget.attrs['class'] = "form-control"


def review_add(request):
    form = ReviewModelForm()
    return render(request, 'review_add.html', {"form": form})


class BrandApiView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer