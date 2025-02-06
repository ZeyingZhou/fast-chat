import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import {CustomSidebar} from "./custom-sidebar";
import {SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar"
export default async function ConversationLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { userId } = await auth()
    if (!userId) {
        redirect('/sign-in')
    }
    return (
        <SidebarProvider>
             <CustomSidebar />
            <div className="flex h-screen">
                {children}
            </div>
        </SidebarProvider>
    );
}