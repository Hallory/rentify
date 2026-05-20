import { API_URL, buildQueryString } from './api';
import type { CreatePropertyPayload, PaginatedResponse, Property, PropertyType } from '@/types/api';

export type PropertyListParams = {
  search?: string;
  city?: string;
  property_type?: PropertyType;
  price_min?: number;
  price_max?: number;
  guests?: number;
  rooms_min?: number;
  rooms_max?: number;
  ordering?: string;
  page?: number;
};

export async function getProperties(params: PropertyListParams = {}) {
  const query = buildQueryString(params);

  const response = await fetch(`${API_URL}/properties/${query}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response.json() as Promise<PaginatedResponse<Property>>;
}

export async function getPopularProperties() {
  const response = await fetch(`${API_URL}/properties/popular/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response.json() as Promise<PaginatedResponse<Property>>;
}

export async function getProperty(id: string){
  const response = await fetch(`${API_URL}/properties/${id}/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response.json() as Promise<Property>;
}

export async function createProperty(
  accessToken: string,
  payload: CreatePropertyPayload
) {
  const response = await fetch(`${API_URL}/properties/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      error?.detail ??
      error?.non_field_errors?.[0] ??
      "Failed to create property"
    );
  }

  return response.json() as Promise<Property>;
}

export async function updateProperty(
  accessToken: string,
  id: string | number,
  payload: Partial<CreatePropertyPayload>
) {
  const response = await fetch(`${API_URL}/properties/${id}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      error?.detail ??
      error?.non_field_errors?.[0] ??
      "Failed to update property"
    );
  }

  return response.json() as Promise<Property>;
}

export async function deleteProperty(accessToken: string, id: string | number) {
  const response = await fetch(`${API_URL}/properties/${id}/`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      error?.detail ?? "Failed to delete property"
    );
  }
}

export async function togglePropertyActive(accessToken: string, id: string | number) {
  const response = await fetch(`${API_URL}/properties/${id}/toggle-active/`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail ?? "Failed to toggle status");
  }

  return response.json() as Promise<Property>;
}
