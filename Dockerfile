FROM python:3
COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENV TZ="America/Chicago"

RUN pip install gunicorn

COPY . /app
WORKDIR /app

RUN export PYTHONPATH=/app:$PYTHONPATH
RUN python setup.py install

ENTRYPOINT [ "python", "/app/test.py" ]
