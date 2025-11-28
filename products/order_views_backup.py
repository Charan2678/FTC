# Order Views with Email Notifications
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction, models
from products.models import product
from users.models import user
from products.models import Order, OrderItem, OrderStatusHistory
from django.core.mail import send_mail
from django.conf import settings
import json
import logging

# Simple email notification functions
def notify_order_placed(order, customer_email):
    """Send order confirmation email"""
    subject = f'Order Confirmation - Order #{order.id}'
    message = f'Dear Customer,\n\nYour order #{order.id} has been placed successfully.\n\nThank you for shopping with FTC Agricultural Marketplace!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email, settings.ADMIN_EMAIL]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        logger.error(f'Email sending failed: {e}')
        return False

def notify_order_status_change(order, new_status):
    """Send order status update email"""
    subject = f'Order Status Update - Order #{order.id}'
    message = f'Dear Customer,\n\nYour order #{order.id} status has been updated to: {new_status}\n\nThank you!'
    from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        # Send to customer if we have their email
        if hasattr(order, 'customer_email') and order.customer_email:
            send_mail(subject, message, from_email, [order.customer_email])
        return True
    except Exception as e:
        logger.error(f'Email sending failed: {e}')
        return False

def test_email_system():
    """Test email configuration"""
    try:
        send_mail(
            'Test Email from FTC',
            'This is a test email from FTC Agricultural Marketplace.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL]
        )
        return True
    except Exception as e:
        logger.error(f'Email test failed: {e}')
        return False

logger = logging.getLogger(__name__)

def place_order(request):
    """Handle customer order placement with email notifications"""
    if request.method == 'POST':
        try:
            # Get customer information
            customer_id = request.POST.get('customer_id')
            customer_email = request.POST.get('customer_email')
            customer_phone = request.POST.get('customer_phone')
            delivery_address = request.POST.get('delivery_address')
            order_notes = request.POST.get('order_notes', '')
            
            # Get cart items (assuming JSON format)
            cart_items = json.loads(request.POST.get('cart_items', '[]'))
            
            if not cart_items:
                messages.error(request, "No items in cart")
                return redirect('products:cart')
            
            # Get or create customer
            try:
                customer = user.objects.get(user_id=customer_id)
            except user.DoesNotExist:
                messages.error(request, "Customer not found")
                return redirect('users:login')
            
            # Calculate total amount
            total_amount = 0
            order_items_data = []
            
            for item in cart_items:
                try:
                    prod = product.objects.get(product_id=item['product_id'])
                    item_total = float(item['quantity']) * float(prod.product_price)
                    total_amount += item_total
                    
                    order_items_data.append({
                        'product': prod,
                        'quantity': int(item['quantity']),
                        'price': float(prod.product_price)
                    })
                except product.DoesNotExist:
                    messages.error(request, f"Product not found: {item['product_id']}")
                    return redirect('products:cart')
            
            # Create order with transaction
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    customer=customer,
                    total_amount=total_amount,
                    delivery_address=delivery_address,
                    customer_phone=customer_phone,
                    customer_email=customer_email,
                    order_notes=order_notes,
                    status='pending',
                    payment_status='pending'
                )
                
                # Create order items
                for item_data in order_items_data:
                    OrderItem.objects.create(
                        order=order,
                        product=item_data['product'],
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    status='pending',
                    notes='Order placed successfully'
                )
                
                # Send email notifications
                try:
                    email_sent = notify_order_placed(order)
                    if email_sent:
                        logger.info(f"Email notifications sent for order #{order.order_id}")
                    else:
                        logger.warning(f"Failed to send email notifications for order #{order.order_id}")
                except Exception as e:
                    logger.error(f"Email notification error for order #{order.order_id}: {str(e)}")
                
                messages.success(request, f"Order placed successfully! Order ID: #{order.order_id}")
                return redirect('products:order_confirmation', order_id=order.order_id)
        
        except Exception as e:
            logger.error(f"Order placement error: {str(e)}")
            messages.error(request, "Failed to place order. Please try again.")
            return redirect('products:cart')
    
    return render(request, 'products/place_order.html')


def order_confirmation(request, order_id):
    """Display order confirmation page"""
    try:
        order = get_object_or_404(Order, order_id=order_id)
        
        context = {
            'order': order,
            'order_items': order.order_items.all(),
            'total_items': order.get_total_items()
        }
        
        return render(request, 'products/order_confirmation.html', context)
    
    except Exception as e:
        logger.error(f"Order confirmation error: {str(e)}")
        messages.error(request, "Order not found")
        return redirect('products:product_list')


