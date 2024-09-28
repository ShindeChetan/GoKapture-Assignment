FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


COPY ./app /app/app

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
