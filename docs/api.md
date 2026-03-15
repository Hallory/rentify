Auth
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
GET    /api/users/me
PATCH  /api/users/me
POST   /api/users/change-password


Properties
GET    /api/properties
GET    /api/properties/:id
POST   /api/properties
PATCH  /api/properties/:id
DELETE /api/properties/:id
PATCH  /api/properties/:id/status
GET    /api/properties/my
POST   /api/properties/:id/images
DELETE /api/properties/:id/images/:image_id


Bookings
POST   /api/bookings
GET    /api/bookings
GET    /api/bookings/:id
PATCH  /api/bookings/:id
PATCH  /api/bookings/:id/confirm
PATCH  /api/bookings/:id/reject
PATCH  /api/bookings/:id/cancel


Reviews
POST   /api/properties/:id/reviews
GET    /api/properties/:id/reviews
PATCH  /api/reviews/:id
DELETE /api/reviews/:id


# Not required for now
Favorites
POST   /api/properties/:id/favorite
DELETE /api/properties/:id/favorite
GET    /api/favorites


Reference / Filters data
GET    /api/reference/property-types
GET    /api/reference/listing-types
GET    /api/reference/cities
GET    /api/reference/amenities