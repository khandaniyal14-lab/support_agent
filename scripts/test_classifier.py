import pandas as pd

from app.ai.classifier import TicketClassifier
from app.core.config import settings


def main() -> None:
    df = pd.read_csv(
        settings.processed_data_path
    )

    classifier = TicketClassifier()

    sample = df.head(10)

    for index, row in sample.iterrows():

        ticket = (
            f"Subject: {row['Ticket Subject']}\n\n"
            f"Description: {row['Ticket Description']}"
        )

        print("\n" + "=" * 70)
        print(f"TICKET {index + 1}")
        print("=" * 70)

        print(ticket)

        result = classifier.classify(
            ticket
        )

        print("\nCLASSIFICATION:")
        print(
            result.model_dump_json(
                indent=2
            )
        )


if __name__ == "__main__":
    main()