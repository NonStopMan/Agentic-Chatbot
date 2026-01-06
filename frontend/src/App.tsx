import React, { useState } from 'react';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { ConversationList } from '@/components/chat/ConversationList';
import { ProviderSelector } from '@/components/chat/ProviderSelector';
import { Button } from '@/components/ui/Button';
import { useChatStore } from '@/stores/chatStore';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Menu, X, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  
  const { config, setProvider, clearCurrentConversation } = useChatStore();
  const { sendMessage, stopStreaming, isStreaming } = useWebSocket();

  const handleNewChat = () => {
    clearCurrentConversation();
    if (window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  };

  const handleProviderChange = (provider: typeof config.provider) => {
    setProvider(provider);
    setShowSettings(false);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside
        className={cn(
          'w-80 border-r flex-shrink-0 transition-transform duration-300',
          'lg:translate-x-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
          'absolute lg:relative h-full z-30 bg-background'
        )}
      >
        <ConversationList onNewChat={handleNewChat} />
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="border-b p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden"
            >
              {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
            
            <div>
              <h1 className="text-xl font-bold">AI Chatbox</h1>
              <p className="text-xs text-muted-foreground">
                Multi-Provider Chatbot
              </p>
            </div>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSettings(!showSettings)}
          >
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </header>

        {/* Settings Panel */}
        {showSettings && (
          <div className="border-b p-4 bg-secondary/20">
            <ProviderSelector
              selectedProvider={config.provider}
              onSelectProvider={handleProviderChange}
            />
          </div>
        )}

        {/* Chat Window */}
        <ChatWindow
          onSendMessage={sendMessage}
          isStreaming={isStreaming}
          onStopStreaming={stopStreaming}
        />
      </div>

      {/* Overlay for mobile sidebar */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}

export default App;
