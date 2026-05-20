"use client";

import { useRouter, useSearchParams } from "next/navigation";

type PropertySortProps = {
    currentValue?: string;
};

export default function PropertySort({ currentValue }: PropertySortProps) {
    const router = useRouter();
    const searchParams = useSearchParams();

    function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
        const val = e.target.value;
        const params = new URLSearchParams(searchParams.toString());
        if (val) {
            params.set("ordering", val);
        } else {
            params.delete("ordering");
        }
        params.delete("page");

        router.push(`/?${params.toString()}`);
    }

    return (
        <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-zinc-500 whitespace-nowrap">Sort by:</span>
            <select
                value={currentValue ?? ""}
                onChange={handleChange}
                className="h-9 rounded-md border border-zinc-200 bg-white px-3 text-xs font-medium text-zinc-700 outline-none focus:border-zinc-400 cursor-pointer shadow-sm"
            >
                <option value="">Default (Newest)</option>
                <option value="price_per_night">Price: Low to High</option>
                <option value="-price_per_night">Price: High to Low</option>
                <option value="-created_at">Date: Newest first</option>
                <option value="created_at">Date: Oldest first</option>
            </select>
        </div>
    );
}
