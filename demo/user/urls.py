from django.urls import path
from . import views

urlpatterns = [
    # ============ EMAIL VERIFICATION ============
    path("send-email-otp/", views.send_email_otp, name="send_email_otp"),
    path("verify-email-otp/", views.verify_email_otp, name="verify_email_otp"),

    # ============ CART OPERATIONS ============
    path("clear/", views.clear_cart, name="clear_cart"),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("addons/update/", views.update_cart_addons, name="update_cart_addons"),
    path("addons/get/", views.get_cart_addons, name="get_cart_addons"),
    path("items/", views.get_cart_items, name="get_cart_items"),
    path("remove/", views.remove_from_cart, name="remove_from_cart"),
    path("update/", views.update_cart_quantity, name="update_cart_quantity"),

    # ============ PAYMENT & SHIPPING ============
    path("initiate-payment/", views.initiate_payu_payment, name="initiate_payu_payment"),
    path("calculate-shipping/", views.calculate_shipping, name="calculate_shipping"),
]
