import { useEffect, useRef, useCallback } from 'react';
import { useChatStore } from '@/stores/chatStore';
import { wsService } from '@/services/websocket';
import { Message } from '@/types';

export const useWebSocket = () => {
  const {
    config,
    currentConversation,
    addMessage,
    updateMessage,
    setIsConnected,
    setIsLoading,
    setError,
  } = useChatStore();

  const streamingMessageRef = useRef<string | null>(null);
  const accumulatedContentRef = useRef<string>('');

  useEffect(() => {
    const connectWebSocket = async () => {
      try {
        await wsService.connect();
      } catch (error) {
        console.error('Failed to connect WebSocket:', error);
        setError('Failed to connect to server. Please try again.');
      }
    };

    connectWebSocket();

    // Setup connection handler
    const unsubConnection = wsService.onConnection((connected) => {
      setIsConnected(connected);
      if (connected) {
        setError(null);
      }
    });

    // Setup message handler
    const unsubMessage = wsService.onMessage((wsMessage) => {
      if (wsMessage.type === 'error') {
        setError(wsMessage.data.error || 'An error occurred');
        setIsLoading(false);
        
        // Update message with error
        if (streamingMessageRef.current) {
          updateMessage(streamingMessageRef.current, {
            error: wsMessage.data.error,
            isStreaming: false,
          });
          streamingMessageRef.current = null;
        }
        return;
      }

      if (wsMessage.type === 'stream') {
        const content = wsMessage.data.content || '';

        if (!streamingMessageRef.current) {
          // Create new streaming message
          const newMessage: Message = {
            id: crypto.randomUUID(),
            role: 'assistant',
            content,
            timestamp: new Date(),
            isStreaming: true,
          };
          
          addMessage(newMessage);
          streamingMessageRef.current = newMessage.id;
          accumulatedContentRef.current = content;
        } else {
          // Update existing streaming message
          accumulatedContentRef.current += content;
          updateMessage(streamingMessageRef.current, {
            content: accumulatedContentRef.current,
            isStreaming: true,
          });
        }
      }

      if (wsMessage.type === 'end') {
        // Finalize streaming message
        if (streamingMessageRef.current) {
          updateMessage(streamingMessageRef.current, {
            isStreaming: false,
          });
          streamingMessageRef.current = null;
          accumulatedContentRef.current = '';
        }
        setIsLoading(false);
      }
    });

    // Setup error handler
    const unsubError = wsService.onError((error) => {
      console.error('WebSocket error:', error);
      setError('Connection error. Please check your internet connection.');
      setIsLoading(false);
    });

    // Cleanup
    return () => {
      unsubConnection();
      unsubMessage();
      unsubError();
      wsService.disconnect();
    };
  }, [setIsConnected, setError, setIsLoading, addMessage, updateMessage]);

  const sendMessage = useCallback(
    (content: string) => {
      if (!wsService.isConnected()) {
        setError('Not connected to server. Please wait...');
        return;
      }

      try {
        // Add user message
        const userMessage: Message = {
          id: crypto.randomUUID(),
          role: 'user',
          content,
          timestamp: new Date(),
        };
        
        addMessage(userMessage);
        setIsLoading(true);
        setError(null);

        // Send to server
        wsService.sendMessage(
          content,
          config.provider,
          currentConversation?.id
        );
      } catch (error) {
        console.error('Failed to send message:', error);
        setError('Failed to send message. Please try again.');
        setIsLoading(false);
      }
    },
    [config.provider, currentConversation?.id, addMessage, setIsLoading, setError]
  );

  const stopStreaming = useCallback(() => {
    // TODO: Implement stop streaming functionality
    // This will require backend support to cancel ongoing requests
    if (streamingMessageRef.current) {
      updateMessage(streamingMessageRef.current, {
        isStreaming: false,
      });
      streamingMessageRef.current = null;
      accumulatedContentRef.current = '';
    }
    setIsLoading(false);
  }, [updateMessage, setIsLoading]);

  return {
    sendMessage,
    stopStreaming,
    isStreaming: !!streamingMessageRef.current,
  };
};
