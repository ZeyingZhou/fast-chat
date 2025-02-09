import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function RootLayout({children}: {children: React.ReactNode}) {
    const user = await currentUser();

    if (!user) {
        redirect("/sign-in");
    }

    return (
        <>
            {children}
        </>
    )
}