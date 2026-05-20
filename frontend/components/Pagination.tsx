import Link from "next/link";

type PaginationProps = {
    currentPage: number;
    hasNext: boolean;
    hasPrevious: boolean;
    searchParams: Record<string, string | number | undefined>;
};

function pageHref(
    searchParams: Record<string, string | number | undefined>,
    page: number
) {
    const params = new URLSearchParams();

    Object.entries(searchParams).forEach(([key, value]) => {
        if (value !== undefined && value !== "") {
            params.set(key, String(value));
        }
    });

    if (page > 1) {
        params.set("page", String(page));
    } else {
        params.delete("page");
    }

    const query = params.toString();
    return query ? `/?${query}` : "/";
}

export default function Pagination({
    currentPage,
    hasNext,
    hasPrevious,
    searchParams,
}: PaginationProps) {
    return (
        <div className="mt-8 flex items-center justify-between border-t border-zinc-200 pt-5">
            <Link
                href={pageHref(searchParams, currentPage - 1)}
                aria-disabled={!hasPrevious}
                className={`rounded-md border px-4 py-2 text-sm font-medium ${
                    hasPrevious
                        ? "border-zinc-200 text-zinc-700 hover:bg-zinc-100"
                        : "pointer-events-none border-zinc-100 text-zinc-300"
                }`}
            >
                Previous
            </Link>

            <span className="text-sm text-zinc-500">Page {currentPage}</span>

            <Link
                href={pageHref(searchParams, currentPage + 1)}
                aria-disabled={!hasNext}
                className={`rounded-md border px-4 py-2 text-sm font-medium ${
                    hasNext
                        ? "border-zinc-200 text-zinc-700 hover:bg-zinc-100"
                        : "pointer-events-none border-zinc-100 text-zinc-300"
                }`}
            >
                Next
            </Link>
        </div>
    );
}
