import { Property } from '@/types/api'
import { Bath, BedDouble, Eye } from 'lucide-react'
import Link from 'next/link'
type PropertyCardProps = {
    property: Property
}
const PropertyCard = ({ property }: PropertyCardProps) => {
    return (
        <Link href={`/properties/${property.id}`} className='block'>

            <article className='rounded-lg border border-zinc-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md'>
                <div className='mb-4 flex h-36 items-center justify-center rounded-md bg-zinc-100'>
                    <span className='text-sm font-medium capitalize text-zinc-500'>{property.property_type}</span>
                </div>
                <div className='flex items-start justify-between gap-3'>
                    <div>
                        <h3 className='mt-1 flex items-center gap-1 text-sm text-zinc-950'>{property.title}</h3>
                    </div>
                </div>

                <div className='text-right'>
                    <div className='text-base font-semibold text-zinc-950'>
                        EUR {Number(property.price_per_night).toFixed(0)}
                    </div>
                    <div className='text-xs text-zinc-500'>
                        per night
                    </div>
                </div>
                <p className='mt-3 line-clamp-2 text-sm leading-6 text-zinc-600'>
                    {property.description}
                </p>
                <div className='mt-5 grid grid-cols-4 gap-2 border-t border-zinc-100 pt-4 text-sm text-zinc-600'>
                    <div className='flex items-center gap-1'>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                        </svg>
                        <span>{property.city}</span>
                    </div>
                    <div className='flex items-center gap-1'>
                        <BedDouble size={16} />
                        {property.bedrooms}
                    </div>
                    <div className='flex items-center gap-1'>
                        <Bath size={15} />
                        {property.bathrooms}
                    </div>
                    <div className='flex items-center gap-1'>
                        <Eye size={15} />
                        {property.views_count}
                    </div>
                </div>
            </article>
        </Link>
    )
}

export default PropertyCard  