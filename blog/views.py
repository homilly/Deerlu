from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello ,world! I am in bolg view now.")
# Create your views here.
