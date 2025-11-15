from django.shortcuts import render, get_object_or_404
from .models import Book

def home_page(request):
    # Filter books by category for each section
    context = {
        'sale_books': Book.objects.filter(category='self_help', on_sale=True).order_by('title'),
        'romance_books': Book.objects.filter(category='romance').order_by('title'),
        'trading_finance_books': Book.objects.filter(category='trading_finance').order_by('title'),
        'manga_books': Book.objects.filter(category='manga').order_by('title'),
    }
    return render(request, 'index.html', context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book_detail.html', {'book': book})