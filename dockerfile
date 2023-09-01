FROM amazonlinux:latest

WORKDIR /root
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone 

RUN yum update -y && \
    yum install -y latexmk texlive texlive-latex texlive-xetex git python3-pip


# 从GitHub克隆项目
COPY ./src /root/autolatex

# 进入项目目录
WORKDIR /root/autolatex

RUN pip3 install --no-cache-dir -r requirements.txt

# 指定容器启动时运行的命令
CMD [ "python3", "main.py" ]
