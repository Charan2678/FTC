from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_order_notification_to_admin(order_details):
    """
    Send email notification to admin when a new order is placed
    """
    subject = f'New Order Received - Order #{order_details["order_id"]}'
    
    message = f"""
    New Order Notification
    =====================
    
    Order ID: #{order_details['order_id']}
    Customer Name: {order_details['customer_name']}
    Customer Email: {order_details['customer_email']}
    Customer Mobile: {order_details['customer_mobile']}
    
    Order Details:
    --------------
    Total Amount: ₹{order_details['order_total']}
    Payment Method: {order_details['payment_method']}
    Order Date: {order_details['order_date']}
    
    Delivery Address:
    ----------------
    {order_details['delivery_address']}
    
    Status: Pending Confirmation
    
    Please login to admin panel to confirm this order.
    
    ---
    FTC - Farmer to Consumer Platform
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        print(f"✅ Admin notification sent for Order #{order_details['order_id']}")
        return True
    except Exception as e:
        print(f"❌ Failed to send admin notification: {str(e)}")
        return False


def send_order_confirmation_to_customer(order_details):
    """
    Send order confirmation email to customer
    """
    subject = f'Order Confirmed - Order #{order_details["order_id"]}'
    
    message = f"""
    Dear {order_details['customer_name']},
    
    Thank you for your order! Your order has been successfully placed.
    
    Order Summary
    =============
    
    Order ID: #{order_details['order_id']}
    Order Date: {order_details['order_date']}
    Total Amount: ₹{order_details['order_total']}
    Payment Method: {order_details['payment_method']}
    
    Delivery Address:
    ----------------
    {order_details['delivery_address']}
    
    Order Status: {order_details['status']}
    
    You will receive another email once your order is confirmed by admin.
    
    Track your order: Login to your account and go to "My Orders"
    
    Thank you for shopping with FTC!
    
    ---
    FTC - Farmer to Consumer Platform
    Fresh from Farm to Your Home
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order_details['customer_email']],
            fail_silently=False,
        )
        print(f"✅ Customer confirmation sent to {order_details['customer_email']}")
        return True
    except Exception as e:
        print(f"❌ Failed to send customer confirmation: {str(e)}")
        return False


def send_order_status_update_to_customer(order_details, new_status):
    """
    Send email to customer when order status is updated by admin
    """
    subject = f'Order Status Update - Order #{order_details["order_id"]}'
    
    status_messages = {
        'Confirmed': 'Your order has been confirmed and is being prepared for dispatch.',
        'Packed': 'Your order has been packed and will be dispatched soon.',
        'Dispatched': 'Your order has been dispatched and is on its way!',
        'Delivered': 'Your order has been successfully delivered. Thank you for shopping with us!',
        'Cancelled': 'Your order has been cancelled. If you have any questions, please contact us.'
    }
    
    status_message = status_messages.get(new_status, f'Your order status has been updated to: {new_status}')
    
    message = f"""
    Dear {order_details['customer_name']},
    
    Order Status Update
    ===================
    
    Order ID: #{order_details['order_id']}
    New Status: {new_status}
    
    {status_message}
    
    Order Details:
    --------------
    Total Amount: ₹{order_details['order_total']}
    Order Date: {order_details['order_date']}
    
    Track your order: Login to your account and go to "My Orders"
    
    Thank you for choosing FTC!
    
    ---
    FTC - Farmer to Consumer Platform
    Fresh from Farm to Your Home
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order_details['customer_email']],
            fail_silently=False,
        )
        print(f"✅ Status update sent to {order_details['customer_email']} - Status: {new_status}")
        return True
    except Exception as e:
        print(f"❌ Failed to send status update: {str(e)}")
        return False


def send_admin_dashboard_notification(message_text):
    """
    Send general notification to admin dashboard (can be extended for SMS/push notifications)
    """
    print(f"📢 ADMIN NOTIFICATION: {message_text}")
    # This can be extended to send SMS or push notifications
    return True
