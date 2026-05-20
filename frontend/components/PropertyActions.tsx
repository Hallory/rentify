"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Edit, Trash, EyeOff, Eye } from "lucide-react";

import { getMe } from "@/lib/auth";
import { deleteProperty, togglePropertyActive } from "@/lib/properties";
import { getAccessToken } from "@/lib/token";
import type { Property, User } from "@/types/api";

type PropertyActionsProps = {
    property: Property;
};

export default function PropertyActions({ property }: PropertyActionsProps) {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isToggling, setIsToggling] = useState(false);
    const [status, setStatus] = useState(property.status);

    useEffect(() => {
        const token = getAccessToken();
        if (!token) return;

        getMe(token)
            .then(setUser)
            .catch(() => setUser(null));
    }, []);

    if (!user || user.role !== "landlord" || user.id !== property.owner) {
        return null;
    }

    async function handleToggleActive() {
        const token = getAccessToken();
        if (!token) return;

        setIsToggling(true);
        try {
            const updated = await togglePropertyActive(token, property.id);
            setStatus(updated.status);
            router.refresh();
        } catch (err) {
            alert(err instanceof Error ? err.message : "Failed to toggle status");
        } finally {
            setIsToggling(false);
        }
    }

    async function handleDelete() {
        if (!confirm("Are you sure you want to delete this listing? This action cannot be undone.")) {
            return;
        }

        const token = getAccessToken();
        if (!token) return;

        setIsDeleting(true);
        try {
            await deleteProperty(token, property.id);
            router.push("/");
            router.refresh();
        } catch (err) {
            alert(err instanceof Error ? err.message : "Failed to delete property");
            setIsDeleting(false);
        }
    }

    return (
        <div className="mt-6 flex flex-wrap gap-3 border-t border-zinc-100 pt-6">
            <Link
                href={`/properties/${property.id}/edit`}
                className="flex h-10 items-center gap-2 rounded-md border border-zinc-200 bg-white px-4 text-sm font-medium text-zinc-700 hover:bg-zinc-50 shadow-sm"
            >
                <Edit size={16} />
                Edit Listing
            </Link>

            <button
                type="button"
                onClick={handleToggleActive}
                disabled={isToggling}
                className="flex h-10 items-center gap-2 rounded-md border border-zinc-200 bg-white px-4 text-sm font-medium text-zinc-700 hover:bg-zinc-50 shadow-sm"
            >
                {status === "published" ? (
                    <>
                        <EyeOff size={16} />
                        {isToggling ? "Hiding..." : "Hide Listing (Draft)"}
                    </>
                ) : (
                    <>
                        <Eye size={16} />
                        {isToggling ? "Publishing..." : "Publish Listing"}
                    </>
                )}
            </button>

            <button
                type="button"
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex h-10 items-center gap-2 rounded-md border border-red-200 bg-red-50 px-4 text-sm font-medium text-red-700 hover:bg-red-100 shadow-sm"
            >
                <Trash size={16} />
                {isDeleting ? "Deleting..." : "Delete Listing"}
            </button>
        </div>
    );
}
