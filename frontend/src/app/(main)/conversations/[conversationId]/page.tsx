// "use client";

import getConversationById from "@/actions/get-conversationById";
import getMessages from "@/actions/get-messages";
import EmptyState from "../../components/empty-state";
import Header from "./components/header";
import ChatInput from "./components/chat-input";
import MessagesList from "./components/message-list";
import { useSocket } from "@/hooks/use-socket";
// import { useEffect } from "react";


interface ConversationIdPageProps {     
    params: Promise<{ conversationId: string }>
}

const ConversationIdPage: React.FC<ConversationIdPageProps> = async ({ params }) => {
    const { conversationId } = await params;
    const conversation = await getConversationById(conversationId);
    const messages = await getMessages(conversationId);
    // const { socket, isConnected } = useSocket();

    // useEffect(() => {
    //     if (socket && isConnected && conversationId) {
    //         socket.emit('join_conversation', { conversationId });
            
    //         return () => {
    //             socket.emit('leave_conversation', { conversationId });
    //         };
    //     }
    // }, [socket, isConnected, conversationId]);

    if(!conversation) {
        return (
            <div className="lg:pl-[464px] h-full">
                <div className="h-full flex flex-col">
                    <EmptyState />
                </div>
            </div>
        )
    }
    return ( 
        <div className="lg:pl-[464px] h-full">
            <div className="h-full flex flex-col">
                <Header conversation={conversation} />
                <MessagesList initialMessages={messages} />
                <ChatInput />
            </div>
        </div>
     );
}
 
export default ConversationIdPage;