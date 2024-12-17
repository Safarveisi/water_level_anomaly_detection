FROM python:3.9.1-slim

ENV user=ssafarveiei

RUN useradd -m -d /home/${user} ${user} && \
    chown -R ${user} /home/${user}

USER ${user}
WORKDIR /home/${user}

ENV PATH=/home/${user}/.local/bin:$PATH

COPY  poetry.toml poetry.lock pyproject.toml ./

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

EXPOSE 8502