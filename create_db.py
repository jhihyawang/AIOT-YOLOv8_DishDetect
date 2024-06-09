import sqlite3

# 連接到SQLite資料庫（如果不存在則創建）
conn = sqlite3.connect('nutrition.db')
cursor = conn.cursor()

# 創建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    name TEXT,
    price INTEGER,
    calories INTEGER,
    protein REAL,
    fat REAL,
    carbohydrates REAL,
    fiber REAL
)
''')

# 插入資料
items = [
    ("Bean sprouts", 30, 30, 3.2, 0.2, 6.0, 2.0),
    ("Wood ear fungus", 25, 20, 1.5, 0.1, 5.0, 5.0),
    ("Loofah", 35, 14, 0.6, 0.1, 3.4, 0.5),
    ("Water spinach", 30, 19, 2.6, 0.2, 3.1, 2.1),
    ("Cabbage", 35, 25, 1.3, 0.1, 5.8, 2.5),
    ("Broccoli", 30, 34, 2.8, 0.4, 7.0, 3.3),
    ("Sweet potato leaves", 30, 22, 2.5, 0.3, 3.8, 2.5),
    ("Long beans", 30, 47, 2.8, 0.2, 10.6, 2.9),
    ("Mixed vegetables", 20, 28, 1.8, 0.1, 6.5, 2.0),
    ("Sausage", 40, 300, 10.0, 25.0, 5.0, 0.0),
    ("Sweet and sour chicken nuggets", 45, 250, 15.0, 15.0, 12.0, 1.0),
    ("Braised pork belly", 45, 450, 9.0, 40.0, 5.0, 0.0),
    ("Fish", 70, 206, 22.0, 12.0, 0.0, 0.0),
    ("Garlic pork belly", 45, 400, 8.0, 35.0, 5.0, 0.0),
    ("Fried chicken leg", 50, 260, 20.0, 18.0, 5.0, 0.0),
    ("Fried chicken fillet", 55, 290, 25.0, 15.0, 10.0, 1.0),
    ("Lion's head meatballs", 50, 300, 12.0, 25.0, 8.0, 2.0),
    ("White rice", 10, 130, 2.5, 0.2, 28.0, 0.4),
    ("Black rice", 15, 150, 4.0, 1.0, 31.0, 3.5),
    ("Braised egg", 15, 150, 13.0, 10.0, 1.0, 0.0),
    ("Fried egg", 15, 200, 14.0, 15.0, 1.0, 0.0)
]

# 批量插入資料
cursor.executemany('''
INSERT INTO items (name, price, calories, protein, fat, carbohydrates, fiber)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', items)

# 提交變更並關閉連接
conn.commit()
conn.close()

print("資料庫建立並填充完成。")
