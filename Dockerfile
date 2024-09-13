FROM python:3.11-slim

ARG WORK_SPACE=/workspace
WORKDIR ${WORK_SPACE}
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:${WORK_SPACE}

RUN python -m pip install --upgrade pip
COPY requirements.txt ${WORK_SPACE}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY lib ${WORK_SPACE}/lib
COPY templates ${WORK_SPACE}/templates
COPY main.py ${WORK_SPACE}/main.py

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "-k", "gevent", "--worker-connections=100"]