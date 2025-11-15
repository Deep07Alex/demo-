from django.urls import path , include
from . import views
from sale import views as sale_views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('sale/', sale_views.sale_page, name='sale'),
    path('romance/', sale_views.romance_page, name='romance'),
    path('trading-finance/', sale_views.trading_finance_page, name='trading-finance'),
    path('manga/', sale_views.manga_page, name='manga'),
]