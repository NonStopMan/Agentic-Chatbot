# AI Chatbox - Agentic Multi-Provider Chatbot

A full-stack AI chatbot application with multi-provider support, RAG capabilities, tool calling, and multi-agent workflows.

## 🎯 Features

- **Multi-Provider Support**: Choose between OpenAI, Anthropic Claude, Google Gemini, and local models
- **Real-time Communication**: WebSocket-based streaming responses
- **RAG Integration**: Upload documents for context-aware conversations
- **Tool Calling**: AI can execute functions and tools
- **Multi-Agent Workflows**: Complex agent orchestration with LangGraph
- **Conversation History**: Persistent chat sessions across devices

## 🏗️ Architecture

This is a monorepo containing:

- **frontend/**: React + TypeScript + Vite + TailwindCSS + shadcn/ui
- **backend/**: FastAPI + Python + LangChain + LangGraph
- **shared/**: Shared TypeScript types and constants
- **docker/**: Docker configuration files

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Docker and Docker Compose (optional)
- PostgreSQL 15+
- Redis 7+

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/NonStopMan/Agentic-Chatbot.git
cd Agentic-Chatbot
```

2. **Frontend Setup**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

3. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

4. **Using Docker Compose** (Recommended)
```bash
docker-compose up --build
```

Access the application at `http://localhost:5173`

## 📁 Project Structure

```
agentic-chatbot/
├── frontend/                 # React + TypeScript
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── features/         # Feature-based modules
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API/Socket services
│   │   ├── stores/           # State management
│   │   └── types/            # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI + Python
│   ├── app/
│   │   ├── api/              # REST endpoints
│   │   ├── websocket/        # Socket.io handlers
│   │   ├── services/         # Business logic
│   │   ├── models/           # Database models
│   │   └── schemas/          # Pydantic schemas
│   └── requirements.txt
│
├── shared/                   # Shared types
├── docker/                   # Docker configs
└── docker-compose.yml
```

## 🛠️ Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS + shadcn/ui for styling
- Socket.io-client for WebSocket
- Zustand for state management
- React Query for server state

### Backend
- FastAPI for async Python web framework
- Socket.io for WebSocket communication
- LangChain for AI orchestration
- LangGraph for multi-agent workflows
- PostgreSQL for data persistence
- Redis for caching and sessions
- SQLAlchemy for ORM

## 📋 Development Phases

- [x] **Phase 1**: Foundation - Basic chat with streaming ✅
- [x] **Phase 2**: Multi-provider support and persistence ✅
- [ ] **Phase 3**: RAG implementation
- [ ] **Phase 4**: Tool calling
- [ ] **Phase 5**: Multi-agent workflows
- [ ] **Phase 6**: Production deployment

## 🔑 Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## 📝 License

MIT

## 👤 Author

Mo - Senior Software Engineer

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
