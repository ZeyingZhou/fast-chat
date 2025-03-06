'use client';

import { useEffect, useRef, useState } from "react";
import useConversation from "@/hooks/use-conversation";
import { Message } from "@/types";
import MessageBox from "./message-box";
import { useSocket } from "@/hooks/use-socket";

interface MessagesListProps {
    initialMessages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({ initialMessages = [] }) => {
    const bottomRef = useRef<HTMLDivElement>(null);
    const [messages, setMessages] = useState(initialMessages ?? []);
    const { conversationId } = useConversation();
    const { socket } = useSocket();

    // Scroll to bottom when messages change
    useEffect(() => {
        bottomRef.current?.scrollIntoView();
    }, [messages]);

    // Join conversation room
    useEffect(() => {
        if (!socket) return;
        
        console.log(`Joining conversation room: ${conversationId}`);
        socket.emit('join_conversation', { conversationId });
        
        return () => {
            console.log(`Leaving conversation room: ${conversationId}`);
            socket.emit('leave_conversation', { conversationId });
        };
    }, [socket, conversationId]);

    // Listen for new messages - SEPARATE useEffect to avoid dependency issues
    useEffect(() => {
        if (!socket) return;
        
        console.log('Setting up message listener');
        
        const handleMessage = (data: any) => {
            console.log('Received message:', data);
            
            if (data.type === 'NEW_MESSAGE') {
                const message = data.message;
                if (message.conversationId === conversationId) {
                    console.log('Adding new message to state');
                    setMessages(current => [...current, message]);
                }
            } else if (data.conversationId === conversationId) {
                console.log('Adding direct message to state');
                setMessages(current => [...current, data]);
            }
        };
        
        socket.on('message', handleMessage);
        
        return () => {
            console.log('Removing message listener');
            socket.off('message', handleMessage);
        };
    }, [socket, conversationId]); // Don't include messages in dependencies

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