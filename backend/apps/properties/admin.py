from django.contrib import admin
from .models import Property, Amenity, PropertyImage


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name', 'slug')


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    
    
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'deal_type', 'price_per_night', 'is_published')
    list_filter = ('city', 'property_type', 'deal_type', 'status')
    search_fields = ('title', 'description','city','address','owner__email')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    filter_horizontal = ('amenities',)
    inlines = [PropertyImageInline]
    
    

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_main', 'order','created_at')
    list_filter = ('is_main',)

