"use client";
import { Booking } from '@/types/api';
import { bookingAction, getBookings } from '@/lib/bookings';
import { createReview } from '@/lib/reviews';
import { getAccessToken } from '@/lib/token';
import { CalendarDays, Check, Loader2, X } from 'lucide-react';
import React, { useEffect } from 'react';
import { getMe } from '@/lib/auth';
import type { User } from '@/types/api';

const statusClass: Record<Booking['status'], string> = {
    pending: 'bg-amber-50 text-amber-700 border-amber-200',
    confirmed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    cancelled: 'bg-zinc-50 text-zinc-700 border-zinc-200',
    rejected: 'bg-red-50 text-red-700 border-red-200',
    completed: 'bg-blue-50 text-blue-700 border-blue-200',
};

const BookingsPanel = () => {
    const [bookings, setBookings] = React.useState<Booking[]>([]);
    const [user, setUser] = React.useState<User | null>(null);
    const [isLoading, setIsLoading] = React.useState(true);
    const [message, setMessage] = React.useState<string | null>(null);
    const [error, setError] = React.useState<string | null>(null);

    const [activeReviewBookingId, setActiveReviewBookingId] = React.useState<number | null>(null);
    const [reviewRating, setReviewRating] = React.useState(5);
    const [reviewComment, setReviewComment] = React.useState("");
    const [isSubmittingReview, setIsSubmittingReview] = React.useState(false);

    async function loadBookings() {
        const accessToken = getAccessToken();

        if(!accessToken){
            setIsLoading(false);
            setError("Sign in to view bookings");
            return;
        }

        try{
            setError(null);
            const [currentUser, data] = await Promise.all([
                getMe(accessToken),
                getBookings(accessToken),
            ]);
            setUser(currentUser);
            setBookings(data.results);
        }catch{
            setError("Failed to load bookings");
        }finally{
            setIsLoading(false);
        };
    }

    useEffect(() => {
        void loadBookings();
    },[]);

    async function handleAction(
        bookingId:number, 
        action: "cancel" | "confirm" | "reject" | "complete"
    ) {
        const accessToken = getAccessToken();

        if(!accessToken){
            setError("Sign in to manage bookings");
            return;
        }

        try{
            setMessage(null);
            setError(null);
            await bookingAction(accessToken, bookingId, action);
            setMessage(`Booking ${action} action completed`);
            await loadBookings();
        }catch(error){
            setError(error instanceof Error ? error.message : "Failed to update booking");
        }
    }

    async function handleReviewSubmit(bookingId: number) {
        const accessToken = getAccessToken();
        if (!accessToken) return;

        setIsSubmittingReview(true);
        setError(null);
        setMessage(null);

        try {
            await createReview(accessToken, {
                booking: bookingId,
                rating: reviewRating,
                comment: reviewComment,
            });
            setMessage("Review submitted successfully!");
            setActiveReviewBookingId(null);
            setReviewComment("");
            await loadBookings();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to submit review");
        } finally {
            setIsSubmittingReview(false);
        }
    }

    if(isLoading){
        return (
            <div className='flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 p-6'>
                <Loader2 className='animate-spin' size={18}/>
                Loading Bookings...
            </div>
        )
    }

    return (
        <div className='space-y-4'>
            {message && (
                <div className='rounded-md border border-emerald-200 bg-emerald-50 px-4 py-3 text-emerald-700'>{message}</div>
            )}
            {error && (
                <div className='rounded-md border border-red-200 bg-red-50 px-4 py-3 text-red-700'>{error}</div>
            )}
            {bookings.length === 0 ? (
                <div className='rounded-lg border border-dashed border-zinc-300 bg-white p-10 text-center'>
                    <h2 className='text-base font-semibold text-zinc-950'>No bookings yet</h2>
                    <p className='mt-2 text-sm text-zinc-500'>Reservation will appear here after they are created</p>
                </div>
            ):(
                <div className='grid gap-4'>
                    {bookings.map((booking) => (
                        <article key={booking.id} className='rounded-lg border border-zinc-200 bg-white p-5 shadow-sm'>
                            <div className='flex flex-col justify-between gap-4 md:flex-row md:items-center'>
                                <div>
                                    <div className='flex items-center gap-2'>
                                        <CalendarDays size={18} className='text-zinc-500' />
                                        <h2 className='text-base font-semibold text-zinc-950'>
                                            Booking #{booking.id}
                                        </h2>
                                        <span className={`rounded-md border px-2 py-1 text-xs font-medium capitalize ${statusClass[booking.status]}`}>
                                            {booking.status}
                                        </span>
                                    </div>

                                    <div className='mt-3 grid gap-2 text-sm text-zinc-600 sm:grid-cols-2 lg:grid-cols-4'>
                                        <p>Property ID: {booking.rental_property}</p>
                                        <p>Check-in: {booking.check_in}</p>
                                        <p>Check-out: {booking.check_out}</p>
                                        <p>Guests: {booking.guests}</p>
                                    </div>
                                    <div className='mt-3 text-sm text-zinc-600'>
                                        Total:{' '}
                                        <span className='font-semibold text-zinc-950'>EUR {Number(booking.total_price).toFixed(0)}</span>
                                    </div>
                                </div>
                                <div className='flex flex-wrap gap-2'>
                                    {user?.id === booking.user && ["pending", "confirmed"].includes(booking.status) && (
                                        <button 
                                            type='button'
                                            onClick={() => void handleAction(booking.id, "cancel")}
                                            className='flex h-9 items-center gap-2 rounded-md border border-zinc-200 px-3 text-sm font-medium text-zinc-700 hover:bg-zinc-100'
                                        >
                                            <X size={15} />
                                            Cancel
                                        </button>
                                    )}
                                    {user?.role === "landlord" && user.id !== booking.user && booking.status === "pending" && (
                                        <>
                                            <button 
                                            type='button'
                                            onClick={() => void handleAction(booking.id, "confirm")}
                                            className='flex h-9 items-center gap-2 rounded-md bg-zinc-950 px-3 text-sm font-medium text-white hover:bg-zinc-800'>
                                                <Check size={15} />
                                                Confirm
                                            </button>
                                            <button 
                                            type='button'
                                            onClick={() => void handleAction(booking.id, "reject")}
                                            className='flex h-9 items-center gap-2 rounded-md border border-red-200 px-3 text-sm font-medium text-red-700 hover:bg-red-50'>
                                                Reject
                                            </button>
                                        </>
                                    )}
                                    {user?.role === "landlord" && user.id !== booking.user && booking.status === "confirmed" && (
                                        <button type='button' onClick={() => void handleAction(booking.id, "complete")} className='flex h-9 items-center gap-2 rounded-md border border-blue-200 px-3 text-sm font-medium text-blue-700 hover:bg-blue-50'>
                                            Complete
                                        </button>
                                    )}
                                    {user?.id === booking.user && booking.status === "completed" && !booking.has_review && activeReviewBookingId !== booking.id && (
                                        <button 
                                            type='button'
                                            onClick={() => {
                                                setActiveReviewBookingId(booking.id);
                                                setReviewRating(5);
                                                setReviewComment("");
                                            }}
                                            className='flex h-9 items-center gap-2 rounded-md bg-zinc-950 px-3 text-sm font-medium text-white hover:bg-zinc-800'
                                        >
                                            Leave Review
                                        </button>
                                    )}
                                    {user?.id === booking.user && booking.status === "completed" && booking.has_review && (
                                        <span className="flex h-9 items-center px-3 text-xs font-medium text-zinc-500 bg-zinc-100 rounded-md">
                                            Reviewed
                                        </span>
                                    )}
                                </div>
                            </div>
                            {activeReviewBookingId === booking.id && (
                                <form onSubmit={(e) => { e.preventDefault(); void handleReviewSubmit(booking.id); }} className="mt-4 border-t border-zinc-100 pt-4 space-y-3">
                                    <h4 className="text-sm font-semibold text-zinc-950">Leave a Review</h4>
                                    <div className="flex gap-4 items-center">
                                        <div>
                                            <label className="block text-xs font-medium text-zinc-500 mb-1">Rating</label>
                                            <select 
                                                value={reviewRating} 
                                                onChange={(e) => setReviewRating(Number(e.target.value))}
                                                className="h-9 rounded-md border border-zinc-200 bg-white px-2 text-sm outline-none"
                                            >
                                                <option value={5}>5 - Excellent</option>
                                                <option value={4}>4 - Very Good</option>
                                                <option value={3}>3 - Good</option>
                                                <option value={2}>2 - Fair</option>
                                                <option value={1}>1 - Poor</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-xs font-medium text-zinc-500 mb-1">Comment</label>
                                        <textarea 
                                            value={reviewComment}
                                            onChange={(e) => setReviewComment(e.target.value)}
                                            required
                                            rows={2}
                                            placeholder="Share your experience staying here..."
                                            className="w-full rounded-md border border-zinc-200 px-3 py-1.5 text-sm outline-none focus:border-zinc-400"
                                        />
                                    </div>
                                    <div className="flex gap-2">
                                        <button 
                                            type="submit" 
                                            disabled={isSubmittingReview}
                                            className="h-9 rounded-md bg-zinc-950 px-3 text-xs font-medium text-white hover:bg-zinc-800 disabled:opacity-60"
                                        >
                                            {isSubmittingReview ? "Submitting..." : "Submit Review"}
                                        </button>
                                        <button 
                                            type="button" 
                                            onClick={() => { setActiveReviewBookingId(null); setReviewComment(""); }}
                                            className="h-9 rounded-md border border-zinc-200 px-3 text-xs font-medium text-zinc-700 hover:bg-zinc-100"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </form>
                            )}
                        </article>
                    ))}
                </div>
            )}
        </div>
    );
};

export default BookingsPanel;
