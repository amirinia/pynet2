From python:3-alpine3.12
MAINTAINER amirinia
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python","run.py"]