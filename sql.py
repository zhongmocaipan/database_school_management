import pymysql

# 连接到数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='school_management',
    cursorclass=pymysql.cursors.DictCursor
)

# 使用连接执行 SQL 查询或其他操作
try:
    with connection.cursor() as cursor:
        # 示例：执行 SQL 查询
        sql = "SELECT * FROM students"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
finally:
    # 关闭数据库连接
    connection.close()