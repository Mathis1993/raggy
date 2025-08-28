# Raggy - Learning RAG System with LlamaIndex and Milvus

**Raggy** is a **learning-focused** Retrieval-Augmented Generation (RAG) system built to understand the fundamentals of modern AI applications. This side project was created to practice and explore:

- **RAG Architecture**: How retrieval-augmented generation works in practice
- **Vector Databases**: Using Milvus for efficient similarity search and storage
- **Embeddings**: Understanding how documents are chunked, embedded, and retrieved
- **Frontend Development**: Learning Svelte as a modern frontend framework
- **Source Attribution**: Implementing proper quote extraction and source linking

> **Note**: This is a **learning project**, not production-ready software. The focus is on understanding RAG concepts, embeddings, and vector search rather than building a polished application.

![raggy](https://github.com/user-attachments/assets/3a674ca8-96d7-4eb8-be12-2febe2f88887)

## 🎯 Project Goals

- **Educational**: Deep dive into RAG systems, vector databases, and embeddings
- **Hands-on Learning**: Practical experience with LlamaIndex, Milvus, and Svelte
- **Concept Understanding**: Learn how source attribution and quote extraction work
- **Modern Stack**: Explore contemporary AI development tools and practices

## ✨ Features

### Core RAG Functionality
- **Document Processing**: Upload and process various document types (PDF, Word, text, websites)
- **Intelligent Chunking**: Smart document splitting with configurable chunk sizes and overlap
- **Embedding Generation**: Create vector embeddings using sentence-transformers
- **Vector Search**: Efficient similarity search using Milvus vector database
- **Context Retrieval**: Retrieve relevant document chunks for question answering

### Conversation & Chat
- **Conversation Memory**: Maintain chat history and context across sessions
- **Source Attribution**: Show which documents were used to answer questions
- **Quote Extraction**: Display relevant quotes from source documents
- **Multi-turn Conversations**: Support for follow-up questions and clarifications

### User Experience
- **Modern UI**: Clean, responsive interface built with Svelte and Tailwind CSS
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Document Management**: Upload, view, and manage your knowledge base
- **Source Visualization**: See which documents contributed to each answer

## 🏗️ Project Structure

```
raggy/
├── backend/                    # Django backend application
│   ├── manage.py              # Django management script
│   ├── backend/               # Django project configuration
│   ├── conversations/         # Chat and conversation handling
│   │   ├── engine.py         # LlamaIndex chat engine
│   │   └── models.py         # Conversation and message models
│   ├── knowledge_base/        # Document processing and vector storage
│   │   ├── extractors/       # Document content extractors
│   │   ├── ingestion/        # Document ingestion pipeline
│   │   └── vector_store.py   # Milvus vector store integration
│   ├── users/                # User authentication and management
│   └── core/                 # Core utilities and Celery tasks
├── frontend/                  # Svelte frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── routes/           # SvelteKit routes and pages
│   │   ├── stores/           # State management
│   │   └── types/            # TypeScript type definitions
│   └── package.json          # Frontend dependencies
├── docker-compose.yml         # Docker services configuration
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## 🛠️ Technology Stack

### Backend
- **Django 5.1**: Web framework and API
- **Django REST Framework**: RESTful API development
- **LlamaIndex**: RAG framework for document processing and retrieval
- **Milvus**: Vector database for similarity search
- **Celery**: Asynchronous task processing
- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker

### Frontend
- **SvelteKit**: Modern frontend framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Flowbite**: UI component library
- **Vite**: Build tool and dev server

### Infrastructure
- **Docker**: Containerization
- **Milvus**: Vector database (standalone mode)
- **MinIO**: Object storage for Milvus
- **Etcd**: Metadata storage for Milvus

## 🚀 Setup Instructions

### Prerequisites

- **Docker and Docker Compose**
- **Python 3.12+**
- **Node.js 18+**
- **uv** (Python package installer)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd raggy
```

### 2. Install uv (Python Package Manager)

```bash
# Using curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew (macOS)
brew install uv
```

### 3. Configure Environment

Create a `.env` file in the root directory:

```bash
# Database
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres

# Redis
REDIS_URL=redis://localhost:6379/0

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# OpenAI (for embeddings and chat)
OPENAI_API_KEY=your_openai_api_key_here

# Python Path
PYTHONPATH=${PYTHONPATH}:${PWD}/backend
```

### 4. Setup Python Environment

```bash
# Create virtual environment and install dependencies
uv venv
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

### 5. Start Infrastructure Services

```bash
# Start all required services
docker-compose up -d

# Verify services are running
docker-compose ps
```

This starts:
- **PostgreSQL** (port 5432)
- **Redis** (port 6379)
- **Milvus** (port 19530)
- **Milvus Attu UI** (port 3000) - Vector database management
- **MinIO** (ports 9000, 9001) - Object storage
- **Etcd** - Metadata storage

### 6. Initialize Database

```bash
cd backend

# Run migrations
PYTHONPATH=${PWD} uv run python manage.py migrate

# Create superuser
PYTHONPATH=${PWD} uv run python manage.py createsuperuser
```

### 7. Start Backend Services

```bash
# Terminal 1: Start Django server
cd backend
PYTHONPATH=${PWD} uv run python manage.py runserver

# Terminal 2: Start Celery worker
cd backend
PYTHONPATH=${PWD} uv run celery --app core worker --loglevel=info --concurrency=1 --pool=solo --queues=celery
```

### 8. Start Frontend

```bash
# Terminal 3: Install dependencies and start dev server
cd frontend
npm install
npm run dev
```

## 🌐 Access Points

- **Frontend Application**: http://localhost:5173 (Svelte dev server)
- **Django Admin**: http://localhost:8000/admin
- **Django API**: http://localhost:8000/api
- **Milvus Attu UI**: http://localhost:3000 (Username: `root`, Password: `milvus`)

## 🔧 Development Workflow

### Adding New Dependencies

```bash
# Python dependencies
uv add <package-name>

# Frontend dependencies
cd frontend
npm install <package-name>
```

### Running Tests

```bash
# Backend tests
cd backend
PYTHONPATH=${PWD} uv run python manage.py test

# Frontend tests
cd frontend
npm run test
```

### Code Quality

```bash
# Frontend linting and formatting
cd frontend
npm run lint
npm run format
```

## 📚 Learning Resources

### RAG and Vector Databases
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Milvus Documentation](https://milvus.io/docs/)
- [Vector Database Concepts](https://milvus.io/docs/vector_database.md)

### Frontend Development
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: If you get port conflicts, check if services are already running:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

2. **Milvus Connection Issues**: Ensure Milvus is fully started:
   ```bash
   docker-compose logs standalone
   ```

3. **Python Path Issues**: Always use the correct PYTHONPATH:
   ```bash
   PYTHONPATH=${PWD} uv run python manage.py <command>
   ```

### Stopping Services

```bash
# Stop frontend and backend servers (Ctrl+C)
# Stop Docker services
docker-compose down
```
