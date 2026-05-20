"use client";
import { login } from '@/lib/auth'
import { setTokens } from '@/lib/token'
import { Building2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import React from 'react'


export default function LoginForm() {
    const router = useRouter()
    const [email, setEmail] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [error, setError] = React.useState<string | null>(null)
    const [isSubmitting, setIsSubmitting] = React.useState(false)

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError(null)
        setIsSubmitting(true)

        try {
            const tokens = await login({ email, password });
            setTokens(tokens);
            router.push("/");
            router.refresh();

        } catch {
            setError("Invalid email or password");
        } finally {
            setIsSubmitting(false);
        }

    }
    return (
        <main className='min-h-screen bg-zinc-50'>
            <div className='mx-auto flex min-h-screen max-w-md flex-col justify-center px-5'>
                <div className='mb-8 flex items-center gap-3'>
                    <div className='flex h-11 w-11 items-center justify-center rounded-md bg-zinc-950 text-white'>
                        <Building2 size={21} />
                    </div>
                    <div>
                        <h1 className='text-xl font-semibold text-zinc-950'>Rentify</h1>
                        <p className='text-sm text-zinc-500'>Sign in to your account</p>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className='rounded-lg border border-zinc-200 bg-white p-8 shadow-sm'>
                    <div>
                        <label className='text-sm font-medium text-zinc-700'>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder='tenant@example.com'
                            required
                            className='mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 py-2 text-sm placeholder:text-zinc-400 focus:z-10 focus:border-zinc-500 focus:outline-none focus:ring-zinc-500'
                        />
                    </div>

                    <div className='mt-4'>
                        <label className='text-sm font-medium text-zinc-700'>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className='mt-2 h-11 w-full rounded-md border border-zinc-200 px-3 py-2 text-sm placeholder:text-zinc-400 focus:z-10 focus:border-zinc-500 focus:outline-none focus:ring-zinc-500'
                        />
                    </div>
                    {error && (
                        <div className='mt-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700'>
                            {error}
                        </div>
                    )}

                    <button
                        type='submit'
                        disabled={isSubmitting}
                        className="mt-5 h-11 w-full rounded-md bg-zinc-950 text-sm font-medium text-white hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-60">
                        {isSubmitting ? "Signing in..." : "Sign in"}
                    </button>
                </form>
                <div className='mt-4 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-500'>
                    <div className="mt-4 rounded-lg border border-zinc-200 bg-white p-4 text-sm text-zinc-600">
                        <p className="font-medium text-zinc-800">Demo accounts</p>
                        <div className="mt-2 space-y-1">
                            <p>Tenant: demo.tenant1@example.com</p>
                            <p>Landlord: demo.landlord1@example.com</p>
                            <p>Password: password123</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    )
}