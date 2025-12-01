from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Book

def home_page(request):
    context = {
        'sale_books': Book.objects.filter(category='self_help', on_sale=True).order_by('title'),
        'romance_books': Book.objects.filter(category='romance').order_by('title'),
        'trading_finance_books': Book.objects.filter(category='trading_finance').order_by('title'),
        'manga_books': Book.objects.filter(category='manga').order_by('title'),
        'robert_greene_special_books': Book.objects.filter(category='robert_greene_special').order_by('title'),
        'mythology_books': Book.objects.filter(category='mythology').order_by('title'),
        'hindi_books': Book.objects.filter(category='hindi').order_by('title'),
        'preloved_bestsellers_books': Book.objects.filter(category='preloved_bestsellers').order_by('title'),
        'new_arrivals_books': Book.objects.filter(category='new_arrivals').order_by('title'),
    }
    return render(request, 'index.html', context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'pages/book_detail.html', {'book': book})

CATEGORY_SLUG_MAP = {
    'sale': {'category': 'self_help', 'on_sale': True, 'name': 'Self-Help On Sale'},
    'romance': {'category': 'romance', 'on_sale': False, 'name': 'Romance'},
    'trading-finance': {'category': 'trading_finance', 'on_sale': False, 'name': 'Trading & Finance'},
    'manga': {'category': 'manga', 'on_sale': False, 'name': 'Manga'},
    'robert-greene-special': {'category': 'robert_greene_special', 'on_sale': False, 'name': 'Robert Greene Special'},
    'mythology': {'category': 'mythology', 'on_sale': False, 'name': 'Mythology'},
    'hindi-books': {'category': 'hindi', 'on_sale': False, 'name': 'Hindi Books'},
    'preloved-bestsellers': {'category': 'preloved_bestsellers', 'on_sale': False, 'name': 'Preloved Bestsellers'},
    'new-arrivals': {'category': 'new_arrivals', 'on_sale': False, 'name': 'New Arrivals'},
}

def category_view(request, category_slug):
    """Generic view for all category pages"""
    config = CATEGORY_SLUG_MAP.get(category_slug)
    if not config:
        raise Http404(f"Category '{category_slug}' not found")

    books = Book.objects.filter(category=config['category'])
    if config['on_sale']:
        books = books.filter(on_sale=True)
    
    books = books.order_by('title')
    
    return render(request, 'pages/category_detail.html', {
        'books': books,
        'category_name': config['name'],
        'category_slug': category_slug,
    })