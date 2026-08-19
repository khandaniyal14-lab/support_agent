from app.tools import (
    get_customer,
    get_order,
    get_payment_status,
    get_ticket,
    search_knowledge_base,
)


def main() -> None:

    print("\nCUSTOMER")
    print(
        get_customer.invoke(
            {
                "customer_id": 1
            }
        )
    )

    print("\nORDER")
    print(
        get_order.invoke(
            {
                "order_id": 1001
            }
        )
    )

    print("\nPAYMENT")
    print(
        get_payment_status.invoke(
            {
                "order_id": 1001
            }
        )
    )

    print("\nTICKET")
    print(
        get_ticket.invoke(
            {
                "ticket_id": 1
            }
        )
    )

    print("\nKNOWLEDGE BASE")
    results = search_knowledge_base.invoke(
        {
            "query": (
                "What is the refund period?"
            )
        }
    )

    for result in results:
        print(
            f"\nSource: {result['source']}"
        )
        print(
            result["content"]
        )


if __name__ == "__main__":
    main()