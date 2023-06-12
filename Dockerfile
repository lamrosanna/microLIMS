FROM python:3.9.6-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . . 
EXPOSE 8000:8000