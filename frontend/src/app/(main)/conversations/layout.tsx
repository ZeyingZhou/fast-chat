import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import ConversationList from "./components/conversation-list";
import Sidebar from "./components/sidebar";
import getConversations from "@/actions/get-conversations";
import getUsers from "@/actions/get-users";
const ConversationsLayout = async ({
    children,
}: {
    children: React.ReactNode;
}) => {
    const conversations = await getConversations();
    const users = await getUsers();
    const { userId } = await auth()
  
    if (!userId) {
        redirect('/sign-in')
    }
    return (
        <>
            <ConversationList
                users={users}
                initialItems={conversations}
                title="Conversations"
            />
            {children}
        </>
    );
}

export default ConversationsLayout;