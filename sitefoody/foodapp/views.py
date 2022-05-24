from django.shortcuts import render


def index(request):
    return render(request, 'foodapp/index.html')


def about(request):
    return render(request, 'foodapp/index.html')