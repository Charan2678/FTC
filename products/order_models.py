# Order Management and Email Notification System
from django.db import models
from django.contrib.auth.models import User
from users.models import user
from products.models import product
from django.utils import timezone

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(user, on_delete=models.CASCADE, related_name='customer_orders')
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Customer Information
    delivery_address = models.TextField()
    customer_phone = models.CharField(max_length=15, default='')
    customer_email = models.EmailField(max_length=255)
    
    # Order Details
    order_notes = models.TextField(blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer.user_name}"
    
    def get_total_items(self):
        return self.order_items.count()
    
    def get_order_summary(self):
        items = []
        for item in self.order_items.all():
            items.append({
                'product': item.product.product_name,
                'quantity': item.quantity,
                'price': item.price,
                'total': item.get_total_price()
            })
        return items

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"
    
    def get_total_price(self):
        return self.quantity * self.price

    class Meta:
        db_table = 'order_items'


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.order.order_id} - {self.status} at {self.changed_at}"

    class Meta:
        db_table = 'order_status_history'
        ordering = ['-changed_at']