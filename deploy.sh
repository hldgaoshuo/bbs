#!/usr/bin/env bash
# 1. 拉代码到 /var/www/web19
# 2. 执行 bash deploy.sh

set -ex

# 系统设置
apt-get install -y curl ufw
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 465
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# redis 需要 ipv6
sysctl -w net.ipv6.conf.all.disable_ipv6=0

# 安装过程中选择默认选项，这样不会弹出 libssl 确认框
export DEBIAN_FRONTEND=noninteractive

# 装依赖
apt-get install -y git nginx python3-pip mysql-server redis-server apache2-utils
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_admin flask_mail marrow.mailer redis Celery

# 删除测试用户和测试数据库
# 删除测试用户和测试数据库并限制关闭公网访问
mysql -u root -pzaoshuizaoqi -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root -pzaoshuizaoqi -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -u root -pzaoshuizaoqi -e "DROP DATABASE IF EXISTS test;"
mysql -u root -pzaoshuizaoqi -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"

# 设置密码并切换成密码验证
mysql -u root -pzaoshuizaoqi -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'zaoshuizaoqi';"

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 不要再 sites-available 里面放任何东西
cp /var/www/web19/web19.nginx /etc/nginx/sites-enabled/web19
chmod -R o+rwx /var/www/web19

cp web19.service /etc/systemd/system/web19.service
cp web19-message-queue.service /etc/systemd/system/web19-message-queue.service

# 初始化
cd /var/www/web19
python3 reset.py

# 重启服务器
systemctl daemon-reload
systemctl restart web19
systemctl restart web19-message-queue
systemctl restart nginx

echo 'succsss'
echo 'ip'
hostname -I
