from django.urls import include, path

urlpatterns = [
    path("", include("bookings.urls")),
    path("", include("properties.urls")),
    path("", include("reviews.urls")),
    path("", include("favorites.urls")),
    path("", include("analytics.urls")),
    path("", include("users.urls")),
]
