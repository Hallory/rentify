from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    rental_property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='review')
    
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review #{self.id} for {self.rental_property.title}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']