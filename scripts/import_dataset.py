from app.core.config import settings
from app.db.session import SessionLocal
from app.services.dataset_service import import_dataset


def main() -> None:
    db = SessionLocal()

    try:
        result = import_dataset(
            db=db,
            dataset_path=settings.processed_data_path,
        )

        print("\n" + "=" * 60)
        print("DATASET IMPORT COMPLETE")
        print("=" * 60)

        print(
            f"Customers created : "
            f"{result['customers_created']}"
        )

        print(
            f"Products created  : "
            f"{result['products_created']}"
        )

        print(
            f"Tickets created   : "
            f"{result['tickets_created']}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()