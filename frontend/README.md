# Frontend - AI Chatbox

React + TypeScript frontend for the AI Chatbox application.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend server running (see `/backend` folder)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Basic UI components (Button, Input, Card, etc.)
│   └── chat/           # Chat-specific components
├── features/           # Feature modules (for future phases)
├── hooks/              # Custom React hooks
├── services/           # External services (WebSocket, API)
├── stores/             # Zustand state management
├── types/              # TypeScript type definitions
└── lib/                # Utility functions and constants
```

## 🎨 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS
- **shadcn/ui** - UI component patterns
- **Zustand** - State management
- **Socket.io-client** - WebSocket communication
- **React Query** - Server state management (planned)
- **React Markdown** - Markdown rendering

## 🔧 Available Scripts

```bash
# Development
npm run dev              # Start dev server with hot reload

# Building
npm run build            # Build for production
npm run preview          # Preview production build

# Code Quality
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript type checking
```

## 📁 Component Overview

### Core Components

- **App.tsx** - Main application layout and routing
- **ChatWindow** - Main chat interface with message display
- **ChatInput** - Message input with auto-resize and keyboard shortcuts
- **ChatMessage** - Individual message rendering with markdown support
- **ProviderSelector** - AI provider selection UI
- **ConversationList** - Sidebar with conversation history

### Custom Hooks

- **useWebSocket** - WebSocket connection and message handling
- More hooks will be added in future phases

### State Management

- **chatStore** - Main chat state (conversations, messages, config)
  - Persisted to localStorage
  - Includes actions for CRUD operations

## 🔌 WebSocket Communication

The frontend connects to the backend via Socket.io:

```typescript
// Message format
{
  type: 'message' | 'stream' | 'error' | 'system' | 'end',
  data: {
    conversationId?: string,
    messageId?: string,
    content?: string,
    role?: 'user' | 'assistant',
    provider?: AIProvider,
    error?: string
  }
}
```

### Events

- **connect** - Connection established
- **disconnect** - Connection lost
- **message** - Complete message received
- **stream** - Streaming chunk received
- **error** - Error occurred

## 🎯 Features

### Phase 1 (Current)
- [x] Real-time chat with WebSocket
- [x] AI provider selection (OpenAI, Anthropic, Google)
- [x] Streaming responses
- [x] Message history
- [x] Conversation persistence
- [x] Responsive design
- [x] Dark/light mode support
- [x] Markdown rendering

### Future Phases
- [ ] RAG document upload and search
- [ ] Tool calling visualization
- [ ] Multi-agent workflow display
- [ ] Advanced settings (temperature, max tokens, etc.)
- [ ] Conversation search
- [ ] Export conversations
- [ ] User authentication

## 🎨 Styling

The application uses TailwindCSS with a custom design system:

- CSS variables for theming
- Dark mode support via `class` strategy
- Custom scrollbar styling
- Markdown content styling
- Responsive design (mobile-first)

## 🔐 Environment Variables

```env
VITE_API_URL=http://localhost:8000    # Backend API URL
VITE_WS_URL=ws://localhost:8000       # WebSocket URL
```

## 🐛 Common Issues

### WebSocket Connection Fails
- Ensure backend server is running
- Check `VITE_WS_URL` in `.env` file
- Verify CORS settings in backend

### Styling Not Applied
```bash
npm install
npm run dev  # Restart dev server
```

### TypeScript Errors
```bash
npm run type-check  # Check for type errors
```

## 📝 Code Style

- Use functional components with hooks
- TypeScript strict mode enabled
- ESLint + Prettier for code formatting
- Component props should have TypeScript interfaces
- Use Zustand for global state, React state for local state

## 🤝 Contributing

When adding new features:

1. Create types in `/types/index.ts`
2. Add components to appropriate folders
3. Update state management if needed
4. Add necessary hooks in `/hooks`
5. Update this README with new features

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [Socket.io Client API](https://socket.io/docs/v4/client-api/)
