# Base python image
FROM python:3.9-slim AS python-base


# Disables buffering
ENV PYTHONUNBUFFERED=1 \
    # Prevents Python from creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # Disables the cache
    PIP_NO_CACHE_DIR=off \
    # Don't check for new versions of pip to download
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    # This is where poetry is installed
    POETRY_HOME=/opt/poetry \
    # Creates a virtual env dir (.venv) in the project root dir
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH=/opt/pysetup \
    VENV_PATH=/opt/pysetup/.venv

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder-base

# Dependencies for poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project requirement files here to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --without dev


FROM python-base AS serve

# Create a non-root user and group (necessary for Streamlit to function properly)
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Switch to the new user
USER appuser
WORKDIR /home/appuser

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY water_level_anomaly_detection/ ./

EXPOSE 8501

CMD [ "streamlit", "run", "app.py" ]