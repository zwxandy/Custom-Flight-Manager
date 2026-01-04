"""
数据库工具模块
处理所有数据库相关的操作
"""

import sqlite3
import json

# 数据库文件路径
DB_FILE = 'flights.db'


def init_database():
    """
    初始化SQLite数据库，创建flights表（如果不存在），并添加flight_time列（如果不存在）
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_city TEXT NOT NULL,
            arrival_city TEXT NOT NULL,
            date TEXT NOT NULL,
            distance REAL NOT NULL,
            departure_coords TEXT NOT NULL,
            arrival_coords TEXT NOT NULL,
            flight_time INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 检查并添加flight_time列（如果表已存在但列不存在）
    cursor.execute("PRAGMA table_info(flights)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'flight_time' not in columns:
        cursor.execute('ALTER TABLE flights ADD COLUMN flight_time INTEGER')
    
    conn.commit()
    conn.close()


def save_flight_to_db(flight_record):
    """
    保存航班记录到数据库
    flight_record: 包含航班信息的字典
    返回: 插入的记录ID
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (departure_city, arrival_city, date, distance, departure_coords, arrival_coords, flight_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        flight_record['departure_city'],
        flight_record['arrival_city'],
        flight_record['date'],
        flight_record['distance'],
        json.dumps(flight_record['departure_coords']),  # 将tuple转为JSON字符串存储
        json.dumps(flight_record['arrival_coords']),
        flight_record.get('flight_time', None)  # 飞行时间（分钟），可选
    ))
    conn.commit()
    flight_id = cursor.lastrowid
    conn.close()
    return flight_id


def load_flights_from_db():
    """
    从数据库加载所有航班记录
    返回: 航班记录列表
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights ORDER BY date DESC, id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    flights = []
    for row in rows:
        flight_dict = {
            'id': row[0],
            'departure_city': row[1],
            'arrival_city': row[2],
            'date': row[3],
            'distance': row[4],
            'departure_coords': json.loads(row[5]),  # 从JSON字符串解析回tuple
            'arrival_coords': json.loads(row[6])
        }
        # 处理flight_time字段（可能在旧数据中不存在）
        if len(row) > 7:
            flight_time = row[7]
            # 确保flight_time是整数类型（SQLite可能返回字符串）
            try:
                flight_dict['flight_time'] = int(flight_time) if flight_time is not None else None
            except (ValueError, TypeError):
                flight_dict['flight_time'] = None
        else:
            flight_dict['flight_time'] = None
        flights.append(flight_dict)
    return flights


def clear_all_flights_from_db():
    """
    清空数据库中的所有航班记录
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flights')
    conn.commit()
    conn.close()


def delete_flight_from_db(flight_id):
    """
    从数据库删除指定ID的航班记录
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
    conn.commit()
    conn.close()


def update_flight_in_db(flight_id, flight_record):
    """
    更新数据库中的航班记录
    flight_id: 要更新的记录ID
    flight_record: 包含更新后航班信息的字典
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE flights 
        SET departure_city = ?, arrival_city = ?, date = ?, distance = ?, 
            departure_coords = ?, arrival_coords = ?, flight_time = ?
        WHERE id = ?
    ''', (
        flight_record['departure_city'],
        flight_record['arrival_city'],
        flight_record['date'],
        flight_record['distance'],
        json.dumps(flight_record['departure_coords']),
        json.dumps(flight_record['arrival_coords']),
        flight_record.get('flight_time', None),
        flight_id
    ))
    conn.commit()
    conn.close()
