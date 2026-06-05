
from __future__ import annotations

import flet as ft

from db import initialize_database
from repository import FridgeRepository

repo = FridgeRepository()

def main(page: ft.Page) -> None:
    page.title = "FridgeMate - 식재료 관리"
    page.window_width = 1200
    page.window_height = 820
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    message = ft.Text("")

    search_field = ft.TextField(label="식재료 검색", width=280)
    image_view = ft.Image(
        src="images/milk.png",
        width=180,
        height=120,
        fit=ft.ImageFit.CONTAIN,
    )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("식재료")),
            ft.DataColumn(ft.Text("보관 위치")),
            ft.DataColumn(ft.Text("수량")),
            ft.DataColumn(ft.Text("소비기한")),
            ft.DataColumn(ft.Text("구매처")),
            ft.DataColumn(ft.Text("상태")),
        ],
        rows=[],
    )

    integrated_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("식재료")),
            ft.DataColumn(ft.Text("카테고리")),
            ft.DataColumn(ft.Text("태그")),
            ft.DataColumn(ft.Text("알레르기")),
            ft.DataColumn(ft.Text("위치")),
            ft.DataColumn(ft.Text("구매처")),
            ft.DataColumn(ft.Text("소비 합계")),
        ],
        rows=[],
    )

    def show_message(text: str, error: bool = False) -> None:
        message.value = text
        message.color = ft.Colors.RED if error else ft.Colors.BLACK
        page.update()

    def load_items(keyword: str = "") -> None:
        rows = repo.find_items(keyword)
        table.rows.clear()
        for row in rows:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(row["ingredient_name"]),
                            on_tap=lambda e, path=row["image_path"]: select_image(path),
                        ),
                        ft.DataCell(ft.Text(row["location_name"])),
                        ft.DataCell(ft.Text(f'{row["quantity"]:g}{row["unit"]}')),
                        ft.DataCell(ft.Text(str(row["expiry_date"]))),
                        ft.DataCell(ft.Text(row["store_name"])),
                        ft.DataCell(ft.Text(row["status"])),
                    ]
                )
            )
        page.update()

    def select_image(path: str) -> None:
        image_view.src = path
        page.update()

    def load_integrated(_: ft.ControlEvent | None = None) -> None:
        rows = repo.integrated_view()
        integrated_table.rows.clear()
        for row in rows:
            integrated_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["ingredient_name"])),
                        ft.DataCell(ft.Text(row["category_name"] or "")),
                        ft.DataCell(ft.Text(row["tag_name"] or "")),
                        ft.DataCell(ft.Text(row["allergen_name"] or "")),
                        ft.DataCell(ft.Text(row["location_name"])),
                        ft.DataCell(ft.Text(row["store_name"] or "미등록")),
                        ft.DataCell(ft.Text(f'{row["consumed_total"]:g}')),
                    ]
                )
            )
        show_message("10개 이상의 테이블을 LEFT JOIN하여 통합 조회했습니다.")

    ingredient_options = [
        ft.dropdown.Option(str(i), f"{name} ({unit})")
        for i, name, unit in repo.list_ingredients()
    ]
    location_options = [
        ft.dropdown.Option(str(i), name) for i, name in repo.list_locations()
    ]
    store_options = [
        ft.dropdown.Option(str(i), name) for i, name in repo.list_stores()
    ]

    item_ingredient = ft.Dropdown(label="식재료", options=ingredient_options, width=220)
    item_location = ft.Dropdown(label="보관 위치", options=location_options, width=220)
    item_quantity = ft.TextField(label="수량", width=150)
    item_unit = ft.TextField(label="단위", width=150)
    item_expiry = ft.TextField(label="소비기한 YYYY-MM-DD", width=220)
    item_memo = ft.TextField(label="메모", width=250)

    purchase_item = ft.TextField(label="fridge_items.item_id", width=180)
    purchase_store = ft.Dropdown(label="구매처", options=store_options, width=220)
    purchase_date = ft.TextField(label="구매일 YYYY-MM-DD", width=220)
    purchase_price = ft.TextField(label="가격", width=150)

    consume_item = ft.TextField(label="fridge_items.item_id", width=180)
    consume_quantity = ft.TextField(label="사용 수량", width=150)
    consume_date = ft.TextField(label="소비일 YYYY-MM-DD", width=220)
    consume_memo = ft.TextField(label="메모", width=220)

    def add_item(_: ft.ControlEvent) -> None:
        try:
            repo.add_item(
                ingredient_id=int(item_ingredient.value),
                location_id=int(item_location.value),
                quantity=float(item_quantity.value),
                unit=item_unit.value.strip(),
                expiry_date=item_expiry.value.strip(),
                memo=item_memo.value.strip(),
            )
            show_message("식재료를 등록했습니다.")
            load_items()
        except Exception as exc:
            show_message(f"등록 실패: {exc}", True)

    def add_purchase(_: ft.ControlEvent) -> None:
        try:
            repo.add_purchase(
                item_id=int(purchase_item.value),
                store_id=int(purchase_store.value),
                purchase_date=purchase_date.value.strip(),
                price=int(purchase_price.value),
            )
            show_message("구매 기록을 저장했습니다.")
            load_items()
        except Exception as exc:
            show_message(f"구매 기록 저장 실패: {exc}", True)

    def add_consumption(_: ft.ControlEvent) -> None:
        try:
            repo.add_consumption(
                item_id=int(consume_item.value),
                quantity=float(consume_quantity.value),
                consumption_date=consume_date.value.strip(),
                memo=consume_memo.value.strip(),
            )
            show_message("소비 기록을 저장하고 현재 수량을 차감했습니다.")
            load_items()
        except Exception as exc:
            show_message(f"소비 기록 저장 실패: {exc}", True)

    def search(_: ft.ControlEvent) -> None:
        load_items(search_field.value.strip())

    page.add(
        ft.Text("FridgeMate - 식재료 관리", size=28, weight=ft.FontWeight.BOLD),
        message,
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="목록 조회",
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    search_field,
                                    ft.ElevatedButton("검색", on_click=search),
                                    ft.ElevatedButton("전체 보기", on_click=lambda e: load_items()),
                                    image_view,
                                ]
                            ),
                            ft.Row([table], scroll=ft.ScrollMode.AUTO),
                            ft.Text("식재료명을 클릭하면 DB에 저장된 image_path의 이미지를 출력합니다."),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
                ft.Tab(
                    text="식재료 등록",
                    content=ft.Column(
                        [
                            item_ingredient,
                            item_quantity,
                            item_unit,
                            item_location,
                            item_expiry,
                            item_memo,
                            ft.ElevatedButton("등록", on_click=add_item),
                        ]
                    ),
                ),
                ft.Tab(
                    text="구매 기록",
                    content=ft.Column(
                        [
                            purchase_item,
                            purchase_store,
                            purchase_date,
                            purchase_price,
                            ft.ElevatedButton("저장", on_click=add_purchase),
                        ]
                    ),
                ),
                ft.Tab(
                    text="소비 기록",
                    content=ft.Column(
                        [
                            consume_item,
                            consume_quantity,
                            consume_date,
                            consume_memo,
                            ft.ElevatedButton("저장", on_click=add_consumption),
                        ]
                    ),
                ),
                ft.Tab(
                    text="통합 조회",
                    content=ft.Column(
                        [
                            ft.ElevatedButton("10개 테이블 LEFT JOIN 실행", on_click=load_integrated),
                            ft.Row([integrated_table], scroll=ft.ScrollMode.AUTO),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
            ],
            expand=1,
        ),
    )

    load_items()

if __name__ == "__main__":
    initialize_database()
    ft.app(target=main, assets_dir="assets")
