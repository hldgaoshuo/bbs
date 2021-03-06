# 在 Dockerfile 文件中 # 是注释
# FROM 用于指定构建镜像使用的基础镜像
FROM ubuntu:18.04


# RUN 用于在构建镜像的时候在镜像中执行命令
# 这里我们安装 python3 和 flask web 框架
# 使用阿里云的 apt 源
COPY sources.list /etc/apt/sources.list
RUN apt update
RUN apt -y install python3 python3-pip
# 使用阿里云的 pip 源
COPY pip.conf /etc/pip.conf
RUN pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_admin flask_mail marrow.mailer redis Celery


# WORKDIR 用于指定从镜像启动的容器内的工作目录
WORKDIR /code


# CMD 用于指定容器运行后要执行的命令和参数列表
# 这样从本镜像启动容器后会自动执行 python3 app.py 这个命令
#
# 由于我们已经用 WORKDIR 指定了容器的工作目录
# 所以下面的命令都是在 /code 下执行的
CMD ["python3", "app.py"]

# 你可能会看到有资料介绍一个 ENTRYPOINT 参数用于指定容器运行后的入口程序
# 但是这个参数在现在的意义已经很小了，请忽略之
