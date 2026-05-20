import AppHeader from "@/components/AppHeader";
import NewPropertyForm from "@/components/NewPropertyForm";
import { getProperty } from "@/lib/properties";

type EditPropertyPageProps = {
    params: Promise<{ id: string }>;
};

export default async function EditPropertyPage({ params }: EditPropertyPageProps) {
    const { id } = await params;
    const property = await getProperty(id);

    return (
        <>
            <AppHeader />
            <main className="min-h-screen bg-zinc-50">
                <section className="border-b border-zinc-200 bg-white">
                    <div className="mx-auto max-w-7xl px-5 py-10">
                        <h1 className="text-3xl font-semibold text-zinc-950">Edit property</h1>
                        <p className="mt-2 text-zinc-600">
                            Update details for "{property.title}"
                        </p>
                    </div>
                </section>

                <section className="mx-auto max-w-3xl px-5 py-8">
                    <NewPropertyForm initialData={property} />
                </section>
            </main>
        </>
    );
}
