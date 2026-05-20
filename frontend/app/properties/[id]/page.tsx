import { getProperty } from '@/lib/properties'
import { getReviews } from '@/lib/reviews'
import { Bath, BedDouble, Eye, MapPin, UserRound } from 'lucide-react'
import AppHeader from '../../../components/AppHeader'
import BookingForm from '@/components/BookingForm'
import PropertyActions from '@/components/PropertyActions'

type PropertyDetailPageProps = {
    params: Promise<{ id: string }>
}

export default async function PropertyDetailPage({ params }: PropertyDetailPageProps) {
    const { id } = await params
    const [property, reviewsData] = await Promise.all([
        getProperty(id),
        getReviews(id).catch(() => ({ results: [] })),
    ]);

    const reviews = reviewsData.results;
    const averageRating = reviews.length > 0
        ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
        : null;

    return (
        <>
            <AppHeader />

            <main className='bg-zinc-50'>
                <section className='border-b border-zinc-200 bg-white'>
                    <div className='mx-auto max-w-7xl px-5 py-10'>
                        <div className='max-w-3xl'>
                            <p className='text-sm font-medium capitalize text-zinc-500 flex items-center gap-3'>
                                <span>{property.property_type} in {property.city}</span>
                                {averageRating && (
                                    <span className="text-amber-500 font-semibold flex items-center gap-1">
                                        ★ {averageRating} ({reviews.length} {reviews.length === 1 ? 'review' : 'reviews'})
                                    </span>
                                )}
                            </p>
                            <h1 className='mt-3 text-4xl font-semibold tracking-normal text-zinc-950'>
                                {property.title}
                            </h1>
                            <div className='mt-3 flex items-center gap-2 text-zinc-600'>
                                <MapPin size={17} />
                                <span>{property.address}, {property.city}</span>
                            </div>
                        </div>
                    </div>
                </section>

                <section className='mx-auto max-w-7xl px-5 py-8 grid lg:grid-cols-[1fr_360px] gap-8'>
                    <div className='rounded-lg border border-zinc-200 bg-white p-6'>
                        <div className='mb-6 flex h-72 items-center justify-center rounded-md bg-zinc-100'>
                            <span className='text-sm font-medium capitalize text-zinc-500'>
                                {property.property_type}
                            </span>
                        </div>
                        <h2 className='text-xl font-semibold text-zinc-950'>Description</h2>
                        <p className='mt-3 leading-7 text-zinc-600'>
                            {property.description}
                        </p>

                        <div className='mt-6 grid gap-3 border-t border-zinc-100 pt-6 sm:grid-cols-4'>
                            <div className='flex items-center gap-2 text-sm text-zinc-600'>
                                <UserRound size={17} />
                                {property.guests} guests
                            </div>
                            <div className='flex items-center gap-2 text-sm text-zinc-600'>
                                <BedDouble size={17} />
                                {property.bedrooms} bedrooms
                            </div>
                            <div className='flex items-center gap-2 text-sm text-zinc-600'>
                                <Bath size={17} />
                                {property.bathrooms} bathrooms
                            </div>
                            <div className='flex items-center gap-2 text-sm text-zinc-600'>
                                <Eye size={17} />
                                {property.views_count} views
                            </div>
                        </div>

                        <PropertyActions property={property} />

                        <div className="mt-8 border-t border-zinc-100 pt-8">
                            <h3 className="text-xl font-semibold text-zinc-950">
                                Reviews ({reviews.length})
                            </h3>
                            {reviews.length > 0 ? (
                                <div className="mt-4 space-y-4">
                                    {reviews.map((review) => (
                                        <div key={review.id} className="rounded-lg border border-zinc-100 bg-zinc-50/50 p-4">
                                            <div className="flex items-center justify-between">
                                                <span className="text-sm font-medium text-zinc-700">
                                                    Guest #{review.author}
                                                </span>
                                                <span className="text-amber-500 font-semibold text-sm">
                                                    {"★".repeat(review.rating)}{"☆".repeat(5 - review.rating)}
                                                </span>
                                            </div>
                                            <p className="mt-2 text-sm leading-6 text-zinc-600">
                                                {review.comment}
                                            </p>
                                            <span className="mt-2 block text-xs text-zinc-400">
                                                {new Date(review.created_at).toLocaleDateString()}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="mt-3 text-sm text-zinc-500">
                                    No reviews for this property yet.
                                </p>
                            )}
                        </div>
                    </div>

                    <aside className='h-fit rounded-lg border border-zinc-200 bg-white p-5 shadow-sm'>
                        <div className='text-2xl font-semibold text-zinc-950'>
                            EUR {Number(property.price_per_night).toFixed(0)}
                        </div>
                        <div className='text-sm text-zinc-500'>per night</div>
                        <BookingForm property={property} />               
                    </aside>
                </section>
            </main>
        </>
    )
}