from app.agents.support_agent import SupportAgent


def main() -> None:

    agent = SupportAgent()

    conversation_id = "customer-1001"

    print("=" * 70)
    print("MESSAGE 1")
    print("=" * 70)

    response_1 = agent.run(
        request=(
            "My payment was deducted but "
            "my order was cancelled."
        ),
        conversation_id=conversation_id,
    )

    print(response_1)

    print()
    print("=" * 70)
    print("MESSAGE 2")
    print("=" * 70)

    response_2 = agent.run(
        request=(
            "What will happen to my money?"
        ),
        conversation_id=conversation_id,
    )

    print(response_2)


if __name__ == "__main__":
    main()