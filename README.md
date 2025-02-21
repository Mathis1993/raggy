# Raggy - Advanced RAG System with Django and Milvus

Raggy is a sophisticated Retrieval-Augmented Generation (RAG) system built with Django and Milvus vector database. It provides a scalable and efficient solution for document processing, embedding generation, and intelligent information retrieval.

## Features

- Document processing and embedding generation
- Vector similarity search using Milvus
- RESTful API using Django REST Framework
- Asynchronous task processing with Celery
- Caching with Redis
- Modern frontend interface
- Docker-based deployment

## Project Structure

```
raggy/
├── backend/           # Django backend application
│   ├── manage.py     # Django management script
│   ├── backend/      # Django project configuration
│   ├── conversations/ # Conversations app
│   ├── knowledge_base/ # Knowledge base app
│   └── ...           # Other Django apps
├── frontend/         # Frontend application
├── .docker/          # Docker volume mounts and configurations
├── concepts/         # Project documentation and concepts
├── docker-compose.yml # Docker services configuration
├── pyproject.toml    # Python dependencies and project configuration
└── milvus.py        # Milvus integration utilities
```

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- uv (Python package installer)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd raggy
   ```

2. **Install uv**
   ```bash
   # Using curl (Linux/macOS)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or using Homebrew (macOS)
   brew install uv
   ```

3. **Set up the Python environment**
   ```bash
   # Create virtual environment and install dependencies
   uv venv
   uv sync

   # Optionally activate the virtual environment
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows

   # To add new dependencies (during development)
   uv add <package-name>
   
   # To run commands without activating venv
   uv run python your_script.py
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with necessary configurations:
   ```bash
   # Database
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
   
   # Redis
   REDIS_URL=redis://localhost:6379/0
   
   # Milvus
   MILVUS_HOST=localhost
   MILVUS_PORT=19530
   
   # Python Path
   PYTHONPATH=${PYTHONPATH}:${PWD}/backend
   
   # Add other required environment variables
   ```

5. **Start Docker services**
   ```bash
   docker-compose up -d
   ```

   This will start the following services:
   - PostgreSQL (port 5432)
   - Redis (port 6379)
   - Milvus standalone (port 19530)
   - Milvus Attu UI (port 3000)
   - MinIO (ports 9000, 9001)
   - Etcd

6. **Initialize the database**
   ```bash
   # Make sure you're in the backend directory
   cd backend
   
   # Run migrations and create superuser
   PYTHONPATH=${PWD} uv run python manage.py migrate
   PYTHONPATH=${PWD} uv run python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   # Make sure you're in the backend directory
   cd backend
   
   # Start the Django development server
   PYTHONPATH=${PWD} uv run python manage.py runserver
   ```

## Development

- The backend is built with Django 5.1 and uses Django REST Framework for API development
- Milvus is used as the vector database for efficient similarity search
- Celery handles asynchronous tasks with Redis as the message broker
- PostgreSQL serves as the primary database

## Services

### Milvus Setup
- Milvus runs in standalone mode for development
- Attu UI is available at http://localhost:3000 for vector database management
- MinIO provides object storage for Milvus
- Etcd handles metadata storage

### Database
- PostgreSQL stores relational data and metadata
- Default credentials (for development only):
  - Database: postgres
  - User: postgres
  - Password: postgres

### Caching
- Redis handles caching and Celery task queue
- Available on port 6379

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Write tests if applicable
4. Submit a pull request

## Security Notes

- Default credentials in docker-compose.yml are for development only
- Configure proper authentication for Milvus in production
- Use environment variables for sensitive information

## Resources

### Milvus Documentation
- [Milvus Documentation](https://milvus.io/docs/index.md)
- [Index Types](https://milvus.io/docs/index.md) - Choose between in-memory and disk index

## ToDo

- [ ] Configure Milvus user authentication
- [ ] Add production deployment guide
- [ ] Implement automated testing pipeline






RUN COMMANDS
python manage.py runserver
❯ celery --app  core worker --loglevel=info --concurrency=1 --pool=solo --queues=celery