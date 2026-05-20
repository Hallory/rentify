import re
from decimal import Decimal

from django.db.models import Q

from properties.models import Property

KNOWN_CITIES = {
    "berlin": "Berlin",
    "берлин": "Berlin",
    "munich": "Munich",
    "мюнхен": "Munich",
    "hamburg": "Hamburg",
    "гамбург": "Hamburg",
    "cologne": "Cologne",
    "кельн": "Cologne",
    "frankfurt": "Frankfurt",
    "франкфурт": "Frankfurt",
    "duesseldorf": "Duesseldorf",
    "düsseldorf": "Duesseldorf",
    "дюссельдорф": "Duesseldorf",
    "stuttgart": "Stuttgart",
    "штутгарт": "Stuttgart",
    "leipzig": "Leipzig",
    "лейпциг": "Leipzig",
}

PROPERTY_TYPE_ALIASES = {
    "studio": Property.PropertyType.STUDIO,
    "студия": Property.PropertyType.STUDIO,
    "room": Property.PropertyType.ROOM,
    "комната": Property.PropertyType.ROOM,
    "apartment": Property.PropertyType.APARTMENT,
    "квартира": Property.PropertyType.APARTMENT,
    "house": Property.PropertyType.HOUSE,
    "дом": Property.PropertyType.HOUSE,
}
AMENITY_ALIASES = {
    "балкон": "Balcony",
    "balcony": "Balcony",
    "парковка": "Parking",
    "parking": "Parking",
    "wifi": "WiFi",
    "вайфай": "WiFi",
    "workspace": "Workspace",
    "рабочее место": "Workspace",
    "pet friendly": "Pet friendly",
    "с животными": "Pet friendly",
    "near metro": "Near metro",
    "метро": "Near metro",
}

KEYWORD_ALIASES = {
    "центр": "central",
    "central": "central",
    "тихо": "quiet",
    "quiet": "quiet",
    "недорог": "budget",
    "budget": "budget",
    "luxury": "luxury",
    "люкс": "luxury",
}

ROOM_WORDS = {
    "однокомнат": 1,
    "1 комнат": 1,
    "1-комнат": 1,
    "one room": 1,
    "single room": 1,
    "двухкомнат": 2,
    "2 комнат": 2,
    "2-комнат": 2,
    "two room": 2,
    "трехкомнат": 3,
    "трёхкомнат": 3,
    "3 комнат": 3,
    "3-комнат": 3,
    "three room": 3,
    "четырехкомнат": 4,
    "четырёхкомнат": 4,
    "4 комнат": 4,
    "4-комнат": 4,
    "four room": 4,
}


def normalize_query(query):
    normalized_query = re.sub(r"\s+", " ", query.strip().lower())
    return normalized_query


def parse_local_query(query):
    normalized = normalize_query(query)

    filters = {
        "city": None,
        "district": None,
        "property_type": None,
        "price_min": None,
        "price_max": None,
        "guests": None,
        "rooms_min": None,
        "amenities": [],
        "keywords": [],
    }

    for token, city in KNOWN_CITIES.items():
        if re.search(rf"\b{token}\b", normalized):
            filters["city"] = city
            break

    for token, property_type in PROPERTY_TYPE_ALIASES.items():
        if re.search(rf"\b{token}\b", normalized):
            filters["property_type"] = property_type
            break

    price_match = re.search(r"(?:до|under|below|up to|<)\s*(\d+)", normalized)

    if price_match:
        filters["price_max"] = Decimal(price_match.group(1))

    guest_match = re.search(
        r"(\d+)\s*(?:guest|guests|people|person|человек|чел|гост)", normalized
    )
    if guest_match:
        filters["guests"] = int(guest_match.group(1))

    for token, amenity in AMENITY_ALIASES.items():
        if re.search(rf"\b{token}\b", normalized) and amenity not in filters["amenities"]:
            filters["amenities"].append(amenity)

    for token, keyword in KEYWORD_ALIASES.items():
        if re.search(rf"\b{token}\b", normalized) and keyword not in filters["keywords"]:
            filters["keywords"].append(keyword)

    for token, rooms in ROOM_WORDS.items():
        if re.search(rf"\b{token}\b", normalized):
            filters["rooms_min"] = rooms
            break

    rooms_match = re.search(r"(\d+)\s*(?:room|rooms|комнат|комнаты|комн)", normalized)

    if rooms_match:
        filters["rooms_min"] = int(rooms_match.group(1))

    confidence = calculate_confidence(filters=filters)

    return filters, confidence


def calculate_confidence(filters):
    score = 0

    for key in ["city", "property_type", "price_max", "rooms_min", "guests"]:
        if filters[key]:
            score += 1

    score += len(filters.get("amenities", []))
    score += len(filters.get("keywords", []))

    return score


def build_property_queryset(filters):
    queryset = Property.objects.filter(
        status=Property.Status.PUBLISHED
    ).prefetch_related("amenities")

    if filters.get("city"):
        queryset = queryset.filter(city__iexact=filters["city"])

    if filters.get("district"):
        queryset = queryset.filter(district__icontains=filters["district"])

    if filters.get("property_type"):
        queryset = queryset.filter(property_type=filters["property_type"])

    if filters.get("price_min"):
        queryset = queryset.filter(price_per_night__gte=filters["price_min"])

    if filters.get("price_max"):
        queryset = queryset.filter(price_per_night__lte=filters["price_max"])

    if filters.get("guests"):
        queryset = queryset.filter(guests__gte=filters["guests"])

    if filters.get("rooms_min"):
        queryset = queryset.filter(rooms__gte=filters["rooms_min"])

    if filters.get("amenities", []):
        for amenity in filters.get("amenities", []):
            queryset = queryset.filter(amenities__name__iexact=amenity)

    hard_filter_keys = [
        "city",
        "district",
        "property_type",
        "price_min",
        "price_max",
        "guests",
        "rooms_min",
    ]
    has_hard_filters = any(filters.get(key) for key in hard_filter_keys) or bool(
        filters.get("amenities", [])
    )

    keywords = filters.get("keywords", [])
    if keywords and not has_hard_filters:
        keyword_query = Q()
        for keyword in keywords:
            keyword_query |= Q(title__icontains=keyword)
            keyword_query |= Q(description__icontains=keyword)
            keyword_query |= Q(district__icontains=keyword)
            keyword_query |= Q(city__icontains=keyword)
            keyword_query |= Q(amenities__name__icontains=keyword)

        queryset = queryset.filter(keyword_query)

    return queryset.distinct().order_by("price_per_night", "-views_count")
