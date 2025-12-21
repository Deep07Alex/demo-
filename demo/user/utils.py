import os
import requests
from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

# Admin email for notifications (from settings)
ADMIN_EMAIL = settings.ADMIN_ORDER_EMAIL

def send_otp_to_user(phone_number, otp, delivery_method='sms'):
    """Send OTP - unchanged"""
    try:
        clean_phone = phone_number.replace(' ', '')
        if not clean_phone.startswith('+'):
            clean_phone = f"+91{clean_phone}"
            
        if delivery_method == 'whatsapp':
            return send_otp_via_whatsapp(clean_phone, otp)
        else:
            return send_otp_via_fast2sms(clean_phone, otp)
            
    except Exception as e:
        print(f"[OTP ERROR] {str(e)}")
        return False, str(e)


def send_otp_via_fast2sms(phone, otp):
    """ONLY for OTP - unchanged"""
    try:
        indian_number = phone.replace('+91', '')
        url = "https://www.fast2sms.com/dev/bulkV2"
        headers = {
            'authorization': settings.FAST2SMS_API_KEY,
            'Content-Type': 'application/json'
        }
        
        message = f"Family BookStore: Your OTP is {otp}. Valid for 10 minutes. Don't share it."
        
        payload = {
            "route": "q",
            "message": message,
            "language": "english",
            "numbers": indian_number,
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if result.get('return') is True:
            return True, result.get('request_id')
        else:
            error = result.get('message', 'Unknown Fast2SMS error')
            return False, error
            
    except Exception as e:
        return False, f"Fast2SMS API failed: {str(e)}"


def send_otp_via_whatsapp(phone, otp):
    """ONLY for OTP - unchanged"""
    try:
        url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_ID}/messages"
        headers = {
            'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {
                "body": f"🏪 *Family BookStore OTP*\n\nYour code: *{otp}*\nValid for: 10 minutes\n\n⚠️ Do not share this code with anyone."
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if 'messages' in result and len(result['messages']) > 0:
            return True, result['messages'][0].get('id')
        else:
            error = result.get('error', {}).get('message', 'WhatsApp API error')
            return False, error
            
    except Exception as e:
        return False, f"WhatsApp API failed: {str(e)}"


def send_sms_message(phone_number, message_text):
    """
    ✅ NEW: Generic function to send any SMS message
    """
    try:
        # Clean phone: remove +91 and spaces
        clean_phone = phone_number.replace('+91', '').replace(' ', '').strip()
        
        # Ensure 10 digits
        if len(clean_phone) != 10:
            return False, "Phone must be exactly 10 digits"
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        headers = {
            'authorization': settings.FAST2SMS_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "route": "q",
            "message": message_text,
            "language": "english",
            "numbers": clean_phone,
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if result.get('return') is True:
            return True, result.get('request_id')
        else:
            error = result.get('message', 'Unknown Fast2SMS error')
            return False, error
            
    except Exception as e:
        return False, f"Fast2SMS API failed: {str(e)}"


def send_admin_order_notification(order, items):
    """
    Send detailed email to admin about new order
    """
    try:
        items_details = "\n".join([
            f"• {item.title} (Qty: {item.quantity}, Price: ₹{item.price})"
            for item in items
        ])
        
        subject = f'🛒 New Order Received - #{order.id}'
        
        message = f"""
Hello Admin,

A new order has been placed on Family BookStore!

═══════════════════════════════════════

📋 ORDER DETAILS:
Order ID: #{order.id}
Order Date: {order.created_at.strftime('%d-%b-%Y %I:%M %p')}
Status: {order.status.upper()}
Payment Method: {order.payment_method}

═══════════════════════════════════════

👤 CUSTOMER DETAILS:
Name: {order.full_name}
Phone: {order.phone_number}
Email: {order.email}

📍 SHIPPING ADDRESS:
{order.address}
{order.city}, {order.state} - {order.pin_code}

═══════════════════════════════════════

📦 ORDER ITEMS:
{items_details}

═══════════════════════════════════════

💳 PAYMENT SUMMARY:
Subtotal: ₹{order.subtotal}
Shipping: ₹{order.shipping}
TOTAL: ₹{order.total}

═══════════════════════════════════════

Delivery Type: {order.delivery_type}

Thank you!
Family BookStore System
        """.strip()
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=False,
        )
        
        logger.info(f"Admin notification sent for Order #{order.id}")
        return True, "Admin email sent successfully"
        
    except Exception as e:
        logger.error(f"Admin notification failed: {str(e)}")
        return False, str(e)


def send_customer_order_confirmation(order, items, delivery_method='sms'):
    """
    Send order confirmation to customer via SMS or WhatsApp
    """
    try:
        # Clean phone number
        phone = order.phone_number.replace(' ', '')
        if not phone.startswith('+'):
            phone = f"+91{phone}"
        
        # Format item names (max 3 for conciseness)
        item_names = [item.title for item in items[:3]]
        items_text = ", ".join(item_names)
        if len(items) > 3:
            items_text += f" and {len(items) - 3} more"
        
        # Format address
        address = f"{order.city}, {order.pin_code}"
        
        if delivery_method == 'whatsapp':
            # WhatsApp message with formatting
            message = (
                f"🏪 *Family BookStore - Order Confirmed!*\n\n"
                f"*Order ID:* #{order.id}\n"
                f"*Items:* {items_text}\n"
                f"*Total:* ₹{order.total}\n"
                f"*Delivery Address:* {address}\n\n"
                f"📦 *Estimated Delivery:* 3-6 business days\n"
                f"📞 *Need help?* Contact us at /contactinformation/\n\n"
                f"Thank you for shopping with us! 😊"
            )
            success, message_id = send_otp_via_whatsapp(phone, message)
            
        else:
            # SMS message (concise, within 160 chars)
            message = (
                f"Family BookStore: Order #{order.id} confirmed! "
                f"Items: {items_text}. Total: ₹{order.total}. "
                f"Delivery to: {address}. 3-6 days. "
                f"Help: /contactinformation/"
            )
            # ✅ Use the NEW generic SMS function
            success, message_id = send_sms_message(phone, message)
        
        if success:
            logger.info(f"Customer confirmation sent via {delivery_method} for Order #{order.id}")
        
        return success, message_id
        
    except Exception as e:
        logger.error(f"Customer notification failed: {str(e)}")
        return False, str(e)