# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-30 21:57
@Project  :   Hands-on Crawler with Python-connection
MySQL连接
'''

import logging
import uuid

import pymysql


class SQLExecutionError(Exception):
    '''自定义SQL执行异常'''
    pass


class Connection:
    '''连接类'''

    def __init__(self, pool, trace_sql=False, logger=None, *args, **kwargs):
        self._pool = pool  # 连接池
        self.id = uuid.uuid4()  # 连接ID
        self._logger = logger if logger else logging.getLogger(__name__)  # 日志
        self._trace_logger = self.__create_trace_logger() if trace_sql else None  # 跟踪日志
        self.transaction_id = None  # 事务ID

        # 尝试连接数据库
        try:
            self._conn = pymysql.Connection(*args, **kwargs)
            self.__is_closed = False
        except pymysql.err.OperationalError:  # 连接不上时，自动重试
            self._conn = pymysql.Connection(*args, **kwargs)
            self.__is_closed = False

    def __del__(self):
        '''销毁连接'''
        self.drop()

    def __create_trace_logger(self):
        '''创建MySQL跟踪日志'''
        LOG_NAME = 'mysql.log'  # 日志文件名
        logger = logging.getLogger()  # 创建一个logger对象
        logger.setLevel(logging.INFO)  # 设置日志级别为INFO
        formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - %(pathName)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 创建一个格式化器
        console_handler = logging.StreamHandler()  # 创建一个输出到控制台的日志处理器
        console_handler.setFormatter(formatter)  # 设置日志处理器的格式化器为之前创建的格式化器
        logger.addHandler(console_handler)  # 将日志处理器添加到logger对象中
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_NAME,  # 日志文件名
            maxBytes=1024 * 1024 * 10,  # 最大文件大小
            backupCount=5,  # 备份文件数量
            encoding='utf-8'  # 编码方式
        )
        file_handler.setFormatter(formatter)  # 设置日志处理器的格式化器为之前创建的格式化器
        logger.addHandler(file_handler)  # 将日志处理器添加到logger对象中
        return logger  # 返回logger对象

    def set_transaction_id(self, transaction_id):
        '''设置事务ID'''
        self.transaction_id = transaction_id

    def execute(self, sql, args=None):
        '''执行SQL语句'''
        cursor = self._conn.cursor()
        if self._trace_logger:
            self._trace_logger.debug({'SQL': sql, 'ARGS': args, 'TRANSACTION_ID': self.transaction_id})
        cursor.execute(sql, args)
        return cursor

    def insert(self, sql, args=None):
        '''插入数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_id = cursor.lastrowid
                return row_id
            else:
                raise SQLExecutionError(f'SQL Error: {sql}')
        except:
            raise  # 直接向上层继续抛出try块中发生并抛出的异常
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        '''更新数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_count = cursor.rowcount

                if not row_count:
                    self._logger.debug(cursor._last_executed)

                return row_count
            else:
                raise SQLExecutionError(f'SQL Error: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def delete(self, sql, args=None):
        '''删除数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                row_count = cursor.rowcount
                return row_count
            else:
                raise SQLExecutionError(f'SQL Error: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def query(self, sql, args=None):
        '''查询数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.fetchall()
            else:
                raise SQLExecutionError(f'SQL Error: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def query_one(self, sql, args=None):
        '''查询1条数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.fetchone()
            else:
                raise SQLExecutionError(f'SQL Error: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def release(self):
        '''释放连接，将连接放回连接池'''
        self._pool.release_connection(self)

    def close(self):
        '''关闭连接，将连接放回连接池'''
        self.release()

    def drop(self):  ## ?
        '''丢弃连接'''
        self._pool._close_connection(self)

    def _close(self):
        '''真正关闭连接'''
        if self.__is_closed:
            return False
        try:
            self._conn.close()
            self.__is_closed = True
        except:
            self._logger.error('MySQL connection close error', exc_info=True)
        return True
