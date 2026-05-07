from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from analytics.models import PropertyView, SearchHistory
from bookings.models import Booking
from favorites.models import Favorite
from reviews.models import Review
from properties.models import Property, Amenity
from users.models import User


class Command(BaseCommand):
    help = "Seed demo data for Rentify"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")
        amenity_names = [
            "WiFi",
            "Kitchen",
            "Washer",
            "Parking",
            "Balcony",
            "Workspace",
            "Heating",
            "Air conditioning",
        ]
        amenities = []
        for name in amenity_names:
            amenity, _ = Amenity.objects.get_or_create(
                slug = slugify(name),
                defaults={"name": name}
            )
            amenities.append(amenity)
            
        landlords_data = [
    {
        "email": "demo.landlord1@example.com",
        "username": "demo_landlord1",
        "first_name": "Anna",
        "last_name": "Schmidt",
    },
    {
        "email": "demo.landlord2@example.com",
        "username": "demo_landlord2",
        "first_name": "Max",
        "last_name": "Weber",
    },
]

        tenants_data = [
    {
        "email": "demo.tenant1@example.com",
        "username": "demo_tenant1",
        "first_name": "Mia",
        "last_name": "Fischer",
    },
    {
        "email": "demo.tenant2@example.com",
        "username": "demo_tenant2",
        "first_name": "Leon",
        "last_name": "Wagner",
    },
]
        
        landlords = []
        for data in landlords_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
            )
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.role = User.Roles.LANDLORD
            user.set_password("password123")
            user.save()
            landlords.append(user)
            
        tenants = []
        for data in tenants_data:
            user, created = User.objects.get_or_create(
             username=data["username"],
            )
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.role = User.Roles.TENANT
            user.set_password("password123")
            user.save()
            tenants.append(user)
            
        properties_data = [
    {
        "owner": landlords[0],
        "title": "Bright Studio in Berlin Mitte",
        "description": "Compact furnished studio close to public transport and cafes.",
        "property_type": Property.PropertyType.STUDIO,
        "deal_type": Property.DealType.RENT,
        "guests": 2,
        "rooms": 1,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqm": 34,
        "price_per_night": Decimal("89.00"),
        "address": "Invalidenstrasse 12",
        "country": "Germany",
        "city": "Berlin",
        "district": "Mitte",
        "zip_code": "10115",
        "status": Property.Status.PUBLISHED,
        "amenities": ["WiFi", "Kitchen", "Workspace", "Heating"],
    },
    {
        "owner": landlords[0],
        "title": "Family Apartment in Hamburg",
        "description": "Spacious apartment with balcony near parks and shops.",
        "property_type": Property.PropertyType.APARTMENT,
        "deal_type": Property.DealType.RENT,
        "guests": 4,
        "rooms": 3,
        "bedrooms": 2,
        "bathrooms": 1,
        "area_sqm": 76,
        "price_per_night": Decimal("145.00"),
        "address": "Eppendorfer Weg 45",
        "country": "Germany",
        "city": "Hamburg",
        "district": "Eimsbuettel",
        "zip_code": "20259",
        "status": Property.Status.PUBLISHED,
        "amenities": ["WiFi", "Kitchen", "Washer", "Balcony"],
    },
    {
        "owner": landlords[1],
        "title": "Quiet Room in Munich",
        "description": "Private room in a quiet shared apartment.",
        "property_type": Property.PropertyType.ROOM,
        "deal_type": Property.DealType.RENT,
        "guests": 1,
        "rooms": 1,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqm": 18,
        "price_per_night": Decimal("59.00"),
        "address": "Lindwurmstrasse 88",
        "country": "Germany",
        "city": "Munich",
        "district": "Sendling",
        "zip_code": "80337",
        "status": Property.Status.PUBLISHED,
        "amenities": ["WiFi", "Heating", "Washer"],
    },
]
 
        properties = []
        amenities_by_slug = {amenity.slug: amenity for amenity in amenities}

        for data in properties_data:
            amenity_names_for_property = data['amenities']
            property_defaults={
                key: value for key, value in data.items() if key != 'amenities'
            }
            
            rental_property, _ = Property.objects.update_or_create(
                title=data["title"],
                defaults=property_defaults,
            )
            rental_property.amenities.set(
                amenities_by_slug[slugify(name)] for name in amenity_names_for_property
            )
            properties.append(rental_property)
            
        today = timezone.localdate()
        bookings_data = [
    {
        "user": tenants[0],
        "rental_property": properties[0],
        "check_in": today + timedelta(days=10),
        "check_out": today + timedelta(days=13),
        "guests": 2,
        "status": Booking.Status.CONFIRMED,
    },
    {
        "user": tenants[1],
        "rental_property": properties[1],
        "check_in": today + timedelta(days=20),
        "check_out": today + timedelta(days=25),
        "guests": 3,
        "status": Booking.Status.PENDING,
    },
    {
        "user": tenants[0],
        "rental_property": properties[2],
        "check_in": today + timedelta(days=35),
        "check_out": today + timedelta(days=37),
        "guests": 1,
        "status": Booking.Status.COMPLETED,
    },
]
        
        bookings = []
        for data in bookings_data:
            nights = (data['check_out'] - data['check_in']).days
            price = data['rental_property'].price_per_night
            
            booking, _ = Booking.objects.update_or_create(
                user=data['user'],
                rental_property=data['rental_property'],
                check_in=data['check_in'],
                check_out=data['check_out'],
                defaults={
                    'guests': data['guests'],
                    'status': data['status'],
                    'price_per_night_snapshot': price,
                    'total_price': price * nights,
                }
            )
            bookings.append(booking)
            
        reviews_data = [
    {
        "booking": bookings[0],
        "rating": 5,
        "comment": "Great location and very clean apartment.",
    },
    {
        "booking": bookings[2],
        "rating": 4,
        "comment": "Quiet room, good value for a short stay.",
    },
]
        
        reviews = []
        for data in reviews_data:
            booking=data['booking']
            review, _ = Review.objects.update_or_create(
                booking=booking,
                defaults={
                    'author': booking.user,
                    'rental_property': booking.rental_property,
                    'rating': data['rating'],
                    'comment': data['comment'],
                }
            )
            reviews.append(review)
            
            
        
        favorites_data = [
            {
                "user": tenants[0],
                "rental_property": properties[1],
            },
            {
                "user": tenants[1],
                "rental_property": properties[0],
            },
            {
                "user": tenants[1],
                "rental_property": properties[2],
            }
        ]
        
        favorites = []
        for data in favorites_data:
            favorite, _ = Favorite.objects.update_or_create(
                user=data['user'],
                rental_property=data['rental_property'],
            )
            favorites.append(favorite)
            
            
        
        searches_data = [
            {
                "user": tenants[0],
                "query": "berlin studio",
                "normalized_query": "berlin studio",
                "city": "Berlin",
                "property_type": Property.PropertyType.STUDIO,
                "results_count": 1,
            },
            {
                "user": tenants[1],
                "query": "hamburg apartment",
                "normalized_query": "hamburg apartment",
                "city": "Hamburg",
                "property_type": Property.PropertyType.APARTMENT,
                "results_count": 1,
            },
            {
                "user": None,
                "query": "munich room",
                "normalized_query": "munich room",
                "city": "Munich",
                "property_type": Property.PropertyType.ROOM,
                "results_count": 1,
            },
            {
                "user": tenants[0],
                "query": "berlin studio",
                "normalized_query": "berlin studio",
                "city": "Berlin",
                "property_type": Property.PropertyType.STUDIO,
                "results_count": 1,
            },
        ]
        
        search_history = []
        for data in searches_data:
            search_history.append(SearchHistory.objects.create(**data))
            
            
        PropertyView.objects.filter(rental_property__in=properties).delete()
        
        view_plan = [
            (properties[0], tenants[0], "127.0.0.10", 4),
            (properties[1], tenants[1], "127.0.0.11", 2),
            (properties[2], None, "127.0.0.12", 1),
        ]
        
        for rental_property in properties:
            rental_property.views_count = 0
            rental_property.save(update_fields=["views_count"])

        property_views = []
        for rental_property, user, ip_address, count in view_plan:
            for _ in range(count):
                property_views.append(PropertyView.objects.create(rental_property=rental_property, user=user, ip_address=ip_address, user_agent="Rentify seed demo"))
        
        rental_property.views_count = count
        rental_property.save(update_fields=["views_count"])
        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))