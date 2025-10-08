from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from main.forms import ShoesForm, SizeFormSet
from main.models import ShoeSize, Shoes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch
from django.views.decorators.http import require_http_methods
from django.utils.html import strip_tags
from main.models import SIZE_CHOICES, ShoeSize, Shoes


def _shoe_dict(obj, request=None):
    rel = list(obj.sizes.all())
    sizes = [{"size": s.size, "stock": s.stock} for s in rel]
    return {
        "id": str(obj.id),
        "name": obj.name,
        "price": obj.price,
        "description": obj.description or "",
        "thumbnail": obj.thumbnail or "",
        "total_stock": sum(s.stock for s in rel),
        "sizes": sizes,
        "user_id": obj.user_id,
        "username": obj.user.username if obj.user_id else None,
        "is_owner": bool(
            request and request.user.is_authenticated and obj.user_id == request.user.id
        ),
    }

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

@login_required(login_url='/login')
def create_shoes(request):
    shoes = Shoes(user=request.user)
    if request.method == "POST":
        form = ShoesForm(request.POST, instance=shoes)
        formset = SizeFormSet(request.POST, instance=shoes)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Shoes created!")
            return redirect('main:show_main')
    else:
        form = ShoesForm(instance=shoes)
        formset = SizeFormSet(instance=shoes)
    return render(request, "create_shoes.html", {"form": form, "formset": formset})


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

@login_required(login_url='/login')
def edit_shoes(request, id):
    shoes = get_object_or_404(Shoes, pk=id)
    if request.method == "POST":
        form = ShoesForm(request.POST, instance=shoes)
        formset = SizeFormSet(request.POST, instance=shoes)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Shoes updated!")
            return redirect('main:show_main')
    else:
        form = ShoesForm(instance=shoes)
        formset = SizeFormSet(instance=shoes)
    return render(request, "edit_shoes.html", {"form": form, "formset": formset, "shoes": shoes})

def delete_shoes(request, id):
    shoes = get_object_or_404(Shoes, pk=id)
    shoes.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@require_http_methods(["POST"])
@login_required(login_url='/login')
def create_shoes_ajax(request):
    name = strip_tags(request.POST.get("name", "")).strip()
    price_raw = request.POST.get("price")
    description = strip_tags(request.POST.get("description") or "")
    thumbnail = (request.POST.get("thumbnail") or "").strip() or None

    try:
        price = int(price_raw or 0)
    except ValueError:
        return JsonResponse({"ok": False, "errors": ["Invalid price"]}, status=400)

    if not name or price < 0:
        return JsonResponse({"ok": False, "errors": ["Invalid data"]}, status=400)

    shoe = Shoes.objects.create(
        user=request.user,
        name=name,
        price=price,
        description=description,
        thumbnail=thumbnail,
    )

    sizes = request.POST.getlist("size[]")
    stocks = request.POST.getlist("stock[]")

    valid_sizes = {str(s) for (s, _label) in SIZE_CHOICES}
    seen = set()
    rows = []
    for i, sz in enumerate(sizes):
        s = str(sz)
        if s not in valid_sizes or s in seen:
            continue
        try:
            st = int(stocks[i])
        except (ValueError, IndexError):
            continue
        if st < 0:
            continue
        seen.add(s)
        rows.append(ShoeSize(shoes=shoe, size=s, stock=st))

    if rows:
        ShoeSize.objects.bulk_create(rows)

    return JsonResponse({"ok": True, "data": _shoe_dict(shoe, request)}, status=201)

@require_http_methods(["GET"])
@login_required(login_url='/login')
def shoes_json(request):
    qs = Shoes.objects.prefetch_related("sizes")
    if request.GET.get("filter") == "my":
        qs = qs.filter(user=request.user)
    data = [_shoe_dict(s, request) for s in qs]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
@login_required(login_url='/login')
def shoes_json_by_id(request, id):
    obj = get_object_or_404(Shoes.objects.prefetch_related("sizes"), pk=id)
    return JsonResponse(_shoe_dict(obj, request))


@require_http_methods(["POST"])
@login_required(login_url='/login')
def update_shoes_ajax(request, id):
    shoe = get_object_or_404(Shoes.objects.prefetch_related("sizes"), pk=id)
    if shoe.user_id != request.user.id:
        return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)

    name = strip_tags(request.POST.get("name", "")).strip()
    price_raw = request.POST.get("price")
    description = strip_tags(request.POST.get("description") or "")
    thumbnail = (request.POST.get("thumbnail") or "").strip() or None

    try:
        price = int(price_raw or 0)
    except ValueError:
        return JsonResponse({"ok": False, "error": "Invalid price"}, status=400)

    if not name or price < 0:
        return JsonResponse({"ok": False, "error": "Invalid data"}, status=400)

    shoe.name = name
    shoe.price = price
    shoe.description = description
    shoe.thumbnail = thumbnail
    shoe.save()

    sizes = request.POST.getlist("size[]")
    stocks = request.POST.getlist("stock[]")
    valid_sizes = {str(s) for (s, _label) in SIZE_CHOICES}

    ShoeSize.objects.filter(shoes=shoe).delete()
    rows, seen = [], set()
    for i, sz in enumerate(sizes):
        s = str(sz)
        if s not in valid_sizes or s in seen:
            continue
        try:
            st = int(stocks[i])
        except (ValueError, IndexError):
            continue
        if st < 0:
            continue
        seen.add(s)
        rows.append(ShoeSize(shoes=shoe, size=s, stock=st))
    if rows:
        ShoeSize.objects.bulk_create(rows)

    return JsonResponse({"ok": True, "data": _shoe_dict(shoe, request)})


@require_http_methods(["POST"])
@login_required(login_url='/login')
def delete_shoes_ajax(request, id):
    shoe = get_object_or_404(Shoes, pk=id)
    if shoe.user_id != request.user.id:
        return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)
    shoe.delete()
    return JsonResponse({"ok": True})

@require_http_methods(["POST"])
def login_ajax(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        resp = JsonResponse({
            "ok": True,
            "username": user.username,
            "redirect": reverse("main:show_main"),
        })
        resp.set_cookie('last_login', str(datetime.datetime.now()))
        return resp
    # build nice error messages
    errors = {field: [str(m) for m in msgs] for field, msgs in form.errors.items()}
    return JsonResponse({"ok": False, "errors": errors}, status=400)


@require_http_methods(["POST"])
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "ok": True,
            "redirect": reverse("main:login"),
        }, status=201)
    errors = []
    for field, msgs in form.errors.items():
        for m in msgs:
            errors.append(m)
    return JsonResponse({"ok": False, "errors": errors}, status=400)


@require_http_methods(["POST"])
def logout_ajax(request):
    logout(request)
    resp = JsonResponse({"ok": True, "redirect": reverse("main:login")})
    resp.delete_cookie('last_login')
    return resp
