# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.



class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, default = '')
    product_type_id = models.CharField(max_length=255, default = "")
    product_company_id = models.CharField(max_length=255, default = "")
    product_price = models.CharField(max_length=255, default = "")
    product_image = models.CharField(max_length=255, null = True)
    product_description = models.TextField(default = "")
    product_stock = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.product_name


# Order Management Models
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
    customer_id = models.CharField(max_length=255, default='')  # Link to user table
    customer_name = models.CharField(max_length=255, default='')
    customer_email = models.EmailField(max_length=255, default='')
    customer_phone = models.CharField(max_length=15, default='')
    
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Order Details
    delivery_address = models.TextField(default='')
    order_notes = models.TextField(blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer_name}"
    
    def get_total_items(self):
        return self.order_items.count()

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, default='')  # Store product name at time of order
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Price at time of order
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def get_total_price(self):
        return self.quantity * self.price

    class Meta:
        db_table = 'order_items'


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, default='')
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.order.order_id} - {self.status} at {self.changed_at}"

    class Meta:
        db_table = 'order_status_history'
        ordering = ['-changed_at']    
