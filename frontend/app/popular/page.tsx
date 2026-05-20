import AppHeader from "@/components/AppHeader";
import PropertyCard from "@/components/PropertyCard";
import { getPopularProperties } from "@/lib/properties";

export default async function PopularPage() {
    const properties = await getPopularProperties();

    return (
        <>
            <AppHeader />
            <main className="min-h-screen bg-zinc-50">
                <section className="border-b border-zinc-200 bg-white">
                    <div className="mx-auto max-w-7xl px-5 py-10">
                        <p className="text-sm font-medium uppercase tracking-wide text-zinc-500">
                            Analytics
                        </p>
                        <h1 className="mt-3 text-3xl font-semibold text-zinc-950">
                            Popular properties
                        </h1>
                        <p className="mt-2 max-w-2xl text-zinc-600">
                            Listings ordered by view count from the Rentify analytics API.
                        </p>
                    </div>
                </section>

                <section className="mx-auto max-w-7xl px-5 py-8">
                    {properties.results.length > 0 ? (
                        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                            {properties.results.map((property) => (
                                <PropertyCard key={property.id} property={property} />
                            ))}
                        </div>
                    ) : (
                        <div className="rounded-lg border border-dashed border-zinc-300 bg-white p-10 text-center">
                            <h2 className="text-base font-semibold text-zinc-950">
                                No popular properties yet
                            </h2>
                            <p className="mt-2 text-sm text-zinc-500">
                                Open a few property pages to generate views.
                            </p>
                        </div>
                    )}
                </section>
            </main>
        </>
    );
}
