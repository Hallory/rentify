"use client";

import { createBooking } from "@/lib/bookings";
import { getAccessToken } from "@/lib/token";
import { Property } from "@/types/api";
import { CalendarDays } from "lucide-react";
import React, { SyntheticEvent } from "react";


type BookingFormProps = {
    property: Property
};
export default function BookingForm({ property }: BookingFormProps) {
    const [checkIn, setCheckIn] = React.useState("");
    const [checkOut, setCheckOut] = React.useState("");
    const [guests, setGuests] = React.useState(1);
    const [message, setMessage] = React.useState<string | null>(null);
    const [error, setError] = React.useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = React.useState(false);

    async function handleSubmit(event: SyntheticEvent<HTMLFormElement>) {
        {
            event.preventDefault();

            const accessToken = getAccessToken();

            if (!accessToken) {
                setError("You must be logged in to book a property");
                return;
            }
            setMessage(null);
            setError(null);
            setIsSubmitting(true);

            try {
                await createBooking(accessToken, {
                    rental_property: property.id,
                    check_in: checkIn,
                    check_out: checkOut,
                    guests,
                });
                setMessage("Booking successful!");
                setCheckIn("");
                setCheckOut("");
                setGuests(1);
            } catch(error){
                setError(error instanceof Error ? error.message : "Failed to create booking");
            } finally {
                setIsSubmitting(false);
            }
        };
    }

    return (
    <form onSubmit={handleSubmit} className="mt-5 space-y-3">
        <div>
            <label className="text-sm font-medium text-zinc-700">Check-in</label>
            <input type="date" value={checkIn} onChange={(e) => setCheckIn(e.target.value)} required className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400" />
        </div>
        <div>
            <label className="text-sm font-medium text-zinc-700">Check-out</label>
            <input type="date" value={checkOut} onChange={(e) => setCheckOut(e.target.value)} required className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400" />
        </div>
        <div>
            <label className="text-sm font-medium text-zinc-700">Guests</label>
            <input type="number" min={1} max={property.guests} value={guests} onChange={(event)=>setGuests(Number(event.target.value))} required className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"/>
        </div>

        {error && (
            <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
            </div>
        )}

        {message && (
            <div className="rounded-md border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                {message}
            </div>
        )}

        <button
            type="submit"
            className="flex h-11 items-center justify-center gap-2 rounded-md bg-zinc-950 px-4 text-sm font-medium text-white hover:bg-zinc-800"
            disabled={isSubmitting}
        >           
            <CalendarDays size={16} />
            <span>{isSubmitting ? "Creating..." : "Reserve"}</span>
        </button>
    </form>
    )
}
