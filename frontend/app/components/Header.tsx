'use client'

import { Building2, Heart, Home, Plus, Search, UserRound } from "lucide-react";
import type { User } from "@/types/api";
import Link from "next/link";

type HeaderProps = {
    user: User | null,
    onLogout?: () => void
}

const commonLinks = [
    { label: "Properties", href: "/", icon: Home },
    { label: "Popular", href: "/popular", icon: Building2 },
    { label: "Search", href: "/search", icon: Search },
]
const linkClass = "flex h-10 items-center gap-2 rounded-md px-3 font-medium leading-6 text-zinc-600 hover:bg-zinc-100 hover:text-zinc-950 "
export default function Header({ user, onLogout }: HeaderProps) {
    return (
        <header className="sticky top-0 z-40 border-b border-zinc-200 bg-white/95 backdrop-blur">
            <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5">
                <Link href="/" className="flex items-center gap-2">
                    <div className="flex h-9 w-9 items-center justify-center rounded-md bg-zinc-950 text-white">
                        <Building2 size={19} />
                    </div>
                    <span className="text-lg font-semibold tracking-normal text-zinc-950">
                        Rentify
                    </span>
                </Link>

                <nav className="hidden items-center gap-1 md:flex">
                    {commonLinks.map(({ label, href, icon: Icon }) => (
                        <Link
                            key={label}
                            href={href}
                            className={linkClass}
                        >
                            <Icon size={19} />
                            {label}
                        </Link>
                    ))}
                    {user?.role === "tenant" && (
                        <>
                            <Link
                                href="/favorites"
                                className={linkClass}
                            >
                                <Heart size={19} />
                                Favorites
                            </Link>
                            <Link
                                href="/bookings" className={linkClass}
                            >
                                My Bookings
                            </Link>
                        </>
                    )}
                    {user?.role === "landlord" && (
                        <>
                            <Link
                                href="/bookings"
                                className={linkClass}
                            >
                                My Bookings
                            </Link>
                            <Link
                                href="/properties/new"
                                className={linkClass}
                            >
                                <Plus size={19} />
                                New Property
                            </Link>
                        </>
                    )}
                </nav>

                <div className="flex items-center gap-2">
                    {user ? (
                        <>
                            <div className="flex h-9 items-center gap-2 rounded-md border border-zinc-200 px-3 text-sm font-medium text-zinc-700">
                                <UserRound size={16} />
                                {user.username}
                                <span className="rounded bg-zinc-100 px-2 py-0.5 text-xs capitalize text-zinc-500">
                                    {user.role}
                                </span>
                            </div>
                            <button
                                type="button"
                                onClick={onLogout}
                                className="h-9 rounded-md px-3 text-sm font-medium text-zinc-700 hover:bg-zinc-100"
                            >
                                Logout
                            </button>
                        </>
                    )
                        : (
                            <>
                                <Link href="/login" className="hidden h-9 items-center rounded-md px-3 text-sm font-medium text-zinc-700 hover:bg-zinc-100 md:flex">Sign in</Link>
                                <Link href="/register" className="flex h-9 items-center rounded-md bg-zinc-700 px-3 text-sm font-medium text-white hover:bg-zinc-800 md:flex">Create account</Link>
                            </>
                        )
                    }
                </div>
            </div>
        </header>
    )
}
