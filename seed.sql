
INSERT OR IGNORE INTO users VALUES
(1, '자취생', 'student@example.com');

INSERT OR IGNORE INTO ingredients VALUES
(1, '우유', 'ml', 'images/milk.png', '냉장 보관 유제품'),
(2, '계란', '개', 'images/egg.png', '단백질 식재료'),
(3, '딸기', 'g', 'images/strawberry.png', '과일'),
(4, '두부', '모', 'images/tofu.png', '찌개와 부침용');

INSERT OR IGNORE INTO categories VALUES
(1, '유제품'), (2, '단백질'), (3, '과일'), (4, '냉장식품');

INSERT OR IGNORE INTO storage_locations VALUES
(1, '냉장실 상단', '냉장'),
(2, '냉장실 하단', '냉장'),
(3, '야채칸', '냉장'),
(4, '냉동실', '냉동');

INSERT OR IGNORE INTO stores VALUES
(1, '이마트', '대형마트'),
(2, '동네마트', '소형마트'),
(3, '쿠팡프레시', '온라인');

INSERT OR IGNORE INTO fridge_items VALUES
(1, 1, 1, 1, 900, 'ml', DATE '2026-06-05', '보관', '아침 식사용'),
(2, 1, 2, 2, 10, '개', DATE '2026-06-10', '보관', '계란말이 예정'),
(3, 1, 3, 3, 300, 'g', DATE '2026-06-01', '임박', '디저트용'),
(4, 1, 4, 2, 2, '모', DATE '2026-06-03', '보관', '찌개용');

INSERT OR IGNORE INTO ingredient_categories VALUES
(1,1),(1,4),(2,2),(2,4),(3,3),(4,2),(4,4);

INSERT OR IGNORE INTO purchase_records VALUES
(1, 1, 1, DATE '2026-05-17', 2800),
(2, 2, 2, DATE '2026-05-16', 4500),
(3, 3, 3, DATE '2026-05-15', 5200),
(4, 4, 2, DATE '2026-05-18', 2200);

INSERT OR IGNORE INTO item_consumptions VALUES
(1, 1, 200, DATE '2026-05-20', '시리얼'),
(2, 2, 2, DATE '2026-05-19', '계란말이');

INSERT OR IGNORE INTO tags VALUES
(1,'아침식사'),(2,'간식'),(3,'한식');

INSERT OR IGNORE INTO ingredient_tags VALUES
(1,1),(2,3),(3,2),(4,3);

INSERT OR IGNORE INTO allergens VALUES
(1,'우유'),(2,'대두'),(3,'계란');

INSERT OR IGNORE INTO ingredient_allergens VALUES
(1,1),(2,3),(4,2);

INSERT OR IGNORE INTO recipes VALUES
(1,'계란말이','계란을 이용한 간단한 반찬'),
(2,'두부찌개','두부를 이용한 국물 요리');

INSERT OR IGNORE INTO recipe_ingredients VALUES
(1,2,3,'개'),(2,4,1,'모');

INSERT OR IGNORE INTO meal_plans VALUES
(1,1,1,DATE '2026-06-02','저녁');

INSERT OR IGNORE INTO waste_records VALUES
(1,3,DATE '2026-06-04',50,'상함');

INSERT OR IGNORE INTO favorite_ingredients VALUES
(1,2,CURRENT_TIMESTAMP);
