# FridgeMate

요리를 좋아하는 자취생을 위한 냉장고 식재료 관리 프로그램입니다.  
Python, Flet, DuckDB를 사용합니다.

## 과제 제한요소 충족

- 18개 테이블 생성 및 예제 데이터 삽입
- Entity 5개 이상, Relationship/기록 테이블 3개 이상
- 3개 이상 테이블 JOIN: 실제 통합 조회는 10개 이상 테이블 LEFT JOIN
- Flet GUI에서 DuckDB 접근
- 식재료 이미지 경로를 `ingredients.image_path`에 저장
- Flet의 `Image` Control로 이미지 출력
- PK, FK, 복합키, CHECK, UNIQUE, NOT NULL, 정규화, Repository 패턴 활용
- GitHub Public Repository 제출 가능

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

## GitHub Public Repository 제출 방법

1. GitHub에서 새 Repository를 생성합니다.
2. Repository 이름 예시: `fridgemate-db-project`
3. Visibility를 **Public**으로 설정합니다.
4. 이 폴더에서 다음 명령을 실행합니다.

```bash
git init
git add .
git commit -m "Initial FridgeMate project"
git branch -M main
git remote add origin https://github.com/본인아이디/fridgemate-db-project.git
git push -u origin main
```

5. 최종보고서에 Public Repository 주소를 텍스트로 첨부합니다.

## 주의

- `assets/images`의 파일명과 DB의 `ingredients.image_path` 값이 일치해야 합니다.
- 보고서에는 SQL 실행 결과, Flet 실행 화면, 이미지 출력 화면, GitHub Public 화면을 직접 캡처해 넣으세요.
