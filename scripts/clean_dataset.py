from pathlib import Path

import pandas as pd

from app.core.config import settings

REQUIRED_COLUMNS = [
    "Ticket ID",
    "Customer Name",
    "Customer Email",
    "Customer Age",
    "Customer Gender",
    "Product Purchased",
    "Date of Purchase",
    "Ticket Type",
    "Ticket Subject",
    "Ticket Description",
    "Ticket Status",
    "Resolution",
    "Ticket Priority",
    "Ticket Channel",
    "First Response Time",
    "Time to Resolution",
    "Customer Satisfaction Rating",
]


def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    return " ".join(value.split())


def main() -> None:
    input_path = Path(settings.raw_data_path)
    output_path = Path(settings.processed_data_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    print("\nLoading dataset...")
    print(f"Original rows: {len(df)}")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset schema does not match expected schema.\n"
            f"Missing columns: {missing_columns}"
        )

    df = df.copy()

    # Remove exact duplicates.
    df = df.drop_duplicates()

    # Clean column names.
    df.columns = [
        column.strip()
        for column in df.columns
    ]

    # Clean text fields.
    text_columns = [
        "Customer Name",
        "Customer Email",
        "Customer Gender",
        "Product Purchased",
        "Ticket Type",
        "Ticket Subject",
        "Ticket Description",
        "Ticket Status",
        "Resolution",
        "Ticket Priority",
        "Ticket Channel",
        "First Response Time",
        "Time to Resolution",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # Normalize email.
    df["Customer Email"] = (
        df["Customer Email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Normalize categories.
    category_columns = [
        "Ticket Type",
        "Ticket Status",
        "Ticket Priority",
        "Ticket Channel",
        "Product Purchased",
    ]

    for column in category_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Convert date.
    df["Date of Purchase"] = pd.to_datetime(
        df["Date of Purchase"],
        errors="coerce",
    )

    # Convert numeric fields.
    df["Customer Age"] = pd.to_numeric(
        df["Customer Age"],
        errors="coerce",
    )

    df["Customer Satisfaction Rating"] = pd.to_numeric(
        df["Customer Satisfaction Rating"],
        errors="coerce",
    )

    # Remove records without the minimum required information.
    required_data_columns = [
        "Ticket ID",
        "Customer Name",
        "Customer Email",
        "Ticket Description",
    ]

    df = df.dropna(
        subset=required_data_columns
    )

    # Remove duplicate ticket IDs.
    df = df.drop_duplicates(
        subset=["Ticket ID"],
        keep="first",
    )

    # Validate age.
    df.loc[
        (df["Customer Age"] < 0)
        | (df["Customer Age"] > 120),
        "Customer Age",
    ] = pd.NA

    # Validate satisfaction rating.
    df.loc[
        ~df["Customer Satisfaction Rating"].isin(
            [1, 2, 3, 4, 5]
        ),
        "Customer Satisfaction Rating",
    ] = pd.NA

    # Restore readable date format.
    df["Date of Purchase"] = (
        df["Date of Purchase"]
        .dt.strftime("%Y-%m-%d")
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print("\nCleaning complete.")
    print(f"Final rows: {len(df)}")
    print(f"Output: {output_path}")

    print("\nFinal missing values:")

    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            percentage = (count / len(df)) * 100

            print(
                f"  {column}: "
                f"{count} ({percentage:.2f}%)"
            )


if __name__ == "__main__":
    main()