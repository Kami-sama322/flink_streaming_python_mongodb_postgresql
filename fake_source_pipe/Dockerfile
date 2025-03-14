FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip; \
    pip install -r ./requirements.txt


CMD ["python", "mongo_pipe.py"]
