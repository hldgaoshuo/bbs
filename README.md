# bbs
基于 Flask 的论坛 

#### 地址

[https://hldgaohsuo.xyz](https://hldgaohsuo.xyz)

测试账号：shuo

密码：123

#### 功能

- 用户板块包括用户的注册、登录、密码找回、主页与信息管理。
- 论坛板块包括不同板块帖子的编辑、发布、删除和评论。
- 私信板块包括站内信及其邮件通知与评论中的 @ 功能及其邮件提醒。
- 支持系统中数据的批量管理。

#### 要点

- Gunicorn 充当应用服务器，通过多工作进程实现负载均衡，并搭配 gevent 协程并发处理请求。
- 利用 MySQL 实现数据持久化、Redis 实现多进程间的数据共享、Celery 处理站内信的邮件发送。
- 使用摘要算法与盐的组合保证用户密码的安全性。
- 利用服务端 Session 替换 Flask 内置 Session。
- 通过后端转义防范跨站执行脚本（XSS，cross site script）攻击。
- 利用 Token 防范跨站请求伪造（XSRF，cross site request forgery）攻击。

#### 部署与管理

- 部署环境选择 Ubuntu18.04。
- 通过 Systemd 管理服务。
- 通过云服务器的硬件防火墙与 Ubutu 内置的软件防火墙来锁死端口，提高安全性。
- 利用 shell 脚本实现一键部署。
- Nginx 配置了HTTPS加密传输，反向代理，静态资源请求处理以及多类型文件压缩标准。

