export type UserRole = "tenant" | "landlord";

export type User = {
    id: number;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    role: UserRole;
    image?: string | null;
};

export type PropertyType = "studio" | "apartment" | "house" | "room";
export type PropertyStatus = "draft" | "published" | "archived";
export type DealType = "rent" | "sale";

export type Property = {
    id: number;
    owner: number;
    title: string;
    description: string;
    property_type: PropertyType;
    deal_type: DealType;
    guests: number;
    rooms: number;
    bedrooms: number;
    bathrooms: number;
    area_sqm: number;
    price_per_night: string;
    address: string;
    country: string;
    city: string;
    district: string;
    zip_code: string;
    amenities: number[];
    status: PropertyStatus;
    views_count: number;
    created_at: string;
    updated_at: string;
}

export type PaginatedResponse<T> = {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export type BookingStatus = 
| "pending"
| "confirmed"
| "cancelled"
| "rejected"
| "completed";

export type Booking = {
  id: number;
  rental_property: number;
  user: number;
  check_in: string;
  check_out: string;
  guests: number;
  price_per_night_snapshot: number;
  total_price: number;
  status: BookingStatus;
  created_at: string;
  updated_at: string;
  cancelled_at: string | null;
  has_review?: boolean;
}

export type CreateBookingPayload = {
  rental_property: number;
  check_in: string;
  check_out: string;
  guests: number;
}

export type CreatePropertyPayload = {
  title: string;
  description: string;
  property_type: PropertyType;
  deal_type: DealType;
  guests: number;
  rooms: number;
  bedrooms: number;
  bathrooms: number;
  area_sqm: number;
  price_per_night: string;
  address: string;
  country: string;
  city: string;
  district: string;
  zip_code: string;
  status: PropertyStatus;
}
