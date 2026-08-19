from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


class ConversationRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create(
        self,
        conversation_id: str,
    ) -> Conversation:

        conversation = self.db.scalar(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        if conversation is None:

            conversation = Conversation(
                id=conversation_id,
            )

            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)

        return conversation

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[Message]:

        result = self.db.scalars(
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(Message.created_at)
        )

        return list(result)