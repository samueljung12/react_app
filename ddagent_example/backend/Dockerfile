FROM python:3.9-slim
WORKDIR /flask_backend
COPY . .
RUN pip install -r ./requirements.txt

CMD ["ddtrace-run", "python3", "application.py"]