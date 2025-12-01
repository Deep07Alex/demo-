from django.urls import path 
from . import views

urlpatterns = [
   path('', views.productcatagory, name="productcatagory"),
   path('<str:category_type>/', views.product_category_detail, name="product_category_detail"),
]