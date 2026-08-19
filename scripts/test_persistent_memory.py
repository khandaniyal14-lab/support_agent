from app.db.session import SessionLocal
from app.memory.service import (
    ConversationMemoryService,
)


def main() -> None:

    db = SessionLocal()

    try:

        memory = (
            ConversationMemoryService(db)
        )

        conversation_id = (
            "phase5-memory-test"
        )

        memory.add_user_message(
            conversation_id=conversation_id,
            content="My order was cancelled.",
        )

        memory.add_assistant_message(
            conversation_id=conversation_id,
            content="I will investigate your order.",
        )

        history = memory.get_history(
            conversation_id
        )

        print("\nConversation History")
        print("=" * 70)

        for message in history:
            print(
                f"{message['role']}: "
                f"{message['content']}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()