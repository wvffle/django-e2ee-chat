# Build assets with node.js
FROM node:15-alpine AS builder

WORKDIR /app
COPY . .

RUN yarn install
RUN yarn build


# Run django app
FROM python:3-alpine AS production
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /app .

RUN apk add gcc g++ make libffi-dev openssl-dev python3-dev build-base linux-headers zlib-dev jpeg-dev musl-dev cargo
RUN pip install "poetry==1.0.0"
RUN poetry install --no-dev --no-root
RUN poetry run python manage.py migrate

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]
