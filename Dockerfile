FROM python:3.11.9

WORKDIR /app

COPY . .

RUN pip install -U pip
RUN pip install setuptools
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "api/app.py", "--port", "80", "--workers", "1"]
