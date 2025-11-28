# Comprehensive Rating & Review System
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class ReviewCategory(models.Model):
    """Categories for different types of reviews"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductReview(models.Model):
    """Detailed product reviews with multiple criteria"""
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    order = models.ForeignKey('products.order', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Overall rating
    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Detailed ratings
    quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, blank=True
    )
    freshness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, blank=True
    )
    packaging_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, blank=True
    )
    value_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        null=True, blank=True
    )
    
    # Review content
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    
    # Media attachments
    images = models.JSONField(default=list, blank=True)  # Store image URLs
    videos = models.JSONField(default=list, blank=True)  # Store video URLs
    
    # Verification and moderation
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    moderation_notes = models.TextField(blank=True)
    
    # Interaction metrics
    helpful_votes = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']  # One review per user per product
        ordering = ['-created_at']
    
    @property
    def helpfulness_percentage(self):
        """Calculate helpfulness percentage"""
        if self.total_votes > 0:
            return (self.helpful_votes / self.total_votes) * 100
        return 0
    
    @property
    def average_detailed_rating(self):
        """Calculate average of detailed ratings"""
        ratings = [r for r in [self.quality_rating, self.freshness_rating, 
                              self.packaging_rating, self.value_rating] if r is not None]
        return sum(ratings) / len(ratings) if ratings else self.overall_rating
    
    def __str__(self):
        return f"{self.product.product_name} - {self.overall_rating}★ by {self.user.user_name}"

class FarmerReview(models.Model):
    """Reviews for farmers/suppliers"""
    review_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='farmer_reviews')
    reviewer = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='given_farmer_reviews')
    order = models.ForeignKey('products.order', on_delete=models.SET_NULL, null=True)
    
    # Ratings
    communication_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    delivery_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    product_quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Review content
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    would_buy_again = models.BooleanField()
    
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['farmer', 'reviewer', 'order']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Farmer {self.farmer.user_name} - {self.overall_rating}★"

class ReviewHelpfulness(models.Model):
    """Track review helpfulness votes"""
    vote_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    is_helpful = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']

class ReviewResponse(models.Model):
    """Farmer/seller responses to reviews"""
    response_id = models.AutoField(primary_key=True)
    review = models.OneToOneField(ProductReview, on_delete=models.CASCADE)
    responder = models.ForeignKey('users.user', on_delete=models.CASCADE)
    response_text = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.review.title}"

class ReviewModeration(models.Model):
    """Review moderation and flagging"""
    FLAG_REASONS = [
        ('spam', 'Spam'),
        ('fake', 'Fake Review'),
        ('inappropriate', 'Inappropriate Content'),
        ('offensive', 'Offensive Language'),
        ('irrelevant', 'Irrelevant Content'),
        ('personal_info', 'Contains Personal Information'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('requires_edit', 'Requires Edit')
    ]
    
    moderation_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    flagged_by = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True)
    flag_reason = models.CharField(max_length=20, choices=FLAG_REASONS)
    flag_details = models.TextField(blank=True)
    
    moderator = models.ForeignKey('users.user', on_delete=models.SET_NULL, null=True, related_name='moderated_reviews')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    moderation_notes = models.TextField(blank=True)
    
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Flag: {self.review.title} - {self.flag_reason}"

class ReviewIncentive(models.Model):
    """Incentives for leaving reviews"""
    INCENTIVE_TYPES = [
        ('points', 'Loyalty Points'),
        ('discount', 'Discount Coupon'),
        ('cashback', 'Cashback'),
        ('free_shipping', 'Free Shipping')
    ]
    
    incentive_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    incentive_type = models.CharField(max_length=15, choices=INCENTIVE_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Conditions
    min_rating_required = models.IntegerField(default=1)
    min_review_length = models.IntegerField(default=50)
    requires_photo = models.BooleanField(default=False)
    requires_verified_purchase = models.BooleanField(default=True)
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ReviewReward(models.Model):
    """Track awarded review incentives"""
    reward_id = models.AutoField(primary_key=True)
    review = models.OneToOneField(ProductReview, on_delete=models.CASCADE)
    incentive = models.ForeignKey(ReviewIncentive, on_delete=models.CASCADE)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    
    reward_code = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    is_redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    
    awarded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.incentive.name} for {self.user.user_name}"

class ProductRating(models.Model):
    """Aggregated rating statistics per product"""
    product = models.OneToOneField('products.product', on_delete=models.CASCADE, related_name='rating_stats')
    
    # Overall statistics
    total_reviews = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Rating distribution
    five_star_count = models.IntegerField(default=0)
    four_star_count = models.IntegerField(default=0)
    three_star_count = models.IntegerField(default=0)
    two_star_count = models.IntegerField(default=0)
    one_star_count = models.IntegerField(default=0)
    
    # Detailed averages
    avg_quality_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_freshness_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_packaging_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    avg_value_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def update_statistics(self):
        """Recalculate all rating statistics"""
        reviews = self.product.reviews.filter(is_approved=True)
        
        self.total_reviews = reviews.count()
        if self.total_reviews > 0:
            # Overall rating
            self.average_rating = reviews.aggregate(
                avg=models.Avg('overall_rating')
            )['avg'] or 0
            
            # Rating distribution
            self.five_star_count = reviews.filter(overall_rating=5).count()
            self.four_star_count = reviews.filter(overall_rating=4).count()
            self.three_star_count = reviews.filter(overall_rating=3).count()
            self.two_star_count = reviews.filter(overall_rating=2).count()
            self.one_star_count = reviews.filter(overall_rating=1).count()
            
            # Detailed ratings
            self.avg_quality_rating = reviews.aggregate(
                avg=models.Avg('quality_rating')
            )['avg'] or 0
            self.avg_freshness_rating = reviews.aggregate(
                avg=models.Avg('freshness_rating')
            )['avg'] or 0
            self.avg_packaging_rating = reviews.aggregate(
                avg=models.Avg('packaging_rating')
            )['avg'] or 0
            self.avg_value_rating = reviews.aggregate(
                avg=models.Avg('value_rating')
            )['avg'] or 0
        
        self.save()
    
    def __str__(self):
        return f"{self.product.product_name} - {self.average_rating}★ ({self.total_reviews} reviews)"