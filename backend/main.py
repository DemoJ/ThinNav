import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ 创建一个数据库连接到SQLite数据库指定的db文件 """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ 使用提供的conn连接和create_table_sql语句创建一个表 """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"./backend/db/data.db"

    sql_create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        id integer PRIMARY KEY,
        name text NOT NULL,
        icon_url text
    );
    """

    sql_create_websites_table = """
    CREATE TABLE IF NOT EXISTS websites (
        id integer PRIMARY KEY,
        category_id integer NOT NULL,
        name text NOT NULL,
        icon_url text,
        description text,
        url text NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
    """

    # 创建数据库连接
    conn = create_connection(database)

    # 创建表
    if conn is not None:
        # 创建 categories 表
        create_table(conn, sql_create_categories_table)

        # 创建 websites 表
        create_table(conn, sql_create_websites_table)

        # 关闭连接
        conn.close()
    else:
        print("无法创建数据库连接。")

if __name__ == '__main__':
    main()
