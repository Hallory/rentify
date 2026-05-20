from django.urls import include, path

urlpatterns = [
    path("bookings/", include("bookings.urls")),
    path("properties/", include("properties.urls")),
    path("reviews/", include("reviews.urls")),
    path("favorites/", include("favorites.urls")),
    path("analytics/", include("analytics.urls")),
    path("users/", include("users.urls")),
]
