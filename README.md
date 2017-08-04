# web.py 注册登录系统



## 流程
使用 [你会做WEB上的用户登录功能吗？](http://coolshell.cn/articles/5353.html) 记录的用户登录机制.

## 注意
- 项目使用 **web.py 0.40**开发版, **debian** 系统可以使用 `sudo pip3 install web.py==0.40.dev0` 命令安装.
- 使用 **python 3** 需要修改 **/dist-packages/web/db.py**文件, 将`import MySQLdb as db` 修改为 `import pymysql as db`

## LICENSE
MIT