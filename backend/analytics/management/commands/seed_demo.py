from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from analytics.models import PropertyView, SearchHistory
from bookings.models import Booking
from favorites.models import Favorite
from properties.models import Amenity, Property
from reviews.models import Review
from users.models import User


class Command(BaseCommand):
    help = "Seed demo data for Rentify"

    def _upsert_user(self, data, role):
        user, _ = User.objects.update_or_create(
            username=data["username"],
            defaults={
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "role": role,
            },
        )
        user.set_password("password123")
        user.save(update_fields=["password"])
        return user

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
            "Elevator",
            "Pet friendly",
            "Near metro",
            "Family friendly",
        ]
        amenities = []
        for name in amenity_names:
            amenity, _ = Amenity.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )
            amenities.append(amenity)
        amenities_by_slug = {amenity.slug: amenity for amenity in amenities}

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
            {
                "email": "demo.landlord3@example.com",
                "username": "demo_landlord3",
                "first_name": "Sofia",
                "last_name": "Keller",
            },
            {
                "email": "demo.landlord4@example.com",
                "username": "demo_landlord4",
                "first_name": "Jonas",
                "last_name": "Becker",
            },
            {
                "email": "demo.landlord5@example.com",
                "username": "demo_landlord5",
                "first_name": "Clara",
                "last_name": "Hoffmann",
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
            {
                "email": "demo.tenant3@example.com",
                "username": "demo_tenant3",
                "first_name": "Emma",
                "last_name": "Bauer",
            },
            {
                "email": "demo.tenant4@example.com",
                "username": "demo_tenant4",
                "first_name": "Noah",
                "last_name": "Richter",
            },
            {
                "email": "demo.tenant5@example.com",
                "username": "demo_tenant5",
                "first_name": "Lina",
                "last_name": "Wolf",
            },
            {
                "email": "demo.tenant6@example.com",
                "username": "demo_tenant6",
                "first_name": "Paul",
                "last_name": "Neumann",
            },
            {
                "email": "demo.tenant7@example.com",
                "username": "demo_tenant7",
                "first_name": "Marie",
                "last_name": "Schulz",
            },
            {
                "email": "demo.tenant8@example.com",
                "username": "demo_tenant8",
                "first_name": "Felix",
                "last_name": "Krause",
            },
        ]

        landlords = [
            self._upsert_user(data, User.Roles.LANDLORD) for data in landlords_data
        ]
        tenants = [self._upsert_user(data, User.Roles.TENANT) for data in tenants_data]

        Review.objects.filter(author__in=tenants).delete()
        Booking.objects.filter(user__in=tenants).delete()
        Favorite.objects.filter(user__in=tenants).delete()
        SearchHistory.objects.filter(user__in=tenants).delete()
        PropertyView.objects.filter(user__in=tenants).delete()
        Property.objects.filter(owner__in=landlords).delete()

        property_templates = [
            (
                "Bright Studio in Berlin Mitte",
                "Compact furnished studio near metro, cafes, workspace and museums. Great for business trips and short city stays.",
                Property.PropertyType.STUDIO,
                2,
                1,
                34,
                "89.00",
                "Berlin",
                "Mitte",
                "Invalidenstrasse 12",
                "10115",
                ["WiFi", "Kitchen", "Workspace", "Heating", "Near metro"],
            ),
            (
                "Budget Room near Berlin Kreuzberg",
                "Student friendly private room close to nightlife, coworking spaces and public transport.",
                Property.PropertyType.ROOM,
                1,
                1,
                18,
                "49.00",
                "Berlin",
                "Kreuzberg",
                "Oranienstrasse 50",
                "10999",
                ["WiFi", "Heating", "Washer", "Near metro"],
            ),
            (
                "Pet Friendly Apartment in Prenzlauer Berg",
                "Quiet apartment with balcony, kitchen and parks nearby. Comfortable for couples and remote workers.",
                Property.PropertyType.APARTMENT,
                3,
                2,
                58,
                "128.00",
                "Berlin",
                "Prenzlauer Berg",
                "Kollwitzstrasse 7",
                "10405",
                ["WiFi", "Kitchen", "Balcony", "Pet friendly", "Workspace"],
            ),
            (
                "Luxury Loft in Berlin Charlottenburg",
                "Premium loft with elevator, air conditioning, parking and elegant workspace near Kurfuerstendamm.",
                Property.PropertyType.APARTMENT,
                4,
                3,
                92,
                "260.00",
                "Berlin",
                "Charlottenburg",
                "Kantstrasse 18",
                "10623",
                ["WiFi", "Kitchen", "Parking", "Elevator", "Air conditioning"],
            ),
            (
                "Family Apartment in Hamburg Eimsbuettel",
                "Spacious family friendly apartment with balcony near parks, shops and schools.",
                Property.PropertyType.APARTMENT,
                4,
                3,
                76,
                "145.00",
                "Hamburg",
                "Eimsbuettel",
                "Eppendorfer Weg 45",
                "20259",
                ["WiFi", "Kitchen", "Washer", "Balcony", "Family friendly"],
            ),
            (
                "Modern Flat in Hamburg HafenCity",
                "Central apartment with river views, elevator, workspace and quick access to restaurants.",
                Property.PropertyType.APARTMENT,
                2,
                2,
                54,
                "168.00",
                "Hamburg",
                "HafenCity",
                "Am Sandtorkai 22",
                "20457",
                ["WiFi", "Kitchen", "Workspace", "Elevator", "Heating"],
            ),
            (
                "Quiet Room in Hamburg Altona",
                "Affordable room in a calm shared apartment near S-Bahn and local cafes.",
                Property.PropertyType.ROOM,
                1,
                1,
                20,
                "55.00",
                "Hamburg",
                "Altona",
                "Grosse Bergstrasse 11",
                "22767",
                ["WiFi", "Heating", "Washer", "Near metro"],
            ),
            (
                "Quiet Room in Munich Sendling",
                "Private room in a quiet shared apartment with washer and fast WiFi.",
                Property.PropertyType.ROOM,
                1,
                1,
                18,
                "59.00",
                "Munich",
                "Sendling",
                "Lindwurmstrasse 88",
                "80337",
                ["WiFi", "Heating", "Washer"],
            ),
            (
                "Central Studio in Munich Maxvorstadt",
                "Bright studio close to universities, museums and metro. Good for students and short stays.",
                Property.PropertyType.STUDIO,
                2,
                1,
                31,
                "102.00",
                "Munich",
                "Maxvorstadt",
                "Theresienstrasse 21",
                "80333",
                ["WiFi", "Kitchen", "Workspace", "Near metro"],
            ),
            (
                "Premium Apartment in Munich Schwabing",
                "Stylish apartment with balcony, parking and workspace in a popular residential district.",
                Property.PropertyType.APARTMENT,
                4,
                3,
                82,
                "215.00",
                "Munich",
                "Schwabing",
                "Leopoldstrasse 90",
                "80802",
                ["WiFi", "Kitchen", "Parking", "Balcony", "Workspace"],
            ),
            (
                "Cozy Apartment in Cologne Ehrenfeld",
                "Creative district apartment near tram, restaurants and music venues. Pet friendly and central.",
                Property.PropertyType.APARTMENT,
                3,
                2,
                62,
                "119.00",
                "Cologne",
                "Ehrenfeld",
                "Venloer Strasse 310",
                "50823",
                ["WiFi", "Kitchen", "Pet friendly", "Near metro"],
            ),
            (
                "Budget Studio in Cologne Innenstadt",
                "Simple central studio for short city visits with kitchen and fast WiFi.",
                Property.PropertyType.STUDIO,
                2,
                1,
                29,
                "74.00",
                "Cologne",
                "Innenstadt",
                "Hohe Strasse 14",
                "50667",
                ["WiFi", "Kitchen", "Heating"],
            ),
            (
                "Family House near Cologne",
                "Large family friendly house with parking, kitchen and quiet garden area.",
                Property.PropertyType.HOUSE,
                6,
                5,
                130,
                "240.00",
                "Cologne",
                "Lindenthal",
                "Duerener Strasse 205",
                "50931",
                ["WiFi", "Kitchen", "Parking", "Family friendly", "Washer"],
            ),
            (
                "Business Apartment in Frankfurt Innenstadt",
                "Modern business apartment with workspace, elevator and fast connection to the financial district.",
                Property.PropertyType.APARTMENT,
                2,
                2,
                48,
                "150.00",
                "Frankfurt",
                "Innenstadt",
                "Taunusanlage 6",
                "60329",
                ["WiFi", "Kitchen", "Workspace", "Elevator", "Near metro"],
            ),
            (
                "Luxury Skyline Flat in Frankfurt",
                "Premium high floor apartment with air conditioning, parking and skyline views.",
                Property.PropertyType.APARTMENT,
                3,
                3,
                88,
                "285.00",
                "Frankfurt",
                "Westend",
                "Bockenheimer Landstrasse 25",
                "60325",
                ["WiFi", "Kitchen", "Parking", "Air conditioning", "Elevator"],
            ),
            (
                "Student Room in Frankfurt Bockenheim",
                "Budget room near university campus with washer, heating and public transport nearby.",
                Property.PropertyType.ROOM,
                1,
                1,
                17,
                "52.00",
                "Frankfurt",
                "Bockenheim",
                "Leipziger Strasse 93",
                "60487",
                ["WiFi", "Washer", "Heating", "Near metro"],
            ),
            (
                "Elegant Apartment in Duesseldorf Pempelfort",
                "Quiet apartment with balcony, workspace and easy access to the old town.",
                Property.PropertyType.APARTMENT,
                3,
                2,
                64,
                "132.00",
                "Duesseldorf",
                "Pempelfort",
                "Nordstrasse 42",
                "40477",
                ["WiFi", "Kitchen", "Balcony", "Workspace"],
            ),
            (
                "Central Studio in Duesseldorf",
                "Compact city studio near shopping streets, metro and restaurants.",
                Property.PropertyType.STUDIO,
                2,
                1,
                32,
                "84.00",
                "Duesseldorf",
                "Stadtmitte",
                "Schadowstrasse 35",
                "40212",
                ["WiFi", "Kitchen", "Near metro", "Heating"],
            ),
            (
                "Modern House in Stuttgart",
                "Comfortable house with parking, washer and family friendly layout near green areas.",
                Property.PropertyType.HOUSE,
                5,
                4,
                118,
                "220.00",
                "Stuttgart",
                "Degerloch",
                "Epplestrasse 61",
                "70597",
                ["WiFi", "Kitchen", "Parking", "Washer", "Family friendly"],
            ),
            (
                "Workspace Apartment in Stuttgart Mitte",
                "Central apartment designed for remote work with fast WiFi, desk and quiet bedroom.",
                Property.PropertyType.APARTMENT,
                2,
                2,
                51,
                "118.00",
                "Stuttgart",
                "Mitte",
                "Koenigstrasse 12",
                "70173",
                ["WiFi", "Kitchen", "Workspace", "Near metro"],
            ),
            (
                "Budget Room in Leipzig Suedvorstadt",
                "Affordable room for students and solo travelers near cafes and tram stops.",
                Property.PropertyType.ROOM,
                1,
                1,
                19,
                "45.00",
                "Leipzig",
                "Suedvorstadt",
                "Karl-Liebknecht-Strasse 88",
                "04275",
                ["WiFi", "Heating", "Washer", "Near metro"],
            ),
            (
                "Artist Apartment in Leipzig Plagwitz",
                "Bright pet friendly apartment with balcony, workspace and creative neighborhood atmosphere.",
                Property.PropertyType.APARTMENT,
                3,
                2,
                60,
                "92.00",
                "Leipzig",
                "Plagwitz",
                "Karl-Heine-Strasse 44",
                "04229",
                ["WiFi", "Kitchen", "Balcony", "Workspace", "Pet friendly"],
            ),
            (
                "Quiet House near Leipzig",
                "Family house with garden feeling, parking, kitchen and long stay comfort.",
                Property.PropertyType.HOUSE,
                6,
                5,
                125,
                "175.00",
                "Leipzig",
                "Gohlis",
                "Lindenthaler Strasse 73",
                "04155",
                ["WiFi", "Kitchen", "Parking", "Family friendly", "Washer"],
            ),
            (
                "Long Stay Apartment in Berlin Neukoelln",
                "Affordable long stay apartment with washer, kitchen and workspace near public transport.",
                Property.PropertyType.APARTMENT,
                2,
                2,
                46,
                "96.00",
                "Berlin",
                "Neukoelln",
                "Sonnenallee 120",
                "12045",
                ["WiFi", "Kitchen", "Washer", "Workspace", "Near metro"],
            ),
            (
                "Premium Family Apartment in Hamburg Winterhude",
                "Large family friendly apartment with balcony, elevator and parking near the lake.",
                Property.PropertyType.APARTMENT,
                5,
                4,
                105,
                "235.00",
                "Hamburg",
                "Winterhude",
                "Muehlenkamp 19",
                "22303",
                ["WiFi", "Kitchen", "Parking", "Balcony", "Family friendly"],
            ),
            (
                "Minimal Studio in Munich Altstadt",
                "Central minimal studio for city breaks, close to metro, old town and restaurants.",
                Property.PropertyType.STUDIO,
                2,
                1,
                27,
                "115.00",
                "Munich",
                "Altstadt",
                "Sendlinger Strasse 5",
                "80331",
                ["WiFi", "Kitchen", "Near metro", "Heating"],
            ),
            (
                "Pet Friendly House in Duesseldorf Oberkassel",
                "Quiet house for families with pets, parking, washer and easy river access.",
                Property.PropertyType.HOUSE,
                5,
                4,
                110,
                "205.00",
                "Duesseldorf",
                "Oberkassel",
                "Luegallee 65",
                "40545",
                ["WiFi", "Kitchen", "Parking", "Pet friendly", "Family friendly"],
            ),
            (
                "Compact Studio in Frankfurt Sachsenhausen",
                "Budget studio near river, metro and restaurants. Good for solo travelers and couples.",
                Property.PropertyType.STUDIO,
                2,
                1,
                30,
                "82.00",
                "Frankfurt",
                "Sachsenhausen",
                "Schweizer Strasse 58",
                "60594",
                ["WiFi", "Kitchen", "Near metro", "Heating"],
            ),
            (
                "Quiet Apartment in Stuttgart West",
                "Quiet apartment with balcony and workspace, ideal for business trips and long stays.",
                Property.PropertyType.APARTMENT,
                3,
                2,
                57,
                "126.00",
                "Stuttgart",
                "West",
                "Rotebuehlstrasse 140",
                "70197",
                ["WiFi", "Kitchen", "Balcony", "Workspace"],
            ),
            (
                "Central Apartment in Leipzig Zentrum",
                "Central apartment with elevator, workspace and quick access to restaurants and museums.",
                Property.PropertyType.APARTMENT,
                4,
                3,
                70,
                "108.00",
                "Leipzig",
                "Zentrum",
                "Grimmaische Strasse 10",
                "04109",
                ["WiFi", "Kitchen", "Workspace", "Elevator", "Near metro"],
            ),
        ]

        properties = []
        for index, template in enumerate(property_templates):
            (
                title,
                description,
                property_type,
                guests,
                rooms,
                area_sqm,
                price,
                city,
                district,
                address,
                zip_code,
                property_amenities,
            ) = template
            owner = landlords[index % len(landlords)]
            defaults = {
                "owner": owner,
                "description": description,
                "property_type": property_type,
                "deal_type": Property.DealType.RENT,
                "guests": guests,
                "rooms": rooms,
                "bedrooms": max(1, min(rooms - 1, 4)),
                "bathrooms": 2 if rooms >= 4 else 1,
                "area_sqm": area_sqm,
                "price_per_night": Decimal(price),
                "address": address,
                "country": "Germany",
                "city": city,
                "district": district,
                "zip_code": zip_code,
                "status": Property.Status.PUBLISHED,
            }
            rental_property, _ = Property.objects.update_or_create(
                title=title,
                defaults=defaults,
            )
            rental_property.amenities.set(
                amenities_by_slug[slugify(name)] for name in property_amenities
            )
            properties.append(rental_property)

        today = timezone.localdate()
        booking_specs = [
            (0, 0, -45, -41, 2, Booking.Status.COMPLETED),
            (1, 1, -38, -34, 3, Booking.Status.COMPLETED),
            (2, 2, -32, -30, 1, Booking.Status.COMPLETED),
            (3, 3, -25, -21, 2, Booking.Status.COMPLETED),
            (4, 4, -20, -16, 4, Booking.Status.COMPLETED),
            (5, 5, -14, -10, 2, Booking.Status.COMPLETED),
            (6, 6, -9, -6, 1, Booking.Status.COMPLETED),
            (7, 7, -5, -2, 2, Booking.Status.COMPLETED),
            (8, 0, 7, 10, 2, Booking.Status.CONFIRMED),
            (9, 1, 12, 16, 3, Booking.Status.CONFIRMED),
            (10, 2, 18, 21, 2, Booking.Status.CONFIRMED),
            (11, 3, 24, 29, 4, Booking.Status.CONFIRMED),
            (12, 4, 31, 36, 5, Booking.Status.PENDING),
            (13, 5, 38, 41, 2, Booking.Status.PENDING),
            (14, 6, 44, 48, 1, Booking.Status.PENDING),
            (15, 7, 52, 56, 2, Booking.Status.PENDING),
            (16, 0, 60, 64, 3, Booking.Status.CANCELLED),
            (17, 1, 67, 70, 2, Booking.Status.REJECTED),
        ]

        bookings = []
        for property_index, tenant_index, start_offset, end_offset, guests, status in booking_specs:
            rental_property = properties[property_index]
            check_in = today + timedelta(days=start_offset)
            check_out = today + timedelta(days=end_offset)
            nights = (check_out - check_in).days
            booking, _ = Booking.objects.update_or_create(
                user=tenants[tenant_index],
                rental_property=rental_property,
                check_in=check_in,
                check_out=check_out,
                defaults={
                    "guests": guests,
                    "status": status,
                    "price_per_night_snapshot": rental_property.price_per_night,
                    "total_price": rental_property.price_per_night * nights,
                    "cancelled_at": timezone.now()
                    if status == Booking.Status.CANCELLED
                    else None,
                },
            )
            bookings.append(booking)

        review_comments = [
            "Excellent location, clean apartment and smooth communication.",
            "Very comfortable stay with fast WiFi and a useful workspace.",
            "Quiet room, good value and easy access to public transport.",
            "Premium feeling apartment, perfect for a business trip.",
            "Great for our family, enough space and close to parks.",
            "Nice balcony, practical kitchen and very central location.",
            "Simple, affordable and exactly what I needed for a short stay.",
            "Clean property with friendly host and reliable check-in.",
        ]

        reviews = []
        completed_bookings = [
            booking for booking in bookings if booking.status == Booking.Status.COMPLETED
        ]
        for index, booking in enumerate(completed_bookings):
            review, _ = Review.objects.update_or_create(
                booking=booking,
                defaults={
                    "author": booking.user,
                    "rental_property": booking.rental_property,
                    "rating": 5 if index % 3 != 1 else 4,
                    "comment": review_comments[index % len(review_comments)],
                },
            )
            reviews.append(review)

        favorites = []
        Favorite.objects.filter(user__in=tenants, rental_property__in=properties).delete()
        for tenant_index, tenant in enumerate(tenants):
            for offset in range(3):
                rental_property = properties[(tenant_index * 3 + offset + 1) % len(properties)]
                favorite, _ = Favorite.objects.get_or_create(
                    user=tenant,
                    rental_property=rental_property,
                )
                favorites.append(favorite)

        searches_data = [
            ("berlin studio under 100", "Berlin", Property.PropertyType.STUDIO, 3),
            ("pet friendly apartment berlin balcony", "Berlin", Property.PropertyType.APARTMENT, 2),
            ("family apartment hamburg parking", "Hamburg", Property.PropertyType.APARTMENT, 2),
            ("quiet room munich", "Munich", Property.PropertyType.ROOM, 1),
            ("luxury apartment frankfurt", "Frankfurt", Property.PropertyType.APARTMENT, 2),
            ("budget room leipzig student", "Leipzig", Property.PropertyType.ROOM, 1),
            ("workspace apartment stuttgart", "Stuttgart", Property.PropertyType.APARTMENT, 2),
            ("central studio duesseldorf", "Duesseldorf", Property.PropertyType.STUDIO, 1),
            ("family house cologne", "Cologne", Property.PropertyType.HOUSE, 1),
            ("near metro berlin long stay", "Berlin", "", 4),
            ("balcony workspace apartment", "", Property.PropertyType.APARTMENT, 6),
            ("cheap studio near metro", "", Property.PropertyType.STUDIO, 5),
        ]
        normalized_queries = [query for query, *_ in searches_data]
        SearchHistory.objects.filter(user__in=tenants).delete()
        SearchHistory.objects.filter(
            user__isnull=True,
            normalized_query__in=normalized_queries,
        ).delete()

        search_history = []
        for index, (query, city, property_type, results_count) in enumerate(searches_data):
            repeats = 3 if "berlin" in query else 2 if "studio" in query else 1
            for repeat in range(repeats):
                search_history.append(
                    SearchHistory.objects.create(
                        user=tenants[(index + repeat) % len(tenants)]
                        if repeat % 2 == 0
                        else None,
                        query=query,
                        normalized_query=query,
                        city=city,
                        property_type=property_type,
                        price_min=None,
                        price_max=None,
                        rooms_min=None,
                        rooms_max=None,
                        results_count=results_count,
                    )
                )

        PropertyView.objects.filter(rental_property__in=properties).delete()
        for index, rental_property in enumerate(properties):
            view_count = (index % 7) + 1
            for view_number in range(view_count):
                PropertyView.objects.create(
                    rental_property=rental_property,
                    user=tenants[(index + view_number) % len(tenants)]
                    if view_number % 2 == 0
                    else None,
                    ip_address=f"127.0.{index}.{view_number + 10}",
                    user_agent="Rentify seed demo",
                )
            rental_property.views_count = view_count
            rental_property.save(update_fields=["views_count"])

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data seeded successfully: "
                f"{len(landlords)} landlords, "
                f"{len(tenants)} tenants, "
                f"{len(properties)} properties, "
                f"{len(bookings)} bookings, "
                f"{len(reviews)} reviews, "
                f"{len(favorites)} favorites, "
                f"{len(search_history)} searches."
            )
        )
