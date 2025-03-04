import { useEffect, useRef, useCallback } from 'react';
import { useUser } from '@clerk/nextjs';

export const useSocket = () => {
  const { user } = useUser();
  const socket = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (!user?.id) return;

    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/${user.id}`;
    socket.current = new WebSocket(wsUrl);

    socket.current.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.current.onclose = () => {
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(connect, 5000);
    };

    socket.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }, [user?.id]);

  const addMessageHandler = useCallback((handler: (event: MessageEvent) => void) => {
    if (socket.current) {
      socket.current.onmessage = handler;
    }
  }, []);

  // Add a function to send messages via WebSocket
  const sendMessage = useCallback((message: any) => {
    if (socket.current && socket.current.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify(message));
      return true;
    }
    return false;
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (socket.current) {
        socket.current.close();
      }
    };
  }, [connect]);

  return { socket, addMessageHandler, sendMessage };
}; 