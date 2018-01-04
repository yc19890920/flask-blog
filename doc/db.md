host=127.0.0.1
port=3306
user=fblog
passwd=123456
dbname=flaskblog

### 创建数据库
1. mysql数据库连接：
```
mysql -h 127.0.0.1 -u root -P 3306 -p
```

2. 创建数据库  flaskblog
```
CREATE DATABASE flaskblog DEFAULT CHARACTER SET UTF8;
-- CREATE schema flaskblog default character set utf8 collate utf8_general_ci;
```

3. 创建用户  dblog
```
create user 'fblog'@'%' identified by '123456';
```

4. 授权 fblog 用户拥有 flask-blog 数据库的所有权限。
```
GRANT ALL ON flaskblog.* TO 'fblog'@'%';
```

- 部分授权
```
GRANT SELECT, INSERT ON flaskblog.* TO 'fblog'@'%';
GRANT ALL ON . TO 'fblog'@'%';
```

5. 启用修改
```
flush  privileges;
```

### phpmyadmin
phpMyAdmin: http://192.168.181.129:88/phpmyadmin/


## 备份数据库
```
mysqldump -u fblog -P 3306 -p flaskblog > ~/git/flask-blog/doc/data.sql
```

## 数据还原
```
mysql -u root -p flaskblog < ~/git/flask-blog/doc/data.sql
```
