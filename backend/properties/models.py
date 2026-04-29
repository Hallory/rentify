from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
        ordering = ['name']


class Property(models.Model):

    class PropertyType(models.TextChoices):
        APARTMENT = 'apartment', 'Apartment'
        HOUSE = 'house', 'House'
        STUDIO = 'studio', 'Studio'
        ROOM = 'room', 'Room'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    class DealType(models.TextChoices):
        RENT = 'rent', 'Rent'
        SALE = 'sale', 'Sale'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PropertyType.choices)
    deal_type = models.CharField(max_length=20, choices=DealType.choices, default=DealType.RENT)

    guests = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area_sqm = models.PositiveIntegerField()

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100, default='Germany')
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20)

    amenities = models.ManyToManyField(Amenity, related_name='properties', blank=True)

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.DRAFT)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_published(self):
        return self.status == self.Status.PUBLISHED

    def is_rent(self):
        return self.deal_type == self.DealType.RENT

    def is_sale(self):
        return self.deal_type == self.DealType.SALE

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['property_type']),
            models.Index(fields=['deal_type']),
            models.Index(fields=['status']),
            models.Index(fields=['price_per_night']),
            models.Index(fields=['created_at']),
        ]


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

    class Meta:
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'
        ordering = ['order', 'created_at']