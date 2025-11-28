# Enhanced Product Models with Inventory Management
from django.db import models
from django.utils import timezone
from decimal import Decimal

class Category(models.Model):
    """Enhanced product categories"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class ProductInventory(models.Model):
    """Track product inventory and stock levels"""
    product = models.OneToOneField('products.product', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    max_stock_level = models.PositiveIntegerField(default=1000)
    reorder_point = models.PositiveIntegerField(default=10)
    last_restocked = models.DateTimeField(null=True, blank=True)
    
    @property
    def available_quantity(self):
        """Calculate available stock after reservations"""
        return max(0, self.stock_quantity - self.reserved_quantity)
    
    @property
    def is_low_stock(self):
        """Check if stock is below minimum level"""
        return self.available_quantity <= self.min_stock_level
    
    @property
    def needs_reorder(self):
        """Check if stock needs reordering"""
        return self.available_quantity <= self.reorder_point
    
    def reserve_stock(self, quantity):
        """Reserve stock for pending orders"""
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            self.save()
            return True
        return False
    
    def release_reservation(self, quantity):
        """Release reserved stock"""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.save()
    
    def consume_stock(self, quantity):
        """Consume stock for completed orders"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.reserved_quantity = max(0, self.reserved_quantity - quantity)
            self.save()
            return True
        return False
    
    def add_stock(self, quantity):
        """Add new stock"""
        self.stock_quantity += quantity
        self.last_restocked = timezone.now()
        self.save()

class ProductReview(models.Model):
    """Product reviews and ratings"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']  # One review per user per product
    
    def __str__(self):
        return f"{self.product.product_name} - {self.rating} stars by {self.user.user_name}"

class PriceHistory(models.Model):
    """Track product price changes"""
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, related_name='price_history')
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey('users.user', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.product_name}: {self.old_price} → {self.new_price}"

class WishlistItem(models.Model):
    """User wishlist functionality"""
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.user_name} - {self.product.product_name}"

class ProductView(models.Model):
    """Track product views for analytics"""
    product = models.ForeignKey('products.product', on_delete=models.CASCADE)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.product_name} viewed at {self.viewed_at}"