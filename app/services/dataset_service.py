from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer, Product, Ticket


def import_dataset(
    db: Session,
    dataset_path: str,
) -> dict:
    path = Path(dataset_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_csv(path)

    customers_created = 0
    products_created = 0
    tickets_created = 0

    customer_cache: dict[str, Customer] = {}
    product_cache: dict[str, Product] = {}

    for _, row in df.iterrows():

        email = str(
            row["Customer Email"]
        ).strip().lower()

        customer = customer_cache.get(email)

        if customer is None:
            customer = db.scalar(
                select(Customer).where(
                    Customer.email == email
                )
            )

        if customer is None:
            customer = Customer(
                name=str(row["Customer Name"]).strip(),
                email=email,
                age=_safe_int(row["Customer Age"]),
                gender=_safe_string(
                    row["Customer Gender"]
                ),
            )

            db.add(customer)
            db.flush()

            customers_created += 1

        customer_cache[email] = customer

        product_name = _safe_string(
            row["Product Purchased"]
        )

        product = None

        if product_name:
            product = product_cache.get(
                product_name
            )

            if product is None:
                product = db.scalar(
                    select(Product).where(
                        Product.name == product_name
                    )
                )

            if product is None:
                product = Product(
                    name=product_name
                )

                db.add(product)
                db.flush()

                products_created += 1

            product_cache[product_name] = product

        external_ticket_id = str(
            row["Ticket ID"]
        ).strip()

        existing_ticket = db.scalar(
            select(Ticket).where(
                Ticket.external_ticket_id
                == external_ticket_id
            )
        )

        if existing_ticket:
            continue

        ticket = Ticket(
            external_ticket_id=external_ticket_id,
            customer_id=customer.id,
            product_id=(
                product.id
                if product
                else None
            ),
            purchase_date=_safe_date(
                row["Date of Purchase"]
            ),
            ticket_type=_safe_string(
                row["Ticket Type"]
            ),
            subject=_safe_string(
                row["Ticket Subject"]
            ),
            description=_safe_string(
                row["Ticket Description"]
            ) or "",
            status=_safe_string(
                row["Ticket Status"]
            ),
            resolution=_safe_string(
                row["Resolution"]
            ),
            priority=_safe_string(
                row["Ticket Priority"]
            ),
            channel=_safe_string(
                row["Ticket Channel"]
            ),
            first_response_time=_safe_string(
                row["First Response Time"]
            ),
            time_to_resolution=_safe_string(
                row["Time to Resolution"]
            ),
            satisfaction_rating=_safe_int(
                row["Customer Satisfaction Rating"]
            ),
        )

        db.add(ticket)

        tickets_created += 1

    db.commit()

    return {
        "customers_created": customers_created,
        "products_created": products_created,
        "tickets_created": tickets_created,
    }


def _safe_string(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    return value


def _safe_int(value):
    if pd.isna(value):
        return None

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _safe_date(value):
    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()
    except (TypeError, ValueError):
        return None