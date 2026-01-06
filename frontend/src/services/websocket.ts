import { io, Socket } from 'socket.io-client';
import { WS_URL } from '@/lib/constants';
import { WebSocketMessage, AIProvider } from '@/types';

type MessageHandler = (message: WebSocketMessage) => void;
type ConnectionHandler = (connected: boolean) => void;
type ErrorHandler = (error: Error) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private messageHandlers: Set<MessageHandler> = new Set();
  private connectionHandlers: Set<ConnectionHandler> = new Set();
  private errorHandlers: Set<ErrorHandler> = new Set();
  private isConnecting = false;

  connect(): Promise<void> {
    if (this.socket?.connected) {
      console.log('WebSocket already connected');
      return Promise.resolve();
    }

    if (this.isConnecting) {
      console.log('WebSocket connection in progress');
      return Promise.resolve();
    }

    this.isConnecting = true;

    return new Promise((resolve, reject) => {
      try {
        this.socket = io(WS_URL, {
          transports: ['websocket', 'polling'],
          reconnection: true,
          reconnectionAttempts: 5,
          reconnectionDelay: 1000,
        });

        this.socket.on('connect', () => {
          console.log('WebSocket connected');
          this.isConnecting = false;
          this.notifyConnectionHandlers(true);
          resolve();
        });

        this.socket.on('disconnect', () => {
          console.log('WebSocket disconnected');
          this.notifyConnectionHandlers(false);
        });

        this.socket.on('message', (data: WebSocketMessage) => {
          this.notifyMessageHandlers(data);
        });

        this.socket.on('stream', (data: WebSocketMessage) => {
          this.notifyMessageHandlers({ ...data, type: 'stream' });
        });

        this.socket.on('error', (error: Error) => {
          console.error('WebSocket error:', error);
          this.isConnecting = false;
          this.notifyErrorHandlers(error);
          reject(error);
        });

        this.socket.on('connect_error', (error: Error) => {
          console.error('WebSocket connection error:', error);
          this.isConnecting = false;
          this.notifyErrorHandlers(error);
          reject(error);
        });
      } catch (error) {
        this.isConnecting = false;
        console.error('Failed to create WebSocket connection:', error);
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.notifyConnectionHandlers(false);
    }
  }

  sendMessage(
    content: string,
    provider: AIProvider,
    conversationId?: string
  ): void {
    if (!this.socket?.connected) {
      throw new Error('WebSocket is not connected');
    }

    const message: WebSocketMessage = {
      type: 'message',
      data: {
        content,
        provider,
        conversationId,
        role: 'user',
      },
    };

    this.socket.emit('chat_message', message);
  }

  onMessage(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler);
    return () => {
      this.messageHandlers.delete(handler);
    };
  }

  onConnection(handler: ConnectionHandler): () => void {
    this.connectionHandlers.add(handler);
    // Immediately notify of current state
    if (this.socket?.connected) {
      handler(true);
    }
    return () => {
      this.connectionHandlers.delete(handler);
    };
  }

  onError(handler: ErrorHandler): () => void {
    this.errorHandlers.add(handler);
    return () => {
      this.errorHandlers.delete(handler);
    };
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  private notifyMessageHandlers(message: WebSocketMessage): void {
    this.messageHandlers.forEach((handler) => {
      try {
        handler(message);
      } catch (error) {
        console.error('Error in message handler:', error);
      }
    });
  }

  private notifyConnectionHandlers(connected: boolean): void {
    this.connectionHandlers.forEach((handler) => {
      try {
        handler(connected);
      } catch (error) {
        console.error('Error in connection handler:', error);
      }
    });
  }

  private notifyErrorHandlers(error: Error): void {
    this.errorHandlers.forEach((handler) => {
      try {
        handler(error);
      } catch (error) {
        console.error('Error in error handler:', error);
      }
    });
  }
}

// Singleton instance
export const wsService = new WebSocketService();
