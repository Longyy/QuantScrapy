import pymysql
from pymysql.cursors import DictCursor


class PymysqlUtil(object):
    __config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123456",
        "database": "scrapy",
        "autocommit": True
    }

    def __init__(self):
        self.db = self.__get_conn()

    def __get_conn(self):
        try:
            return pymysql.connect(**self.__config)
        except Exception as ex:
            print(ex)
            return None

    def get_one(self, sql):
        try:
            with self.db.cursor(cursor=DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception as ex:
            print(ex)
            return None

    def get_all(self, sql):
        try:
            with self.db.cursor(cursor=DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as ex:
            print(ex)
            return None

    def insert(self, sql, data):
        try:
            with self.db.cursor() as cursor:
                result = cursor.execute(sql, data)
                return result
        except Exception as ex:
            print(ex)
            return None

    def delete(self, sql, data):
        try:
            with self.db.cursor() as cursor:
                result = cursor.execute(sql, data)
                return result
        except Exception as ex:
            print(ex)
            return None

    def update(self):
        pass

    def close(self):
        self.db.close()

