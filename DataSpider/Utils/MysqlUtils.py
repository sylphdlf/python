# encoding=utf-8
import pymysql as pymysql
from Utils import RedisUtils

redis_ = RedisUtils.get_conn()


class MysqlUtils:

    @staticmethod
    def get_connection():
        user = redis_.get("mysql_user")
        password = redis_.get("mysql_password")
        print(user, password)
        conn = pymysql.connect(host='118.25.197.159', user=user, password=password, database='cloud')
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def insert(sql_list):
        conn, cursor = MysqlUtils.get_connection()
        try:
            if len(sql_list) != 0:
                for index, sql in enumerate(sql_list):
                    print(sql)
                    cursor.execute(sql)
                    # if index % 10 == 0:
                    conn.commit()
            cursor.close()
        except Exception as e:
            print(e)
        finally:
            cursor.close()