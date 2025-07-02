import pymysql
import datetime

# 数据库配置
DB_CONFIG_1 = {
    "host": "116.63.47.216",
    "user": "zhuzhenjin",
    "password": "plORmnE*KYnQRvF8",
    "database": "luyao"
}

DB_CONFIG_2 = {
    "host": "luyao.procoding.cn",
    "user": "root",
    "password": "2885368",
    "database": "luyao",
    "port": 12002
}

# 需要同步的表列表
TABLES = [
    "ods_amazon_product_data",
    "ods_keepa",
    "ods_daughter_sales",
    "ods_market_average_price"
]

def get_table_columns(conn, table_name):
    """获取表的所有列名（排除id列）"""
    with conn.cursor() as cursor:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [col[0] for col in cursor.fetchall() if col[0].lower() != 'id']
    return columns

def sync_table(source_conn, target_conn, table_name):
    """同步单个表的数据"""
    print(f"\n开始同步表: {table_name}")
    
    # 获取目标数据库最大batch
    with target_conn.cursor() as cursor:
        cursor.execute(f"SELECT MAX(batch) FROM {table_name}")
        max_batch = cursor.fetchone()[0]
    
    # 处理无数据情况
    if max_batch is None:
        max_batch = "000000000000"
        print("目标表无数据，将同步所有数据")
    else:
        print(f"目标表最大batch: {max_batch}")
    
    # 获取列名（排除id）
    columns = get_table_columns(source_conn, table_name)
    col_str = ", ".join(columns)
    
    # 查询源数据库数据
    with source_conn.cursor() as cursor:
        query = f"SELECT {col_str} FROM {table_name} WHERE batch > %s"
        cursor.execute(query, (max_batch,))
        rows = cursor.fetchall()
    
    # 插入目标数据库
    if not rows:
        print("没有需要同步的新数据")
        return 0
    
    print(f"找到 {len(rows)} 条新数据，开始插入...")
    
    with target_conn.cursor() as cursor:
        placeholders = ", ".join(["%s"] * len(columns))
        insert_sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, rows)
        target_conn.commit()
    
    print(f"成功插入 {cursor.rowcount} 条数据")
    return cursor.rowcount

def main():
    print(f"开始数据同步 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print("=" * 50)
    
    # 建立数据库连接
    source_conn = pymysql.connect(**DB_CONFIG_1)
    target_conn = pymysql.connect(**DB_CONFIG_2)
    
    total_synced = 0
    try:
        for table in TABLES:
            synced = sync_table(source_conn, target_conn, table)
            total_synced += synced
    finally:
        source_conn.close()
        target_conn.close()
    
    print("\n" + "=" * 50)
    print(f"同步完成! 总共同步 {total_synced} 条记录")
    print(f"结束时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()