import pymysql.cursors

def conn_to_database():
    try:
        conn = pymysql.connect(
            # 
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f'Gagal terhubung ke database MySQL: {e}')
        return None
