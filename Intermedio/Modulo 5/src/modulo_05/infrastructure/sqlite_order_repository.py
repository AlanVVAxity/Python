import sqlite3
from decimal import Decimal

from modulo_05.domain.order import Order


class SQLiteOrderRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._create_table()

    def _create_table(self) -> None:
        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                total TEXT NOT NULL
            )
            """)
        self._connection.commit()

    def save(self, order: Order) -> None:
        self._connection.execute(
            """
            INSERT INTO orders (id, customer_name, total)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                customer_name = excluded.customer_name,
                total = excluded.total
            """,
            (order.id, order.customer_name, str(order.total)),
        )
        self._connection.commit()

    def get_by_id(self, order_id: str) -> Order | None:
        row = self._connection.execute(
            """
            SELECT id, customer_name, total
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        ).fetchone()

        if row is None:
            return None

        return Order(
            id=row[0],
            customer_name=row[1],
            total=Decimal(row[2]),
        )

    def list_all(self) -> list[Order]:
        rows = self._connection.execute("""
            SELECT id, customer_name, total
            FROM orders
            ORDER BY id
            """).fetchall()

        return [
            Order(
                id=row[0],
                customer_name=row[1],
                total=Decimal(row[2]),
            )
            for row in rows
        ]
