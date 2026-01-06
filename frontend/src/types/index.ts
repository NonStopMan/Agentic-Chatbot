export type AIProvider = 'openai' | 'anthropic' | 'google' | 'local';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  error?: string;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  provider: AIProvider;
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatConfig {
  provider: AIProvider;
  model?: string;
  temperature?: number;
  maxTokens?: number;
  streamingEnabled: boolean;
}

export interface ProviderConfig {
  id: AIProvider;
  name: string;
  description: string;
  icon: string;
  models: string[];
  enabled: boolean;
}

export interface WebSocketMessage {
  type: 'message' | 'stream' | 'error' | 'system' | 'end';
  data: {
    conversationId?: string;
    messageId?: string;
    content?: string;
    role?: 'user' | 'assistant';
    provider?: AIProvider;
    error?: string;
  };
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}

// Future phase types (placeholders)
export interface RAGDocument {
  id: string;
  name: string;
  content: string;
  embedding?: number[];
  metadata?: Record<string, unknown>;
  uploadedAt: Date;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  enabled: boolean;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  status: 'idle' | 'working' | 'error';
}
