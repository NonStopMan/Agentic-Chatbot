import { ProviderConfig } from '@/types';

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export const PROVIDERS: ProviderConfig[] = [
  {
    id: 'openai',
    name: 'OpenAI',
    description: 'GPT-4 and GPT-3.5 models from OpenAI',
    icon: '🤖',
    models: ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
    enabled: true,
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    description: 'Claude 3 models from Anthropic',
    icon: '🧠',
    models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
    enabled: true,
  },
  {
    id: 'google',
    name: 'Google',
    description: 'Gemini models from Google',
    icon: '✨',
    models: ['gemini-pro', 'gemini-pro-vision'],
    enabled: true,
  },
  {
    id: 'local',
    name: 'Local Models',
    description: 'Run models locally with Ollama',
    icon: '💻',
    models: ['llama2', 'mistral', 'codellama'],
    enabled: false, // Disabled by default
  },
];

export const DEFAULT_CONFIG = {
  provider: 'openai' as const,
  model: 'gpt-4',
  temperature: 0.7,
  maxTokens: 2048,
  streamingEnabled: true,
};

export const MESSAGES = {
  WELCOME: 'Hello! I\'m your AI assistant. Choose a provider and start chatting!',
  CONNECTING: 'Connecting to server...',
  CONNECTED: 'Connected successfully',
  DISCONNECTED: 'Disconnected from server',
  ERROR: 'An error occurred. Please try again.',
};
