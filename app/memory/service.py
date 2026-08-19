from sqlalchemy.orm import Session

from app.memory.repository import ConversationRepository


class ConversationMemoryService:

    def __init__(self, db: Session) -> None:
        self.repository = ConversationRepository(db)

    def add_user_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:

        self.repository.get_or_create(
            conversation_id
        )

        self.repository.add_message(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:

        self.repository.get_or_create(
            conversation_id
        )

        self.repository.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
        )

    def get_history(
        self,
        conversation_id: str,
    ) -> list[dict[str, str]]:

        messages = self.repository.get_messages(
            conversation_id
        )

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]