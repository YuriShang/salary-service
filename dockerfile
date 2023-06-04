FROM python:3.10.11
WORKDIR /test_app
COPY . /test_app
RUN curl -sSL https://install.python-poetry.org | python3 - --git https://github.com/python-poetry/poetry.git@master
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN poetry --version
RUN poetry install
EXPOSE 8080
RUN chmod 755  docker-entrypoint.sh
ENV PYTHONPATH /test_app
ENTRYPOINT ["./docker-entrypoint.sh"]
