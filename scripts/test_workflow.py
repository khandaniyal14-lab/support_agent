from app.agents.support_agent import (
    SupportAgent,
)


def main() -> None:

    agent = SupportAgent()

    response = agent.run(
        request=(
            "My payment was deducted but "
            "my order was cancelled. "
            "What will happen to my money?"
        ),
        conversation_id="test-1",
        ticket_id=1,
    )

    print("\n")
    print("=" * 70)
    print("AGENT RESPONSE")
    print("=" * 70)
    print(response)


if __name__ == "__main__":
    main()