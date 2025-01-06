# Use Python Alpine-based image for a lightweight base
FROM python:3.12.3-alpine3.20



# Set environment variables to optimize Python and configure Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies for Python and Django
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    libpq \
    bash \
    curl \
    git \
    openssh-client \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apk del curl \
    && pip install poetry \
    && pip install --upgrade pip \
    && mkdir -p "/app"

# Set working directory
WORKDIR ./app

COPY . .

# Install Poetry dependencies in a virtual environment
RUN poetry config virtualenvs.create true && poetry env use python
# Install dependencies using Poetry (runtime-only dependencies)
RUN poetry check && poetry install

RUN poetry run python manage.py collectstatic --no-input --clear

# Expose the app's port (default for Gunicorn/Django apps)
EXPOSE 8000

# Command to run the app using Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "cryptek.wsgi:application"]