# sale/models.py
from django.db import models

class Category(models.TextChoices):
    SALE = 'sale', 'Self-Help (On Sale)'
    ROMANCE = 'romance', 'Romance'
    TRADING = 'trading', 'Trading & Finance'
    MANGA = 'manga' , 'Manga'

class SaleBook(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sale_books/')
    old_price = models.DecimalField(max_digits=8, decimal_places=2)
    new_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_on_sale = models.BooleanField(default=True)
    # ADD THIS FIELD
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.SALE)

    def __str__(self):
        return self.title