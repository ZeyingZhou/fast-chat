'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { useSocket } from '@/hooks/useSocket';

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
    addMessageHandler((event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'NEW_MESSAGE':
          window.dispatchEvent(new CustomEvent('new-message', { 
            detail: data.message 
          }));
          break;
        case 'typing':
          window.dispatchEvent(new CustomEvent('user-typing', { 
            detail: { userId: data.userId } 
          }));
          break;
        case 'seen':
          window.dispatchEvent(new CustomEvent('message-seen', { 
            detail: { userId: data.userId } 
          }));
          break;
      }
    });
  }, [addMessageHandler]);

  return (
    <SocketContext.Provider value={{ isConnected, sendTyping, sendSeen }}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocketContext = () => useContext(SocketContext); 