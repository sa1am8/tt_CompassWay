FROM python:3.12-slim

RUN python -m pip install -U pip

RUN adduser -uid 2001 app
USER app
WORKDIR /home/app

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

RUN pip install --user poetry
ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app poetry.lock .
COPY --chown=app:app poetry.toml .
COPY --chown=app:app pyproject.toml .

RUN poetry install --only main --no-interaction --no-ansi
ENV PATH="/home/app/.venv/bin:${PATH}"

COPY --chown=app:app . .

RUN poetry run python manage.py collectstatic --noinput

RUN poetry add gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "loan_schedule.wsgi:application"]

EXPOSE 8000
