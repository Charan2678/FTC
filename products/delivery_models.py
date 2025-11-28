# Real-time Delivery Tracking System
from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid

class DeliveryPartner(models.Model):
    """Delivery service providers"""
    partner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    service_areas = models.TextField(help_text="Comma-separated list of areas served")
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    per_km_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class DeliveryDriver(models.Model):
    """Individual delivery drivers"""
    driver_id = models.AutoField(primary_key=True)
    partner = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=50, choices=[
        ('bike', 'Motorcycle'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck')
    ])
    vehicle_number = models.CharField(max_length=20)
    current_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    current_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_deliveries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.vehicle_number}"

class DeliveryOrder(models.Model):
    """Delivery tracking for orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending Pickup'),
        ('assigned', 'Driver Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed'),
        ('returned', 'Returned to Sender')
    ]
    
    delivery_id = models.AutoField(primary_key=True)
    tracking_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    order = models.ForeignKey('products.order', on_delete=models.CASCADE)
    partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Addresses
    pickup_address = models.TextField()
    pickup_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    pickup_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    
    delivery_address = models.TextField()
    delivery_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    delivery_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_pickup_time = models.DateTimeField(null=True, blank=True)
    actual_pickup_time = models.DateTimeField(null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    
    # Costs
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    
    # Special instructions
    delivery_instructions = models.TextField(blank=True)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=15)
    
    # Proof of delivery
    delivery_photo = models.ImageField(upload_to='delivery_proof/', null=True, blank=True)
    signature_image = models.ImageField(upload_to='delivery_signatures/', null=True, blank=True)
    delivery_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery {self.tracking_number} - {self.status}"
    
    @property
    def is_delayed(self):
        """Check if delivery is delayed"""
        if self.estimated_delivery_time and timezone.now() > self.estimated_delivery_time:
            return self.status not in ['delivered', 'failed', 'returned']
        return False

class DeliveryTracking(models.Model):
    """Real-time location tracking for deliveries"""
    tracking_id = models.AutoField(primary_key=True)
    delivery = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='tracking_updates')
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.CASCADE)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional metadata
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    accuracy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Tracking {self.delivery.tracking_number} at {self.timestamp}"

class DeliveryStatusUpdate(models.Model):
    """Status change history for deliveries"""
    update_id = models.AutoField(primary_key=True)
    delivery = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='status_updates')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    updated_by = models.CharField(max_length=100)  # Driver name or system
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    location_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    location_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.delivery.tracking_number}: {self.old_status} → {self.new_status}"

class DeliveryRoute(models.Model):
    """Optimized delivery routes for multiple orders"""
    route_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.CASCADE)
    date = models.DateField()
    deliveries = models.ManyToManyField(DeliveryOrder, through='RouteDelivery')
    
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    estimated_duration = models.DurationField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    
    route_data = models.JSONField(null=True, blank=True)  # Store route coordinates
    is_optimized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Route {self.route_id} - {self.driver.name} ({self.date})"

class RouteDelivery(models.Model):
    """Junction table for route deliveries with sequence"""
    route = models.ForeignKey(DeliveryRoute, on_delete=models.CASCADE)
    delivery = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE)
    sequence_number = models.IntegerField()
    estimated_arrival = models.DateTimeField(null=True)
    actual_arrival = models.DateTimeField(null=True)
    
    class Meta:
        ordering = ['sequence_number']
        unique_together = ['route', 'sequence_number']