import { useEffect, useRef, useCallback, useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { io, Socket } from 'socket.io-client';

export const useSocket = () => {
  const { user } = useUser();
  const socketRef = useRef<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const connect = useCallback(() => {
    if (!user?.id) return;

    const socketUrl = 'http://localhost:8080';
    socketRef.current = io(socketUrl, {
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 5000,
    });

    socketRef.current.on('connect', () => {
      console.log('Socket.IO connected');
      setIsConnected(true);
      
      // Authenticate with the server
      socketRef.current?.emit('authenticate', { user_id: user.id }, (response: any) => {
        if (response.status === 'success') {
          console.log('Socket.IO authenticated');
        } else {
          console.error('Socket.IO authentication failed');
        }
      });
    });

    socketRef.current.on('disconnect', () => {
      console.log('Socket.IO disconnected');
      setIsConnected(false);
    });

    socketRef.current.on('connect_error', (error) => {
      console.error('Socket.IO connection error:', error);
      setIsConnected(false);
    });
    
  }, [user?.id]);

  // Add a function to send messages via Socket.IO
  const sendMessage = useCallback((event: string, data: any) => {
    if (socketRef.current && socketRef.current.connected) {
      console.log(`Emitting ${event} event:`, data);
      socketRef.current.emit(event, data);
      return true;
    }
    console.log('Socket not connected, cannot send message');
    return false;
  }, []);
  
  const sendTyping = useCallback((conversationId: string) => {
    if (user?.id) {
      sendMessage('typing', {
        user_id: user.id,
        conversationId
      });
    }
  }, [user?.id, sendMessage]);

  const sendSeen = useCallback((conversationId: string) => {
    if (user?.id) {
      sendMessage('seen', {
        user_id: user.id,
        conversationId
      });
    }
  }, [user?.id, sendMessage]);
  
  // Add a new function specifically for sending chat messages via Socket.IO
  const sendChatMessage = useCallback((content: string, conversationId: string, files: any[] = []) => {
    if (user?.id) {
      return sendMessage('message', {
        user_id: user.id,
        conversationId,
        content,
        files
      });
    }
    return false;
  }, [user?.id, sendMessage]);

  useEffect(() => {
    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, [connect]);

  return { 
    isConnected, 
    sendTyping, 
    sendSeen,
    sendChatMessage, // Add the new function to the returned object
    sendMessage: (message: any) => sendMessage('message', message),
    socket: socketRef.current // Expose the socket instance
  };
};