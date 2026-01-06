# Backend - AI Chatbox

FastAPI + Python backend with multi-provider AI support, WebSocket streaming, and database persistence.

## 🎉 Phase 2 Complete!

The backend is now fully functional with:
- ✅ FastAPI server with async support
- ✅ WebSocket (Socket.io) for real-time chat
- ✅ Multi-provider AI integration (OpenAI, Anthropic, Google)
- ✅ PostgreSQL database with SQLAlchemy
- ✅ Redis for caching and sessions
- ✅ Streaming responses
- ✅ Conversation persistence
- ✅ RESTful API endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### Database Setup

```bash
# Make sure PostgreSQL is running
# Create database (if not exists)
createdb chatbot

# Run migrations (tables will be created automatically on startup)
# Or use Alembic:
alembic upgrade head
```

### Run the Server

```bash
# Development mode with hot reload
uvicorn app.main:app --reload

# Or use the script
python -m app.main

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/socket.io

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                      # REST API endpoints
│   │   ├── conversations.py      # Conversation CRUD
│   │   └── health.py             # Health check
│   │
│   ├── websocket/                # WebSocket handlers
│   │   └── handler.py            # Socket.io chat handler
│   │
│   ├── services/                 # Business logic
│   │   ├── ai/                   # AI provider integrations
│   │   │   ├── base.py           # Base provider class
│   │   │   ├── openai_provider.py
│   │   │   ├── anthropic_provider.py
│   │   │   ├── google_provider.py
│   │   │   └── manager.py        # Provider manager
│   │   ├── conversation_service.py
│   │   ├── rag/                  # RAG (Phase 3)
│   │   ├── agents/               # Agents (Phase 5)
│   │   └── tools/                # Tools (Phase 4)
│   │
│   ├── models/                   # Database models
│   │   └── conversation.py       # Conversation & Message models
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   └── conversation.py       # Request/Response schemas
│   │
│   ├── core/                     # Core configuration
│   │   ├── config.py             # Settings
│   │   ├── database.py           # Database connection
│   │   └── redis.py              # Redis connection
│   │
│   ├── utils/                    # Utility functions
│   └── main.py                   # FastAPI application
│
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   ├── env.py                    # Alembic environment
│   └── script.py.mako            # Migration template
│
├── tests/                        # Test files
│
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic configuration
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🔌 API Endpoints

### REST API

#### Health Check
```
GET /health
```

#### Conversations
```
POST   /api/v1/conversations           # Create conversation
GET    /api/v1/conversations           # List conversations
GET    /api/v1/conversations/{id}      # Get conversation
PATCH  /api/v1/conversations/{id}      # Update conversation
DELETE /api/v1/conversations/{id}      # Delete conversation
GET    /api/v1/conversations/{id}/messages  # Get messages
```

### WebSocket Events

#### Client → Server
```javascript
// Connect
socket.connect()

// Send message
socket.emit('chat_message', {
  type: 'message',
  data: {
    content: 'Hello!',
    provider: 'openai',  // or 'anthropic', 'google'
    conversationId: 'uuid',  // optional
    model: 'gpt-4',  // optional
    temperature: 0.7,  // optional
    maxTokens: 2048  // optional
  }
})
```

#### Server → Client
```javascript
// System messages
socket.on('message', (data) => {
  // data.type: 'system', 'stream', 'error', 'end'
})

// Stream chunks
{
  type: 'stream',
  data: {
    conversationId: 'uuid',
    messageId: 'uuid',
    content: 'chunk of text',
    role: 'assistant'
  }
}

// End of stream
{
  type: 'end',
  data: {
    conversationId: 'uuid',
    messageId: 'uuid'
  }
}

// Error
{
  type: 'error',
  data: {
    error: 'Error message',
    conversationId: 'uuid'  // optional
  }
}
```

## 🤖 AI Providers

### OpenAI
- **Models**: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- **API Key**: `OPENAI_API_KEY` in `.env`

### Anthropic (Claude)
- **Models**: claude-3-opus, claude-3-sonnet, claude-3-haiku
- **API Key**: `ANTHROPIC_API_KEY` in `.env`

### Google (Gemini)
- **Models**: gemini-pro, gemini-pro-vision
- **API Key**: `GOOGLE_API_KEY` in `.env`

## 🗄️ Database Schema

### Conversations Table
```sql
- id: UUID (PK)
- title: VARCHAR(200)
- provider: ENUM (openai, anthropic, google, local)
- model: VARCHAR(100)
- temperature: FLOAT
- max_tokens: INTEGER
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Messages Table
```sql
- id: UUID (PK)
- conversation_id: UUID (FK)
- role: ENUM (user, assistant, system)
- content: TEXT
- metadata: JSONB
- error: TEXT
- created_at: TIMESTAMP
```

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_api.py -v
```

## 🔧 Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## 📝 Environment Variables

See `.env.example` for all available options. Key variables:

```bash
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/chatbot
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Optional
DEBUG=True
PORT=8000
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4
```

## 🚨 Common Issues

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Verify connection string
psql $DATABASE_URL
```

### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping

# Should return PONG
```

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### WebSocket Not Connecting
- Check CORS settings in `config.py`
- Verify frontend is using correct WebSocket URL
- Check firewall rules

## 🔒 Security Notes

For production:
1. Use strong `SECRET_KEY`
2. Enable HTTPS only
3. Restrict CORS origins
4. Use environment-based secrets
5. Enable rate limiting
6. Regular dependency updates

## 📈 Performance Tips

- Use connection pooling (configured)
- Enable Redis caching
- Use async operations
- Monitor database query performance
- Consider read replicas for scaling

## 🔄 What's Next (Future Phases)

### Phase 3: RAG Implementation
- Vector database (Chroma/Pinecone)
- Document upload and processing
- Embedding generation
- Semantic search

### Phase 4: Tool Calling
- Tool registry and definitions
- Function execution engine
- Tool result handling
- UI integration

### Phase 5: Multi-Agent Workflows
- LangGraph integration
- Agent definitions
- Workflow orchestration
- State management

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with the React frontend:

1. **WebSocket**: Real-time streaming chat
2. **REST API**: Conversation management
3. **CORS**: Configured for local development
4. **Error Handling**: Consistent error responses

## 📊 Monitoring

Consider adding:
- Logging (already configured)
- APM tools (New Relic, DataDog)
- Error tracking (Sentry)
- Metrics (Prometheus)

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Socket.IO Documentation](https://socket.io/)
- [OpenAI API](https://platform.openai.com/docs)
- [Anthropic API](https://docs.anthropic.com/)
- [Google AI](https://ai.google.dev/)

---

**Phase 2 Complete! 🎉**

Your backend is production-ready and fully integrated with the frontend!
