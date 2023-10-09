#python version
FROM python:3.8.1
MAINTAINER Mosnoi Ion <moshnoi2000@gmail.com>

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 6017

CMD ["/bin/bash"]
# CMD ["python","app.py","6017"]
