'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { useSocket } from '@/hooks/useSocket';
import { useUser } from '@clerk/nextjs';

type SocketContextType = {
  isConnected: boolean;
  sendTyping: (conversationId: string) => void;
  sendSeen: (conversationId: string) => void;
};

const SocketContext = createContext<SocketContextType>({
  isConnected: false,
  sendTyping: () => {},
  sendSeen: () => {},
});

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);
  const { socket, addMessageHandler } = useSocket();
  const { user } = useUser();

  useEffect(() => {
    if (!user?.id) return;
    const wsUrl = `ws://localhost:8080/ws/${user.id}`;
    console.log("Attempting to connect to WebSocket at:", wsUrl);
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('Connected to WebSocket');
      setIsConnected(true);
      socket.current = ws;
    };

    ws.onclose = () => {
      console.log('Disconnected from WebSocket');
      setIsConnected(false);
      socket.current = null;
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [user?.id]);

  const sendTyping = (conversationId: string) => {
    socket.current?.send(JSON.stringify({
      type: 'typing',
      conversationId
    }));
  };

  const sendSeen = (conversationId: string) => {
    socket.current?.send(JSON.stringify({
      type: 'seen',
      conversationId
    }));
  };

  useEffect(() => {
    if (!socket.current) return;

    const messageHandler = (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'NEW_MESSAGE':
          window.dispatchEvent(new CustomEvent('new-message', { 
            detail: data.message 
          }));
          break;
        case 'typing':
          window.dispatchEvent(new CustomEvent('user-typing', { 
            detail: { 
              userId: data.userId,
              conversationId: data.conversationId 
            } 
          }));
          break;
        case 'seen':
          window.dispatchEvent(new CustomEvent('message-seen', { 
            detail: { 
              userId: data.userId,
              conversationId: data.conversationId 
            } 
          }));
          break;
      }
    };

    socket.current.addEventListener('message', messageHandler);

    return () => {
      socket.current?.removeEventListener('message', messageHandler);
    };
  }, [socket.current]);

  return (
    <SocketContext.Provider value={{ isConnected, sendTyping, sendSeen }}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocketContext = () => useContext(SocketContext); 