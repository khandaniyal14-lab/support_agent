from collections import defaultdict


class ConversationMemory:

    def __init__(self) -> None:

        self._conversations: dict[
            str,
            list[dict[str, str]],
        ] = defaultdict(list)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:

        self._conversations[
            conversation_id
        ].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict[str, str]]:

        return self._conversations.get(
            conversation_id,
            [],
        )

    def clear(
        self,
        conversation_id: str,
    ) -> None:

        self._conversations.pop(
            conversation_id,
            None,
        )