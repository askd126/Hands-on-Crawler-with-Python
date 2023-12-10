# MySQL基本操作
基于Docker安装和运行MySQL步骤：
```bash
docker run --name mysql -p 3306:3306 -v E:\Docker\data\mysql\conf:/etc/mysql/conf.d -v E:\Docker\data\mysql\logs:/var/log/mysql -v E:\Docker\data\mysql\data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql
```
## 1.数据库操作
创建数据库：
```sql
CREATE DATABASE test CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';
```
输出：
```sql
Query OK, 1 row affected (0.02 sec)
```

删除数据库：
```sql
DROP DATABASE test;
```
输出：
```sql
Query OK, 0 rows affected (0.01 sec)
```

查看数据库列表：
```sql
CREATE DATABASE question_answer CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';
SHOW DATABASES;
```
输出：
```sql
Query OK, 1 row affected (0.02 sec)

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| question_answer    |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

选择数据库：
```sql
USE question_answer;
```
输出：
```sql
Database changed
```

## 2.表操作
创建表：
```sql
CREATE TABLE answer (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '回答id',
	user_id INT NOT NULL DEFAULT 0 COMMENT '用户id',
	question_id INT NOT NULL DEFAULT 0 COMMENT '问题id',
	answer_summary VARCHAR ( 100 ) NOT NULL DEFAULT '' COMMENT '回答摘要',
	answer_detail TEXT NOT NULL COMMENT '回答详情',
	review TEXT NOT NULL COMMENT '评论',
	created_time INT NOT NULL COMMENT '创建时间',
	updated_time INT NOT NULL COMMENT '更新时间',
	is_deleted TINYINT ( 1 ) NOT NULL DEFAULT 0 COMMENT '是否删除',
KEY idx_user_id ( user_id )
) ENGINE = INNODB DEFAULT CHARSET = utf8 COMMENT = '回答';
```
输出：
```sql
Query OK, 0 rows affected, 1 warning (0.09 sec)
```

删除表：
```sql
CREATE TABLE question (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '问题id',
	user_id INT NOT NULL DEFAULT 0 COMMENT '用户id',
	question_title VARCHAR ( 100 ) NOT NULL DEFAULT '' COMMENT '问题标题',
	question_summary VARCHAR ( 100 ) NOT NULL DEFAULT '' COMMENT '问题摘要',
	question_detail TEXT NOT NULL COMMENT '问题详情',
	created_time INT NOT NULL COMMENT '创建时间'
);
SHOW TABLES;
DROP TABLE question;
SHOW TABLES;
```
输出：
```sql
Query OK, 0 rows affected (0.03 sec)

+---------------------------+
| Tables_in_question_answer |
+---------------------------+
| answer                    |
| question                  |
+---------------------------+
2 rows in set (0.01 sec)

Query OK, 0 rows affected (0.03 sec)

+---------------------------+
| Tables_in_question_answer |
+---------------------------+
| answer                    |
+---------------------------+
1 row in set (0.00 sec)
```

## 3.数据操作
插入数据：
```sql
INSERT INTO answer (user_id, question_id, answer_summary, answer_detail, review, created_time, updated_time, is_deleted) VALUES (1, 1, '这是回答摘要', '这是回答详情', '这是评论', UNIX_TIMESTAMP(NOW()), UNIX_TIMESTAMP(NOW()), 0);
```
输出：
```sql
Query OK, 1 row affected (0.01 sec)
```

查询数据（全部字段）：
```sql
SELECT * FROM answer;
```
输出：
```sql
+----+---------+-------------+----------------+---------------+----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary | answer_detail | review   | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------+---------------+----------+--------------+--------------+------------+
|  1 |       1 |           1 | 这是回答摘要   | 这是回答详情  | 这是评论 |   1701186793 |   1701186793 |          0 |
+----+---------+-------------+----------------+---------------+----------+--------------+--------------+------------+
1 row in set (0.04 sec)
```
查询数据（指定字段）：
```sql
SELECT answer_summary, answer_detail, review, created_time, updated_time FROM answer;
```
输出：
```sql
+----------------+---------------+----------+--------------+--------------+
| answer_summary | answer_detail | review   | created_time | updated_time |
+----------------+---------------+----------+--------------+--------------+
| 这是回答摘要   | 这是回答详情  | 这是评论 |   1701186793 |   1701186793 |
+----------------+---------------+----------+--------------+--------------+
1 row in set (0.03 sec)
```

插入多条数据：
```sql
INSERT INTO answer ( user_id, question_id, answer_summary, answer_detail, review, created_time, updated_time, is_deleted )
VALUES
	( 1, 1, '这是回答摘要2', '这是回答详情2', '这是评论2', UNIX_TIMESTAMP( NOW()), UNIX_TIMESTAMP( NOW()), 0 ),
	( 1, 2, '这是回答摘要3', '这是回答详情3', '这是评论3', UNIX_TIMESTAMP( NOW()), UNIX_TIMESTAMP( NOW()), 0 );