@csrf_exempt
@require_http_methods(["POST"])
def quick_order_api(request):
    """API endpoint for quick order placement (AJAX)"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['customer_id', 'customer_email', 'customer_phone', 'delivery_address', 'items']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'Missing required field: {field}'})
        
        # Get customer
        try:
            customer = user.objects.get(user_id=data['customer_id'])
        except user.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer not found'})
        
        # Calculate total and prepare items
        total_amount = 0
        order_items_data = []
        
        for item in data['items']:
            try:
                prod = product.objects.get(product_id=item['product_id'])
                item_total = float(item['quantity']) * float(prod.product_price)
                total_amount += item_total
                
                order_items_data.append({
                    'product': prod,
                    'quantity': int(item['quantity']),
                    'price': float(prod.product_price)
                })
            except product.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Product not found: {item["product_id"]}'})
        
        # Create order
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                delivery_address=data['delivery_address'],
                customer_phone=data['customer_phone'],
                customer_email=data['customer_email'],
                order_notes=data.get('order_notes', ''),
                status='pending',
                payment_status='pending'
            )
            
            # Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            # Send email notifications
            email_sent = notify_order_placed(order)
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id,
                'total_amount': float(order.total_amount),
                'email_sent': email_sent,
                'message': f'Order placed successfully! Order ID: #{order.order_id}'
            })
    
    except Exception as e:
        logger.error(f"Quick order API error: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Failed to place order'})


def update_order_status(request, order_id):
    """Update order status (Admin only) with email notification"""
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('users:login')
    
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, order_id=order_id)
            old_status = order.status
            new_status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            tracking_number = request.POST.get('tracking_number', '')
            
            if new_status in dict(Order.ORDER_STATUS_CHOICES).keys():
                order.status = new_status
                if tracking_number:
                    order.tracking_number = tracking_number
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    status=new_status,
                    notes=notes
                )
                
                # Send email notification to customer
                email_sent = notify_order_status_change(order, old_status, new_status, notes)
                
                if email_sent:
                    messages.success(request, f"Order status updated and customer notified via email")
                else:
                    messages.warning(request, f"Order status updated but email notification failed")
                
            else:
                messages.error(request, "Invalid status")
        
        except Exception as e:
            logger.error(f"Order status update error: {str(e)}")
            messages.error(request, "Failed to update order status")
    
    return redirect('admin:products_order_change', order_id)


def test_email_notifications(request):
    """Test email notification system with detailed diagnostics"""
    try:
        # Email diagnostic functionality simplified
        
        # Run comprehensive email diagnostic
        results = run_email_diagnostic()
        
        if results['console_mode']:
            return JsonResponse({
                'success': True,
                'message': 'Console mode active - Check terminal for email content',
                'details': 'Emails are printing to terminal. Switch to SMTP for real email delivery.',
                'instructions': fix_gmail_app_password_instructions()
            })
        elif results['django_ok']:
            return JsonResponse({
                'success': True,
                'message': 'Email configuration working! Check inbox (including spam folder).',
                'details': 'Email sent successfully via Django backend'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Email configuration has issues. Check Gmail App Password.',
                'details': 'SMTP connection failed',
                'instructions': fix_gmail_app_password_instructions()
            })
    
    except Exception as e:
        logger.error(f"Email test error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Email test failed: {str(e)}',
            'instructions': fix_gmail_app_password_instructions()
        })


def order_list(request):
    """List all orders (Admin view)"""
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('users:login')
    
    try:
        orders = Order.objects.all().order_by('-order_date')
        
        # Filter by status if provided
        status_filter = request.GET.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        # Search by order ID or customer name
        search = request.GET.get('search')
        if search:
            orders = orders.filter(
                models.Q(order_id__icontains=search) |
                models.Q(customer__user_name__icontains=search) |
                models.Q(customer_email__icontains=search)
            )
        
        context = {
            'orders': orders,
            'status_choices': Order.ORDER_STATUS_CHOICES,
            'current_status': status_filter,
            'search_query': search
        }
        
        return render(request, 'products/order_list.html', context)
    
    except Exception as e:
        logger.error(f"Order list error: {str(e)}")
        messages.error(request, "Failed to load orders")
        return redirect('admin:index')


def customer_orders(request):
    """List customer's own orders"""
    try:
        # Get customer from session or login
        customer_id = request.session.get('user_id')
        if not customer_id:
            messages.error(request, "Please login to view your orders")
            return redirect('users:login')
        
        customer = get_object_or_404(user, user_id=customer_id)
        orders = Order.objects.filter(customer=customer).order_by('-order_date')
        
        context = {
            'orders': orders,
            'customer': customer
        }
        
        return render(request, 'products/my_orders.html', context)
    
    except Exception as e:
        logger.error(f"Customer orders error: {str(e)}")
        messages.error(request, "Failed to load your orders")
        return redirect('pages:index')