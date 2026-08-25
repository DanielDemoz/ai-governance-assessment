FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
ENV NEXT_STATIC_EXPORT=true
ENV NEXT_PUBLIC_API_URL=
RUN npm run build

FROM python:3.11-slim AS runtime
WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend-build /app/frontend/out ./static

ENV APP_ENV=production
ENV DATABASE_URL=sqlite:///./data/assessments.db
ENV STATIC_DIR=./static
ENV CORS_ORIGINS=https://danieldemoz.github.io,http://localhost:3000

EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
