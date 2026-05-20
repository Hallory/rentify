"use client";

import AppHeader from "@/components/AppHeader";
import { Heart } from "lucide-react";
import Link from "next/link";

export default function FavoritesPage() {
    return (
        <>
            <AppHeader />
            <main className="min-h-screen bg-zinc-50 flex flex-col justify-between">
                <div>
                    <section className="border-b border-zinc-200 bg-white">
                        <div className="mx-auto max-w-7xl px-5 py-10">
                            <h1 className="text-3xl font-semibold text-zinc-950">Favorites</h1>
                            <p className="mt-2 text-zinc-600">
                                Properties you've saved to your list
                            </p>
                        </div>
                    </section>

                    <section className="mx-auto max-w-7xl px-5 py-16">
                        <div className="rounded-lg border border-dashed border-zinc-300 bg-white p-12 text-center max-w-xl mx-auto shadow-sm">
                            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-50 text-red-500">
                                <Heart size={24} />
                            </div>
                            <h2 className="mt-4 text-base font-semibold text-zinc-950">
                                No favorite properties yet
                            </h2>
                            <p className="mt-2 text-sm text-zinc-500 leading-6">
                                Click the heart button on property cards to save listings here. This feature is currently being finalized.
                            </p>
                            <div className="mt-6">
                                <Link
                                    href="/"
                                    className="inline-flex h-10 items-center justify-center rounded-md bg-zinc-950 px-4 text-sm font-medium text-white hover:bg-zinc-800 transition-colors"
                                >
                                    Browse Properties
                                </Link>
                            </div>
                        </div>
                    </section>
                </div>
            </main>
        </>
    );
}
