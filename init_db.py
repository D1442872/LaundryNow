import sqlite3
import os

DATABASE = 'laundry.db'

def init_db():
    print("正在初始化 SQLite 資料庫...")
    
    # 建立或連接資料庫
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 建立 laundry 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS laundry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_number TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('空閒', '使用中', '故障')),
            remaining_time INTEGER NOT NULL DEFAULT 0 CHECK(remaining_time >= 0),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 檢查是否已有資料，若無則插入測試用預設資料
    cursor.execute('SELECT COUNT(*) FROM laundry')
    if cursor.fetchone()[0] == 0:
        print("資料表為空，正在插入預設測試資料...")
        sample_data = [
            ('A01', '福星宿舍 1 樓洗衣間', '空閒', 0, '2026-05-14 10:00:00'),
            ('A02', '福星宿舍 1 樓洗衣間', '使用中', 25, '2026-05-14 10:05:00'),
            ('B01', '福星宿舍 2 樓洗衣間', '故障', 0, '2026-05-14 09:50:00')
        ]
        cursor.executemany('''
            INSERT INTO laundry (machine_number, location, status, remaining_time, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_data)
        print("預設測試資料插入成功！")
    else:
        print("資料庫已存在資料，略過預設資料插入。")
        
    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

if __name__ == '__main__':
    init_db()
