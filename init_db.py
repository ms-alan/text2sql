"""
创建 Chinook 示例数据库
Chinook 是一个模拟音乐商店的示例数据库
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "chinook.db"

# 删除已存在的空数据库
if DB_PATH.exists():
    DB_PATH.unlink()

# 创建数据库连接
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 创建表并插入测试数据
print("正在创建 Chinook 数据库...")

# Artists 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "Artists" (
    "ArtistId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT
)
''')

# Albums 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "Albums" (
    "AlbumId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Title" TEXT NOT NULL,
    "ArtistId" INTEGER NOT NULL,
    FOREIGN KEY ("ArtistId") REFERENCES "Artists"("ArtistId")
)
''')

# songs 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "songs" (
    "TrackId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT NOT NULL,
    "AlbumId" INTEGER,
    "MediaTypeId" INTEGER NOT NULL,
    "GenreId" INTEGER,
    "Composer" TEXT,
    "Milliseconds" INTEGER NOT NULL,
    "Bytes" INTEGER,
    "UnitPrice" NUMERIC(10,2) NOT NULL,
    FOREIGN KEY ("AlbumId") REFERENCES "Albums"("AlbumId"),
    FOREIGN KEY ("MediaTypeId") REFERENCES "MediaType"("MediaTypeId"),
    FOREIGN KEY ("GenreId") REFERENCES "Genres"("GenreId")
)
''')

# MediaType 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "MediaType" (
    "MediaTypeId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT
)
''')

# Genres 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "Genres" (
    "GenreId" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT
)
''')

# 插入测试数据
print("插入测试数据...")

# 艺术家
artists = [
    (1, 'AC/DC'),
    (2, 'Accept'),
    (3, 'Aerosmith'),
    (4, 'Alanis Morissette'),
    (5, 'Alice In Chains'),
]
cursor.executemany('INSERT INTO Artists VALUES (?, ?)', artists)

# 专辑
albums = [
    (1, 'For Those About To Rock We Salute You', 1),
    (2, 'Balls to the Wall', 2),
    (3, 'Restless and Wild', 2),
    (4, 'Let There Be Rock', 1),
    (5, 'Jagged Little Pill', 4),
]
cursor.executemany('INSERT INTO Albums VALUES (?, ?, ?)', albums)

# 媒体类型
media_types = [
    (1, 'MPEG audio file'),
    (2, 'Protected AAC audio file'),
    (3, 'Protected MPEG-4 video file'),
]
cursor.executemany('INSERT INTO MediaType VALUES (?, ?)', media_types)

# 流派
genres = [
    (1, 'Rock'),
    (2, 'Jazz'),
    (3, 'Metal'),
    (4, 'Alternative & Punk'),
    (5, 'Rock And Roll'),
]
cursor.executemany('INSERT INTO Genres VALUES (?, ?)', genres)

# 歌曲
songs = [
    (1, 'For Those About To Rock (We Salute You)', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 343719, 11170334, 0.99),
    (2, 'Balls to the Wall', 2, 2, 1, None, 342562, 6318800, 0.99),
    (3, 'Fast As a Shark', 3, 2, 1, 'F. Baltes, S. Kaufman, G. Hoffmann', 230619, 3990994, 0.99),
    (4, 'Restless and Wild', 3, 2, 1, 'F. Baltes, R.A. Smith-Diesel, S. Kaufman, G. Hoffmann', 252051, 4331779, 0.99),
    (5, 'Princess of the Dawn', 3, 2, 1, 'Deaffy & R.A. Smith-Diesel', 375418, 6290521, 0.99),
    (6, 'Put The Finger On You', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 205662, 6711082, 0.99),
    (7, 'Let\'s Get It Up', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 233926, 7636567, 0.99),
    (8, 'Inject The Venom', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 210834, 6852860, 0.99),
    (9, 'Snowballed', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 232198, 7559072, 0.99),
    (10, 'Evil Walks', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 203389, 6599424, 0.99),
]
cursor.executemany('INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', songs)

# 提交并关闭
conn.commit()
conn.close()

print(f"✅ 数据库创建成功：{DB_PATH}")
print(f"📊 表数量：5 (Artists, Albums, songs, MediaType, Genres)")
print(f"🎵 艺术家数量：{len(artists)}")
print(f"💿 专辑数量：{len(albums)}")
print(f"🎶 歌曲数量：{len(songs)}")
