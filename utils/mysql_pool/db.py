# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-02 23:42
@Project  :   Hands-on Crawler with Python-db
'''

import logging
import uuid

import pymysql

from .connection import SQLExecutionError
from .pool import PooledConnection


class Transaction:
    '''事务类'''

    def __init__(self, conn):
        self.__is_began = False
        self.conn = conn
        self.__old_autocommit = self.conn._conn.get_autocommit()
        self.conn._conn.autocommit(False)
        self.id = None

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

    def begin(self):
        '''开启事务'''
        if not self.__is_began:
            self.conn._conn.begin()
            self.__is_began = True
            self.id = str(uuid.uuid1())
            self.conn.set_transaction_id(self.id)

    def commit(self):
        '''提交事务'''
        try:
            self.conn._conn.commit()
        except:
            self.conn._conn.rollback()
            raise
        finally:
            self._end()

    def rollback(self):
        '''回滚事务'''
        try:
            self.conn._conn.rollback()
        finally:
            self._end()

    def __reset_autocommit(self):
        '''重置自动提交为原来的设置'''
        self.conn._conn.autocommit(self.__old_autocommit)

    def _end(self):
        '''结束事务'''
        self.__is_began = False
        self.__reset_autocommit()
        self.conn.set_transaction_id(None)
        self.conn.release()


class MySQLDB:
    '''MySQL数据库操作类，支持连接池'''

    def __init__(self, config, logger=None):
        self.config = config
        self._pool = PooledConnection(
            self.config,
            self.config.get('maxConnections'),
            self.config.get('minFreeConnections', 1),
            self.config.get('pingInterval'),
            self.config.get('keepConnectionAlive'),
            self.config.get('traceSql', False),
            logger
        )
        self.logger = logger if logger else logging.getLogger(__name__)

    def execute(self, sql, args=None):
        '''执行SQL语句'''
        cursor = None
        conn = None
        try:
            try:
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
            except (pymysql.err.OperationalError, RuntimeError):
                self.logger.warning('Execution error ready to retry', exc_info=True)
                conn and conn.drop()
                conn = self._pool.get_connection()
                cursor = conn.execute(sql, args)
        except:
            self.logger.error('MySQL execution error', exc_info=True)
            conn and conn.drop()
            conn = None
            raise
        finally:
            conn and conn.release()

        return cursor

    def insert(self, sql, args=None):
        '''插入数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.lastrowid
            else:
                raise SQLExecutionError(f'Insert failed: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def update(self, sql, args=None):
        '''更新数据'''
        cursor = None
        try:
            cursor = self.execute(sql, args)
            if cursor:
                return cursor.rowcount
            else:
                raise SQLExecutionError(f'Update failed: {sql}')
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
                raise SQLExecutionError(f'Query failed: {sql}')
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
                raise SQLExecutionError(f'Query failed: {sql}')
        except:
            raise
        finally:
            cursor and cursor.close()

    def begin(self):
        '''开始1个事务并返回'''
        transaction = Transaction(self._pool.get_connection())
        transaction.begin()
        return transaction

    def commit(self, transaction):
        '''提交事务'''
        transaction.commit()

    def rollback(self, transaction):
        '''回滚事务'''
        transaction.rollback()
