'use client';

import { useEffect, useRef, useState } from "react";
import useConversation from "@/hooks/use-conversation";
import { Message } from "@/types";
import MessageBox from "./message-box";
import { useSocket } from "@/providers/socket-provider";

interface MessagesListProps {
    initialMessages: Message[];
}

const MessagesList: React.FC<MessagesListProps> = ({ initialMessages = [] }) => {
    const bottomRef = useRef<HTMLDivElement>(null);
    const [messages, setMessages] = useState(initialMessages ?? []);
    const { conversationId } = useConversation();
    const { socket, isConnected, joinConversation, leaveConversation } = useSocket();

    // Scroll to bottom when messages change
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Join conversation room when component mounts
    // useEffect(() => {
    //     if (!socket || !isConnected || !conversationId) return;
        
    //     console.log(`Joining conversation room: ${conversationId}`);
    //     joinConversation(conversationId);
    //     console.log(socket);
    //     return () => {
    //         console.log(`Leaving conversation room: ${conversationId}`);
    //         leaveConversation(conversationId);
    //     };
    // }, [socket, isConnected, conversationId, joinConversation, leaveConversation]);

    // Listen for new messages
    useEffect(() => {
        socket?.emit('list_rooms');
        if (!socket || !isConnected || !conversationId) return;
        
        console.log('Setting up message listener for conversation:', conversationId);
        
        const handleMessage = (data: any) => {
            console.log('Received message event:', data);
            
            const message = data;
            if (message.conversationId === conversationId) {
                console.log('Adding new message to state:', message);
                setMessages(current => [...current, message]);
            }
        };
        
        // Listen for 'message received' event
        socket.on('message received', handleMessage);
        
        return () => {
            console.log('Removing message listener');
            socket.off('message received', handleMessage);
        };
    }, [socket, isConnected, conversationId]);

    return (
        <div className="flex-1 overflow-y-auto">
            {messages?.length > 0 ? (
                messages.map((message, i) => (
                    <MessageBox 
                        isLast={i === messages.length - 1} 
                        key={message.id || i} 
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