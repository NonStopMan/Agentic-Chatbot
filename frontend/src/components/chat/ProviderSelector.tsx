import React from 'react';
import { AIProvider } from '@/types';
import { PROVIDERS } from '@/lib/constants';
import { Card, CardContent } from '@/components/ui/Card';
import { cn } from '@/lib/utils';
import { Check } from 'lucide-react';

interface ProviderSelectorProps {
  selectedProvider: AIProvider;
  onSelectProvider: (provider: AIProvider) => void;
  disabled?: boolean;
}

export const ProviderSelector: React.FC<ProviderSelectorProps> = ({
  selectedProvider,
  onSelectProvider,
  disabled = false,
}) => {
  const enabledProviders = PROVIDERS.filter((p) => p.enabled);

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">AI Provider</label>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {enabledProviders.map((provider) => (
          <Card
            key={provider.id}
            className={cn(
              'cursor-pointer transition-all hover:shadow-md',
              selectedProvider === provider.id && 'ring-2 ring-primary',
              disabled && 'opacity-50 cursor-not-allowed'
            )}
            onClick={() => !disabled && onSelectProvider(provider.id)}
          >
            <CardContent className="p-4">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{provider.icon}</span>
                  <div>
                    <h3 className="font-semibold text-sm">{provider.name}</h3>
                    <p className="text-xs text-muted-foreground line-clamp-2">
                      {provider.description}
                    </p>
                  </div>
                </div>
                {selectedProvider === provider.id && (
                  <Check className="h-5 w-5 text-primary shrink-0" />
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
