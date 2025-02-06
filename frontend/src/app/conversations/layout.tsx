import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Sidebar from "./sidebar";
export default async function ConversationsLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { userId } = await auth()
    if (!userId) {
        redirect('/sign-in')
    }
    return (
        <Sidebar>
            <div>
                <ConversationList
                    users={users}
                    title="Conversations"
                    initialItems={conversations}
                />
            {children}
            </div>
        </Sidebar>
    );
}