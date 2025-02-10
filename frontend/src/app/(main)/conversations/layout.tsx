import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import ConversationList from "./components/conversation-list";
import Sidebar from "./components/sidebar";
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
            <ConversationList/>
            {children}
        </>
    );
}

export default ConversationsLayout;