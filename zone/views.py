from django.shortcuts import render
from django.http import HttpResponse
from .models import Article


def index(request):
    return HttpResponse("Hello world")


def news(request):
    a_news = Article.objects.all()
    context = {'article_list': a_news}
    return render(request, 'zone/news.html', context)


def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'zone/year_archive.html', context)


def month_archive(request, year, month):
    a_list = Article.objects.filter(pub_date__year=year, pub_date__month=month)
    context = {'year': year, 'month': month, 'article_list':a_list}
    return render(request, 'zone/month_archive.html', context)


def article_detail(request, article_id):
    a_list = Article.objects.filter(id=article_id)
    context = {'article_list': a_list}
    return render(request, 'zone/article_detail.html', context)
