import type { Booking, CreateBookingPayload, PaginatedResponse } from "@/types/api";
import { API_URL } from "./api";



function authHeaders(accessToken:string){
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
    }
}

export async function createBooking(
    accessToken: string,
    payload: CreateBookingPayload
){
    const response = await fetch(`${API_URL}/bookings/`, {
        method: "POST",
        headers: authHeaders(accessToken),
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const error = await response.json().catch(() => null);
        throw new Error(
            error?.non_field_errors?.[0] ??
            error.detail ??
            "Failed to create booking"
        );
    }
    return response.json() as Promise<Booking>;
}

export async function getBookings(accessToken: string) {
    const response = await fetch(`${API_URL}/bookings/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
        cache: "no-store",
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return response.json() as Promise<PaginatedResponse<Booking>>;
}


export async function bookingAction(
    accessToken: string,
    bookingId: number,
    action: "cancel" | "confirm" | "reject" | "complete"
){
    const response = await fetch(`${API_URL}/bookings/${bookingId}/${action}/`,{
        method: "PATCH",
        headers:{
            Authorization: `Bearer ${accessToken}`
        },
    });

    if(!response.ok){
        const error = await response.json().catch(() => null);
        throw new Error(error?.detail ?? "Failed to update booking");
    }
    return response.json() as Promise<Booking>;
}
