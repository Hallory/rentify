import AppHeader from "@/components/AppHeader";
import BookingsPanel from "@/components/BookingsPanel";
export default function BookingsPage() {
    return (
        <>
            <AppHeader />
            <main className="bg-zinc-50 min-h-screen">
                <section className="border-b border-zinc-200 bg-white">
                    <div className="mx-auto max-w-7xl px-5 py-10">
                        <h1 className="text-3xl font-semibold tracking-normal text-zinc-950">Bookings</h1>
                        <p className="mt-2 text-zinc-600">Manage your booking requests and reservations</p>
                    </div>
                </section>

                <section className="mx-auto max-w-7xl px-5 py-8">
                    <BookingsPanel/>
                </section>
            </main>
        </>
    )
}