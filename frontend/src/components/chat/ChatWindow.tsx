import React, { useEffect, useRef } from 'react';
import { ScrollArea } from '@/components/ui/ScrollArea';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useChatStore } from '@/stores/chatStore';
import { AlertCircle, Loader2 } from 'lucide-react';
import { MESSAGES } from '@/lib/constants';

interface ChatWindowProps {
  onSendMessage: (message: string) => void;
  isStreaming?: boolean;
  onStopStreaming?: () => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  onSendMessage,
  isStreaming = false,
  onStopStreaming,
}) => {
  const { currentConversation, isConnected, isLoading, error } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation?.messages]);

  const messages = currentConversation?.messages || [];
  const hasMessages = messages.length > 0;

  return (
    <div className="flex flex-col h-full">
      {/* Connection Status Banner */}
      {!isConnected && (
        <div className="bg-yellow-500/10 border-b border-yellow-500/20 px-4 py-2 flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-yellow-600 dark:text-yellow-400" />
          <span className="text-sm text-yellow-600 dark:text-yellow-400">
            {MESSAGES.DISCONNECTED} - Attempting to reconnect...
          </span>
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div className="bg-destructive/10 border-b border-destructive/20 px-4 py-2 flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-destructive" />
          <span className="text-sm text-destructive">{error}</span>
        </div>
      )}

      {/* Messages Area */}
      <ScrollArea ref={scrollAreaRef} className="flex-1 p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {!hasMessages ? (
            <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center">
              <div className="text-6xl mb-4">💬</div>
              <h2 className="text-2xl font-semibold mb-2">Start a Conversation</h2>
              <p className="text-muted-foreground max-w-md">
                {MESSAGES.WELCOME}
              </p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Thinking...</span>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <ChatInput
        onSendMessage={onSendMessage}
        disabled={!isConnected || isLoading}
        isStreaming={isStreaming}
        onStopStreaming={onStopStreaming}
        placeholder={
          !isConnected
            ? 'Connecting to server...'
            : isLoading
            ? 'Waiting for response...'
            : 'Type your message...'
        }
      />
    </div>
  );
};
