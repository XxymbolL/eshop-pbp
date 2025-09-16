from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ShoesForm
from main.models import Shoes
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    shoes_list = Shoes.objects.prefetch_related('sizes').all()
    context = {
        'title': 'Alpha Shoes',
        'npm': '2406422922',
        'name': 'Rifqy Pradipta Kurniawan',
        'class': 'PBP B',
        'shoes_list': shoes_list,
    }
    return render(request, "main.html", context)

def create_shoes(request):
    form = ShoesForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_main')
    return render(request, "create_shoes.html", {'form': form})

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