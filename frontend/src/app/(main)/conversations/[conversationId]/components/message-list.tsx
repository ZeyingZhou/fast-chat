'use client';

import { useEffect, useRef, useState } from "react";
import useConversation from "@/hooks/use-conversation";

import MessageBox from "./message-box";
import { useSocketContext } from "@/components/providers/socket-provider";
import { Message } from "@/types";

interface MessagesListProps {
    initialMessages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({ initialMessages = [] }) => {
    const bottomRef = useRef<HTMLDivElement>(null);
    const [messages, setMessages] = useState(initialMessages ?? []);
    const { conversationId } = useConversation();
    const { sendSeen } = useSocketContext();

    // Mark messages as seen when conversation opens or new messages arrive
    useEffect(() => {
        sendSeen(conversationId);
    }, [conversationId, messages.length]);

    // Scroll to bottom on new messages
    useEffect(() => {
        bottomRef?.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Listen for new messages
    useEffect(() => {
        const handleNewMessage = (event: CustomEvent) => {
            const newMessage = event.detail;
            
            // Avoid duplicate messages
            setMessages((current) => {
                if (current.some(msg => msg.id === newMessage.id)) {
                    return current;
                }
                return [...current, newMessage];
            });

            // Mark as seen
            sendSeen(conversationId);
            
            // Scroll to bottom
            bottomRef?.current?.scrollIntoView({ behavior: 'smooth' });
        };

        // Listen for message updates (e.g., seen status)
        const handleMessageUpdate = (event: CustomEvent) => {
            const updatedMessage = event.detail;
            setMessages((current) => 
                current.map((msg) => 
                    msg.id === updatedMessage.id ? updatedMessage : msg
                )
            );
        };

        // Add event listeners
        window.addEventListener('new-message', handleNewMessage as EventListener);
        window.addEventListener('message-seen', handleMessageUpdate as EventListener);

        // Cleanup
        return () => {
            window.removeEventListener('new-message', handleNewMessage as EventListener);
            window.removeEventListener('message-seen', handleMessageUpdate as EventListener);
        };
    }, [conversationId, sendSeen]);

    return (
        <div className="flex-1 overflow-y-auto">
            {messages?.length > 0 ? (
                messages.map((message, i) => (
                    <MessageBox 
                        isLast={i === messages.length - 1} 
                        key={message.id} 
                        data={message}
                    />
                ))
            ) : (
                <div className="flex justify-center items-center h-full">
                    <p className="text-gray-500">No messages yet</p>
                </div>
            )}
            <div className="pt-24" ref={bottomRef} />
        </div>
    );
}

export default MessagesList;