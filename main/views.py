from django.shortcuts import render

def show_main(request):
    context = {
        'title': 'Alpha Shoes',
        'npm' : '2406422922',
        'name': 'Rifqy Pradipta Kurniawan',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
