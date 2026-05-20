"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { createProperty, updateProperty } from "@/lib/properties";
import { getAccessToken } from "@/lib/token";
import type { Property, PropertyType } from "@/types/api";

type PropertyFormProps = {
    initialData?: Property;
};

export default function NewPropertyForm({ initialData }: PropertyFormProps) {
    const router = useRouter();
    const [title, setTitle] = useState(initialData?.title ?? "");
    const [description, setDescription] = useState(initialData?.description ?? "");
    const [propertyType, setPropertyType] = useState<PropertyType>(initialData?.property_type ?? "apartment");
    const [city, setCity] = useState(initialData?.city ?? "Berlin");
    const [district, setDistrict] = useState(initialData?.district ?? "");
    const [address, setAddress] = useState(initialData?.address ?? "");
    const [zipCode, setZipCode] = useState(initialData?.zip_code ?? "");
    const [price, setPrice] = useState(initialData?.price_per_night ? String(Number(initialData.price_per_night).toFixed(0)) : "120");
    const [guests, setGuests] = useState(initialData?.guests ?? 2);
    const [rooms, setRooms] = useState(initialData?.rooms ?? 2);
    const [bedrooms, setBedrooms] = useState(initialData?.bedrooms ?? 1);
    const [bathrooms, setBathrooms] = useState(initialData?.bathrooms ?? 1);
    const [areaSqm, setAreaSqm] = useState(initialData?.area_sqm ?? 55);
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    async function handleSubmit() {
        const accessToken = getAccessToken();

        if (!accessToken) {
            setError("Sign in as a landlord to manage properties.");
            return;
        }

        setError(null);
        setIsSubmitting(true);

        try {
            const payload = {
                title,
                description,
                property_type: propertyType,
                deal_type: "rent" as const,
                guests,
                rooms,
                bedrooms,
                bathrooms,
                area_sqm: areaSqm,
                price_per_night: price,
                address,
                country: "Germany",
                city,
                district,
                zip_code: zipCode,
                status: initialData?.status ?? ("published" as const),
            };

            let property;
            if (initialData) {
                property = await updateProperty(accessToken, initialData.id, payload);
            } else {
                property = await createProperty(accessToken, payload);
            }

            router.push(`/properties/${property.id}`);
            router.refresh();
        } catch (error) {
            setError(error instanceof Error ? error.message : "Failed to save property");
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <form
            onSubmit={(event) => {
                event.preventDefault();
                void handleSubmit();
            }}
            className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm"
        >
            <div className="grid gap-4">
                <div>
                    <label className="text-sm font-medium text-zinc-700">Title</label>
                    <input
                        value={title}
                        onChange={(event) => setTitle(event.target.value)}
                        required
                        className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                    />
                </div>

                <div>
                    <label className="text-sm font-medium text-zinc-700">Description</label>
                    <textarea
                        value={description}
                        onChange={(event) => setDescription(event.target.value)}
                        required
                        rows={4}
                        className="mt-2 w-full rounded-md border border-zinc-200 px-3 py-2 text-sm outline-none focus:border-zinc-400"
                    />
                </div>

                <div className="grid gap-4 sm:grid-cols-3">
                    <div>
                        <label className="text-sm font-medium text-zinc-700">Type</label>
                        <select
                            value={propertyType}
                            onChange={(event) => setPropertyType(event.target.value as PropertyType)}
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 bg-white px-3 text-sm outline-none focus:border-zinc-400"
                        >
                            <option value="apartment">Apartment</option>
                            <option value="house">House</option>
                            <option value="studio">Studio</option>
                            <option value="room">Room</option>
                        </select>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-zinc-700">Price</label>
                        <input
                            type="number"
                            min={1}
                            value={price}
                            onChange={(event) => setPrice(event.target.value)}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-zinc-700">Area sqm</label>
                        <input
                            type="number"
                            min={1}
                            value={areaSqm}
                            onChange={(event) => setAreaSqm(Number(event.target.value))}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-4">
                    <NumberField label="Guests" value={guests} onChange={setGuests} />
                    <NumberField label="Rooms" value={rooms} onChange={setRooms} />
                    <NumberField label="Bedrooms" value={bedrooms} onChange={setBedrooms} />
                    <NumberField label="Bathrooms" value={bathrooms} onChange={setBathrooms} />
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                    <div>
                        <label className="text-sm font-medium text-zinc-700">City</label>
                        <input
                            value={city}
                            onChange={(event) => setCity(event.target.value)}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium text-zinc-700">District</label>
                        <input
                            value={district}
                            onChange={(event) => setDistrict(event.target.value)}
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>
                </div>

                <div>
                    <label className="text-sm font-medium text-zinc-700">Address</label>
                    <input
                        value={address}
                        onChange={(event) => setAddress(event.target.value)}
                        required
                        className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                    />
                </div>

                <div>
                    <label className="text-sm font-medium text-zinc-700">Zip code</label>
                    <input
                        value={zipCode}
                        onChange={(event) => setZipCode(event.target.value)}
                        required
                        className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                    />
                </div>
            </div>

            {error && (
                <div className="mt-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                    {error}
                </div>
            )}

            <button
                type="submit"
                disabled={isSubmitting}
                className="mt-5 h-11 w-full rounded-md bg-zinc-950 text-sm font-medium text-white hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Saving..." : initialData ? "Save changes" : "Create property"}
            </button>
        </form>
    );
}

function NumberField({
    label,
    value,
    onChange,
}: {
    label: string;
    value: number;
    onChange: (value: number) => void;
}) {
    return (
        <div>
            <label className="text-sm font-medium text-zinc-700">{label}</label>
            <input
                type="number"
                min={1}
                value={value}
                onChange={(event) => onChange(Number(event.target.value))}
                required
                className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
            />
        </div>
    );
}
