from django.urls import path
from . import views
from user import views as user_views

urlpatterns = [
    path('api/send-otp/', views.send_otp, name='send_otp'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/resend-otp/', views.resend_otp, name='resend_otp'),
]
