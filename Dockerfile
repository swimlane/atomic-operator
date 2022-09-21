FROM python:3.9-alpine AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-root

# ---

FROM python:3.9-alpine
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

# For options, see https://boxmatrix.info/wiki/Property:adduser
#RUN adduser app -DHh ${WORKDIR} -u 1000
#USER 1000

# change this to match your application
#CMD /app/.venv/bin/python -m module_name
# or
CMD /app/.venv/bin/python test.py