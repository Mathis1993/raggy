from .base import *

OPENAI_API_KEY = env.str("OPENAI_API_KEY")

# LLMs
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 100

# VECTOR STORE (Milvus)
MILVUS_HOST = os.environ.get("MILVUS_HOST", "localhost")
MILVUS_PORT = os.environ.get("MILVUS_PORT", 19350)


# TASK MANAGEMENT (Celery)
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

# CELERY_DEFAULT_QUEUE = os.getenv("CELERY_DEFAULT_QUEUE", "standard")
# CELERY_HIGH_PRIORITY_QUEUE = os.getenv("CELERY_HIGH_PRIORITY_QUEUE", "high_priority")

# CELERYD_TIME_LIMIT = os.getenv("CELERYD_TIME_LIMIT", 3600)
# CELERYD_SOFT_TIME_LIMIT = os.getenv("CELERYD_SOFT_TIME_LIMIT", 3600)
# CELERY_TASK_TRACK_STARTED = True

# EMAIL
FROM_EMAIL = os.environ.get("FROM_EMAIL", "noreply@localhost.de")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True