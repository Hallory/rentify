"use client";

import { useEffect, useState } from "react";
import AppHeader from "@/components/AppHeader";
import PropertyCard from "@/components/PropertyCard";
import { getAccessToken } from "@/lib/token";
import { API_URL } from "@/lib/api";
import type { Property } from "@/types/api";
import { Search, History, Sparkles, TrendingUp, AlertCircle } from "lucide-react";

type SearchHistoryItem = {
    id: number;
    query: string;
    created_at: string;
};

type PopularQueryItem = {
    query: string;
    count: number;
};

type SmartSearchResponse = {
    query: string;
    interpreted_filters: Record<string, any>;
    results: Property[];
    warnings?: string[];
};

export default function SearchPage() {
    const [query, setQuery] = useState("");
    const [isSearching, setIsSearching] = useState(false);
    const [results, setResults] = useState<Property[]>([]);
    const [interpretedFilters, setInterpretedFilters] = useState<Record<string, any> | null>(null);
    const [warnings, setWarnings] = useState<string[]>([]);
    const [history, setHistory] = useState<SearchHistoryItem[]>([]);
    const [popular, setPopular] = useState<PopularQueryItem[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const token = getAccessToken();

        fetch(`${API_URL}/search-history/popular/`)
            .then((res) => (res.ok ? res.json() : []))
            .then((data) => setPopular(data))
            .catch(() => { });

        if (token) {
            fetch(`${API_URL}/search-history/`, {
                headers: { Authorization: `Bearer ${token}` },
            })
                .then((res) => (res.ok ? res.json() : { results: [] }))
                .then((data) => setHistory(data.results || []))
                .catch(() => { });
        }
    }, [isSearching]);

    async function handleSearch(searchQuery: string) {
        if (!searchQuery.trim()) return;

        setIsSearching(true);
        setError(null);
        setWarnings([]);
        setInterpretedFilters(null);

        const token = getAccessToken();
        const headers: Record<string, string> = {
            "Content-Type": "application/json",
        };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        try {
            const res = await fetch(`${API_URL}/properties/search/`, {
                method: "POST",
                headers,
                body: JSON.stringify({ query: searchQuery }),
            });

            if (!res.ok) {
                throw new Error("Search failed. Please try again.");
            }

            const data = (await res.json()) as SmartSearchResponse;
            setResults(data.results);
            setInterpretedFilters(data.interpreted_filters);
            if (data.warnings) {
                setWarnings(data.warnings);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : "Something went wrong");
        } finally {
            setIsSearching(false);
        }
    }

    function handleTagClick(tagText: string) {
        setQuery(tagText);
        void handleSearch(tagText);
    }

    async function handleClearHistory() {
        const token = getAccessToken();
        if (!token) return;

        try {
            const res = await fetch(`${API_URL}/search-history/clear/`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (res.ok) {
                setHistory([]);
            }
        } catch { }
    }

    return (
        <>
            <AppHeader />
            <main className="min-h-screen bg-zinc-50">
                <section className="border-b border-zinc-200 bg-white shadow-sm">
                    <div className="mx-auto max-w-7xl px-5 py-12">
                        <div className="max-w-3xl">
                            <p className="mt-2 text-zinc-600">
                                Search naturally in your own words, e.g. &quot;apartment in Berlin under 1500&quot; or &quot;cozy house with 3 rooms&quot;.
                            </p>
                        </div>

                        <form
                            onSubmit={(e) => {
                                e.preventDefault();
                                void handleSearch(query);
                            }}
                            className="mt-8 flex gap-3 max-w-3xl"
                        >
                            <div className="relative flex-1">
                                <input
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    type="text"
                                    placeholder="Type your search request..."
                                    className="h-12 w-full rounded-md border border-zinc-200 pl-11 pr-4 text-sm placeholder:text-zinc-400 outline-none focus:border-zinc-400 focus:ring-1 focus:ring-zinc-400"
                                />
                                <Search className="absolute left-4 top-3.5 text-zinc-400" size={18} />
                            </div>
                            <button
                                type="submit"
                                disabled={isSearching}
                                className="h-12 rounded-md bg-zinc-950 px-6 text-sm font-medium text-white hover:bg-zinc-800 disabled:opacity-60"
                            >
                                {isSearching ? "Searching..." : "Search"}
                            </button>
                        </form>

                        {popular.length > 0 && (
                            <div className="mt-4 flex flex-wrap items-center gap-2 max-w-3xl">
                                <span className="flex items-center gap-1 text-xs font-medium text-zinc-500 mr-1">
                                    <TrendingUp size={13} />
                                    Popular:
                                </span>
                                {popular.map((item, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => handleTagClick(item.query)}
                                        className="rounded-full bg-zinc-100 hover:bg-zinc-200 px-3 py-1 text-xs text-zinc-600 font-medium transition-colors"
                                    >
                                        {item.query}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                </section>

                <section className="mx-auto max-w-7xl px-5 py-8 grid lg:grid-cols-[1fr_300px] gap-8">
                    <div>
                        {error && (
                            <div className="mb-4 rounded-md border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
                                {error}
                            </div>
                        )}

                        {warnings.length > 0 && (
                            <div className="mb-4 rounded-md border border-amber-200 bg-amber-50 p-4 text-amber-700 text-sm flex items-start gap-2">
                                <AlertCircle size={18} className="mt-0.5 shrink-0" />
                                <div>
                                    {warnings.map((w, idx) => (
                                        <p key={idx}>{w}</p>
                                    ))}
                                </div>
                            </div>
                        )}

                        {interpretedFilters && Object.keys(interpretedFilters).length > 0 && (
                            <div className="mb-6 rounded-md border border-indigo-100 bg-indigo-50/50 p-4 text-sm text-indigo-950">
                                <span className="font-semibold block mb-1">Interpreted Filters:</span>
                                <div className="flex flex-wrap gap-2">
                                    {Object.entries(interpretedFilters).map(([key, val]) => (
                                        <span key={key} className="bg-indigo-100/80 px-2 py-0.5 rounded text-xs">
                                            <strong>{key}:</strong> {String(val)}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {results.length > 0 ? (
                            <div className="grid gap-5 md:grid-cols-2">
                                {results.map((property) => (
                                    <PropertyCard key={property.id} property={property} />
                                ))}
                            </div>
                        ) : (
                            <div className="rounded-lg border border-dashed border-zinc-300 bg-white p-12 text-center">
                                <h3 className="text-base font-semibold text-zinc-950">
                                    {isSearching ? "Searching listings..." : "No search results yet"}
                                </h3>
                                <p className="mt-2 text-sm text-zinc-500">
                                    {isSearching
                                        ? "AI is parsing your query and retrieving matching properties."
                                        : "Enter a natural text query in the search box to find matching properties."}
                                </p>
                            </div>
                        )}
                    </div>

                    <aside className="space-y-6">
                        <div className="rounded-lg border border-zinc-200 bg-white p-5 shadow-sm">
                            <h3 className="flex items-center justify-between text-sm font-semibold text-zinc-950 border-b border-zinc-100 pb-3">
                                <span className="flex items-center gap-2">
                                    <History size={16} className="text-zinc-500" />
                                    Your Search History
                                </span>
                                {history.length > 0 && (
                                    <button
                                        onClick={handleClearHistory}
                                        className="text-xs font-normal text-red-600 hover:text-red-800 transition-colors"
                                    >
                                        Clear
                                    </button>
                                )}
                            </h3>
                            {history.length > 0 ? (
                                <ul className="mt-3 divide-y divide-zinc-100">
                                    {history.slice(0, 8).map((item) => (
                                        <li key={item.id} className="py-2.5">
                                            <button
                                                onClick={() => handleTagClick(item.query)}
                                                className="text-left text-sm text-zinc-600 hover:text-zinc-900 hover:underline line-clamp-2 w-full font-medium"
                                            >
                                                {item.query}
                                            </button>
                                            <span className="block text-[10px] text-zinc-400 mt-0.5">
                                                {new Date(item.created_at).toLocaleDateString()}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="mt-3 text-xs text-zinc-500 leading-5">
                                    {getAccessToken()
                                        ? "No search history yet."
                                        : "Sign in and perform search queries to view your history here."}
                                </p>
                            )}
                        </div>
                    </aside>
                </section>
            </main>
        </>
    );
}
