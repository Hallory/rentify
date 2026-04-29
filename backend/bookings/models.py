from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'
        
    rental_property = models.ForeignKey('properties.Property',related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User',related_name='bookings', on_delete=models.CASCADE)
    
    check_in = models.DateField()
    check_out = models.DateField()
    
    guests = models.PositiveIntegerField()
    
    price_per_night_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError("Check out date must be after check in date.")
        
        
        if self.property_id:
            if not self.property.is_rent():
                raise ValidationError("Only properties with 'rent' deal type can be booked.")
            
            if not self.property.is_published():
                raise ValidationError("Only published properties can be booked.")
            
        if self.property_id and self.user_id:
            if self.property.owner_id == self.user_id:
                raise ValidationError("You cannot book your own property.")
            
        if self.property_id and self.guests:
            if self.guests > self.property.guests:
                raise ValidationError("Number of guests cannot exceed property's maximum guests.")        

        today = timezone.localdate()
        if self.check_in and self.check_in < today:
            raise ValidationError("Check in date cannot be in the past.")
        
        
    @property   
    def nights(self):
        if not self.check_in or not self.check_out:
            return 0
        return (self.check_out - self.check_in).days
    
    def __str__(self):
        return f"Booking #{self.id} - {self.property.title}"
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rental_property','check_in','check_out']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]