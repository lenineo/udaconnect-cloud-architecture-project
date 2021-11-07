FROM python:3.7-alpine

WORKDIR /app
COPY . .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

RUN pip install -r requirements.txt

EXPOSE 5005

ENTRYPOINT ["python", "app.py"]