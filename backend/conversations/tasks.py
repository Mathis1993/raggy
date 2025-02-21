import logging
from celery import shared_task

from conversations.exceptions import ConversationError
from conversations.handler import ConversationHandler


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def task_handle_user_message(self, conversation_id: int, user_message: str):
    try:
        handler = ConversationHandler(conversation_id=conversation_id)
        response_message = handler.handle_message(
            user_message=user_message, add_to_conversation=False
        )
        return response_message.text
    except ConversationError as e:
        logger.error(f"Conversation error in task: {e}")
        self.retry(exc=e)
    except Exception as e:
        logger.error(f"Unexpected error in task: {e}")
        raise