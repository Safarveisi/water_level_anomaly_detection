FROM python:3.9-slim

ENV user=developer

RUN useradd -m -d /home/${user} ${user} && \
    chown -R ${user} /home/${user} && \
    apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

USER ${user}
WORKDIR /home/${user}

ENV PATH=/home/${user}/.local/bin:$PATH

COPY pyproject.toml poetry.lock water_level_anomaly_detection/ ./

# Install poetry (package mode: FALSE)
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry install --no-root

EXPOSE 8501

ENTRYPOINT [ "poetry", "run", "streamlit", "run", "app.py" ]