```

where子句：
```sql
SELECT * FROM answer WHERE user_id = 1;
```
输出：
```sql
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary | answer_detail | review    | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
|  1 |       1 |           1 | 这是回答摘要   | 这是回答详情  | 这是评论  |   1701186793 |   1701186793 |          0 |
|  3 |       1 |           2 | 这是回答摘要3  | 这是回答详情3 | 这是评论3 |   1701347569 |   1701347569 |          0 |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
2 rows in set (0.06 sec)
```

like子句：
```sql
SELECT * FROM answer WHERE answer_summary LIKE '%回答%';
```
输出：
```sql
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary | answer_detail | review    | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
|  1 |       1 |           1 | 这是回答摘要   | 这是回答详情  | 这是评论  |   1701186793 |   1701186793 |          0 |
|  2 |       2 |           3 | 这是回答摘要2  | 这是回答详情2 | 这是评论2 |   1701347446 |   1701347446 |          0 |
|  3 |       1 |           2 | 这是回答摘要3  | 这是回答详情3 | 这是评论3 |   1701347569 |   1701347569 |          0 |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
3 rows in set (0.07 sec)
```

order by排序：
```sql
SELECT * FROM answer ORDER BY created_time DESC;
```
输出：
```sql
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary | answer_detail | review    | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
|  3 |       1 |           2 | 这是回答摘要3  | 这是回答详情3 | 这是评论3 |   1701347569 |   1701347569 |          0 |
|  2 |       2 |           3 | 这是回答摘要2  | 这是回答详情2 | 这是评论2 |   1701347446 |   1701347446 |          0 |
|  1 |       1 |           1 | 这是回答摘要   | 这是回答详情  | 这是评论  |   1701186793 |   1701186793 |          0 |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
3 rows in set (0.08 sec)
```

update语句：
```sql
UPDATE answer SET answer_summary = '这是修改后的回答摘要' WHERE id = 1;

select * from  answer;
```
输出：
```sql
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

+----+---------+-------------+----------------------+---------------+-----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary       | answer_detail | review    | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------------+---------------+-----------+--------------+--------------+------------+
|  1 |       1 |           1 | 这是修改后的回答摘要 | 这是回答详情  | 这是评论  |   1701186793 |   1701186793 |          0 |
|  2 |       2 |           3 | 这是回答摘要2        | 这是回答详情2 | 这是评论2 |   1701347446 |   1701347446 |          0 |
|  3 |       1 |           2 | 这是回答摘要3        | 这是回答详情3 | 这是评论3 |   1701347569 |   1701347569 |          0 |
+----+---------+-------------+----------------------+---------------+-----------+--------------+--------------+------------+
3 rows in set (0.09 sec)
```

delete语句：
```sql
DELETE FROM answer WHERE id = 1;

select * from  answer;
```
输出：
```sql
Query OK, 1 row affected (0.01 sec)

+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
| id | user_id | question_id | answer_summary | answer_detail | review    | created_time | updated_time | is_deleted |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
|  2 |       2 |           3 | 这是回答摘要2  | 这是回答详情2 | 这是评论2 |   1701347446 |   1701347446 |          0 |
|  3 |       1 |           2 | 这是回答摘要3  | 这是回答详情3 | 这是评论3 |   1701347569 |   1701347569 |          0 |
+----+---------+-------------+----------------+---------------+-----------+--------------+--------------+------------+
2 rows in set (0.08 sec)
```