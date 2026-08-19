from pathlib import Path

import pandas as pd

from app.core.config import settings


def main() -> None:
    path = Path(settings.raw_data_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_csv(path)

    print("\n" + "=" * 70)
    print("CUSTOMER SUPPORT DATASET EXPLORATION")
    print("=" * 70)

    print("\nDataset shape:")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    missing = df.isnull().sum()

    for column, count in missing.items():
        percentage = (count / len(df)) * 100
        print(
            f"  {column}: "
            f"{count} ({percentage:.2f}%)"
        )

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    categorical_columns = [
        "Ticket Type",
        "Ticket Status",
        "Ticket Priority",
        "Ticket Channel",
        "Product Purchased",
    ]

    for column in categorical_columns:
        if column not in df.columns:
            continue

        print("\n" + "-" * 70)
        print(f"{column}")
        print("-" * 70)

        print(
            df[column]
            .value_counts(dropna=False)
            .to_string()
        )

    if "Customer Satisfaction Rating" in df.columns:
        print("\n" + "-" * 70)
        print("Customer Satisfaction Rating")
        print("-" * 70)

        print(
            df["Customer Satisfaction Rating"]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

    print("\nText statistics:")

    text_columns = [
        "Ticket Subject",
        "Ticket Description",
        "Resolution",
    ]

    for column in text_columns:
        if column not in df.columns:
            continue

        lengths = (
            df[column]
            .fillna("")
            .astype(str)
            .str.len()
        )

        print(
            f"\n{column}:"
            f"\n  Average length : {lengths.mean():.2f}"
            f"\n  Minimum length: {lengths.min()}"
            f"\n  Maximum length: {lengths.max()}"
        )

    print("\n" + "=" * 70)
    print("EXPLORATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()