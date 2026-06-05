
from __future__ import annotations

from datetime import date
from typing import Any

from db import connect, next_id, rows_as_dicts

class FridgeRepository:
    def find_items(self, keyword: str = "") -> list[dict[str, Any]]:
        sql = """
        SELECT
            fi.item_id,
            i.name AS ingredient_name,
            sl.location_name,
            fi.quantity,
            fi.unit,
            fi.expiry_date,
            COALESCE(s.store_name, '미등록') AS store_name,
            fi.status,
            i.image_path
        FROM fridge_items fi
        LEFT JOIN ingredients i ON fi.ingredient_id = i.ingredient_id
        LEFT JOIN storage_locations sl ON fi.location_id = sl.location_id
        LEFT JOIN purchase_records pr ON fi.item_id = pr.item_id
        LEFT JOIN stores s ON pr.store_id = s.store_id
        WHERE i.name ILIKE ?
        ORDER BY fi.expiry_date, fi.item_id
        """
        with connect() as con:
            return rows_as_dicts(con.execute(sql, [f"%{keyword}%"]))

    def integrated_view(self) -> list[dict[str, Any]]:
        # 10개 테이블 LEFT JOIN
        sql = """
        SELECT
            fi.item_id,
            u.name AS user_name,
            i.name AS ingredient_name,
            sl.location_name,
            fi.quantity,
            fi.unit,
            fi.expiry_date,
            s.store_name,
            pr.purchase_date,
            pr.price,
            c.category_name,
            t.tag_name,
            a.allergen_name,
            COALESCE(SUM(icn.consumed_quantity), 0) AS consumed_total,
            i.image_path
        FROM fridge_items fi
        LEFT JOIN users u ON fi.user_id = u.user_id
        LEFT JOIN ingredients i ON fi.ingredient_id = i.ingredient_id
        LEFT JOIN storage_locations sl ON fi.location_id = sl.location_id
        LEFT JOIN purchase_records pr ON fi.item_id = pr.item_id
        LEFT JOIN stores s ON pr.store_id = s.store_id
        LEFT JOIN ingredient_categories ic ON i.ingredient_id = ic.ingredient_id
        LEFT JOIN categories c ON ic.category_id = c.category_id
        LEFT JOIN ingredient_tags it ON i.ingredient_id = it.ingredient_id
        LEFT JOIN tags t ON it.tag_id = t.tag_id
        LEFT JOIN ingredient_allergens ia ON i.ingredient_id = ia.ingredient_id
        LEFT JOIN allergens a ON ia.allergen_id = a.allergen_id
        LEFT JOIN item_consumptions icn ON fi.item_id = icn.item_id
        GROUP BY ALL
        ORDER BY fi.expiry_date, fi.item_id
        """
        with connect() as con:
            return rows_as_dicts(con.execute(sql))

    def list_ingredients(self) -> list[tuple[int, str, str]]:
        with connect() as con:
            return con.execute(
                "SELECT ingredient_id, name, default_unit FROM ingredients ORDER BY name"
            ).fetchall()

    def list_locations(self) -> list[tuple[int, str]]:
        with connect() as con:
            return con.execute(
                "SELECT location_id, location_name FROM storage_locations ORDER BY location_id"
            ).fetchall()

    def list_stores(self) -> list[tuple[int, str]]:
        with connect() as con:
            return con.execute(
                "SELECT store_id, store_name FROM stores ORDER BY store_id"
            ).fetchall()

    def add_item(
        self,
        ingredient_id: int,
        location_id: int,
        quantity: float,
        unit: str,
        expiry_date: str,
        memo: str = "",
    ) -> int:
        with connect() as con:
            item_id = next_id(con, "fridge_items", "item_id")
            con.execute(
                """
                INSERT INTO fridge_items
                (item_id, user_id, ingredient_id, location_id, quantity, unit,
                 expiry_date, status, memo)
                VALUES (?, 1, ?, ?, ?, ?, CAST(? AS DATE), '보관', ?)
                """,
                [item_id, ingredient_id, location_id, quantity, unit, expiry_date, memo],
            )
            return item_id

    def add_purchase(
        self,
        item_id: int,
        store_id: int,
        purchase_date: str,
        price: int,
    ) -> int:
        with connect() as con:
            purchase_id = next_id(con, "purchase_records", "purchase_id")
            con.execute(
                """
                INSERT INTO purchase_records
                VALUES (?, ?, ?, CAST(? AS DATE), ?)
                """,
                [purchase_id, item_id, store_id, purchase_date, price],
            )
            return purchase_id

    def add_consumption(
        self,
        item_id: int,
        quantity: float,
        consumption_date: str,
        memo: str = "",
    ) -> int:
        with connect() as con:
            current = con.execute(
                "SELECT quantity FROM fridge_items WHERE item_id = ?", [item_id]
            ).fetchone()
            if current is None:
                raise ValueError("존재하지 않는 식재료입니다.")
            if quantity <= 0 or quantity > current[0]:
                raise ValueError("사용 수량이 현재 수량보다 많거나 올바르지 않습니다.")

            consumption_id = next_id(con, "item_consumptions", "consumption_id")
            con.execute(
                """
                INSERT INTO item_consumptions
                VALUES (?, ?, ?, CAST(? AS DATE), ?)
                """,
                [consumption_id, item_id, quantity, consumption_date, memo],
            )
            con.execute(
                "UPDATE fridge_items SET quantity = quantity - ? WHERE item_id = ?",
                [quantity, item_id],
            )
            return consumption_id
