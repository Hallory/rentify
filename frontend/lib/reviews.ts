import { API_URL } from "./api";
import type { PaginatedResponse } from "@/types/api";

export type Review = {
    id: number;
    author: number;
    rental_property: number;
    booking: number;
    rating: number;
    comment: string;
    created_at: string;
    updated_at: string;
    author_username?: string;
};

export type CreateReviewPayload = {
    booking: number;
    rating: number;
    comment: string;
};

export async function getReviews(propertyId: string | number) {
    const response = await fetch(`${API_URL}/reviews/?rental_property=${propertyId}`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error(response.statusText);
    }

    return response.json() as Promise<PaginatedResponse<Review>>;
}

export async function createReview(accessToken: string, payload: CreateReviewPayload) {
    const response = await fetch(`${API_URL}/reviews/`, {
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
            "Failed to submit review"
        );
    }

    return response.json() as Promise<Review>;
}
