# FridgeMate

요리를 좋아하는 자취생을 위한 냉장고 식재료 관리 프로그램입니다.  
Python, Flet, DuckDB를 사용합니다.


## 주요 기능

1. 식재료 목록 조회 및 검색
2. 식재료 등록
3. 구매 기록 등록
4. 소비 기록 등록 및 현재 수량 차감
5. 통합 LEFT JOIN 조회
6. DB에 저장된 이미지 경로를 이용한 이미지 출력

## 실행

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

최초 실행 시 `data/fridgemate.duckdb`가 자동 생성됩니다.

## 테이블

Entity 성격의 주요 테이블:
- users
- ingredients
- categories
- storage_locations
- stores

Relationship/기록 성격의 주요 테이블:
- fridge_items
- ingredient_categories
- purchase_records
- item_consumptions
- ingredient_tags
- ingredient_allergens
- recipe_ingredients
- meal_plans
- waste_records
- favorite_ingredients



