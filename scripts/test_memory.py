from app.agents.support_agent import (
    SupportAgent,
)


def main() -> None:

    agent = SupportAgent()

    conversation_id = "memory-test"

    first_response = agent.run(
        request=(
            "My order 1001 was cancelled "
            "after payment."
        ),
        conversation_id=conversation_id,
        ticket_id=1,
    )

    print("\nFIRST RESPONSE")
    print("-" * 70)
    print(first_response)

    second_response = agent.run(
        request=(
            "What should I do next?"
        ),
        conversation_id=conversation_id,
        ticket_id=1,
    )

    print("\nSECOND RESPONSE")
    print("-" * 70)
    print(second_response)


if __name__ == "__main__":
    main()