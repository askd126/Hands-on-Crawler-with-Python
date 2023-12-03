# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-01 7:31
@Project  :   Hands-on Crawler with Python-pool
连接池
'''

import logging
import threading
import time
from queue import Queue, Empty

import pymysql

from .connection import Connection


class PoolError(Exception):
    '''连接池异常类'''
    pass


class PooledConnection:
    '''连接池类 '''

    def __init__(self, connection_config, max_count=5, min_free_count=1, ping_interval=300, keep_conn_alive=False,
                trace_sql=False, logger=None):
        self._connection_config = connection_config
        self._max_count = max_count
        self._min_free_count = min_free_count
        self._count = 0
        self._queue = Queue(max_count)
        self._lock = threading.Lock()
        self.trace_sql = trace_sql
        self._logger = logger if logger else logging.getLogger(__name__)
        if keep_conn_alive:
            self._ping_interval = ping_interval
            self._run_ping()

    def __del__(self):
        while self._queue._qsize() > 0:
            self._lock.acquire()
            try:
                conn_info = self._queue.get(block=False)
                conn = conn_info.get('connection') if conn_info else None
            except Empty:
                conn = None
            finally:
                self._lock.release()

            if conn:
                self._close_connection(conn)
            else:
                break

    def _run_ping(self):
        ''' 开启1个后台线程，定时ping连接池中的连接，保证连接池中的连接可用'''

        def ping_conn(pool_queue, pool_lock, ping_interval, logger):
            '''每隔默认5分钟检测连接池中未操作过的连接、进行ping操作，移除失效的连接'''
            while True:
                logger.debug(f'pool connection count:({self._count}/{pool_queue._qsize()})')
                while pool_queue._qsize() > 0:  # 使用Queue的_qsize()方法，防止队列里的lock与pool_lock造成死锁
                    conn = None
                    usable = True
                    pool_lock.acquire()
                    try:
                        conn_info = pool_queue.get(block=False)
                        if conn_info:
                            if time.time() - conn_info.get('active_time') > ping_interval:  # 连接上次活跃时间超过ping_interval
                                conn = conn_info.get('connection')
                                try:
                                    conn._conn.ping()
                                except:
                                    usable = False
                            else:  # 活跃时间未超过ping_interval
                                break  # 只要遇到连接的活跃时间未到ping时间，因为队列先入先出的特性，后面的连接活跃时间一定大于ping_interval，则可直接结束检测后面的连接
                    finally:
                        pool_lock.release()

                    if conn:  # 必须放在pool_lock.release()之后，避免在drop、release时出现死锁
                        if not usable:
                            conn.drop()
                        else:
                            conn.release()

                time.sleep(ping_interval)

        thread = threading.Thread(target=ping_conn, args=(self._queue, self._lock, self._ping_interval, self._logger),
                                  daemon=True)
        thread.start()

    def _create_connection(self, auto_commit=True):
        '''创建连接'''
        if self._count >= self._max_count:
            raise PoolError('Maximum number of connections exceeded!')
        self._logger.info('Creating MySQL connection start...')
        conn = Connection(
            self,
            self.trace_sql,
            self._logger,
            host=self._connection_config.get('host'),
            port=self._connection_config.get('port'),
            user=self._connection_config.get('user'),
            password=self._connection_config.get('password'),
            db=self._connection_config.get('database'),
            charset=self._connection_config.get('charset', 'utf8'),
            autocommit=auto_commit,
            cursorclass=pymysql.cursors.DictCursor
        )
        self._logger.info('Creating MySQL connection finished!')
        self._count += 1
        return conn

    def get_connection(self, timeout=15):
        '''获取1个连接'''
        start = time.time()

        def get_conn():
            '''获取连接'''
            self._lock.acquire()
            try:
                if self._queue._qsize() > 0:
                    try:
                        conn_info = self._queue.get(block=False)
                        conn = conn_info.get('connection') if conn_info else None
                    except Empty:
                        conn = None
                elif self._count < self._max_count:
                    conn = self._create_connection()
                else:
                    conn = None
                return conn
            except:
                raise
            finally:
                self._lock.release()

        conn = get_conn()
        if conn:
            return conn
        else:
            if timeout:
                while time.time() - start < timeout:
                    conn = get_conn()
                    if conn:
                        break
                    time.sleep(0.2)
            if not conn:
                raise PoolError('MySQL pool: get connection timeout, not enough connections are available(modify the maxConnections config maybe can fix it)!')
            return conn

    def release_connection(self, conn):
        '''释放连接'''
        self._lock.acquire()
        try:
            if self._queue._qsize() > self._min_free_count:
                self._close_connection(conn)
            else:
                self._queue.put({'connection': conn, 'active_time': time.time()})
        finally:
            self._lock.release()

    def _close_connection(self, conn):
        '''关闭连接'''
        try:
            if conn._close():
                self._count -= 1
        except Exception as e:
            self._logger.error(f'close connection error: {e}')
