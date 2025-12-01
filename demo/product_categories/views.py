from django.shortcuts import render
from django.http import Http404
from .models import product_variety, MarvelComic

# Map type codes to models and display names
PRODUCT_CATEGORY_MAP = {
    'MC': {'name': 'Marvel Comics', 'model': MarvelComic, 'template': 'comic'},
    'DC': {'name': 'DC Comics', 'model': None, 'template': 'default'},
    'MG': {'name': 'Manga Club', 'model': None, 'template': 'default'},
    'NA': {'name': 'New Arrivals', 'model': None, 'template': 'default'},
    'LAFK': {'name': 'Learning Apps For Kids', 'model': None, 'template': 'default'},
    'PF': {'name': 'Popular Fictions', 'model': None, 'template': 'default'},
    'AAL': {'name': 'All About Love', 'model': None, 'template': 'default'},
    'RF': {'name': 'Romance & Fictions', 'model': None, 'template': 'default'},
    'KB': {'name': 'Kids Books', 'model': None, 'template': 'default'},
    'MT': {'name': 'Mythology & Tails', 'model': None, 'template': 'default'},
}

def productcatagory(request):
    products = product_variety.objects.all().order_by('type')
    return render(request, 'pages/productcatagory.html', {'products_category': products})

def product_category_detail(request, category_type):
    """Generic view for product category details"""
    config = PRODUCT_CATEGORY_MAP.get(category_type)
    if not config:
        raise Http404(f"Product category '{category_type}' not found")
    
    # Get items if model exists
    items = []
    if config['model']:
        items = config['model'].objects.all().order_by('id')
    
    return render(request, 'pages/product_category_detail.html', {
        'category_name': config['name'],
        'items': items,
        'category_type': category_type,
    })