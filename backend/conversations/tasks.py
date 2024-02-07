from celery import shared_task

from conversations.handler import ConversationHandler


@shared_task
def task_handle_user_message(conversation_id: int, user_message: str):
    handler = ConversationHandler(conversation_id=conversation_id)
    response_message = handler.handle_message(user_message=user_message)
    return response_message.text
