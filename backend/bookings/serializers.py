from rest_framework import serializers
from django.utils import timezone

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'rental_property',
            'user',
            'check_in',
            'check_out',
            'guests',
            'price_per_night_snapshot',
            'total_price',
            'status',
            'created_at',
            'updated_at',
            'cancelled_at'
            ]
        read_only_fields = [
            'id',
            'price_per_night_snapshot',
            'total_price',
            'status',
            'created_at',
            'updated_at',
            'cancelled_at',
            'user'
            ]
        
        
    def validate(self, attrs):
        request = self.context.get('request')
        
        rental_property = attrs.get('rental_property')
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        guests = attrs.get('guests')
        
        if request is None and not request.user.is_anonymous:
            raise serializers.ValidationError("User is not authenticated.")
        
        if not rental_property.is_rent():
            raise serializers.ValidationError("Only properties with 'rent' deal type can be booked.")

        if not rental_property.is_published():
            raise serializers.ValidationError("Only published properties can be booked.")
        
        if check_in < timezone.localdate():
            raise serializers.ValidationError("Check in date cannot be in the past.")
        
        if check_out <= check_in:
            raise serializers.ValidationError("Check out date must be after check in date.")
        
        if guests > rental_property.guests:
            raise serializers.ValidationError("Number of guests cannot exceed property's maximum guests.")
        
        overlapping_bookings = Booking.objects.filter(rental_property=rental_property, status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED], check_in__lt=check_out, check_out__gt=check_in)
        if overlapping_bookings.exists():
            raise serializers.ValidationError("Property is already booked for the specified dates.")
        
        if request and request.user.is_authenticated and request.user == rental_property.owner:
            raise serializers.ValidationError("You cannot book your own property.")
        
        return attrs
    
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            raise serializers.ValidationError("User is not authenticated.")
        
        user = request.user
        
        rental_property = validated_data['rental_property']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        nights = (check_out - check_in).days
        price = rental_property.price_per_night
        validated_data['user'] = user
        validated_data['price_per_night_snapshot'] = price
        validated_data['total_price'] = price * nights

        return super().create(validated_data)