import PropertyFilters from "@/components/PropertyFilters";
import { getProperties, PropertyListParams } from "@/lib/properties";
import PropertyCard from "@/components/PropertyCard";
import AppHeader from "../components/AppHeader";
import Pagination from "@/components/Pagination";
import PropertySort from "@/components/PropertySort";

type HomeProps = {
  searchParams: Promise<PropertyListParams>;
}

export default async function Home({ searchParams }: HomeProps) {

  const params = await searchParams;
  const properties = await getProperties(params);
  const currentPage = Number(params.page ?? 1);

  return (
    <>
      <AppHeader />
      <main className="bg-zinc-50">
        <section className="border-b border-zinc-200 bg-white">
          <div className="mx-auto max-w-7xl px-5 py-12">
            <div className="max-w-3xl">
              <p className="text-sm font-medium uppercase tracking-wide text-zinc-500">
                Rental platform
              </p>
              <h1 className="mt-3 text-4xl font-semibold tracking-normal text-zinc-950">
                Find a place that fits your stay.
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-zinc-600">
                Browse apartments, houses, studios and rooms with booking,
                reviews and landlord workflows powered by Rentify API.
              </p>
            </div>

            <div className="mt-8">
              <PropertyFilters defaultValues={params} />
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-8">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-zinc-950">
                Available Properties
              </h2>
              <p className="mt-1 text-sm text-zinc-500">
                {properties.count} published listing found
              </p>
            </div>
            <div>
              <PropertySort currentValue={params.ordering} />
            </div>
          </div>

          {properties.results.length > 0 ? (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {properties.results.map((property) => (
                <PropertyCard key={property.id} property={property} />
              ))}
            </div>
          ) : (
            <div className="rounded-lg border border-dashed border-zinc-300 bg-white p-10 text-center">
              <h3 className="text-base font-semibold text-zinc-950">
                No properties found
              </h3>
              <p className="mt-2 text-sm text-zinc-500">
                Try changing city, price or property type.
              </p>
            </div>
          )}

          {(properties.previous || properties.next) && (
            <Pagination
              currentPage={currentPage}
              hasPrevious={Boolean(properties.previous)}
              hasNext={Boolean(properties.next)}
              searchParams={params}
            />
          )}
        </section>
      </main>
    </>
  );
}
