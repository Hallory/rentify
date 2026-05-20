import { Search } from "lucide-react";

type PropertyFiltersProps = {
  defaultValues: {
    search?: string;
    city?: string;
    property_type?: string;
    price_min?: number;
    price_max?: number;
    rooms_min?: number;
    rooms_max?: number;
  };
};

export default function PropertyFilters({ defaultValues }: PropertyFiltersProps) {
  return (
    <form className="grid gap-3 rounded-lg border border-zinc-200 bg-white p-4 shadow-sm grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
      {/* Row 1 */}
      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-zinc-500 mb-1">Search Keywords</label>
        <input
          name="search"
          defaultValue={defaultValues.search}
          type="text"
          placeholder="e.g. cozy, quiet, central..."
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">City</label>
        <input
          name="city"
          defaultValue={defaultValues.city}
          type="text"
          placeholder="e.g. Berlin, Munich..."
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">Property Type</label>
        <select
          name="property_type"
          defaultValue={defaultValues.property_type ?? ""}
          className="h-10 w-full rounded-md border border-zinc-200 bg-white px-3 text-sm outline-none focus:border-zinc-400"
        >
          <option value="">All Types</option>
          <option value="apartment">Apartment</option>
          <option value="house">House</option>
          <option value="studio">Studio</option>
          <option value="room">Room</option>
        </select>
      </div>

      {/* Row 2 */}
      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">Min Price (EUR)</label>
        <input
          name="price_min"
          defaultValue={defaultValues.price_min}
          type="number"
          placeholder="No min"
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">Max Price (EUR)</label>
        <input
          name="price_max"
          defaultValue={defaultValues.price_max}
          type="number"
          placeholder="No max"
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">Min Rooms</label>
        <input
          name="rooms_min"
          defaultValue={defaultValues.rooms_min}
          type="number"
          placeholder="No min"
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-zinc-500 mb-1">Max Rooms</label>
        <input
          name="rooms_max"
          defaultValue={defaultValues.rooms_max}
          type="number"
          placeholder="No max"
          className="h-10 w-full rounded-md border border-zinc-200 px-3 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400"
        />
      </div>

      <div className="flex items-end">
        <button
          type="submit"
          className="flex h-10 w-full items-center justify-center gap-2 rounded-md bg-zinc-950 px-4 text-sm font-medium text-white hover:bg-zinc-800 shadow-sm"
        >
          <Search size={16} />
          Search
        </button>
      </div>
    </form>
  );
}