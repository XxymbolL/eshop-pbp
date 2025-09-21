from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import ShoesForm, OneSizeForm
from main.models import ShoeSize, Shoes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")

    qs = Shoes.objects.prefetch_related('sizes')

    if filter_type == "my":
        qs = qs.filter(user=request.user)

    context = {
        'title': 'Alpha Shoes',
        'npm': '2406422922',
        'name': request.user.username,
        'class': 'PBP B',
        'shoes_list': qs,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)


def create_shoes(request):
    shoe_form = ShoesForm(request.POST or None)
    size_form = OneSizeForm(request.POST or None)

    if request.method == "POST" and shoe_form.is_valid() and size_form.is_valid():
        shoes = shoe_form.save(commit=False)
        shoes.user = request.user
        shoes.save()
        ShoeSize.objects.create(
            shoes=shoes,
            size=size_form.cleaned_data["size"],
            stock=size_form.cleaned_data["stock"],
        )
        return redirect('main:show_main')

    context = {
        'form': shoe_form,
        'size_form': size_form,
    }
    return render(request, "create_shoes.html", context)

@login_required(login_url='/login')
def show_shoes(request, id):
    shoes = get_object_or_404(Shoes, pk=id)
    context = {
        'shoes': shoes,
    }
    return render(request, "shoes_detail.html", context)

def show_xml(request):
     shoes_list = Shoes.objects.all()
     xml_data = serializers.serialize("xml", shoes_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    shoes_list = Shoes.objects.all()
    json_data = serializers.serialize("json", shoes_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, shoes_id):
   try:
    shoes_item = Shoes.objects.filter(pk=shoes_id)
    xml_data = serializers.serialize("xml", shoes_item)
    return HttpResponse(xml_data, content_type="application/xml")
   except Shoes.DoesNotExist:
       return HttpResponse(status=404)


def show_json_by_id(request, shoes_id):
    try:
        shoes_item = Shoes.objects.get(pk=shoes_id)
        json_data = serializers.serialize("json", [shoes_item])
        return HttpResponse(json_data, content_type="application/json")
    except Shoes.DoesNotExist:
        return HttpResponse(status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response