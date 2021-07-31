# Using Python 3.8 Base docker image
FROM python:3.8-slim 
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt 
CMD ["python3","main.py"]