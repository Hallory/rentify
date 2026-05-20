"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Building2 } from "lucide-react";
import { useState } from "react";

import { login, register } from "@/lib/auth";
import { setTokens } from "@/lib/token";
import type { UserRole } from "@/types/api";

export default function RegisterForm() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState<UserRole>("tenant");
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    async function handleSubmit() {
        setError(null);
        setIsSubmitting(true);

        try {
            await register({
                email,
                username,
                first_name: firstName,
                last_name: lastName,
                password,
                role,
            });

            const tokens = await login({ email, password });
            setTokens(tokens);
            router.push("/");
            router.refresh();
        } catch (error) {
            setError(error instanceof Error ? error.message : "Registration failed");
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <main className="min-h-screen bg-zinc-50">
            <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-5 py-10">
                <div className="mb-8 flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-md bg-zinc-950 text-white">
                        <Building2 size={21} />
                    </div>
                    <div>
                        <h1 className="text-xl font-semibold text-zinc-950">Rentify</h1>
                        <p className="text-sm text-zinc-500">Create your account</p>
                    </div>
                </div>

                <form
                    onSubmit={(event) => {
                        event.preventDefault();
                        void handleSubmit();
                    }}
                    className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm"
                >
                    <div>
                        <label className="text-sm font-medium text-zinc-700">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>

                    <div className="mt-4">
                        <label className="text-sm font-medium text-zinc-700">Username</label>
                        <input
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
                    </div>

                    <div className="mt-4 grid gap-3 sm:grid-cols-2">
                        <div>
                            <label className="text-sm font-medium text-zinc-700">First name</label>
                            <input
                                value={firstName}
                                onChange={(event) => setFirstName(event.target.value)}
                                className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium text-zinc-700">Last name</label>
                            <input
                                value={lastName}
                                onChange={(event) => setLastName(event.target.value)}
                                className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                            />
                        </div>
                    </div>

                    <div className="mt-4">
                        <label className="text-sm font-medium text-zinc-700">Role</label>
                        <select
                            value={role}
                            onChange={(event) => setRole(event.target.value as UserRole)}
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 bg-white px-3 text-sm outline-none focus:border-zinc-400"
                        >
                            <option value="tenant">Tenant</option>
                            <option value="landlord">Landlord</option>
                        </select>
                    </div>

                    <div className="mt-4">
                        <label className="text-sm font-medium text-zinc-700">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            minLength={8}
                            required
                            className="mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 text-sm outline-none focus:border-zinc-400"
                        />
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
                        {isSubmitting ? "Creating account..." : "Create account"}
                    </button>
                </form>

                <p className="mt-4 text-center text-sm text-zinc-600">
                    Already have an account?{" "}
                    <Link href="/login" className="font-medium text-zinc-950 hover:underline">
                        Sign in
                    </Link>
                </p>
            </div>
        </main>
    );
}
