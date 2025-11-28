# Advanced Inventory Management System
from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
import json

class InventoryLocation(models.Model):
    """Storage locations/warehouses"""
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    manager_name = models.CharField(max_length=100)
    manager_phone = models.CharField(max_length=15)
    capacity_cubic_meters = models.DecimalField(max_digits=10, decimal_places=2)
    temperature_controlled = models.BooleanField(default=False)
    min_temp = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    max_temp = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductInventory(models.Model):
    """Enhanced inventory tracking per product per location"""
    inventory_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    location = models.ForeignKey(InventoryLocation, on_delete=models.CASCADE)
    
    # Stock levels
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    damaged_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Thresholds and limits
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    economic_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    
    # Cost tracking
    average_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    last_purchase_price = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Dates
    last_restocked = models.DateTimeField(null=True, blank=True)
    last_sold = models.DateTimeField(null=True, blank=True)
    next_reorder_date = models.DateField(null=True, blank=True)
    
    # Product condition
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'location']
    
    @property
    def available_stock(self):
        """Available stock for sale"""
        return max(0, self.current_stock - self.reserved_stock - self.damaged_stock)
    
    @property
    def stock_status(self):
        """Current stock status"""
        available = self.available_stock
        if available <= 0:
            return 'out_of_stock'
        elif available <= self.minimum_stock:
            return 'low_stock'
        elif available <= self.reorder_point:
            return 'reorder_needed'
        elif available >= self.maximum_stock:
            return 'overstock'
        else:
            return 'in_stock'
    
    @property
    def days_until_expiry(self):
        """Days until product expires"""
        if self.expiry_date:
            return (self.expiry_date - timezone.now().date()).days
        return None
    
    @property
    def is_expiring_soon(self):
        """Check if product is expiring within 7 days"""
        days_left = self.days_until_expiry
        return days_left is not None and days_left <= 7
    
    def reserve_stock(self, quantity):
        """Reserve stock for pending orders"""
        if self.available_stock >= quantity:
            self.reserved_stock += quantity
            self.save()
            return True
        return False
    
    def release_stock(self, quantity):
        """Release reserved stock"""
        self.reserved_stock = max(0, self.reserved_stock - quantity)
        self.save()
    
    def consume_stock(self, quantity, update_cost=True):
        """Consume stock and update costs"""
        if self.available_stock >= quantity:
            self.current_stock -= quantity
            self.reserved_stock = max(0, self.reserved_stock - quantity)
            self.last_sold = timezone.now()
            self.save()
            
            # Create stock movement record
            StockMovement.objects.create(
                inventory=self,
                movement_type='sale',
                quantity=-quantity,
                reference_type='order',
                notes=f'Stock sold: {quantity} units'
            )
            return True
        return False

class StockMovement(models.Model):
    """Track all stock movements"""
    MOVEMENT_TYPES = [
        ('purchase', 'Purchase/Restock'),
        ('sale', 'Sale'),
        ('adjustment', 'Stock Adjustment'),
        ('damage', 'Damaged Goods'),
        ('return', 'Customer Return'),
        ('transfer', 'Location Transfer'),
        ('expired', 'Expired Products')
    ]
    
    movement_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Reference information
    reference_type = models.CharField(max_length=50, blank=True)  # 'order', 'purchase', 'adjustment'
    reference_id = models.IntegerField(null=True, blank=True)
    
    # Details
    notes = models.TextField(blank=True)
    performed_by = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Stock levels after this movement
    stock_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.movement_type}: {self.quantity} - {self.inventory.product.product_name}"

class StockAlert(models.Model):
    """Automated stock alerts and notifications"""
    ALERT_TYPES = [
        ('low_stock', 'Low Stock Level'),
        ('out_of_stock', 'Out of Stock'),
        ('overstock', 'Overstock'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('reorder_due', 'Reorder Due'),
        ('damaged_stock', 'Damaged Stock Reported')
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent')
    ]
    
    alert_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    message = models.TextField()
    
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    acknowledged_by = models.CharField(max_length=100, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def acknowledge(self, user):
        """Acknowledge the alert"""
        self.acknowledged_by = user
        self.acknowledged_at = timezone.now()
        self.save()
    
    def resolve(self, user):
        """Mark alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.is_active = False
        self.save()

class InventoryPrediction(models.Model):
    """AI-powered demand prediction"""
    prediction_id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    
    # Prediction period
    prediction_date = models.DateField()
    days_ahead = models.IntegerField()  # 7, 14, 30 days
    
    # Predicted values
    predicted_demand = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100%
    recommended_stock_level = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Factors considered
    seasonal_factor = models.DecimalField(max_digits=5, decimal_places=4, default=1.0)
    trend_factor = models.DecimalField(max_digits=5, decimal_places=4, default=1.0)
    promotional_impact = models.DecimalField(max_digits=5, decimal_places=4, default=1.0)
    
    # Model performance
    actual_demand = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['inventory', 'prediction_date', 'days_ahead']

class SupplierPerformance(models.Model):
    """Track supplier reliability and performance"""
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    
    # Performance metrics
    total_orders = models.IntegerField(default=0)
    on_time_deliveries = models.IntegerField(default=0)
    quality_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    price_competitiveness = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reliability_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Relationship details
    preferred_supplier = models.BooleanField(default=False)
    payment_terms = models.CharField(max_length=100, blank=True)
    lead_time_days = models.IntegerField(default=7)
    minimum_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def on_time_percentage(self):
        """Calculate on-time delivery percentage"""
        if self.total_orders > 0:
            return (self.on_time_deliveries / self.total_orders) * 100
        return 0
    
    def __str__(self):
        return self.name