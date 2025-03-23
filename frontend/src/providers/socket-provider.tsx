'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useUser } from '@clerk/nextjs';

interface SocketContextType {
  socket: Socket | null;
  isConnected: boolean;
  sendMessage: (event: string, data: any) => boolean;
  joinConversation: (conversationId: string) => boolean;
  leaveConversation: (conversationId: string) => boolean;
  checkRooms: () => void;
}

const SocketContext = createContext<SocketContextType>({
  socket: null,
  isConnected: false,
  sendMessage: () => false,
  joinConversation: () => false,
  leaveConversation: () => false,
  checkRooms: () => {},
});

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const { user, isLoaded } = useUser();

  useEffect(() => {
    if (!isLoaded || !user?.id) return;

    let socketInstance: Socket | null = null;

    const initializeSocket = () => {
      if (socketInstance) {
        socketInstance.disconnect();
      }

      const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:8080';
      console.log('Initializing socket connection to:', socketUrl);

      socketInstance = io(socketUrl, {
        autoConnect: true,
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 5000,
        timeout: 10000,
        transports: ['websocket', 'polling'],
        withCredentials: true,
      });

      socketInstance.on('connect', () => {
        console.log('Socket connected with ID:', socketInstance?.id);
        setIsConnected(true);
        
        socketInstance?.emit('authenticate', { user_id: user.id }, (response: any) => {
          if (response?.status === 'success') {
            console.log('Socket authenticated successfully');
          } else {
            console.error('Socket authentication failed:', response);
          }
        });
      });

      socketInstance.on('disconnect', (reason) => {
        console.log('Socket disconnected. Reason:', reason);
        setIsConnected(false);
      });

      socketInstance.on('connect_error', (error) => {
        console.error('Socket connection error:', error.message);
        console.error('Error details:', {
          name: error.name,
          message: error.message,
          stack: error.stack,
          url: socketUrl
        });
        setIsConnected(false);
      });

      socketInstance.on('error', (error) => {
        console.error('Socket general error:', error);
        setIsConnected(false);
      });

      socketInstance.on('reconnect_attempt', (attemptNumber) => {
        console.log(`Socket reconnection attempt #${attemptNumber}`);
      });

      socketInstance.on('reconnect_failed', () => {
        console.error('Socket failed to reconnect after all attempts');
      });

      setSocket(socketInstance);
    };

    initializeSocket();

    return () => {
      console.log('Cleaning up socket connection');
      if (socketInstance) {
        socketInstance.disconnect();
        socketInstance = null;
      }
    };
  }, [user?.id, isLoaded]);

  const sendMessage = (event: string, data: any): boolean => {
    if (socket && isConnected) {
      console.log(`Emitting ${event} event:`, data);
      socket.emit(event, data);
      return true;
    }
    console.log('Socket not connected, cannot send message');
    return false;
  };

  const joinConversation = (conversationId: string): boolean => {
    if (socket && isConnected) {
      console.log(`Joining conversation: ${conversationId}`);
      socket.emit('join_conversation', { conversationId });
      return true;
    }
    console.log('Socket not connected, cannot join conversation');
    return false;
  };

  const leaveConversation = (conversationId: string): boolean => {
    if (socket && isConnected) {
      console.log(`Leaving conversation: ${conversationId}`);
      socket.emit('leave_conversation', { conversationId });
      return true;
    }
    console.log('Socket not connected, cannot leave conversation');
    return false;
  };

  const checkRooms = (): void => {
    if (socket && isConnected) {
      console.log('Checking room membership...');
      socket.emit('get_room_info', {}, (response: any) => {
        console.log('Room membership:', response);
      });
    } else {
      console.log('Socket not connected, cannot check rooms');
    }
  };

  return (
    <SocketContext.Provider value={{ 
      socket, 
      isConnected, 
      sendMessage,
      joinConversation,
      leaveConversation,
      checkRooms
    }}>
      {children}
    </SocketContext.Provider>
  );
}; 