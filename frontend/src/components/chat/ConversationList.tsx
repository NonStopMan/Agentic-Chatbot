import React from 'react';
import { useChatStore } from '@/stores/chatStore';
import { Button } from '@/components/ui/Button';
import { ScrollArea } from '@/components/ui/ScrollArea';
import { MessageSquarePlus, Trash2, MessageSquare } from 'lucide-react';
import { format, isToday, isYesterday, isThisWeek } from 'date-fns';
import { cn } from '@/lib/utils';

interface ConversationListProps {
  onNewChat: () => void;
}

export const ConversationList: React.FC<ConversationListProps> = ({ onNewChat }) => {
  const { conversations, currentConversation, setCurrentConversation, deleteConversation } =
    useChatStore();

  const formatDate = (date: Date) => {
    if (isToday(date)) return 'Today';
    if (isYesterday(date)) return 'Yesterday';
    if (isThisWeek(date)) return format(date, 'EEEE');
    return format(date, 'MMM d, yyyy');
  };

  const groupedConversations = conversations.reduce((groups, conv) => {
    const dateKey = formatDate(new Date(conv.updatedAt));
    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }
    groups[dateKey].push(conv);
    return groups;
  }, {} as Record<string, typeof conversations>);

  const handleDelete = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      deleteConversation(id);
    }
  };

  return (
    <div className="flex flex-col h-full bg-secondary/30">
      {/* Header */}
      <div className="p-4 border-b">
        <Button onClick={onNewChat} className="w-full" size="sm">
          <MessageSquarePlus className="h-4 w-4 mr-2" />
          New Chat
        </Button>
      </div>

      {/* Conversations List */}
      <ScrollArea className="flex-1 p-2">
        {conversations.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center p-4">
            <MessageSquare className="h-12 w-12 text-muted-foreground mb-2" />
            <p className="text-sm text-muted-foreground">No conversations yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(groupedConversations).map(([dateKey, convs]) => (
              <div key={dateKey}>
                <h3 className="text-xs font-semibold text-muted-foreground uppercase px-3 mb-2">
                  {dateKey}
                </h3>
                <div className="space-y-1">
                  {convs.map((conv) => (
                    <div
                      key={conv.id}
                      className={cn(
                        'group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-colors',
                        'hover:bg-secondary',
                        currentConversation?.id === conv.id && 'bg-secondary'
                      )}
                      onClick={() => setCurrentConversation(conv)}
                    >
                      <MessageSquare className="h-4 w-4 shrink-0 text-muted-foreground" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{conv.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {conv.messages.length} messages
                        </p>
                      </div>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="opacity-0 group-hover:opacity-100 shrink-0 h-8 w-8"
                        onClick={(e) => handleDelete(e, conv.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};
