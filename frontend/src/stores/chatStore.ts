import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { Conversation, Message, ChatConfig, AIProvider } from '@/types';
import { DEFAULT_CONFIG } from '@/lib/constants';

interface ChatState {
  // Current conversation
  currentConversation: Conversation | null;
  conversations: Conversation[];
  
  // Configuration
  config: ChatConfig;
  
  // UI State
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setCurrentConversation: (conversation: Conversation | null) => void;
  addConversation: (conversation: Conversation) => void;
  updateConversation: (id: string, updates: Partial<Conversation>) => void;
  deleteConversation: (id: string) => void;
  
  addMessage: (message: Message) => void;
  updateMessage: (messageId: string, updates: Partial<Message>) => void;
  
  setConfig: (config: Partial<ChatConfig>) => void;
  setProvider: (provider: AIProvider) => void;
  
  setIsConnected: (connected: boolean) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  
  clearCurrentConversation: () => void;
  reset: () => void;
}

const createNewConversation = (provider: AIProvider): Conversation => ({
  id: crypto.randomUUID(),
  title: 'New Chat',
  messages: [],
  provider,
  createdAt: new Date(),
  updatedAt: new Date(),
});

export const useChatStore = create<ChatState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        currentConversation: null,
        conversations: [],
        config: DEFAULT_CONFIG,
        isConnected: false,
        isLoading: false,
        error: null,

        // Actions
        setCurrentConversation: (conversation) =>
          set({ currentConversation: conversation }),

        addConversation: (conversation) =>
          set((state) => ({
            conversations: [conversation, ...state.conversations],
            currentConversation: conversation,
          })),

        updateConversation: (id, updates) =>
          set((state) => {
            const conversations = state.conversations.map((conv) =>
              conv.id === id ? { ...conv, ...updates, updatedAt: new Date() } : conv
            );
            
            const currentConversation =
              state.currentConversation?.id === id
                ? { ...state.currentConversation, ...updates, updatedAt: new Date() }
                : state.currentConversation;

            return { conversations, currentConversation };
          }),

        deleteConversation: (id) =>
          set((state) => ({
            conversations: state.conversations.filter((conv) => conv.id !== id),
            currentConversation:
              state.currentConversation?.id === id ? null : state.currentConversation,
          })),

        addMessage: (message) =>
          set((state) => {
            const current = state.currentConversation;
            if (!current) {
              // Create new conversation if none exists
              const newConversation = createNewConversation(state.config.provider);
              newConversation.messages = [message];
              newConversation.title = message.content.slice(0, 50) + (message.content.length > 50 ? '...' : '');
              
              return {
                currentConversation: newConversation,
                conversations: [newConversation, ...state.conversations],
              };
            }

            const updatedConversation = {
              ...current,
              messages: [...current.messages, message],
              updatedAt: new Date(),
            };

            return {
              currentConversation: updatedConversation,
              conversations: state.conversations.map((conv) =>
                conv.id === current.id ? updatedConversation : conv
              ),
            };
          }),

        updateMessage: (messageId, updates) =>
          set((state) => {
            const current = state.currentConversation;
            if (!current) return state;

            const updatedMessages = current.messages.map((msg) =>
              msg.id === messageId ? { ...msg, ...updates } : msg
            );

            const updatedConversation = {
              ...current,
              messages: updatedMessages,
              updatedAt: new Date(),
            };

            return {
              currentConversation: updatedConversation,
              conversations: state.conversations.map((conv) =>
                conv.id === current.id ? updatedConversation : conv
              ),
            };
          }),

        setConfig: (config) =>
          set((state) => ({
            config: { ...state.config, ...config },
          })),

        setProvider: (provider) =>
          set((state) => ({
            config: { ...state.config, provider },
          })),

        setIsConnected: (connected) => set({ isConnected: connected }),
        setIsLoading: (loading) => set({ isLoading: loading }),
        setError: (error) => set({ error }),

        clearCurrentConversation: () =>
          set({
            currentConversation: null,
          }),

        reset: () =>
          set({
            currentConversation: null,
            conversations: [],
            config: DEFAULT_CONFIG,
            isConnected: false,
            isLoading: false,
            error: null,
          }),
      }),
      {
        name: 'chat-storage',
        partialize: (state) => ({
          conversations: state.conversations,
          config: state.config,
        }),
      }
    )
  )
);
