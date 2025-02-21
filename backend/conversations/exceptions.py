class ConversationError(Exception):
    """Base exception for conversation related errors"""

    pass


class ChatEngineError(ConversationError):
    """Raised when there's an error in the chat engine"""

    pass


class PersistenceError(ConversationError):
    """Raised when there's an error persisting conversation data"""

    pass
