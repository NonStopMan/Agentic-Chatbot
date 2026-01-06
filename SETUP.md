# Setup Guide - AI Chatbox

This guide will walk you through setting up the AI Chatbox application for development.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm/yarn ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Docker** and Docker Compose (optional, for containerized setup) ([Download](https://www.docker.com/get-started))
- **PostgreSQL** 15+ (if not using Docker)
- **Redis** 7+ (if not using Docker)

## 🚀 Quick Start (Recommended)

### Option 1: Docker Compose (Easiest)

1. **Clone the repository**
```bash
git clone https://github.com/NonStopMan/Agentic-Chatbot.git
cd Agentic-Chatbot
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your AI provider API keys
```

3. **Start all services**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/NonStopMan/Agentic-Chatbot.git
cd Agentic-Chatbot
```

#### Step 2: Set Up the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env if needed (default values should work for local development)
nano .env  # or use your preferred editor

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:5173

#### Step 3: Set Up the Backend (Coming Soon)

The backend implementation is in progress. For now, the frontend will show connection errors, which is expected.

```bash
cd ../backend

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

# Edit .env and add your configuration
nano .env

# Run database migrations (when backend is implemented)
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload
```

The backend will be available at http://localhost:8000

#### Step 4: Set Up Database (Manual Installation)

If not using Docker, you need to set up PostgreSQL and Redis:

**PostgreSQL:**
```bash
# On macOS with Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb chatbot

# Create user
psql postgres
CREATE USER chatbot_user WITH PASSWORD 'chatbot_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot TO chatbot_user;
\q
```

**Redis:**
```bash
# On macOS with Homebrew
brew install redis
brew services start redis

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

## 🔑 API Keys Setup

You'll need API keys from AI providers to use the chatbot:

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Anthropic (Claude)
1. Go to https://console.anthropic.com/
2. Create an API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### Google (Gemini)
1. Go to https://makersuite.google.com/app/apikey
2. Create an API key
3. Add to `.env`: `GOOGLE_API_KEY=...`

## 📁 Project Structure Overview

```
agentic-chatbot/
├── frontend/           # React + TypeScript application
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API services
│   │   ├── stores/       # State management
│   │   └── types/        # TypeScript types
│   └── package.json
│
├── backend/            # FastAPI + Python application
│   ├── app/
│   │   ├── api/          # REST endpoints
│   │   ├── websocket/    # Socket handlers
│   │   └── services/     # Business logic
│   └── requirements.txt
│
├── docker/             # Docker configuration
├── shared/             # Shared types
└── docker-compose.yml
```

## 🛠️ Development Workflow

### Running the Frontend

```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run linter
npm run type-check   # Check TypeScript types
```

### Running the Backend (When Implemented)

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload  # Start with hot reload
pytest                          # Run tests
```

### Database Migrations (When Implemented)

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔧 Troubleshooting

### Frontend Issues

**Port 5173 already in use**
```bash
# Kill the process using the port
lsof -ti:5173 | xargs kill -9
# Or change the port in vite.config.ts
```

**Dependencies not installing**
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**WebSocket connection failing**
- Ensure backend is running
- Check `.env` file has correct backend URL
- Verify firewall isn't blocking connections

### Backend Issues (When Implemented)

**Database connection error**
```bash
# Check PostgreSQL is running
pg_isready

# Check connection string in .env
# Make sure DATABASE_URL is correct
```

**Redis connection error**
```bash
# Check Redis is running
redis-cli ping

# Should return PONG
```

**Module import errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker Issues

**Port already in use**
```bash
# Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

**Build fails**
```bash
# Clean Docker cache
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose up --build
```

## 🧪 Testing

### Frontend Tests (To be added)
```bash
cd frontend
npm test              # Run tests
npm test -- --watch   # Watch mode
npm test -- --coverage # With coverage
```

### Backend Tests (To be added)
```bash
cd backend
pytest                    # Run all tests
pytest tests/test_api.py  # Run specific test file
pytest -v                 # Verbose output
pytest --cov              # With coverage
```

## 📦 Building for Production

### Frontend
```bash
cd frontend
npm run build
# Output will be in frontend/dist/
```

### Backend
```bash
cd backend
# Backend will use Dockerfile in production
docker build -f ../docker/backend.Dockerfile -t chatbot-backend .
```

### Full Stack with Docker
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 🔒 Security Considerations

For production deployment:

1. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management (AWS Secrets Manager, etc.)
   - Rotate API keys regularly

2. **Database**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **API**
   - Implement rate limiting
   - Add authentication/authorization
   - Use HTTPS only

4. **Dependencies**
   - Regular security updates
   - Use `npm audit` and `pip-audit`

## 📝 Next Steps

1. ✅ Frontend is ready for development
2. ⏳ Backend implementation in progress
3. ⏳ RAG features coming in Phase 3
4. ⏳ Tool calling in Phase 4
5. ⏳ Multi-agent workflows in Phase 5

## 🆘 Getting Help

- **Issues**: https://github.com/NonStopMan/Agentic-Chatbot/issues
- **Discussions**: https://github.com/NonStopMan/Agentic-Chatbot/discussions
- **Documentation**: See README.md and individual component docs

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Socket.io Documentation](https://socket.io/docs/v4/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)
