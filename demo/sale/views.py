from django.shortcuts import render
from .models import SaleBook
# Create your views here.


def sale_page(request):
    books = SaleBook.objects.filter(category='sale').order_by('title')
    return render(request, 'pages/sale.html', {'salebooks': books})

def romance_page(request):
    books = SaleBook.objects.filter(category='romance').order_by('title')
    return render(request, 'pages/romance.html', {'romancebooks': books})

def trading_finance_page(request):
    books = SaleBook.objects.filter(category='trading').order_by('title')
    return render(request, 'pages/trading_finance.html', {'trading': books})

def manga_page(request):
    books = SaleBook.objects.filter(category='trading').order_by('title')
    return render(request, 'pages/manga.html', {'manga': books})