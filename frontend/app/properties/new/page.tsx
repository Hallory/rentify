import AppHeader from "@/components/AppHeader";
import NewPropertyForm from "@/components/NewPropertyForm";

export default function NewPropertyPage() {
    return (
        <>
            <AppHeader />
            <main className="min-h-screen bg-zinc-50">
                <section className="border-b border-zinc-200 bg-white">
                    <div className="mx-auto max-w-7xl px-5 py-10">
                        <h1 className="text-3xl font-semibold text-zinc-950">New property</h1>
                        <p className="mt-2 text-zinc-600">
                            Create a rental listing as a landlord.
                        </p>
                    </div>
                </section>

                <section className="mx-auto max-w-3xl px-5 py-8">
                    <NewPropertyForm />
                </section>
            </main>
        </>
    );
}
